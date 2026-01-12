#include "common.h"
#include "telemetry.h"
#include <ifaddrs.h>
#include <net/if.h>
#include <net/if_dl.h>
#include <net/if_var.h>

#define HISTORY_LEN 40
#define CALIBRATION_STEPS 30
#define THRESHOLD 3.0

// UI Constants
#define RESET "\033[0m"
#define BOLD "\033[1m"
#define RED "\033[1;31m"
#define GREEN "\033[1;32m"
#define YELLOW "\033[1;33m"
#define BLUE "\033[1;34m"
#define CYAN "\033[1;36m"
#define BG_BLUE "\033[44m"

// Global for differential IO
static uint64_t prev_net_in = 0;
static uint64_t prev_net_out = 0;

void get_io_stats(SystemStats *stats, double dt) {
  // Network Rates
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
    stats->net_load_score =
        (double)((ibytes - prev_net_in) + (obytes - prev_net_out)) / 1024.0 /
        dt;
  }
  prev_net_in = ibytes;
  prev_net_out = obytes;

  // Disk Rate (Simplified: if CPU is extremely busy but memory is low, we check
  // for IO wait signatures) For this dashboard, we'll focus on the core
  // metrics.
}

void calibrate(Baseline *b) {
  printf(BG_BLUE BOLD " ⚙️ STARTING NATIVE C-CALIBRATION (30 Steps) " RESET
                      "\n");
  SystemStats s;
  double c_sum = 0, m_sum = 0, n_sum = 0;
  double c_sq = 0, m_sq = 0, n_sq = 0;

  for (int i = 0; i < CALIBRATION_STEPS; i++) {
    get_cpu_stats(&s);
    get_mem_stats(&s);
    get_io_stats(&s, 0.3);

    c_sum += s.cpu_total_load;
    m_sum += s.mem_percent;
    n_sum += s.net_load_score;
    c_sq += s.cpu_total_load * s.cpu_total_load;
    m_sq += s.mem_percent * s.mem_percent;
    n_sq += s.net_load_score * s.net_load_score;

    printf("\rProgress: [%d/%d] CPU: %.1f%% | RAM: %.1f%% | Net: %.1fKB/s",
           i + 1, CALIBRATION_STEPS, s.cpu_total_load, s.mem_percent,
           s.net_load_score);
    fflush(stdout);
    usleep(300000);
  }

  b->avg_cpu = c_sum / CALIBRATION_STEPS;
  b->avg_mem = m_sum / CALIBRATION_STEPS;
  b->avg_net = n_sum / CALIBRATION_STEPS;
  b->std_cpu =
      sqrt((c_sq / CALIBRATION_STEPS) - (b->avg_cpu * b->avg_cpu)) + 0.1;
  b->std_mem =
      sqrt((m_sq / CALIBRATION_STEPS) - (b->avg_mem * b->avg_mem)) + 0.1;
  b->std_net =
      sqrt((n_sq / CALIBRATION_STEPS) - (b->avg_net * b->avg_net)) + 1.0;

  FILE *f = fopen(BASELINE_FILE, "wb");
  fwrite(b, sizeof(Baseline), 1, f);
  fclose(f);
  printf("\n" GREEN "✅ Baseline Established." RESET "\n");
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
  printf(" %.1f", val);
}

void render_dashboard(SystemStats *stats, Baseline b, double history[]) {
  double cz = fabs(stats->cpu_total_load - b.avg_cpu) / b.std_cpu;
  double mz = fabs(stats->mem_percent - b.avg_mem) / b.std_mem;
  double nz = fabs(stats->net_load_score - b.avg_net) / b.std_net;

  const char *cause = "NORMAL";
  bool anomaly = false;
  if (cz > THRESHOLD || mz > THRESHOLD || nz > THRESHOLD) {
    anomaly = true;
    if (cz >= mz && cz >= nz)
      cause = "CPU";
    else if (mz >= cz && mz >= nz)
      cause = "MEMORY";
    else
      cause = "NETWORK";
  }

  printf("\033[H\033[J");
  printf(BG_BLUE BOLD " 🚀 M4 PRO HYPER-ENGINE | %-7s | %s " RESET "\n\n",
         cause, anomaly ? RED "⚠️ ANOMALY" : GREEN "🛡️ SECURE");

  printf(BOLD "--- LIVE TELEMETRY ---" RESET "\n");
  printf("CPU LOAD: ");
  draw_bar(stats->cpu_total_load, 100, 20);
  printf(" %%\n");
  printf("RAM UTIL: ");
  draw_bar(stats->mem_percent, 100, 20);
  printf(" %%\n");
  printf("NET RATE: ");
  draw_bar(stats->net_load_score, 512, 20);
  printf(" KB/s\n\n");

  printf(BOLD "--- INFERENCE (Z-SCORES) ---" RESET "\n");
  printf("CPU: %s%.2f%s | MEM: %s%.2f%s | NET: %s%.2f%s\n\n",
         cz > THRESHOLD ? RED : GREEN, cz, RESET, mz > THRESHOLD ? RED : GREEN,
         mz, RESET, nz > THRESHOLD ? RED : GREEN, nz, RESET);

  printf(BOLD "--- HISTORY ---" RESET "\n");
  for (int i = 0; i < HISTORY_LEN; i++) {
    if (history[i] > THRESHOLD)
      printf(RED "█" RESET);
    else if (history[i] > 1.0)
      printf(YELLOW "▄" RESET);
    else
      printf(GREEN "_" RESET);
  }
  printf("\n\n" CYAN "Press Ctrl+C to exit" RESET "\n");
}

int main(int argc, char **argv) {
  Baseline b;
  if (argc > 1 && strcmp(argv[1], "--calibrate") == 0)
    calibrate(&b);
  else {
    FILE *f = fopen(BASELINE_FILE, "rb");
    if (!f)
      calibrate(&b);
    else {
      fread(&b, sizeof(Baseline), 1, f);
      fclose(f);
    }
  }

  SystemStats stats;
  double history[HISTORY_LEN] = {0};
  int h_idx = 0;
  while (1) {
    get_cpu_stats(&stats);
    get_mem_stats(&stats);
    get_io_stats(&stats, 0.4);

    double cz = fabs(stats.cpu_total_load - b.avg_cpu) / b.std_cpu;
    double mz = fabs(stats.mem_percent - b.avg_mem) / b.std_mem;
    double nz = fabs(stats.net_load_score - b.avg_net) / b.std_net;
    double max_z = (cz > mz) ? (cz > nz ? cz : nz) : (mz > nz ? mz : nz);

    history[h_idx % HISTORY_LEN] = max_z;
    h_idx++;
    render_dashboard(&stats, b, history);
    usleep(400000);
  }
  return 0;
}
