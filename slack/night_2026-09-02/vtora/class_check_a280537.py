#!/usr/bin/env python3
"""class_check_a280537.py — класс эквивалентности свидетеля A280537 относительно всех известных свидетелей того же n и размера:
certs/a280537/*.txt, certs/a280537_first_solver/**/*.txt, strata_p_mirror/, strata_p_long_mirror/ (кроме самого файла).
Каноническая форма под 48 движениями куба (cube_strata.act) + инварианты (стабилизатор, мультимножество квадратов расстояний).
usage: python3 class_check_a280537.py ФАЙЛ   → одна строка: НОВЫЙ класс / эквивалентен <файл>"""
import sys, glob, re, os, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(HERE + "/../../..")
sys.path.insert(0, HERE + "/.."); sys.path.insert(0, HERE)
from cube_strata import all_matrices, act
from kappa_general import read_pts
G = all_matrices()
def canon(S, n): return min(tuple(sorted(act(M, c, n) for c in S)) for M in G)
def stab(S, n): return sum(1 for M in G if {act(M, c, n) for c in S} == set(S))
def dinv(S): return tuple(sorted(collections.Counter(sum((a[i]-b[i])**2 for i in range(3)) for i, a in enumerate(S) for b in S[i+1:]).items()))
path = sys.argv[1]; S = read_pts(path)
hdr = re.search(r'\bn=(\d+)', open(path).readline()); n = int(hdr.group(1)) if hdr else max(max(p) for p in S) + 1
m = len(S); cS = canon(S, n)
pool = glob.glob(ROOT + "/certs/a280537/*.txt") + glob.glob(ROOT + "/certs/a280537_first_solver/**/*.txt", recursive=True) + glob.glob(HERE + "/strata_p_mirror/*.txt") + glob.glob(HERE + "/strata_p_long_mirror/*.txt")
same = []; equiv = []
for f in pool:
    if os.path.abspath(f) == os.path.abspath(path) or "verify_witness" in f: continue
    try: T = read_pts(f)
    except Exception: continue
    if len(T) != m or not T: continue
    h = re.search(r'\bn=(\d+)', open(f).readline()); nT = int(h.group(1)) if h else max(max(p) for p in T) + 1
    if nT != n: continue
    same.append(f)
    if canon(T, n) == cS: equiv.append(os.path.relpath(f, ROOT))
if equiv: print(f"класс: эквивалентен {equiv[0]}" + (f" (+{len(equiv)-1})" if len(equiv) > 1 else "") + f"; |стаб|={stab(S, n)}")
else: print(f"класс: НОВЫЙ среди {len(same)} известных того же n={n} и размера {m}; |стаб|={stab(S, n)}; инвариант расстояний отличен от всех: {all(dinv(read_pts(f)) != dinv(S) for f in same)}")
