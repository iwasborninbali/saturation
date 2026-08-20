#!/bin/bash
# rebuild_from_name.sh <имя_узла> <база.cnf> <выход.cnf>
# Восстанавливает кусок ИЗ ИМЕНИ: k-е звено имени фиксирует столбец k подмножеством с этим индексом.
# Промежуточные файлы не нужны вовсе — кусок есть база плюс единичные дизъюнкты.
# ПРОВЕРЯТЬ ОБЯЗАТЕЛЬНО побайтово против существующего файла: если восстановление разойдётся,
# факты пойдут под чужими именами — ровно та ошибка, что стоила 280 отзывов.
set -u
name="$1"; base="$2"; out="$3"; n=7
python3 - "$name" "$base" "$out" "$n" <<'PY'
import sys
from itertools import combinations
name, base, out, n = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
subs = [s for k in range(4) for s in combinations(range(n), k)]
parts = name.split("_s")
idx = [int(parts[0].split("_")[-1])] + [int(p) for p in parts[1:]]
lines = open(base).read().splitlines()
h = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
nv, ncl = lines[h].split()[2:4]
units = []
for col, j in enumerate(idx):
    x, y = col // n, col % n
    for z in range(n):
        v = ((x * n + y) * n + z) + 1
        units.append(v if z in subs[j] else -v)
with open(out, "w") as f:
    f.write(f"c rebuilt from name {name}: columns 0..{len(idx)-1} fixed\n")
    f.write(f"p cnf {nv} {int(ncl)+len(units)}\n")
    f.write("\n".join(lines[h+1:]) + "\n")
    f.write("".join(f"{u} 0\n" for u in units))
print(f"{name}: столбцов {len(idx)}, единичных клауз {len(units)}")
PY
