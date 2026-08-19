"""constant_km1.py — the constant of the block-decomposition bound for k = -1:
   alpha(P_{-1}) <= (4 - sum_{k<=K} 2^{-(k+2)} sum_S (D_k(S)/k!) sav(S) + o(1))(p-1),
with the EXACT descent densities D_k(S)/k! (docs/research/run_signature_law.md) and the table of exact IP savings
(slack/t221/sig_savings.json, collected by slack/sig_savings.py; cross-checked against the second solver's comp_savings.json).
usage: constant_km1.py [K]"""
import json, math, sys
from itertools import product, permutations
from fractions import Fraction as F
K = int(sys.argv[1]) if len(sys.argv) > 1 else 8
sav = json.load(open('slack/t221/sig_savings.json'))['saving']
canon = lambda b: min(tuple(b), tuple(1 - x for x in reversed(b)))
D = lambda k, S: sum(1 for q in permutations(range(k)) if {i + 1 for i in range(k - 1) if q[i] > q[i + 1]} == S)
tot = F(0)
for k in range(2, K + 1):
    for pat in product((0, 1), repeat=k - 1):
        S = {i + 1 for i in range(k - 1) if pat[i]}
        key = ''.join(map(str, canon(pat)))
        if key in sav:
            tot += F(D(k, S), math.factorial(k)) * F(1, 2 ** (k + 2)) * F(sav[key]).limit_denominator(1000)
print(f"K={K}: saving/p = {tot} = {float(tot):.6f}   =>   alpha <= {4 - tot} = {float(4-tot):.4f} (p-1)")
print(f"tail (k>K, sav <= 4(k-1)) <= {float(sum(F(4*(k-1), 2**(k+2)) for k in range(K+1, 80))):.4f}")
