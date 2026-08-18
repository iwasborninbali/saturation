"""vertical_model.py — the 'vertical 2-factor' S_v of H(1) u H(k) in the HJSW box: for every class of H(1) take the copies (r,0),(r,1)
in column X+rp with r = r1, for every class of H(k) the copies in column X + (1-r1)p (so every column and every row has exactly 2
points: |S_v| = 4(p-1)).  Reports: collinear triples of S_v (count, by slope, by hyperbola composition), and the maximum lawful
subset of S_v (CP-SAT).   usage: python3 slack/vertical_model.py p k [r1] [workers] [secs]"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from math import gcd
from collections import Counter, defaultdict
p = int(sys.argv[1]); k = int(sys.argv[2]) % p; rule = sys.argv[3] if len(sys.argv) > 3 else "0"
# rule: "0"/"1" = constant r1 for H(1); "par" = H(1) in column X (r=0) iff |X| odd, else X+p — i.e. H(1) on odd x, H(k) on even x;
#       "par1" = the opposite parity
workers = int(sys.argv[4]) if len(sys.argv) > 4 else 4; secs = float(sys.argv[5]) if len(sys.argv) > 5 else 600
h = (p - 1) // 2
def base_x(a): return a if a <= h else a - p          # representative of residue a in [-h, h]
pts = {}   # (X,Y) -> (hyp, class)
for a in range(1, p):
    b1 = pow(a, -1, p); b2 = (k * b1) % p
    X = base_x(a)
    if rule in ("0", "1"): r1 = int(rule)
    elif rule == "par": r1 = 0 if abs(X) % 2 == 1 else 1
    elif rule == "par1": r1 = 1 if abs(X) % 2 == 1 else 0
    else: raise SystemExit("rule?")
    for s in (0, 1):
        pts[(X + r1 * p, b1 + s * p)] = (1, a)
        pts[(X + (1 - r1) * p, b2 + s * p)] = (2, a)
P = sorted(pts)
assert len(P) == 4 * (p - 1)
cols = Counter(X for X, Y in P); rows = Counter(Y for X, Y in P)
assert set(cols.values()) == {2} and set(rows.values()) == {2}, (cols, rows)
# collinear triples
lines = defaultdict(set)
for i in range(len(P)):
    for j in range(i + 1, len(P)):
        (x1, y1), (x2, y2) = P[i], P[j]; dx, dy = x2 - x1, y2 - y1; g = gcd(abs(dx), abs(dy)); dx //= g; dy //= g
        if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
        lines[(dx, dy, dx * y1 - dy * x1)].update([P[i], P[j]])
rich = {L: v for L, v in lines.items() if len(v) >= 3}
comp = Counter(); slopes = Counter(); sizes = Counter()
for L, v in rich.items():
    hs = tuple(sorted(Counter(pts[q][0] for q in v).items())); comp[hs] += 1; slopes[(L[0], L[1])] += 1; sizes[len(v)] += 1
print(f"p={p} k={k} rule={rule}: |S_v|={len(P)}; rich lines (>=3 points): {len(rich)}; sizes {dict(sizes)}")
print("  composition (hyperbola: count) of rich lines:", dict(comp))
print("  slopes of rich lines (top 10):", slopes.most_common(10))
# points on how many rich lines
inc = Counter()
for L, v in rich.items():
    for q in v: inc[q] += 1
print("  points on 0/1/2/3+ rich lines:", Counter(min(inc.get(q, 0), 3) for q in P))
# maximum lawful subset
try:
    from ortools.sat.python import cp_model
    idx = {q: i for i, q in enumerate(P)}
    m = cp_model.CpModel(); x = [m.NewBoolVar(f"x{i}") for i in range(len(P))]
    for L, v in rich.items(): m.Add(sum(x[idx[q]] for q in v) <= 2)
    m.Maximize(sum(x)); sol = cp_model.CpSolver(); sol.parameters.num_search_workers = workers; sol.parameters.max_time_in_seconds = secs
    st = sol.Solve(m)
    val = int(sol.ObjectiveValue()); print(f"  max lawful subset of S_v: {val} = 3(p-1)+{val-3*(p-1)}  (status {sol.StatusName(st)}, bound {sol.BestObjectiveBound():.0f}); loss from 4(p-1): {4*(p-1)-val}")
except ImportError:
    print("  (ortools not available: no maximum computed)")
