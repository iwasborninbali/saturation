#!/bin/bash
# even n: C4 orbits + main-axis loop (x,x) + anti-axis loop (y,m-y); random subclasses, first book wins
n=$1; secs=${2:-90}; tries=${3:-64}
m=$((n-1)); h=$((n/2))
for t in $(seq 1 $tries); do
  x=$((RANDOM % h)); y=$((RANDOM % h)); [ $y -eq $x ] && continue
  echo "$x $y"
done | xargs -P 8 -L 1 sh -c 'out=$(PAIRS="$0,$0;$1,$(( '$m' - $1 ))" ./there '$n' 2 $((RANDOM)) '$secs'); echo "x=$0 y=$1 :: ${out}"' 2>&1
