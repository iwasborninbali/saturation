"""km1_lines.py — for k = -1: sizes of the slope +1 integer lines x-y=d of P = (H(1) u H(-1)) ∩ G(p), counted from the class data
(no point enumeration): the H(1) points on x-y=d come from classes kappa with d_kappa ≡ d, the H(-1) points are the reflection
x -> p-x of the H(1) points on the antidiagonal x+y = p-d.  Prints, per p: number of +1 lines with 5,6,7,8 points, and the
'coincidence' counts.   usage: python3 slack/km1_lines.py pmax"""
import sys
from collections import Counter
def primes(n): return [q for q in range(3, n+1) if all(q % d for d in range(2, int(q**0.5)+1))]
def analyse(p):
    h = (p-1)//2
    X = lambda a: a if a <= h else a - p            # rep in [-h,h]
    Y = lambda b: b                                 # rep in [1,p-1]
    # H(1) points on slope+1 integer lines: class kappa=(a,1/a) base (X_a, Y_{1/a}); copies (r,s): x-y = d_kappa + (r-s)p
    diag = Counter(); anti = Counter()
    for a in range(1, p):
        b = pow(a, -1, p); x, y = X(a), Y(b)
        for r in (0, 1):
            for s in (0, 1):
                diag[x - y + (r - s) * p] += 1          # slope +1 line x-y = const
                anti[x + y + (r + s) * p] += 1          # slope -1 line x+y = const
    # H(-1) points: reflection x' = p - x of H(1) points; a H(1) point on x+y = e maps to x'-y = p - e
    sizes = Counter()
    for d, n1 in list(diag.items()):
        n2 = anti.get(p - d, 0)
        sizes[n1 + n2] += 1
    for e, n2 in anti.items():
        d = p - e
        if d not in diag: sizes[n2] += 1
    return sizes
pmax = int(sys.argv[1]) if len(sys.argv) > 1 else 200
print("p: #lines with 5,6,7,8 points (slope +1); 8-lines/p")
for p in primes(pmax):
    if p < 11: continue
    s = analyse(p)
    print(f"{p:4d}: 5:{s.get(5,0):3d} 6:{s.get(6,0):3d} 7:{s.get(7,0):3d} 8:{s.get(8,0):3d}   8/p={s.get(8,0)/p:.3f}  (>=5 total {sum(v for k,v in s.items() if k>=5)}, /p={sum(v for k,v in s.items() if k>=5)/p:.3f})")
