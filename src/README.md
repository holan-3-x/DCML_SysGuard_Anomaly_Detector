# 🐍 The Python Ecosystem: The "Brain" of the Project

Welcome to the intelligent core of the DCML Anomaly Detection System. This directory (`src/`) focuses on **Learning** and **Decision Making**. While C focuses on speed, Python focuses on *smart* analysis using Machine Learning.

![Dashboard Demo](../docs/dashboard_demo.gif)

## 🎓 Educational Guide: Getting Started

### 1. The "Virtual Environment" (venv)
In Python, we use a **Virtual Environment** to keep our project clean. It's like a sandbox. If we install libraries here, they don't mess up your main computer.

**How to set it up (The Right Way):**
```bash
# 1. Create the sandbox (named .venv)
python3 -m venv .venv

# 2. Jump into the sandbox (Activate it)
source .venv/bin/activate

# 3. Install our tools (scikit-learn, psutil, rich)
pip install -r ../requirements.txt
```
*You will know it worked if you see `(.venv)` in your terminal prompt!*

---

## 🧠 The "Extreme Benchmarking" Engine
Many tutorials just show you how to train a "Random Forest". But in the real world (and for DCML), we don't guess—we **prove**.

**`ModelTrainer.py`** is an advanced script that:
1.  Takes your `monitored_data.csv`.
2.  Trains **13 different AI Models** on it simultaneously.
3.  Calculates the **F1-Score** (Precision vs Recall) for each one.
4.  **Automatically Selects the Champion** and saves it as `best_model.bin`.

**Models We Test:**
- 🌲 **Random Forest** (Ensemble of Decision Trees)
- 🧠 **Neural Networks** (Multi-Layer Perceptron)
- 🚀 **Gradient Boosting** (XGBoost logic)
- 🔍 **Isolation Forest** (Unsupervised Anomaly Detection)
- 📏 **SVM** (Support Vector Machines - Linear & RBF)
- ...and 8 more!

---

## 🛠️ Component Breakdown (Teachable)

| File | Type | Educational Purpose |
| :--- | :--- | :--- |
| **`DataCollector.py`** | *Sensor* | Like a "Black Box" recorder for an airplane. It writes down everything your CPU/RAM does into a CSV file. |
| **`Simulator.py`** | *Stress Test* | A script designed to *break* things. It artificially creates CPU, RAM, and Disk stress so the AI can learn what "Danger" looks like. |
| **`ModelTrainer.py`** | *Teacher* | Reads the Black Box data and teaches the AI to recognize the difference between "Resting" and "Danger". |
| **`AnomalyEngine.py`** | *Guard* | The final product. It uses the trained AI to watch your computer in real-time and alert you if something looks wrong. |

---

## 🧪 Experimental Zone (V2)
Inside `src/experimental/`, you will find "Version 2" of our system.
- **Why?**: V1 uses "Total Bytes" (Cumulative). V2 uses "Bytes Per Second" (Differential).
- **Lesson**: V2 is mathematically better for long-term monitoring, but V1 is simpler to understand for beginners.

---
*Part of the DCML 2025 Submission.*
