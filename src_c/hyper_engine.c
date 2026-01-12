#include "common.h"
#include <math.h>

#define THRESHOLD 3.0 // Z-score threshold

void detect(SystemStats *stats, double avg_cpu, double std_cpu) {
  double z_cpu = (stats->cpu_total_load - avg_cpu) / (std_cpu + 0.001);

  printf("\r[DETECTOR] CPU: %.1f%% | Z: %.2f | Status: ", stats->cpu_total_load,
         z_cpu);

  if (fabs(z_cpu) > THRESHOLD) {
    printf("\033[1;31m⚠️ ANOMALY DETECTED (C-SPEED) ⚠️\033[0m   ");
  } else {
    printf("\033[1;32m🛡️ SECURE\033[0m                     ");
  }
  fflush(stdout);
}

int main() {
  printf("🚀 Starting C-HyperEngine (Low-Latency Inference)...\n");

  // Baseline (Mocked for demo, usually loaded from a file/training)
  double avg_cpu = 15.0;
  double std_cpu = 5.0;

  SystemStats stats;
  memset(&stats, 0, sizeof(stats));

  // In a real scenario, this would read from the monitor pipe/shared memory
  // For now, it simulates the fast inference loop
  for (int i = 0; i < 100; i++) {
    // Mocking a spike for demo
    stats.cpu_total_load = (i > 40 && i < 60) ? 85.0 : (10.0 + (rand() % 10));
    detect(&stats, avg_cpu, std_cpu);
    usleep(100000); // 100ms
  }
  printf("\n✅ C-Detection test finished.\n");
  return 0;
}
