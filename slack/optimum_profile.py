"""optimum_profile.py — how is a TRUE optimum of P_{-1} distributed over the orbit unions U_i = O_i ∪ R(O_i)?
Locally each U_i admits 16 (generic) / 8 (exceptional) points, and the sum of these is 4(p-1); the truth is ~3(p-1),
so on average each union gives up ~4 points.  This prints the per-union profile of an optimal solution (and of several optima).
usage: optimum_profile.py p [nsolutions]"""
import sys
from collections import defaultdict
from ortools.sat.python import cp_model
sys.path.insert(0, 'slack')
from orbit_pairs import unions
from lp_curve import lines as alllines
p = int(sys.argv[1]); K = int(sys.argv[2]) if len(sys.argv) > 2 else 3
Us = unions(p)
allpts = sorted({q for _, U in Us for q in U})
idx = {q: i for i, q in enumerate(allpts)}
L = alllines(allpts, 'all')
own = {}
for i, (_, U) in enumerate(Us):
    for q in U: own[q] = i
m = cp_model.CpModel()
x = [m.NewBoolVar(f'x{i}') for i in range(len(allpts))]
for s in L: m.Add(sum(x[i] for i in s) <= 2)
m.Maximize(sum(x))
sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = 600; sol.parameters.num_search_workers = 6
st = sol.Solve(m)
best = int(sol.ObjectiveValue())
prof = defaultdict(int)
for q in allpts:
    if sol.Value(x[idx[q]]): prof[own[q]] += 1
caps = [len(U) // 2 for _, U in Us]
print(f"p={p}: alpha = {best} ({best/(p-1):.3f}(p-1)); unions {len(Us)} with local caps {caps} (sum {sum(caps)} = 4(p-1) = {4*(p-1)})")
print(f"  optimum profile per union: {[prof[i] for i in range(len(Us))]}  (deficits {[caps[i]-prof[i] for i in range(len(Us))]})", flush=True)
