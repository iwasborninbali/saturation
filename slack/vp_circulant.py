"""vp_circulant.py — analyse C_p of the vertical-pair model (input: output of slack/vp_lines p): the multiplier-circulant part
Cbar (means along mu = b/a in F_p^*), its l1/l2 norms and its spectrum via FFT over discrete logs, the fluctuation part Ctilde,
lambda_min of C, Cbar, Ctilde, m2 = tr C^2/(p-1).  usage: python3 slack/vp_circulant.py p file [--noeig]"""
import sys, numpy as np
p=int(sys.argv[1]); f=open(sys.argv[2]); E=float(f.readline().split()[1]); f.readline(); noeig='--noeig' in sys.argv
m=p-1; C=np.zeros((m,m))
for line in f:
    a,b,v=line.split(); a=int(a)-1;b=int(b)-1;v=float(v); C[a,b]+=v/2; C[b,a]+=v/2
# primitive root
def prim_root(p):
    fac=[]; n=p-1; d=2
    while d*d<=n:
        if n%d==0:
            fac.append(d)
            while n%d==0: n//=d
        d+=1
    if n>1: fac.append(n)
    for g in range(2,p):
        if all(pow(g,(p-1)//q,p)!=1 for q in fac): return g
g=prim_root(p); logt={}; x=1
for k in range(m): logt[x]=k; x=x*g%p
# w_bar[k] = mean over a of C[a, mu a] with mu = g^k
wbar=np.zeros(m); l1_raw=0.0
for k in range(m):
    mu=pow(g,k,p); s=0.0
    for a in range(1,p):
        b=mu*a%p; s+=C[a-1,b-1]
    wbar[k]=s/m
l2sq=float((wbar**2).sum()); l1=float(np.abs(wbar).sum())
what=np.fft.fft(wbar)      # eigenvalues of the circulant (as a function on Z/(p-1)); real if wbar symmetric under k -> -k
sym=np.max(np.abs(wbar-np.roll(wbar[::-1],1)))
ev=what.real; maxabs=float(np.max(np.abs(what))); lmin_bar=float(ev.min()); lmax_bar=float(ev.max())
m2=float((C**2).sum())/m
En=E/m
print(f"p={p}: E/(p-1)={En:.3f}  m2={m2:.3f}  ||wbar||_1={l1:.3f} ({l1/En:.3f} E/(p-1))  ||wbar||_2^2={l2sq:.4f} ({l2sq/m2:.4f} m2)  "
      f"max|what|={maxabs:.3f} ({maxabs/En:.3f})  lmin(Cbar)={lmin_bar:.3f} ({lmin_bar/En:.3f})  lmax(Cbar)={lmax_bar:.3f}  sym_err={sym:.1e}")
# top |wbar| multipliers
order=np.argsort(-np.abs(wbar))[:12]
print("  largest |wbar| (mu, wbar):", ", ".join(f"({pow(g,int(k),p)},{wbar[k]:+.4f})" for k in order))
if not noeig:
    Cbar=np.zeros((m,m))
    for k in range(m):
        mu=pow(g,k,p)
        for a in range(1,p): Cbar[a-1, mu*a%p-1]=wbar[k]
    Ct=C-Cbar
    lam=np.linalg.eigvalsh(C); lamt=np.linalg.eigvalsh(Ct)
    m2t=float((Ct**2).sum())/m
    print(f"  lambda_min(C)={lam[0]:.3f} ({lam[0]/En:.3f} E/(p-1); {lam[0]/np.sqrt(m2):.3f} sqrt m2)  lambda_max(C)={lam[-1]:.3f}  "
          f"||Ctilde||={max(-lamt[0],lamt[-1]):.3f} ({max(-lamt[0],lamt[-1])/np.sqrt(m2t):.3f} sqrt m2t; {max(-lamt[0],lamt[-1])/En:.3f} E/(p-1))  spectral bound (E+(p-1)lmin)/(p-1)={En+lam[0]:.3f}")
