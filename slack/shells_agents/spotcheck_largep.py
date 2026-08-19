"""spotcheck_largep.py -- VERIFIER task (3): independent large-p spot check, pair vs quad{1,-1,2,-2},
at p not covered by the concurrent large_p.py sweep (which used 41,53,61,71,89,101,127).
Uses null_search.anneal (same annealer, but freshly invoked, independent driver code, and its
own certification pass) at p=43, 47.

usage: python3 spotcheck_largep.py
"""
import sys, time, math, itertools
sys.path.insert(0, '/home/pmbot/projects/saturation_peer/slack')
from diffusion_sampler import hyper_points, build_lines
from null_search import anneal

def certify(points):
    n = len(points)
    for i, j, k in itertools.combinations(range(n), 3):
        x1, y1 = points[i]; x2, y2 = points[j]; x3, y3 = points[k]
        if (x2 - x1) * (y3 - y1) - (y2 - y1) * (x3 - x1) == 0:
            return False
    return True

LOG = '/home/pmbot/projects/saturation_peer/slack/verification/verify_spotcheck_largep.txt'

if __name__ == '__main__':
    ps = [43, 47]
    budget = 90.0
    seeds = 3
    with open(LOG, 'a') as log:
        def out(s):
            print(s, flush=True); print(s, file=log, flush=True)
        out(f"\n=== spotcheck_largep.py {time.ctime()} budget={budget}s/config seeds={seeds} ===")
        for p in ps:
            row = {}
            for name, cs in (("pair", (1, p - 1)), ("quad_k2", (1, p - 1, 2, p - 2))):
                pts = hyper_points(p, cs); lines = build_lines(pts)
                best = 0; bestS = []
                per_seed = budget / seeds
                t0 = time.time()
                for s in range(seeds):
                    v, idxs = anneal(pts, lines, seconds=per_seed, seed=100 + s)
                    if v > best: best, bestS = v, idxs
                el = time.time() - t0
                chosen = [pts[i] for i in bestS]
                ok = certify(chosen)
                N = 2 * p
                out(f"p={p:3d} {name:8s}: points={len(pts):4d} lines={len(lines):5d} best={best:3d} "
                    f"certified={ok} alpha/N={best/N:.4f} alpha/(p-1)={best/(p-1):.4f} time={el:.0f}s")
                row[name] = best
            adv = row["quad_k2"] - row["pair"]
            ratio = row["quad_k2"] / row["pair"]
            out(f"p={p}: quad-pair={adv:+d} quad/pair={ratio:.4f}")
