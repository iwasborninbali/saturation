"""diffusion_sampler.py — "points in superposition, collapsed by diffusion" (owner's idea, 2026-08-19).
State: u in [0,1]^n — the amplitude of each candidate point (a point is not fixed until the calculation collapses it).
Step (denoise): for every line l with sum_{i in l} u_i > 2, push the excess back proportionally to u_i (a soft projection onto
the polytope {sum_l u <= 2}); a few sweeps = alternating projections.  Step (noise): u += eta*N(0,1), clipped to [0,1].
Annealing: the temperature (eta) decreases while a sharpening exponent grows, so the cloud condenses onto a lawful configuration.
Rounding: greedily fix points in order of u, keeping feasibility; then a local repair pass (drop-2-add-3).
usage: diffusion_sampler.py <points-spec> ...  (see main); as a library: run(points, lines, iters, seed) -> lawful subset"""
import sys, time
import numpy as np

def build_lines(pts):
    from collections import defaultdict
    import math
    idx = {q: i for i, q in enumerate(pts)}; L = defaultdict(set)
    n = len(pts)
    for i in range(n):
        x1, y1 = pts[i]
        for j in range(i + 1, n):
            x2, y2 = pts[j]
            dx, dy = x2 - x1, y2 - y1
            g = math.gcd(abs(dx), abs(dy)); dx //= g; dy //= g
            if dx < 0 or (dx == 0 and dy < 0): dx, dy = -dx, -dy
            c = dy * x1 - dx * y1
            L[(dx, dy, c)] |= {i, j}
    return [sorted(s) for s in L.values() if len(s) >= 3]

def run(pts, lines, iters=400, seed=0, eta0=0.35, verbose=False):
    rng = np.random.default_rng(seed)
    n = len(pts)
    inc = [np.array(l, dtype=np.int64) for l in lines]
    u = rng.random(n) * 0.5 + 0.25
    best = None; best_size = -1
    for t in range(iters):
        frac = t / iters
        eta = eta0 * (1 - frac) ** 2
        # denoise: soft projection onto the line constraints (several sweeps)
        for _ in range(3):
            for l in inc:
                s = u[l].sum()
                if s > 2:
                    u[l] *= 2.0 / s
        # sharpen (condensation): push towards {0,1}
        gamma = 1.0 + 3.0 * frac
        u = np.clip(u ** gamma * (1 + 0.6 * frac), 0, 1)
        # noise
        u = np.clip(u + eta * rng.standard_normal(n), 0, 1)
        if t % 25 == 0 or t == iters - 1:
            S = round_greedy(u, inc, n)
            if len(S) > best_size: best_size, best = len(S), S
            if verbose: print(f"   t={t} |S|={len(S)} best={best_size}", flush=True)
    return best

def round_greedy(u, inc, n):
    order = np.argsort(-u)
    cnt = np.zeros(len(inc), dtype=np.int64)
    memb = [[] for _ in range(n)]
    for li, l in enumerate(inc):
        for i in l: memb[i].append(li)
    S = []
    for i in order:
        if all(cnt[li] < 2 for li in memb[i]):
            S.append(int(i))
            for li in memb[i]: cnt[li] += 1
    # local repair: try to add any point that fits (after the greedy pass some may fit)
    changed = True
    while changed:
        changed = False
        for i in range(n):
            if i in S: continue
            if all(cnt[li] < 2 for li in memb[i]):
                S.append(i)
                for li in memb[i]: cnt[li] += 1
                changed = True
    return sorted(S)

def hyper_points(p, cs):
    h = (p - 1) // 2; x0, y0 = -h, 0
    P = set()
    for c in cs:
        for x in range(1, p):
            y = c * pow(x, -1, p) % p
            bx = x0 + ((x - x0) % p); by = y0 + ((y - y0) % p)
            for r in (0, 1):
                for s in (0, 1): P.add((bx + r * p, by + s * p))
    return sorted(P)

if __name__ == '__main__':
    p = int(sys.argv[1]); k = int(sys.argv[2]); iters = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 3
    for name, cs in (("pair", (1, p - 1)), ("quad", (1, p - 1, k % p, (p - k) % p))):
        pts = hyper_points(p, cs); lines = build_lines(pts)
        t0 = time.time(); best = 0
        for s in range(seeds):
            S = run(pts, lines, iters=iters, seed=s)
            best = max(best, len(S))
        print(f"p={p} {name} (k={k}): points {len(pts)}, lines {len(lines)}; diffusion best = {best} = {best/(p-1):.3f}(p-1) = {best/(2*p):.3f}N  [{time.time()-t0:.0f}s]", flush=True)
