# -*- coding: utf-8 -*-
# Полная независимая проверка hjsw_window: написано с нуля, кода статьи не открывал.
# ЕДИНИЦА ИСТИНЫ: определение гиперболы и окна из аннотации; всё остальное выводится здесь.
import sys, itertools
from math import gcd

def is_qr(a,p): return pow(a%p,(p-1)//2,p)==1
def points(p,c,x0=None,y0=None):
    # окно HJSW по умолчанию: x in [-(p-1)/2,(3p-1)/2], y in [0,2p-1]
    if x0 is None: xs=range(-(p-1)//2,(3*p-1)//2+1)
    else: xs=range(x0,x0+2*p)
    if y0 is None: ys=range(0,2*p)
    else: ys=range(y0,y0+2*p)
    return [(x,y) for x in xs for y in ys if x%p and (x*y-c)%p==0]

def rich_lines(pts):
    # все прямые с >=3 точками; ключ прямой: нормализованный (a,b,c): ax+by=c
    from collections import defaultdict
    idx={q:i for i,q in enumerate(pts)}
    lines=defaultdict(set)
    n=len(pts)
    for i in range(n):
        x1,y1=pts[i]
        for j in range(i+1,n):
            x2,y2=pts[j]
            a=y2-y1; b=x1-x2; g=gcd(abs(a),abs(b))
            a//=g; b//=g
            if a<0 or (a==0 and b<0): a,b=-a,-b
            cc=a*x1+b*y1
            lines[(a,b,cc)].update((i,j))
    return {k:frozenset(v) for k,v in lines.items() if len(v)>=3}

def orbit_of(cl,p):
    a,b=cl
    return frozenset({(a,b),((-b)%p,(-a)%p),(b,a),((-a)%p,(-b)%p)})

def alpha_enum(masks_lines, npts, want_sets=False, atmost=2):
    # полный перебор по подмножествам: npts<=16 всегда (одна орбита)
    best=0; cnt=0; best_sets=[]; lawful_by_size={}
    for S in range(1<<npts):
        ok=True
        for L in masks_lines:
            if bin(S&L).count('1')>atmost: ok=False; break
        if not ok: continue
        k=bin(S).count('1')
        if want_sets: lawful_by_size.setdefault(k,[]).append(S)
        if k>best: best,cnt,best_sets=k,1,[S]
        elif k==best: cnt+=1; best_sets.append(S)
    return best,cnt,best_sets,lawful_by_size

def run_single(p,c,do_lp,do_stab):
    out=[]
    s=(1 if is_qr(c,p) else 0)+(1 if is_qr(-c,p) else 0)
    pts=points(p,c); N=len(pts)
    RL=rich_lines(pts)
    # 1. наклоны и количества
    slopes_ok=all((a,b) in ((1,-1),(1,1)) for (a,b,_) in RL)   # x-y=c (наклон +1): a=1,b=-1; x+y=c: a=1,b=1
    n4=sum(1 for v in RL.values() if len(v)==4)
    n3=sum(1 for v in RL.values() if len(v)==3)
    exp_lines=3*(p-1)//2 - s
    ok_counts=(len(RL)==exp_lines and n4==(p-1-2*s)//2 and n3==p-1 and max((len(v) for v in RL.values()),default=0)<=4)
    # 2. орбиты и принадлежность прямых
    cls={}
    for i,(x,y) in enumerate(pts): cls.setdefault((x%p,y%p),[]).append(i)
    orb_map={}
    for cl in cls: orb_map[cl]=orbit_of(cl,p)
    orbits={}
    for cl,o in orb_map.items(): orbits.setdefault(o,set()).update(cls[cl])
    lines_in_orbit=True
    for L in RL.values():
        os={next(o for o,mem in orbits.items() if i in mem) for i in L}
        if len(os)!=1: lines_in_orbit=False
    # 3. per-orbit alpha/count/stability/no4
    tot_a=0; tot_cnt=1; orb_ok=True; stab_ok=True; no4_tot=0
    for o,mem in orbits.items():
        mem=sorted(mem); loc={g:i for i,g in enumerate(mem)}
        lm=[sum(1<<loc[i] for i in L) for L in RL.values() if set(L)<=set(mem)]
        a,cntm,best_sets,lbs=alpha_enum(lm,len(mem),want_sets=do_stab)
        no4,_ ,_,_=alpha_enum(lm,len(mem),atmost=3)
        no4_tot+=no4
        generic=(len(o)==4)
        exp=(12,1) if generic else (6,9)
        if len(mem) not in (16,8) or (a,cntm)!=exp: orb_ok=False
        tot_a+=a; tot_cnt*=cntm
        if do_stab:
            for d in (1,2,3):
                for S in lbs.get(a-d,[]):
                    m=min(bin(S&~M).count('1') for M in best_sets)
                    lim=d if generic else 0
                    if m>lim: stab_ok=False
    ok_alpha=(tot_a==3*(p-1)); ok_cnt=(tot_cnt==9**s)
    ok_no4=(no4_tot==7*(p-1)//2+s)
    ok_uni=((tot_cnt==1)==(s==0))and((s==0)==((p%4==1)and not is_qr(c,p)))
    lp_ok=None
    if do_lp:
        from scipy.optimize import linprog
        A=[[1 if i in L else 0 for i in range(N)] for L in RL.values()]
        r=linprog([-1.0]*N,A_ub=A,b_ub=[2.0]*len(A),bounds=[(0,1)]*N,method='highs')
        lp_ok=abs(-r.fun-3*(p-1))<1e-6
    return dict(p=p,c=c,s=s,N=N,slopes=slopes_ok,counts=ok_counts,inorb=lines_in_orbit,
                orb=orb_ok,alpha=ok_alpha,cnt=ok_cnt,no4=ok_no4,uni=ok_uni,stab=(stab_ok if do_stab else None),lp=lp_ok)

def run_boxes(p,c):
    s=(1 if is_qr(c,p) else 0)+(1 if is_qr(-c,p) else 0)
    bad=[]; hjsw_attained=False
    for x0 in range(p):
        for y0 in range(p):
            pts=points(p,c,x0,y0); RL=rich_lines(pts)
            if not all((a,b) in ((1,-1),(1,1)) for (a,b,_) in RL): bad.append((x0,y0,'наклон')); continue
            cls={}
            for i,(x,y) in enumerate(pts): cls.setdefault((x%p,y%p),[]).append(i)
            orbits={}
            for cl,ii in cls.items(): orbits.setdefault(orbit_of(cl,p),set()).update(ii)
            n2=n1=n0=0; tot=0; okbox=True
            for o,mem in orbits.items():
                mem=sorted(mem); loc={g:i for i,g in enumerate(mem)}
                lms=[(ab,sum(1<<loc[i] for i in L)) for (ab0,ab1,_),L in RL.items() if set(L)<=set(mem) for ab in [(ab0,ab1)]]
                if any(not set(L)<=set(mem) and set(L)&set(mem) for L in RL.values()): okbox=False
                lm=[m for _,m in lms]
                a,cnt,_,_=alpha_enum(lm,len(mem))
                tot+=a
                if len(o)==2:
                    if a!=6: okbox=False
                    continue
                d4p=sum(1 for (ab,m) in lms if ab==(1,-1) and bin(m).count('1')==4)
                d4m=sum(1 for (ab,m) in lms if ab==(1,1)  and bin(m).count('1')==4)
                e,f=2-d4p,2-d4m
                if e+f not in (0,2): okbox=False
                if e+f==0:
                    n0+=1; okbox &= (a==8)
                elif (e,f)==(1,1):
                    n1+=1; okbox &= (a==10)
                else:
                    n2+=1; okbox &= (a==12)
            formula=12*n2+10*n1+8*n0+6*s
            if tot!=formula or tot>3*(p-1) or not okbox: bad.append((x0,y0,f'tot={tot},form={formula}'))
            if x0==(p+1)//2%p and y0==0 and tot==3*(p-1): hjsw_attained=True
    return bad,hjsw_attained

PR=[5,7,11,13,17,19,23,29,31]
print("=== ОДИНОЧНАЯ ГИПЕРБОЛА, ОКНО HJSW: все c для p<=31 ===",flush=True)
fails=0; done=0
for p in PR:
    for c in range(1,p):
        r=run_single(p,c,do_lp=(p<=13 and c<=3),do_stab=(p<=13))
        done+=1
        bad=[k for k in ('slopes','counts','inorb','orb','alpha','cnt','no4','uni','stab','lp') if r[k] is False]
        if bad: fails+=1; print(f"  ПРОВАЛ p={p} c={c}: {bad}",flush=True)
    print(f"  p={p}: все c=1..{p-1} пройдены, накопл. инстансов {done}, провалов {fails}",flush=True)
print(f"ИТОГ одиночной: {done} инстансов, провалов {fails}",flush=True)
print("=== ВСЕ ОКНА (x0,y0) in [0,p)^2: p in 5,7,11,13; c in 1..3 ===",flush=True)
for p in (5,7,11,13):
    for c in (1,2,3):
        bad,att=run_boxes(p,c)
        print(f"  p={p} c={c}: позиций {p*p}, нарушений {len(bad)}{' — '+str(bad[:3]) if bad else ''}, HJSW достигает 3(p-1): {att}",flush=True)
print("ГОТОВО",flush=True)
