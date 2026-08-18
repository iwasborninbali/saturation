#!/bin/bash
# exhaustive sweep of the mixed families (bench/mixed3.py): --c4v2 with there_tw sym 9, --v2c4 with sym 10
# usage: bench/mixed_sweep.sh n jobs [secs]     journals: bench/mixed_c4v2_n<N>.txt, bench/mixed_v2c4_n<N>.txt
cd "$(dirname "$0")/.."
n=$1; jobs=${2:-2}; secs=${3:-3600}
for mode in c4v2 v2c4; do
  [ $mode = c4v2 ] && sym=9 || sym=10
  list=bench/mixed_${mode}_list_n$n.txt; [ -s $list ] || python3 bench/mixed3.py $n --$mode > $list 2>/dev/null
  out=bench/mixed_${mode}_n${n}.txt
  [ -f $out ] || echo "# $(date -u +%FT%TZ) mixed family $mode n=$n sym=$sym subclasses=$(wc -l < $list | tr -d ' ') secs=$secs" > $out
  grep -v '^#' $out | grep -v '^BOOK' | awk '{print $1}' | sort -u > /tmp/mdone_${mode}_$n.txt
  grep -vxF -f /tmp/mdone_${mode}_$n.txt $list > /tmp/mtodo_${mode}_$n.txt
  cat /tmp/mtodo_${mode}_$n.txt | xargs -P $jobs -I{} sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="{}" ./there_tw2 '"$n $sym"' 1 '"$secs"'); echo "$r" | grep "^sol" | sed "s/^/BOOK {} /"; echo "$r" | tail -1 | sed "s/^/{} /"' >> $out
  echo "# done $(date -u +%FT%TZ) books=$(grep -c '^BOOK' $out) exhausted=$(grep -c ' all n=' $out) dead=$(grep -c dead $out) timeouts=$(grep -c timeout $out) skipped=$(grep -c skip $out)" >> $out
  tail -1 $out
done
