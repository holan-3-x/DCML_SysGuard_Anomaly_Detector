# 🚀 DCML Anomaly Detector (M4 Pro Optimized)

An end-to-end anomaly detection system for macOS, featuring real-time monitoring, multi-model AI training (Supervised & Unsupervised), and a premium terminal dashboard.

## 💻 System Compatibility
- **Hardware**: Specifically optimized for **MacBook Pro M4 Pro** (14 CPU cores).
- **OS**: macOS (using custom busy-loop stressors for ARM architecture).
- **Python**: 3.13+ recommended.

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

## 📊 Workflow Steps

### Step 1: Data Collection (Monitoring)
Collect baseline performance data (Normal vs Injected Anomalies) to train the AI.
```bash
./.venv/bin/python3 src/main_monitor_injector.py
```
*Creates: `src/output_folder/monitored_data.csv`*

### Step 2: AI Model Training
Train both **Supervised** (Random Forest) and **Unsupervised** (Isolation Forest) models.
```bash
./.venv/bin/python3 src/train_advanced.py
```
*Creates: `src/random_forest.bin`, `src/isolation_forest.bin`, and `src/standard_scaler.bin`*

### Step 3: Run the Dashboard
```bash
# Use the auto-selected best model (recommended)
./.venv/bin/python3 src/enhanced_detector.py 5 best

# Or choose a specific architecture: rf, mlp, iso
./.venv/bin/python3 src/enhanced_detector.py 5 mlp
```

### Step 4: Inject a Test Anomaly
In a second terminal, trigger any anomaly to see the dashboard react.
```bash
# Test Options: cpu, disk, ram, net

./.venv/bin/python3 src/test_anomaly.py cpu
./.venv/bin/python3 src/test_anomaly.py disk
./.venv/bin/python3 src/test_anomaly.py ram
./.venv/bin/python3 src/test_anomaly.py net
```

---

## 📂 Project Structure
- `src/enhanced_detector.py`: The premium terminal dashboard.
- `src/train_advanced.py`: Advanced training script for multiple models.
- `src/main_monitor_injector.py`: Data collection & fault injection engine.
- `src/LoadInjector.py`: Core logic for simulating CPU and Memory stress (Mac optimized).
- `src/test_anomaly.py`: Helper script to trigger a 10-second anomaly.

---

## 📝 Logs & Data
- `src/warnings.log`: History of all detected anomalies.
- `src/raw_predictions.log`: Detailed timestamped logs of every prediction made.
- `src/output_folder/`: Contains the raw CSV data used for training.

---
*Created for the DCML 25/26 Project.*