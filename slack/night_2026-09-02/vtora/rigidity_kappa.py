#!/usr/bin/env python3
"""rigidity_kappa.py — жёсткость как покрытие (вопрос 4 плана 2.09).

κ_S(q) — число пар точек S, коллинеарных с пустой клеткой q (в плоскости или в кубе). Клетка мертва ⟺ κ ≥ 1.
Лемма: в множестве без трёх коллинеарных прямая через точку p и клетку q несёт не больше одной другой точки S,
значит удаление p уменьшает κ(q) не больше чем на 1. Отсюда
  S жёстко (удаление любой точки оживляет только её) ⟺ min κ над пустыми клетками ≥ 2;
  удаление любых j точек оживляет только их же, если j < min κ.
Следствие: 2n-решение плоскости жёстко автоматически — строчная и столбцовая пары дают κ ≥ 2 (насыщенность, не максимальность).
Здесь: (а) плоскость — жадный случайный рост до тупика, доля жёстких среди тупиков размера 2n−1 и 2n−2, min κ;
       (б) куб — min κ и гистограмма κ у свидетелей A399138; оба счёта (прямой — оживление после удаления — и через κ) сверяются.
usage: python3 rigidity_kappa.py plane n runs seed | cube ФАЙЛ [ФАЙЛ …]
"""
import sys, math, random, collections, re

