/* no3_3d.c — exhaustive proof of the maximum subset of [n]^3 with no three collinear points.
   DFS over cells in lex order (x,y,z; z fastest, so z-columns are contiguous blocks of n cells).
   Pruning: chosen + 2*(whole columns ahead) + min(2-used_cur, cells left in the current column) <= best  =>  cut.
   Counts NODES (calls), so the growth ratio can be measured.  Usage: no3_3d n [best_known_lower_bound] */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int n, N, NL;
static int *lineof, *lineoff, *lcnt;      /* lines through each cell (CSR) */
static unsigned char *cnt;                /* points chosen on each line */
static int best; static long long nodes;
static int *colused;                      /* points chosen in each z-column */
static int gcd3(int a,int b,int c){int g=a;while(b){int t=b;b=g%b;g=t;}while(c){int t=c;c=g%c;g=t;}return g<0?-g:g;}
static void dfs(int i, int chosen){
    nodes++;
    if (i == N){ if (chosen > best){ best = chosen; fprintf(stderr,"  new best %d (nodes %lld)\n",best,nodes);} return; }
    int col = i / n, off = i % n;
    int ub = chosen + (n*n - col - 1)*2 + (2 - colused[col] < n - off ? 2 - colused[col] : n - off);
    if (ub <= best) return;
    /* take cell i if allowed */
    int ok = 1;
    for (int k = lineoff[i]; k < lineoff[i+1]; k++) if (cnt[lineof[k]] >= 2){ ok = 0; break; }
    if (ok && colused[col] < 2){
        for (int k = lineoff[i]; k < lineoff[i+1]; k++) cnt[lineof[k]]++;
        colused[col]++;
        dfs(i+1, chosen+1);
        colused[col]--;
        for (int k = lineoff[i]; k < lineoff[i+1]; k++) cnt[lineof[k]]--;
    }
    dfs(i+1, chosen);
}
int main(int argc, char **argv){
    n = atoi(argv[1]); best = (argc > 2) ? atoi(argv[2]) : 0; N = n*n*n;
    int m0 = (argc > 3) ? atoi(argv[3]) : -1, m1 = (argc > 4) ? atoi(argv[4]) : -1;   /* optional prefix: chosen cells of columns 0 and 1 */
    /* enumerate lines: canonical (base, dir) */
    int cap = 1<<20, nl = 0; int (*lines)[3] = malloc(sizeof(int)*3*cap);
    unsigned char *seen = calloc((size_t)N*N, 1);
    int *members = malloc(sizeof(int)*cap*  (n>16?n:16));
    int *mstart = malloc(sizeof(int)*(cap+1)); int mn = 0;
    for (int a = 0; a < N; a++) for (int b = a+1; b < N; b++){
        if (seen[(size_t)a*N+b]) continue;
        int ax=a/(n*n), ay=(a/n)%n, az=a%n, bx=b/(n*n), by=(b/n)%n, bz=b%n;
        int dx=bx-ax, dy=by-ay, dz=bz-az; int g=gcd3(dx,dy,dz); dx/=g; dy/=g; dz/=g;
        int sx=ax, sy=ay, sz=az;
        while (sx-dx>=0 && sx-dx<n && sy-dy>=0 && sy-dy<n && sz-dz>=0 && sz-dz<n){ sx-=dx; sy-=dy; sz-=dz; }
        int cells[64], m=0, cx=sx, cy=sy, cz=sz;
        while (cx>=0&&cx<n&&cy>=0&&cy<n&&cz>=0&&cz<n){ cells[m++] = (cx*n+cy)*n+cz; cx+=dx; cy+=dy; cz+=dz; }
        for (int u=0;u<m;u++) for (int v=u+1;v<m;v++){ seen[(size_t)cells[u]*N+cells[v]] = 1; seen[(size_t)cells[v]*N+cells[u]] = 1; }
        if (m >= 3){ mstart[nl] = mn; for (int u=0;u<m;u++) members[mn++] = cells[u]; nl++; }
    }
    mstart[nl] = mn; NL = nl;
    /* CSR: lines through each cell */
    lineoff = calloc(N+2, sizeof(int));
    for (int l=0;l<nl;l++) for (int k=mstart[l];k<mstart[l+1];k++) lineoff[members[k]+1]++;
    for (int i=0;i<N;i++) lineoff[i+1]+=lineoff[i];
    lineof = malloc(sizeof(int)*mn); int *pos = malloc(sizeof(int)*N); memcpy(pos, lineoff, sizeof(int)*N);
    for (int l=0;l<nl;l++) for (int k=mstart[l];k<mstart[l+1];k++) lineof[pos[members[k]]++] = l;
    cnt = calloc(nl,1); colused = calloc(n*n, sizeof(int));
    fprintf(stderr,"n=%d cells=%d lines>=3: %d (start best=%d) prefix=%d,%d\n", n, N, nl, best, m0, m1);
    if (m0 < 0){ dfs(0,0); }
    else {
        int chosen = 0, ok = 1;
        for (int i = 0; i < 2*n && ok; i++){
            int bit = (i < n) ? ((m0 >> i) & 1) : ((m1 >> (i-n)) & 1);
            if (!bit) continue;
            int col = i / n;
            for (int k = lineoff[i]; k < lineoff[i+1]; k++) if (cnt[lineof[k]] >= 2){ ok = 0; break; }
            if (!ok || colused[col] >= 2) { ok = 0; break; }
            for (int k = lineoff[i]; k < lineoff[i+1]; k++) cnt[lineof[k]]++;
            colused[col]++; chosen++;
        }
        if (ok) dfs(2*n, chosen);
    }
    printf("n=%d  MAX=%d  nodes=%lld  lines=%d\n", n, best, nodes, nl);
    return 0;
}
