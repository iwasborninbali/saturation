"""subsplit_c.py — доразбиение узла по столбцу, с ЗАПИСЬЮ СТОЛБЦА В ИМЯ.

Прежняя схема `{родитель}_s{индекс}` не хранит столбец нигде, кроме комментария внутри файла
(да и его пишет только split_sat, а subsplit — нет). Поэтому два дробления одного узла по разным
столбцам дают файлы с ОДИНАКОВЫМИ именами и разным содержимым, а правило «узел закрыт, когда
закрыты все 64 потомка» примет такую смесь: имён ровно 64 и все на месте. Каждое разбиение по
отдельности исчерпывающе, смесь — нет.

Опасно при этом НЕ повторное использование столбца (это расточительно, но состоятельно: ребёнок,
противоречащий родителю, невыполним по-настоящему), а НЕОДНОРОДНОСТЬ столбца среди братьев.
Имя вида `{родитель}_c{столбец}s{индекс}` делает неоднородность видимой сразу.

    python3 subsplit_c.py base.cnf n col cap outdir
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
made = 0
for j, s in enumerate(subs):
    units = [((x*n + y)*n + z) + 1 if z in s else -(((x*n + y)*n + z) + 1) for z in range(n)]
    with open(os.path.join(outdir, f"{stem}_c{col}s{j:03d}.cnf"), "w") as f:
        f.write(f"c subsplit of {stem} on column {col} = cell ({x},{y}), subset {j} of {len(subs)}\n")
        f.write(f"p cnf {nv} {int(ncl)+len(units)}\n{body}\n")
        f.write("".join(f"{u} 0\n" for u in units))
    made += 1
on_disk = len([f for f in os.listdir(outdir) if f.startswith(stem + f"_c{col}s")])
print(f"{stem}: столбец {col} = клетка ({x},{y}); записано {made}, на диске {on_disk} "
      f"{'— сходится' if made == on_disk == len(subs) else '— ОТКАЗ: не сходится'}")
sys.exit(0 if made == on_disk == len(subs) else 2)
