#!/usr/bin/env python3
"""soft_T_pt.py — мягкая T-модель P ∝ exp(−β·T) с параллельным темперингом (обмен реплик), чтобы дойти до ⟨T⟩ ~ 1–5,
где одиночная цепь замерзает (soft_T.py). Реплики на лестнице β; каждая делает M локальных ходов (обмены рёбер, ΔT через κ-массив),
потом попарные обмены соседних реплик с вероятностью min(1, exp((β_i − β_j)(T_i − T_j))). Наблюдаемые по каждой реплике:
⟨T⟩, κ (x−y), абсолютный спектр c_v = пар примитивного направления v на конфигурацию / n (среднее по ориентациям), прямоугольники,
дисперсия чётности, гамильтоновых, ρ(k) (наклон/Спирмен против решений n=20).
usage: python3 soft_T_pt.py n sweeps M seed  [лестница β фиксирована в коде]
"""
import sys, math, random, collections
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from maxent_pairs import random_config, observe
from soft_T import build_lines

BETAS = [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 6.0]
SHAPES = [(1, 1), (1, 2), (1, 3), (2, 3), (1, 4)]

def abs_spectrum(rows, n):
    pts = [(r, c) for r in range(n) for c in rows[r]]
    cnt = collections.Counter()
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dx, dy = pts[j][0] - pts[i][0], pts[j][1] - pts[i][1]
            if dx == 0 or dy == 0: continue
            g = math.gcd(abs(dx), abs(dy)); a, b = abs(dx) // g, abs(dy) // g
            cnt[(min(a, b), max(a, b))] += 1
    out = {}
    for s in SHAPES:
        orient = 2 if s[0] == s[1] else 4
        out[s] = cnt[s] / n / orient
    return out

class Replica:
    def __init__(self, n, beta, lines, rnd):
        self.n = n; self.beta = beta; self.lines = lines; self.rnd = rnd; N = n * n
        self.rows = random_config(n, rnd); self.occ = set(r * n + c for r in range(n) for c in self.rows[r])
        self.kap = [0] * N; S = sorted(self.occ)
        for a in range(len(S)):
            for b in range(a + 1, len(S)):
                for c in lines[S[a]][S[b]]: self.kap[c] += 1
        self.T = sum(self.kap[s] for s in self.occ) // 3; self.acc = 0; self.tries = 0
    def remove(self, p):
        self.occ.remove(p)
        for s in self.occ:
            for c in self.lines[p][s]: self.kap[c] -= 1
    def add(self, q):
        for s in self.occ:
            for c in self.lines[q][s]: self.kap[c] += 1
        self.occ.add(q)
    def sweep(self, M):
        n, rnd, rows, occ = self.n, self.rnd, self.rows, self.occ
        for _ in range(M):
            r1 = rnd.randrange(n); r2 = rnd.randrange(n)
            if r1 == r2: continue
            c1 = rows[r1][rnd.randrange(2)]; c2 = rows[r2][rnd.randrange(2)]
            if c1 == c2: continue
            p1, p2 = r1 * n + c1, r2 * n + c2; q1, q2 = r1 * n + c2, r2 * n + c1
            if q1 in occ or q2 in occ: continue
            self.tries += 1
            self.remove(p1); self.remove(p2); self.add(q1); self.add(q2)
            Tn = sum(self.kap[s] for s in occ) // 3; dT = Tn - self.T
            if dT <= 0 or rnd.random() < math.exp(-self.beta * dT):
                rows[r1][rows[r1].index(c1)] = c2; rows[r2][rows[r2].index(c2)] = c1; self.T = Tn; self.acc += 1
            else:
                self.remove(q1); self.remove(q2); self.add(p1); self.add(p2)

def swap_states(a, b):
    a.rows, b.rows = b.rows, a.rows; a.occ, b.occ = b.occ, a.occ; a.kap, b.kap = b.kap, a.kap; a.T, b.T = b.T, a.T

