#!/bin/bash
# exhaustive sweep of the whole directed-3-cycle family (bench/defects3.py: ALL defects mod D4, central class included),
# both bases (sym 10 = dia2 base, sym 9 = C4 base), program there_tw2 (= there_twisted_experiment.c, even n allowed).
# usage: bench/family_sweep2.sh n jobs [secs] [tag]   journals: bench/<tag>_sym{10,9}_n<N>.txt (resumable), tag default family3full
cd "$(dirname "$0")/.."
n=$1; jobs=${2:-4}; secs=${3:-7200}; tag=${4:-family3full}
list=bench/${tag}_list_n$n.txt
[ -s $list ] || python3 bench/defects3.py $n > $list 2>/dev/null
for sym in 10 9; do
  out=bench/${tag}_sym${sym}_n${n}.txt
  [ -f $out ] || echo "# $(date -u +%FT%TZ) $tag n=$n sym=$sym subclasses=$(wc -l < $list | tr -d ' ') secs=$secs program=there_tw2 $(git rev-parse --short HEAD 2>/dev/null)" > $out
  grep -v '^#' $out | grep -v '^BOOK' | awk '{print $1}' | sort -u > /tmp/fdone_${tag}_${sym}_$n.txt
  grep -vxF -f /tmp/fdone_${tag}_${sym}_$n.txt $list > /tmp/ftodo_${tag}_${sym}_$n.txt
  echo "# resume $(date -u +%FT%TZ): todo $(wc -l < /tmp/ftodo_${tag}_${sym}_$n.txt | tr -d ' ')" >> $out
  cat /tmp/ftodo_${tag}_${sym}_$n.txt | xargs -P $jobs -I{} sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="{}" ./there_tw2 '"$n $sym"' 1 '"$secs"'); echo "$r" | grep "^sol" | sed "s/^/BOOK {} /"; echo "$r" | tail -1 | sed "s/^/{} /"' >> $out
  echo "# done $(date -u +%FT%TZ) books=$(grep -c '^BOOK' $out) exhausted=$(grep -c ' all n=' $out) dead=$(grep -c dead $out) timeouts=$(grep -c timeout $out)" >> $out
  tail -1 $out
done
