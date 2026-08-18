"""lp1_anatomy.py — T2.17 (third solver): anatomy of the optimal LP(1) dual for k=-1 by residue-group types.
LP(1): max sum x_q s.t. sum_{q in l} x_q <= 2 for rows, columns and slope-±1 integer lines with >= 3 points of P_{-1}, 0<=x<=1.
Dual: weights y_l >= 0 on lines, z_q >= 0 on points, sum_{l ∋ q} y_l + z_q >= 1; value 2 sum y + sum z.  We symmetrise the dual under
R:(x,y)->(p-x,y) and R':(x,y)->(x,2p-y) (average of optimal duals is optimal), then attribute the value to points:
   cost(q) = (y_row + y_col + z_q)/2 + z_q/2 + sum_{±1 lines l ∋ q} 2 y_l/|l|      (sum_q cost = dual value; trivial cover: 1/2 per point)
and split cost(q) = cost+(q) + cost-(q) with cost±(q) = (y_row+y_col+2 z_q)/4 + sum_{slope ±1 lines ∋ q} 2y_l/|l|.  The economy of a slope-(+1)
residue group G (residue d = x-y mod p; its integer lines c ≡ d) is  econ(G) = |G|/4 - sum_{q in G} cost+(q); by R-symmetry the slope-(-1)
groups mirror them, and sum over all groups of both slopes = 4(p-1) - LP(1).  Types: sorted line-size profile of the group + class composition
(#kappa-type classes from a-1/a ≡ d, #lambda-type from b+1/b ≡ -d).   usage: python3 slack/lp1_anatomy.py p [p ...]"""
import sys, os
import numpy as np
from scipy.optimize import linprog
from collections import defaultdict, Counter
def run(p):
    h=(p-1)//2
    pts=[(x,y) for x in range(-h,3*h+2) for y in range(0,2*p) if (x*y)%p in (1,p-1)]
    idx={q:i for i,q in enumerate(pts)}; n=len(pts)
    lines=defaultdict(list)
    for (x,y) in pts:
        lines[('r',y)].append(idx[(x,y)]); lines[('c',x)].append(idx[(x,y)])
        lines[('d',x-y)].append(idx[(x,y)]); lines[('a',x+y)].append(idx[(x,y)])
    L=[(key,mem) for key,mem in lines.items() if len(mem)>=3]; lid={key:i for i,(key,mem) in enumerate(L)}
    A=np.zeros((len(L),n))
    for i,(key,mem) in enumerate(L):
        for j in mem: A[i,j]=1
    res=linprog(-np.ones(n),A_ub=A,b_ub=2*np.ones(len(L)),bounds=[(0,1)]*n,method='highs')
    val=-res.fun; y=np.maximum(-res.ineqlin.marginals,0); z=np.maximum(-res.upper.marginals,0)
    # symmetrise under R, R', RR'
    def img_pt(q,g):
        x,yy=q
        if g&1: x=p-x
        if g&2: yy=2*p-yy
        return (x,yy)
    def img_line(key,g):
        t,c=key
        if t=='r': return ('r', 2*p-c if g&2 else c)
        if t=='c': return ('c', p-c if g&1 else c)
        # d: x-y=c ; a: x+y=c
        if t=='d':
            if g==0: return ('d',c)
            if g==1: return ('a',p-c)        # (p-x)-y = c  -> x+y = p-c
            if g==2: return ('a',c+2*p)      # x-(2p-y)=c -> x+y = c+2p
            return ('d',-c-p)                # (p-x)-(2p-y)=c -> -x+y = c+p -> x-y = -c-p
        else:
            if g==0: return ('a',c)
            if g==1: return ('d',p-c)        # (p-x)+y=c -> x-y = p-c
            if g==2: return ('d',c-2*p)      # x+2p-y=c -> x-y=c-2p
            return ('a',3*p-c)               # (p-x)+(2p-y)=c -> x+y=3p-c
    ys=np.zeros(len(L)); zs=np.zeros(n)
    for g in range(4):
        for i,(key,mem) in enumerate(L):
            k2=img_line(key,g); assert k2 in lid, (key,g,k2)
            ys[lid[k2]]+=y[i]/4
        for i,q in enumerate(pts):
            zs[idx[img_pt(q,g)]]+=z[i]/4
    # check feasibility & value of symmetrised dual
    cover=A.T@ys+zs
    assert cover.min()>1-1e-6, cover.min()
    val_s=2*ys.sum()+zs.sum(); assert abs(val_s-val)<1e-6*val
    # per point costs
    yrow=np.zeros(n); ycol=np.zeros(n); plus=np.zeros(n); minus=np.zeros(n)
    for i,(key,mem) in enumerate(L):
        for j in mem:
            if key[0]=='r': yrow[j]+=ys[i]
            elif key[0]=='c': ycol[j]+=ys[i]
            elif key[0]=='d': plus[j]+=2*ys[i]/len(mem)
            else: minus[j]+=2*ys[i]/len(mem)
    costp=(yrow+ycol+2*zs)/4+plus; costm=(yrow+ycol+2*zs)/4+minus
    assert abs((costp+costm).sum()-val)<1e-6*val
    # groups of slope +1 by residue d=(x-y) mod p
    grp=defaultdict(list)
    for i,(x,yy) in enumerate(pts): grp[(x-yy)%p].append(i)
    types=defaultdict(list); linew=defaultdict(list)
    for d,mem in grp.items():
        # integer lines in the group and their sizes
        cs=Counter((pts[i][0]-pts[i][1]) for i in mem); prof=tuple(sorted(cs.values(),reverse=True))
        # class composition: kappa: a - 1/a ≡ d ; lambda: b + 1/b ≡ -d
        nk=sum(1 for a in range(1,p) if (a-pow(a,-1,p))%p==d); nl=sum(1 for b in range(1,p) if (b+pow(b,-1,p))%p==(-d)%p)
        econ=len(mem)/4-costp[mem].sum()
        t=(prof,nk,nl)
        types[t].append(econ)
        for c,sz in cs.items():
            key=('d',c)
            w=ys[lid[key]] if key in lid else 0.0
            linew[(t,sz)].append(w)
    tot_econ=2*sum(sum(v) for v in types.values())      # both slopes by symmetry
    print(f"p={p}: LP(1)={val:.3f} = {val/(p-1):.4f}(p-1); saving 4(p-1)-LP(1) = {4*(p-1)-val:.3f}; attributed saving (both slopes) = {tot_econ:.3f}; z-mass {zs.sum():.3f}; groups(+1) = {len(grp)}")
    print("   type (line-size profile; #kappa,#lambda): count | econ mean [min,max] | mean dual weight of the group's lines by size")
    rows=[]
    for t,v in sorted(types.items(), key=lambda kv:-len(kv[1])*abs(np.mean(kv[1]))):
        prof,nk,nl=t
        w={sz:np.mean(linew[(t,sz)]) for sz in set(prof)}
        rows.append((t,len(v),np.mean(v),min(v),max(v),w))
        print(f"   {str(prof):22s} k{nk} l{nl}: {len(v):4d} | {np.mean(v):7.4f} [{min(v):7.4f},{max(v):7.4f}] | " + " ".join(f"{sz}:{w[sz]:.3f}" for sz in sorted(w,reverse=True)))
    # rows/columns/points weight summary
    ry=[ys[i] for i,(k,m) in enumerate(L) if k[0]=='r']; cy=[ys[i] for i,(k,m) in enumerate(L) if k[0]=='c']
    print(f"   rows: mean weight {np.mean(ry):.4f} (min {min(ry):.3f} max {max(ry):.3f}); cols: mean {np.mean(cy):.4f}; points with z>0: {int((zs>1e-9).sum())}, mean z {zs.mean():.4f}")
    return rows
if __name__=="__main__":
    for a in sys.argv[1:]: run(int(a))
