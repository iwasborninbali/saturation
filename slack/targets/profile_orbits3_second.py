"""profile_orbits3.py — представители орбит ТРОЕК профилей под группой куба.

Приём первого солвера. Фиксировать все три профиля слоёв (по осям x, y, z), а не один или два:
кусок становится несравнимо жёстче, потому что кардинальность распадается на 3n маленьких равенств
вместо одного большого. Кусков при этом больше, но орбитальное сокращение съедает рост.

Группа действует на тройке профилей: перестановка осей переставляет профили (6 способов),
отражение вдоль оси обращает СВОЙ профиль (2^3 способов) — всего 48 образов.

ЗАКОННОСТЬ. Симметрия переносит конфигурацию ВМЕСТЕ с её профилями, поэтому достаточно взять по
представителю от каждой орбиты: любая конфигурация эквивалентна какой-то, чья тройка профилей есть
представитель. Условие жёсткое: перебирать ВСЕ орбиты; пропуск одной обесценивает всё. Вес орбиты
(число троек в ней) берётся из этого же кода, а не проставляется руками.

usage: profile_orbits3.py n M cap  [--weights]
"""
import sys
from itertools import product, permutations

def main():
    n, M, cap = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    profs = [c for c in product(range(cap+1), repeat=n) if sum(c) == M]
    triples = [(a, b, c) for a in profs for b in profs for c in profs]
    def images(t):
        out = set()
        for perm in permutations(range(3)):
            for rev in product((0, 1), repeat=3):
                out.add(tuple(tuple(reversed(t[perm[k]])) if rev[k] else t[perm[k]] for k in range(3)))
        return out
    seen, reps = set(), []
    for t in triples:
        if t in seen: continue
        im = images(t)
        reps.append((t, len(im)))
        seen |= im
    tot = sum(w for _, w in reps)
    print(f"# n={n} M={M} cap={cap}: профилей по оси {len(profs)}, троек {len(triples)}, "
          f"ОРБИТ {len(reps)}, сумма весов {tot} (должна равняться числу троек: {tot == len(triples)})",
          file=sys.stderr)
    for t, w in reps:
        spec = ";".join(f"{i}=" + ",".join(map(str, t[i])) for i in range(3))
        print(f"{spec}\t{w}" if "--weights" in sys.argv else spec)

if __name__ == "__main__":
    main()
