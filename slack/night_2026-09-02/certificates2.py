"""Сертификаты смерти на узлах, которые DFS с forward-checking действительно посещает (n=12).
A = forward-checking (в каждой оставшейся строке >= 2 живых, в столбцах хватает);  B = Холл/поток;
D = одношаговый просмотр (есть пара в следующей строке, после которой A держится);  C = истина + число узлов до доказательства."""
import random, math, itertools, collections, time, sys
random.seed(7)
n = 12
pairs = list(itertools.combinations(range(n), 2))
CAP = 300000

def line_cells(p, q):
    (x1,y1),(x2,y2) = p, q
    dx, dy = x2-x1, y2-y1; g = math.gcd(abs(dx),abs(dy)); dx//=g; dy//=g
    out = []; x, y = x1, y1
    while 0 <= x < n and 0 <= y < n: out.append((x,y)); x += dx; y += dy
    x, y = x1-dx, y1-dy
    while 0 <= x < n and 0 <= y < n: out.append((x,y)); x -= dx; y -= dy
    return out

def place(pts, forb, colc, p):
    for q in pts:
        for c in line_cells(p, q): forb.add(c)
    pts.append(p); colc[p[0]] += 1

def alive_rows(forb, colc, d):
    return {y: [x for x in range(n) if colc[x] < 2 and (x,y) not in forb] for y in range(d, n)}

def check_A(forb, colc, d):
    ar = alive_rows(forb, colc, d)
    if any(len(v) < 2 for v in ar.values()): return False
    cols = collections.Counter(x for v in ar.values() for x in v)
    return all(cols[x] >= 2 - colc[x] for x in range(n))

def lawful_pairs(pts, forb, colc, r):
    """пары для строки r, законные и сохраняющие A для строк > r; возвращает список готовых состояний"""
    out = []
    cand = [x for x in range(n) if colc[x] < 2 and (x,r) not in forb]
    for i in range(len(cand)):
        for j in range(i+1, len(cand)):
            pts2, forb2, colc2 = list(pts), set(forb), list(colc)
            place(pts2, forb2, colc2, (cand[i], r))
            if (cand[j], r) in forb2: continue
            place(pts2, forb2, colc2, (cand[j], r))
            if check_A(forb2, colc2, r+1): out.append((pts2, forb2, colc2))
    return out

def sample_node(d):
    pts, forb, colc = [], set(), [0]*n
    for r in range(d):
        opts = lawful_pairs(pts, forb, colc, r)
        if not opts: return None
        pts, forb, colc = random.choice(opts)
    return pts, forb, colc

def check_B(forb, colc, d):
    ar = alive_rows(forb, colc, d); rows = list(ar)
    cap_col = {x: 2 - colc[x] for x in range(n)}
    flow = collections.defaultdict(int); used = collections.defaultdict(int)
    def aug(y, seen):
        for x in ar[y]:
            if flow[(y,x)] or x in seen: continue
            seen.add(x)
            if used[x] < cap_col[x]: flow[(y,x)] = 1; used[x] += 1; return True
            for y2 in rows:
                if y2 != y and flow[(y2,x)] and aug(y2, seen):
                    flow[(y2,x)] = 0; flow[(y,x)] = 1; return True
        return False
    return all(aug(y, set()) for y in rows for _ in range(2))

def check_C(pts, forb, colc, d, counter):
    if d == n: return True
    for pts2, forb2, colc2 in lawful_pairs(pts, forb, colc, d):
        counter[0] += 1
        if counter[0] > CAP: return None
        r = check_C(pts2, forb2, colc2, d+1, counter)
        if r is None or r: return r
    return False

plan = {4: 120, 6: 250, 8: 400}
print(f"n={n}; узлы после forward-checking; на глубину: {plan}")
print(f"{'d':>3} {'узлов':>5} {'мёртвых':>8} {'B ловит':>8} {'D ловит':>8} {'невидимых':>10} {'узлов на смерть: медиана / p90 / max':>36} {'доля работы в невидимых':>24}")
for d, M in plan.items():
    t0 = time.time(); dead = b = dd = 0; work_all = []; work_inv = []; unmeasured = 0; live = 0
    for _ in range(M):
        s = None
        while s is None: s = sample_node(d)
        pts, forb, colc = s
        B = check_B(forb, colc, d)
        D = len(lawful_pairs(pts, forb, colc, d)) > 0
        cnt = [0]; C = check_C(pts, forb, colc, d, cnt)
        if C is None: unmeasured += 1; continue
        if C: live += 1; continue
        dead += 1; b += (not B); dd += (not D)
        work_all.append(cnt[0])
        if B and D: work_inv.append(cnt[0])
    w = sorted(work_all); tot = sum(work_all) or 1
    med = w[len(w)//2] if w else 0; p90 = w[int(0.9*len(w))] if w else 0; mx = w[-1] if w else 0
    print(f"{d:>3} {M:>5} {dead/(M-unmeasured):8.3f} {b/max(dead,1):8.3f} {dd/max(dead,1):8.3f} {1-max(b,dd)/max(dead,1):10.3f} "
          f"{med:>12} / {p90:>6} / {mx:>6} {sum(work_inv)/tot:24.3f}   (живых {live}, не измерено {unmeasured}, {time.time()-t0:.0f} с)")
