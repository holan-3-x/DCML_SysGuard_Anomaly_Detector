#include "common.h"
#include <fcntl.h>

void *cpu_stress(void *arg) {
  printf("🔥 [C] Saturating CPU Core...\n");
  int duration = *(int *)arg;
  time_t start = time(NULL);
  while (time(NULL) - start < duration) {
    for (volatile int i = 0; i < 1000000; i++)
      ;
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
    memset(ptr, 0xFF, size);
    usleep(100000);
  }
  free(ptr);
}

void disk_stress(int duration_s) {
  printf("💿 [C] Generating high IO throughput...\n");
  char *buf = malloc(1024 * 1024 * 50); // 50MB buffer
  memset(buf, 0xAA, 1024 * 1024 * 50);
  time_t start = time(NULL);
  int fd = open("stress_tmp.bin", O_WRONLY | O_CREAT | O_TRUNC, 0644);
  while (time(NULL) - start < duration_s) {
    write(fd, buf, 1024 * 1024 * 50);
    lseek(fd, 0, SEEK_SET);
  }
  close(fd);
  remove("stress_tmp.bin");
  free(buf);
}

int main(int argc, char **argv) {
  if (argc < 2) {
    printf("Usage: %s <cpu|ram|disk> [duration]\n", argv[0]);
    return 1;
  }
  int duration = (argc > 2) ? atoi(argv[2]) : 10;
  char *mode = argv[1];
  if (strcmp(mode, "cpu") == 0) {
    pthread_t threads[14];
    for (int i = 0; i < 14; i++)
      pthread_create(&threads[i], NULL, cpu_stress, &duration);
    for (int i = 0; i < 14; i++)
      pthread_join(threads[i], NULL);
  } else if (strcmp(mode, "ram") == 0) {
    ram_stress(duration);
  } else if (strcmp(mode, "disk") == 0) {
    disk_stress(duration);
  } else {
    printf("Mode %s not implemented.\n", mode);
  }
  printf("✅ [C] Simulation finished.\n");
  return 0;
}
