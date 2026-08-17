#!/bin/bash
# even two-loop family (C4 orbits + main-axis loop (x,x) + anti-axis loop (y,m-y)), exhaustive per subclass, K workers
# usage: twoloop_cal.sh n secs workers   -> kit71/bench/twoloop_n{n}_all_linux.txt
cd "$(dirname "$0")/../.."
n=$1; secs=${2:-600}; K=${3:-2}; m=$((n-1)); h=$((n/2)); out=kit71/bench/twoloop_n${n}_all_linux.txt
echo "# $(date -u +%FT%TZ) two-loop family n=$n exhaustive, $secs s cap per subclass, $K workers (linux-12c)" > $out
for x in $(seq 0 $((h-1))); do for y in $(seq 0 $((h-1))); do [ $y -eq $x ] && continue; echo "$x $y"; done; done | \
xargs -P $K -L 1 sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="$0,$0;$1,$(( '$m' - $1 ))" ./there '$n' 2 1 '$secs'); echo "$r" | grep "^sol" | sed "s/^/BOOK $0,$0;$1,$(( '$m' - $1 )) /"; echo "x=$0 y=$1 :: $(echo "$r" | tail -1)"' >> $out
echo "# done $(date -u +%FT%TZ) books=$(grep -c ^BOOK $out) exhausted=$(grep -c ' all n=' $out) timeouts=$(grep -c timeout $out)" >> $out
tail -1 $out
