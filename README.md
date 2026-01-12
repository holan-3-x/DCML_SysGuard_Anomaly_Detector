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

### Step 3: Deployment (Real-time Dashboard)
```bash
# Auto-calibrated mode (Uses the Champion model from training)
./.venv/bin/python3 src/AnomalyEngine.py 15 best

# Specific model mode (e.g. RandomForest, NeuralNetwork, IsolationForest)
./.venv/bin/python3 src/AnomalyEngine.py 20 RandomForest
```

### Step 4: Verification (Trigger Simulation)
In a separate terminal, run these to verify detection:
```bash
./.venv/bin/python3 src/Validator.py cpu   # High CPU Load
./.venv/bin/python3 src/Validator.py ram   # Aggressive Memory Allocation
./.venv/bin/python3 src/Validator.py disk  # High IO Throughput
./.venv/bin/python3 src/Validator.py net   # Multi-threaded Network Traffic
```

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