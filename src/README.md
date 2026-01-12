# 🐍 Python High-Fidelity Ecosystem

This directory contains the Python-based AI core of the DCML project. It is responsible for training the machine learning models and providing the high-level interactive dashboard.

![Dashboard Demo](../docs/dashboard_demo.gif)
*(Example of the real-time anomaly detection engine in action)*

## 🧠 Core Components

### 1. `AnomalyEngine.py` (The Guard)
The real-time dashboard.
- **Inputs**: Live system telemetry (via `DataCollector`).
- **Logic**: Uses the `best_model.bin` to predict anomaly vs normal.
- **Controls**:
    - `C`: Mute CPU alerts.
    - `R`: Mute RAM alerts.
    - `D`: Mute Disk alerts.
    - `N`: Mute Network alerts.

### 2. `ModelTrainer.py` (The Brain)
**Extreme Benchmarking Engine**.
It doesn't just train one model. It trains **13+ algorithms** including:
- Random Forest (Ensemble)
- Neural Networks (MLP)
- Isolation Forest (Unsupervised)
- Gradient Boosting
- SVM (Linear & RBF)
- KNN, Naive Bayes, LOF, and more...

It automatically picks the winner based on **F1-Score** and saves it as `best_model.bin`.

### 3. `Simulator.py` (The Stress Test)
Contains the "Load Injectors".
- `CPUSimulator`: Uses multiprocessing to saturate cores.
- `RAMSimulator`: Uses NumPy to flood memory channels.
- `DiskSimulator`: Writes large chunks to `/tmp` to stress I/O.
- `NetworkSimulator`: Floods localhost loopback.

---

## 📂 Data & Artifacts

- **`archive/`**: Contains ALL 13 trained models (e.g., `NeuralNetwork.bin`, `SVM_RBF.bin`).
- **`analytics/`**: Contains visual reports (Confusion Matrices, Loss Curves).
- **`output_folder/`**: Contains the raw CSV training data.
- **`experimental/`**: Contains the Beta V2 ecosystem (Differential Rate Logic).

---

## 🧪 How to Run
```bash
# 1. Collect Data
python3 DataCollector.py

# 2. Train Models (Takes time!)
python3 ModelTrainer.py

# 3. Predict & Protect
python3 AnomalyEngine.py
```
