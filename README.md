# 🚀 M4 Pro Hyper-Detector

An industrial-grade anomaly detection system specifically optimized for **MacBook Pro M4 Pro**. This system uses multi-threaded performance simulators and high-frequency monitoring to train AI models that can distinguish between "Normal" system states and "Anomalous" stress conditions.

## 💻 System Compatibility
- **Hardware**: Specifically optimized for **Apple M4 Pro** (14 CPU cores).
- **RAM**: 24GB+ recommended (Simulators use NumPy for aggressive allocation).
- **OS**: macOS Sequoia+ (using custom ARM-native busy-loops).

---

## 🛠️ Setup Instructions

### 1. Create Virtual Environment
```bash
python3 -m venv .venv
```

### 2. Install Dependencies
```bash
./.venv/bin/pip install -r requirements.txt
```

---

## 📊 Deployment Workflow

### Step 1: Data Acquisition
Collect baseline performance data and simulated anomalies.
```bash
./.venv/bin/python3 src/DataCollector.py
```
*Creates: `src/output_folder/monitored_data.csv`*

### Step 2: AI Model Engineering
Benchmarking 13+ architectures (Supervised/Unsupervised).
```bash
./.venv/bin/python3 src/ModelTrainer.py
```
*Creates: All models in `src/archive/` (as .bin) and visual leaderboard in `src/analytics/`*

# Deployment (Real-time Dashboard)
```bash
./.venv/bin/python3 src/AnomalyEngine.py 15 best
```
### Dashboard Interactive Keys:
- **`C`**: Toggle CPU Muting
- **`R`**: Toggle RAM Muting
- **`D`**: Toggle Disk Muting
- **`N`**: Toggle Network Muting
*Use these to "shutdown" detection for parts of the system.*

### Step 4: Verification (Trigger Simulation)
In a separate terminal, run these to verify detection:
```bash
# Python Version (Ease of Use)
./.venv/bin/python3 src/Validator.py cpu

# C Version (High Performance)
cd src_c && ./simulator cpu
```

---

## ⚡ Python vs C Implementation

| Feature | Python (Standard) | C (Hyper-Suite) |
| :--- | :--- | :--- |
| **Speed** | 10-50ms latency | **<1ms latency** |
| **Overhead** | Medium (Interpreter) | **Microscopic (Static)** |
| **ML Training**| **Rich Ecosystem** | Difficult |
| **Telemetry** | Higher Level (psutil) | **Direct Syscalls** |

### Which one to use?
- Use **Python** for development, training, and building complex AI models.
- Use **C** for production monitoring where every microsecond and CPU cycle counts.

---

## 📂 Industrial Structure
- `src/`: The Python ecosystem (Inference, Training, UI).
- `src_c/`: The C ecosystem (Performance, Syscalls, Speed).
- `src/simulation_config.json`: Shared configuration for scenarios.

---

## 🎓 How it works: Teach Me!

If you are new to Anomaly Detection on macOS, here is the secret sauce:

1.  **Direct Syscalls (The C Side)**: Instead of asking Python to ask the OS for CPU info, our C code talks directly to the **Mach Kernel** (`mach/mach.h`). This is how Activity Monitor works. It's the fastest way to get data without slowing down your M4 Pro core.
2.  **The AI Brain (The Python Side)**: C is fast but "dumb". Python is "smart". We use Python to look at thousands of data points and find the **F1-Score Champion**. We then save that "Gold Model" as a `.bin` file.
3.  **The Threshold (The Detector)**:
    - **Anomaly Score**: We don't just alert on one spike. We use a **trailing window**. If the last 5 seconds look suspicious, the "Threat Level" rises.
    - **Muting**: We added **Selective Monitoring**. If you press `C` in the dashboard, the system ignores CPU spikes but keeps watching RAM. This prevents false alarms when you know you're doing heavy work.
4.  **ARM Optimization**: Your M4 Pro has P-cores (Performance) and E-cores (Efficiency). Our simulators specifically target the **M-series memory controller** using **Vectorized NumPy** (Python) and **Direct Mapped Memory** (C) to ensure the stress test is realistic.

---

## 📂 Component Description

| File | Purpose |
| :--- | :--- |
| `src/DataCollector.py` | High-frequency telemetry engine. Gathers CPU, RAM, Disk, and Net metrics. |
| `src/Simulator.py` | The "Heart" of the simulation. Contains ARM-native stress logic. |
| `src/ModelTrainer.py` | The "Brain" factory. Trains 13+ models and picks the best one. |
| `src/AnomalyEngine.py` | The "Security Guard". Real-time dashboard and inference engine. |
| `src/Validator.py` | The "Test Kit". One-click script to verify the system's reaction. |
| `src/simulation_config.json` | Configuration file for different simulation scenarios. |

---

## 💎 Build Artifacts (Generated after Training)

| Artifact | Location | Description |
| :--- | :--- | :--- |
| `monitored_data.csv` | `src/output_folder/` | Raw dataset used for AI training. |
| `archive/*.bin` | `src/archive/` | All 13+ trained models stored in binary format. |
| `best_model.bin` | `src/` | A copy of the top-performing model (Champion). |
| `leaderboard.json` | `src/analytics/` | Machine-readable ranking of all trained models. |
| `leaderboard.md` | `src/analytics/` | Human-readable ranking with visual charts. |
| `*.png` | `src/analytics/` | Performance charts, confusion matrices, and loss curves. |

---

## 📝 Compliance & Performance
The system is designed to be "silent" during monitoring and "aggressive" during simulation to ensure clear signatures for the machine learning models. Built for high-reliability detection on Apple Silicon.

---
*Created for the DCML 2025 Anomaly Detection Project.*