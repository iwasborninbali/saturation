#!/usr/bin/env python3
"""lambda_scan_n.py — температура λ(n) max-entropy модели (maxent_pairs.py) при n=12…19: при каком λ модель воспроизводит
прямоугольники на решение и дисперсию чётности iden-решений базы; масштаб λ·n.
usage: python3 lambda_scan_n.py n_min n_max [moves]
"""
import sys, math, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from maxent_pairs import run
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c: i for i, c in enumerate(ALPHA)}
DB = "/Users/iwasborninbali/saturation/web/all_known_solutions"

def sol_stats(n):
    m2s = []; kees = []; hams = 0; sols = 0; dist = collections.Counter()
    for l in open(DB):
        l = l.strip()
        if not l or (len(l) - 1) // 2 != n or l[0] != '.': continue
        body = l[1:]; sols += 1
        rows = [[IDX[body[2 * r]], IDX[body[2 * r + 1]]] for r in range(n)]
        seen = collections.Counter(frozenset(cs) for cs in rows); m2s.append(sum(1 for v in seen.values() if v == 2))
        kees.append(sum(1 for r in range(n) for c in rows[r] if r % 2 == 0 and c % 2 == 0))
        cols = collections.defaultdict(list)
        for r in range(n):
            for c in rows[r]: cols[c].append(r)
        for rs in cols.values(): dist[abs(rs[0] - rs[1])] += 1
        seenr = [False] * n; cyc = 0
        for r0 in range(n):
            if seenr[r0]: continue
            cyc += 1; r, c = r0, rows[r0][0]
            while not seenr[r]:
                seenr[r] = True; c = rows[r][1] if c == rows[r][0] else rows[r][0]
                rr = cols[c]; r = rr[1] if rr[0] == r else rr[0]
        hams += (cyc == 1)
    mk = sum(kees) / sols; vk = sum((k - mk) ** 2 for k in kees) / sols
    q0 = {k: 2 * (n - k) / (n * (n - 1)) for k in range(1, n)}; tot = sum(dist.values())
    rho = {k: dist[k] / tot / q0[k] for k in range(1, n)}
    return sols, sum(m2s) / sols, vk, hams / sols, rho

def model_stats(n, lam, moves, seed):
    samples, _ = run(n, lam, moves, moves // 10, 100, seed); S = len(samples)
    m2 = sum(s[1] for s in samples) / S; kees = [s[3] for s in samples]; mk = sum(kees) / S; vk = sum((k - mk) ** 2 for k in kees) / S
    ham = sum(1 for s in samples if s[4]) / S
    dist = collections.Counter()
    for s in samples: dist.update(s[2])
    q0 = {k: 2 * (n - k) / (n * (n - 1)) for k in range(1, n)}; tot = sum(dist.values())
    rho = {k: dist[k] / tot / q0[k] for k in range(1, n)}
    return m2, vk, ham, rho

def cross(xs, ys, target):
    """λ, при котором кривая ys(xs) пересекает target (линейная интерполяция; None если не пересекает)."""
    for i in range(len(xs) - 1):
        a, b = ys[i] - target, ys[i + 1] - target
        if a == 0: return xs[i]
        if a * b < 0: return xs[i] + (xs[i + 1] - xs[i]) * a / (a - b)
    return None

if __name__ == "__main__":
    n_min, n_max = int(sys.argv[1]), int(sys.argv[2]); moves = int(sys.argv[3]) if len(sys.argv) > 3 else 600000
    ln_grid = [1.5, 2.0, 2.5, 3.0, 3.5, 4.0]
    print(f"{'n':>3} {'решений':>7} | {'прямоуг.':>8} {'дисп.k':>6} {'гам':>5} | " + " ".join(f"λn={x}: m2/vk/ρ-накл" for x in ln_grid) + " | λ*n(прямоуг) λ*n(чётн) λ*n(ρ)")
    for n in range(n_min, n_max + 1):
        sols, m2s, vks, hams, rho_s = sol_stats(n)
        ys_m2 = []; ys_vk = []; ys_sl = []; cells = []
        for x in ln_grid:
            lam = x / n
            m2, vk, ham, rho = model_stats(n, lam, moves, 100 + n)
            ks = [k for k in range(1, n) if rho[k] > 0 and rho_s[k] > 0]
            xs = [math.log(rho[k]) for k in ks]; ys = [math.log(rho_s[k]) for k in ks]
            mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            slope = sum((a - mx) * (b - my) for a, b in zip(xs, ys)) / sum((b - my) ** 2 for b in ys)
            ys_m2.append(m2); ys_vk.append(vk); ys_sl.append(slope); cells.append(f"{m2:.3f}/{vk:.2f}/{slope:.2f}")
        l_m2 = cross(ln_grid, ys_m2, m2s); l_vk = cross(ln_grid, ys_vk, vks); l_sl = cross(ln_grid, ys_sl, 1.0)
        f = lambda v: f"{v:.2f}" if v is not None else "—"
        print(f"{n:>3} {sols:>7} | {m2s:8.4f} {vks:6.3f} {hams:5.3f} | " + " ".join(f"{c:>18}" for c in cells) + f" | {f(l_m2):>8} {f(l_vk):>8} {f(l_sl):>6}", flush=True)
