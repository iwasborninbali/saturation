"""arcmod_cpsat.py — A(m) = max |S|, S ⊂ Z_m², no triple with det(b−a,c−a) ≡ 0 (mod m), via CP-SAT (maximize, multi-worker).
Symmetry breaking (valid for maximum arcs with |S| ≥ 3): (0,0) ∈ S; some (g,0) ∈ S for a divisor g<m of m; FIX1: (1,0) ∈ S when m=p².
Witness re-checked: det condition mod m + saturation.the_law (lawful in the m×m grid).  usage: arcmod_cpsat.py m secs [workers] [FIX1] [lb]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
from ortools.sat.python import cp_model
m = int(sys.argv[1]); secs = float(sys.argv[2]); workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8
fix1 = "FIX1" in sys.argv; lb = int(sys.argv[-1]) if sys.argv[-1].isdigit() and len(sys.argv) > 4 and sys.argv[-1] != sys.argv[3] else 0
N = m * m
mdl = cp_model.CpModel(); x = [mdl.NewBoolVar(f"x{i}") for i in range(N)]
# rows/cols: at most 2 (implied, but helps propagation)
for u in range(m): mdl.Add(sum(x[u * m + v] for v in range(m)) <= 2)
for v in range(m): mdl.Add(sum(x[u * m + v] for u in range(m)) <= 2)
# every det-zero triple is a clause (det ≡ 0 mod m is not transitive for composite/prime-power m: no "lines")
nt = 0
for a in range(N):
    ua, va = divmod(a, m)
    for b in range(a + 1, N):
        ub, vb = divmod(b, m); du, dv = ub - ua, vb - va
        for c in range(b + 1, N):
            uc, vc = divmod(c, m)
            if (du * (vc - va) - dv * (uc - ua)) % m == 0:
                mdl.AddBoolOr([x[a].Not(), x[b].Not(), x[c].Not()]); nt += 1
nl = nt
mdl.Add(x[0] == 1)
divs = [g for g in range(1, m) if m % g == 0]
mdl.AddBoolOr([x[g * m] for g in divs])
if fix1: mdl.Add(x[1 * m] == 1)
if lb: mdl.Add(sum(x) >= lb)
mdl.Maximize(sum(x))
solver = cp_model.CpSolver(); solver.parameters.max_time_in_seconds = secs; solver.parameters.num_workers = workers
st = solver.Solve(mdl)
status = solver.StatusName(st)
if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    pts = [i for i in range(N) if solver.Value(x[i])]
    P = [divmod(p, m) for p in pts]
    for i in range(len(P)):
        for j in range(i + 1, len(P)):
            for k in range(j + 1, len(P)):
                (ua, va), (ub, vb), (uc, vc) = P[i], P[j], P[k]
                assert ((ub - ua) * (vc - va) - (vb - va) * (uc - ua)) % m != 0
    S.the_law(frozenset(pts), m)
    print(f"m={m}: {status} best={len(pts)} bound={solver.BestObjectiveBound():.0f} lines={nl} secs={solver.WallTime():.0f} fix1={int(fix1)} points={sorted(P)}", flush=True)
else:
    print(f"m={m}: {status} bound={solver.BestObjectiveBound():.0f}", flush=True)
