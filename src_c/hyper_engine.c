#include "common.h"
#include <math.h>

#define THRESHOLD 2.5

typedef struct {
  double cpu_z;
  double mem_z;
  double net_z;
} ZScores;

const char *identify_cause(ZScores z) {
  double max_z = z.cpu_z;
  const char *cause = "CPU";

  if (z.mem_z > max_z) {
    max_z = z.mem_z;
    cause = "MEMORY";
  }
  if (z.net_z > max_z) {
    max_z = z.net_z;
    cause = "NETWORK";
  }

  return (max_z > THRESHOLD) ? cause : "NORMAL";
}

void detect(SystemStats *stats, double avg_cpu, double std_cpu, double avg_mem,
            double std_mem) {
  ZScores z;
  z.cpu_z = fabs(stats->cpu_total_load - avg_cpu) / (std_cpu + 0.01);
  z.mem_z = fabs(stats->mem_percent - avg_mem) / (std_mem + 0.01);
  z.net_z = 0.0; // Network baseline omitted for simplicity in demo

  const char *cause = identify_cause(z);

  printf("\r[C-ENGINE] CPU: %.1f%% | RAM: %.1f%% | Cause: ",
         stats->cpu_total_load, stats->mem_percent);

  if (strcmp(cause, "NORMAL") != 0) {
    printf("\033[1;31m⚠️ %s ANOMALY ⚠️\033[0m   ", cause);
  } else {
    printf("\033[1;32m🛡️ SECURE\033[0m                ");
  }
  fflush(stdout);
}

int main() {
  printf("🚀 Starting C-HyperEngine-v2 (Multi-Category Diagnostics)...\n");

  // Mock baselines
  double avg_cpu = 15.0, std_cpu = 5.0;
  double avg_mem = 40.0, std_mem = 2.0;

  SystemStats stats;
  memset(&stats, 0, sizeof(stats));

  for (int i = 0; i < 100; i++) {
    // Mocking a spike
    if (i > 30 && i < 50) {
      stats.cpu_total_load = 92.0;
      stats.mem_percent = 42.0;
    } else if (i > 60 && i < 80) {
      stats.cpu_total_load = 15.0;
      stats.mem_percent = 85.0;
    } else {
      stats.cpu_total_load = 10.0 + (rand() % 10);
      stats.mem_percent = 40.0 + (rand() % 2);
    }

    detect(&stats, avg_cpu, std_cpu, avg_mem, std_mem);
    usleep(100000);
  }
  printf("\n✅ C-Detection finished.\n");
  return 0;
}
