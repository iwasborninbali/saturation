"""Monte-Carlo of the local model for the neighbour types of a (7,5,3,1)-orbit (k=-1).
Positions u_i in (-1/2,1/2) uniform, with the linear relations (mod 1) forced by a-1/a=b+1/b, a''-1/a''=a+1/a, b''+1/b''=b-1/b:
 u1=X(a)/p, u2=X(1/a)/p, u3=X(b)/p, u4=X(1/b)/p, u5=X(a'')/p, u6=X(1/a'')/p, u7=X(b'')/p, u8=X(1/b'')/p;
 u1-u2-u3-u4 in Z, u5-u6-u1-u2 in Z, u7+u8-u3+u4 in Z; free coords u1,u2,u3,u5,u7 uniform; u4,u6,u8 = lifts.
Sharing: sigma-pair (t,-1/t) of a +1 group shared iff sgn X(t) != sgn X(1/t); tau-pair (t,1/t) shared iff sgn X(t) = sgn X(1/t).
G_d: sigma=(a,-1/a): S1 = sgn u1 != sgn u2 ; tau=(b,1/b): T1 = sgn u3 == sgn u4.  7-type iff S1 xor T1.
e+ neighbour (exists w.p. 1/2): +1 group with sigma''=(a'',-1/a''): S2 = sgn u5 != sgn u6; tau=(a,1/a): T2 = sgn u1 == sgn u2 (= not S1).
e- neighbour (exists w.p. 1/2): sigma=(b,-1/b): S3 = sgn u3 != sgn u4 (= not T1); tau''=(b'',1/b''): T3 = sgn u7 == sgn u8.
used iff (exists and (S or T)); 8-type iff both shared."""
import random, sys
def lift(x):
    x = x - round(x)  # into [-1/2,1/2]
    return x
N=int(sys.argv[1]) if len(sys.argv)>1 else 2000000
random.seed(1)
cnt={'n7':0,'clean':0,'dirtyB':0,'dirty7':0,'both':0,'shared_used':0,'unshared_used':0,'unshared_8':0}
for _ in range(N):
    u1,u2,u3,u5,u7=[random.uniform(-0.5,0.5) for _ in range(5)]
    u4=lift(u1-u2-u3); u6=lift(u5-u1-u2); u8=lift(-u7+u3-u4)
    S1=(u1>0)!=(u2>0); T1=(u3>0)==(u4>0)
    if S1==T1: continue
    cnt['n7']+=1
    ex_p=random.random()<0.5; ex_m=random.random()<0.5
    S2=(u5>0)!=(u6>0); T2=not S1
    S3=not T1; T3=(u7>0)==(u8>0)
    up = ex_p and (S2 or T2); um = ex_m and (S3 or T3)
    t8p = up and S2 and T2; t8m = um and S3 and T3
    if S1: cnt['shared_used']+=up; cnt['unshared_used']+=um; cnt['unshared_8']+=t8m
    else:  cnt['shared_used']+=um; cnt['unshared_used']+=up; cnt['unshared_8']+=t8p
    meetsB = t8p or t8m; meets7 = (up and not t8p) or (um and not t8m)
    if not up and not um: cnt['clean']+=1
    elif meetsB and meets7: cnt['both']+=1
    elif meetsB: cnt['dirtyB']+=1
    else: cnt['dirty7']+=1
n=cnt['n7']
print({k:round(v/n,4) for k,v in cnt.items() if k!='n7'}, 'n7=',n, ' model: clean 7/16=%.4f dirtyB 21/64=%.4f dirty7 12/64=%.4f both 3/64=%.4f'%(7/16,21/64,12/64,3/64))
