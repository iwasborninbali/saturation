/* kit71/bp.c — belief propagation + decimation for saturated books ("tokens in superposition until observed").
 *
 * Variables: cells x_c in {0,1}. Factors: every row and column "exactly 2"; every grid line with >= 3 cells
 * "at most 2". Sum-product messages for cardinality factors via truncated polynomial products (degree <= 2),
 * leave-one-out by polynomial division. Decimation: fix the most polarised free cell, apply hard consequences
 * (shading of pairs, full classes), re-run BP; restart on contradiction. Only proposes; certify decides.
 *
 * usage: bp n [seed] [iters] [damping] [restarts] [sym]   sym: 0 none, 1 half-turn (variables = orbits)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>

#define MAXN 72
#define MAXC (MAXN * MAXN)

static int n, m, sym;
static int ncell;
/* factors: list of member cells; kind 0 = exactly 2, 1 = at most 2 */
static int nfac; static int *fstart, *fmem, *fkind;   /* CSR */
static int nmemb;
/* messages indexed by membership slot: msg_fv[k] = factor->variable message ratio r = m(1)/m(0) (log domain), msg_vf similarly */
static double *lfv, *lvf;      /* log-ratio messages */
static int *memb_cell;         /* membership slot -> cell */
static int *cell_start, *cell_slots;  /* CSR of a cell's membership slots */
static int fixed[MAXC];        /* -1 free, 0 forced zero, 1 chosen */
static double belief[MAXC];
static int gcdtab[MAXN][MAXN];
static unsigned long long rs = 0x9E3779B97F4A7C15ULL;
static inline unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline double runif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }

/* ---- enumerate lines with >= 3 cells: canonical (primitive direction, offset) via hashing ---- */
typedef struct { long key; int start; int len; } Line;
static int *line_cells; static int nlines_cells;
static void build_factors(void) {
    /* rows and columns first */
    int cap_f = 2 * n + 4 * n * n * n / 3 + 1000;   /* generous upper bound on lines */
    fstart = malloc(sizeof(int) * (cap_f + 1)); fkind = malloc(sizeof(int) * cap_f);
    long cap_m = (long)2 * n * n + (long)8 * n * n * n; fmem = malloc(sizeof(int) * cap_m);
    nfac = 0; nmemb = 0;
    for (int u = 0; u < n; u++) { fstart[nfac] = nmemb; fkind[nfac] = 0; for (int v = 0; v < n; v++) fmem[nmemb++] = u * n + v; nfac++; }
    for (int v = 0; v < n; v++) { fstart[nfac] = nmemb; fkind[nfac] = 0; for (int u = 0; u < n; u++) fmem[nmemb++] = u * n + v; nfac++; }
    /* lines: for each primitive direction (du,dv) with du>0 or (du==0 && dv>0), excluding axes (rows/cols), enumerate lines */
    for (int du = 0; du <= m; du++) for (int dv = -m; dv <= m; dv++) {
        if (du == 0 && dv <= 0) continue;
        if (gcd(du, abs(dv)) != 1) continue;
        if (du == 0 || dv == 0) continue;               /* rows/cols already */
        /* starting cells: those with no predecessor inside the grid */
        for (int u = 0; u < n; u++) for (int v = 0; v < n; v++) {
            int pu = u - du, pv = v - dv;
            if (pu >= 0 && pu < n && pv >= 0 && pv < n) continue;
            int cnt = 0, uu = u, vv = v;
            while (uu >= 0 && uu < n && vv >= 0 && vv < n) { cnt++; uu += du; vv += dv; }
            if (cnt < 3) continue;
            if (nfac >= cap_f) { fprintf(stderr, "factor cap\n"); exit(2); }
            fstart[nfac] = nmemb; fkind[nfac] = 1;
            uu = u; vv = v;
            while (uu >= 0 && uu < n && vv >= 0 && vv < n) { fmem[nmemb++] = uu * n + vv; uu += du; vv += dv; }
            nfac++;
        }
    }
    fstart[nfac] = nmemb;
    /* cell CSR */
    cell_start = calloc(ncell + 1, sizeof(int)); cell_slots = malloc(sizeof(int) * nmemb); memb_cell = malloc(sizeof(int) * nmemb);
    for (int k = 0; k < nmemb; k++) cell_start[fmem[k] + 1]++;
    for (int c = 0; c < ncell; c++) cell_start[c + 1] += cell_start[c];
    int *fill = calloc(ncell, sizeof(int));
    for (int k = 0; k < nmemb; k++) { int c = fmem[k]; memb_cell[k] = c; cell_slots[cell_start[c] + fill[c]++] = k; }
    free(fill);
    lfv = calloc(nmemb, sizeof(double)); lvf = calloc(nmemb, sizeof(double));
}

