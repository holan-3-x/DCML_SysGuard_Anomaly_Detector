import os
import pathlib
import threading
import time
import random
import platform
import multiprocessing
import requests
try:
    from cpu_load_generator import load_all_cores as _load_all_cores, load_single_core as _load_single_core
except ImportError:
    _load_all_cores = None
    _load_single_core = None

def busy_loop(duration_s, target_load):
    start = time.time()
    while time.time() - start < duration_s:
        interval = 0.1
        busy_time = interval * target_load
        sleep_time = interval * (1 - target_load)
        loop_start = time.time()
        while time.time() - loop_start < busy_time:
            pass
        if sleep_time > 0:
            time.sleep(sleep_time)

def load_all_cores(duration_s, target_load):
    if platform.system() != 'Darwin' and _load_all_cores:
        return _load_all_cores(duration_s=duration_s, target_load=target_load)
    
    procs = []
    for _ in range(multiprocessing.cpu_count()):
        p = multiprocessing.Process(target=busy_loop, args=(duration_s, target_load))
        p.start()
        procs.append(p)
    for p in procs:
        p.join()

def load_single_core(core_num, duration_s, target_load):
    if platform.system() != 'Darwin' and _load_single_core:
        return _load_single_core(core_num=core_num, duration_s=duration_s, target_load=target_load)
    
    # Simple busy loop on a single process (no affinity on Mac)
    p = multiprocessing.Process(target=busy_loop, args=(duration_s, target_load))
    p.start()
    p.join()

def current_ms():
    """
    Reports the current time in milliseconds
    :return: long int
    """
    return round(time.time() * 1000)

class LoadInjector:
    """
    Abstract class for Injecting Errors in the System probes
    """

    def __init__(self, tag: str = '', duration_ms: float = 1000):
        """
        Constructor
        """
        self.valid = True
        self.tag = tag
        self.duration_ms = duration_ms
        self.inj_thread = None
        self.completed_flag = True
        self.injected_interval = []
        self.init()

    def is_valid(self):
        return self.valid

    def init(self):
        """
        Override needed only if the injector needs some pre-setup to be run. Default is an empty method
        :return:
        """
        pass

    def inject_body(self):
        """
        Abstract method to be overridden
        """
        pass

    def inject(self):
        """
        Caller of the body of the injection mechanism, which will be executed in a separate thread
        """
        self.inj_thread = threading.Thread(target=self.inject_body, args=())
        self.inj_thread.start()

    def is_injector_running(self):
        """
        True if the injector has finished working (end of the 'injection_body' function)
        """
        return not self.completed_flag

    def force_close(self):
        """
        Try to force-close the injector
        """
        pass

    def get_injections(self) -> list:
        """
        Returns start-end times of injections exercised with this method
        """
        return self.injected_interval

    def get_name(self) -> str:
        """
        Abstract method to be overridden
        """
        return "[" + self.tag + "]Injector" + "(d" + str(self.duration_ms) + ")"

    @classmethod
    def fromJSON(cls, job):
        if job is not None:
            if 'type' in job:
                if job['type'] in {'Memory', 'RAM', 'MemoryUsage', 'Mem', 'MemoryStress'}:
                    return MemoryStressInjection.fromJSON(job)
                if job['type'] in {'CPU', 'Proc', 'CPUUsage', 'CPUStress'}:
                    return CPUStressInjection.fromJSON(job)
                if job['type'] in {'Disk', 'DiskStress', 'IO'}:
                    return DiskStressInjection.fromJSON(job)
                if job['type'] in {'Network', 'Net', 'NetworkStress'}:
                    return NetworkStressInjection.fromJSON(job)
        return None


class CPUStressInjection(LoadInjector):
    """
    CPUStress Error
    """

    def __init__(self, tag: str = '', duration_ms: float = 1000, target_load: int = 70, target_core: int = -1):
        """
        Constructor
        """
        self.target_load = int(target_load*random.choice([0.9, 1, 1.1]))
        self.target_core = target_core
        LoadInjector.__init__(self, tag, duration_ms)

    def inject_body(self):
        self.completed_flag = False
        start_time = current_ms()

        if self.target_core == -1:
            load_all_cores(duration_s=self.duration_ms/1000,
                       target_load=self.target_load/100)
        else:
            load_single_core(core_num=self.target_core, 
                             duration_s=self.duration_ms/1000,
                             target_load=self.target_load/100)
        
        self.injected_interval.append({'start': start_time, 'end': current_ms()})
        self.completed_flag = True

    def get_name(self) -> str:
        return "[" + self.tag + "]CPUStressInjection" + "(d" + str(self.duration_ms) + "-t"+str(self.target_load)+")"

    @classmethod
    def fromJSON(cls, job):
        return CPUStressInjection(tag=(job['tag'] if 'tag' in job else ''),
                                  duration_ms=(job['duration_ms'] if 'duration_ms' in job else 1000),
                                  target_load=(job['target_load'] if 'target_load' in job else 70),
                                  target_core=(job['target_core'] if 'target_core' in job else -1))

