"""uniqueness.py — единственность оптимума с точностью до 48 симметрий куба (первый солвер).
КОРРЕКТНАЯ форма блокировки: кардинальность РОВНО M, и для каждого из 48 образов T найденного решения ставится
sum_{p in T} x_p <= M-1, что при |S| = |T| = M равносильно «S != T» (без надмножеств/подмножеств).
Порядок переменных можно перемешать (--shuffle SEED), чтобы совпадение решений разных решателей не объяснялось порядком.
usage: uniqueness.py n M [seconds] [--shuffle SEED]"""
import sys, time, random
from itertools import combinations, permutations, product
from collections import defaultdict
from math import gcd
from ortools.sat.python import cp_model
n = int(sys.argv[1]); M = int(sys.argv[2]); T = float(sys.argv[3]) if len(sys.argv) > 3 else 900
shuffle = int(sys.argv[sys.argv.index('--shuffle')+1]) if '--shuffle' in sys.argv else None
pts = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
if shuffle is not None: random.Random(shuffle).shuffle(pts)
idx = {p: i for i, p in enumerate(pts)}
L = defaultdict(set)
for i in range(len(pts)):
    for j in range(i+1, len(pts)):
        p, q = pts[i], pts[j]; d = tuple(q[k]-p[k] for k in range(3))
        g = gcd(gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = tuple(v//g for v in d)
        if d[0] < 0 or (d[0] == 0 and (d[1] < 0 or (d[1] == 0 and d[2] < 0))): d = tuple(-v for v in d)
        base = p
        while all(0 <= base[k]-d[k] < n for k in range(3)): base = tuple(base[k]-d[k] for k in range(3))
        L[(base, d)] |= {i, j}
lines = [sorted(s) for s in L.values() if len(s) >= 3]
def images(S):
    out = set()
    for perm in permutations(range(3)):
        for fl in product([False, True], repeat=3):
            out.add(frozenset(tuple((n-1-p[perm[k]] if fl[k] else p[perm[k]]) for k in range(3)) for p in S))
    return out
def solve(blocked):
    m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(pts))]
    for s in lines: m.Add(sum(x[i] for i in s) <= 2)
    m.Add(sum(x) == M)                      # EXACT cardinality: "not superset of T" == "not equal to T"
    for Tset in blocked: m.Add(sum(x[idx[p]] for p in Tset) <= M-1)
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = 4
    t0 = time.time(); st = sol.Solve(m); el = time.time()-t0
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return {pts[i] for i in range(len(pts)) if sol.Value(x[i])}, el, sol.StatusName(st)
    return None, el, sol.StatusName(st)
S1, el1, st1 = solve([])
if S1 is None: print(f"n={n} M={M}: no solution at all ({st1}, {el1:.0f}s)"); sys.exit()
imgs = images(S1)
print(f"n={n} M={M} shuffle={shuffle}: first solution found in {el1:.0f}s; the configuration has {len(imgs)} distinct images under the 48 symmetries (stabiliser of order {48//len(imgs)}); blocking all of them...", flush=True)
S2, el2, st2 = solve(imgs)
if S2 is None:
    if st2 == 'INFEASIBLE':
        print(f"  second solution: INFEASIBLE in {el2:.0f}s  ->  THE OPTIMUM IS UNIQUE UP TO THE 48 CUBE SYMMETRIES")
    else:
        print(f"  second solution: {st2} in {el2:.0f}s  ->  NOT DECIDED (a timeout is NOT a proof of uniqueness)")
else:
    def canon(P):
        return min(tuple(sorted(Q)) for Q in images(P))
    print(f"  second solution FOUND in {el2:.0f}s, inequivalent to the first: {canon(S2)!=canon(S1)}")
    print("  second:", sorted(S2))
