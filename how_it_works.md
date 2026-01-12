# 🧠 Internal System Logic: The M4 Pro Hyper-Detector

This document outlines the engineering principles and architectural design of the Anomaly Detection system, specifically tailored for high-performance computing on the **MacBook Pro M4 Pro**.

---

## 1. Professional Architecture
The system utilizes a **Telemetry-Driven Model Pipeline**:

### A. Telemetry Gathering (DataCollector.py)
Standard kernel monitoring is insufficient for 14-core ARM architectures. Our **DataCollector** captures a multi-dimensional feature set every 500ms:
- **Core-Grained CPU**: Individual usage of all 14 cores to detect pin-point anomalies.
- **Aggressive RAM Monitoring**: Tracking virtual vs physical footprint.
- **IO Throughput**: Real-time read/write speeds, optimized for fast NVMe storage.
- **Network Congestion**: Socket counts and packet flow.

### B. High-Fidelity Simulation (Simulator.py)
To generate reliable labels, the **Simulator** uses ARM-compatible stress patterns:
- **NumPy Parallelism**: Memory stress uses vectorized allocations to saturate the M4 memory controller.
- **Threaded Network Bursts**: Simulates multi-client traffic spikes via concurrent fetchers.
- **Async Disk Bursts**: Large block writes (50MB+) to stress the integrated storage controller.

---

## 2. Machine Learning Logic (ModelTrainer.py)
We treat anomaly detection as a **Binary Classification Problem** but evaluate it against 13 different architectures:

1.  **Feature Normalization**: Using `StandardScaler` to ensure features with large ranges (like bytes) don't overpower percentage-based features (like core load).
2.  **Cross-Architecture Benchmarking**: We train everything from **Random Forests** (robust/fast) to **Multi-Layer Perceptrons** (deep pattern recognition) and **Isolation Forests** (unsupervised).
3.  **Gold-Model Selection**: The system automatically archives all models and selects the "Champion" based on the highest **F1-Score**, ensuring the best balance between precision and recall.

---

## 3. Real-time Inference Engine (AnomalyEngine.py)
When the dashboard is running, it performs the following cycle:
1.  **Stream Data**: Grabs a packet from the `monitor_system()` function.
2.  **Vectorize**: Aligns the data with the features used during training.
3.  **Predict**: Feeds the vector into the `.bin` model files.
4.  **Confidence Smoothing**: Uses a trailing window to calculate an "Anomaly Score", reducing false positives from sudden M4 Pro performance boosts.

---

## 4. Why this System is "Better"
- **Leading Columns**: As requested, all data exports put `Timestamp` and `UserReadTime` first for human auditability in Excel/CSV.
- **M4 Pro Aware**: Unlike standard generic detectors, this system is aware of the core count and the aggressive memory management of macOS Sequoia.
- **Transparent Analytics**: Every training cycle generates a visual leaderboard so you can see why the system chose a specific "Best Model".

---
*Reference: DCML 2025 Architectural Documentation.*
