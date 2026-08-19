"""alpha_cnf.py — CNF for "does a lawful subset of P_{-1} of size >= K exist?" (k=-1, HJSW box).
Line constraints: for every line with >=3 candidates, no 3 of its points are all chosen (C(k,3) clauses, k<=8).
Cardinality: at-least-K via a sequential counter (Sinz) on the negated literals (at-most-(N-K) false).
usage: python3 alpha_cnf.py p K out.cnf"""
import sys
from collections import defaultdict
from math import gcd
p=int(sys.argv[1]); K=int(sys.argv[2]); out=sys.argv[3]
h=(p-1)//2
pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
N=len(pts); idx={q:i+1 for i,q in enumerate(pts)}      # vars 1..N
lines=defaultdict(set)
for i in range(N):
    for j in range(i+1,N):
        (x1,y1),(x2,y2)=pts[i],pts[j]; dx,dy=x2-x1,y2-y1
        g=gcd(abs(dx),abs(dy)) or 1; dx,dy=dx//g,dy//g
        if dx<0 or (dx==0 and dy<0): dx,dy=-dx,-dy
        lines[(dx,dy,dy*x1-dx*y1)]|={i+1,j+1}
L=[sorted(m) for m in lines.values() if len(m)>=3]
cls=[]
from itertools import combinations
for mem in L:
    for a,b,c in combinations(mem,3): cls.append([-a,-b,-c])
# at-most-M false, M = N-K, over literals f_i = -x_i  (sequential counter)
M=N-K
nv=N
s=[[0]*(M+1) for _ in range(N+1)]
for i in range(1,N+1):
    for j in range(1,M+1):
        nv+=1; s[i][j]=nv
f=lambda i: -i                      # f_i true means x_i false
for i in range(1,N+1):
    cls.append([-f(i), s[i][1]])
    if i>1:
        for j in range(1,M+1):
            cls.append([-s[i-1][j], s[i][j]])
        for j in range(2,M+1):
            cls.append([-f(i), -s[i-1][j-1], s[i][j]])
        cls.append([-f(i), -s[i-1][M]])
with open(out,'w') as fh:
    fh.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls: fh.write(" ".join(map(str,c))+" 0\n")
print(f"p={p} K={K}: points={N} lines={len(L)} vars={nv} clauses={len(cls)} -> {out}")