class MemoryStressInjection(LoadInjector):
    """
    Loops and adds data to an array simulating memory usage
    """

    def __init__(self, tag: str = '', duration_ms: float = 1000, items_for_loop: int = 1234567):
        LoadInjector.__init__(self, tag, duration_ms)
        self.items_for_loop = items_for_loop
        self.force_stop = False

    def inject_body(self):
        self.completed_flag = False
        start_time = current_ms()
        my_list = []
        while True:
            my_list.append([999 for _ in range(self.items_for_loop)])
            if current_ms() - start_time > self.duration_ms or self.force_stop:
                break
            else:
                time.sleep(0.0001)

        self.injected_interval.append({'start': start_time, 'end': current_ms()})
        self.completed_flag = True
        self.force_stop = False

    def force_close(self):
        self.force_stop = True

    def get_name(self) -> str:
        return "[" + self.tag + "]MemoryStressInjection(d" + str(self.duration_ms) + "-i" \
               + str(self.items_for_loop) + ")"

    @classmethod
    def fromJSON(cls, job):
        return MemoryStressInjection(tag=(job['tag'] if 'tag' in job else ''),
                                     duration_ms=(job['duration_ms'] if 'duration_ms' in job else 1000),
                                     items_for_loop=(job['items_for_loop']
                                                     if 'items_for_loop' in job else 1234567))

class DiskStressInjection(LoadInjector):
    """
    Stress the disk by writing and reading large files.
    """

    def __init__(self, tag: str = '', duration_ms: float = 1000, file_size_mb: int = 100):
        LoadInjector.__init__(self, tag, duration_ms)
        self.file_size_mb = file_size_mb
        self.force_stop = False

    def inject_body(self):
        self.completed_flag = False
        start_time = current_ms()
        test_file = pathlib.Path(__file__).parent.resolve() / "disk_stress_test.tmp"
        
        try:
            data = os.urandom(10 * 1024 * 1024) # 10MB chunks
            while current_ms() - start_time < self.duration_ms and not self.force_stop:
                with open(test_file, "wb") as f:
                    for _ in range(max(1, self.file_size_mb // 10)):
                        f.write(data)
                        if self.force_stop: break
                with open(test_file, "rb") as f:
                    while f.read(10 * 1024 * 1024):
                        if self.force_stop: break
                time.sleep(0.1)
        except Exception:
            pass
        finally:
            if test_file.exists():
                try:
                    test_file.unlink()
                except Exception:
                    pass

        self.injected_interval.append({'start': start_time, 'end': current_ms()})
        self.completed_flag = True
        self.force_stop = False

    def force_close(self):
        self.force_stop = True

    def get_name(self) -> str:
        return "[" + self.tag + "]DiskStressInjection(d" + str(self.duration_ms) + "-s" + str(self.file_size_mb) + "MB)"

    @classmethod
    def fromJSON(cls, job):
        return DiskStressInjection(tag=(job['tag'] if 'tag' in job else ''),
                                   duration_ms=(job['duration_ms'] if 'duration_ms' in job else 1000),
                                   file_size_mb=(job['file_size_mb'] if 'file_size_mb' in job else 100))

class NetworkStressInjection(LoadInjector):
    """
    Stress the network by repeatedly visiting a list of URLs.
    """

    def __init__(self, tag: str = '', duration_ms: float = 1000, urls_file: str = 'websites_urls.csv'):
        LoadInjector.__init__(self, tag, duration_ms)
        self.urls_file = urls_file
        self.force_stop = False
        self.urls = []
        try:
            path = pathlib.Path(__file__).parent.resolve() / urls_file
            with open(path, 'r') as f:
                self.urls = [line.strip() for line in f if line.strip()]
        except Exception:
            self.urls = ["http://www.google.com", "http://www.github.com"]

    def inject_body(self):
        self.completed_flag = False
        start_time = current_ms()
        
        while current_ms() - start_time < self.duration_ms and not self.force_stop:
            url = random.choice(self.urls)
            if not url.startswith('http'):
                url = 'http://' + url
            try:
                # Use a small timeout to keep it moving fast
                requests.get(url, timeout=2)
            except Exception:
                pass
            time.sleep(0.05)

        self.injected_interval.append({'start': start_time, 'end': current_ms()})
        self.completed_flag = True
        self.force_stop = False

    def force_close(self):
        self.force_stop = True

    def get_name(self) -> str:
        return "[" + self.tag + "]NetworkStressInjection(d" + str(self.duration_ms) + ")"

    @classmethod
    def fromJSON(cls, job):
        return NetworkStressInjection(tag=(job['tag'] if 'tag' in job else ''),
                                      duration_ms=(job['duration_ms'] if 'duration_ms' in job else 1000),
                                      urls_file=(job['urls_file'] if 'urls_file' in job else 'websites_urls.csv'))