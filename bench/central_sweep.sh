#!/bin/bash
# exhaustive sweep of the directed-3-cycle sub-classes that use the CENTRAL row/column class (omitted by cycle_family.py),
# both bases: sym 10 = V2 (both diagonal reflections) base, sym 9 = C4 (quarter turns) base, program there_tw.
# usage: bench/central_sweep.sh n jobs [secs]      journals: bench/central3_sym{10,9}_n<N>.txt (resumable)
cd "$(dirname "$0")/.."
n=$1; jobs=${2:-4}; secs=${3:-7200}
list=bench/central3_list_n$n.txt
[ -s $list ] || python3 bench/defects3.py $n --central-only > $list 2>/dev/null
for sym in 10 9; do
  out=bench/central3_sym${sym}_n${n}.txt
  [ -f $out ] || echo "# $(date -u +%FT%TZ) central-class 3-cycle sweep n=$n sym=$sym subclasses=$(wc -l < $list | tr -d ' ') secs=$secs" > $out
  grep -v '^#' $out | grep -v '^BOOK' | awk '{print $1}' | sort -u > /tmp/cdone_${sym}_$n.txt
  grep -vxF -f /tmp/cdone_${sym}_$n.txt $list > /tmp/ctodo_${sym}_$n.txt
  echo "# resume $(date -u +%FT%TZ): todo $(wc -l < /tmp/ctodo_${sym}_$n.txt | tr -d ' ')" >> $out
  cat /tmp/ctodo_${sym}_$n.txt | xargs -P $jobs -I{} sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="{}" ./there_tw '"$n $sym"' 1 '"$secs"'); echo "$r" | grep "^sol" | sed "s/^/BOOK {} /"; echo "$r" | tail -1 | sed "s/^/{} /"' >> $out
  echo "# done $(date -u +%FT%TZ) books=$(grep -c '^BOOK' $out) exhausted=$(grep -c ' all n=' $out) dead=$(grep -c dead $out) timeouts=$(grep -c timeout $out)" >> $out
  tail -1 $out
done
