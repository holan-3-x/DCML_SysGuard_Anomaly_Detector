#include "common.h"

void *cpu_stress(void *arg) {
  printf("🔥 [C] Saturating CPU Core...\n");
  int duration = *(int *)arg;
  time_t start = time(NULL);
  while (time(NULL) - start < duration) {
    for (volatile int i = 0; i < 1000000; i++)
      ; // Busy loop
  }
  return NULL;
}

void ram_stress(int duration_s) {
  printf("🧠 [C] Allocating 4GB RAM...\n");
  size_t size = 4ULL * 1024 * 1024 * 1024;
  char *ptr = malloc(size);
  if (!ptr)
    return;

  time_t start = time(NULL);
  while (time(NULL) - start < duration_s) {
    memset(ptr, 0xFF, size); // Heavy write
    usleep(100000);
  }
  free(ptr);
}

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: %s <cpu|ram|disk|net> [duration]\n", argv[0]);
    return 1;
  }

  int duration = (argc > 2) ? atoi(argv[2]) : 10;
  char *mode = argv[1];

  if (strcmp(mode, "cpu") == 0) {
    pthread_t threads[MAX_CORES];
    for (int i = 0; i < 14; i++) {
      pthread_create(&threads[i], NULL, cpu_stress, &duration);
    }
    for (int i = 0; i < 14; i++) {
      pthread_join(threads[i], NULL);
    }
  } else if (strcmp(mode, "ram") == 0) {
    ram_stress(duration);
  } else {
    printf("Mode %s not implemented in C yet.\n", mode);
  }

  printf("✅ [C] Simulation finished.\n");
  return 0;
}
