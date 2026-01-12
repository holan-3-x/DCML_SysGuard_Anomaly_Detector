#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <stdbool.h>
#include <time.h>
#include <string.h>
#include <unistd.h>
#include <pthread.h>

#define MAX_CORES 16
#define DATA_FILE "monitored_data_c.csv"

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
    
    // Disk
    uint64_t disk_read;
    uint64_t disk_write;
    
    // Network
    uint64_t net_in;
    uint64_t net_out;
    
    // Label
    char injector[32];
} SystemStats;

#endif
