"""arc_imbalance_k.py — general k (order L, index r=(p-1)/L): per-coset imbalance Δ(a0)=#K−#M specials in the coset cycle,
walk range per cycle (max arc |imbalance| after removing the linear drift = range of prefix sums of D minus drift), and the
character-sum maxima max_{ψ≠1}|Ŝ_K(ψ)|/√p over ALL characters of F_p^* (DFT along a primitive root). usage: p k [p k ...]"""
import sys, math, numpy as np
sys.path.insert(0, 'slack')
from cycle_stats import specials, prim_root
args = list(map(int, sys.argv[1:]))
for p, k in zip(args[0::2], args[1::2]):
    S = specials(p, k); g = prim_root(p)
    L = 1
    while pow(k, L, p) != 1: L += 1
    r = (p - 1) // L
    # DFT along primitive root of the full indicator functions
    FK = np.zeros(p - 1); FM = np.zeros(p - 1); a = 1
    for j in range(p - 1):
        FK[j] = ('K', a) in S; FM[j] = ('M', a) in S; a = a * g % p
    fk = np.abs(np.fft.fft(FK)); fm = np.abs(np.fft.fft(FM))
    # cosets: a0 = g^i, i=0..r-1
    worst = 0; worstD = 0
    for i in range(r):
        a0 = pow(g, i, p); D = []; x = a0
        for j in range(L):
            D.append((('K', x) in S) - (('M', k * x % p) in S)); x = k * x % p
        D = np.array(D, dtype=float); tot = D.sum()
        pref = np.concatenate([[0], np.cumsum(D - tot / L)])
        worst = max(worst, pref.max() - pref.min()); worstD = max(worstD, abs(tot))
    print(f"p={p} k={k} L={L} r={r}: |K|={int(FK.sum())} |M|={int(FM.sum())} max_ψ|S_K|/√p={fk[1:].max()/math.sqrt(p):.2f} max|S_M|/√p={fm[1:].max()/math.sqrt(p):.2f} "
          f"max coset |Δ|={int(worstD)} ({worstD/math.sqrt(p):.2f}√p) max drift-free walk range={worst:.1f} ({worst/math.sqrt(p):.2f}√p)", flush=True)
