"""Independent check of the W4 + family-(1,3) matching numbers (second solver): y = a x^3, box (0,0), p ≡ 2 mod 3."""
import sys
from collections import defaultdict
p=int(sys.argv[1]); a=int(sys.argv[2]) if len(sys.argv)>2 else 1
inv3=pow(3,-1,p)
def cube(x): return (a*x*x*x)%p
# roots of a t^3 - s t = c for slope s=+1 (c=ax^3-x) and s=-1 (c=ax^3+x)
roots={+1:defaultdict(list), -1:defaultdict(list)}
for t in range(p):
    roots[+1][(cube(t)-t)%p].append(t); roots[-1][(cube(t)+t)%p].append(t)
# W4: for each residue x, which of its 4 lifts (delta,eps) lie on a ±1 line with >=4 points (box (0,0): r_x = x, s_x = a x^3 mod p)
covered=defaultdict(set)  # x -> set of (delta,eps) covered
for s in (+1,-1):
    for c,R in roots[s].items():
        if len(R)<3: 
            # k<=2: lines have <=4 points only if k=2 and same class -> handle generally below
            pass
        # classes: slope +1: value Y-X = s_t - r_t + (eps-delta)p ; c' = the smaller of the two integers ≡ c in (-p, p)
        # slope -1: X+Y = r_t + s_t + (delta+eps)p ; two integers ≡ c in [0,2p)
        cls={}
        for t in R:
            r=t; sy=cube(t)
            if s==+1:
                d=sy-r  # in (-p,p); the two integers ≡ c mod p in (-p,p): c0 = c-p if c>0 else ...; class 0 iff d is the smaller
                # candidates: d and d±p; the smaller of the two in (-p,p) is c1 = ((c) % p) - p if that > -p ... simpler: class = 0 if d<0 else 1? no: c' = c-p (in (-p,0]) and c'+p = c (in [0,p)); d ≡ c; d in (-p,p) so d ∈ {c-p, c}; class 0 iff d == c-p (smaller)
                cls[t]= 0 if d==(c%p)-p else 1
            else:
                d=r+sy  # in [0,2p): the two integers ≡ c: c and c+p; class 0 iff d==c
                cls[t]= 0 if d==c%p else 1
        n0=sum(1 for t in R if cls[t]==0); n1=len(R)-n0; k=len(R)
        # line sizes: for slope +1: lines c'-p, c', c'+p, c'+2p carry n0, k+n0, k+n1, n1  (c' = smaller);
        # lifts of a class-0 root: (delta=eps) on line c' (size k+n0); (0,1) on c'+p (k+n1); (1,0) on c'-p (n0)
        # class-1 root: (delta=eps) on c'+p (k+n1); (0,1) on c'+2p (n1); (1,0) on c' (k+n0)
        # slope -1: lines c'', c''+p, c''+2p, c''+3p carry n0, k+n0, k+n1, n1; class-0 root: (0,0) on c'' (n0), mixed on c''+p (k+n0), (1,1) on c''+2p (k+n1)
        # class-1 root: (0,0) on c''+p (k+n0), mixed on c''+2p (k+n1), (1,1) on c''+3p (n1)
        for t in R:
            c0=cls[t]
            if s==+1:
                sizes={(0,0):(k+n0 if c0==0 else k+n1),(1,1):(k+n0 if c0==0 else k+n1),(0,1):(k+n1 if c0==0 else n1),(1,0):(n0 if c0==0 else k+n0)}
            else:
                sizes={(0,0):(n0 if c0==0 else k+n0),(1,1):(k+n1 if c0==0 else n1),(0,1):(k+n0 if c0==0 else k+n1),(1,0):(k+n0 if c0==0 else k+n1)}
            for lift,sz in sizes.items():
                if sz>=4: covered[t].add(lift)
S0=set()
for x in range(p):
    for lift in ((0,0),(0,1),(1,0),(1,1)):
        if lift not in covered[x]: S0.add((x,lift))
U=len(S0); L4=0
# count L4 lines: per residue class c with (k,n0): number of lines with >=4 among sizes n0,k+n0,k+n1,n1
for s in (+1,-1):
    for c,R in roots[s].items():
        k=len(R)
        if k==0: continue
        cls0=0
        for t in R:
            r=t; sy=cube(t)
            if s==+1: cls0+= 1 if (sy-r)==(c%p)-p else 0
            else: cls0+= 1 if (r+sy)==c%p else 0
        n0=cls0; n1=k-n0
        L4+= (n0>=4)+(k+n0>=4)+(k+n1>=4)+(n1>=4)
costW4=2*L4+U
print(f"p={p} a={a}: L4={L4} U={U} ({U/p:.4f} p) cost(W4)={costW4} = {costW4/(2*p):.4f} N  [note: 11/8=1.375]")
# family (1,3): x1 ≡ -4u/3, points x1, x1+u, x1+3u; v ≡ c1 u^3 + a u with c1 = (1-3+9)/3 = 7/3 (for f = a x^3: v = a*c1*u^3? recheck: f(x+t)-f(x) for f=ax^3: a(3x^2 t+3x t^2+t^3); with x=-4u/3: v = a*u*[3x^2+3xu+u^2] = a u [16u^2/3 -4u^2 + u^2] = a u^3 (16/3-3) = (7/3) a u^3 )
c1=(7*inv3)%p
good=[]; pts_lines=defaultdict(list)
for u in range(1,p):
    x1=(-4*u*inv3)%p; x2=(x1+u)%p; x3=(x1+3*u)%p
    v=(c1*a*pow(u,3,p))%p
    ys=[cube(x1),cube(x2),cube(x3)]
    for us in (u, u-p):
        for vs in (v, v-p):
            for dx in (0,1):
                for dy in (0,1):
                    X1=x1+dx*p; Y1=ys[0]+dy*p
                    X2=X1+us; Y2=Y1+vs; X3=X1+3*us; Y3=Y1+3*vs
                    if not (0<=X2<2*p and 0<=Y2<2*p and 0<=X3<2*p and 0<=Y3<2*p): continue
                    # residues check
                    assert X2%p==x2 and X3%p==x3 and Y2%p==ys[1] and Y3%p==ys[2]
                    lifts=[(x1,(dx,dy)),(x2,((X2//p),(Y2//p))),(x3,((X3//p),(Y3//p)))]
                    if all(l in S0 for l in lifts):
                        good.append(tuple(lifts))
                        for l in lifts: pts_lines[l].append(len(good)-1)
G=len(good); pairs=sum(len(v)*(len(v)-1)//2 for v in pts_lines.values())
print(f"  family (1,3): good lines={G} ({G/p:.4f} p), intersecting pairs={pairs} ({pairs/p:.4f} p), |good|-pairs={(G-pairs)/p:.4f} p  (threshold for 4/3: {(costW4-8*p/3)/p:.4f} p; asymptotic 1/12=0.0833)")
print(f"  => certified alpha <= {costW4-(G-pairs)} = {(costW4-(G-pairs))/(2*p):.4f} N")