if __name__ == "__main__":
    n, sweeps, M, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    rnd = random.Random(seed); lines = build_lines(n)
    reps = [Replica(n, b, lines, random.Random(seed * 100 + i)) for i, b in enumerate(BETAS)]
    swaps = [0] * (len(BETAS) - 1); swap_tries = [0] * (len(BETAS) - 1)
    samples = collections.defaultdict(list); burn = sweeps // 5
    for sw in range(sweeps):
        for r in reps: r.sweep(M)
        for i in range(len(reps) - 1):
            a, b = reps[i], reps[i + 1]; swap_tries[i] += 1
            if rnd.random() < min(1.0, math.exp((a.beta - b.beta) * (a.T - b.T))):
                swap_states(a, b); swaps[i] += 1
        if sw >= burn:
            for r in reps:
                samples[r.beta].append(observe(r.rows, n) + (r.T, abs_spectrum(r.rows, n)))
    obs_rho = {1: 1.07, 2: 1.35, 3: 1.36, 4: 1.30, 5: 0.96, 6: 1.22, 7: 0.59, 8: 0.83, 9: 0.66, 10: 0.88, 11: 0.44, 12: 1.18, 13: 0.43, 14: 0.71, 15: 1.26, 16: 0.91, 17: 0.69, 18: 1.30, 19: 1.02}
    print(f"n={n}, sweeps {sweeps} × M={M} локальных ходов на реплику, лестница β {BETAS}; обмены приняты: " + " ".join(f"{s}/{t}" for s, t in zip(swaps, swap_tries)))
    print(f"{'β':>4} {'⟨T⟩':>6} {'P(T=0)':>6} {'κ':>6} {'c11':>6} {'c12':>6} {'c13':>6} {'c23':>6} {'c14':>6} {'прям.':>6} {'дисп.k':>6} {'гам':>5} {'ρ накл/Сп':>10} {'лок.прин.':>9}")
    for r in reps:
        S = samples[r.beta]; L = len(S)
        Tm = sum(s[8] for s in S) / L; P0 = sum(1 for s in S if s[8] == 0) / L; kap1 = sum(s[6] for s in S) / L
        cs = {sh: sum(s[9][sh] for s in S) / L for sh in SHAPES}
        m2 = sum(s[1] for s in S) / L; kees = [s[3] for s in S]; mk = sum(kees) / L; vk = sum((k - mk) ** 2 for k in kees) / L
        ham = sum(1 for s in S if s[4]) / L
        dist = collections.Counter()
        for s in S: dist.update(s[2])
        tot = sum(dist.values()); q0 = {k: 2 * (n - k) / (n * (n - 1)) for k in range(1, n)}
        rho = {k: dist[k] / tot / q0[k] for k in range(1, n)}
        ks = [k for k in range(1, n) if rho[k] > 0]
        if n == 20 and len(ks) > 3:
            xs = [math.log(rho[k]) for k in ks]; ys = [math.log(obs_rho[k]) for k in ks]; mx, my = sum(xs) / len(xs), sum(ys) / len(ys)
            slope = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((y - my) ** 2 for y in ys)
            def ranks(v): s_ = sorted(v); return [s_.index(t) for t in v]
            rx, ry = ranks(xs), ranks(ys); a_, b_ = sum(rx) / len(rx), sum(ry) / len(ry)
            sp = sum((u - a_) * (w - b_) for u, w in zip(rx, ry)) / math.sqrt(sum((u - a_) ** 2 for u in rx) * sum((w - b_) ** 2 for w in ry))
        else: slope = sp = float('nan')
        print(f"{r.beta:>4} {Tm:6.2f} {P0:6.3f} {kap1:6.3f} {cs[(1,1)]:6.3f} {cs[(1,2)]:6.3f} {cs[(1,3)]:6.3f} {cs[(2,3)]:6.3f} {cs[(1,4)]:6.3f} {m2:6.3f} {vk:6.3f} {ham:5.3f} {slope:5.2f}/{sp:4.2f} {r.acc/max(r.tries,1):9.4f}")
    print("решения n=20: κ=c11 0.731, c12 0.56, c13 0.455, c23 0.41, c14 0.38 (коллега, abs_spectrum.py); прям. 0.340; дисп.k 0.422; гам 0.307")
