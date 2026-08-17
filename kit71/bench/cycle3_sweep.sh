#!/bin/bash
# exhaustive sweep of the 3-cycle-defect family at resolution n: usage cycle3_sweep.sh n sym jobs
# every sub-class is exhausted (ALL=1); solutions are printed (PRINTALL) and collected.
cd "$(dirname "$0")/../.."
n=$1; sym=$2; jobs=${3:-12}
h=$(( (n-1)/2 )); m=$((n-1))
out=kit71/bench/sweep3_sym${sym}_n${n}.txt; : > $out
echo "# $(date -u +%FT%TZ) sweep n=$n sym=$sym (C4 base=9 / both-swaps base=10) + 3-cycle of half-turn pairs" > $out
for x in $(seq 0 $((h-1))); do for y in $(seq 0 $m); do
  [ $y -eq $h ] && continue; [ $y -eq $x ] && continue; [ $y -eq $((m-x)) ] && continue
  for z in $(seq 0 $m); do
    [ $z -eq $h ] && continue; [ $z -eq $x ] && continue; [ $z -eq $((m-x)) ] && continue; [ $z -eq $y ] && continue; [ $z -eq $((m-y)) ] && continue
    echo "$x $y $z $x"; echo "$x $y $z $((m-x))"
  done
done; done | xargs -P $jobs -L 1 sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="$0,$1;$1,$2;$2,$3" ./there_tw '"$n $sym"' 1 3600); echo "$r" | grep "^sol" | sed "s/^/BOOK $0,$1,$2,$3 /"; echo "$r" | tail -1 | sed "s/^/$0 $1 $2 $3 /"' >> $out
echo "# done $(date -u +%FT%TZ) books=$(grep -c ^BOOK $out) subclasses=$(grep -vc '^#\|^BOOK' $out)" >> $out
tail -1 $out