/* one BP sweep; returns max change */
static double bp_iter(double damp) {
    double maxd = 0;
    /* variable -> factor: sum of incoming log-ratios from other factors, plus prior (0) and fixed evidence */
    for (int c = 0; c < ncell; c++) {
        double tot = 0;
        for (int s = cell_start[c]; s < cell_start[c + 1]; s++) tot += lfv[cell_slots[s]];
        double ev = fixed[c] == 1 ? 30.0 : fixed[c] == 0 ? -30.0 : 0.0;
        belief[c] = tot + ev;
        for (int s = cell_start[c]; s < cell_start[c + 1]; s++) { int k = cell_slots[s]; lvf[k] = tot - lfv[k] + ev; }
    }
    /* factor -> variable */
    static double p0[MAXC], p1[MAXC];
    for (int f = 0; f < nfac; f++) {
        int a = fstart[f], b = fstart[f + 1], len = b - a;
        if (len == 0) continue;
        /* member probabilities q_j = P(x_j = 1) from lvf */
        double A0 = 1, A1 = 0, A2 = 0, A3 = 0;       /* product polynomial coefficients up to degree 3 */
        for (int k = a; k < b; k++) {
            double l = lvf[k]; if (l > 30) l = 30; if (l < -30) l = -30;
            double q = 1.0 / (1.0 + exp(-l)), r = 1 - q;
            p1[k - a] = q; p0[k - a] = r;
            /* multiply (r + q t) */
            A3 = A3 * r + A2 * q; A2 = A2 * r + A1 * q; A1 = A1 * r + A0 * q; A0 = A0 * r;
        }
        for (int k = a; k < b; k++) {
            double q = p1[k - a], r = p0[k - a];
            /* divide out (r + q t): B0 = A0/r, B1 = (A1 - B0 q)/r, B2 = (A2 - B1 q)/r  (r > 0 guaranteed by clamp) */
            double B0, B1, B2;
            if (r > 1e-12) { B0 = A0 / r; B1 = (A1 - B0 * q) / r; B2 = (A2 - B1 * q) / r; }
            else { /* recompute directly */ B0 = 1; B1 = 0; B2 = 0; for (int j = a; j < b; j++) { if (j == k) continue; double qq = p1[j - a], rr = p0[j - a]; B2 = B2 * rr + B1 * qq; B1 = B1 * rr + B0 * qq; B0 = B0 * rr; } }
            if (B0 < 0) B0 = 0; if (B1 < 0) B1 = 0; if (B2 < 0) B2 = 0;
            double m1, m0;
            if (fkind[f] == 0) { m1 = B1; m0 = B2; }               /* exactly 2: x=1 needs others==1; x=0 needs others==2 */
            else { m1 = B0 + B1; m0 = B0 + B1 + B2; }             /* at most 2 */
            double newl = log((m1 + 1e-300) / (m0 + 1e-300));
            if (newl > 30) newl = 30; if (newl < -30) newl = -30;
            double d = fabs(newl - lfv[k]); if (d > maxd) maxd = d;
            lfv[k] = damp * lfv[k] + (1 - damp) * newl;
        }
    }
    return maxd;
}

