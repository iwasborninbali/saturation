CC ?= cc
CFLAGS ?= -O3
# portable by default; for a machine-tuned build: make CFLAGS="-O3 -march=native"
all: there there128 there_tw there_tw2
there: there.c
	$(CC) $(CFLAGS) -o there there.c
there128: there.c
	$(CC) $(CFLAGS) -DBIG -o there128 there.c
there_tw: kit71/there_twisted_experiment.c
	$(CC) $(CFLAGS) -o there_tw kit71/there_twisted_experiment.c -lm
there_tw2: bench/there_tw_even.c
	$(CC) $(CFLAGS) -o there_tw2 bench/there_tw_even.c -lm
check: there there128 there_tw there_tw2
	python3 saturation.py
	ALL=1 ./there 10 0 1 60 | tail -1        # must say solutions=1135 (A000769: 156 classes)
	ALL=1 ./there128 24 2 1 60 | tail -1     # must say solutions=46
	ALL=1 ./there 21 8 1 60 | tail -1        # must say solutions=2
	ALL=1 PAIRS="1,3;3,31;31,1" ./there 37 2 1 600 | tail -1   # must say solutions=1 (first n=37 configuration)
	ALL=1 PAIRS="0,4;4,6;6,0" ./there_tw 13 10 1 60 | tail -1  # must say solutions=1 (n=13, V2 base, central class)
	python3 slack/gadget11_check.py 7 3 | tail -1
	python3 -c "import there; print(there.unleaked_here())"
clean:
	rm -f there there128 there_tw there_tw2
