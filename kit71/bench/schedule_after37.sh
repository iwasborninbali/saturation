#!/bin/bash
# after the 37 sym9 sweep completes: stop the 3-cycle chain; launch the generic rot2 hunt at 37 (10 seeds);
# with 2 workers: two-loop family calibration at 30/32/34 (for the peer's 36 push), then the 39 3-cycle sweep (resumable).
cd "$(dirname "$0")/../.."
until [ -f kit71/bench/family3_sym9_n37.txt ] && grep -q '^# done' kit71/bench/family3_sym9_n37.txt; do sleep 30; done
pkill -f "[f]amily_sweep.sh 39"; pkill -f "[f]amily_sweeps"; for p in $(pgrep -f "^\./there_tw 39"); do kill $p; done; sleep 2
setsid nohup ./kit71/hunt.sh 37 1 10 40000 > kit71/bench/hunt37.log 2>&1 < /dev/null &
sleep 5
setsid nohup sh -c './kit71/bench/twoloop_cal.sh 30 600 2; ./kit71/bench/twoloop_cal.sh 32 900 2; ./kit71/bench/twoloop_cal.sh 34 1200 2; ./kit71/bench/family_sweep.sh 39 2' > kit71/bench/side_chain.log 2>&1 < /dev/null &
echo "scheduled at $(date -u +%FT%TZ)" >> kit71/bench/schedule_after37.log
