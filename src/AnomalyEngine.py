"""
AnomalyEngine.py: Real-time security dashboard and inference engine.
Gathers live metrics and uses the best-trained AI model to detect potential threats.
"""
import datetime
import pathlib
import pandas as pd
import time
import sys
import psutil
import numpy as np
import os
from collections import deque
from DataCollector import monitor_system
from sklearn.preprocessing import StandardScaler
from joblib import load
import json
import threading
import sys
import select
from rich.console import Console
from rich.layout import Layout
from rich.panel import Panel
from rich.live import Live
from rich.table import Table
from rich.text import Text

console = Console()

def create_layout() -> Layout:
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="main"),
        Layout(name="footer", size=3)
    )
    layout["main"].split_row(
        Layout(name="left", ratio=2),
        Layout(name="right", ratio=1)
    )
    layout["left"].split_column(
        Layout(name="cpu", ratio=1),
        Layout(name="io", ratio=1)
    )
    layout["right"].split_column(
        Layout(name="status", ratio=1),
        Layout(name="graph", ratio=1)
    )
    return layout

def draw_bar(value, max_val=100, width=20):
    val = min(max(value, 0), max_val)
    done = int((val / max_val) * width)
    color = "red" if val > 80 else "yellow" if val > 50 else "green"
    return f"[{color}]{'█' * done}{'░' * (width - done)}[/] {value:>5.1f}%"

def draw_graph(history, width=30, height=8):
    if not history: return "No data"
    history_list = list(history)
    output = []
    # Normalize to 0-height
    # Ensure history is at least width long
    if len(history_list) < width:
        history_list = [0.0] * (width - len(history_list)) + history_list
    else:
        history_list = history_list[-width:]
    
    vals = [int(v * height) for v in history_list]
    
    for h in range(height, -1, -1):
        line = ""
        for v in vals:
            if v > h: line += "█"
            elif v == h: line += "▄"
            else: line += " "
        output.append(line)
    return "\n".join(output)
def identify_root_cause(X_scaled, features) -> str:
    """
    Sums absolute z-scores per category with heuristic weighting.
    """
    vals = np.abs(X_scaled[0])
    sums = {"CPU": 0.0, "MEMORY": 0.0, "DISK": 0.0, "NETWORK": 0.0}
    
    for i, name in enumerate(features):
        name = name.lower()
        v = vals[i]
        
        if 'virtual' in name or 'swap' in name or 'mem' in name:
            sums["MEMORY"] += v
        elif 'disk' in name:
            # Disk spikes are less common than CPU, favor them slightly less in tie-breakers
            sums["DISK"] += v * 0.8 
        elif 'net' in name:
            # Network is highly volatile, give it a lower weight to avoid false claims
            sums["NETWORK"] += v * 0.5
        else:
            # Core loads/times are direct evidence of CPU stress
            sums["CPU"] += v * 1.5 
            
    return max(sums, key=sums.get)

def check_keys(active_filters):
    """
    Non-blocking check for keypresses to toggle filters
    """
    if sys.stdin in select.select([sys.stdin], [], [], 0)[0]:
        key = sys.stdin.read(1).lower()
        if key == 'c': active_filters['CPU'] = not active_filters['CPU']
        elif key == 'r': active_filters['MEM'] = not active_filters['MEM']
        elif key == 'd': active_filters['DISK'] = not active_filters['DISK']
        elif key == 'n': active_filters['NET'] = not active_filters['NET']

