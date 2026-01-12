#include "telemetry.h"
#include <mach/mach.h>
#include <mach/mach_host.h>
#include <mach/processor_info.h>

static processor_cpu_load_info_t prev_cpu_load = NULL;
static mach_msg_type_number_t prev_cpu_msg_count = 0;

void get_cpu_stats(SystemStats *stats) {
  processor_cpu_load_info_t cpu_load;
  mach_msg_type_number_t cpu_msg_count;
  natural_t processor_count;

  kern_return_t kr = host_processor_info(
      mach_host_self(), PROCESSOR_CPU_LOAD_INFO, &processor_count,
      (processor_info_array_t *)&cpu_load, &cpu_msg_count);
  if (kr != KERN_SUCCESS)
    return;

  if (prev_cpu_load != NULL) {
    double total_all = 0;
    for (int i = 0; i < (int)processor_count && i < MAX_CORES; i++) {
      uint64_t user = cpu_load[i].cpu_ticks[CPU_STATE_USER] -
                      prev_cpu_load[i].cpu_ticks[CPU_STATE_USER];
      uint64_t system = cpu_load[i].cpu_ticks[CPU_STATE_SYSTEM] -
                        prev_cpu_load[i].cpu_ticks[CPU_STATE_SYSTEM];
      uint64_t idle = cpu_load[i].cpu_ticks[CPU_STATE_IDLE] -
                      prev_cpu_load[i].cpu_ticks[CPU_STATE_IDLE];
      uint64_t total = user + system + idle;

      if (total > 0) {
        stats->cpu_load[i] = (double)(user + system) / total * 100.0;
        total_all += stats->cpu_load[i];
      }
    }
    stats->cpu_total_load = total_all / processor_count;
    vm_deallocate(mach_task_self(), (vm_address_t)prev_cpu_load,
                  prev_cpu_msg_count * sizeof(int));
  }
  prev_cpu_load = cpu_load;
  prev_cpu_msg_count = cpu_msg_count;
}

void get_mem_stats(SystemStats *stats) {
  vm_size_t page_size;
  mach_port_t host_port = mach_host_self();
  mach_msg_type_number_t count = HOST_VM_INFO64_COUNT;
  vm_statistics64_data_t vm_stats;
  host_page_size(host_port, &page_size);
  if (host_statistics64(host_port, HOST_VM_INFO64, (host_info64_t)&vm_stats,
                        &count) == KERN_SUCCESS) {
    uint64_t free_mem = (uint64_t)vm_stats.free_count * page_size;
    uint64_t active_mem = (uint64_t)vm_stats.active_count * page_size;
    stats->mem_used = active_mem;
    stats->mem_free = free_mem;
    stats->mem_percent =
        (double)stats->mem_used / (stats->mem_used + stats->mem_free) * 100.0;
  }
}
