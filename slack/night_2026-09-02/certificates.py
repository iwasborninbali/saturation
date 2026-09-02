"""Линза duality_certificate: чем удостоверяется смерть ветки? n=12, случайные законные префиксы глубины d.
A = в каждой оставшейся строке >= 2 живых клетки и в каждом столбце хватает живых;  B = существует 2-паросочетание
(Холл, поток);  C = истина: есть ли достройка (полный перебор оставшихся строк)."""
import random, math, itertools, collections, time, sys
random.seed(3)
n = 12
pairs = list(itertools.combinations(range(n), 2))

def line_cells(p, q):
    (x1,y1),(x2,y2) = p, q
    dx, dy = x2-x1, y2-y1; g = math.gcd(abs(dx),abs(dy)); dx//=g; dy//=g
    out = []
    x, y = x1, y1
    while 0 <= x < n and 0 <= y < n: out.append((x,y)); x += dx; y += dy
    x, y = x1-dx, y1-dy
    while 0 <= x < n and 0 <= y < n: out.append((x,y)); x -= dx; y -= dy
    return out

def place(pts, forb, colc, p):
    """добавить точку p: затенить прямые через p и все прежние точки"""
    for q in pts:
        for c in line_cells(p, q): forb.add(c)
    pts.append(p); colc[p[0]] += 1

def sample_prefix(d):
    pts, forb, colc = [], set(), [0]*n
    for r in range(d):
        cands = [(c1,c2) for c1,c2 in pairs if colc[c1] < 2 and colc[c2] < 2 and (c1,r) not in forb and (c2,r) not in forb]
        if not cands: return None
        c1, c2 = random.choice(cands)
        place(pts, forb, colc, (c1,r)); place(pts, forb, colc, (c2,r))
    return pts, forb, colc

def alive(forb, colc, d):
    return {(x,y) for y in range(d, n) for x in range(n) if colc[x] < 2 and (x,y) not in forb}

def check_A(al, colc, d):
    rows = collections.Counter(y for _,y in al); cols = collections.Counter(x for x,_ in al)
    return all(rows[y] >= 2 for y in range(d, n)) and all(cols[x] >= 2 - colc[x] for x in range(n))

def check_B(al, colc, d):
    """поток: источник -> строка (2) -> столбец (1 на ребро) -> сток (2-colc)"""
    rows = list(range(d, n)); adj = {y: [x for x in range(n) if (x,y) in al] for y in rows}
    cap_col = {x: 2 - colc[x] for x in range(n)}
    flow_rc = collections.defaultdict(int)          # (y,x) -> 0/1
    col_used = collections.defaultdict(int)
    def augment(y, seen_cols):
        for x in adj[y]:
            if flow_rc[(y,x)] or x in seen_cols: continue
            seen_cols.add(x)
            if col_used[x] < cap_col[x]:
                flow_rc[(y,x)] = 1; col_used[x] += 1; return True
            # попытаться перекинуть чьё-то ребро из столбца x
            for y2 in rows:
                if y2 != y and flow_rc[(y2,x)]:
                    if augment(y2, seen_cols):
                        flow_rc[(y2,x)] = 0; flow_rc[(y,x)] = 1; return True
        return False
    total = 0
    for y in rows:
        for _ in range(2):
            if augment(y, set()): total += 1
            else: return False
    return total == 2*len(rows)

def check_C(pts, forb, colc, d):
    """есть ли достройка строк d..n-1"""
    if d == n: return True
    cand = [x for x in range(n) if colc[x] < 2 and (x,d) not in forb]
    for i in range(len(cand)):
        for j in range(i+1, len(cand)):
            p1, p2 = (cand[i], d), (cand[j], d)
            pts2, forb2, colc2 = list(pts), set(forb), list(colc)
            place(pts2, forb2, colc2, p1)
            if p2 in forb2: continue
            place(pts2, forb2, colc2, p2)
            if check_C(pts2, forb2, colc2, d+1): return True
    return False

M = int(sys.argv[1]) if len(sys.argv) > 1 else 600
print(f"n={n}, по {M} случайных законных префиксов на глубину; сертификаты смерти: A (счёт по строкам/столбцам), B (Холл/поток), C (истина)")
print(f"{'d':>3} {'мёртвых':>8} {'A ловит':>8} {'B ловит':>8} {'невидимых':>10} {'из прошедших B — мёртвых':>26}  время")
for d in (8, 9, 10):
    t0 = time.time(); dead = a = b = passB = passB_dead = 0; tries = 0
    for _ in range(M):
        s = None
        while s is None: s = sample_prefix(d); tries += 1
        pts, forb, colc = s
        al = alive(forb, colc, d)
        A = check_A(al, colc, d); B = A and check_B(al, colc, d)
        C = check_C(pts, forb, colc, d)
        assert not (C and not B), "истина жива, а сертификат говорит мертва — ошибка сертификата"
        if not C:
            dead += 1; a += (not A); b += (not B)
        if B: passB += 1; passB_dead += (not C)
    print(f"{d:>3} {dead/M:8.3f} {a/max(dead,1):8.3f} {b/max(dead,1):8.3f} {1-b/max(dead,1):10.3f} {passB_dead/max(passB,1):26.3f}  {time.time()-t0:5.0f} с")
