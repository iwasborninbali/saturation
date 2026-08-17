/* algebraicity.c — how "algebraic mod p" is a point set?  For each prime p in [pmin,pmax] compute the largest number of
   points of S lying on one curve of three cheap families over F_p: y = a x^2 + b x + c, x = a y^2 + b y + c,
   (x-h)(y-k) = c (c != 0).  Reads lines "n t1 t2 ... " (tokens u*n+v) from stdin; prints per line: n |S| best_p best_count family
   and the max over p of best_count.   usage: algebraicity pmin pmax < input */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
static int isprime(int p){ if(p<2) return 0; for(int d=2; d*d<=p; d++) if(p%d==0) return 0; return 1; }
int main(int argc, char **argv) {
    int pmin = atoi(argv[1]), pmax = atoi(argv[2]);
    static int cnt[64][64];
    char line[65536];
    while (fgets(line, sizeof line, stdin)) {
        int n; char *s = line; int off; if (sscanf(s, "%d%n", &n, &off) != 1) continue; s += off;
        static int xs[400], ys[400]; int m = 0, t;
        while (sscanf(s, "%d%n", &t, &off) == 1) { xs[m] = t / n; ys[m] = t % n; m++; s += off; }
        int bestAll = 0, bestP = 0; char bestF = '-';
        for (int p = pmin; p <= pmax; p++) {
            if (!isprime(p) || p > 61) continue;
            int best = 0; char fam = '-';
            /* residues */
            static int rx[400], ry[400];
            for (int i = 0; i < m; i++) { rx[i] = xs[i] % p; ry[i] = ys[i] % p; }
            /* family 1: y = a x^2 + b x + c  -> for each (a,b), c = y - a x^2 - b x ; count max over c */
            for (int a = 0; a < p; a++) for (int b = 0; b < p; b++) {
                static int c_count[64]; memset(c_count, 0, sizeof(int) * p);
                for (int i = 0; i < m; i++) { int c = ((ry[i] - a * rx[i] * rx[i] - b * rx[i]) % p + p) % p; c_count[c]++; }
                for (int c = 0; c < p; c++) if (c_count[c] > best) { best = c_count[c]; fam = 'P'; }
            }
            /* family 2: x = a y^2 + b y + c */
            for (int a = 0; a < p; a++) for (int b = 0; b < p; b++) {
                static int c_count[64]; memset(c_count, 0, sizeof(int) * p);
                for (int i = 0; i < m; i++) { int c = ((rx[i] - a * ry[i] * ry[i] - b * ry[i]) % p + p) % p; c_count[c]++; }
                for (int c = 0; c < p; c++) if (c_count[c] > best) { best = c_count[c]; fam = 'Q'; }
            }
            /* family 0: lines y = a x + b and x = c (degree 1) */
            for (int a = 0; a < p; a++) {
                static int c_count[64]; memset(c_count, 0, sizeof(int) * p);
                for (int i = 0; i < m; i++) { int c = ((ry[i] - a * rx[i]) % p + p) % p; c_count[c]++; }
                for (int c = 0; c < p; c++) if (c_count[c] > best) { best = c_count[c]; fam = 'L'; }
            }
            { static int c_count[64]; memset(c_count, 0, sizeof(int) * p);
              for (int i = 0; i < m; i++) c_count[rx[i]]++;
              for (int c = 0; c < p; c++) if (c_count[c] > best) { best = c_count[c]; fam = 'L'; } }
            /* family 3: (x-h)(y-k) = c, c != 0 */
            for (int h = 0; h < p; h++) for (int k = 0; k < p; k++) {
                static int c_count[64]; memset(c_count, 0, sizeof(int) * p);
                for (int i = 0; i < m; i++) { int c = (((rx[i] - h) * (ry[i] - k)) % p + p) % p; c_count[c]++; }
                for (int c = 1; c < p; c++) if (c_count[c] > best) { best = c_count[c]; fam = 'H'; }
            }
            if (best > bestAll) { bestAll = best; bestP = p; bestF = fam; }
        }
        printf("n=%d |S|=%d best=%d p=%d fam=%c frac=%.3f\n", n, m, bestAll, bestP, bestF, (double)bestAll / m);
    }
    return 0;
}
