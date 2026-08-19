"""tradeoff_curve.py — the exact trade-off a(b) = max |S ∩ H(1)| over lawful S with |S ∩ H(-1)| = b (HJSW box, k = -1).
H4' says a(b) + b <= 3(p-1) + O(1), i.e. the curve has slope <= -1 in b relative to a(0) = 3(p-1).  usage: tradeoff_curve.py p [bmax]"""
import sys
from ortools.sat.python import cp_model
sys.path.insert(0, 'slack')
from exchange_pairs import pts
from lp_curve import lines
p = int(sys.argv[1]); P1, Pm = pts(p)
allp = sorted(set(P1) | set(Pm)); idx = {q: i for i, q in enumerate(allp)}
L = lines(allp, 'all')
i1 = [idx[q] for q in P1]; im = [idx[q] for q in Pm]
bmax = int(sys.argv[2]) if len(sys.argv) > 2 else 3 * (p - 1)
print(f"p={p}: |H(1)|={len(P1)} |H(-1)|={len(Pm)} points={len(allp)} lines>=3: {len(L)}; 3(p-1)={3*(p-1)}")
prev = None
for b in range(0, bmax + 1):
    m = cp_model.CpModel()
    x = [m.NewBoolVar(f'x{i}') for i in range(len(allp))]
    for s in L: m.Add(sum(x[i] for i in s) <= 2)
    m.Add(sum(x[i] for i in im) == b)
    m.Maximize(sum(x[i] for i in i1))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 120; sol.parameters.num_search_workers = 6
    st = sol.Solve(m)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        print(f"  b={b}: infeasible/unknown ({sol.StatusName(st)})"); break
    a = int(sol.ObjectiveValue()); tot = a + b
    print(f"  b={b:3d}: a(b)={a:3d}  a+b={tot:3d}  (a+b) - 3(p-1) = {tot - 3*(p-1):+3d}  [{sol.StatusName(st)}]", flush=True)
    prev = a
