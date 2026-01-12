# DCML 2026 Project: Anomaly Detection System
## Final Academic Report

---

**Course**: Data Collection and Machine Learning (DCML)  
**Academic Year**: 2025-2026  
**Submission Date**: January 2026  
**Author**: Holan  
**Target Platform**: Apple MacBook Pro M4 Pro (14 Cores, 24GB RAM, macOS Sequoia)

---

## Abstract

This report presents the design, implementation, and evaluation of a real-time anomaly detection system for modern computing platforms. The project addresses the DCML course requirement of applying machine learning techniques to real-world data collection scenarios. The system employs a **dual-ecosystem architecture**: a Python-based Machine Learning pipeline that benchmarks 13 classification algorithms, and a complementary C-based statistical engine for high-performance verification. Experimental results demonstrate detection accuracy exceeding 98% for CPU, Memory, and Disk anomalies.

**Keywords**: Anomaly Detection, Machine Learning, Data Collection, System Monitoring, Classification, Apple Silicon

---

## 1. Introduction

### 1.1 Background and Motivation

Modern computing systems generate vast amounts of telemetry data including CPU utilization, memory consumption, disk I/O rates, and network traffic. Monitoring these metrics is essential for system administration, security, and performance optimization. Traditional threshold-based monitoring (e.g., "alert if CPU > 90%") is limited because:

1. It cannot capture complex multi-dimensional patterns.
2. Fixed thresholds do not adapt to different workloads.
3. It fails to identify the *root cause* of anomalies.

Machine Learning offers a solution by learning the normal operating patterns and detecting deviations automatically.

### 1.2 Objectives

This project aims to:

1. **Collect** high-frequency system telemetry data (CPU, RAM, Disk, Network).
2. **Annotate** data using controlled stress injections ("ground truth" labeling).
3. **Train** multiple supervised and unsupervised ML algorithms.
4. **Evaluate** models using standard metrics (F1-Score, Precision, Recall).
5. **Deploy** a real-time detection dashboard with root cause identification.
6. **Verify** results using an independent C-based statistical approach.

### 1.3 Scope

The system is specifically optimized for Apple Silicon (M4 Pro) but the methodology is transferable to other platforms. This report covers:

- Data collection methodology
- Feature engineering decisions
- Model training and selection
- Real-time inference architecture
- Comparative analysis of Python ML vs C Statistical approaches

---

## 2. Literature Review

### 2.1 Anomaly Detection in System Monitoring

Chandola et al. (2009) provide a comprehensive survey of anomaly detection techniques, categorizing them into:

- **Statistical methods**: Z-score, Gaussian models
- **Classification-based**: Decision Trees, SVM, Neural Networks
- **Nearest-neighbor**: KNN, Local Outlier Factor
- **Isolation methods**: Isolation Forest

For system monitoring, Isolation Forest (Liu et al., 2008) is particularly effective because it isolates anomalies based on *path length* in random trees, making it computationally efficient.

### 2.2 Feature Engineering for System Metrics

Gregg (2020) emphasizes the importance of collecting **rate metrics** (e.g., bytes/second) rather than **cumulative counters** (e.g., total bytes since boot). This prevents baseline drift in long-running monitoring systems.

### 2.3 Classification Algorithms

The following algorithms were selected based on their established performance in anomaly detection literature:

| Algorithm | Type | Reference |
| :--- | :--- | :--- |
| Random Forest | Ensemble | Breiman, 2001 |
| Gradient Boosting | Ensemble | Friedman, 2001 |
| MLP Neural Network | Deep Learning | Haykin, 1999 |
| Isolation Forest | Unsupervised | Liu et al., 2008 |
| SVM (RBF/Linear) | Kernel | Cortes & Vapnik, 1995 |

---

## 3. Methodology

### 3.1 Data Collection

#### 3.1.1 Telemetry Gathering

The `DataCollector.py` module uses the `psutil` library to capture system metrics at 0.5-second intervals:

```python
cpu_percent = psutil.cpu_percent(percpu=True)  # Per-core CPU load
virtual_memory = psutil.virtual_memory()        # RAM statistics
disk_io = psutil.disk_io_counters()            # Disk read/write
net_io = psutil.net_io_counters()              # Network traffic
```

#### 3.1.2 Differential Telemetry

To address the baseline drift problem identified in Section 2.2, cumulative counters are converted to rates:

$$\text{Rate} = \frac{\text{Current Value} - \text{Previous Value}}{\Delta t}$$

#### 3.1.3 Ground Truth Labeling

Controlled stress injections are used to create labeled training data:

- **CPU Stress**: Multiprocessing busy-loops on all 14 cores
- **RAM Stress**: NumPy array allocation (up to 8GB)
- **Disk Stress**: Sequential write operations to `/tmp`
- **Network Stress**: HTTP request flooding

### 3.2 Feature Engineering

Approximately 100 features are extracted per sample, grouped into four categories:

| Category | Example Features | Count |
| :--- | :--- | :--- |
| CPU | load0...load13, user_time, system_time | ~60 |
| Memory | virtual_percent, swap_used | ~10 |
| Disk | disk_read_rate, disk_write_rate | ~10 |
| Network | net_bytes_sent_rate, connections | ~10 |

### 3.3 Model Training ("Extreme Benchmarking")

The `ModelTrainer.py` module implements a comparative evaluation framework:

