#!/bin/bash
# after 41A (C4 base) completes: 45A (V2 then C4), then 47A, then the 39A remainder.
cd "$(dirname "$0")/../.."
until [ -f kit71/bench/family3A_sym9_n41.txt ] && grep -q '^# done' kit71/bench/family3A_sym9_n41.txt; do sleep 60; done
sleep 5
./kit71/bench/family_sweep.sh 45 12 kit71/bench/family3_list_n45_A.txt family3A > kit71/bench/family_sweep45.log 2>&1
./kit71/bench/family_sweep.sh 47 12 kit71/bench/family3_list_n47_A.txt family3A > kit71/bench/family_sweep47.log 2>&1
./kit71/bench/family_sweep.sh 39 12 kit71/bench/family3_list_n39_A.txt family3A > kit71/bench/family_sweep39b.log 2>&1
echo "chain done $(date -u +%FT%TZ)" >> kit71/bench/schedule_after41.log
