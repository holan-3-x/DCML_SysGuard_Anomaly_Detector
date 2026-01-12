#include "common.h"
#include "telemetry.h"

#define HISTORY_LEN 40
#define CALIBRATION_STEPS 30

// UI Constants
#define RESET "\033[0m"
#define BOLD "\033[1m"
#define RED "\033[1;31m"
#define GREEN "\033[1;32m"
#define YELLOW "\033[1;33m"
#define BLUE "\033[1;34m"
#define MAGENTA "\033[1;35m"
#define CYAN "\033[1;36m"
#define BG_BLUE "\033[44m"

void calibrate(Baseline *b) {
  printf(BG_BLUE BOLD " ⚙️ STARTING NATIVE C-CALIBRATION (30 Steps) " RESET
                      "\n");
  printf("Establishing baseline for M4 Pro cores and memory...\n");
  SystemStats s;
  double cpu_sum = 0, mem_sum = 0;
  double cpu_sq_sum = 0, mem_sq_sum = 0;
  for (int i = 0; i < CALIBRATION_STEPS; i++) {
    get_cpu_stats(&s);
    get_mem_stats(&s);
    cpu_sum += s.cpu_total_load;
    mem_sum += s.mem_percent;
    cpu_sq_sum += s.cpu_total_load * s.cpu_total_load;
    mem_sq_sum += s.mem_percent * s.mem_percent;
    printf("\rProgress: [%d/%d] CPU: %.1f%% | RAM: %.1f%%", i + 1,
           CALIBRATION_STEPS, s.cpu_total_load, s.mem_percent);
    fflush(stdout);
    usleep(300000);
  }
  b->avg_cpu = cpu_sum / CALIBRATION_STEPS;
  b->avg_mem = mem_sum / CALIBRATION_STEPS;
  b->std_cpu =
      sqrt((cpu_sq_sum / CALIBRATION_STEPS) - (b->avg_cpu * b->avg_cpu)) + 0.1;
  b->std_mem =
      sqrt((mem_sq_sum / CALIBRATION_STEPS) - (b->avg_mem * b->avg_mem)) + 0.1;
  b->avg_disk = 1.0;
  b->std_disk = 2.0;
  b->avg_net = 5.0;
  b->std_net = 10.0;
  FILE *f = fopen(BASELINE_FILE, "wb");
  fwrite(b, sizeof(Baseline), 1, f);
  fclose(f);
  printf("\n" GREEN "✅ Calibration complete! Saved to %s" RESET "\n",
         BASELINE_FILE);
  sleep(1);
}

void draw_bar(double val, double max_val, int width) {
  int done = (int)((val / max_val) * width);
  if (done > width)
    done = width;
  if (done < 0)
    done = 0;
  const char *color = (val > 80) ? RED : (val > 50) ? YELLOW : GREEN;
  printf("%s", color);
  for (int i = 0; i < done; i++)
    printf("█");
  printf(RESET);
  for (int i = 0; i < width - done; i++)
    printf("░");
  printf(" %.1f%%", val);
}

void render_dashboard(SystemStats *stats, Baseline b, double history[]) {
  double cpu_z = fabs(stats->cpu_total_load - b.avg_cpu) / b.std_cpu;
  double mem_z = fabs(stats->mem_percent - b.avg_mem) / b.std_mem;
  const char *cause = "NORMAL";
  bool anomaly = false;
  if (cpu_z > 3.0 || mem_z > 3.0) {
    anomaly = true;
    cause = (cpu_z > mem_z) ? "CPU" : "MEMORY";
  }
  printf("\033[H\033[J");
  printf(BG_BLUE BOLD " 🚀 M4 PRO C-DASHBOARD | %s | %s " RESET "\n\n", cause,
         anomaly ? RED "⚠️ ANOMALY" : GREEN "🛡️ SECURE");
  printf(BOLD "--- LIVE PERFORMANCE ---" RESET "\n");
  printf("CPU CORES: ");
  draw_bar(stats->cpu_total_load, 100, 20);
  printf("\n");
  printf("MEM USAGE: ");
  draw_bar(stats->mem_percent, 100, 20);
  printf("\n\n");
  printf(BOLD "--- DIAGNOSTICS ---" RESET "\n");
  printf("CPU Z-Score: %s%.2f%s\n", cpu_z > 3.0 ? RED : GREEN, cpu_z, RESET);
  printf("MEM Z-Score: %s%.2f%s\n\n", mem_z > 3.0 ? RED : GREEN, mem_z, RESET);
  printf(BOLD "--- HISTORY ---" RESET "\n");
  for (int i = 0; i < HISTORY_LEN; i++) {
    if (history[i] > 3.0)
      printf(RED "█" RESET);
    else if (history[i] > 1.5)
      printf(YELLOW "▄" RESET);
    else
      printf(GREEN "_" RESET);
  }
  printf("\n\n" CYAN "Press Ctrl+C to Stop" RESET "\n");
}

int main(int argc, char **argv) {
  Baseline b;
  bool force_calibrate = (argc > 1 && strcmp(argv[1], "--calibrate") == 0);
  FILE *f = fopen(BASELINE_FILE, "rb");
  if (!f || force_calibrate)
    calibrate(&b);
  else {
    fread(&b, sizeof(Baseline), 1, f);
    fclose(f);
  }
  SystemStats stats;
  double history[HISTORY_LEN] = {0};
  int h_idx = 0;
  while (1) {
    get_cpu_stats(&stats);
    get_mem_stats(&stats);
    double cpu_z = fabs(stats.cpu_total_load - b.avg_cpu) / b.std_cpu;
    double mem_z = fabs(stats.mem_percent - b.avg_mem) / b.std_mem;
    double max_z = (cpu_z > mem_z) ? cpu_z : mem_z;
    history[h_idx % HISTORY_LEN] = max_z;
    h_idx++;
    render_dashboard(&stats, b, history);
    usleep(400000);
  }
  return 0;
}
