"""decode_columns.py — какие СТОЛБЦЫ зафиксированы в куске, по СОДЕРЖИМОМУ, а не по имени.

Существует потому, что 2026-08-20 первый солвер нашёл: схема имён `{родитель}_s{индекс}` НЕ
записывает столбец, по которому дробили. Отсюда два разных вида беды, и они не равны:

  (а) один и тот же столбец зафиксирован ДВАЖДЫ под одним узлом — расточительно, но БЕЗОПАСНО:
      ребёнок с другим подмножеством противоречит родительским единичным клаузам и невыполним
      по-настоящему, а ребёнок с тем же подмножеством эквивалентен родителю; объединение
      по-прежнему покрывает родителя;
  (б) под ОДНИМ узлом смешаны дети от РАЗНЫХ столбцов — НЕСОСТОЯТЕЛЬНО: каждое разбиение
      исчерпывающе по отдельности, смесь — нет, а правило «все 64 потомка» её примет, потому
      что имён ровно нужное число и они на месте.

Опасна (б), а не (а). Имя тут не поможет — помогает только содержимое.

usage: decode_columns.py <n> <файл.cnf> [файл.cnf ...]
"""
import sys
from collections import defaultdict

def fixed_columns(path: str, n: int):
    """Возвращает {линейный индекс столбца: подмножество} и число ПОВТОРНЫХ фиксаций."""
    raw = open(path, "rb").read()
    lines = raw[-64000:].decode("utf8", "replace").splitlines()
    units = []
    for l in reversed(lines):
        p = l.split()
        if len(p) == 2 and p[1] == "0" and p[0].lstrip("-").isdigit():
            units.append(int(p[0]))
        elif units:
            break
    cells = defaultdict(list)
    for u in units:
        v = abs(u) - 1
        z, y, x = v % n, (v // n) % n, v // (n * n)
        cells[(x, y)].append((z, u > 0))
    cols, repeats = {}, 0
    for (x, y), zs in cells.items():
        if len(zs) % n:
            continue                       # неполная фиксация — не столбец
        if len(zs) > n:
            repeats += len(zs) // n - 1
        seen = {}
        for z, pos in zs:
            seen[z] = seen.get(z, False) or pos
        cols[x * n + y] = tuple(sorted(z for z, pos in seen.items() if pos))
    return cols, repeats

if __name__ == "__main__":
    n = int(sys.argv[1])
    for path in sys.argv[2:]:
        cols, rep = fixed_columns(path, n)
        name = path.split("/")[-1]
        print(f"{name}: зафиксировано столбцов {len(cols)} -> {sorted(cols)}"
              + (f"  ПОВТОРНЫХ фиксаций {rep} (расточительно, но безопасно)" if rep else ""))
        for c in sorted(cols):
            print(f"     столбец {c} = клетка ({c//n},{c%n}): подмножество {cols[c]}")
