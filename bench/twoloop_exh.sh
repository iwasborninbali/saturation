#!/bin/bash
# even n: EXHAUSTIVE sweep of the two-loop family up to the quarter turn ((x,y) ~ (y,x)); x<y only.
# usage: bench/twoloop_exh.sh n secs_per_subclass procs
n=$1; secs=${2:-3600}; P=${3:-6}
m=$((n-1)); h=$((n/2)); out=bench/twoloop_n${n}_exh.txt; sols=bench/twoloop_n${n}_exh_sols.txt
[ -f $out ] || echo "# exhaustive two-loop sweep n=$n, unordered {x,y}, x<y<h=$h ($((h*(h-1)/2)) sub-classes), $(date -u +%FT%TZ)" > $out
for x in $(seq 0 $((h-1))); do for y in $(seq $((x+1)) $((h-1))); do grep -q "^x=$x y=$y ::" $out || echo "$x $y"; done; done | \
xargs -P $P -L 1 sh -c 'o=$(ALL=1 PRINTALL=1 PAIRS="$0,$0;$1,$(( '$m' - $1 ))" ./there '$n' 2 $((RANDOM+1)) '$secs'); r=$(echo "$o" | tail -1); echo "$o" | grep "^sol" | sed "s/^/x=$0 y=$1 :: /" >> '$sols'; echo "x=$0 y=$1 :: $r" >> '$out'; case "$r" in *solutions=[1-9]*) echo "FOUND x=$0 y=$1 :: $r";; esac'
echo "# done $(date -u +%FT%TZ)" >> $out
