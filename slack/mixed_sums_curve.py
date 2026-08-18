"""mixed_sums_curve.py — direct check of Step 3 of the arc lemma: mixed sums T(ψ;f) = Σ_{(x,b)∈C0(k)(F_p)} ψ(x) e(f/p),
f = m1 x + n1/x + m2 b + n2 k/b, along the partner curve C0(k): x b^2 - (x^2-1) b - k x = 0.  Reports max |T|/√p over
(a) all ψ≠1 with f=0 (DFT of the fibre count along a primitive root), (b) random (ψ,f) samples, (c) all ψ for a few fixed f.
usage: mixed_sums_curve.py p k [samples]"""
import sys, math, cmath, random, numpy as np
sys.path.insert(0, 'slack'); from cycle_stats import prim_root
p = int(sys.argv[1]); k = int(sys.argv[2]) % p; S = int(sys.argv[3]) if len(sys.argv) > 3 else 300
g = prim_root(p); ind = [0] * p; a = 1
for j in range(p - 1): ind[a] = j; a = a * g % p
sq = {}; 
for b in range(p): sq.setdefault(b * b % p, []).append(b)
pts = []  # (x, b)
for x in range(1, p):
    d = (x - pow(x, -1, p)) % p; disc = (d * d + 4 * k) % p
    if disc not in sq: continue
    for r in sq[disc]:
        b = (d + r) * pow(2, -1, p) % p
        pts.append((x, b))
        if r == 0: break
N = np.zeros(p - 1)
for x, b in pts: N[ind[x]] += 1
T0 = np.abs(np.fft.fft(N))  # T(ψ_m; 0) for all m (m=0 is the point count)
print(f"p={p} k={k}: |C0(k)(F_p) affine, x≠0| = {len(pts)} = p + {len(pts)-p:+d};  max_{{ψ≠1}} |T(ψ;0)|/√p = {T0[1:].max()/math.sqrt(p):.2f}")
rng = random.Random(1); e = lambda t: cmath.exp(2j * math.pi * t)
worst = 0
for _ in range(S):
    m = rng.randrange(1, p - 1); m1, n1, m2, n2 = (rng.randrange(p) for _ in range(4))
    T = 0
    for x, b in pts:
        f = (m1 * x + n1 * pow(x, -1, p) + m2 * b + n2 * k * pow(b, -1, p)) % p if b else None
        if f is None: continue
        T += e(m * ind[x] / (p - 1)) * e(f / p)
    worst = max(worst, abs(T) / math.sqrt(p))
print(f"  random (ψ,f) samples ({S}): max |T|/√p = {worst:.2f}")
# all ψ for fixed f: T(ψ_m; f) = DFT of the sequence u_j = Σ_{pts with ind x = j} e(f/p)
for (m1, n1, m2, n2) in [(1, 0, 0, 0), (0, 0, 1, 0), (1, 1, 1, 1), (3, 5, 7, 11)]:
    u = np.zeros(p - 1, dtype=complex)
    for x, b in pts:
        if b == 0: continue
        f = (m1 * x + n1 * pow(x, -1, p) + m2 * b + n2 * k * pow(b, -1, p)) % p
        u[ind[x]] += e(f / p)
    F = np.abs(np.fft.fft(u))
    print(f"  f=({m1},{n1},{m2},{n2}): max_ψ |T(ψ;f)|/√p = {F.max()/math.sqrt(p):.2f}  (incl. ψ=1: {F[0]/math.sqrt(p):.2f})")
