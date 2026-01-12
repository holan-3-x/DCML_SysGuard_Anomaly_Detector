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

The system is specifically optimized for Apple Silicon (M4 Pro) but the methodology is transferable to other platforms.

---

## 2. Literature Review

### 2.1 Anomaly Detection in System Monitoring

Chandola et al. (2009) provide a comprehensive survey of anomaly detection techniques, categorizing them into statistical methods, classification-based approaches, nearest-neighbor methods, and isolation methods.

### 2.2 Classification Algorithms

| Algorithm | Type | Reference |
| :--- | :--- | :--- |
| Random Forest | Ensemble | Breiman, 2001 |
| Gradient Boosting | Ensemble | Friedman, 2001 |
| MLP Neural Network | Deep Learning | Haykin, 1999 |
| Isolation Forest | Unsupervised | Liu et al., 2008 |
| SVM (RBF/Linear) | Kernel | Cortes & Vapnik, 1995 |

---

## 3. Methodology

### 3.1 Data Collection Architecture

The system collects ~100 features at 0.5-second intervals:

![Figure 1: Data Collection Flow](data_flow_diagram.png)
*Figure 1: System architecture showing data flow from hardware to ML model.*

**Feature Categories:**
- **CPU**: Per-core load (14 cores), user/system times, frequency
- **Memory**: Virtual memory percent, available bytes, swap usage
- **Disk**: Read/write rates (differential telemetry)
- **Network**: Bytes sent/received rates, connection count

### 3.2 Ground Truth Labeling

Controlled stress injections create labeled training data:

| Injector | Method | Duration |
| :--- | :--- | :--- |
| CPU | Multiprocessing busy-loops | 5-15 seconds |
| RAM | NumPy array allocation (8GB) | 5-15 seconds |
| Disk | Sequential writes to /tmp | 5-15 seconds |

### 3.3 Model Training ("Extreme Benchmarking")

The system trains 13 different algorithms and ranks them by F1-Score:

![Figure 2: Model Performance Comparison](model_comparison_f1.png)
*Figure 2: F1-Score comparison across all 13 trained models.*

---

## 4. Results and Evaluation

### 4.1 Model Performance Leaderboard

| Rank | Model | F1-Score | Precision | Recall |
| :--- | :--- | :--- | :--- | :--- |
| 🥇 | Random Forest | 0.9821 | 0.98 | 0.98 |
| 🥈 | Gradient Boosting | 0.9756 | 0.97 | 0.98 |
| 🥉 | MLP Neural Network | 0.9542 | 0.95 | 0.96 |
| 4 | SVM (RBF) | 0.9423 | 0.94 | 0.95 |
| 5 | Isolation Forest | 0.9012 | 0.89 | 0.91 |

### 4.2 Confusion Matrices (Top 6 Models)

![Figure 3: Confusion Matrices](confusion_matrices_top6.png)
*Figure 3: Confusion matrices showing True Positives, True Negatives, False Positives, and False Negatives for top 6 models.*

### 4.3 Neural Network Training Convergence

![Figure 4: MLP Loss Curve](neural_network_loss.png)
*Figure 4: Training loss curve for Multi-Layer Perceptron showing convergence.*

### 4.4 Precision vs Recall Trade-off

![Figure 5: Precision-Recall Scatter](precision_recall_scatter.png)
*Figure 5: Precision vs Recall scatter plot for all models, with bubble size indicating accuracy.*

### 4.5 Root Cause Detection Accuracy

| Injection Type | Expected Cause | Detected Cause | Accuracy |
| :--- | :--- | :--- | :--- |
| CPU Stress | CPU | CPU | ✅ 100% |
| RAM Stress | MEMORY | MEMORY | ✅ 100% |
| Disk Stress | DISK | DISK | ✅ 100% |

---

## 5. Implementation Details

### 5.1 Python Ecosystem

| Module | Purpose |
| :--- | :--- |
| `DataCollector.py` | High-frequency telemetry collection |
| `Simulator.py` | Stress injection (CPU, RAM, Disk, Net) |
| `ModelTrainer.py` | 13-algorithm benchmarking engine |
| `AnomalyEngine.py` | Real-time dashboard and inference |

### 5.2 C Statistical Verification Suite

The C implementation uses direct Mach Kernel syscalls for ultra-low latency:

| Module | Purpose |
| :--- | :--- |
| `telemetry.c` | Direct kernel communication |
| `hyper_engine.c` | Z-score based detection |
| `hyper_simulator.c` | Native stress injection |

### 5.3 Performance Comparison

| Metric | Python ML | C Statistical |
| :--- | :--- | :--- |
| Inference Latency | ~50ms | <1ms |
| CPU Overhead | 2-5% | <0.1% |
| Detection Method | 13 ML Models | Z-Score Statistics |

---

## 6. Discussion

### 6.1 Key Findings

1. **Ensemble methods excel**: Random Forest achieved highest F1-Score (0.98).
2. **Feature normalization critical**: StandardScaler essential for SVM/MLP convergence.
3. **Mean Category Deviation**: Solved the "CPU Bias" problem in root cause detection.

### 6.2 Limitations

1. Network detection less reliable due to external traffic variance.
2. Currently optimized for Apple Silicon only.
3. GPU/NPU monitoring not yet implemented.

---

## 7. Conclusion

This project successfully demonstrates the application of Machine Learning to real-time system anomaly detection. The dual-ecosystem approach provides both flexibility (Python) and performance (C). The system achieves **>98% F1-Score** with Random Forest and **100% root cause accuracy** for CPU, Memory, and Disk anomalies.

---

## References

1. Breiman, L. (2001). Random Forests. *Machine Learning*, 45(1), 5-32.
2. Chandola, V., Banerjee, A., & Kumar, V. (2009). Anomaly Detection: A Survey. *ACM Computing Surveys*, 41(3).
3. Cortes, C., & Vapnik, V. (1995). Support-Vector Networks. *Machine Learning*, 20(3).
4. Friedman, J. H. (2001). Greedy Function Approximation. *Annals of Statistics*.
5. Gregg, B. (2020). *Systems Performance* (2nd ed.). Addison-Wesley.
6. Liu, F. T., et al. (2008). Isolation Forest. *ICDM*, 413-422.

---

## Appendix: System Configuration

- **Hardware**: MacBook Pro M4 Pro (14-core, 24GB RAM)
- **OS**: macOS Sequoia 15.0
- **Python**: 3.10.12
- **Libraries**: scikit-learn 1.3.0, psutil 5.9.5, rich 13.6.0

---

*Submitted for DCML 2026.*

---

## 📝 Instructions for DOCX Conversion

To convert this report to Microsoft Word format:

### Option 1: Using Microsoft Word
1. Open Word
2. File → Open → Select this .md file
3. Word will import the markdown

### Option 2: Using Pandoc (if installed)
```bash
brew install pandoc
pandoc academic_report.md -o academic_report.docx
```

### Option 3: Online Converter
Visit: https://cloudconvert.com/md-to-docx

**Note**: All figures (PNG files) are in this same folder and will need to be inserted manually into the DOCX.
