import math,subprocess,sys,os
from collections import defaultdict
from itertools import combinations
def build(p, ks):
    h=(p-1)//2; X=lambda a: a if a<=h else a-p; pts=[]
    for c in ks:
        c%=p
        for a in range(1,p):
            b=(c*pow(a,-1,p))%p
            for r in (0,1):
                for s in (0,1):
                    x,y=X(a)+r*p, b+s*p
                    if -h<=x<=(3*p-1)//2 and 0<=y<=2*p-1: pts.append((x,y,c))
    return pts
def rich(pts):
    L=defaultdict(set)
    for i in range(len(pts)):
        for j in range(i+1,len(pts)):
            x1,y1,_=pts[i]; x2,y2,_=pts[j]; dx,dy=x2-x1,y2-y1
            g=math.gcd(abs(dx),abs(dy)); dx//=g; dy//=g
            if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
            key=(dx,dy,dy*x1-dx*y1); L[key].add(i); L[key].add(j)
    return [sorted(v) for v in L.values() if len(v)>=3]
def cnf_atleast(n, K, nv):
    """sequential counter: at least K of x_1..x_n true  <=>  at most n-K of (not x_i)"""
    cl=[]; U=n-K
    if U<0: return None,nv
    # s[i][j] : among first i of (¬x), at least j true.  Sinz encoding for at-most-U
    s={}
    for i in range(1,n+1):
        for j in range(1,U+1):
            nv+=1; s[(i,j)]=nv
    lit=lambda i: -i   # ¬x_i
    if U==0:
        for i in range(1,n+1): cl.append([i])
        return cl,nv
    cl.append([-lit(1), s[(1,1)]])
    for j in range(2,U+1): cl.append([-s[(1,j)]])
    for i in range(2,n+1):
        cl.append([-lit(i), s[(i,1)]])
        cl.append([-s[(i-1,1)], s[(i,1)]])
        for j in range(2,U+1):
            cl.append([-lit(i), -s[(i-1,j-1)], s[(i,j)]])
            cl.append([-s[(i-1,j)], s[(i,j)]])
        cl.append([-lit(i), -s[(i-1,U)]])
    return cl,nv
def solve(n, base, K, blocking, tmp="/tmp/x.cnf"):
    card,nv=cnf_atleast(n,K,n)
    if card is None: return None
    cls=base+card+blocking
    with open(tmp,"w") as f:
        f.write(f"p cnf {nv} {len(cls)}\n")
        for c in cls: f.write(" ".join(map(str,c))+" 0\n")
    r=subprocess.run(["kissat","-q",tmp],capture_output=True,text=True)
    out=r.stdout
    if "s UNSATISFIABLE" in out: return None
    if "s SATISFIABLE" not in out: raise RuntimeError(out[:500]+r.stderr[:300])
    model=set()
    for line in out.splitlines():
        if line.startswith("v "):
            for t in line[2:].split():
                v=int(t)
                if 0<v<=n: model.add(v)
    return sorted(model)
def run(p,ks,label,count_max=True,cap=200000):
    pts=build(p,ks); n=len(pts); R=rich(pts)
    base=[]
    for L in R:
        for t in combinations(L,3): base.append([-(t[0]+1),-(t[1]+1),-(t[2]+1)])
    K=n
    while True:
        m=solve(n,base,K,[])
        if m is not None: break
        K-=1
    print(f"{label} p={p} |V|={n} rich={len(R)} alpha={K}  (3(p-1)={3*(p-1)}, 4(p-1)={4*(p-1)}, gain={K-3*(p-1)})",flush=True)
    if not count_max: return K,None
    blocking=[]; cnt=0
    while cnt<cap:
        m=solve(n,base,K,blocking)
        if m is None: break
        cnt+=1
        blocking.append([-v for v in m])
    print(f"    number of maximum sets = {cnt}{' (capped)' if cnt>=cap else ''}",flush=True)
    return K,cnt
if __name__=="__main__":
    run(11,(1,),"ONE  ")   # expect alpha=30, 9^s = 9 maxima (s=1)
    run(13,(1,),"ONE  ")   # s=2 -> 81
