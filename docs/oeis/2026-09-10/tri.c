/* tri.c -- independent recount (Conductor, 10 Sep 2026).
   For the n x n grid: T(n,k) = number of k-subsets with no three collinear points (empty set included),
   and M(n,k) = number of such subsets of size k that are maximal (no grid point can be added).
   Method: depth-first enumeration in cell order; a cell is admissible iff it is not collinear with any
   two already chosen cells; collinearity of (a,b,c) tested by an exact integer cross product.
   The set of cells blocked by the chosen pairs is kept as a bitmask (B) updated incrementally:
   when cell c is chosen, every cell x with cross(s, c, x) == 0 for some earlier chosen s is blocked.
   Maximality: every cell outside S is blocked. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
typedef unsigned long long u64;
static int n, N, X[64], Y[64];
static u64 blockmask[64][64];   /* blockmask[s][c] = cells x collinear with s and c (x != s, x != c) */
static u64 cnt[65], mx[65], FULL;
static int chosen[64];
static void dfs(int start, u64 S, u64 B, int k){
    cnt[k]++;
    if ((S | B) == FULL) mx[k]++;
    for (int c = start; c < N; c++){
        if (B >> c & 1) continue;
        u64 B2 = B;
        for (int t = 0; t < k; t++) B2 |= blockmask[chosen[t]][c];
        chosen[k] = c;
        dfs(c + 1, S | (1ULL << c), B2, k + 1);
    }
}
int main(int argc, char **argv){
    n = atoi(argv[1]); N = n * n; FULL = (N == 64) ? ~0ULL : ((1ULL << N) - 1);
    for (int i = 0; i < N; i++){ X[i] = i / n; Y[i] = i % n; }
    for (int s = 0; s < N; s++) for (int c = 0; c < N; c++){
        u64 m = 0;
        if (s != c) for (int x = 0; x < N; x++){
            if (x == s || x == c) continue;
            long cr = (long)(X[c]-X[s])*(Y[x]-Y[s]) - (long)(Y[c]-Y[s])*(X[x]-X[s]);
            if (cr == 0) m |= 1ULL << x;
        }
        blockmask[s][c] = m;
    }
    dfs(0, 0ULL, 0ULL, 0);
    u64 tot = 0, totm = 0; int last = 0;
    for (int k = 0; k <= N; k++){ tot += cnt[k]; totm += mx[k]; if (cnt[k]) last = k; }
    printf("n=%d total=%llu maximal=%llu maxsize=%d\n", n, tot, totm, last);
    printf("T(%d,k) k=0..%d:", n, last); for (int k = 0; k <= last; k++) printf(" %llu", cnt[k]); printf("\n");
    printf("M(%d,k) k=0..%d:", n, last); for (int k = 0; k <= last; k++) printf(" %llu", mx[k]); printf("\n");
    return 0;
}
