# 🎓 How It Works: Theory & Practice

This document bridges the gap between **Computer Science Theory** and **Practical Implementation**. It is designed for students and developers who want to understand *why* we wrote the code this way.

---

## 🧠 Part 1: The Theory (Anomaly Detection)

### What is an "Anomaly"?
In data science, an anomaly (or outlier) is a data point that differs significantly from the majority of the data.
*   **Contextual Anomalies**: High CPU usage is "normal" when rendering a video, but "abnormal" when the computer is idle. Our system learns this context.

### Supervised vs. Unsupervised Learning
Our project supports both, which is rare!

| Type | Theory | In Our Code |
| :--- | :--- | :--- |
| **Supervised** | We tell the AI "This is Normal" and "This is an Attack". It learns the difference. | We train **Random Forest** on labeled data (where `injector != rest`). |
| **Unsupervised** | We give the AI unlabeled data and say "Find the weird stuff". | We use **Isolation Forest** to detect patterns that are statistically rare. |

### The "Z-Score" (Statistical Distance)
For simple metrics (like checking if RAM is full), we don't always need AI. We can use Statistics.
*   **Formula**: $Z = \frac{(X - \mu)}{\sigma}$
*   **Translation**: "How many standard deviations is the current value ($X$) away from the average ($\mu$)? "
*   **In Practice**: If CPU usage has a Z-Score of **3.0**, it means it is in the top **0.1%** of extreme values. That is an anomaly.

---

## 💻 Part 2: The Practice (The Code)

How do we turn those equations into Python and C code?

### 1. Data Collection (`DataCollector.py`)
**Problem**: How do we get the variables ($X$) for our equations?
**Solution**: We act as a "Sensor".
*   **Step A**: We ask the OS for counters (CPU ticks, RAM pages).
*   **Step B (Critical)**: We calculate the **Rate of Change**.
    *   *Bad Code*: `current_bytes` (This number always goes up).
    *   *Good Code*: `(current_bytes - previous_bytes) / time_elapsed` (This gives us Bytes/Sec).
*   **Result**: We get a clean vector of numbers $[x_1, x_2, ... x_n]$ representing the system state.

### 2. The Training Loop (`ModelTrainer.py`)
**Problem**: How do we find the parameters ($\mu, \sigma$) or the Decision Trees?
**Solution**: "Extreme Benchmarking".
*   We splitting our data into **Training Set (70%)** and **Test Set (30%)**.
*   We train **13 different brains** (models) on the Training Set.
*   We quiz them on the Test Set.
*   The one with the highest **F1-Score** (Combination of Precision and Recall) becomes the **Champion**.

### 3. Real-Time Inference (`AnomalyEngine.py`)
**Problem**: We have a trained brain. How do we use it live?
**Solution**: The "Infinite Loop".
1.  **Capture**: Snap a picture of the system (get the vector).
2.  **Scale**: Shrink the numbers so they fit the model (StandardScaler).
3.  **Predict**: Ask the model "Safe or Danger?".
4.  **Visualize**: Draw the result to the screen (using `rich` library).
5.  **Sleep**: Wait 0.5s and repeat.

---

## 🏎️ Part 3: Systems Optimization (C-Language)

Why did we verify this in C?
*   **The Python Overhead**: Python is an interpreted language. Every time you say `a + b`, the computer runs thousands of C instructions to figure out what `a` and `b` are.
*   **The C Solution**: In `src_c/`, we removed the "Middle Man". We talk directly to the **Mach Kernel**.
*   **Lesson**: This makes the verification tool **100x faster**, proving that the anomalies we see are real, not just Python being slow.

---

## 📚 Study Questions for Students
1.  Why is **Differential Telemetry** (Rates) better than **Cumulative Telemetry** (Totals) for long-running AI?
2.  Why might **Isolation Forest** be better than **Random Forest** if we don't have a label for every possible attack?
3.  Look at `hyper_monitor.c`: Can you find the line where we use `mach_host_self()`? What does that function do?

---
*Prepared for DCML 2025.*
