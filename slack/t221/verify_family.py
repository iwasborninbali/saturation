"""verify_family.py — INDEPENDENT enumeration of one 3-cycle-family subclass, to validate the solver's sym=9/10 modes.
Family (odd n): S = (union of base-group orbits) + the given half-turn pairs; |S| = 2n; two points per row and per column;
no three collinear.  base = C4 (sym 9) or the 'both swaps' group V2/dia2 (sym 10).
usage: python3 verify_family.py n base PAIRS   e.g.  python3 verify_family.py 13 9 "0,1;11,2;10,0" """
import sys
from itertools import combinations

def run(n, base, pairspec):
    m=n-1
    def rot90(c): x,y=divmod(c,n); return y*n+(m-x)
    def half(c):  x,y=divmod(c,n); return (m-x)*n+(m-y)
    def tr(c):    x,y=divmod(c,n); return y*n+x
    def atr(c):   x,y=divmod(c,n); return (m-y)*n+(m-x)
    if base==9:   gen=[rot90]
    elif base==10: gen=[tr,atr]
    else: raise SystemExit("base must be 9 or 10")
    def orbit(c):
        o={c}
        while True:
            new={g(z) for z in o for g in gen}|o
            if new==o: return frozenset(o)
            o=new
    pairs=[]
    for tok in pairspec.split(';'):
        x,y=map(int,tok.split(',')); c=x*n+y; pairs.append((c,half(c)))
    pcells={c for pr in pairs for c in pr}
    if len(pcells)!=2*len(pairs): return None,"degenerate pairs"
    orbs=set()
    for c in range(n*n):
        if c in pcells: continue
        o=orbit(c)
        if o & pcells: continue
        orbs.add(o)
    orbs=[sorted(o) for o in orbs]
    need=2*n-len(pcells)
    orbs=[o for o in orbs if len(o)<=need]
    rowc=[0]*n; colc=[0]*n
    for c in pcells: rowc[c//n]+=1; colc[c%n]+=1
    if max(rowc)>2 or max(colc)>2: return [],"pairs already violate row/col"
    sols=[]; base_pts=sorted(pcells)
    def collinear_ok(P):
        L=len(P)
        for i in range(L):
            x1,y1=divmod(P[i],n)
            for j in range(i+1,L):
                x2,y2=divmod(P[j],n); dx,dy=x2-x1,y2-y1
                for k in range(j+1,L):
                    x3,y3=divmod(P[k],n)
                    if dx*(y3-y1)==dy*(x3-x1): return False
        return True
    def rec(i, chosen, cnt, rc, cc):
        if cnt==need:
            P=sorted(base_pts+[c for o in chosen for c in o])
            if all(v==2 for v in rc) and all(v==2 for v in cc) and collinear_ok(P): sols.append(tuple(P))
            return
        if i>=len(orbs) or cnt>need: return
        # bound: remaining orbits cannot fill
        o=orbs[i]
        if cnt+len(o)<=need:
            ok=True; rc2=rc[:]; cc2=cc[:]
            for c in o:
                rc2[c//n]+=1; cc2[c%n]+=1
                if rc2[c//n]>2 or cc2[c%n]>2: ok=False; break
            if ok: rec(i+1, chosen+[o], cnt+len(o), rc2, cc2)
        rec(i+1, chosen, cnt, rc, cc)
    rec(0, [], 0, rowc, colc)
    return sols, f"orbits available={len(orbs)} need={need} points"

if __name__=='__main__':
    n=int(sys.argv[1]); base=int(sys.argv[2]); spec=sys.argv[3]
    s,info=run(n,base,spec)
    print(f"n={n} base={base} PAIRS={spec}: {info}; INDEPENDENT solutions = {len(s) if s is not None else 'n/a'}")
    for t in (s or [])[:3]: print("   sol", " ".join(map(str,t)))
