from LoadInjector import CPUStressInjection, DiskStressInjection, MemoryStressInjection, NetworkStressInjection
import time
import sys

def main(mode="cpu"):
    if mode == "cpu":
        print("Injecting CPU Stress anomaly (10s)...")
        inj = CPUStressInjection(tag="TEST_CPU", duration_ms=10000, target_load=90)
    elif mode == "disk":
        print("Injecting Disk Stress anomaly (10s)...")
        inj = DiskStressInjection(tag="TEST_DISK", duration_ms=10000, file_size_mb=500)
    elif mode == "ram" or mode == "memory":
        print("Injecting RAM Stress anomaly (10s)...")
        # items_for_loop=12345678 is a high stress for M4 Pro
        inj = MemoryStressInjection(tag="TEST_RAM", duration_ms=10000, items_for_loop=12345678)
    elif mode == "net" or mode == "network":
        print("Injecting Network Stress anomaly (10s)...")
        inj = NetworkStressInjection(tag="TEST_NET", duration_ms=10000, urls_file='websites_urls.csv')
    else:
        print("Unknown mode. Use 'cpu', 'disk', 'ram', or 'net'.")
        return

    inj.inject()
    while not inj.completed_flag:
        time.sleep(1)
    print("\n[DONE] Injection finished.")

if __name__ == '__main__':
    m = sys.argv[1].lower() if len(sys.argv) > 1 else "cpu"
    main(m)
