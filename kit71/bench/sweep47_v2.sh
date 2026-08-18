#!/bin/bash
cd "$(dirname "$0")/../.."
n=47; sym=10; list=kit71/bench/family3_list_n47_A_plus_central.txt; out=kit71/bench/f47A_sym10_n47.txt
[ -f $out ] || echo "# $(date -u +%FT%TZ) 47 half A (+central) V2 base, there_tw, 12 workers, 7200 s cap" > $out
grep -v '^#' $out | awk '{print $1}' | sort -u > /tmp/done47.txt
grep -vxF -f /tmp/done47.txt $list > /tmp/todo47.txt
echo "# resume $(date -u +%FT%TZ): todo $(wc -l < /tmp/todo47.txt)" >> $out
cat /tmp/todo47.txt | xargs -P 12 -I{} sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="{}" ./there_tw 47 10 1 7200); echo "$r" | grep "^sol" | sed "s/^/BOOK {} /"; echo "$r" | tail -1 | sed "s/^/{} /"' >> $out
echo "# done $(date -u +%FT%TZ) books=$(grep -c ^BOOK $out) exhausted=$(grep -c ' all n=' $out) dead=$(grep -c dead $out) timeouts=$(grep -c timeout $out)" >> $out
