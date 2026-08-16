/* walk.c — a second search at this end: local search instead of tree search.
 *
 * State: every reading class of the first register (row u) holds exactly two
 * tokens; the second register of each is free.  Cost: number of degenerate
 * triples (three tokens read alike by some rank-1 probe).  Move: one token
 * changes its second register.  Min-conflicts with tabu + noise; restarts.
 * Cost is zero  <=>  the book is lawful, and 2n tokens with 2 per class of one
 * register and no degenerate triple forces 2 per class of the other as well.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/time.h>

#define MAXN 128
static int n, K;                     /* resolution, K = 2n tokens */
static int pu[2 * MAXN], pv[2 * MAXN];/* registers of token i (token 2u, 2u+1 live in row u) */
static unsigned char occ[MAXN * MAXN];
static int gtab[MAXN][MAXN];         /* gcd table */
static int dirkey[2 * MAXN + 1][2 * MAXN + 1]; /* (du+n, dv+n) -> counter slot */
static int cnt[8 * MAXN * MAXN];     /* counter per direction slot */
static int touched[2 * MAXN], ntouched;
static long tri[2 * MAXN];           /* degenerate triples through token i */
static long cost;
static int tabu[MAXN][MAXN];         /* iteration until which (u, v) is tabu */
static uint64_t rs = 0x9E3779B97F4A7C15ULL;
static double t0;

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* number of pairs among tokens (except 'skip') aliased with cell (u, v) */
static long pairs_through(int u, int v, int skip) {
    long s = 0; ntouched = 0;
    for (int i = 0; i < K; i++) {
        if (i == skip) continue;
        int du = pu[i] - u, dv = pv[i] - v;
        if (du == 0 && dv == 0) { continue; }             /* same cell: handled by caller */
        int g = gtab[abs(du)][abs(dv)];
        du /= g; dv /= g;
        if (du < 0 || (du == 0 && dv < 0)) { du = -du; dv = -dv; }
        int slot = dirkey[du + n][dv + n];
        if (cnt[slot]++ == 0) touched[ntouched++] = slot;
        else s += cnt[slot] - 1;                          /* new pairs with the earlier ones */
    }
    for (int j = 0; j < ntouched; j++) cnt[touched[j]] = 0;
    return s;
}

static void recompute(void) {
    cost = 0;
    for (int i = 0; i < K; i++) { tri[i] = pairs_through(pu[i], pv[i], i); cost += tri[i]; }
    cost /= 3;
}

static int verify(void) {
    for (int a = 0; a < K; a++) for (int b = a + 1; b < K; b++) for (int c = b + 1; c < K; c++) {
        long x = (long)(pu[b] - pu[a]) * (pv[c] - pv[a]) - (long)(pv[b] - pv[a]) * (pu[c] - pu[a]);
        if (x == 0) return 0;
    }
    return 1;
}

static void randomize(void) {
    memset(occ, 0, sizeof occ);
    for (int u = 0; u < n; u++) {
        int a = rnd() % n, b;
        do { b = rnd() % n; } while (b == a);
        pu[2 * u] = u; pv[2 * u] = a; pu[2 * u + 1] = u; pv[2 * u + 1] = b;
        occ[u * n + a] = occ[u * n + b] = 1;
    }
    memset(tabu, 0, sizeof tabu);
    recompute();
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: walk n [seed] [seconds] [tabu] [noise%%] [restart_iters]\n"); return 64; }
    n = atoi(argv[1]); K = 2 * n;
    uint64_t seed = argc > 2 ? strtoull(argv[2], 0, 10) : 1;
    double tlimit = argc > 3 ? atof(argv[3]) : 60;
    int tabulen = argc > 4 ? atoi(argv[4]) : n / 2;
    int noise = argc > 5 ? atoi(argv[5]) : 5;
    long restart_iters = argc > 6 ? atol(argv[6]) : 200000;
    if (n < 2 || n > MAXN) return 64;
    rs ^= seed * 0x2545F4914F6CDD1DULL; for (int i = 0; i < 20; i++) rnd();
    for (int a = 0; a < MAXN; a++) for (int b = 0; b < MAXN; b++) gtab[a][b] = (a || b) ? gcd(a, b) : 1;
    int slots = 0;
    for (int du = 0; du <= n; du++) for (int dv = -n; dv <= n; dv++) dirkey[du + n][dv + n] = slots++;
    t0 = now();
    long iter = 0, best = 1L << 60, sincebest = 0, restarts = 0;
    randomize();
    while (cost > 0) {
        iter++;
        if (now() - t0 > tlimit && (iter & 1023) == 0) {
            printf("timeout n=%d seed=%llu iters=%ld restarts=%ld best=%ld secs=%.1f\n", n, (unsigned long long)seed, iter, restarts, best, now() - t0);
            return 1;
        }
        /* pick a conflicted token */
        int i;
        do { i = rnd() % K; } while (tri[i] == 0);
        int u = pu[i], oldv = pv[i];
        int other = pv[i ^ 1];
        long bestscore = 1L << 60; int bestv = -1, ties = 0;
        if ((int)(rnd() % 100) < noise) {
            do { bestv = rnd() % n; } while (bestv == oldv || bestv == other);
        } else {
            for (int v = 0; v < n; v++) {
                if (v == oldv || v == other) continue;
                if (tabu[u][v] > iter) continue;
                long s = pairs_through(u, v, i);
                if (s < bestscore) { bestscore = s; bestv = v; ties = 1; }
                else if (s == bestscore && rnd() % ++ties == 0) bestv = v;
            }
            if (bestv < 0) continue;
        }
        occ[u * n + oldv] = 0; occ[u * n + bestv] = 1;
        pv[i] = bestv;
        tabu[u][oldv] = iter + tabulen + rnd() % (tabulen + 1);
        recompute();
        if (cost < best) { best = cost; sincebest = 0; } else sincebest++;
        if (sincebest > restart_iters) { restarts++; sincebest = 0; best = 1L << 60; randomize(); }
    }
    if (!verify()) { printf("BUG\n"); return 70; }
    int book[2 * MAXN];
    for (int i = 0; i < K; i++) book[i] = pu[i] * n + pv[i];
    for (int i = 0; i < K; i++) for (int j = i + 1; j < K; j++) if (book[j] < book[i]) { int t = book[i]; book[i] = book[j]; book[j] = t; }
    printf("book n=%d sym=0 seed=%llu iters=%ld restarts=%ld secs=%.2f :", n, (unsigned long long)seed, iter, restarts, now() - t0);
    for (int i = 0; i < K; i++) printf(" %d", book[i]);
    printf("\n");
    return 0;
}
