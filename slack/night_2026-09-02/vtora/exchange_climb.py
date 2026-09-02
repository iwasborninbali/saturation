#!/usr/bin/env python3
"""exchange_climb.py — подъём обменами: к свидетелю применяется исчерпывающий j-обмен (j ≤ J) до тех пор, пока он даёт +1 точку.
Каждый шаг проверяется полным перебором троек (внутри exchange_search.search). Итог пишется в файл <prefix>_climb_<m>.txt.
usage: python3 exchange_climb.py J ФАЙЛ [out_prefix]"""
import sys, itertools
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from exchange_search import search
from rigidity_kappa import read_cube_files
J = int(sys.argv[1]); path = sys.argv[2]; prefix = sys.argv[3] if len(sys.argv) > 3 else path.rsplit('/', 1)[-1].replace('.txt', '')
name, pts = next(read_cube_files([path])); n = max(max(p) for p in pts) + 1; step = 0
while True:
    new = search(f"{prefix} шаг {step} ({len(pts)} точек)", pts, n, J)
    if not new: break
    pts = sorted(new); step += 1
    with open(f"{prefix}_climb_{len(pts)}.txt", "w") as f:
        f.write(f"# A399138 n={n} points={len(pts)} — exchange climb (j<={J}) from {path}, step {step}; verified inside exchange_search (all triples)\n")
        f.write("\n".join(f"{x} {y} {z}" for x, y, z in pts) + "\n")
print(f"ИТОГ подъёма: {len(pts)} точек после {step} шагов (старт {name})")
