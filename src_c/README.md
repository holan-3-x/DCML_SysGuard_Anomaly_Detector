# ⚡ C-Language Hyper-Suite (M4 Pro Native)

This is the standalone, high-performance C implementation of the DCML Anomaly Detection system. It is designed to run with zero dependency on Python for monitoring and real-time inference.

## 🚀 Native C-Workflow

### 1. Build the Suite
Compile all modules (Monitor, Simulator, Engine) using the optimized Clang flags.
```bash
cd src_c
make clean && make
```

### 2. Native Calibration (The C-Way)
Unlike the Python version that needs massive datasets, the C-suite uses a **Native Calibration** mode. It "learns" your M4 Pro's idle state in 30 seconds to establish a high-accuracy baseline.
```bash
./engine --calibrate
```
*Creates: `baseline.bin`*

### 3. Launch the Dashboard
Run the premium terminal UI to monitor your system in real-time.
```bash
./engine
```

### 4. High-Frequency Telemetry
If you only need to record data to a CSV without the dashboard.
```bash
./monitor
```

### 5. Native Stress Testing
Trigger anomalies manually using the C-simulator.
```bash
./simulator cpu   # Saturation 14 cores
./simulator ram   # Memory Burn (4GB)
./simulator disk  # High IO Burst
```

---

## 🏗️ Architecture
- **`telemetry.c`**: Direct Mach Kernel syscalls for CPU and RAM.
- **`hyper_monitor.c`**: Background data logger (Differential Rate logic).
- **`hyper_engine.c`**: Interactive Dashboard and Z-Score Inference.
- **`hyper_simulator.c`**: Native macOS stress patterns.

## ⚖️ Diagnostic Logic
The C-suite uses **Mean Category Deviation** to ensure that CPU cores do not overpower RAM or Disk stats. This ensures that every anomaly is diagnosed with its true root cause.
