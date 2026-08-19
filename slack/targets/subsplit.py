"""subsplit.py — доразбиение ОДНОГО тяжёлого куска по следующему столбцу.

Нужно потому, что при разбиении по двум столбцам куски с почти пустыми первыми столбцами
несоизмеримо тяжелее прочих (то же самое мы видели в переборе). Полнота сохраняется тем же
аргументом: подмножества размера <= cap исчерпывают столбец.

usage: python3 subsplit.py base_case.cnf n col cap outdir
"""
import os, sys
from itertools import combinations
base, n, col, cap, outdir = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
os.makedirs(outdir, exist_ok=True)
lines = open(base).read().splitlines()
h = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
nv, ncl = lines[h].split()[2:4]
body = "\n".join(lines[h+1:])
x, y = col // n, col % n
stem = os.path.basename(base)[:-4]
subs = [s for k in range(cap+1) for s in combinations(range(n), k)]
for j, s in enumerate(subs):
    units = [((x*n + y)*n + z) + 1 if z in s else -(((x*n + y)*n + z) + 1) for z in range(n)]
    with open(os.path.join(outdir, f"{stem}_s{j:03d}.cnf"), "w") as f:
        f.write(f"c subsplit of {stem} on column {col}, subset {j}\n")
        f.write(f"p cnf {nv} {int(ncl)+len(units)}\n{body}\n")
        f.write("".join(f"{u} 0\n" for u in units))
# ПРОВЕРКА, ЧТО НАПИСАНО РОВНО СТОЛЬКО, СКОЛЬКО ПРОСИЛИ.
# Существует потому, что при переполнении диска записалось меньше файлов, и программа
# промолчала: разбиение стало неполным, а сказать об этом было некому.
written = len([f for f in os.listdir(outdir) if f.startswith(stem + "_s") and f.endswith(".cnf")])
if written != len(subs):
    raise SystemExit(f"ОТКАЗ: {stem}: просили {len(subs)} подкусков, записалось {written} "
                     f"(проверь место на диске). Разбиение НЕПОЛНО, пользоваться им нельзя.")
print(f"{stem}: {len(subs)} подкусков, проверено на диске: {written}")
