"""conjA_replicate.py — independent replication of Reverse Finding 1 of deep research 8 (Conjecture A without Burgess).
Model (B.17 / §21): families z = s1 + i s2 in Z[i] (up to units/conjugation); a family is PRESENT for the prime p iff
chi_p(N) = +1 with N = s1^2 + s2^2; a present family contributes >= c0 * p/(s1+s2)^2 patterns, so
   E(p)/(p-1)  >=  c0 * SUM_{present, sigma <= sigma0} 1/sigma^2,     sigma = s1+s2.
Since chi_p is multiplicative, the presence pattern is determined by the bits chi_p(q) for the primes q dividing some N to an ODD power:
a point of F_2^m.  Hence  min over p  >=  min over all 2^m patterns  — a finite computation (Walsh/enumeration).
usage: conjA_replicate.py [sigma0 ...]"""
import sys
from math import gcd
from collections import defaultdict

def families(sigma0, primitive=True, s1_pos=True):
    """z = s1 + i s2 up to units and conjugation: 0 <= s1 <= s2 (or 1 <= s1 <= s2), s1 + s2 <= sigma0"""
    out = []
    lo = 1 if s1_pos else 0
    for s1 in range(lo, sigma0 + 1):
        for s2 in range(s1, sigma0 + 1 - s1 + 1):
            if s1 + s2 > sigma0: break
            if primitive and gcd(s1, s2) != 1: continue
            if s1 == s2 and s1 > 1: continue
            out.append((s1, s2))
    return out

def factor(n):
    f = {}; d = 2
    while d * d <= n:
        while n % d == 0: f[d] = f.get(d, 0) + 1; n //= d
        d += 1
    if n > 1: f[n] = f.get(n, 0) + 1
    return f

def analyse(sigma0, primitive=True, s1_pos=True, verbose=True):
    fams = families(sigma0, primitive, s1_pos)
    prim_index = {}; masks = []; weights = []
    for (s1, s2) in fams:
        N = s1 * s1 + s2 * s2
        odd = [q for q, a in factor(N).items() if a % 2 == 1]
        mask = 0
        for q in odd:
            if q not in prim_index: prim_index[q] = len(prim_index)
            mask |= 1 << prim_index[q]
        masks.append(mask); weights.append(1.0 / (s1 + s2) ** 2)
    m = len(prim_index)
    if verbose:
        print(f"sigma0={sigma0} (primitive={primitive}): families={len(fams)}, generators m={m}, primes={sorted(prim_index)}")
    # min over 2^m patterns of sum of weights of families with EVEN parity (chi(N) = +1 <=> parity of the bits is even)
    best = None; arg = None
    if m <= 26:
        import numpy as np
        w = np.array(weights); mk = np.array(masks, dtype=np.int64)
        # parity of popcount(mask & pattern)
        tot = np.zeros(1 << m)
        for wi, mi in zip(w, mk):
            if mi == 0:                      # N is a perfect square: always present
                tot += wi; continue
            idx = np.arange(1 << m, dtype=np.int64)
            par = np.bitwise_and(idx, mi)
            # popcount parity
            v = par.copy(); pc = np.zeros_like(v)
            while v.any():
                pc ^= (v & 1).astype(np.int64); v >>= 1
            tot += wi * (pc == 0)
        j = int(np.argmin(tot)); best = float(tot[j]); arg = j
    return len(fams), m, best, arg, prim_index

if __name__ == '__main__':
    for s0 in (map(int, sys.argv[1:]) if len(sys.argv) > 1 else (16, 18, 20)):
        for prim in (True, False):
            n, m, best, arg, pi = analyse(s0, primitive=prim, verbose=(prim is True))
            if best is not None:
                print(f"   primitive={prim}: families={n} m={m} min over 2^m of SUM 1/sigma^2 = {best:.6f}"
                      f"  (x c0=24.4 -> {24.4*best:.2f})", flush=True)