# ---------- общий счёт κ для решётки любой размерности ----------
def line_cells(p, q, n, dim):
    """все клетки решётки [0,n)^dim на прямой через p и q (включая p и q)."""
    d = [q[i] - p[i] for i in range(dim)]; g = 0
    for x in d: g = math.gcd(g, abs(x))
    d = [x // g for x in d]
    cells = []
    for sign in (1, -1):
        k = 0 if sign == 1 else -1
        while True:
            c = tuple(p[i] + k * sign * d[i] if sign == 1 else p[i] + k * d[i] for i in range(dim))
            c = tuple(p[i] + (k if sign == 1 else k) * d[i] for i in range(dim))
            if not all(0 <= x < n for x in c): break
            cells.append(c); k += 1 if sign == 1 else -1
    return cells

def kappa_map(S, n, dim):
    """κ для всех клеток (у занятых — тоже считается, но не используется)."""
    kap = collections.Counter(); S = list(S)
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            for c in line_cells(S[i], S[j], n, dim):
                if c != S[i] and c != S[j]: kap[c] += 1
    return kap

def alive_count(S, n, dim):
    kap = kappa_map(S, n, dim); Sset = set(S)
    return sum(1 for c in all_cells(n, dim) if c not in Sset and kap[c] == 0)

def all_cells(n, dim):
    import itertools
    return itertools.product(range(n), repeat=dim)

def rigidity_report(S, n, dim):
    """возвращает (min κ по пустым, гистограмма κ, число точек, удаление которых оживляет ≥ 2 клетки — прямой счёт)."""
    kap = kappa_map(S, n, dim); Sset = set(S)
    empties = [c for c in all_cells(n, dim) if c not in Sset]
    hist = collections.Counter(kap[c] for c in empties)
    mink = min(kap[c] for c in empties) if empties else None
    # прямой счёт: сколько клеток живы после удаления каждой точки
    revive = []
    for p in S:
        T = [s for s in S if s != p]
        revive.append(alive_count(T, n, dim))
    nonrigid_pts = sum(1 for r in revive if r >= 2)
    return mink, hist, nonrigid_pts, revive

# ---------- (а) плоскость: жадный случайный рост ----------
def greedy_deadend(n, rnd):
    kap = [[0] * n for _ in range(n)]; S = []
    occ = [[False] * n for _ in range(n)]
    while True:
        alive = [(x, y) for x in range(n) for y in range(n) if not occ[x][y] and kap[x][y] == 0]
        if not alive: return S
        q = rnd.choice(alive)
        for s in S:
            for c in line_cells(s, q, n, 2):
                if c != s and c != q: kap[c[0]][c[1]] += 1
        S.append(q); occ[q[0]][q[1]] = True

def plane(n, runs, seed):
    rnd = random.Random(seed); sizes = collections.Counter()
    stats = collections.defaultdict(lambda: {"total": 0, "rigid": 0, "mink": collections.Counter(), "mismatch": 0, "example": None})
    for _ in range(runs):
        S = greedy_deadend(n, rnd); m = len(S); sizes[m] += 1
        if m < 2 * n - 2: continue
        mink, hist, nonrigid, revive = rigidity_report(S, n, 2)
        st = stats[m]; st["total"] += 1; st["mink"][mink] += 1
        rigid = mink >= 2
        if rigid != (nonrigid == 0): st["mismatch"] += 1          # лемма: оба счёта обязаны совпасть
        if rigid: st["rigid"] += 1
        elif st["example"] is None: st["example"] = (S, revive)
    print(f"n={n}, тупиков {runs} (seed {seed}); размеры: " + " ".join(f"{k}:{v}" for k, v in sorted(sizes.items())))
    for m in sorted(stats):
        st = stats[m]
        print(f"  размер {m} ({'насыщенный' if m == 2*n else f'2n−{2*n-m}'}): тупиков {st['total']}, жёстких {st['rigid']} = {st['rigid']/st['total']:.3f}; "
              f"min κ: {dict(sorted(st['mink'].items()))}; расхождений двух счётов: {st['mismatch']}")
        if st["example"]:
            S, revive = st["example"]
            print(f"    контрпример (нежёсткий тупик): {sorted(S)}; оживает после удаления каждой точки: {revive}")

# ---------- (б) куб ----------
def read_cube_files(paths):
    for path in paths:
        txt = open(path).read()
        first = next((l for l in txt.splitlines() if l.strip()), '')
        if re.fullmatch(r'[\d,;]+', first.strip()):               # n4_28pt_optima_all14: строка = конфигурация "x,y,z;..."
            for i, l in enumerate(txt.splitlines()):
                pts = [tuple(map(int, t.split(','))) for t in l.strip().strip(';').split(';') if t]
                if pts: yield f"{path.rsplit('/',1)[-1]}#{i+1}", pts
            continue
        blocks = re.split(r'(?m)^(?=n= )', txt)
        found = False
        for b in blocks:
            m = re.match(r'n= (\d+) m= (\d+)', b)
            if not m: continue
            found = True
            pts = [tuple(int(t) for t in l.split()) for l in b.splitlines()[1:] if len(l.split()) == 3 and all(t.isdigit() for t in l.split())]
            yield f"{path.rsplit('/',1)[-1]} n={m.group(1)} m={m.group(2)}", pts
        if not found:
            pts = [tuple(int(t) for t in l.split()) for l in txt.splitlines() if not l.startswith('#') and len(l.split()) == 3 and all(t.isdigit() for t in l.split())]
            if pts: yield path.rsplit('/', 1)[-1], pts

def cube(paths):
    for name, pts in read_cube_files(paths):
        n = max(max(p) for p in pts) + 1
        # у файла свидетелей блоки с разным n — n берём как max+1 (для n=1 это 1)
        mink, hist, nonrigid, revive = rigidity_report(pts, n, 3)
        h = " ".join(f"{k}:{v}" for k, v in sorted(hist.items())[:8])
        rv = collections.Counter(revive)
        rigid_kappa = (mink is None) or mink >= 2          # нет пустых клеток — жёстко вакуумно
        rigid_direct = nonrigid == 0
        tag = 'ЖЁСТКО' if rigid_kappa else 'НЕЖЁСТКО'
        if rigid_kappa != rigid_direct: tag += '  !!! РАСХОЖДЕНИЕ ДВУХ СЧЁТОВ'
        print(f"{name:<44} n={n} m={len(pts):>3}  min κ={mink}  {tag}  нежёстких точек {nonrigid}/{len(pts)}  "
              f"оживает: {dict(sorted(rv.items()))}  κ-гистограмма пустых: {h}")

if __name__ == "__main__":
    if sys.argv[1] == "plane": plane(int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]))
    else: cube(sys.argv[2:])
