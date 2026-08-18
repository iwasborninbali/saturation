"""periodic_model.py — k=-1, the y-PERIODIC model: S is a union of vertical pairs (both lifts of a class in one column); per column x
choose H(1) (both copies), H(-1) (both copies) or nothing.  Row/column and collinearity constraints via the rich lines of P.
CP-SAT exact optimum; compare with alpha(P_{-1}).   usage: python3 slack/periodic_model.py p [workers] [secs]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import cands_M, lines
from ortools.sat.python import cp_model
p = int(sys.argv[1]); workers = int(sys.argv[2]) if len(sys.argv) > 2 else 8; secs = float(sys.argv[3]) if len(sys.argv) > 3 else 600
h = (p - 1) // 2; N = 2 * p
cands = cands_M(p, {1, p - 1}, N); idx = {c: i for i, c in enumerate(cands)}
L = lines(cands)
# column-class variables: (x, eps) -> its two points
def cls(c):
    a, b = c; X, Y = a - h, b
    return (a, 1 if (X * Y) % p == 1 else -1)
groups = {}
for c in cands: groups.setdefault(cls(c), []).append(idx[c])
assert all(len(v) == 2 for v in groups.values())
m = cp_model.CpModel(); z = {g: m.NewBoolVar(f"z{g}") for g in groups}
for x in {g[0] for g in groups}:
    m.Add(z[(x, 1)] + z[(x, -1)] <= 1)
# point selected iff its group selected; every line (>=3 candidates) gets <= 2 selected points
for mem in L:
    m.Add(sum(z[cls(cands[i])] for i in mem) <= 2)      # each group contributes its number of points on the line
m.Maximize(sum(2 * v for v in z.values()))
s = cp_model.CpSolver(); s.parameters.num_search_workers = workers; s.parameters.max_time_in_seconds = secs
st = s.Solve(m)
val = int(s.ObjectiveValue()); print(f"p={p}: periodic optimum = {val} = 3(p-1)+{val-3*(p-1)}  ({s.StatusName(st)}, bound {s.BestObjectiveBound():.0f}); columns used {val//2} of {2*p-2}")
