#!/bin/bash
# count books in the twisted classes (sym 9: C4 orbits + pair anywhere; sym 10: both-swaps orbits + pair anywhere)
# for each odd n: raw sum over all pair positions (a,b), a,b != h, a != b, a+b != m; each book is counted twice (pair reps).
cd "$(dirname "$0")/../.."
for n in 13 15 17 19 21 23 25; do
  h=$(( (n-1)/2 )); m=$((n-1))
  for sym in 9 10; do
    out=kit71/bench/twist_sym${sym}_n${n}.txt
    : > $out
    for a in $(seq 0 $m); do for b in $(seq 0 $m); do
      [ $a -eq $h ] && continue; [ $b -eq $h ] && continue; [ $a -eq $b ] && continue; [ $((a+b)) -eq $m ] && continue
      echo "$a $b"
    done; done | nice -n 19 xargs -P 4 -L 1 sh -c 'r=$(ALL=1 PAIR=$0,$1 ./there '"$n $sym"' 1 600 | sed -n "s/.*solutions=\([0-9]*\) nodes=\([0-9]*\).*/\1 \2/p"); echo "$0 $1 $r"' >> $out
    raw=$(awk '{s+=$3} END{print s}' $out); nodes=$(awk '{s+=$4} END{print s}' $out)
    ref=$( [ $sym -eq 9 ] && ALL=1 ./there $n 8 1 600 || ALL=1 ./there $n 6 1 600 )
    echo "n=$n sym=$sym twisted: books=$((raw/2)) (raw $raw) nodes=$nodes | reference: $ref" | tee -a kit71/bench/twist_summary.txt
  done
done
echo TWIST DONE
