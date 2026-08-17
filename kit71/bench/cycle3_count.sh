#!/bin/bash
# odd-cycle defects: C4 orbits (sym 9) or both-swaps orbits (sym 10) + a 3-cycle of half-turn pairs (x,y),(y,z),(z,x') with x' in {x, m-x}
# raw counts over all ordered (x<h, y, z) and both closings; each book is counted several times (rotations/signs) — this measures existence/density.
cd "$(dirname "$0")/../.."
for n in "$@"; do
  h=$(( (n-1)/2 )); m=$((n-1))
  for sym in 9 10; do
    out=kit71/bench/cycle3_sym${sym}_n${n}.txt; : > $out
    for x in $(seq 0 $((h-1))); do for y in $(seq 0 $m); do
      [ $y -eq $h ] && continue; [ $y -eq $x ] && continue; [ $y -eq $((m-x)) ] && continue
      for z in $(seq 0 $m); do
        [ $z -eq $h ] && continue; [ $z -eq $x ] && continue; [ $z -eq $((m-x)) ] && continue; [ $z -eq $y ] && continue; [ $z -eq $((m-y)) ] && continue
        echo "$x $y $z $x"; echo "$x $y $z $((m-x))"
      done
    done; done | nice -n 19 xargs -P 4 -L 1 sh -c 'r=$(ALL=1 PAIRS="$0,$1;$1,$2;$2,$3" ./there_tw '"$n $sym"' 1 600 | sed -n "s/.*solutions=\([0-9]*\) nodes=\([0-9]*\).*/\1 \2/p"); echo "$0 $1 $2 $3 $r"' >> $out
    raw=$(awk '{s+=$5} END{print s+0}' $out); nodes=$(awk '{s+=$6} END{print s+0}' $out); cnt=$(wc -l < $out); nz=$(awk '$5>0' $out | wc -l)
    echo "n=$n sym=$sym 3-cycle defects: subclasses=$cnt with_books=$nz raw_books=$raw nodes=$nodes" | tee -a kit71/bench/cycle3_summary.txt
  done
done
echo CYCLE3 DONE
