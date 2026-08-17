/* arcmod2.c — CNF for det-arcs over Z_m x Z_m: |S| >= s, no triple with det(b-a,c-a) = 0 (mod m).
   Symmetry breaking (all valid for maximum arcs with |S| >= 3):
     (0,0) in S                                   (translations preserve det mod m)
     OR over divisors g of m, g < m: (g,0) in S   (GL2(Z_m) maps a difference d to (gcd(d,m),0))
     if m = p^2 (env FIX1=1): (1,0) in S           (an arc with |S|>=3 mod p^2 has a unimodular difference)
   usage: arcmod2 m s > file.cnf */
#include <stdio.h>
#include <stdlib.h>
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
int main(int argc, char **argv) {
    int m = atoi(argv[1]), s = atoi(argv[2]);
    int N = m * m;
    int fix1 = getenv("FIX1") != NULL;
    /* count det=0 triples: for each pair (a,b) count c > b with det = 0; total triples counted once each */
    long ncl = 0;
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) {
        int ua = a / m, va = a % m, ub = b / m, vb = b % m;
        int du = ub - ua, dv = vb - va;
        for (int c = b + 1; c < N; c++) {
            int uc = c / m, vc = c % m;
            long d = (long)du * (vc - va) - (long)dv * (uc - ua);
            if (((d % m) + m) % m == 0) ncl++;
        }
    }
    int K = N - s;
    long aux = (long)(N - 1) * K;
    long card = 1 + (K - 1) + (long)(N - 2) * (2 + 2 * (K - 1) + 1) + 1;
    int ndiv = 0; for (int g = 1; g < m; g++) if (m % g == 0) ndiv++;
    printf("p cnf %ld %ld\n", (long)N + aux, ncl + card + 1 + 1 + (fix1 ? 1 : 0));
    printf("1 0\n");                                            /* (0,0) in S */
    for (int g = 1; g < m; g++) if (m % g == 0) printf("%d ", g * m + 0 + 1); printf("0\n");   /* some (g,0) in S */
    if (fix1) printf("%d 0\n", 1 * m + 0 + 1);                  /* (1,0) in S */
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) {
        int ua = a / m, va = a % m, ub = b / m, vb = b % m;
        int du = ub - ua, dv = vb - va;
        for (int c = b + 1; c < N; c++) {
            int uc = c / m, vc = c % m;
            long d = (long)du * (vc - va) - (long)dv * (uc - ua);
            if (((d % m) + m) % m == 0) printf("%d %d %d 0\n", -(a + 1), -(b + 1), -(c + 1));
        }
    }
    #define R(i, j) ((long)N + (long)((i) - 1) * K + (j))
    #define L(i) (-(i))
    printf("%d %ld 0\n", -L(1), R(1, 1));
    for (int j = 2; j <= K; j++) printf("%ld 0\n", -R(1, j));
    for (int i = 2; i <= N - 1; i++) {
        printf("%d %ld 0\n", -L(i), R(i, 1));
        printf("%ld %ld 0\n", -R(i - 1, 1), R(i, 1));
        for (int j = 2; j <= K; j++) {
            printf("%d %ld %ld 0\n", -L(i), -R(i - 1, j - 1), R(i, j));
            printf("%ld %ld 0\n", -R(i - 1, j), R(i, j));
        }
        printf("%d %ld 0\n", -L(i), -R(i - 1, K));
    }
    printf("%d %ld 0\n", -L(N), -R(N - 1, K));
    return 0;
}
