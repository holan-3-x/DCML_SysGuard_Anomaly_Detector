# 🧠 Internal System Logic: The M4 Pro Hyper-Detector

This document outlines the engineering principles and architectural design of the Anomaly Detection system, specifically tailored for high-performance computing on the **MacBook Pro M4 Pro**.

---

## 1. Professional Architecture
The system utilizes a **Telemetry-Driven Model Pipeline**:

### A. Telemetry Gathering (DataCollector.py)
Our **DataCollector** captures a multi-dimensional feature set every 500ms:
- **Core-Grained CPU**: Individual usage of all 14 cores to detect pin-point anomalies.
- **Aggressive RAM Monitoring**: Tracking virtual vs physical footprint.
- **IO Throughput**: Real-time read/write speeds, optimized for fast NVMe storage.
- **Network Congestion**: Socket counts and packet flow.

### B. High-Fidelity Simulation (Simulator.py)
The **Simulator** generates reliable labels using ARM-compatible stress patterns:
- **NumPy Parallelism**: Vectorized memory saturation.
- **Threaded Network Bursts**: Concurrent fetchers for traffic spikes.
- **Async Disk Bursts**: Large block writes (50MB+).

---

## 2. Machine Learning Logic (ModelTrainer.py)
We evaluate detection against 13+ architectures:
1.  **Feature Normalization**: Using `StandardScaler` to balance core load vs byte metrics.
2.  **Cross-Architecture Benchmarking**: Training Random Forests, MLP Networks, and Isolation Forests.
3.  **Gold-Model Selection**: Automatic ranking based on the highest **F1-Score**.

---

## 3. Advanced Real-time Features (AnomalyEngine.py)

### 🧩 Root Cause Inference
When an anomaly is detected, the system calculates which feature group has the highest deviation from the "Normal" baseline. The dashboard will display the **Probable Cause** (CPU, MEM, DISK, or NETWORK) in the security panel.

### 🔇 Selective Monitoring (Muting)
To prevent false alarms during high-usage work (like video editing or compiling code), you can **shutdown** detection for specific subsystems using interactive keyboard toggles:
- **`C`**: Toggle CPU Monitoring
- **`R`**: Toggle RAM Monitoring
- **`D`**: Toggle Disk Monitoring
- **`N`**: Toggle Network Monitoring

If a subsystem is MUTED, the system will ignore anomalies caused by that part while still showing you the live performance stats.

---

## 4. Why this System is "Better"
- **Leading Columns**: `Timestamp` and `UserReadTime` come first in all exports.
- **M4 Pro Native**: Aware of core counts and ARM memory management.
- **Transparent Analytics**: Visual leaderboard generated after every training.

---
*Reference: DCML 2025 Architectural Documentation.*
