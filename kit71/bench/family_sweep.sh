#!/bin/bash
# canonical sweep of the 3-cycle defect family: usage family_sweep.sh n jobs   (both bases: 9 = C4 orbits, 10 = both-swaps orbits)
cd "$(dirname "$0")/../.."
n=$1; jobs=${2:-12}
python3 kit71/bench/cycle_family.py $n > kit71/bench/family3_list_n$n.txt 2>/dev/null
for sym in 10 9; do
  out=kit71/bench/family3_sym${sym}_n${n}.txt
  echo "# $(date -u +%FT%TZ) canonical 3-cycle family n=$n sym=$sym subclasses=$(wc -l < kit71/bench/family3_list_n$n.txt)" > $out
  cat kit71/bench/family3_list_n$n.txt | xargs -P $jobs -I{} sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="{}" ./there_tw '"$n $sym"' 1 7200); echo "$r" | grep "^sol" | sed "s/^/BOOK {} /"; echo "$r" | tail -1 | sed "s/^/{} /"' >> $out
  echo "# done $(date -u +%FT%TZ) books=$(grep -c ^BOOK $out) exhausted=$(grep -c ' all n=' $out) dead=$(grep -c dead $out) timeouts=$(grep -c timeout $out)" >> $out
  tail -1 $out
done
