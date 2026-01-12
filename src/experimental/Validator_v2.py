"""
Validator_v2.py: Industrial verification script for the V2 ecosystem.
Triggers simulations to test AnomalyEngine_v2.py.
"""
import sys
import argparse
import time
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from Simulator import RAMSimulator, CPUSimulator, NetworkSimulator, DiskSimulator, current_ms

def main():
    parser = argparse.ArgumentParser(description='V2 Anomaly Verification Tool')
    parser.add_argument('type', choices=['cpu', 'ram', 'disk', 'net'], help='Type of anomaly to inject')
    parser.add_argument('--duration', type=int, default=15, help='Duration in seconds')
    args = parser.parse_args()
    
    duration_ms = args.duration * 1000
    
    print(f"🚀 [V2] Triggering {args.type.upper()} Anomaly for {args.duration}s...")
    
    sim = None
    if args.type == 'cpu':
        sim = CPUSimulator({'duration_ms': duration_ms, 'target_load': 100})
    elif args.type == 'ram':
        sim = RAMSimulator({'duration_ms': duration_ms, 'target_gb': 8})
    elif args.type == 'disk':
        sim = DiskSimulator({'duration_ms': duration_ms, 'chunk_size_mb': 50})
    elif args.type == 'net':
        sim = NetworkSimulator({'duration_ms': duration_ms, 'target_mbps': 500})
        
    if sim:
        sim.inject()
        # Since simulators run in threads or background, we wait here to keep process alive if needed
        # But BaseSimulator usually launches threads. 
        # For the demo, we just let it run.
        time.sleep(args.duration + 2)
        print(f"✅ [V2] Injection complete.")
    else:
        print("Error: Simulator failed to initialize.")

if __name__ == "__main__":
    main()
