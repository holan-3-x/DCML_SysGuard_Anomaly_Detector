#include "common.h"
#include "telemetry.h"
#include <ifaddrs.h>
#include <net/if.h>
#include <net/if_dl.h>
#include <net/if_var.h>

static uint64_t prev_net_in = 0;
static uint64_t prev_net_out = 0;
static double prev_time = 0;

void get_io_stats(SystemStats *stats, double dt) {
  struct ifaddrs *ifa_list, *ifa;
  uint64_t ibytes = 0, obytes = 0;
  if (getifaddrs(&ifa_list) != -1) {
    for (ifa = ifa_list; ifa; ifa = ifa->ifa_next) {
      if (ifa->ifa_addr->sa_family == AF_LINK) {
        struct if_data *ifd = (struct if_data *)ifa->ifa_data;
        ibytes += ifd->ifi_ibytes;
        obytes += ifd->ifi_obytes;
      }
    }
    freeifaddrs(ifa_list);
  }
  if (prev_net_in > 0 && dt > 0) {
    stats->net_in_bytes = (ibytes - prev_net_in) / dt;
    stats->net_out_bytes = (obytes - prev_net_out) / dt;
    stats->net_load_score =
        (double)(stats->net_in_bytes + stats->net_out_bytes) / 1024.0;
  }
  prev_net_in = ibytes;
  prev_net_out = obytes;
}

int main() {
  printf("🚀 C-HyperMonitor: Starting Data Collection Loop...\n");
  FILE *f = fopen(DATA_FILE, "w");
  fprintf(f,
          "Timestamp,UserReadTime,CPU_Total,Mem_Percent,Net_KBps,Injector\n");
  SystemStats stats;
  memset(&stats, 0, sizeof(stats));
  strcpy(stats.injector, "rest");
  while (1) {
    double now = (double)time(NULL);
    double dt = (prev_time > 0) ? now - prev_time : 0.5;
    get_cpu_stats(&stats);
    get_mem_stats(&stats);
    get_io_stats(&stats, dt);
    time_t t = (time_t)now;
    strftime(stats.user_read_time, 32, "%Y-%m-%d %H:%M:%S", localtime(&t));
    printf("\r[%s] CPU: %.1f%% | RAM: %.1f%% | Net: %.1f KB/s",
           stats.user_read_time, stats.cpu_total_load, stats.mem_percent,
           stats.net_load_score);
    fflush(stdout);
    fprintf(f, "%.3f,%s,%.2f,%.2f,%.2f,%s\n", now, stats.user_read_time,
            stats.cpu_total_load, stats.mem_percent, stats.net_load_score,
            stats.injector);
    fflush(f);
    prev_time = now;
    usleep(500000);
  }
  fclose(f);
  return 0;
}
