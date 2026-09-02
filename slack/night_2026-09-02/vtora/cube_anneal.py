#!/usr/bin/env python3
"""cube_anneal.py (v3) — T-модель в кубе [n]³ с фиксированным числом точек m: P(S) ∝ exp(−β·T(S)), T — число коллинеарных троек;
параллельный темперинг по лестнице β. Ходы — перенос одной точки (удаляемая — с вероятностью 1/2 участница тройки; целевая клетка — с
вероятностью 1/2 клетка с минимальным κ из случайной выборки). T ведётся через массив κ (число пар точек, коллинеарных с клеткой):
T = Σ_{s∈S} κ(s)/3.  v3: при T ≤ 2 — детерминированная «починка» по лемме о κ: перебор удалений по одной точке из каждой тройки,
живые клетки остатка (κ = 0), поиск совместимого пополнения размера |R| (даёт T = 0 при m точках) или |R|+1 (даёт m+1 точек — улучшение).
Каждое найденное множество с T = 0 размера ≥ m−1 записывается (провенанс в первой строке), m+1 — как отдельный файл с пометкой РЕКОРД.
Калибровка на известном: n=6, m=64; n=7, m=73. Цель — n=7, m=74.
usage: python3 cube_anneal.py n m sweeps M seed [out_prefix]
"""
import sys, math, random, itertools, time

BETAS = [0.3, 0.6, 1.0, 1.5, 2.2, 3.0, 4.0, 5.0, 6.5, 8.0, 10.0, 13.0]
SAMPLE = 32

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

def verify(pts):
    def cz(a, b, c):
        u = [b[i] - a[i] for i in range(3)]; v = [c[i] - a[i] for i in range(3)]
        return u[1] * v[2] - u[2] * v[1] == 0 and u[2] * v[0] - u[0] * v[2] == 0 and u[0] * v[1] - u[1] * v[0] == 0
    return not any(cz(*t) for t in itertools.combinations(pts, 3))

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
        rnd, occ, N, kap = self.rnd, self.occ, self.n ** 3, self.kap
        for _ in range(M):
            occl = tuple(occ)
            if self.T > 0 and rnd.random() < 0.5:
                bad = [s for s in occl if kap[s] > 0]
                p = rnd.choice(bad) if bad else rnd.choice(occl)
            else:
                p = rnd.choice(occl)
            if rnd.random() < 0.5:
                cand = [c for c in rnd.sample(range(N), SAMPLE) if c not in occ]
                if not cand: continue
                q = min(cand, key=lambda c: kap[c])
            else:
                q = rnd.randrange(N)
                if q in occ: continue
            self.tries += 1
            self.remove(p); self.add(q)
            Tn = sum(kap[s] for s in occ) // 3; dT = Tn - self.T
            if dT <= 0 or rnd.random() < math.exp(-self.beta * dT):
                self.T = Tn; self.acc += 1
                if Tn < self.best: self.best = Tn
            else:
                self.remove(q); self.add(p)
    def triples(self):
        occ, kap, lines = self.occ, self.kap, self.lines
        bad = sorted(s for s in occ if kap[s] > 0); out = set()
        for a, b in itertools.combinations(bad, 2):
            for c in lines[a][b]:
                if c in occ: out.add(tuple(sorted((a, b, c))))
        return sorted(out)
    def repair(self):
        """T ≤ 2: перебор удалений по точке из каждой тройки; возвращает список найденных T=0 множеств (индексы) размера m или m+1."""
        found = []; N = self.n ** 3; occ, kap, lines = self.occ, self.kap, self.lines
        trs = self.triples()
        if not trs or len(trs) > 3: return found
        seen = set()
        for R in itertools.product(*trs):
            R = frozenset(R)
            if R in seen: continue
            seen.add(R)
            for p in R: self.remove(p)
            alive = [c for c in range(N) if c not in occ and kap[c] == 0]
            need = len(R)
            if len(alive) >= need:
                rest = set(occ)
                def ok(A):
                    for a, b in itertools.combinations(A, 2):
                        if any(c in rest or c in A for c in lines[a][b]): return False
                    return True
                for k in (need + 1, need):
                    if len(alive) < k: continue
                    for A in itertools.combinations(alive, k):
                        if ok(A):
                            found.append(sorted(rest | set(A)))
                            if k == need + 1: break
                    if found and len(found[-1]) == self.m + 1: break
            for p in R: self.add(p)
            if found and len(found[-1]) == self.m + 1: break
        return found

if __name__ == "__main__":
    n, m, sweeps, M, seed = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])
    prefix = sys.argv[6] if len(sys.argv) > 6 else f"anneal_n{n}_m{m}_s{seed}"
    rnd = random.Random(seed); t0 = time.time(); cells, lines = build_lines(n)
    reps = [Rep(n, m, b, lines, random.Random(seed * 1000 + i)) for i, b in enumerate(BETAS)]
    record = None; swaps = [0] * (len(BETAS) - 1); saved = set(); n_same = 0
    def save(pts_idx, tag, sw, beta):
        global record
        key = tuple(sorted(pts_idx))
        if key in saved: return
        pts = sorted(cells[i] for i in key)
        if not verify(pts): print("ВНИМАНИЕ: кандидат не прошёл полную проверку троек", flush=True); return
        saved.add(key)
        fn = f"{prefix}_{tag}_{len(pts)}_{len(saved)}.txt"
        with open(fn, "w") as f:
            f.write(f"# A399138 n={n} points={len(pts)} found by cube_anneal.py v3 (T-model parallel tempering + κ-repair) seed={seed} sweep={sw} beta={beta} tag={tag}; verified: no three collinear\n")
            f.write("\n".join(f"{x} {y} {z}" for x, y, z in pts) + "\n")
        if len(pts) > m: record = pts; print(f"!!! РЕКОРД: {len(pts)} точек, файл {fn}", flush=True)
    for sw in range(sweeps):
        for r in reps:
            r.sweep(M)
            if r.T == 0:
                save(r.occ, "T0", sw, r.beta); n_same += 1
            elif r.T <= 2:
                for S in r.repair():
                    save(S, "repair", sw, r.beta)
                    if len(S) == m:      # принять починенное состояние как текущее
                        for p in list(r.occ - set(S)): r.remove(p)
                        for q in [c for c in S if c not in r.occ]: r.add(q)
                        r.T = 0; r.best = 0
        for i in range(len(reps) - 1):
            a, b = reps[i], reps[i + 1]
            if rnd.random() < min(1.0, math.exp((a.beta - b.beta) * (a.T - b.T))):
                a.occ, b.occ = b.occ, a.occ; a.kap, b.kap = b.kap, a.kap; a.T, b.T = b.T, a.T; swaps[i] += 1
        if sw % max(sweeps // 20, 1) == 0 or record:
            print(f"sweep {sw:5d} {time.time()-t0:7.1f}s  T по репликам: " + " ".join(f"{r.T:3d}" for r in reps) + f"  лучшее {min(r.best for r in reps)}  T=0-множеств сохранено {len(saved)}" + ("  РЕКОРД" if record else ""), flush=True)
        if record: break
    print("итог:", f"РЕКОРД {len(record)} точек" if record else f"рекорда нет; лучший T = {min(r.best for r in reps)}; сохранено T=0-множеств размера {m}: {len(saved)}", f"; обмены {swaps}; время {time.time()-t0:.0f} с")
