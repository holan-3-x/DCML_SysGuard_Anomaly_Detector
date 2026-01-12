#ifndef COMMON_H
#define COMMON_H

#include <math.h>
#include <pthread.h>
#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <unistd.h>

#define MAX_CORES 16
#define DATA_FILE "monitored_data_c.csv"
#define BASELINE_FILE "baseline.bin"

typedef struct {
  double timestamp;
  char user_read_time[32];

  // CPU
  double cpu_load[MAX_CORES];
  double cpu_total_load;

  // Memory
  uint64_t mem_used;
  uint64_t mem_free;
  double mem_percent;

  // Disk (Rates)
  uint64_t disk_read_bytes;
  uint64_t disk_write_bytes;
  double disk_load_score; // Derived rate

  // Network (Rates)
  uint64_t net_in_bytes;
  uint64_t net_out_bytes;
  double net_load_score;

  // Label
  char injector[32];
} SystemStats;

typedef struct {
  double avg_cpu, std_cpu;
  double avg_mem, std_mem;
  double avg_disk, std_disk;
  double avg_net, std_net;
} Baseline;

#endif
