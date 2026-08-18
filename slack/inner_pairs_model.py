"""inner_pairs_model.py — k=-1 lower-bound family: restrict to 'vertical pairs in inner orbit blocks (|X(a)| <= p*frac), anything (singles or
pairs) elsewhere', i.e. for classes of inner blocks force: use both copies of a column or none (no singles, no horizontal/diagonal pairs);
compute the exact maximum (CP-SAT).  usage: python3 slack/inner_pairs_model.py p frac [workers] [secs]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import cands_M, lines
from ortools.sat.python import cp_model
p = int(sys.argv[1]); frac = float(sys.argv[2]); workers = int(sys.argv[3]) if len(sys.argv) > 3 else 8; secs = float(sys.argv[4]) if len(sys.argv) > 4 else 300
h = (p - 1) // 2; N = 2 * p
def X(u): u %= p; return u if u <= h else u - p
cands = cands_M(p, {1, p - 1}, N); idx = {c: i for i, c in enumerate(cands)}; L = lines(cands)
m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(len(cands))]
for mem in L: m.Add(sum(x[i] for i in mem) <= 2)
# inner blocks: |X(a)| <= frac*p  → for each column of such a class, both copies or none (per class per column)
groups = {}
for c in cands:
    a, b = c; Xa = a - h; A = Xa % p
    hyp = 1 if (Xa * b) % p == 1 else -1
    key = (hyp, A, a)          # class (hyp, residue A) and column a
    groups.setdefault(key, []).append(idx[c])
forced = 0
for (hyp, A, col), mem in groups.items():
    if abs(X(A)) <= frac * p and len(mem) == 2:
        m.Add(x[mem[0]] == x[mem[1]]); forced += 1
m.Maximize(sum(x)); s = cp_model.CpSolver(); s.parameters.num_search_workers = workers; s.parameters.max_time_in_seconds = secs
st = s.Solve(m)
print(f"p={p} frac={frac}: inner-pairs model optimum {int(s.ObjectiveValue())} = 3(p-1)+{int(s.ObjectiveValue())-3*(p-1)} ({s.StatusName(st)}, bound {s.BestObjectiveBound():.0f}); forced column-pairs {forced}")
