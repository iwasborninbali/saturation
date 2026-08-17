#!/bin/bash
# after the 37 sweep: 39 (my half A of the canonical list, C4 base and V2 base), then 41 half A, then a rot2 hunt at 37 (10 seeds).
cd "$(dirname "$0")/../.."
until [ -f kit71/bench/family3_sym9_n37.txt ] && grep -q '^# done' kit71/bench/family3_sym9_n37.txt; do sleep 30; done
sleep 5
./kit71/bench/family_sweep.sh 39 12 kit71/bench/family3_list_n39_A.txt family3A > kit71/bench/family_sweep39.log 2>&1
./kit71/bench/family_sweep.sh 41 12 kit71/bench/family3_list_n41_A.txt family3A > kit71/bench/family_sweep41.log 2>&1
setsid nohup ./kit71/hunt.sh 37 1 10 40000 > kit71/bench/hunt37.log 2>&1 < /dev/null &
echo "chain done $(date -u +%FT%TZ)" >> kit71/bench/schedule_after37.log
