"""block_subsets.py — k=-1: loss as a function of the number m of orbit blocks: for all (or sampled) m-subsets of blocks, the exact
maximum lawful subset of their union vs 8m.   usage: python3 slack/block_subsets.py p [max_subsets_per_m]"""
import sys, os, itertools, random
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maxlawful_pysat import lines
from ortools.sat.python import cp_model
from collections import Counter
p = int(sys.argv[1]); cap = int(sys.argv[2]) if len(sys.argv) > 2 else 60
h = (p - 1) // 2
def X(u): u %= p; return u if u <= h else u - p
pts_all = [(x, y) for x in range(-h, 3 * h + 2) for y in range(0, 2 * p) if (x * y) % p in (1, p - 1)]
blocks = {}
for a in range(1, h + 1):
    ia = pow(a, -1, p); cols = {X(a), X(a) + p, X(p - a), X(p - a) + p}; rows = {ia, ia + p, p - ia, 2 * p - ia}
    blocks[a] = [(x, y) for (x, y) in pts_all if x in cols and y in rows]
def maxlawful(pts, secs=120):
    P = sorted(pts); L = lines([(x + h, y) for x, y in P])
    m = cp_model.CpModel(); z = [m.NewBoolVar(f"z{i}") for i in range(len(P))]
    for mem in L: m.Add(sum(z[i] for i in mem) <= 2)
    m.Maximize(sum(z)); s = cp_model.CpSolver(); s.parameters.num_search_workers = 8; s.parameters.max_time_in_seconds = secs
    st = s.Solve(m); return int(s.ObjectiveValue()), st == cp_model.OPTIMAL
keys = sorted(blocks); rnd = random.Random(1)
for m in range(2, len(keys) + 1):
    subs = list(itertools.combinations(keys, m))
    if len(subs) > cap: subs = rnd.sample(subs, cap)
    losses = Counter(); nonopt = 0
    for sub in subs:
        v, opt = maxlawful(sum((blocks[a] for a in sub), [])); losses[8 * m - v] += 1; nonopt += (not opt)
    mean = sum(d * c for d, c in losses.items()) / sum(losses.values())
    print(f"p={p} m={m}: subsets {len(subs)}, loss distribution {sorted(losses.items())}, mean loss {mean:.2f}, mean loss per block {mean/m:.3f}{' (some not proved optimal)' if nonopt else ''}", flush=True)
