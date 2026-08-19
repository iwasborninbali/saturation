import sys
from math import gcd
def collinear_free(P,n):
    P=list(P)
    for i in range(len(P)):
        for j in range(i+1,len(P)):
            ax,ay,az=P[i]; bx,by,bz=P[j]
            ux,uy,uz=bx-ax,by-ay,bz-az
            for k in range(j+1,len(P)):
                cx,cy,cz=P[k]; vx,vy,vz=cx-ax,cy-ay,cz-az
                if uy*vz-uz*vy==0 and uz*vx-ux*vz==0 and ux*vy-uy*vx==0: return False
    return True
def greedy_from(P,n):
    """take points one by one, keep if no 3 collinear with already kept"""
    keep=[]
    for p in P:
        ok=True
        for i in range(len(keep)):
            for j in range(i+1,len(keep)):
                ax,ay,az=keep[i]; bx,by,bz=keep[j]
                ux,uy,uz=bx-ax,by-ay,bz-az; vx,vy,vz=p[0]-ax,p[1]-ay,p[2]-az
                if uy*vz-uz*vy==0 and uz*vx-ux*vz==0 and ux*vy-uy*vx==0: ok=False;break
            if not ok: break
        if ok: keep.append(p)
    return keep
for n in (5,6,7,8):
    best=0; bestname=''
    fams={
      'z=x^2+y^2': lambda x,y:(x*x+y*y)%n,
      'z=x*y':     lambda x,y:(x*y)%n,
      'z=x^2+y':   lambda x,y:(x*x+y)%n,
      'z=x^2-y^2': lambda x,y:(x*x-y*y)%n,
      'z=x^3+y':   lambda x,y:(x**3+y)%n,
      'z=x^2+xy+y^2': lambda x,y:(x*x+x*y+y*y)%n,
    }
    for name,f in fams.items():
        P=[(x,y,f(x,y)) for x in range(n) for y in range(n)]
        k=greedy_from(P,n)
        if len(k)>best: best=len(k); bestname=name
    print(f"n={n}: лучшая алгебраическая поверхность даёт {best} точек ({bestname}); наш стохастический рекорд: {[0,0,0,0,0,40,64,72,90][n]}")
