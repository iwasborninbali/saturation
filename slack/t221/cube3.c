/* cube3.c — INDEPENDENT exhaustive search for the maximum no-three-collinear subset of the grid [n]^3.
 * Written deliberately differently from the orbit/bitboard enumerator of the first solver: plain
 * include/exclude DFS over cells in index order, with (a) a precomputed mask, for every ordered pair of
 * cells, of all cells collinear with them, and (b) the bound  chosen + |available cells ahead| <= best.
 * No symmetry breaking, no CP solver: the point is to be a second, unrelated witness.
 * usage: cube3 n [target]        prints the maximum and a witness. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
#define MAXW 8
static int n,N,W;
static u64 (*pairmask)[MAXW];      /* [i*N+j] -> cells collinear with i and j (excluding i,j) */
static u64 forb[400][MAXW];
static int chosen[400], nch, best, bestset[400];
static long long nodes;
static int gcd_(int a,int b){while(b){int t=a%b;a=b;b=t;}return a<0?-a:a;}
static inline int popc(const u64*a){int s=0;for(int w=0;w<W;w++)s+=__builtin_popcountll(a[w]);return s;}
static void build(void){
    pairmask=malloc((size_t)N*N*sizeof(u64)*MAXW);
    memset(pairmask,0,(size_t)N*N*sizeof(u64)*MAXW);
    for(int i=0;i<N;i++){
        int xi=i/(n*n), yi=(i/n)%n, zi=i%n;
        for(int j=i+1;j<N;j++){
            int xj=j/(n*n), yj=(j/n)%n, zj=j%n;
            int dx=xj-xi, dy=yj-yi, dz=zj-zi;
            int g=gcd_(gcd_(dx,dy),dz); if(!g) continue; dx/=g; dy/=g; dz/=g;
            u64*m=pairmask[i*N+j];
            for(int s=-n;s<=n;s++){
                int x=xi+s*dx, y=yi+s*dy, z=zi+s*dz;
                if(x<0||x>=n||y<0||y>=n||z<0||z>=n) continue;
                int c=x*n*n+y*n+z;
                if(c==i||c==j) continue;
                m[c>>6] |= 1ULL<<(c&63);
            }
            memcpy(pairmask[j*N+i],m,sizeof(u64)*MAXW);
        }
    }
}
static void rec(int idx,int lvl){
    nodes++;
    /* bound: how many cells from idx..N-1 are still allowed */
    int avail=0;
    for(int c=idx;c<N;c++) if(!(forb[lvl][c>>6]>>(c&63)&1ULL)) avail++;
    if(nch+avail<=best) return;
    if(idx==N){ if(nch>best){best=nch; memcpy(bestset,chosen,sizeof(int)*nch);} return; }
    /* include cell idx if allowed */
    if(!(forb[lvl][idx>>6]>>(idx&63)&1ULL)){
        memcpy(forb[lvl+1],forb[lvl],sizeof(u64)*W);
        for(int t=0;t<nch;t++){ const u64*m=pairmask[chosen[t]*N+idx]; for(int w=0;w<W;w++) forb[lvl+1][w]|=m[w]; }
        chosen[nch++]=idx;
        rec(idx+1,lvl+1);
        nch--;
    }
    rec(idx+1,lvl);
}
/* Knuth (1975) random-probe estimate of the size of the pruned tree: dive from the root choosing a
 * child uniformly at random, accumulating the product of branching factors; the mean over dives is
 * an unbiased estimate of the number of nodes. Pruning uses the same rules, with `best` pre-seeded. */
static u64 rs=88172645463325252ULL;
static double dive(void){
    int idx=0,lvl=0; nch=0; memset(forb[0],0,sizeof(u64)*W);
    double w=1.0, sum=1.0;
    while(idx<N){
        int avail=0;
        for(int c=idx;c<N;c++) if(!(forb[lvl][c>>6]>>(c&63)&1ULL)) avail++;
        if(nch+avail<=best) break;
        int canInc = !(forb[lvl][idx>>6]>>(idx&63)&1ULL);
        int d = canInc?2:1;
        w *= d; sum += w;
        rs^=rs<<13; rs^=rs>>7; rs^=rs<<17;
        int takeInc = canInc && ((rs>>33)&1);
        if(takeInc){
            memcpy(forb[lvl+1],forb[lvl],sizeof(u64)*W);
            for(int t=0;t<nch;t++){const u64*m=pairmask[chosen[t]*N+idx]; for(int wq=0;wq<W;wq++) forb[lvl+1][wq]|=m[wq];}
            chosen[nch++]=idx; lvl++;
        }
        idx++;
    }
    return sum;
}
int main(int argc,char**argv){
    n=atoi(argv[1]); N=n*n*n; W=(N+63)/64; if(W>MAXW){fprintf(stderr,"n too large\n");return 64;}
    best = argc>2 ? atoi(argv[2])-1 : 0;
    build();
    memset(forb,0,sizeof(forb));
    if(getenv("ESTIMATE")){
        int T=atoi(getenv("ESTIMATE")); double s1=0,s2=0;
        for(int t=0;t<T;t++){ double v=dive(); s1+=v; s2+=v*v; }
        double mean=s1/T, sd=(T>1)?__builtin_sqrt((s2-s1*s1/T)/(T-1)):0;
        printf("n=%d best-seed=%d probes=%d  ESTIMATED nodes = %.3g  (sd of probe %.3g)\n", n, best, T, mean, sd);
        return 0;
    }
    rec(0,0);
    printf("n=%d  max no-three-collinear in [n]^3 = %d   nodes=%lld\n", n, best, nodes);
    printf("  witness:"); for(int i=0;i<best;i++) printf(" %d", bestset[i]); printf("\n");
    return 0;
}