/* hard consequences of the chosen set: shade all cells collinear with two chosen cells; full rows/cols */
static int chosen[2 * MAXN], nchosen;
static int rc[MAXN], cc[MAXN];
static int apply_hard(void) {
    for (int c = 0; c < ncell; c++) if (fixed[c] != 1) fixed[c] = -1;
    memset(rc, 0, sizeof rc); memset(cc, 0, sizeof cc);
    for (int i = 0; i < nchosen; i++) { rc[chosen[i] / n]++; cc[chosen[i] % n]++; }
    for (int u = 0; u < n; u++) if (rc[u] > 2) return 0;
    for (int v = 0; v < n; v++) if (cc[v] > 2) return 0;
    for (int i = 0; i < nchosen; i++) for (int j = i + 1; j < nchosen; j++) {
        int a = chosen[i], b = chosen[j];
        int au = a / n, av = a % n, bu = b / n, bv = b % n, du = bu - au, dv = bv - av;
        int g = gcdtab[abs(du)][abs(dv)]; du /= g; dv /= g;
        int u = au - du, v = av - dv;
        while (u >= 0 && u < n && v >= 0 && v < n) { int c = u * n + v; if (c != b) { if (fixed[c] == 1) return 0; fixed[c] = 0; } u -= du; v -= dv; }
        u = au + du; v = av + dv;
        while (u >= 0 && u < n && v >= 0 && v < n) { int c = u * n + v; if (c != b) { if (fixed[c] == 1) return 0; fixed[c] = 0; } u += du; v += dv; }
    }
    for (int c = 0; c < ncell; c++) if (fixed[c] == -1 && (rc[c / n] >= 2 || cc[c % n] >= 2)) fixed[c] = 0;
    /* feasibility: every row/col must still be able to reach 2 */
    for (int u = 0; u < n; u++) { int free_ = 0; for (int v = 0; v < n; v++) if (fixed[u * n + v] == -1) free_++; if (rc[u] + free_ < 2) return 0; }
    for (int v = 0; v < n; v++) { int free_ = 0; for (int u = 0; u < n; u++) if (fixed[u * n + v] == -1) free_++; if (cc[v] + free_ < 2) return 0; }
    return 1;
}
static void choose(int c) {
    chosen[nchosen++] = c; fixed[c] = 1;
    if (sym == 1) { int c2 = (m - c / n) * n + (m - c % n); if (c2 != c && fixed[c2] != 1) { chosen[nchosen++] = c2; fixed[c2] = 1; } }
}
static int verify(void) {
    for (int a = 0; a < nchosen; a++) for (int b = a + 1; b < nchosen; b++) for (int c = b + 1; c < nchosen; c++) {
        long ua = chosen[a] / n, va = chosen[a] % n, ub = chosen[b] / n, vb = chosen[b] % n, uc = chosen[c] / n, vc = chosen[c] % n;
        if ((ub - ua) * (vc - va) == (vb - va) * (uc - ua)) return 0;
    }
    return nchosen == 2 * n;
}
static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: bp n [seed] [iters] [damping] [restarts] [sym]\n"); return 64; }
    n = atoi(argv[1]); m = n - 1; ncell = n * n;
    unsigned long long seed = argc > 2 ? strtoull(argv[2], 0, 10) : 1;
    int iters = argc > 3 ? atoi(argv[3]) : 60;
    double damp = argc > 4 ? atof(argv[4]) : 0.5;
    int restarts = argc > 5 ? atoi(argv[5]) : 20;
    sym = argc > 6 ? atoi(argv[6]) : 0;
    rs ^= seed * 0x2545F4914F6CDD1DULL; for (int i = 0; i < 20; i++) rnd();
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = (a || b) ? gcd(a, b) : 1;
    build_factors();
    fprintf(stderr, "n=%d factors=%d memberships=%d\n", n, nfac, nmemb);
    double t0 = now();
    for (int R = 0; R < restarts; R++) {
        nchosen = 0; for (int c = 0; c < ncell; c++) fixed[c] = -1;
        for (int k = 0; k < nmemb; k++) { lfv[k] = (runif() - 0.5) * 0.2; lvf[k] = 0; }
        int ok = 1, steps = 0;
        while (nchosen < 2 * n) {
            if (!apply_hard()) { ok = 0; break; }
            for (int it = 0; it < iters; it++) { double d = bp_iter(damp); if (d < 1e-3) break; }
            /* pick the free cell with the largest belief (P(x=1)); tie-break random */
            int best = -1; double bb = -1e9;
            for (int c = 0; c < ncell; c++) if (fixed[c] == -1) { double b = belief[c] + (runif() - 0.5) * 0.01; if (b > bb) { bb = b; best = c; } }
            if (best < 0) { ok = 0; break; }
            choose(best); steps++;
        }
        if (ok && verify()) {
            qsort(chosen, nchosen, sizeof(int), cmpint);
            printf("book n=%d sym=%d seed=%llu restarts=%d secs=%.2f :", n, sym, (unsigned long long)seed, R, now() - t0);
            for (int i = 0; i < nchosen; i++) printf(" %d", chosen[i]);
            printf("\n");
            return 0;
        }
        fprintf(stderr, "restart %d: reached %d tokens (%.1fs)\n", R, nchosen, now() - t0);
    }
    printf("fail n=%d sym=%d restarts=%d secs=%.2f\n", n, sym, restarts, now() - t0);
    return 1;
}
