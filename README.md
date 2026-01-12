# 🛡️ DCML 2025: Advanced Anomaly Detection System (M4 Pro Optimized)

**Submission for DCML 2025**
*An educational, industrial-grade anomaly detection system specifically optimized for Apple Silicon.*

![Dashboard Preview](docs/dashboard_preview.png)
*(Run `python3 src/AnomalyEngine.py` to see this live)*

## 📜 License
This project is open source and available under the [MIT License](LICENSE).

---

## 📖 Educational Overview
This project is designed to teach and demonstrate **High-Performance Diagnostic Systems**. It uses a dual-ecosystem approach to show the strengths of different programming languages:

1.  **Python (The Brain)**: Used for complex logic, Machine Learning, and User Interfaces. It's easy to read and modify.
2.  **C (The Muscle)**: Used for raw speed. It talks directly to the macOS Kernel to get data in microseconds.

---

## 📂 "Teachable" File Structure

We have organized the project to make it easy to learn from:

### `src/` (The Python Ecosystem)
Everything here is designed to be **Readable** and **Educational**.
- **`DataCollector.py`**: The "Sensor". It gathers data from your computer.
- **`ModelTrainer.py`**: The "Teacher". It uses **Extreme Benchmarking** to train 13+ AI models and pick the winner.
- **`AnomalyEngine.py`**: The "Guard". It uses the trained brain to protect your Mac.
- *[👉 Read the Python Guide here](src/README.md)*

### `src_c/` (The C Hyper-Suite)
Everything here is designed for **Performance**.
- **`telemetry.c`**: Shows how to use System Calls.
- **`engine.c`**: Shows how to build a UI in C.
- *[👉 Read the Low-Level Systems Guide here](src_c/README.md)*

### `src/experimental/` (The Laboratory)
This is where we test new ideas (like "V2 Differential Telemetry"). It is separated so it doesn't break the main stable project.

---

## ⚡ Quick Start: The "Active" Workflow

This project uses a **Virtual Environment (venv)** to ensure it runs perfectly on any Mac without messing up your system files.

### 1. Setup the "Sandbox"
```bash
# Create a secure area for our libraries
python3 -m venv .venv

# Activate the sandbox
source .venv/bin/activate

# Install the dependencies
pip install -r requirements.txt
```

### 2. Collect Data
Let the system watch your computer for a while to learn.
```bash
python3 src/DataCollector.py
```
*Output: `src/output_folder/monitored_data.csv`*

### 3. "Extreme Benchmarking" (Model Training)
We don't just use Random Forest. This script trains **13+ Algorithms** (SVM, Neural Networks, Isolation Forest, etc.) and automatically selects the **Champion Model**.
```bash
python3 src/ModelTrainer.py
```
*Output: `src/best_model.bin` (The Winner)*

### 4. Launch the Dashboard
Run the real-time protection engine.
```bash
python3 src/AnomalyEngine.py 15 best
```

---

## 🧪 Simulation: Triggering Anomalies
You can verify the system works by intentionally stressing your Mac.

**Python Simulator (Easiest)**:
```bash
python3 src/Validator.py cpu   # Stress 14 Cores
python3 src/Validator.py ram   # Fill RAM
```

**C Simulator (Fastest)**:
```bash
cd src_c && make && ./simulator cpu
```

---

## 📚 Further Reading & References

This project was built on the shoulders of giants. Here are the BEST resources to learn more:

### 📖 Essential Books
| Topic | Book | Why read it? |
| :--- | :--- | :--- |
| **Systems** | *Systems Performance* by **Brendan Gregg** | The "Bible" of understanding CPU, RAM, and Disk metrics. |
| **ML** | *Hands-On Machine Learning* by **Aurélien Géron** | The best practical guide for `scikit-learn` and Neural Nets. |
| **C Language** | *The C Programming Language* by **Kernighan & Ritchie** | The classic text for understanding memory and pointers. |
| **Kernel** | *Mac OS X Internals* by **Amit Singh** | Deep dive into the Mach Kernel and XNU. |

### 🔗 "Awesome" Repositories
- [awesome-machine-learning](https://github.com/josephmisiti/awesome-machine-learning): A curated list of ML frameworks.
- [awesome-python](https://github.com/vinta/awesome-python): Best Python libraries for every task.
- [awesome-c](https://github.com/oz123/awesome-c): Frameworks and libraries for C developers.

### 📄 Academic Papers
- **Random Forest**: Breiman, L. (2001). "Random Forests". *Machine Learning*, 45(1), 5-32.
- **Isolation Forest**: Liu, F., Ting, K. M., & Zhou, Z. H. (2008). "Isolation Forest". *ICDM*.
- **XGBoost**: Chen, T., & Guestrin, C. (2016). "XGBoost: A Scalable Tree Boosting System".

### 🍎 Apple Documentation
- [Mach Kernel Programming Guide](https://developer.apple.com/library/archive/documentation/Darwin/Conceptual/KernelProgramming/): Official guide to `mach_host_statistics`.
- [Apple Silicon CPU Optimization Guide](https://developer.apple.com/documentation/apple-silicon/tuning-your-code-s-performance-for-apple-silicon): How to write code for M-series chips.

---
*Created by Holan for DCML 2025.*