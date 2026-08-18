"""pareto_pair.py — the exchange (Pareto) frontier of H(1) vs H(k) in the HJSW box: for m = 0..3(p-1), f(m) = max |S ∩ P_k| over lawful
S ⊆ P_1 ∪ P_k with |S ∩ P_1| >= m.  alpha(P_k) = max_m (m + f(m)).   usage: python3 slack/pareto_pair.py p k [workers] [secs per m]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import cands_M, lines
from ortools.sat.python import cp_model
p = int(sys.argv[1]); k = int(sys.argv[2]) % p; workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8; secs = float(sys.argv[4]) if len(sys.argv) > 4 else 120
N = 2 * p; h = (p - 1) // 2
cands = cands_M(p, {1, k}, N); L = lines(cands)
def hyp(a, b):
    X, Y = a - h, b
    return 1 if (X * Y) % p == 1 else 2
idx1 = [i for i, c in enumerate(cands) if hyp(*c) == 1]; idx2 = [i for i, c in enumerate(cands) if hyp(*c) == 2]
print(f"p={p} k={k}: |P_1|={len(idx1)} |P_k|={len(idx2)} lines>=3: {len(L)}")
best = 0; front = []
for m in range(3 * (p - 1), -1, -1):
    mod = cp_model.CpModel(); x = [mod.NewBoolVar(f"x{i}") for i in range(len(cands))]
    for mem in L: mod.Add(sum(x[i] for i in mem) <= 2)
    mod.Add(sum(x[i] for i in idx1) >= m)
    mod.Maximize(sum(x[i] for i in idx2))
    s = cp_model.CpSolver(); s.parameters.num_search_workers = workers; s.parameters.max_time_in_seconds = secs
    st = s.Solve(mod)
    if st not in (cp_model.OPTIMAL, cp_model.FEASIBLE): print(f"m={m}: infeasible/unknown ({s.StatusName(st)})"); continue
    f = int(s.ObjectiveValue()); opt = (st == cp_model.OPTIMAL)
    front.append((m, f, opt)); best = max(best, m + f)
    print(f"m>={m:3d}: f(m)={f:3d}{'' if opt else '?'}  m+f={m+f:3d}", flush=True)
    if f >= len(idx2) - 0: break
print(f"alpha >= {best} (from the frontier); frontier:", [(m, f) for m, f, o in front])
