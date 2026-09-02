"""Сила отсечения по «константе»: на n=12 (все решения известны) сравниваем префиксы решений (живые ветки)
со случайными законными префиксами той же глубины (то, что видит DFS). Статистики: k2 = дважды занятые диагонали,
short = пары в коротких направлениях (max(|a|,|b|)<=2, без строк). Если распределения совпадают — отсекать нечего."""
import numpy as np, random, math, collections, itertools
random.seed(20260902)
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c:i for i,c in enumerate(ALPHA)}
n = 12
orbits = [l.strip()[1:] for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions') if len(l.strip()) == 2*n+1]
def d4(pts):
    out = set()
    for x_, y_ in [(lambda x,y:(x,y)), (lambda x,y:(n-1-x,y)), (lambda x,y:(x,n-1-y)), (lambda x,y:(n-1-x,n-1-y)),
                   (lambda x,y:(y,x)), (lambda x,y:(n-1-y,x)), (lambda x,y:(y,n-1-x)), (lambda x,y:(n-1-y,n-1-x))] and []: pass
    T = [lambda x,y:(x,y), lambda x,y:(n-1-x,y), lambda x,y:(x,n-1-y), lambda x,y:(n-1-x,n-1-y),
         lambda x,y:(y,x), lambda x,y:(n-1-y,x), lambda x,y:(y,n-1-x), lambda x,y:(n-1-y,n-1-x)]
    for t in T: out.add(frozenset(t(x,y) for x,y in pts))
    return out
sols = set()
for b in orbits:
    pts = [(IDX[b[2*r+k]], r) for r in range(n) for k in range(2)]   # (x=col, y=row)
    sols |= d4(pts)
sols = [sorted(s, key=lambda p:(p[1],p[0])) for s in sols]
print(f"n={n}: орбит {len(orbits)}, всех решений {len(sols)}")

def stats(pts):
    k2 = sum(1 for v in collections.Counter(x-y for x,y in pts).values() if v == 2)
    short = 0
    for (x1,y1),(x2,y2) in itertools.combinations(pts, 2):
        dx, dy = x2-x1, y2-y1
        if dy == 0: continue
        g = math.gcd(abs(dx), abs(dy)); a, b = abs(dx)//g, abs(dy)//g
        if max(a,b) <= 2: short += 1
    return k2, short

def line_cells(p, q):
    (x1,y1),(x2,y2) = p, q
    dx, dy = x2-x1, y2-y1; g = math.gcd(abs(dx),abs(dy)); dx//=g; dy//=g
    cells = []
    x, y = x1, y1
    while 0 <= x < n and 0 <= y < n: cells.append((x,y)); x += dx; y += dy
    x, y = x1-dx, y1-dy
    while 0 <= x < n and 0 <= y < n: cells.append((x,y)); x -= dx; y -= dy
    return cells

pairs = list(itertools.combinations(range(n), 2))
def random_lawful_prefix(d):
    """случайная законная расстановка по 2 в строках 0..d-1 (<=2 в столбце, нет 3 на прямой); None если тупик"""
    forb = [[False]*n for _ in range(n)]; colc = [0]*n; pts = []
    for r in range(d):
        cands = [(c1,c2) for c1,c2 in pairs if colc[c1] < 2 and colc[c2] < 2 and not forb[r][c1] and not forb[r][c2]]
        if not cands: return None
        c1, c2 = random.choice(cands)
        for c in (c1,c2):
            p = (c, r)
            for q in pts:
                for (x,y) in line_cells(p, q): forb[y][x] = True
            pts.append(p); colc[c] += 1
    return pts

def auc(live, dead):
    """P(live < dead) + 0.5 P(равны)"""
    lv = np.array(live); dd = np.array(dead)
    allv = np.concatenate([lv, dd]); ranks = np.argsort(np.argsort(allv, kind='stable')).astype(float)
    # усреднённые ранги для ничьих
    order = np.argsort(allv, kind='stable'); sv = allv[order]; r = np.empty(len(allv))
    i = 0
    while i < len(sv):
        j = i
        while j+1 < len(sv) and sv[j+1] == sv[i]: j += 1
        r[order[i:j+1]] = (i+j)/2 + 1; i = j+1
    R = r[:len(lv)].sum()
    return (R - len(lv)*(len(lv)+1)/2)/(len(lv)*len(dd))

M = 6000
print(f"\nглубина d (строк из {n}) | живых префиксов | k2: живые / случайные (среднее±σ) | AUC | short: живые / случайные | AUC")
print(" AUC=0.5 — статистика не различает живые и мёртвые ветки; отсечение при потере 5% решений даёт yield, указанный справа")
for d in (3, 4, 6, 8, 10):
    live_pref = {tuple(p for p in s if p[1] < d) for s in sols}
    live = [stats(list(p)) for p in live_pref]
    dead = []; tries = 0
    while len(dead) < M:
        tries += 1
        p = random_lawful_prefix(d)
        if p is not None: dead.append(stats(p))
    lk, ls = np.array([a for a,_ in live]), np.array([b for _,b in live])
    dk, ds = np.array([a for a,_ in dead]), np.array([b for _,b in dead])
    def yield_at(lv, dv, loss=0.05):
        # правило «отсечь, если статистика > t» и «если < t»; берём лучшее
        best = 0.0
        for sign in (1,-1):
            t = np.quantile(sign*lv, 1-loss)
            y = (sign*dv > t).mean(); best = max(best, y)
        return best
    print(f" d={d:2d} | {len(live_pref):6d} | {lk.mean():5.2f}±{lk.std():4.2f} / {dk.mean():5.2f}±{dk.std():4.2f} | {auc(lk,dk):.3f} | "
          f"{ls.mean():5.2f}±{ls.std():4.2f} / {ds.mean():5.2f}±{ds.std():4.2f} | {auc(ls,ds):.3f} | yield@5%: k2 {yield_at(lk,dk):.3f}, short {yield_at(ls,ds):.3f}  (тупиков при сэмплировании: {tries-M})")
