"""quad_hyperbolas.py — "extend the pair to a quadruple": exact maximum lawful subset of H(1) ∪ H(-1) ∪ H(k) ∪ H(-k) in the HJSW box.
Known: one hyperbola 3(p-1); the pair ~3(p-1)+O(1).  Question: does a larger ambient set (more hyperbolas = points in "superposition"
over several y-values per x) admit more?  usage: quad_hyperbolas.py p k [timeout_s]"""
import sys
from ortools.sat.python import cp_model
sys.path.insert(0, 'slack')
from lp_curve import lines as alllines
p = int(sys.argv[1]); k = int(sys.argv[2]) % p; T = float(sys.argv[3]) if len(sys.argv) > 3 else 300
h = (p - 1) // 2; x0, y0 = -h, 0
def hyper(c):
    P = []
    for x in range(1, p):
        y = c * pow(x, -1, p) % p
        bx = x0 + ((x - x0) % p); by = y0 + ((y - y0) % p)
        P += [(bx + r * p, by + s * p) for r in (0, 1) for s in (0, 1)]
    return sorted(set(P))
sets = {c: hyper(c) for c in (1, p - 1, k, (p - k) % p)}
for name, S in [("pair", set(sets[1]) | set(sets[p-1])), ("quad", set().union(*sets.values()))]:
    U = sorted(S); L = alllines(U, 'all')
    m = cp_model.CpModel(); x = [m.NewBoolVar(f'x{i}') for i in range(len(U))]
    for s in L: m.Add(sum(x[i] for i in s) <= 2)
    m.Maximize(sum(x))
    sol = cp_model.CpSolver(); sol.parameters.max_time_in_seconds = T; sol.parameters.num_search_workers = 6
    st = sol.Solve(m)
    print(f"p={p} k={k} {name}: |points|={len(U)} lines>=3: {len(L)}  alpha = {int(sol.ObjectiveValue())} "
          f"= {sol.ObjectiveValue()/(p-1):.3f}(p-1)  [{sol.StatusName(st)}, bound {sol.BestObjectiveBound():.0f}]", flush=True)
