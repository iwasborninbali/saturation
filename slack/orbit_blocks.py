"""orbit_blocks.py — k=-1: decompose P_{-1} into (p-1)/2 'orbit blocks' (the 16 points of {kappa, nu kappa, R kappa, R' kappa} form a full
4x4 grid on rows {y ≡ 1/a} ∪ {y ≡ -1/a} and columns {x ≡ a} ∪ {x ≡ -a}); analyse a witness: points per block, and the block's 4x4 pattern.
usage: python3 slack/orbit_blocks.py p witnessfile"""
import sys
p=int(sys.argv[1]); h=(p-1)//2; f=sys.argv[2]
pts=set()
for l in open(f):
    l=l.strip()
    if not l or l.startswith('#'): continue
    x,y=map(int,l.split()[:2]); pts.add((x-h,y))          # actual coordinates X in [-h,3h+1]
def X(u): u%=p; return u if u<=h else u-p
blocks={}
seen=set()
for a in range(1,p):
    key=frozenset({a, p-a}) 
    if key in seen: continue
    seen.add(key)
    ia=pow(a,-1,p)
    cols=sorted({X(a), X(a)+p, X(p-a), X(p-a)+p}); rows=sorted({ia, ia+p, p-ia, 2*p-ia})
    grid=[[1 if (c,r) in pts else 0 for c in cols] for r in rows]
    n=sum(map(sum,grid))
    blocks[key]=(a, cols, rows, grid, n)
from collections import Counter
print(f"p={p}: {len(blocks)} orbit blocks, points {len(pts)}; per-block counts:", sorted(Counter(v[4] for v in blocks.values()).items()))
for key,(a,cols,rows,grid,n) in sorted(blocks.items(), key=lambda kv: kv[1][0]):
    rowsum=[sum(r) for r in grid]; colsum=[sum(grid[i][j] for i in range(4)) for j in range(4)]
    print(f"  a=±{a:2d} cols {cols} rows {rows}: n={n} rowsums {rowsum} colsums {colsum}  grid {' '.join(''.join(map(str,r)) for r in grid)}")
