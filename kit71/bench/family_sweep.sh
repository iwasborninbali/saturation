#!/bin/bash
# canonical sweep of a defect family: usage family_sweep.sh n jobs [listfile] [tag]
#   default list = 3-cycle family (cycle_family.py n); tag names the output; resumes (skips PAIRS already recorded)
cd "$(dirname "$0")/../.."
n=$1; jobs=${2:-12}; list=${3:-}; tag=${4:-family3}
if [ -z "$list" ]; then list=kit71/bench/family3_list_n$n.txt; [ -s $list ] || python3 kit71/bench/cycle_family.py $n > $list 2>/dev/null; fi
for sym in 10 9; do
  out=kit71/bench/${tag}_sym${sym}_n${n}.txt
  [ -f $out ] || echo "# $(date -u +%FT%TZ) canonical sweep $tag n=$n sym=$sym subclasses=$(wc -l < $list)" > $out
  grep -v '^#' $out | awk '{print $1}' | sort -u > /tmp/done_${tag}_${sym}_$n.txt
  grep -vxF -f /tmp/done_${tag}_${sym}_$n.txt $list > /tmp/todo_${tag}_${sym}_$n.txt
  echo "# resume $(date -u +%FT%TZ): todo $(wc -l < /tmp/todo_${tag}_${sym}_$n.txt)" >> $out
  cat /tmp/todo_${tag}_${sym}_$n.txt | xargs -P $jobs -I{} sh -c 'r=$(PRINTALL=1 ALL=1 PAIRS="{}" ./there_tw '"$n $sym"' 1 7200); echo "$r" | grep "^sol" | sed "s/^/BOOK {} /"; echo "$r" | tail -1 | sed "s/^/{} /"' >> $out
  echo "# done $(date -u +%FT%TZ) books=$(grep -c ^BOOK $out) exhausted=$(grep -c ' all n=' $out) dead=$(grep -c dead $out) timeouts=$(grep -c timeout $out)" >> $out
  tail -1 $out
done
