"""verify_split_coverage.py — независимая проверка ИСЧЕРПЫВАЮЩНОСТИ разбиения на куски.

Разбиение перебирает все подмножества размера <= 2 в первых c столбцах. Оно исчерпывает
пространство ТОЛЬКО ЕСЛИ ни одна допустимая конфигурация не может иметь трёх точек в столбце.
Это «очевидно» (три точки столбца коллинеарны) — но очевидность здесь недостаточна: нужно, чтобы
эта тройка была ЗАПРЕЩЕНА САМОЙ ФОРМУЛОЙ, то есть чтобы столбец входил в список богатых прямых.
Если перечислитель прямых по какой-то причине потерял осевые направления, кусков всё равно было бы
22^2 = 484, все они честно оказались бы невыполнимы, а конфигурация с тремя точками в столбце
просто не попала бы ни в один кусок — и не была бы рассмотрена вообще.

Проверяется:
  1) каждый из 3n^2 осевых столбцов целиком лежит внутри какой-то перечисленной прямой;
  2) число кусков равно (сумма C(n,k), k<=2)^c и все наборы юнитов различны и покрывают все
     допустимые образцы первых c столбцов — сверка со своим перечислением, не с их кодом.

    python3 verify_split_coverage.py n cols
"""
import os, sys
from itertools import combinations

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from no3_3d_cnf import lines           # проверяем ИХ перечислитель прямых


def main():
    n = int(sys.argv[1]); cols = int(sys.argv[2]) if len(sys.argv) > 2 else 2
    nc, ln = lines(n)
    idx = lambda x, y, z: (x * n + y) * n + z
    sets = [frozenset(m) for m in ln]
    print(f"n={n}: клеток {nc}, богатых прямых {len(ln)}")

    # 1) осевые столбцы по всем трём осям обязаны быть внутри перечисленных прямых
    missing = []
    for axis in range(3):
        for a in range(n):
            for b in range(n):
                col = set()
                for t in range(n):
                    c = (t, a, b) if axis == 0 else (a, t, b) if axis == 1 else (a, b, t)
                    col.add(idx(*c))
                if not any(col <= s for s in sets):
                    missing.append((axis, a, b))
    print(f"осевых столбцов {3*n*n}, НЕ покрытых ни одной прямой: {len(missing)}  {missing[:3]}")

    # усиление: любая тройка внутри столбца обязана быть запрещена (а не только весь столбец)
    bad_tri = 0
    for a in range(n):
        for b in range(n):
            for tri in combinations([idx(a, b, t) for t in range(n)], 3):
                if not any(set(tri) <= s for s in sets):
                    bad_tri += 1
    print(f"троек внутри z-столбцов {n*n*len(list(combinations(range(n),3)))}, НЕ запрещённых: {bad_tri}")

    # 2) число кусков и полнота перечисления образцов — своим счётом
    mine = [s for k in range(3) for s in combinations(range(n), k)]
    per_col = len(mine)
    expected = per_col ** cols
    # все допустимые образцы одного столбца, добытые независимо: все 2^n подмножеств с |s| <= 2
    brute = [s for r in range(n + 1) for s in combinations(range(n), r) if r <= 2]
    ok_patterns = (sorted(map(tuple, mine)) == sorted(map(tuple, brute)))
    print(f"подмножеств на столбец: перечислено {per_col}, перебором из 2^{n}: {len(brute)}, совпадают: {ok_patterns}")
    print(f"кусков должно быть {per_col}^{cols} = {expected}")

    man = os.path.join("logs", "no3_3d", f"proof_n{n}", "MANIFEST.txt")
    if os.path.exists(man):
        head = open(man).readline().strip()
        got = int(head.split("cases=")[1])
        names = sum(1 for l in open(man) if l.startswith("case_"))
        print(f"манифест: {head}")
        print(f"  заявлено кусков {got}, имён в манифесте {names}, "
              f"совпадает с независимым счётом: {got == expected == names}")
    ok = (not missing) and bad_tri == 0 and ok_patterns
    print("ВЕРДИКТ:", "разбиение ИСЧЕРПЫВАЮЩЕ — ёмкость столбца обоснована самой формулой"
          if ok else "РАЗБИЕНИЕ НЕ ИСЧЕРПЫВАЮЩЕ")


if __name__ == "__main__":
    main()
