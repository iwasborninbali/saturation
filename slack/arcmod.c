/* arcmod.c — CNF for: a subset S of Z_m x Z_m of size >= s with no three points a,b,c having det(b-a,c-a) = 0 (mod m).
   Such S is lawful in the m x m grid (integer collinearity implies modular collinearity).  usage: arcmod m s > file.cnf */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    int m = atoi(argv[1]), s = atoi(argv[2]);
    int N = m * m;                                    /* variables 1..N : x[u*m+v+1] */
    long ncl = 0;
    /* count clauses first (need header): triples with det = 0 mod m */
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) {
        int ua = a / m, va = a % m, ub = b / m, vb = b % m, uc = c / m, vc = c % m;
        long d = (long)(ub - ua) * (vc - va) - (long)(vb - va) * (uc - ua);
        if (((d % m) + m) % m == 0) ncl++;
    }
    int K = N - s;                                    /* at most K of the negated literals are true  <=>  at least s points */
    long aux = (long)(N - 1) * K;
    long card = 0;                                    /* clause count of the sequential counter */
    card = 1 + (K - 1) + (long)(N - 2) * (2 + 2 * (K - 1) + 1) + 1;
    printf("p cnf %ld %ld\n", (long)N + aux, ncl + card + 1);
    printf("1 0\n");                                  /* symmetry breaking: (0,0) in S (translations preserve det mod m) */
    for (int a = 0; a < N; a++) for (int b = a + 1; b < N; b++) for (int c = b + 1; c < N; c++) {
        int ua = a / m, va = a % m, ub = b / m, vb = b % m, uc = c / m, vc = c % m;
        long d = (long)(ub - ua) * (vc - va) - (long)(vb - va) * (uc - ua);
        if (((d % m) + m) % m == 0) printf("%d %d %d 0\n", -(a + 1), -(b + 1), -(c + 1));
    }
    /* Sinz sequential counter for AtMost K over literals l_i = NOT x_i (i = 1..N); registers R(i,j) = N + (i-1)*K + j */
    #define R(i, j) ((long)N + (long)((i) - 1) * K + (j))
    #define L(i) (-(i))                                /* literal l_i = -x_i */
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
