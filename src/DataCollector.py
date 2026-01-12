"""
DataCollector.py: High-frequency system telemetry and monitoring engine.
This script gathers real-time metrics (CPU, RAM, Disk, Net) and logs them for AI training.
Optimized for MacBook Pro M4 Pro.
"""
import csv
import os.path
import time
import psutil
from tqdm import tqdm
import json
import os.path
import random
from typing import List

from Simulator import BaseSimulator, current_ms

# Global cache for differential telemetry
_prev_stats = {
    'time': time.time(),
    'disk_io': None,
    'net_io': None
}

def read_scenarios(json_path, inj_duration: int = 2, verbose: bool = True, n_inj: int = -1) -> List[BaseSimulator]:
    """
    Method to read a JSON file and extract simulation scenarios
    """
    try:
        if os.path.exists(json_path):
            with open(json_path) as f:
                config_data = json.load(f)
                scenarios = config_data.get('simulation_scenarios', config_data)
        else:
            print(f"Could not find config file {json_path}")
            return []
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return []
    
    available_sims = []
    for scenario in scenarios:
        # Update duration from global param if needed
        if 'params' in scenario:
            scenario['params']['duration_ms'] = inj_duration
        else:
            scenario['duration_ms'] = inj_duration
            
        new_sim = BaseSimulator.from_scenario(scenario)
        if new_sim:
            available_sims.append(new_sim)
            if verbose: print(f'Simulation scenario loaded: {new_sim.get_name()}')
    
    if n_inj != -1 and n_inj > len(available_sims):
        # Fill to reached n_inj
        base_pool = list(available_sims)
        while len(available_sims) < n_inj:
            available_sims.append(random.choice(base_pool))

    return available_sims

def monitor_system() -> dict:
    """
    Method to monitor system
    :return: dictionary with informations about the system
    """
    # Initialize with primary columns first as requested
    now = time.time()
    ret_dict = {
        'Timestamp': now,
        'UserReadTime': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now))
    }

    cpu_times_percent = psutil.cpu_times_percent(interval=0.005, percpu=True)
    cpu_percent = psutil.cpu_percent(interval=0.05, percpu=True)
    cpu_freq = psutil.cpu_freq(percpu=True)
    virtual_memory = psutil.virtual_memory()._asdict() 

    ret_dict.update({str(i)+k: v for i, d in enumerate(cpu_times_percent) for k, v in d._asdict().items()})
    ret_dict.update({f'load{i}': v for i, v in enumerate(cpu_percent)})
    ret_dict.update({str(i)+k: v for i, d in enumerate(cpu_freq) for k, v in d._asdict().items()})
    ret_dict.update({'virtual_'+k:v for k, v in virtual_memory.items()})
    
    # Deep Memory & Swap
    ret_dict.update({'swap_'+k: v for k, v in psutil.swap_memory()._asdict().items()})
    
    global _prev_stats
    
    # 1. Differential Disk Telemetry
    disk_usage = psutil.disk_usage('/')._asdict()
    current_disk_io = psutil.disk_io_counters()._asdict()
    
    dt = now - _prev_stats['time']
    if dt <= 0: dt = 0.001 # Prevent div by zero
    
    if _prev_stats['disk_io'] is None:
        # First run: Initialize with 0 rates
        disk_rates = {f'disk_io_{k}_rate': 0.0 for k in current_disk_io.keys()}
    else:
        disk_rates = {f'disk_io_{k}_rate': (current_disk_io[k] - _prev_stats['disk_io'][k]) / dt for k in current_disk_io.keys()}
        
    ret_dict.update({'disk_usage_'+k: v for k, v in disk_usage.items()})
    ret_dict.update(disk_rates)
    
    # 2. Differential Network Telemetry
    current_net_io = psutil.net_io_counters()._asdict()
    if _prev_stats['net_io'] is None:
        net_rates = {f'net_io_{k}_rate': 0.0 for k in current_net_io.keys()}
    else:
        net_rates = {f'net_io_{k}_rate': (current_net_io[k] - _prev_stats['net_io'][k]) / dt for k in current_net_io.keys()}
    
    ret_dict.update(net_rates)

    # Update cache for next step
    _prev_stats['time'] = now
    _prev_stats['disk_io'] = current_disk_io
    _prev_stats['net_io'] = current_net_io

    # Count active connections as a feature
    try:
        ret_dict['net_connections_count'] = len(psutil.net_connections(kind='inet'))
    except Exception:
        ret_dict['net_connections_count'] = 0
    
    return ret_dict

def main(out_filename: str, obs_interval_sec: float, obs_per_inj: int, obs_between_inj: int, simulators: List[BaseSimulator], verbose: bool = True) -> None:
    """
    Method to perform monitoring during various load tests
    """

    # Checking of out_filename already exists: if yes, delete
    if os.path.exists(out_filename):
        os.remove(out_filename)

    # Variable setup
    first_step = True
    inj_now = None
    obs_left_to_change = obs_between_inj

    # Monitoring Loop
    with open(out_filename, "a", newline="") as csvfile:
        #for obs_count in tqdm(range(max_n_obs), desc='Monitor Progress Bar'):
        while True:
            if obs_left_to_change<=0 and inj_now is None:
                # Start next Simulation
                obs_left_to_change = obs_per_inj
                if len(simulators) == 0: 
                    break
                inj_now = simulators.pop(0)
                if verbose: print(f"{time.time()} | Simulating {inj_now.get_name()}|Remaining: {len(simulators)}")
                inj_now.inject()
            elif obs_left_to_change<=0 and inj_now is not None:
                # Pause from Injections
                if verbose: print(f"{time.time()}|Ending Injection")
                inj_now = None
                obs_left_to_change = obs_between_inj*random.choice([0.6, 0.8, 1, 1.2, 1.4]) # casually increment or decrement the length of the pause between injections

            start_time = time.time()
            data_to_log = monitor_system()
            data_to_log['injector'] = 'rest' if inj_now is None else inj_now.get_name() # add label column

            # Writing as a new line of a CSV file
            # Create a CSV writer using the field/column names
            writer = csv.DictWriter(csvfile, fieldnames=data_to_log.keys())
            if first_step:
                # Write the header row (column names)
                writer.writeheader()
                first_step = False
            writer.writerow(data_to_log)

            exe_time = time.time() - start_time
            if exe_time < obs_interval_sec:
                # Sleeping to synchronize to the obs-interval
                time.sleep(obs_interval_sec - exe_time)
            else:
                if verbose: print(f"[{inj_now.get_name() if inj_now is not None else 'Rest'}]Warning: execution of the monitor took too long (%.3f sec)" % (exe_time - obs_interval_sec))

            obs_left_to_change -= 1

if __name__ == '__main__':
    import pathlib
    config_json = str(pathlib.Path(__file__).parent.resolve()) + '/simulation_config.json'
    time_step_sec = 0.5 
    obs_per_inj = 10 
    obs_between_inj = 10 
    n_sims = 25 

    # Extracting definitions from input JSON
    simulators = read_scenarios(config_json, 
                            inj_duration=obs_per_inj*time_step_sec*1000,
                            n_inj=n_sims)
    random.shuffle(simulators)

    main(out_filename=str(pathlib.Path(__file__).parent.resolve()) + '/output_folder/monitored_data.csv', 
        obs_interval_sec=time_step_sec,
        obs_per_inj=obs_per_inj,
        obs_between_inj=obs_between_inj,
        simulators=simulators)