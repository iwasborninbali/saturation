from itertools import combinations
def maxsf(p):
    best=0;wit=None
    els=list(range(1,p))
    for k in range(p-1,0,-1):
        found=False
        for S in combinations(els,k):
            Ss=set(S)
            if all(((a+b)%p) not in Ss for a in S for b in S):
                return k,S
        if found: break
    return 0,None
for p in [5,7,11,13,17,19,23]:
    k,S=maxsf(p)
    print(p, k, "floor((p+1)/3)=",(p+1)//3, "ceil((p-1)/3)=",-((-(p-1))//3), S)
