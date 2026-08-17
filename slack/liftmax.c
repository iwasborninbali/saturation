/* liftmax.c — CNF: at least s points among the candidates C = { (x,y) in [0,N)^2 : x*y = k (mod p), x,y not = 0 mod p }
   (or parabola y = x^2 mod p with mode 'P'), no three collinear in Z^2.   usage: liftmax mode p N k s > cnf
   Candidate index list is printed to stderr as "cand i x y". */
#include <stdio.h>
#include <stdlib.h>
int main(int argc, char **argv) {
    char mode = argv[1][0]; int p = atoi(argv[2]), N = atoi(argv[3]), k = atoi(argv[4]), s = atoi(argv[5]);
    static int cx[40000], cy[40000]; int n = 0;
    for (int x = 0; x < N; x++) for (int y = 0; y < N; y++) {
        int ok = 0;
        if (mode == 'H') ok = (x % p) && (y % p) && (((long)x * y - k) % p == 0);
        else if (mode == 'W') { long xx = x - (p - 1) / 2; long xm = ((xx % p) + p) % p; ok = xm && (y % p) && (((xm * y) % p - k) % p == 0); }
        else if (mode == 'K') { long xx = x - (p - 1) / 2; long xm = ((xx % p) + p) % p;
                                ok = xm && (y % p) && ((((xm * y) % p) - 1) % p == 0 || (((xm * y) % p) - k) % p == 0); }
        else if (mode == 'U') { int q = k; long xp = ((x - (p - 1) / 2) % p + p) % p, xq = ((x - (q - 1) / 2) % q + q) % q;
                                ok = (xp && (y % p) && (((xp * y) % p) - 1) % p == 0) || (xq && (y % q) && (((xq * y) % q) - 1) % q == 0); }
        else if (mode == 'P') ok = ((y - ((long)x * x + k) % p) % p == 0);
        if (ok) { cx[n] = x; cy[n] = y; n++; }
    }
    for (int i = 0; i < n; i++) fprintf(stderr, "cand %d %d %d\n", i, cx[i], cy[i]);
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
        printf("%d %ld 0\n", -L(i), R(i, 1));
        printf("%ld %ld 0\n", -R(i - 1, 1), R(i, 1));
        for (int j = 2; j <= K; j++) { printf("%d %ld %ld 0\n", -L(i), -R(i - 1, j - 1), R(i, j)); printf("%ld %ld 0\n", -R(i - 1, j), R(i, j)); }
        printf("%d %ld 0\n", -L(i), -R(i - 1, K));
    }
    printf("%d %ld 0\n", -L(n), -R(n - 1, K));
    return 0;
}
