#!/bin/bash
# calibration on the linux-12c box: per-seed time to first book, rct4 (sym 8) then dia2 (sym 6)
cd "$(dirname "$0")/../.."
for sym in 8 6; do for n in 43 47 51 55; do
  out=kit71/bench/sym${sym}_linux12_n${n}.txt
  echo "# $(date -u +%FT%TZ) ./there $n $sym seed 1500 (12 seeds in parallel, gcc -O3 -march=native, Debian 12 x86_64)" > $out
  for seed in $(seq 1 12); do echo "$n $sym $seed 1500"; done | xargs -P 12 -L 1 sh -c './there $0 $1 $2 $3 | sed "s/ : .*//"' >> $out
  echo "# done $(date -u +%FT%TZ)" >> $out
done; done
echo CAL LINUX DONE
