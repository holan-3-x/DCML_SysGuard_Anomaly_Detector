CC = clang
CFLAGS = -O3 -march=native -Wall
LIBS = -framework CoreFoundation -lpthread -lm

OBJ = telemetry.o

all: monitor simulator engine

%.o: %.c common.h
	$(CC) $(CFLAGS) -c $< -o $@

monitor: hyper_monitor.c $(OBJ) common.h
	$(CC) $(CFLAGS) hyper_monitor.c $(OBJ) -o monitor $(LIBS)

simulator: hyper_simulator.c common.h
	$(CC) $(CFLAGS) hyper_simulator.c -o simulator $(LIBS)

engine: hyper_engine.c $(OBJ) common.h
	$(CC) $(CFLAGS) hyper_engine.c $(OBJ) -o engine $(LIBS)

clean:
	rm -f monitor simulator engine *.o *.csv *.bin
