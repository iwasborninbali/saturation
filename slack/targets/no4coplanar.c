/* no4coplanar.c — independent enumerator for A280537: maximal subset of [n]^3 with NO FOUR COPLANAR points.
   Deliberately different logic from the partner's implementation: NO plane enumeration at all.  A candidate point is accepted
   iff it forms no coplanar quadruple with the already chosen ones, tested directly by the integer determinant
   det[b-a, d-a, c-a] == 0 over all triples (a,b,d) of chosen points.
   Order: index = z*n^2 + y*n + x, so the z-layers are contiguous; bound: each layer is a plane, hence <= 3 chosen per layer.
   usage: no4coplanar n [start_best] */
#include <stdio.h>
#include <stdlib.h>
static int n, N, best; static long long nodes;
static int px[512], py[512], pz[512], k;      /* chosen points */
static int used[64];                          /* chosen per z-layer */
static int det3(int ax,int ay,int az,int bx,int by,int bz,int cx,int cy,int cz){
    return ax*(by*cz-bz*cy) - ay*(bx*cz-bz*cx) + az*(bx*cy-by*cx);
}
static int ok_to_add(int x,int y,int z){
    for (int a = 0; a < k; a++)
        for (int b = a+1; b < k; b++)
            for (int d = b+1; d < k; d++){
                int ux=px[b]-px[a], uy=py[b]-py[a], uz=pz[b]-pz[a];
                int vx=px[d]-px[a], vy=py[d]-py[a], vz=pz[d]-pz[a];
                int wx=x-px[a],     wy=y-py[a],     wz=z-pz[a];
                if (det3(ux,uy,uz,vx,vy,vz,wx,wy,wz) == 0) return 0;
            }
    return 1;
}
static void dfs(int i){
    nodes++;
    if (i == N){ if (k > best){ best = k; fprintf(stderr,"  best=%d nodes=%lld\n", best, nodes);} return; }
    int L = i / (n*n), off = i % (n*n);
    int cap = 3 - used[L]; int left = n*n - off; if (cap > left) cap = left;
    if (k + cap + 3*(n - L - 1) <= best) return;
    int x = i % n, y = (i / n) % n, z = L;
    if (used[L] < 3 && ok_to_add(x,y,z)){
        px[k]=x; py[k]=y; pz[k]=z; k++; used[L]++;
        dfs(i+1);
        k--; used[L]--;
    }
    dfs(i+1);
}
int main(int argc, char **argv){
    n = atoi(argv[1]); N = n*n*n; best = (argc > 2) ? atoi(argv[2]) : 0; k = 0;
    for (int i = 0; i < 64; i++) used[i] = 0;
    dfs(0);
    printf("n=%d  MAX=%d  nodes=%lld\n", n, best, nodes);
    return 0;
}
