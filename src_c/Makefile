CC = clang
CFLAGS = -O3 -march=native -Wall
LIBS = -framework CoreFoundation -lpthread

all: monitor simulator engine

monitor: hyper_monitor.c common.h
	$(CC) $(CFLAGS) hyper_monitor.c -o monitor $(LIBS)

simulator: hyper_simulator.c common.h
	$(CC) $(CFLAGS) hyper_simulator.c -o simulator $(LIBS)

engine: hyper_engine.c common.h
	$(CC) $(CFLAGS) hyper_engine.c -o engine $(LIBS)

clean:
	rm -f monitor simulator engine *.csv