def main(warning_threshold: int = 15, model_type: str = "best"):
    base_src = pathlib.Path(__file__).parent.resolve()
    
    # 0. Sensitivity Adjustment: Using a higher window and threshold for M4 Pro stability
    # If the user provides a threshold via CLI, we use it, otherwise use 15
    try:
        standard_scaler = load(str(base_src / 'standard_scaler.bin'))
        
        # Load leaderboard for info
        lb_path = base_src / 'analytics/leaderboard.json'
        leaderboard = {}
        if lb_path.exists():
            with open(lb_path) as f:
                leaderboard = json.load(f)

        # Dynamic Loading
        target_model_path = None
        model_name = "Custom Model"

        if model_type == "best":
            target_model_path = base_src / 'best_model.bin'
            model_name = "System Champion"
        elif (base_src / f'archive/{model_type}.bin').exists():
            target_model_path = base_src / f'archive/{model_type}.bin'
            model_name = f"{model_type} (Archived)"
        elif (base_src / f'{model_type}.bin').exists():
            target_model_path = base_src / f'{model_type}.bin'
            model_name = model_type
        
        if target_model_path and target_model_path.exists():
            model = load(str(target_model_path))
        else:
            # Fallback legacy check
            legacy_map = {"rf": "RandomForest", "mlp": "NeuralNetwork", "iso": "IsolationForest"}
            alt_name = legacy_map.get(model_type, model_type)
            if (base_src / f'archive/{alt_name}.bin').exists():
                model = load(str(base_src / f'archive/{alt_name}.bin'))
                model_name = alt_name
            else:
                raise FileNotFoundError(f"Model {model_type} or {alt_name} not found in archive/ or root.")
                
    except Exception as e:
        console.print(f"[red]Error loading system: {e}.[/red]")
        console.print("[yellow]Hint: Try 'RandomForest', 'NeuralNetwork', or 'IsolationForest' as the 2nd argument.[/yellow]")
        return

    warning_level = 0
    confidence_history = deque(maxlen=40)
    
    # Selective Monitoring Filters
    active_filters = {"CPU": True, "MEM": True, "DISK": True, "NET": True}
    root_cause = "NORMAL"
    
    layout = create_layout()
    
    # Prepare terminal for non-blocking keys
    import tty, termios
    old_settings = termios.tcgetattr(sys.stdin)
    tty.setcbreak(sys.stdin.fileno())

    try:
        # Open log files
        log_warn = open(base_src / "warnings.log", "a")
        log_raw = open(base_src / "raw_predictions.log", "a")

        with Live(layout, refresh_per_second=4, screen=True):
            while True:
                # 0. Check for filter toggles
                check_keys(active_filters)

                # 1. Capture Data
                raw_data = monitor_system()
                
                # 2. Preprocess (Scale only features seen during training)
                df = pd.DataFrame([raw_data])
                scaler_cols = standard_scaler.feature_names_in_
                # If new features are missing in the model, we filter them
                df_input = df[[c for c in scaler_cols if c in df.columns]]
                
                # If current df is missing features expected by scaler, fill with 0
                for col in scaler_cols:
                    if col not in df_input.columns:
                        df_input[col] = 0.0
                
                df_input = df_input[scaler_cols] # Ensure order
                X_scaled = standard_scaler.transform(df_input)
                
                # 3. Predict
                if hasattr(model, "predict_proba"):
                    pred = model.predict(X_scaled)[0]
                    is_anomaly = (pred == 1)
                    probs = model.predict_proba(X_scaled)[0]
                    prob = probs[1] 
                else:
                    pred = model.predict(X_scaled)[0]
                    is_anomaly = (pred == -1)
                    prob = 1.0 if is_anomaly else 0.0

                confidence_history.append(prob)
                root_cause = "CLEAN" if not is_anomaly else identify_root_cause(X_scaled, scaler_cols)

                # 4. Update Warning Logic (Sensitivity Smoothing + Selective Muting)
                # If the cause category is MUTED, we ignore the anomaly
                if is_anomaly:
                    if root_cause == "CPU" and not active_filters['CPU']: is_anomaly = False
                    elif root_cause == "MEMORY" and not active_filters['MEM']: is_anomaly = False
                    elif root_cause == "DISK" and not active_filters['DISK']: is_anomaly = False
                    elif root_cause == "NETWORK" and not active_filters['NET']: is_anomaly = False

                if is_anomaly and prob > 0.6: 
                    warning_level += 2
                elif is_anomaly: 
                    warning_level += 1
                else:
                    # Faster cooldown on rest to avoid long "false" alarms
                    warning_level = max(warning_level - 3, 0)

                # 4b. Logging
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                log_raw.write(f"{ts} | Model: {model_name} | Cause: {root_cause} | Conf: {prob:.4f} | Anomaly: {is_anomaly}\n")
                log_raw.flush()
                
                if warning_level > warning_threshold:
                    log_warn.write(f"[{ts}] CRITICAL: Anomaly detected! Cause: {root_cause} | Conf: {prob:.4f} | Threat Level: {warning_level}\n")
                    log_warn.flush()

                # 5. UI Updates
                layout["header"].update(Panel(
                    Text(f"🚀 M4 PRO HYPER-DETECTOR | {model_name} | {root_cause}", justify="center", style="bold white on blue")
                ))

                # 6. UI: CPU (Left Top)
                cpu_table = Table(box=None, expand=True, show_header=False)
                cpu_percents = psutil.cpu_percent(percpu=True)
                for i in range(0, len(cpu_percents), 2):
                    row = []
                    row.append(f"C{i:02d}: {draw_bar(cpu_percents[i], width=12)}")
                    if i+1 < len(cpu_percents):
                        row.append(f"C{i+1:02d}: {draw_bar(cpu_percents[i+1], width=12)}")
                    cpu_table.add_row(*row)
                cpu_title = f"CPU Performance [{'GREEN' if active_filters['CPU'] else 'RED'}]"
                layout["cpu"].update(Panel(cpu_table, title=cpu_title, border_style="green" if active_filters['CPU'] else "dim"))

                # 7. UI: IO & Storage (Left Bottom)
                io_table = Table(box=None, expand=True, show_header=False)
                mem = psutil.virtual_memory()
                disk = psutil.disk_usage('/')
                disk_io = psutil.disk_io_counters()
                net_io = psutil.net_io_counters()
                
                io_table.add_row("RAM:", draw_bar(mem.percent, width=30))
                io_table.add_row("Disk:", draw_bar(disk.percent, width=30))
                io_table.add_row("Disk R/W:", f"[cyan]{disk_io.read_bytes/1e6:,.1f}MB[/] / [magenta]{disk_io.write_bytes/1e6:,.1f}MB[/]")
                io_table.add_row("Net S/R:", f"[green]{net_io.bytes_sent/1e6:,.1f}MB[/] / [yellow]{net_io.bytes_recv/1e6:,.1f}MB[/]")
                
                io_title = f"RAM / IO / NET [{'GREEN' if all([active_filters['MEM'], active_filters['DISK'], active_filters['NET']]) else 'YELLOW'}]"
                layout["io"].update(Panel(io_table, title=io_title))

                # 8. UI: Status (Right Top)
                status_style = "bold blink white on red" if warning_level > warning_threshold else "bold green"
                status_text = "⚠️ ANOMALY ⚠️" if warning_level > warning_threshold else "🛡️ SECURE"
                
                status_panel = Text("\n" * 1, justify="center")
                status_panel.append(f"{status_text}\n\n", style=status_style)
                status_panel.append(f"Threat Level: {warning_level}\n", style="bold yellow" if is_anomaly else "white")
                status_panel.append(f"Cause: {root_cause}\n", style="bold magenta" if is_anomaly else "dim")
                status_panel.append(f"Conf: {prob:.1%}", style="dim")
                
                layout["status"].update(Panel(status_panel, title="Security Status", border_style="red" if is_anomaly else "green"))

                # 9. UI: Graph (Right Bottom)
                graph_text = Text(draw_graph(confidence_history, width=35, height=8), style="cyan")
                layout["graph"].update(Panel(graph_text, title="Confidence History"))

                # 10. UI: Footer
                layout["footer"].update(Panel(
                    Text(f"Toggles: [C]PU [R]am [D]isk [N]et | Press Ctrl+C to Stop", justify="center", style="bold cyan")
                ))

                time.sleep(0.3)

    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)
        if 'log_warn' in locals() and not log_warn.closed:
            log_warn.close()
        if 'log_raw' in locals() and not log_raw.closed:
            log_raw.close()

if __name__ == '__main__':
    # Usage: AnomalyEngine.py [threshold] [model_name]
    # Example: AnomalyEngine.py 15 best
    # Example: AnomalyEngine.py 20 RandomForest
    thresh = 20
    m_type = "best"
    if len(sys.argv) > 1: thresh = int(sys.argv[1])
    if len(sys.argv) > 2: m_type = sys.argv[2]
    
    try:
        main(thresh, m_type)
    except KeyboardInterrupt:
        pass
