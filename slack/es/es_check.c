/* es_check.c — Erdos-Straus: for n>=2 find positive x,y,z with 4/n = 1/x + 1/y + 1/z.
 * Standard search: x runs over (n/4, 3n/4]; then 4/n - 1/x = (4x-n)/(n x) =: a/b must be 1/y + 1/z,
 * i.e. y runs over (b/a, 2b/a] and (a y - b) must divide b y.
 * Multiplicativity: a solution for a divisor of n gives one for n, so only n prime need checking.
 * usage: es_check N            -- checks all primes p <= N, reports failures and statistics */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static u64 tries;
static int solve(u64 n, u64 *sx, u64 *sy, u64 *sz){
    tries=0;
    for(u64 x=n/4+1; x<=3*n/4+1; x++){
        tries++;
        u64 a = 4*x - n;            /* 4/n - 1/x = a/(n x) */
        if((long long)a<=0) continue;
        u64 b = n*x;
        for(u64 y=b/a+1; y<=2*b/a+2; y++){
            u64 num = a*y - b;
            if((long long)num<=0) continue;
            if((b*y) % num == 0){ *sx=x; *sy=y; *sz=(b*y)/num; return 1; }
        }
    }
    return 0;
}
int main(int argc,char**argv){
    u64 N=strtoull(argv[1],0,10);
    char*comp=calloc(N+1,1);
    for(u64 i=2;i*i<=N;i++) if(!comp[i]) for(u64 j=i*i;j<=N;j+=i) comp[j]=1;
    u64 checked=0, fails=0, maxx=0, argmax=0; u64 x,y,z;
    u64 hist[8]={0}; u64 worstt=0, worstn=0;
    for(u64 p=2;p<=N;p++){
        if(comp[p]) continue;
        checked++;
        if(!solve(p,&x,&y,&z)){ fails++; printf("COUNTEREXAMPLE n=%llu\n",p); }
        else { if(x>maxx){maxx=x; argmax=p;}
            int b=0; u64 t=tries; while(t>1 && b<7){t>>=2; b++;} hist[b]++;
            if(tries>worstt){worstt=tries; worstn=p;} }
    }
    printf("  распределение числа проб x: ");
    for(int i=0;i<8;i++) if(hist[i]) printf("[<=4^%d]=%llu ", i, hist[i]);
    printf("\n  худший случай: %llu проб при n=%llu (доля от n/2: %.4f)\n", worstt, worstn, worstn?(double)worstt/(worstn/2.0):0);
    printf("N=%llu: primes checked=%llu, failures=%llu, worst first-denominator x=%llu at n=%llu (x/n=%.3f)\n",
           N, checked, fails, maxx, argmax, argmax?(double)maxx/argmax:0);
    return 0;
}
