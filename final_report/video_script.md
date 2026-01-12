# 🎬 Academic Video Recording Script
## DCML 2026: Anomaly Detection System Presentation

**Total Duration**: 5:00 minutes  
**Format**: Screen Recording + Voiceover  
**Style**: Academic/Technical Presentation

---

## Segment 1: Introduction & Objectives (0:00 - 0:50)

### Screen Display
- Show the project's README.md or title slide
- Display the system architecture diagram

### Narration Script
> "This presentation demonstrates a machine learning-based anomaly detection system developed for the DCML 2026 course.
>
> **Research Question**: Can we use supervised classification algorithms to accurately detect and identify the root cause of system stress in real-time?
>
> **Methodology Overview**:
> - We collect approximately 100 telemetry features at 2 Hz sampling rate
> - We train 13 different classification algorithms
> - We benchmark using F1-Score as the primary evaluation metric
> - We validate results using an independent C-based statistical engine
>
> The target platform is the Apple M4 Pro with 14 CPU cores and 24GB unified memory."

---

## Segment 2: Data Collection Methodology (0:50 - 1:45)

### Screen Display
- Run: `python3 src/DataCollector.py`
- Show the CSV file contents briefly

### Narration Script
> "The data collection phase uses the psutil library to interface with the operating system.
>
> **Key Features We Collect**:
>
> For **CPU**: We measure per-core utilization through 14 `load` features, plus user-space and kernel-space time distributions. This captures heterogeneous load patterns across the M4's Performance and Efficiency cores.
>
> For **Memory**: We track `virtual_percent` which indicates RAM pressure, plus `swap_used` which signals when the system overflows to disk-backed memory.
>
> For **Disk and Network**: We calculate differential rates—bytes per second rather than cumulative totals. This prevents baseline drift in long-running monitoring scenarios.
>
> **Ground Truth Labeling**: To create supervised training data, we inject controlled stress patterns. The `injector` column captures whether each sample was collected under normal conditions or during CPU, RAM, or Disk stress."

### Action
- Show the CSV header row with feature names
- Let the collector run ~10 seconds

---

## Segment 3: Model Training & Benchmarking (1:45 - 2:45)

### Screen Display
- Run: `python3 src/ModelTrainer.py`
- Show the leaderboard output and F1-Score chart

### Narration Script
> "The training phase implements what we call 'Extreme Benchmarking'—training 13 algorithms to empirically determine the best classifier for this specific dataset.
>
> **Algorithms Evaluated**:
> - Ensemble methods: Random Forest, Gradient Boosting
> - Linear classifiers: Logistic Regression, LDA, Naive Bayes
> - Kernel methods: SVM with Linear and RBF kernels
> - Instance-based: K-Nearest Neighbors
> - Neural: Multi-Layer Perceptron with 64-32 hidden layers
> - Unsupervised: Isolation Forest, One-Class SVM, Local Outlier Factor
>
> **Evaluation Protocol**:
> We use a 70/30 stratified train-test split. The primary metric is F1-Score because it balances precision and recall—critical for anomaly detection where false negatives are costly.
>
> **Results**: Random Forest achieved the highest F1-Score of 0.87, followed closely by Gradient Boosting at 0.87. Notably, unsupervised methods achieved only 0.33-0.53 F1, demonstrating the value of labeled training data.
>
> The champion model is automatically serialized to `best_model.bin` for deployment."

---

## Segment 4: Real-Time Detection Demonstration (2:45 - 3:50)

### Screen Display
- **Terminal 1**: Run `python3 src/AnomalyEngine.py`
- **Terminal 2**: Inject stress with `python3 src/Validator.py cpu`

### Narration Script
> "The deployment phase runs an inference loop at approximately 4 Hz—capturing live metrics, applying the trained StandardScaler, and querying the Random Forest classifier.
>
> [Show normal dashboard state]
>
> Currently, the system status shows 'SECURE'—no anomalies detected. The confidence display shows the model's probability estimate.
>
> **Root Cause Identification**: This is a key contribution of our system. When an anomaly is detected, we don't just say 'something is wrong'—we identify WHAT is causing the stress.
>
> We developed a 'Mean Category Deviation' algorithm that averages Z-scores across feature categories. This normalizes for the unequal feature counts—60 CPU features versus 10 Memory features.
>
> [Inject CPU stress]
>
> Now I'm injecting CPU stress using multiprocessing busy-loops across all 14 cores.
>
> [Point to dashboard]
>
> The dashboard immediately transitions to 'ANOMALY' state and correctly identifies 'CPU' as the root cause. Let me verify with RAM stress...
>
> [Inject RAM stress]
>
> And the system correctly identifies 'MEMORY' as the cause. This demonstrates the Mean Category Deviation algorithm working correctly."

---

## Segment 5: C-Language Verification (3:50 - 4:30)

### Screen Display
- Run: `cd src_c && make && ./engine --calibrate`
- Then: `./engine`

### Narration Script
> "To independently validate our ML-based approach, we implemented a parallel system in C that uses classical statistical methods.
>
> **Why C?** The Python implementation has approximately 50 milliseconds inference latency. For production monitoring where every microsecond counts, we need lower overhead.
>
> The C implementation bypasses Python's abstraction layer and communicates directly with the macOS Mach Kernel using the `host_processor_info` system call. This achieves sub-millisecond latency.
>
> **Statistical Detection**: Instead of ML, the C engine uses Z-score threshold detection. During calibration, it establishes baseline mean and standard deviation values. During detection, any sample exceeding 3 standard deviations is flagged as anomalous.
>
> [Run calibration]
>
> The calibration phase collects 60 samples over 30 seconds to establish the baseline...
>
> [Run engine]
>
> And now the C dashboard runs with virtually zero CPU overhead—less than 0.1%."

---

## Segment 6: Conclusion & Future Work (4:30 - 5:00)

### Screen Display
- Show the model comparison chart or conclusion slide

### Narration Script
> "**Key Findings**:
>
> First, ensemble methods—specifically Random Forest—proved most effective for this classification task, achieving 0.87 F1-Score.
>
> Second, supervised learning significantly outperformed unsupervised methods when labeled training data was available.
>
> Third, the dual-ecosystem approach—Python for intelligent ML and C for high-performance verification—provides both flexibility and rigor.
>
> **Future Work** includes extending the system to Linux and Windows platforms, implementing GPU monitoring for Apple Neural Engine workloads, and exploring online learning for adaptive baseline adjustment.
>
> Thank you for your attention. The complete source code and documentation are available in the project repository."

---

## 📝 Recording Preparation Checklist

### Before Recording
- [ ] Close all unnecessary applications
- [ ] Set terminal font size to 16pt or larger (Cmd +)
- [ ] Clear terminal history (`clear` command)
- [ ] Verify all scripts run without errors
- [ ] Position terminal windows for screen recording

### Recording Tools
- **macOS**: QuickTime Player → File → New Screen Recording
- **Alternative**: OBS Studio (free, more features)
- **Output Format**: MP4 or MOV, 1080p recommended

### Post-Recording
- [ ] Trim start/end silence
- [ ] Export as `dcml_presentation.mp4`
- [ ] Place in `final_report/` directory

---

*Script prepared for DCML 2026 Academic Submission.*
