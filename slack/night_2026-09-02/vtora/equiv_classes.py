#!/usr/bin/env python3
"""equiv_classes.py — классы эквивалентности свидетелей куба под 48 движениями (перестановки координат × отражения x→n−1−x).
usage: python3 equiv_classes.py ФАЙЛ [ФАЙЛ …]   (формат: строки 'x y z', комментарии с #; файл witnesses/ с блоками тоже понимается)
Печатает: для каждого файла — размер, класс; итог — число классов по размерам."""
import sys, itertools, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from rigidity_kappa import read_cube_files
def canon(S, n):
    return min(tuple(sorted(tuple((n-1-p[perm[i]]) if s[i] else p[perm[i]] for i in range(3)) for p in S)) for perm in itertools.permutations(range(3)) for s in itertools.product([0,1], repeat=3))
if __name__ == "__main__":
    classes = {}; rows = []
    for name, pts in read_cube_files(sys.argv[1:]):
        n = max(max(p) for p in pts) + 1; c = canon(pts, n); key = (n, len(pts), c)
        if key not in classes: classes[key] = len([k for k in classes if k[:2] == key[:2]]) + 1
        rows.append((name, n, len(pts), classes[key]))
    for name, n, m, cl in rows: print(f"{name:<44} n={n} m={m:>3}  класс #{cl}")
    cnt = collections.Counter((k[0], k[1]) for k in classes)
    print("классов по (n, m):", dict(sorted(cnt.items())))
