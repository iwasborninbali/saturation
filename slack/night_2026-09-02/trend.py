import numpy as np, collections, math
ALPHA = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz#$%&@?!()[]<>{}=*+|-/~^_:;,."
lut = np.zeros(256, dtype=np.int16)
for i,c in enumerate(ALPHA): lut[ord(c)] = i
data = collections.defaultdict(list)
for l in open('/Users/iwasborninbali/saturation/web/all_known_solutions'):
    l=l.strip()
    if l: data[(len(l)-1)//2].append(l[1:])

def kappa(n, a=1, b=1):
    e = data[n]
    cols = lut[np.frombuffer(''.join(e).encode(), dtype=np.uint8).reshape(len(e), 2*n)].astype(np.int32)
    rows = np.tile(np.repeat(np.arange(n, dtype=np.int32), 2), (len(e),1))
    f = b*cols - a*rows; lo=f.min(); L=int(f.max()-lo+1); S=len(e)
    occ = np.bincount((np.arange(S,dtype=np.int64)[:,None]*L+(f-lo)).ravel(), minlength=S*L).reshape(S,L)
    k2 = (occ==2).sum(1).astype(float)
    return k2.mean()/n, k2.std()/n/math.sqrt(S), S

print("kappa(n) на всём, что есть в базе (n>=100 решений):")
xs, ys, ws = [], [], []
for n in sorted(data):
    if len(data[n]) < 100 or n < 12: continue
    k, se, S = kappa(n)
    flag = "полное" if n <= 20 else "только симм."
    print(f"   n={n:3d} S={S:6d} {flag:12s} kappa={k:.5f} ± {se:.5f}")
    xs.append(n); ys.append(k); ws.append(1/max(se,1e-5)**2)
xs, ys, ws = np.array(xs,float), np.array(ys), np.array(ws)
A = np.vstack([np.ones_like(xs), 1/xs]).T
W = np.diag(ws)
coef = np.linalg.solve(A.T@W@A, A.T@W@ys)
print(f"\nвзвешенная подгонка kappa(n) = K + c/n :  K = {coef[0]:.5f}, c = {coef[1]:.4f}")
print(f"   sqrt(3)-1 = {3**0.5-1:.5f}   2-4/pi = {2-4/np.pi:.5f}   pi^2/12-0.09 = {np.pi**2/12-0.09:.5f}")
