"""
Validator.py: One-click verification tool to trigger manual system stress.
Use this to test if the AnomalyEngine correctly detects high load on CPU, RAM, Disk, or Network.
"""
from Simulator import CPUSimulator, DiskSimulator, RAMSimulator, NetworkSimulator
import time
import sys

def main(mode="cpu"):
    if mode == "cpu":
        print("🚀 [M4 Pro] Triggering CPU Stress simulation (10s)...")
        sim = CPUSimulator(tag="VALIDATOR_CPU", duration_ms=10000, target_load=95)
    elif mode == "disk":
        print("🚀 [M4 Pro] Triggering Disk Stress simulation (10s)...")
        sim = DiskSimulator(tag="VALIDATOR_DISK", duration_ms=10000, file_size_mb=2000)
    elif mode == "ram" or mode == "memory":
        print("🚀 [M4 Pro] Triggering RAM Stress simulation (10s)...")
        # RAMSimulator uses numpy for aggressive allocation
        sim = RAMSimulator(tag="VALIDATOR_RAM", duration_ms=10000)
    elif mode == "net" or mode == "network":
        print("🚀 [M4 Pro] Triggering Network Stress simulation (10s)...")
        sim = NetworkSimulator(tag="VALIDATOR_NET", duration_ms=10000, urls_file='websites_urls.csv')
    else:
        print("Unknown mode. Use 'cpu', 'disk', 'ram', or 'net'.")
        return

    sim.inject()
    while not sim.completed_flag:
        time.sleep(1)
    print("\n✅ Simulation cycle finished.")

if __name__ == '__main__':
    m = sys.argv[1].lower() if len(sys.argv) > 1 else "cpu"
    main(m)
