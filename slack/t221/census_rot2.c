/* census_rot2.c — exhaustive census of half-turn (rot2) invariant no-three-in-line configurations on an n x n grid, n even.
 * A configuration has 2n points, two per row and per column, no three collinear, and is invariant under (x,y) -> (m-x, m-y).
 * Rows pair up: choosing the two columns of each of the n/2 top rows determines the whole configuration.
 * Collinearity is maintained incrementally: when a point is placed, every cell collinear with it and an earlier point is
 * marked forbidden (one bit per cell, one 64-bit word per row).  Counts LABELLED configurations.
 * usage: census_rot2 n [verbose]                                     (second solver, 2026-08-20) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int n, m, half;
static u64 forb[64][64];          /* forb[level][row] : cells forbidden at this level */
static int px[64], py[64], np;    /* placed points */
static int colcnt[64];
static long long solutions, nodes;
static int verbose;
static int gcd_(int a,int b){while(b){int t=a%b;a=b;b=t;}return a<0?-a:a;}

/* mark all cells collinear with (x1,y1),(x2,y2) as forbidden at level L */
static void mark_line(int L,int x1,int y1,int x2,int y2){
    int dx=x2-x1, dy=y2-y1, g=gcd_(dx,dy); if(!g) return; dx/=g; dy/=g;
    int x=x1, y=y1;
    while(x>=0&&x<n&&y>=0&&y<n){ forb[L][x]|=1ULL<<y; x-=dx; y-=dy; }
    x=x1+dx; y=y1+dy;
    while(x>=0&&x<n&&y>=0&&y<n){ forb[L][x]|=1ULL<<y; x+=dx; y+=dy; }
}
/* try to place point (x,y) at level L; returns 0 if it is forbidden */
static int place(int L,int x,int y){
    if(forb[L][x]>>y & 1ULL) return 0;
    for(int i=0;i<np;i++) mark_line(L,px[i],py[i],x,y);
    px[np]=x; py[np]=y; np++;
    return 1;
}
static void rec(int r){
    nodes++;
    if(r==half){
        for(int c=0;c<n;c++) if(colcnt[c]!=2) return;
        solutions++;
        if(verbose){ printf("sol"); for(int i=0;i<np;i++) printf(" %d", px[i]*n+py[i]); printf("\n"); }
        return;
    }
    int L=r;
    for(int y1=0;y1<n;y1++){
        if(forb[L][r]>>y1 & 1ULL) continue;
        if(colcnt[y1]>=2 || colcnt[m-y1]>=2) continue;
        for(int y2=y1+1;y2<n;y2++){
            if(forb[L][r]>>y2 & 1ULL) continue;
            int add1=(y1==m-y2), add2=0;
            /* column capacities for the four points (r,y1),(r,y2),(m-r,m-y1),(m-r,m-y2) */
            int cc[64]; memcpy(cc,colcnt,sizeof(int)*n);
            cc[y1]++; cc[y2]++; cc[m-y1]++; cc[m-y2]++;
            if(cc[y1]>2||cc[y2]>2||cc[m-y1]>2||cc[m-y2]>2) continue;
            (void)add1;(void)add2;
            int savednp=np; memcpy(forb[L+1],forb[L],sizeof(u64)*n);
            int ok = place(L+1,r,y1) && place(L+1,r,y2)
                  && place(L+1,m-r,m-y1) && place(L+1,m-r,m-y2);
            if(ok){
                int savedcol[64]; memcpy(savedcol,colcnt,sizeof(int)*n);
                memcpy(colcnt,cc,sizeof(int)*n);
                rec(r+1);
                memcpy(colcnt,savedcol,sizeof(int)*n);
            }
            np=savednp;
        }
    }
}
int main(int argc,char**argv){
    if(argc<2){fprintf(stderr,"usage: census_rot2 n [verbose]\n");return 64;}
    n=atoi(argv[1]); verbose = argc>2;
    if(n%2){fprintf(stderr,"n must be even\n");return 64;}
    if(n>64){fprintf(stderr,"n<=64\n");return 64;}
    m=n-1; half=n/2;
    memset(forb,0,sizeof(forb)); memset(colcnt,0,sizeof(colcnt)); np=0;
    rec(0);
    fprintf(stderr,"n=%d rot2 census: labelled solutions=%lld nodes=%lld\n", n, solutions, nodes);
    printf("n=%d labelled=%lld nodes=%lld\n", n, solutions, nodes);
    return 0;
}
