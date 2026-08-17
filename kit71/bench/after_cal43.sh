#!/bin/bash
cd "$(dirname "$0")/../.."
until [ $(grep -vc '^#' kit71/bench/sym8_linux12_n43.txt) -ge 12 ]; do sleep 10; done
sleep 5
echo "# done $(date -u +%FT%TZ)" >> kit71/bench/sym8_linux12_n43.txt
pkill -f "[c]al_linux.sh"; for p in $(pgrep -f "^\./there 47 8"); do kill $p; done
sleep 1
./kit71/bench/cycle3_sweep.sh 33 10 12 > kit71/bench/sweep33_10.log 2>&1
./kit71/bench/cycle3_sweep.sh 33 9 12 > kit71/bench/sweep33_9.log 2>&1
echo SWEEPS33 DONE
