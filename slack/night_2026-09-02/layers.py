"""Полное дерево обхода (строки по порядку, forward-checking) при малом n: узлов на слое, из них живых (достраиваемых), решений.
Калибровка: число решений должно совпасть с A000755."""
import math, itertools, sys, time
n = int(sys.argv[1])
A000755 = {8: 380, 9: 368, 10: 1135, 11: 1120, 12: 4348}
pairs = list(itertools.combinations(range(n), 2))

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

def check_A(forb, colc, d):
    for yy in range(d, n):
        if sum(1 for x in range(n) if colc[x] < 2 and (x,yy) not in forb) < 2: return False
    for x in range(n):
        need = 2 - colc[x]
        if need > 0 and sum(1 for yy in range(d, n) if (x,yy) not in forb) < need: return False
    return True

nodes = [0]*(n+1); live = [0]*(n+1)
def dfs(pts, forb, colc, d):
    """возвращает число решений в поддереве"""
    nodes[d] += 1
    if d == n:
        live[d] += 1; return 1
    cand = [x for x in range(n) if colc[x] < 2 and (x,d) not in forb]
    total = 0
    for i in range(len(cand)):
        for j in range(i+1, len(cand)):
            pts2, forb2, colc2 = list(pts), set(forb), list(colc)
            place(pts2, forb2, colc2, (cand[i], d))
            if (cand[j], d) in forb2: continue
            place(pts2, forb2, colc2, (cand[j], d))
            if not check_A(forb2, colc2, d+1): continue
            total += dfs(pts2, forb2, colc2, d+1)
    if total: live[d] += 1
    return total

t0 = time.time(); sols = dfs([], set(), [0]*n, 0)
print(f"n={n}: решений {sols} (A000755: {A000755.get(n,'?')}) — {'совпало' if sols == A000755.get(n) else 'РАСХОЖДЕНИЕ'}; {time.time()-t0:.0f} с")
print(f"{'строк заполнено':>16} {'точек':>6} {'узлов на слое':>14} {'из них живых':>13} {'мёртвых на одно решение':>24}")
for d in range(n+1):
    print(f"{d:>16} {2*d:>6} {nodes[d]:>14} {live[d]:>13} {(nodes[d]-live[d])/max(sols,1):>24.1f}")
