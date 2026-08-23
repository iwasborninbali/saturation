# -*- coding: utf-8 -*-
# Проверка леммы о балансе и классификации малых дефектов (no3inline_defects)
# на ПОЛНОМ материале: все конфигурации A000755 при n<=11, независимым разбором.
import subprocess, sys
from collections import defaultdict
A755={5:32,6:50,7:132,8:380,9:368,10:1135,11:1120}
def enum_configs(n,cap):
    r=subprocess.run(['/tmp/hjfull/rows2d',str(n),str(cap)],capture_output=True,text=True,
                     env={'DUMP':'1','PATH':'/usr/bin:/bin'})
    cfgs=[]
    for line in r.stdout.splitlines():
        if ';' not in line: continue
        pts=frozenset(tuple(map(int,q.split(','))) for q in line.strip(';').split(';'))
        cfgs.append(pts)
    return cfgs, r.stdout.splitlines()[-1] if r.stdout else ''
def rot(pt,m): u,v=pt; return (v,m-u)
def sig(pt,m): u,v=pt; return (v,u)
def orbit(pt,gens,m):
    seen={pt}; front=[pt]
    while front:
        q=front.pop()
        for g in gens:
            r=g(q,m)
            if r not in seen: seen.add(r); front.append(r)
    return frozenset(seen)
def check(n):
    cfgs,tail=enum_configs(n,3000)
    ok_count=(len(cfgs)==A755[n])
    m=n-1
    sym=[C for C in cfgs if frozenset((m-u,m-v) for u,v in C)==C]
    res=dict(n=n,total=len(cfgs),ok_count=ok_count,sym=len(sym),bal_fail=0,cls_fail=0,par_fail=0,details=[])
    for C in sym:
        for Hname,gens in (('C4',[rot]),('V2',[sig, lambda q,mm:(mm-q[1],mm-q[0])])):
            # база: объединение H-орбит, целиком лежащих в C
            B=set()
            for q in C:
                o=orbit(q,gens,m)
                if o<=C: B|=o
            D=C-B
            # D должна быть объединением пар полуоборота, ни одна не H-орбита
            pairs=set()
            okD=True
            for q in D:
                q2=(m-q[0],m-q[1])
                if q2 not in D: okD=False
                pairs.add(frozenset((q,q2)))
            for pr in pairs:
                if orbit(next(iter(pr)),gens,m)==set(pr)|{p for p in pr}: pass
            # дуги и баланс
            out=defaultdict(int); inn=defaultdict(int)
            arcs=[]
            for pr in pairs:
                x,y=sorted(pr)[0]
                cx=frozenset((x,m-x)); cy=frozenset((y,m-y))
                out[cx]+=1; inn[cy]+=1; arcs.append((cx,cy,(x,y)))
            bal=all(out[k]==inn[k] for k in set(out)|set(inn))
            if not (okD and bal): res['bal_fail']+=1; res['details'].append((Hname,'баланс',len(pairs)))
            if Hname=='C4':
                if (len(pairs)%2)!=(n%2): res['par_fail']+=1
                # классификация малых дефектов
                k=len(pairs)
                if k==1:
                    cx,cy,(x,y)=arcs[0]
                    if not (cx==cy and (y==x or y==m-x) and n%2==1):
                        res['cls_fail']+=1; res['details'].append(('C4','|D|=1 не петля-на-диагонали',arcs))
                elif k==2 and n%2==0:
                    loops=[a for a in arcs if a[0]==a[1]]
                    if len(loops)==2:
                        (c1,_,(x1,y1)),(c2,_,(x2,y2))=loops
                        d1='main' if y1==x1 else 'anti'; d2='main' if y2==x2 else 'anti'
                        if c1==c2 or d1==d2:
                            res['cls_fail']+=1; res['details'].append(('C4','две петли не по правилу',arcs))
                    elif len(loops)==0:
                        # должен быть 2-цикл, являющийся dia2-орбитой
                        pl=[p for pr in pairs for p in pr]
                        q=pl[0]; o=orbit(q,[sig,lambda t,mm:(mm-t[1],mm-t[0])],m)
                        if o!=set(pl):
                            res['cls_fail']+=1; res['details'].append(('C4','2-цикл не dia2-орбита',arcs))
                    else:
                        res['cls_fail']+=1; res['details'].append(('C4','|D|=2: одна петля',arcs))
                elif k==3 and n%2==1:
                    loops=[a for a in arcs if a[0]==a[1]]
                    if len(loops)==0:
                        cls=set()
                        for a in arcs: cls.add(a[0]); cls.add(a[1])
                        # ориентированный 3-цикл: 3 класса, in=out=1 у каждого
                        if len(cls)!=3 or any(out[c]!=1 or inn[c]!=1 for c in cls):
                            res['cls_fail']+=1; res['details'].append(('C4','3 дуги не 3-цикл',arcs))
                    elif len(loops)==1:
                        rest=[p for pr in pairs for p in pr if frozenset(pr)!=frozenset()]
                        others=[pr for pr in pairs if not any(a[0]==a[1] and set(pr)=={a[2],(m-a[2][0],m-a[2][1])} for a in loops)]
                        pl=[p for pr in others for p in pr]
                        if len(pl)==4:
                            o=orbit(pl[0],[sig,lambda t,mm:(mm-t[1],mm-t[0])],m)
                            if o!=set(pl):
                                res['cls_fail']+=1; res['details'].append(('C4','петля+2цикл: 2цикл не dia2',arcs))
                    else:
                        res['cls_fail']+=1; res['details'].append(('C4','|D|=3: две петли',arcs))
    return res
print("n | всего(=A000755?) | rho2-симметричных | провалов баланса | классиф. | чётности",flush=True)
for n in (5,6,7,8,9,10,11):
    r=check(n)
    print(f"  n={r['n']:2d}: {r['total']:5d} ({'OK' if r['ok_count'] else 'НЕ СОШЛОСЬ!'})  sym={r['sym']:3d}  баланс_провалов={r['bal_fail']}  класс_провалов={r['cls_fail']}  чётн_провалов={r['par_fail']}",flush=True)
    for d in r['details'][:4]: print("     ",d,flush=True)
print("ГОТОВО",flush=True)
