"""arc_imbalance.py — numerics for the arc-imbalance lemma (theorem C, weak form): along the primitive-root cycle, F_K[j] = 1[κ_{g^j} special],
F_M[j] = 1[μ_{g^{j+1}} special]; the arc sums Σ_{j∈I}(F_K − F_M) are controlled by the DFT of the sequences: Ŝ(m) = Σ_j F[j] e(mj/(p−1)).
Prints max_{m≠0}|Ŝ_K(m)|/√p, same for M and for the difference, and the maximal arc imbalance (walk range) — expected O(√p log^c p).
usage: arc_imbalance.py p1 p2 ..."""
import sys, math, numpy as np
sys.path.insert(0, 'slack')
from cycle_stats import specials, prim_root
for p in map(int, sys.argv[1:]):
    g = prim_root(p); S = specials(p, g); L = p - 1
    FK = np.zeros(L); FM = np.zeros(L); a = 1
    for j in range(L):
        FK[j] = ('K', a) in S; FM[j] = ('M', (g * a) % p) in S; a = (g * a) % p
    D = FK - FM
    fk = np.fft.fft(FK); fm = np.fft.fft(FM); fd = np.fft.fft(D)
    mk = np.max(np.abs(fk[1:])); mm = np.max(np.abs(fm[1:])); md = np.max(np.abs(fd[1:]))
    # walk range = max arc imbalance (cyclic): range of prefix sums (D sums to 0)
    pref = np.concatenate([[0], np.cumsum(D)]); rng = pref.max() - pref.min()
    # also the largest arc sum over ALL arcs (cyclic) = range of prefix sums since total = 0
    print(f"p={p} g={g}: |K|=|M|={int(FK.sum())}  max_m|S_K|/sqrt p={mk/math.sqrt(p):.2f}  max|S_M|/sqrt p={mm/math.sqrt(p):.2f}  max|S_D|/sqrt p={md/math.sqrt(p):.2f}  "
          f"(log p={math.log(p):.1f})  max arc |imbalance|={int(rng)} = {rng/math.sqrt(p):.2f} sqrt p", flush=True)