1. **Split**: 70% training, 30% testing (stratified)
2. **Normalize**: StandardScaler (z-score normalization)
3. **Train**: 13 algorithms (10 supervised, 3 unsupervised)
4. **Evaluate**: F1-Score, Precision, Recall, Accuracy
5. **Select**: Champion model saved to `best_model.bin`

### 3.4 Real-Time Inference

The `AnomalyEngine.py` module implements the detection loop:

```
LOOP:
    1. Capture live system state (100 features)
    2. Apply StandardScaler transformation
    3. Model.predict() → Anomaly / Normal
    4. If Anomaly: identify_root_cause()
    5. Update dashboard UI
    6. Log to file
    7. Sleep 300ms
```

### 3.5 Root Cause Identification (Hybrid Detection)

A key contribution of this project is the **Mean Category Deviation** algorithm:

1. Group feature Z-scores by category (CPU, Memory, Disk, Network)
2. Calculate the mean Z-score for each category
3. Apply sanity checks (raw CPU% > 85% → boost CPU score)
4. Return the category with the highest score

This solves the "CPU Bias" problem where 14 CPU features would dominate 2 Memory features if using simple summation.

---

## 4. Implementation

### 4.1 Python Machine Learning Ecosystem

| Module | Purpose |
| :--- | :--- |
| `DataCollector.py` | High-frequency telemetry collection |
| `Simulator.py` | Stress injection (CPU, RAM, Disk, Net) |
| `ModelTrainer.py` | 13-algorithm benchmarking engine |
| `AnomalyEngine.py` | Real-time dashboard and inference |

### 4.2 C Statistical Verification Suite

To validate results independently, a C implementation was developed using direct macOS Mach Kernel syscalls:

```c
kern_return_t kr = host_processor_info(
    mach_host_self(),
    PROCESSOR_CPU_LOAD_INFO,
    &processor_count,
    &cpu_load,
    &cpu_msg_count
);
```

The C engine uses classical Z-score statistics (no ML) to detect anomalies, providing an independent verification baseline.

---

## 5. Results and Evaluation

### 5.1 Model Performance

| Rank | Model | F1-Score | Type |
| :--- | :--- | :--- | :--- |
| 🥇 | Random Forest | 0.9821 | Supervised |
| 🥈 | Gradient Boosting | 0.9756 | Supervised |
| 🥉 | MLP Neural Network | 0.9542 | Supervised |
| 4 | SVM (RBF) | 0.9423 | Supervised |
| 5 | Isolation Forest | 0.9012 | Unsupervised |

### 5.2 Root Cause Detection Accuracy

| Injection | Expected | Detected | Accuracy |
| :--- | :--- | :--- | :--- |
| CPU Stress | CPU | CPU | ✅ 100% |
| RAM Stress | MEMORY | MEMORY | ✅ 100% |
| Disk Stress | DISK | DISK | ✅ 100% |

### 5.3 Latency Comparison

| Metric | Python | C |
| :--- | :--- | :--- |
| Inference Latency | ~50ms | <1ms |
| CPU Overhead | 2-5% | <0.1% |

---

## 6. Discussion

### 6.1 Key Findings

1. **Ensemble methods outperform others**: Random Forest achieved the highest F1-Score due to its robustness to overfitting.
2. **Feature normalization is critical**: Without StandardScaler, SVM and Neural Networks failed to converge.
3. **Mean Category Deviation solves bias**: Simple Z-score summation favored CPU; averaging fixed this.

### 6.2 Limitations

1. Network anomaly detection is less reliable due to variable external traffic.
2. The system is currently optimized only for Apple Silicon.
3. GPU monitoring is not yet implemented.

### 6.3 Future Work

1. Extend to Linux and Windows platforms.
2. Add GPU/NPU monitoring for Apple Neural Engine.
3. Implement online learning for adaptive baselines.

---

## 7. Conclusion

This project successfully demonstrates the application of Machine Learning to real-time system anomaly detection. The dual-ecosystem approach (Python ML + C Statistical) provides both flexibility and verification. The Extreme Benchmarking methodology ensures optimal model selection, and the Hybrid Detection algorithm solves practical challenges in root cause identification.

The system achieves >98% F1-Score with the Random Forest classifier and correctly identifies the root cause (CPU, Memory, or Disk) with 100% accuracy on controlled tests.

---

## References

1. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32.
2. Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly Detection: A Survey. *ACM Computing Surveys*, 41(3).
3. Cortes, C., & Vapnik, V. (1995). Support-Vector Networks. *Machine Learning*, 20(3), 273-297.
4. Friedman, J. H. (2001). Greedy Function Approximation: A Gradient Boosting Machine. *Annals of Statistics*.
5. Gregg, B. (2020). *Systems Performance* (2nd ed.). Addison-Wesley Professional.
6. Liu, F. T., Ting, K. M., & Zhou, Z. H. (2008). Isolation Forest. *ICDM*, 413-422.

---

## Appendix A: System Configuration

- **Hardware**: MacBook Pro M4 Pro (14-core CPU, 24GB Unified Memory)
- **OS**: macOS Sequoia 15.0
- **Python**: 3.10.12
- **Libraries**: scikit-learn 1.3.0, psutil 5.9.5, rich 13.6.0
- **C Compiler**: Apple Clang 15.0.0

---

*Submitted for DCML 2026.*
