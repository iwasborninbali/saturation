/* cube3_lb.c — stochastic search for LARGE no-three-collinear subsets of [n]^3 (lower bounds where the
 * exhaustive proof is out of reach).  Randomised greedy to a maximal set, then repeated destroy-and-repair
 * (remove r random points, greedily refill) with restarts.  Every reported set is re-verified from scratch
 * by testing all triples with exact integer cross products.
 * usage: cube3_lb n seconds [seed] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
typedef unsigned long long u64;
#define MAXW 24
static int n,N,W;
static u64 (*pm)[MAXW];
static int gcd_(int a,int b){while(b){int t=a%b;a=b;b=t;}return a<0?-a:a;}
static u64 rs=0x2545F4914F6CDD1DULL;
static inline u64 rnd(void){rs^=rs<<13;rs^=rs>>7;rs^=rs<<17;return rs;}
static void build(void){
    pm=malloc((size_t)N*N*sizeof(u64)*MAXW); memset(pm,0,(size_t)N*N*sizeof(u64)*MAXW);
    for(int i=0;i<N;i++){int xi=i/(n*n),yi=(i/n)%n,zi=i%n;
        for(int j=i+1;j<N;j++){int xj=j/(n*n),yj=(j/n)%n,zj=j%n;
            int dx=xj-xi,dy=yj-yi,dz=zj-zi,g=gcd_(gcd_(dx,dy),dz); if(!g)continue; dx/=g;dy/=g;dz/=g;
            u64*m=pm[i*N+j];
            for(int s=-n;s<=n;s++){int x=xi+s*dx,y=yi+s*dy,z=zi+s*dz;
                if(x<0||x>=n||y<0||y>=n||z<0||z>=n)continue; int c=x*n*n+y*n+z;
                if(c==i||c==j)continue; m[c>>6]|=1ULL<<(c&63);}
            memcpy(pm[j*N+i],m,sizeof(u64)*MAXW);}}
}
static int S[4096], ns;
static u64 forb[MAXW];
static void rebuild(void){
    memset(forb,0,sizeof(u64)*W);
    for(int a=0;a<ns;a++) for(int b=a+1;b<ns;b++){const u64*m=pm[S[a]*N+S[b]]; for(int w=0;w<W;w++) forb[w]|=m[w];}
    for(int a=0;a<ns;a++) forb[S[a]>>6]|=1ULL<<(S[a]&63);
}
static void greedy_fill(void){
    int order[4096]; for(int i=0;i<N;i++) order[i]=i;
    for(int i=N-1;i>0;i--){int j=rnd()%(i+1);int t=order[i];order[i]=order[j];order[j]=t;}
    for(int t=0;t<N;t++){int c=order[t];
        if(forb[c>>6]>>(c&63)&1ULL) continue;
        for(int a=0;a<ns;a++){const u64*m=pm[S[a]*N+c]; for(int w=0;w<W;w++) forb[w]|=m[w];}
        forb[c>>6]|=1ULL<<(c&63); S[ns++]=c;}
}
static int verify(void){
    for(int a=0;a<ns;a++)for(int b=a+1;b<ns;b++)for(int c=b+1;c<ns;c++){
        int p=S[a],q=S[b],r=S[c];
        long long ax=p/(n*n),ay=(p/n)%n,az=p%n, bx=q/(n*n),by=(q/n)%n,bz=q%n, cx=r/(n*n),cy=(r/n)%n,cz=r%n;
        long long ux=bx-ax,uy=by-ay,uz=bz-az, vx=cx-ax,vy=cy-ay,vz=cz-az;
        if(uy*vz-uz*vy==0 && uz*vx-ux*vz==0 && ux*vy-uy*vx==0) return 0;}
    return 1;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); double secs=atof(argv[2]); if(argc>3) rs^=strtoull(argv[3],0,10)*0x9E3779B97F4A7C15ULL;
    N=n*n*n; W=(N+63)/64; if(W>MAXW){fprintf(stderr,"n too big\n");return 64;}
    build();
    int best=0, bestS[4096]; clock_t t0=clock();
    while((double)(clock()-t0)/CLOCKS_PER_SEC < secs){
        ns=0; memset(forb,0,sizeof(u64)*W); greedy_fill();
        for(int it=0; it<4000 && (double)(clock()-t0)/CLOCKS_PER_SEC<secs; it++){
            int save[4096], nsave=ns; memcpy(save,S,sizeof(int)*ns);
            int r=1+rnd()%3;
            for(int k=0;k<r && ns>0;k++){int idx=rnd()%ns; S[idx]=S[--ns];}
            rebuild(); greedy_fill();
            if(ns<nsave){ns=nsave; memcpy(S,save,sizeof(int)*ns); rebuild();}
        }
        if(ns>best){best=ns; memcpy(bestS,S,sizeof(int)*ns);}
    }
    ns=best; memcpy(S,bestS,sizeof(int)*best);
    printf("n=%d  lower bound = %d  (verified: %s)\n", n, best, verify()?"OK":"FAILED");
    printf("  set:"); for(int i=0;i<best;i++) printf(" %d", bestS[i]); printf("\n");
    return 0;
}
