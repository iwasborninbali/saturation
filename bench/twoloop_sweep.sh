#!/bin/bash
# even n: sweep all subclasses (x = main-axis loop, y = anti-axis loop) of the two-loop family
# usage: twoloop_sweep.sh n secs [ALL]
n=$1; secs=${2:-120}; mode=${3:-find}
m=$((n-1)); h=$((n/2)); out=bench/twoloop_n${n}_${mode}.txt
: > $out
for x in $(seq 0 $((h-1))); do for y in $(seq 0 $((h-1))); do [ $y -eq $x ] && continue; echo "$x $y"; done; done | sort -R | \
xargs -P 8 -L 1 sh -c 'if [ "'$mode'" = "all" ]; then r=$(ALL=1 PAIRS="$0,$0;$1,$(( '$m' - $1 ))" ./there '$n' 2 $((RANDOM+1)) '$secs' | tail -1); else r=$(PAIRS="$0,$0;$1,$(( '$m' - $1 ))" ./there '$n' 2 $((RANDOM+1)) '$secs'); fi; echo "x=$0 y=$1 :: $r" >> '$out'; case "$r" in book*) echo "FOUND x=$0 y=$1 :: $r";; esac'
echo "SWEEP $n $mode DONE" >> $out
