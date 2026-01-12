# 🧠 How the Anomaly Detector Works: A Junior Guide

Welcome to the team! This report explains the technical architecture and logic behind our Anomaly Detection system, specifically optimized for the **MacBook Pro M4 Pro**.

---

## 1. The Core Philosophy
Imagine you have a health monitor. It knows your heart rate is normally 60-80 BPM. If it jumps to 150 BPM while you are sleeping, it knows something is wrong. 

Our system does exactly this for your computer. It learns the "Normal" behavior of your **CPU, RAM, Disk, and Network**, and alarms you when the "Heartbeat" (Telemetry) looks like an attack or a failure.

---

## 2. Theoretical Architecture
The system follows a classic **Pipeline Architecture**:

### A. Data Collection (The Sensors)
We use `psutil` (Python System Utilities) to grab raw numbers from the OS every 0.5 seconds:
- **CPU**: Load % for all 14 cores, context switches, interrupts.
- **Memory**: Used vs Available RAM.
- **Disk**: How many bytes are being read/written.
- **Network**: Bytes sent and received.

### B. Fault Injection (The Simulation)
To teach the AI what a "bad" day looks like, we use our `LoadInjector` scripts. We intentionally "attack" the system with:
- **CPU Stress**: Forced busy-loops.
- **Memory Leak**: Allocating massive arrays.
- **Disk Trash**: Writing and reading huge files.
- **Network Spam**: Rapidly requesting hundreds of websites.

### C. The Brain (Machine Learning)
We use a **Random Forest Classifier**:
1.  **Scaling**: We use a `StandardScaler`. This is important because CPU load is 0-100, but Memory can be billions of bytes. Scaling makes them all "equal" for the AI.
2.  **Classification**: The Random Forest looks at the scaled numbers and asks: *"Does this combination of core load and disk activity look more like the 'Normal' data I saw, or the 'Stress' data?"*
3.  **Thresholding**: We don't alarm on the first "bad" signal (it could be a glitch). We use a `warning_level`. Every time the AI is worried, the level goes up. When it hits 5, we trigger the alarm.

---

## 3. Why the M4 Pro is Special
Standard anomaly detectors often assume 4 cores. On your **14-core M4 Pro**, a 4-core detector would be blind to 10 of your cores! 

**Our Solution**:
- **Dynamic Feature Selection**: Our code automatically detects how many cores you have and adjusts the AI's "eyes" (Features) to watch all of them.
- **macOS Busy-Loops**: macOS handles CPU affinity differently than Linux. We implemented a custom `busy_loop` that works natively on Apple Silicon to ensure high-fidelity stress testing.

---

## 5. Analytics & Visualization
We don't just guess; we prove it. After training, look in `src/analytics/`:
- **Confusion Matrix**: Shows exactly how many times the AI was right (TP/TN) vs how many times it made a mistake (FP/FN).
- **Loss Curve**: For the MLP Neural Network, you can actually see the "Learning Process" as a graph.
- **Comparison Chart**: Shows which of our 3 models won the "Gold Medal" for accuracy on your specific hardware.

---

## 💡 Quick Summary for You
1.  **Monitor** gets the numbers (CPU, RAM, Disk, Net).
2.  **Scaler** normalizes the numbers so a "byte" is as important as a "percent".
3.  **Model** guesses: "Normal" or "Anomaly".
4.  **Analytics** tells us how much we can trust the model.
5.  **Dashboard** shows you the live results and confidence.

*Now go run `src/enhanced_detector.py` and break things with `src/test_anomaly.py` to see it in action!*
