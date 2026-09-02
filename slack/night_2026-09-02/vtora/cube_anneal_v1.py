#!/usr/bin/env python3
"""cube_anneal.py — T-модель в кубе [n]³ с фиксированным числом точек m: P(S) ∝ exp(−β·T(S)), T — число коллинеарных троек;
параллельный темперинг по лестнице β, ходы — перенос одной точки в пустую клетку (с вероятностью 1/2 — в клетку с минимальным κ среди
случайной выборки, иначе в случайную). T ведётся через массив κ (число пар точек, коллинеарных с клеткой): T = Σ_{s∈S} κ(s)/3.
Найденная конфигурация с T = 0 — свидетель A399138 с m точками; проверяется полным перебором троек и пишется в файл.
Калибровка на известном: n=6, m=64 (точный оптимум) и n=7, m=73 должны находиться; цель — n=7, m=74.
usage: python3 cube_anneal.py n m sweeps M seed [out_prefix]
"""
import sys, math, random, itertools, time

BETAS = [0.3, 0.6, 1.0, 1.5, 2.2, 3.2, 4.6, 6.7, 10.0]

def build_lines(n):
    N = n ** 3; cells = [(x, y, z) for x in range(n) for y in range(n) for z in range(n)]
    idx = {c: i for i, c in enumerate(cells)}; lines = [[() for _ in range(N)] for _ in range(N)]
    for i in range(N):
        x1, y1, z1 = cells[i]
        for j in range(i + 1, N):
            x2, y2, z2 = cells[j]; d = (x2 - x1, y2 - y1, z2 - z1)
            g = math.gcd(math.gcd(abs(d[0]), abs(d[1])), abs(d[2])); d = (d[0] // g, d[1] // g, d[2] // g)
            out = []
            for sgn in (1, -1):
                k = 1
                while True:
                    c = (x1 + sgn * k * d[0], y1 + sgn * k * d[1], z1 + sgn * k * d[2])
                    if not all(0 <= t < n for t in c): break
                    ci = idx[c]
                    if ci != j: out.append(ci)
                    k += 1
            lines[i][j] = lines[j][i] = tuple(out)
    return cells, lines

class Rep:
    def __init__(self, n, m, beta, lines, rnd):
        self.n, self.m, self.beta, self.lines, self.rnd = n, m, beta, lines, rnd; N = n ** 3
        self.occ = set(rnd.sample(range(N), m)); self.kap = [0] * N
        S = sorted(self.occ)
        for a in range(m):
            for b in range(a + 1, m):
                for c in lines[S[a]][S[b]]: self.kap[c] += 1
        self.T = sum(self.kap[s] for s in self.occ) // 3; self.acc = 0; self.tries = 0; self.best = self.T
    def remove(self, p):
        self.occ.remove(p)
        for s in self.occ:
            for c in self.lines[p][s]: self.kap[c] -= 1
    def add(self, q):
        for s in self.occ:
            for c in self.lines[q][s]: self.kap[c] += 1
        self.occ.add(q)
    def sweep(self, M):
        rnd, occ, N = self.rnd, self.occ, self.n ** 3
        for _ in range(M):
            p = rnd.choice(tuple(occ)) if len(occ) < 64 else next(iter(rnd.sample(sorted(occ), 1)))
            if rnd.random() < 0.5:
                cand = [c for c in rnd.sample(range(N), 24) if c not in occ]
                if not cand: continue
                q = min(cand, key=lambda c: self.kap[c])
            else:
                q = rnd.randrange(N)
                if q in occ: continue
            self.tries += 1
            self.remove(p); self.add(q)
            Tn = sum(self.kap[s] for s in occ) // 3; dT = Tn - self.T
            if dT <= 0 or rnd.random() < math.exp(-self.beta * dT):
                self.T = Tn; self.acc += 1
                if Tn < self.best: self.best = Tn
            else:
                self.remove(q); self.add(p)

def verify(pts):
    def cz(a, b, c):
        u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
        return u[1] * v[2] - u[2] * v[1] == 0 and u[2] * v[0] - u[0] * v[2] == 0 and u[0] * v[1] - u[1] * v[0] == 0
    return not any(cz(*t) for t in itertools.combinations(pts, 3))

if __name__ == "__main__":
    n, m, sweeps, M, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    prefix = sys.argv[6] if len(sys.argv) > 6 else f"anneal_n{n}_m{m}_s{seed}"
    rnd = random.Random(seed); t0 = time.time(); cells, lines = build_lines(n)
    reps = [Rep(n, m, b, lines, random.Random(seed * 1000 + i)) for i, b in enumerate(BETAS)]
    found = None; swaps = [0] * (len(BETAS) - 1)
    for sw in range(sweeps):
        for r in reps:
            r.sweep(M)
            if r.T == 0 and found is None:
                pts = sorted(cells[i] for i in r.occ)
                if verify(pts):
                    found = pts
                    with open(f"{prefix}_T0.txt", "w") as f:
                        f.write(f"# A399138 n={n} points={m} found by cube_anneal.py (T-model parallel tempering) seed={seed} sweep={sw} beta={r.beta}; verified: no three collinear\n")
                        f.write("\n".join(f"{x} {y} {z}" for x, y, z in pts) + "\n")
        for i in range(len(reps) - 1):
            a, b = reps[i], reps[i + 1]
            if rnd.random() < min(1.0, math.exp((a.beta - b.beta) * (a.T - b.T))):
                a.occ, b.occ = b.occ, a.occ; a.kap, b.kap = b.kap, a.kap; a.T, b.T = b.T, a.T; swaps[i] += 1
        if sw % max(sweeps // 20, 1) == 0 or found:
            print(f"sweep {sw:5d} {time.time()-t0:7.1f}s  T по репликам: " + " ".join(f"{r.T:3d}" for r in reps) + f"  лучшее {min(r.best for r in reps)}" + ("  НАЙДЕНО T=0" if found else ""), flush=True)
        if found: break
    print("итог:", "найден свидетель" if found else f"не найден; лучший T = {min(r.best for r in reps)}", f"; обмены {swaps}; время {time.time()-t0:.0f} с")
