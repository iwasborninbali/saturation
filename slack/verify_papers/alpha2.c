/* alpha2.c — точный максимум подмножества с <=2 точками на каждой из данных прямых.
 * Ветви-и-границы; независим от кода статьи. stdin: N L, затем L строк: k i1..ik. */
#include <stdio.h>
#include <string.h>
typedef unsigned long long u64;
#define W 4
static int N,L,cnt[4096],cap[4096];
static u64 lm[4096][W];
static int nl_of[256][64], nn_of[256];
static int best; static long long nodes;
static void rec(int i,int taken,u64 *alive){
    nodes++;
    int rest=0;
    for(int w=0;w<W;w++){ u64 m=alive[w]&(~0ULL); if(i<64*(w+1)){ if(i>64*w) m&= ~((1ULL<<(i-64*w))-1); } else m=0; rest+=__builtin_popcountll(m); }
    /* rest = живые с индексом >= i */
    if(taken+rest<=best) return;
    if(i>=N){ if(taken>best) best=taken; return; }
    int w=i/64, b=i%64;
    if(!(alive[w]>>b&1)){ rec(i+1,taken,alive); return; }
    /* ветвь: взять i */
    u64 na[W]; memcpy(na,alive,sizeof na);
    int okv=1, touched[64], nt=0;
    for(int t=0;t<nn_of[i];t++){
        int li=nl_of[i][t];
        if(++cnt[li]==cap[li]+1){ okv=0; }
        touched[nt++]=li;
        if(cnt[li]==cap[li]) for(int ww=0;ww<W;ww++) na[ww]&=~lm[li][ww];
    }
    if(okv){ na[w]|= (1ULL<<b); /* сам остаётся взятым */ rec(i+1,taken+1,na); }
    for(int t=0;t<nt;t++) cnt[touched[t]]--;
    /* ветвь: не брать i */
    u64 nb[W]; memcpy(nb,alive,sizeof nb); nb[w]&=~(1ULL<<b);
    rec(i+1,taken,nb);
}
int main(){
    if(scanf("%d %d",&N,&L)!=2) return 2;
    if(N>256||L>4096){fprintf(stderr,"велико\n");return 2;}
    for(int i=0;i<N;i++) nn_of[i]=0;
    for(int l=0;l<L;l++){int k;scanf("%d",&k);cap[l]=2;cnt[l]=0;memset(lm[l],0,sizeof lm[l]);
        for(int j=0;j<k;j++){int x;scanf("%d",&x);lm[l][x/64]|=1ULL<<(x%64);nl_of[x][nn_of[x]++]=l;}}
    u64 alive[W]; memset(alive,0,sizeof alive);
    for(int i=0;i<N;i++) alive[i/64]|=1ULL<<(i%64);
    best=0; nodes=0; rec(0,0,alive);
    printf("%d %lld\n",best,nodes);
    return 0;
}
