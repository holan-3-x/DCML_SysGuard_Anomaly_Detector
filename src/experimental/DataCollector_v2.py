"""
DataCollector_v2.py: Industrial-grade high-fidelity telemetry engine.
Uses differential logic to convert cumulative OS counters into stable rates.
Optimized for MacBook Pro M4 Pro.
"""
import csv
import os
import time
import psutil
import json
import random
import pandas as pd
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent)) # Add src/ to path
from Simulator import BaseSimulator

# Global cache for rate calculation
_prev_stats = {
    'time': time.time(),
    'disk': None,
    'net': None
}

def monitor_system_v2() -> dict:
    """
    Advanced monitoring with differential rate calculation.
    """
    global _prev_stats
    now = time.time()
    dt = now - _prev_stats['time']
    if dt <= 0: dt = 0.001 
    
    # 1. CPU Metrics (Already Rates/Percentages)
    cpu_percent = psutil.cpu_percent(interval=None, percpu=True)
    
    # 2. Memory Metrics (Absolute & Percentages)
    mem = psutil.virtual_memory()
    swap = psutil.swap_memory()
    
    # 3. Disk I/O (Cumulative -> Rates)
    curr_disk = psutil.disk_io_counters()
    disk_rates = {}
    if _prev_stats['disk'] and curr_disk:
        disk_rates['disk_read_speed'] = (curr_disk.read_bytes - _prev_stats['disk'].read_bytes) / dt
        disk_rates['disk_write_speed'] = (curr_disk.write_bytes - _prev_stats['disk'].write_bytes) / dt
        disk_rates['disk_read_count_rate'] = (curr_disk.read_count - _prev_stats['disk'].read_count) / dt
        disk_rates['disk_write_count_rate'] = (curr_disk.write_count - _prev_stats['disk'].write_count) / dt
    else:
        disk_rates = {'disk_read_speed': 0, 'disk_write_speed': 0, 'disk_read_count_rate': 0, 'disk_write_count_rate': 0}

    # 4. Network I/O (Cumulative -> Rates)
    curr_net = psutil.net_io_counters()
    net_rates = {}
    if _prev_stats['net'] and curr_net:
        net_rates['net_sent_speed'] = (curr_net.bytes_sent - _prev_stats['net'].bytes_sent) / dt
        net_rates['net_recv_speed'] = (curr_net.bytes_recv - _prev_stats['net'].bytes_recv) / dt
        net_rates['net_packets_sent_rate'] = (curr_net.packets_sent - _prev_stats['net'].packets_sent) / dt
        net_rates['net_packets_recv_rate'] = (curr_net.packets_recv - _prev_stats['net'].packets_recv) / dt
    else:
        net_rates = {'net_sent_speed': 0, 'net_recv_speed': 0, 'net_packets_sent_rate': 0, 'net_packets_recv_rate': 0}

    # Assemble Result
    data = {
        'Timestamp': now,
        'UserReadTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)),
    }
    
    # Add CPU
    for i, p in enumerate(cpu_percent):
        data[f'cpu_core_{i}_percent'] = p
    
    # Add MEM
    data['mem_percent'] = mem.percent
    data['mem_available'] = mem.available
    data['swap_percent'] = swap.percent
    
    # Add Disk & Net Rates
    data.update(disk_rates)
    data.update(net_rates)
    
    # Add connection count
    try:
        data['net_connections'] = len(psutil.net_connections())
    except:
        data['net_connections'] = 0

    # Update state
    _prev_stats['time'] = now
    _prev_stats['disk'] = curr_disk
    _prev_stats['net'] = curr_net
    
    return data

def main_v2(output_path: str = None, n_scenarios: int = 50):
    """
    Industrial sampling loop with random rest periods.
    """
    base_src = Path(__file__).parent.resolve()
    # Go one level up for config
    config_path = base_src.parent / 'simulation_config.json'
    
    with open(config_path) as f:
        config = json.load(f)
        scenarios = config.get('simulation_scenarios', [])

    # Expand scenarios to requested count
    target_list = []
    while len(target_list) < n_scenarios:
        target_list.append(random.choice(scenarios))
    random.shuffle(target_list)

    print(f"🚀 V2 Data Collection Started. Goal: {n_scenarios} scenarios.")
    print(f"Saving to: {output_path}")

    fieldnames = []
    first = True
    
    with open(output_path, 'w', newline='') as f:
        writer = None
        
        for idx, scenario_cfg in enumerate(target_list):
            # 1. REST PHASE (Clean baseline)
            rest_ticks = random.randint(15, 25)
            print(f"[{idx+1}/{n_scenarios}] Phase: REST ({rest_ticks} ticks)...")
            for _ in range(rest_ticks):
                row = monitor_system_v2()
                row['injector'] = 'rest'
                if first:
                    fieldnames = list(row.keys())
                    writer = csv.DictWriter(f, fieldnames=fieldnames)
                    writer.writeheader()
                    first = False
                writer.writerow(row)
                time.sleep(0.5)

            # 2. INJECTION PHASE
            sim = BaseSimulator.from_scenario(scenario_cfg)
            print(f"[{idx+1}/{n_scenarios}] Phase: INJECTING {sim.get_name()}...")
            sim.inject()
            
            # Record during injection
            inject_ticks = 15
            for _ in range(inject_ticks):
                row = monitor_system_v2()
                row['injector'] = sim.get_name()
                writer.writerow(row)
                time.sleep(0.5)
            
            f.flush()

    print(f"✅ V2 Data Collection Complete. Dataset: {output_path}")

if __name__ == '__main__':
    base_path = Path(__file__).parent.resolve()
    # Save to src/output_folder (parent/output_folder)
    out = base_path.parent / 'output_folder/monitored_data_v2.csv'
    main_v2(str(out), n_scenarios=40)
