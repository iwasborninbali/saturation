CC ?= cc
CFLAGS ?= -O3 -march=native
all: there there128
there: there.c
	$(CC) $(CFLAGS) -o there there.c
there128: there.c
	$(CC) $(CFLAGS) -DBIG -o there128 there.c
check: there there128
	python3 saturation.py
	ALL=1 ./there 10 0 1 60 | tail -1        # must say solutions=1135 (A000769: 156 classes)
	ALL=1 ./there128 24 2 1 60 | tail -1     # must say solutions=46
	ALL=1 ./there 21 8 1 60 | tail -1        # must say solutions=2
	python3 -c "import there; print(there.unleaked_here())"
clean:
	rm -f there there128
