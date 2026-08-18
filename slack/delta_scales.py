"""delta_scales.py — illustration of B.17: for primes p ≤ pmax, delta_p(M) = fraction of Gaussian integers z (up to units, gcd-free not
required) with M ≤ N(z) < 2M whose norm N(z) = s1²+s2² is a quadratic residue mod p, at dyadic scales M = 2^j with 2M < p; the Lemma
(square scales never empty) predicts delta_p(M²)+delta_p(2M²) ≥ c/log M.  Also the sum S(p) = Σ_j delta_p(2^j) (drives E(p)/(p-1) ≫ log log p).
usage: delta_scales.py pmax"""
import sys, math
def primes(n): return [q for q in range(3, n + 1) if all(q % d for d in range(2, int(q ** 0.5) + 1))]
def legendre(x, p): x %= p; return 0 if x == 0 else (1 if pow(x, (p - 1) // 2, p) == 1 else -1)
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 400
print("p: [delta_p(M) for M=2,4,8,...] (2M<p) | S=sum delta | zero scales | min over j of delta(2^j)+delta(2^{j+1})")
worst = []
for p in primes(pmax):
    if p < 11: continue
    deltas = []; M = 2
    while 2 * M < p:
        tot = qr = 0
        # z = s1 + i s2 up to units: take s1 > 0, s2 >= 0 (one representative of each unit orbit, z ≠ 0)
        r = int(math.isqrt(2 * M)) + 1
        for s1 in range(1, r + 1):
            for s2 in range(0, r + 1):
                n = s1 * s1 + s2 * s2
                if M <= n < 2 * M:
                    tot += 1; qr += (legendre(n, p) == 1)
        deltas.append(qr / tot if tot else float('nan')); M *= 2
    S = sum(d for d in deltas if d == d)
    zeros = sum(1 for d in deltas if d == 0)
    pairs = [deltas[j] + deltas[j + 1] for j in range(len(deltas) - 1)]
    mn = min(pairs) if pairs else float('nan')
    worst.append((mn, p))
    print(f"{p:4d}: {' '.join(f'{d:.2f}' for d in deltas)} | S={S:.2f} | zeros={zeros} | min pair={mn:.2f}", flush=True)
worst.sort(); print("# smallest consecutive-scale sums (delta(2^j)+delta(2^{j+1})):", worst[:8])
