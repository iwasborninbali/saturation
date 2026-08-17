#!/bin/bash
# production: launched after phase 2 ends
cd /home/pmbot/projects/solver_kit
until [ $(grep -l 'done:' logs/r5_*.log 2>/dev/null | wc -l) -ge 12 ]; do sleep 10; done
i=0
for s in 1 2 3 4 5 6 7 8; do i=$((i+1)); TABU=20 RELOAD=20000 DRIFT=6 nohup ./fast/mc2 71 100 rot2 $((100+s)) 3600 0.4 0.1 out/p1_$i 1 > logs/p1_$i.log 2>&1 & done
i=$((i+1)); TABU=20 RELOAD=20000 DRIFT=6 nohup ./fast/mc2 71 100 h 111 3600 0.4 0.1 out/p1_$i 1 > logs/p1_$i.log 2>&1 &
i=$((i+1)); TABU=20 RELOAD=20000 DRIFT=6 nohup ./fast/mc2 71 100 hv 112 3600 0.8 0.1 out/p1_$i 1 > logs/p1_$i.log 2>&1 &
i=$((i+1)); TABU=20 nohup ./fast/mc2 71 142 rot2 113 3600 0.4 0.1 out/p1_$i 0 > logs/p1_$i.log 2>&1 &
i=$((i+1)); nohup ./fast/sa 71 142 rot2 114 3600 0.35 0.35 out/p1_$i 0 > logs/p1_$i.log 2>&1 &
echo "production launched at $(date)" >> logs/p1_launch.txt
