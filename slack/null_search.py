"""null_search.py — local search on a union of hyperbolas (mass shells) with LIGHT-LIKE (null) moves.
Light-cone coordinates: u = x - y, v = x + y; the hyperbola xy = c is the shell v^2 - u^2 = 4c; lines of slope ±1 are the null lines
u = const / v = const.  A "photon-like" move slides a chosen point along a null line to another point of the union (possibly on a
different shell) -- this is the neighbourhood suggested by the owner's picture.  Simulated annealing over these moves plus add/drop.
usage: null_search.py p k [seconds] [seeds]"""
import sys, time, math, random
from collections import defaultdict
sys.path.insert(0, 'slack')
from diffusion_sampler import hyper_points, build_lines

def anneal(pts, lines, seconds=20.0, seed=0, T0=1.2, T1=0.02):
    n = len(pts); rng = random.Random(seed)
    memb = [[] for _ in range(n)]
    for li, l in enumerate(lines):
        for i in l: memb[i].append(li)
    # null-neighbour lists: same u = x-y or same v = x+y
    byu = defaultdict(list); byv = defaultdict(list)
    for i, (x, y) in enumerate(pts): byu[x - y].append(i); byv[x + y].append(i)
    nb = [list({j for j in byu[pts[i][0]-pts[i][1]] + byv[pts[i][0]+pts[i][1]] if j != i}) for i in range(n)]
    cnt = [0] * len(lines); inS = [False] * n; size = 0
    best = 0; bestS = []
    t0 = time.time()
    while True:
        el = time.time() - t0
        if el > seconds: break
        T = T0 * (T1 / T0) ** (el / seconds)
        r = rng.random()
        if r < 0.45:                                  # add
            i = rng.randrange(n)
            if inS[i]: continue
            if all(cnt[li] < 2 for li in memb[i]):
                inS[i] = True; size += 1
                for li in memb[i]: cnt[li] += 1
        elif r < 0.6:                                 # drop (accept with Boltzmann)
            i = rng.randrange(n)
            if not inS[i]: continue
            if rng.random() < math.exp(-1.0 / T):
                inS[i] = False; size -= 1
                for li in memb[i]: cnt[li] -= 1
        else:                                         # NULL MOVE: slide a point along a light-like line
            i = rng.randrange(n)
            if not inS[i] or not nb[i]: continue
            j = rng.choice(nb[i])
            if inS[j]: continue
            inS[i] = False
            for li in memb[i]: cnt[li] -= 1
            if all(cnt[li] < 2 for li in memb[j]):
                inS[j] = True
                for li in memb[j]: cnt[li] += 1
            else:                                     # revert unless the temperature allows the loss
                if rng.random() < math.exp(-1.0 / T): size -= 1
                else:
                    inS[i] = True
                    for li in memb[i]: cnt[li] += 1
        if size > best:
            best = size; bestS = [i for i in range(n) if inS[i]]
    return best, bestS

if __name__ == '__main__':
    p = int(sys.argv[1]); k = int(sys.argv[2]); secs = float(sys.argv[3]) if len(sys.argv) > 3 else 20
    seeds = int(sys.argv[4]) if len(sys.argv) > 4 else 4
    for name, cs in (("pair", (1, p - 1)), ("quad", (1, p - 1, k % p, (p - k) % p))):
        pts = hyper_points(p, cs); lines = build_lines(pts)
        b = 0
        for s in range(seeds):
            v, _ = anneal(pts, lines, seconds=secs, seed=s)
            b = max(b, v)
        print(f"p={p} {name} (k={k}): points {len(pts)} lines {len(lines)}; null-SA best = {b} = {b/(p-1):.3f}(p-1) = {b/(2*p):.3f}N", flush=True)
