"""Перепись rct4-решений (нечётные n) из базы: структура относительно центра и диагоналей."""
import numpy as np, collections
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
IDX = {c:i for i,c in enumerate(ALPHA)}
sols = collections.defaultdict(list)
for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions'):
    l = l.strip()
    if l and l[0] == 'c':
        n = (len(l)-1)//2
        pts = [(IDX[l[1+2*r+k]], r) for r in range(n) for k in range(2)]   # (x=col, y=row)
        sols[n].append(pts)
total = sum(len(v) for v in sols.values())
print("rct4 в базе по n:", {n: len(v) for n, v in sorted(sols.items())}, f"всего {total}")

b_hist = collections.Counter(); which = collections.Counter(); d_rel = []; d_abs = collections.defaultdict(list)
center_occ = 0; corner_occ = 0; border_x = []; ratio_map = np.zeros((11,11)); expect_map = np.zeros((11,11))
per_n_rows = {}
for n, L in sols.items():
    m = n-1; c = m//2
    for pts in L:
        S = set(pts)
        main = [(x,y) for x,y in pts if x == y]; anti = [(x,y) for x,y in pts if x + y == m]
        b_hist[(len(main), len(anti))] += 1
        diag = main if main else anti; which['main' if main else 'anti'] += 1
        # смещение пары от центра вдоль диагонали
        ds = sorted(abs(x - c) for x,_ in diag)
        if len(diag) == 2 and ds[0] == ds[1]:
            d_rel.append(ds[0]/n); d_abs[n].append(ds[0])
        center_occ += ((c,c) in S)
        corner_occ += sum(((x,y) in S) for x in (0,m) for y in (0,m))
        border_x += [min(x, m-x)/n for x,y in pts if y == 0]
        for x,y in pts:
            ratio_map[min(10, int(11*y/n)), min(10, int(11*x/n))] += 1
        # ожидание при равномерной плотности 2/n на клетку по тем же корзинам
        for y in range(n):
            for x in range(n):
                expect_map[min(10, int(11*y/n)), min(10, int(11*x/n))] += 2/n
print(f"\n(точек на главной, на антидиагонали): {dict(b_hist)}   -> на какой диагонали пара: {dict(which)}")
print(f"центр занят: {center_occ}/{total};  углы заняты: {corner_occ}/{4*total}")
d_rel = np.array(d_rel)
print(f"\nсмещение полуоборотной пары от центра, d/n: среднее {d_rel.mean():.3f}, σ {d_rel.std():.3f}, min {d_rel.min():.3f}, max {d_rel.max():.3f}")
h, edges = np.histogram(d_rel, bins=[0,0.05,0.1,0.15,0.2,0.25,0.3,0.35,0.4,0.45,0.5])
for i in range(len(h)): print(f"   d/n in [{edges[i]:.2f},{edges[i+1]:.2f}): {h[i]:5d}  {'#'*int(60*h[i]/h.max())}")
print("\nпо n (только n>=59): смещения d самих одиночных решений:")
for n in sorted(d_abs):
    if n >= 59: print(f"   n={n}: d = {sorted(d_abs[n])}  (d/n = {[round(d/n,3) for d in sorted(d_abs[n])]})")
bx = np.array(border_x)
print(f"\nточки в крайней строке: расстояние до ближайшего края, /n: среднее {bx.mean():.3f}, доля < 0.1n: {(bx<0.1).mean():.3f}, доля > 0.4n: {(bx>0.4).mean():.3f}")
print("\nплотность заполнения относительно равномерной (11x11 корзин по относительному положению, все rct4 вместе):")
R = ratio_map/expect_map
for i in range(11): print("   " + " ".join(f"{R[i,j]:4.2f}" for j in range(11)))
