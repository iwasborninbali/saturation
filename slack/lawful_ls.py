"""lawful_ls.py — fast lower bounds: local search for a large lawful subset of a candidate set (min-conflicts on the
collinearity hypergraph of the candidates), witnesses re-checked with saturation.the_law.
usage: lawful_ls.py M p N k1,k2 [seconds] [seed]   |   lawful_ls.py PH p k N [seconds] [seed]"""
import sys, os, random, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import saturation as S
from maxlawful_pysat import cands_M, cands_PH, lines

def search(cands, secs, seed):
    rng = random.Random(seed)
    n = len(cands); L = lines(cands)
    # for each candidate: the lines it lies on (indices), each line = set of member indices
    memb = [[] for _ in range(n)]
    for li, mem in enumerate(L):
        for k in mem: memb[k].append(li)
    Lset = [set(mem) for mem in L]
    # also pairs of candidates that are the only two on their line: no constraint (fine)
    inS = [False] * n; cnt = [0] * len(L)   # cnt[li] = chosen points on line li
    def conflicts(k):                     # extra collinear triples created by adding k
        return sum(cnt[li] * (cnt[li] - 1) // 2 for li in memb[k])
    def add(k):
        inS[k] = True
        for li in memb[k]: cnt[li] += 1
    def rem(k):
        inS[k] = False
        for li in memb[k]: cnt[li] -= 1
    best = 0; best_set = []
    t0 = time.time()
    order = list(range(n))
    while time.time() - t0 < secs:
        # random greedy start
        for k in range(n):
            if inS[k]: rem(k)
        rng.shuffle(order)
        for k in order:
            if conflicts(k) == 0: add(k)
        # plateau / (1,2)-swap walk
        stall = 0
        while stall < 400 and time.time() - t0 < secs:
            cur = sum(inS)
            if cur > best:
                best = cur; best_set = [i for i in range(n) if inS[i]]; stall = 0
            # try adding any free candidate
            free = [k for k in range(n) if not inS[k] and conflicts(k) == 0]
            if free: add(rng.choice(free)); continue
            # (1,1)/(1,2) swap: remove a random chosen point, add up to two now-free candidates
            chosen = [k for k in range(n) if inS[k]]
            r = rng.choice(chosen); rem(r)
            free = [k for k in range(n) if not inS[k] and k != r and conflicts(k) == 0]
            rng.shuffle(free)
            added = 0
            for k in free:
                if conflicts(k) == 0: add(k); added += 1
            if added == 0: add(r)
            stall += 1
    return best, best_set

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "M":
        p, N = int(sys.argv[2]), int(sys.argv[3]); ks = {int(k) % p for k in sys.argv[4].split(",")}
        cands = cands_M(p, ks, N); secs = float(sys.argv[5]) if len(sys.argv) > 5 else 60; seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
        tag = f"M p={p} ks={sorted(ks)} N={N}"
    else:
        p, k, N = int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]); cands = cands_PH(p, k, N)
        secs = float(sys.argv[5]) if len(sys.argv) > 5 else 60; seed = int(sys.argv[6]) if len(sys.argv) > 6 else 1
        tag = f"PH p={p} k={k} N={N}"
    best, bs = search(cands, secs, seed)
    pts = [cands[i] for i in bs]
    S.the_law(frozenset(x * N + y for (x, y) in pts), N)
    print(f"{tag}: candidates={len(cands)} local-search best={best} (ratio {best/N:.3f}) lawful ✓ seed={seed}", flush=True)
    print("witness:", sorted(pts))
