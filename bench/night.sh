#!/bin/bash
# night queue: after the 36 finding pass -> map (odd rct4 31..39, even rot4 42/44) -> exhaustive 36 two-loop family -> 38/40 finding passes
until grep -q "SWEEP 36 find DONE" bench/twoloop_n36_find.txt 2>/dev/null; do sleep 30; done
echo "[$(date +%H:%M)] 36 find pass done: $(grep -c book bench/twoloop_n36_find.txt) books"
for n in 31 33 35 37 39; do python3 -u there.py $n --sym 8 --secs 3600 --seeds 8; done
for n in 42 44; do python3 -u there.py $n --sym 2 --secs 7200 --seeds 8; done
echo "[$(date +%H:%M)] map done"
./bench/twoloop_sweep.sh 36 1800 all
echo "[$(date +%H:%M)] 36 exhaustive pass done: $(grep -c 'solutions=[1-9]' bench/twoloop_n36_all.txt) subclasses with books"
for n in 38 40; do ./bench/twoloop_sweep.sh $n 120 find; echo "[$(date +%H:%M)] $n find pass: $(grep -c book bench/twoloop_n${n}_find.txt) books"; done
echo NIGHT DONE
