"""min_triples.py — H4 numerics: for P_{-1} (H(1)∪H(-1) in the HJSW box) minimise the number of collinear triples inside S subject to
<= 2 points per row and column and |S| = 3(p-1)+t.  CP-SAT: per rich line an integer count n_l and triples C(n_l,3) via AddElement.
usage: min_triples.py p t_lo t_hi [secs] [workers]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import cands_M, lines
from ortools.sat.python import cp_model
from math import comb
p = int(sys.argv[1]); tlo, thi = int(sys.argv[2]), int(sys.argv[3]); secs = float(sys.argv[4]) if len(sys.argv) > 4 else 300; workers = int(sys.argv[5]) if len(sys.argv) > 5 else 8
N = 2 * p; cands = cands_M(p, {1, p - 1}, N); n = len(cands); L = lines(cands)
rows = {}; cols = {}
for i, (x, y) in enumerate(cands): rows.setdefault(y, []).append(i); cols.setdefault(x, []).append(i)
for t in range(tlo, thi + 1):
    size = 3 * (p - 1) + t
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(n)]
    for mem in rows.values(): m.Add(sum(x[i] for i in mem) <= 2)
    for mem in cols.values(): m.Add(sum(x[i] for i in mem) <= 2)
    m.Add(sum(x) == size)
    tri = []
    for mem in L:
        k = len(mem)
        if all(cands[i][1] == cands[mem[0]][1] for i in mem) or all(cands[i][0] == cands[mem[0]][0] for i in mem): continue  # rows/cols
        cnt = m.NewIntVar(0, k, ""); m.Add(cnt == sum(x[i] for i in mem))
        tv = m.NewIntVar(0, comb(k, 3), ""); m.AddElement(cnt, [comb(j, 3) for j in range(k + 1)], tv); tri.append(tv)
    m.Minimize(sum(tri))
    s = cp_model.CpSolver(); s.parameters.max_time_in_seconds = secs; s.parameters.num_workers = workers
    st = s.Solve(m)
    print(f"p={p} |S|={size} (t={t}): {s.StatusName(st)} min_triples={int(s.ObjectiveValue()) if st in (cp_model.OPTIMAL, cp_model.FEASIBLE) else None} bound={s.BestObjectiveBound():.1f} time={s.WallTime():.0f}s", flush=True)
