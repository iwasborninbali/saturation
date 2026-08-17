/* maxsub.c — CNF: at least s points among candidates read from stdin ("x y" per line), no three collinear in Z^2.
   usage: maxsub s < cands > cnf   (candidate order = input order; variable i <-> line i, 1-based) */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    int s = atoi(argv[1]); static int cx[4096], cy[4096]; int n = 0;
    while (scanf("%d %d", &cx[n], &cy[n]) == 2) n++;
    long ncl = 0;
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        long d = (long)(cx[b] - cx[a]) * (cy[c] - cy[a]) - (long)(cy[b] - cy[a]) * (cx[c] - cx[a]);
        if (d == 0) ncl++;
    }
    int K = n - s; long aux = (long)(n - 1) * K;
    long card = 1 + (K - 1) + (long)(n - 2) * (2 + 2 * (K - 1) + 1) + 1;
    printf("p cnf %ld %ld\n", (long)n + aux, ncl + card);
    for (int a = 0; a < n; a++) for (int b = a + 1; b < n; b++) for (int c = b + 1; c < n; c++) {
        long d = (long)(cx[b] - cx[a]) * (cy[c] - cy[a]) - (long)(cy[b] - cy[a]) * (cx[c] - cx[a]);
        if (d == 0) printf("%d %d %d 0\n", -(a + 1), -(b + 1), -(c + 1));
    }
    #define R(i, j) ((long)n + (long)((i) - 1) * K + (j))
    #define L(i) (-(i))
    printf("%d %ld 0\n", -L(1), R(1, 1));
    for (int j = 2; j <= K; j++) printf("%ld 0\n", -R(1, j));
    for (int i = 2; i <= n - 1; i++) {
        printf("%d %ld 0\n", -L(i), R(i, 1)); printf("%ld %ld 0\n", -R(i - 1, 1), R(i, 1));
        for (int j = 2; j <= K; j++) { printf("%d %ld %ld 0\n", -L(i), -R(i - 1, j - 1), R(i, j)); printf("%ld %ld 0\n", -R(i - 1, j), R(i, j)); }
        printf("%d %ld 0\n", -L(i), -R(i - 1, K));
    }
    printf("%d %ld 0\n", -L(n), -R(n - 1, K));
    return 0;
}
