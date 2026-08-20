#!/bin/bash
# work_parent_first.sh <имя_родителя> [лимит] [глубина]
# Восстанавливает РОДИТЕЛЯ один раз, дробит на 64 и обходит тех детей, которых нет в фактах.
#
# Зачем не по одному куску: в очереди 54 275 кусков на 1154 родителей, то есть в среднем 47 на
# родителя. Восстановление весит 0.9 с и 54 МБ; по одному это 13.6 часа только на восстановление,
# по родителям — около двух. Мера та же, работа та же, разница в том, что не переделывается.
SP=/tmp/claude-1000/-home-pmbot-projects-solver-kit/df30d6f4-57eb-4267-abb8-3e2d3cd04a69/scratchpad
R=/home/pmbot/projects/saturation_peer
par="$1"; lim="${2:-120}"; maxd="${3:-49}"
FACTS=${FACTS:-$R/logs/a280537/facts_first_solver.txt}
BASEW=/dev/shm/wp_first; mkdir -p $BASEW 2>/dev/null || BASEW=$SP/wp
W=$BASEW/$par; rm -rf $W; mkdir -p $W 2>/dev/null || { BASEW=$SP/wp; W=$BASEW/$par; rm -rf $W; mkdir -p $W; }
f=$W/$par.cnf
$R/slack/targets/rebuild_from_name.sh "$par" $SP/root_aug.cnf "$f" >/dev/null 2>&1
if [ ! -s "$f" ]; then echo "ОТКАЗ $par: восстановление не дало файла"; rm -rf $W; exit 2; fi
hdr=$(awk '/^p cnf/{print $4; exit}' "$f"); body=$(awk '!/^c |^p cnf/ && NF>0' "$f" | wc -l)
if [ "$hdr" != "$body" ]; then echo "ОТКАЗ $par: повреждён ($hdr против $body)"; rm -rf $W; exit 3; fi
ci=$(echo "$par" | awk -F'_s' '{print NF-1}')
col=$ci
# ДЕТИ ПОРОЖДАЮТСЯ ПО ОДНОМУ. Сразу все 64 — это 3.5 ГБ на рабочего; при восьми рабочих 28 ГБ
# из 32 в /dev/shm, то есть на грани. По одному пик равен 54 МБ на рабочего, а суммарная работа та
# же: ребёнок есть родитель плюс семь единичных дизъюнктов, и дописать их дешевле, чем перечитать.
d=$W/kids; mkdir -p $d
for j in $(seq 63 -1 0); do
  b=$(printf "%s_s%03d" "$par" "$j")
  if grep -qxF "$b" "$FACTS" 2>/dev/null; then continue; fi
  g=$d/$b.cnf
  python3 - "$f" "$g" "$col" "$j" 7 <<'PY'
import sys
from itertools import combinations
src, dst, col, j, n = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
subs = [s for k in range(4) for s in combinations(range(n), k)]
lines = open(src).read().splitlines()
h = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
nv, ncl = lines[h].split()[2:4]
x, y = col // n, col % n
units = [(((x*n+y)*n+z)+1 if z in subs[j] else -(((x*n+y)*n+z)+1)) for z in range(n)]
with open(dst, "w") as f:
    f.write(f"c child of {src.split('/')[-1][:-4]} on column {col}, subset {j}\n")
    f.write(f"p cnf {nv} {int(ncl)+len(units)}\n")
    f.write("\n".join(lines[h+1:]) + "\n")
    f.write("".join(f"{u} 0\n" for u in units))
PY
  [ -s "$g" ] || { echo "ОТКАЗ $b: ребёнок не порождён"; continue; }
  $R/slack/targets/solve_or_split.sh "$g" $((ci+1)) "$lim" "$maxd"
  rm -f "$g"
done
rm -f "$f"
rm -rf $W
