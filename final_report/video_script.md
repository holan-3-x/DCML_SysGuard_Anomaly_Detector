# 🎬 Video Recording Script (5 Minutes)
## DCML 2025: Anomaly Detection System Demo

**Total Duration**: 5:00 minutes

---

## Segment 1: Introduction (0:00 - 0:45)

### What to Show
- **Screen**: Display the project's README.md on GitHub or in VS Code.

### Script
> "Hello, I'm presenting my DCML 2025 project: an Advanced Anomaly Detection System built for the Apple M4 Pro.
>
> This system uses Machine Learning to detect when your computer is under stress—whether it's the CPU being maxed out, RAM filling up, or the Disk being overworked.
>
> What makes this project unique is its **dual-ecosystem architecture**:
> - A **Python** ecosystem for intelligent Machine Learning.
> - A **C** ecosystem for ultra-low latency verification.
>
> Let me show you how it works."

---

## Segment 2: Data Collection Demonstration (0:45 - 1:30)

### What to Show
- **Terminal 1**: Run `python3 src/DataCollector.py`
- Show the CSV file being populated in real-time.

### Script
> "First, we need data. The `DataCollector.py` script acts as a sensor.
>
> It captures CPU load across all 14 cores, memory usage, disk read/write speeds, and network traffic.
>
> Notice that we use **Differential Telemetry**—we calculate the *rate* of change, not just the total. This prevents our AI from getting confused over time."

### Action
- Let it run for about 10-15 seconds, then Ctrl+C.

---

## Segment 3: Model Training - "Extreme Benchmarking" (1:30 - 2:30)

### What to Show
- **Terminal 1**: Run `python3 src/ModelTrainer.py`
- Show the training progress and the final leaderboard.

### Script
> "Now, the magic happens. Instead of picking just one algorithm, we perform **Extreme Benchmarking**.
>
> This script trains **13 different AI models**—Random Forest, Neural Networks, Isolation Forest, SVM, and more.
>
> It then ranks them all by **F1-Score**, which balances precision and recall. The winner is automatically saved as our 'Champion Model'.
>
> [Point to the leaderboard] As you can see, Random Forest won with an F1-Score of 0.98."

---

## Segment 4: Real-Time Detection Demo (2:30 - 4:00)

### What to Show
- **Terminal 1**: Run `python3 src/AnomalyEngine.py`
- **Terminal 2**: Inject stress using `python3 src/Validator.py cpu`

### Script
> "Here's the real-time dashboard. It's using the Champion Model we just trained.
>
> Right now, everything is 'SECURE'. Let me inject some stress...
>
> [Run CPU stress] I'm now saturating all 14 cores.
>
> [Point to dashboard] Watch the dashboard—it immediately detects the anomaly and correctly identifies **CPU** as the root cause.
>
> [Stop CPU, then run RAM stress] Now let's try RAM...
>
> [Point to dashboard] And it correctly shows **MEMORY**.
>
> This is the power of our **Hybrid Detection**—it combines ML inference with raw system checks to never miss an obvious problem."

---

## Segment 5: C-Language Verification (4:00 - 4:45)

### What to Show
- **Terminal 1**: Run `cd src_c && make && ./engine --calibrate`
- Then run `./engine`

### Script
> "But what if Python is too slow? What if we need to monitor with almost zero overhead?
>
> That's why we built the **C Hyper-Suite**.
>
> [Run calibrate] Here, the C version is 'learning' the system's baseline using statistics—no Machine Learning, just pure math.
>
> [Run engine] And now it runs...
>
> This C dashboard has less than **1 millisecond latency**. It talks directly to the Mach Kernel using syscalls, bypassing all the Python overhead.
>
> This proves that our anomaly detection works at both the 'smart' level (Python/ML) and the 'fast' level (C/Statistics)."

---

## Segment 6: Conclusion (4:45 - 5:00)

### What to Show
- **Screen**: Show the project structure or the README's "Further Reading" section.

### Script
> "To summarize: this project demonstrates how Machine Learning can be applied to real-time system monitoring.
>
> We used 13 algorithms, dual ecosystems, and hybrid detection to build a robust, educational anomaly detection system.
>
> Thank you for watching."

---

## 📝 Recording Checklist
- [ ] Clean terminal (use `clear` before each segment)
- [ ] Large font size (Cmd + to zoom in terminal)
- [ ] Close unnecessary apps to reduce noise
- [ ] Record screen + audio together (use QuickTime or OBS)
- [ ] Save as `dcml_demo.mp4` in `final_report/`

---
*Script prepared for DCML 2025 Video Submission.*
