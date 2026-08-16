#!/bin/bash
until grep -q "SWEEP DONE" sweep_b.log; do sleep 10; done
for n in 41 45 49 53; do python3 -u there.py $n --secs 1500 --seeds 8; done
echo RCT4 CAL DONE
