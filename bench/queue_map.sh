#!/bin/bash
# after the rot2 calibration: complete the certified map (odd 31..39 via rct4, even 42/44 via rot4)
until [ -f bench/rot2_cal.done ]; do sleep 20; done
for n in 31 33 35 37 39; do python3 -u there.py $n --sym 8 --secs 3600 --seeds 8; done
for n in 42 44; do python3 -u there.py $n --sym 2 --secs 7200 --seeds 8; done
echo MAP DONE
