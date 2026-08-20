#!/bin/bash
# work_unit.sh <имя_узла> — один независимый кусок: восстановить из имени, пройти рекурсией, удалить.
# Промежуточные файлы живут только внутри своего каталога, названного по имени куска, поэтому два
# рабочих никогда не делят путь — та самая беда, что стоила нам 280 отозванных фактов.
SP=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad
R=/home/pmbot/projects/saturation_peer
nm="$1"; lim="${2:-120}"; maxd="${3:-49}"
W=$SP/wu/$nm; rm -rf $W; mkdir -p $W
f=$W/$nm.cnf
$R/slack/targets/rebuild_from_name.sh "$nm" $SP/root_aug.cnf "$f" >/dev/null 2>&1
if [ ! -s "$f" ]; then echo "ОТКАЗ $nm: восстановление не дало файла"; rm -rf $W; exit 2; fi
hdr=$(awk '/^p cnf/{print $4; exit}' "$f"); body=$(awk '!/^c |^p cnf/ && NF>0' "$f" | wc -l)
if [ "$hdr" != "$body" ]; then echo "ОТКАЗ $nm: повреждён ($hdr против $body)"; rm -rf $W; exit 3; fi
ci=$(echo "$nm" | awk -F'_s' '{print NF-1}')
$R/slack/targets/solve_or_split.sh "$f" "$ci" "$lim" "$maxd"
rc=$?
rm -rf $W
exit $rc
