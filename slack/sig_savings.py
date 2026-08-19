"""sig_savings.py — table  signature -> exact IP saving  for the components (runs of consecutive QRs) of P_{-1},
using the xi-bit description of the signature (docs/research/run_signature_law.md).  O(p) per prime + one small MILP per new signature.
Signature = bit pattern (xi_1..xi_{k-1}) canonicalised under the involution eps -> flip(reverse(eps)).
usage: sig_savings.py p_lo p_hi [maxk] [out.json]"""
import sys, json, time
from collections import defaultdict
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds

def primes(a, b): return [q for q in range(max(3, a), b) if all(q % d for d in range(2, int(q**.5) + 1))]

def canon(bits):
    r = tuple(1 - b for b in reversed(bits))
    return min(tuple(bits), r)

def ip_saving(U):
    idx = {q: i for i, q in enumerate(U)}; lines = defaultdict(list)
    for (x, y) in U:
        lines[('r', y)].append(idx[(x, y)]); lines[('c', x)].append(idx[(x, y)])
        lines[('d', x - y)].append(idx[(x, y)]); lines[('a', x + y)].append(idx[(x, y)])
    L = [m for m in lines.values() if len(m) >= 3]
    A = np.zeros((len(L), len(U)))
    for i, m in enumerate(L):
        for j in m: A[i, j] = 1
    r = milp(c=-np.ones(len(U)), constraints=LinearConstraint(A, -np.inf, 2 * np.ones(len(L))),
             bounds=Bounds(0, 1), integrality=np.ones(len(U)))
    return len(U) / 2 - (-r.fun)

def components(p):
    """returns list of (bits, point set) for the runs of consecutive QRs (t = d^2/4)"""
    h = (p - 1) // 2; x0 = -h; y0 = 0
    sq = np.zeros(p, dtype=bool); root = np.zeros(p, dtype=np.int64)
    for r in range(p):
        s = r * r % p
        if not sq[s]: sq[s] = True; root[s] = r
    X = lambda u: u - p if u % p > h else u % p
    inv4 = pow(4, -1, p)
    # points and their t-value
    pts_by_t = defaultdict(list)
    for x in range(1, p):
        ix = pow(x, -1, p)
        for y in (ix, (-ix) % p):
            for Xl in (x0 + ((x - x0) % p), x0 + ((x - x0) % p) + p):
                for Yl in (y0 + ((y - y0) % p), y0 + ((y - y0) % p) + p):
                    t = ((Xl - Yl) ** 2 % p) * inv4 % p
                    pts_by_t[t].append((Xl, Yl))
    # runs of consecutive t with sq[t]
    out = []
    used = set()
    for t0 in range(p):
        if not sq[t0] or t0 in used: continue
        if sq[(t0 - 1) % p]: continue          # not a run start
        run = []; t = t0
        while sq[t % p] and (t % p) not in used:
            used.add(t % p); run.append(t % p); t += 1
            if len(run) > 60: break
        if len(run) < 2: continue
        bits = []
        for i in range(len(run) - 1):
            a = (int(root[run[i]]) + int(root[run[i + 1]])) % p
            b = (int(root[run[i + 1]]) - int(root[run[i]])) % p
            bits.append(1 if X(a) * X(b) < 0 else 0)
        U = sorted(set(q for t_ in run for q in pts_by_t.get(t_, [])))
        out.append((tuple(bits), U))
    return out

if __name__ == '__main__':
    lo, hi = int(sys.argv[1]), int(sys.argv[2])
    maxk = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    out = sys.argv[4] if len(sys.argv) > 4 else 'slack/t221/sig_savings.json'
    TAB = {}; CNT = defaultdict(int); CONFLICT = []
    t0 = time.time()
    for p in primes(lo, hi):
        for bits, U in components(p):
            k = len(bits) + 1
            if k > maxk: continue
            c = canon(bits); CNT[c] += 1
            if len(U) != 32 * (k - 1):     # degenerate component (t = 0 or a degenerate pair): skip
                continue
            if c in TAB: continue
            TAB[c] = ip_saving(U)
        if p % 200 < 20:
            print(f"  p={p}: signatures {len(TAB)} [{time.time()-t0:.0f}s]", flush=True)
    print(f"total signatures with a saving: {len(TAB)}; possible for k<=maxk: {sum(1 for k in range(2, maxk+1) for b in range(2**(k-1)) if canon(tuple((b>>i)&1 for i in range(k-1))) == tuple((b>>i)&1 for i in range(k-1)))}")
    for c in sorted(TAB, key=lambda c: (len(c), c)):
        print(f"  {''.join(map(str,c)):10s} k={len(c)+1} saving={TAB[c]:6.2f} count={CNT[c]}")
    json.dump({'saving': {''.join(map(str, k)): v for k, v in TAB.items()},
               'count': {''.join(map(str, k)): v for k, v in CNT.items()}}, open(out, 'w'), indent=0)
    print("written", out)
