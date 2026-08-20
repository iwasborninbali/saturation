"""add_layer_lb.py — дописать в CNF СЛЕДСТВИЕ: в каждом слое не менее одной точки.

Обоснование чисто счётное и не зависит от геометрии. Слой есть богатая плоскость, значит несёт
не более 3 точек; слоёв n; итого не более 3n. При n=7 это 21 против требуемых M=19, то есть запас
всего две точки. Пустой слой отнял бы 3 и оставил 18 < 19 — противоречие. Значит каждый слой по
каждой из трёх осей содержит хотя бы одну точку.

Утверждение ВЫВОДИМО из уже закодированного (ёмкость плоскостей плюс кардинальность), поэтому
добавление ничего не меняет по существу и не может создать ложной невыполнимости. Но решатель
выводит его не сразу: кардинальность закодирована тотализатором, и связь «слой пуст -> итог < M»
проходит через всю его глубину. Явная клауза даёт то же распространением.

    python3 add_layer_lb.py in.cnf out.cnf n M
"""
import sys

src, dst, n, M = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4])
cap = 3
if M > cap * n - cap:                      # хотя бы одна точка в слое следует из запаса
    lb = M - cap * (n - 1)
else:
    lb = 0
lines = open(src).read().splitlines()
h = [i for i, l in enumerate(lines) if l.startswith("p cnf")][0]
nv, ncl = lines[h].split()[2:4]
extra = []
if lb >= 1:
    for axis in range(3):
        for t in range(n):
            cells = [i + 1 for i in range(n**3)
                     if (i // (n*n) if axis == 0 else (i // n) % n if axis == 1 else i % n) == t]
            extra.append(cells)            # «хотя бы одна» — дизъюнкция всех клеток слоя
with open(dst, "w") as f:
    f.write(f"c {src.split('/')[-1]} + {len(extra)} clauses: each layer holds at least {lb} point(s)\n")
    f.write(f"c derived from capacity {cap} per layer and total {M}: an empty layer leaves "
            f"{cap*(n-1)} < {M}\n")
    f.write(f"p cnf {nv} {int(ncl)+len(extra)}\n")
    f.write("\n".join(lines[h+1:]) + "\n")
    for c in extra:
        f.write(" ".join(map(str, c)) + " 0\n")
print(f"нижняя граница на слой: {lb}; добавлено клауз: {len(extra)}")
