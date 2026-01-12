# ⚡ C-Language Hyper-Suite: Low-Level Systems Programming

Welcome to the **Performance Core** of the DCML project. While Python is great for AI, it can be "slow" (relatively speaking). This directory (`src_c/`) demonstrates how to write **High-Performance Systems Code** for the Apple M4 Pro.

## 🎓 Educational Guide: Why C?

### 1. The "Overhead" Problem
In Python, reading a variable might take 100 CPU instructions because of the interpreter. In C, it takes **1 instruction**.
For anomaly detection, we want our monitoring tool to be "invisible". If the monitor uses 10% of the CPU, it ruins the data! Our C monitor uses **<0.1% CPU**.

### 2. "Syscalls" vs Libraries
In Python, we call `psutil.cpu_percent()`. But what does that *do*?
In this C suite, we "talk" directly to the OS Kernel (the brain of macOS).
- **`host_processor_info()`**: We ask the Mach Kernel (the core of macOS) for the raw tick count of every CPU core.
- **`sysctl()`**: We ask the hardware about its topology (How many Performance Cores? How many Efficiency Cores?).

This is **Systems Programming**: communicating directly with the hardware and kernel without layers of abstraction.

---

## 🛠️ Folder Structure (Teachable)

| File | Purpose | Educational Concept |
| :--- | :--- | :--- |
| **`telemetry.c`** | *The Sensor* | Contains the raw `mach_msg` code to talk to the kernel. This is the "hard" part of systems programming. |
| **`hyper_engine.c`** | *The Visualizer* | Draws the User Interface. Shows how to use ANSI Escape Codes to draw graphics in a text terminal. |
| **`hyper_monitor.c`** | *The Logger* | A background service. Shows how to write a "Daemon" (a program that runs silently in the background). |
| **`hyper_simulator.c`** | *The Stressor* | A native load injector. Shows how to use `pthreads` (Posix Threads) to saturate a multi-core CPU instantly. |

---

## 🚀 How to Run (The "Compiler" Workflow)
Unlike Python, C must be **Compiled** (translated into machine code) before it can run.

### Step 1: Compile
We use `make`, a tool that reads the `Makefile` and runs the compiler (`clang`) with the best optimization settings (`-O3`).
```bash
make clean && make
```

### Step 2: "Native Calibration"
Since C doesn't have our big Python ML models, it uses **Statistical Calibration**. It watches your computer for 30 seconds to learn what "Normal" looks like.
```bash
./engine --calibrate
```

### Step 3: Run
```bash
./engine
```
