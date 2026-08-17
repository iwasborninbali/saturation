/* there.c — the search, at this end ("n=k: your end").
 *
 * Space: tokens t = u*n + v, registers (u, v) in 0..n-1, n <= 64.
 * Law:   no chosen triple has difference rank < 2.
 * Goal:  2n tokens — every reading class of either register holds exactly 2.
 *
 * Depth-first search with restarts, bit-parallel, one state copy per level:
 *  - alive[u] (bits v) / aliveT[v] (bits u): cells not yet shaded, occupied,
 *    or in a full class.  Every pair of chosen tokens casts a shade over all
 *    cells it aliases (a rank-1 probe through both reads them alike).
 *  - Under a symmetry of the space a cell may be chosen only with its whole
 *    orbit; "whole orbit alive" masks are derived from alive/aliveT by
 *    transposition and bit reversal, one word op per symmetry element.
 *  - Branch on the most constrained class (fewest orbit-alive cells); die if
 *    some class cannot be filled any more.  Optional one-step look-ahead and
 *    least-constraining ordering of candidates.
 *  - A failed candidate is killed for its siblings, so under a fixed symmetry
 *    the search is complete: "none" is a proof of absence in that class.
 *  - Restarts with a growing node cap until found / exhausted / time is up.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <sys/time.h>

/* portable 64-bit bit reversal: clang has a builtin, gcc does not */
#if defined(__has_builtin)
# if __has_builtin(__builtin_bitreverse64)
#  define BITREV64(x) __builtin_bitreverse64(x)
# endif
#endif
#ifndef BITREV64
static inline uint64_t bitrev64_sw(uint64_t x) {
    x = ((x >> 1) & 0x5555555555555555ULL) | ((x & 0x5555555555555555ULL) << 1);
    x = ((x >> 2) & 0x3333333333333333ULL) | ((x & 0x3333333333333333ULL) << 2);
    x = ((x >> 4) & 0x0F0F0F0F0F0F0F0FULL) | ((x & 0x0F0F0F0F0F0F0F0FULL) << 4);
    return __builtin_bswap64(x);
}
# define BITREV64(x) bitrev64_sw(x)
#endif

#ifdef BIG
#define MAXN 128
typedef unsigned __int128 bits;
#define POPCOUNT(x) (__builtin_popcountll((uint64_t)(x)) + __builtin_popcountll((uint64_t)((x) >> 64)))
#define CTZ(x) ((uint64_t)(x) ? __builtin_ctzll((uint64_t)(x)) : 64 + __builtin_ctzll((uint64_t)((x) >> 64)))
#define BITREV(x) (((bits)BITREV64((uint64_t)(x)) << 64) | (bits)BITREV64((uint64_t)((x) >> 64)))
#define WORDBITS 128
#else
#define MAXN 64
typedef uint64_t bits;
#define POPCOUNT(x) __builtin_popcountll(x)
#define CTZ(x) __builtin_ctzll(x)
#define BITREV(x) BITREV64(x)
#define WORDBITS 64
#endif
#define MAXD (2 * MAXN + 2)

typedef struct {
    bits alive[MAXN], aliveT[MAXN];
    unsigned char ucount[MAXN], vcount[MAXN];
} State;

static int n, m, sym, order, value, shave_slack = -1, enumerate_all = 0;
static uint64_t solutions;
static State st[MAXD];
static int orb[MAXN * MAXN][8], orbk[MAXN * MAXN];
static int oid[MAXN * MAXN], norb;            /* orbit id per cell, number of orbits */
static int rep[MAXN * MAXN];                  /* representative cell per orbit id */
static int *incompat[MAXN * MAXN], nincompat[MAXN * MAXN];   /* orbits that clash pairwise */
static bits *cmask, *cmaskT;                 /* per orbit: cells of clashing orbits, by row / by col */
static unsigned char selfbad[MAXN * MAXN];
static int use_compat = 1;
static int fixed[2 * MAXN], nfixed;
static unsigned char gtab[MAXN][MAXN];
static int chosen[2 * MAXN], nchosen;
static uint64_t nodes, nodecap, totalnodes, trials, depthhist[MAXD], failhist[MAXD];
static uint64_t rs = 88172645463325252ULL;
static double tlimit, t0;
static int rowseq[MAXN];

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static uint64_t rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
#define BIT(v) ((bits)1 << (v))
static bits rev(bits x) { return BITREV(x) >> (WORDBITS - n); }   /* reverse the low n bits */

/* ---- symmetry ---- */
static int img(int which, int u, int v) {
    switch (which) {
        case 0: return u * n + v;                 /* identity        */
        case 1: return v * n + (m - u);           /* quarter turn    */
        case 2: return (m - u) * n + (m - v);     /* half turn       */
        case 3: return (m - v) * n + u;           /* three quarters  */
        case 4: return (m - u) * n + v;           /* flip u          */
        case 5: return u * n + (m - v);           /* flip v          */
        case 6: return v * n + u;                 /* swap registers  */
        case 7: return (m - v) * n + (m - u);     /* anti-swap       */
    }
    return -1;
}
static const int groups[8][9] = {
    {0, -1}, {0, 2, -1}, {0, 1, 2, 3, -1}, {0, 6, -1}, {0, 4, -1},
    {0, 4, 5, 2, -1}, {0, 6, 7, 2, -1}, {0, 1, 2, 3, 4, 5, 6, 7, -1},
};
static void build_orbits(void) {
    for (int p = 0; p < n * n; p++) {
        int u = p / n, v = p % n, k = 0;
        if (sym == 8) {                       /* rct4: quarter turns off the two long axes, half turn on the main one, the other empty */
            if (u == v) { orb[p][0] = p; orb[p][1] = (m - u) * n + (m - v); k = (m - u == u) ? 1 : 2; }
            else if (u + v == m) { orb[p][0] = p; k = 1; }
            else { for (int i = 0; i < 4; i++) orb[p][i] = img(i, u, v); k = 4; }
            orbk[p] = k; continue;
        }
        for (int i = 0; groups[sym][i] >= 0; i++) {
            int q = img(groups[sym][i], u, v), dup = 0;
            for (int j = 0; j < k; j++) if (orb[p][j] == q) { dup = 1; break; }
            if (!dup) orb[p][k++] = q;
        }
        orbk[p] = k;
    }
    /* orbit ids */
    for (int p = 0; p < n * n; p++) oid[p] = -1;
    norb = 0;
    for (int p = 0; p < n * n; p++) if (oid[p] < 0) { rep[norb] = p; for (int j = 0; j < orbk[p]; j++) oid[orb[p][j]] = norb; norb++; }
}
static int degenerate3(int a, int b, int c) {
    long ua = a / n, va = a % n, ub = b / n, vb = b % n, uc = c / n, vc = c % n;
    return (ub - ua) * (vc - va) == (vb - va) * (uc - ua);
}
/* pairwise clashes between orbits: any degenerate triple inside the union,
   or more than two tokens in one reading class */
static void build_compat(void) {
    if (sym == 0) { use_compat = 0; return; }
    int *buf = malloc(sizeof(int) * norb);
    for (int a = 0; a < norb; a++) {
        int *A = orb[rep[a]], ka = orbk[rep[a]];
        selfbad[a] = 0;
        for (int i = 0; i < ka && !selfbad[a]; i++) for (int j = i + 1; j < ka && !selfbad[a]; j++) for (int l = j + 1; l < ka; l++)
            if (degenerate3(A[i], A[j], A[l])) { selfbad[a] = 1; break; }
        int cnt = 0;
        for (int b = 0; b < norb; b++) {
            if (b == a) continue;
            int *B = orb[rep[b]], kb = orbk[rep[b]], bad = 0;
            int uc[MAXN], vc[MAXN];
            memset(uc, 0, sizeof(int) * n); memset(vc, 0, sizeof(int) * n);
            for (int i = 0; i < ka; i++) { uc[A[i] / n]++; vc[A[i] % n]++; }
            for (int i = 0; i < kb; i++) { if (++uc[B[i] / n] > 2 || ++vc[B[i] % n] > 2) bad = 1; }
            for (int i = 0; i < ka && !bad; i++) for (int j = i + 1; j < ka && !bad; j++) for (int l = 0; l < kb; l++)
                if (degenerate3(A[i], A[j], B[l])) { bad = 1; break; }
            for (int i = 0; i < kb && !bad; i++) for (int j = i + 1; j < kb && !bad; j++) for (int l = 0; l < ka; l++)
                if (degenerate3(B[i], B[j], A[l])) { bad = 1; break; }
            if (bad) buf[cnt++] = b;
        }
        incompat[a] = malloc(sizeof(int) * (cnt ? cnt : 1)); memcpy(incompat[a], buf, sizeof(int) * cnt); nincompat[a] = cnt;
    }
    free(buf);
    cmask = calloc((size_t)norb * MAXN, sizeof(bits)); cmaskT = calloc((size_t)norb * MAXN, sizeof(bits));
    for (int a = 0; a < norb; a++) for (int i = 0; i < nincompat[a]; i++) {
        int b = incompat[a][i];
        for (int j = 0; j < orbk[rep[b]]; j++) { int c = orb[rep[b]][j]; cmask[(size_t)a * MAXN + c / n] |= BIT(c % n); cmaskT[(size_t)a * MAXN + c % n] |= BIT(c / n); }
    }
}
/* bits v of row u whose whole orbit is alive */
static bits orow(const State *s, int u) {
    bits r = s->alive[u];
    if (sym == 8) {
        bits r4 = r & s->aliveT[m - u] & rev(s->alive[m - u]) & rev(s->aliveT[u]);
        bits r2 = r & rev(s->alive[m - u]);
        return ((r4 & ~BIT(u)) | (r2 & BIT(u))) & ~BIT(m - u);
    }
    for (int i = 1; groups[sym][i] >= 0; i++) switch (groups[sym][i]) {
        case 1: r &= s->aliveT[m - u]; break;
        case 2: r &= rev(s->alive[m - u]); break;
        case 3: r &= rev(s->aliveT[u]); break;
        case 4: r &= s->alive[m - u]; break;
        case 5: r &= rev(s->alive[u]); break;
        case 6: r &= s->aliveT[u]; break;
        case 7: r &= rev(s->aliveT[m - u]); break;
    }
    return r;
}
/* bits u of col v whose whole orbit is alive */
static bits ocol(const State *s, int v) {
    bits r = s->aliveT[v];
    if (sym == 8) {
        bits r4 = r & rev(s->alive[v]) & rev(s->aliveT[m - v]) & s->alive[m - v];
        bits r2 = r & rev(s->aliveT[m - v]);
        return ((r4 & ~BIT(v)) | (r2 & BIT(v))) & ~BIT(m - v);
    }
    for (int i = 1; groups[sym][i] >= 0; i++) switch (groups[sym][i]) {
        case 1: r &= rev(s->alive[v]); break;
        case 2: r &= rev(s->aliveT[m - v]); break;
        case 3: r &= s->alive[m - v]; break;
        case 4: r &= rev(s->aliveT[v]); break;
        case 5: r &= s->aliveT[m - v]; break;
        case 6: r &= s->alive[v]; break;
        case 7: r &= rev(s->alive[m - v]); break;
    }
    return r;
}

/* ---- state ops ---- */
#define KILL(s, u, v) do { (s)->alive[u] &= ~BIT(v); (s)->aliveT[v] &= ~BIT(u); } while (0)
static void shade_pair(State *s, int p, int q) {
    int u1 = p / n, v1 = p % n, u2 = q / n, v2 = q % n;
    int du = u2 - u1, dv = v2 - v1, g = gtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    int u = u1 - du, v = v1 - dv;
    while ((unsigned)u < (unsigned)n && (unsigned)v < (unsigned)n) { KILL(s, u, v); u -= du; v -= dv; }
    u = u1 + du; v = v1 + dv;
    while ((unsigned)u < (unsigned)n && (unsigned)v < (unsigned)n) { KILL(s, u, v); u += du; v += dv; }
}
static int legal(const State *s, int p) {
    return (s->alive[p / n] & BIT(p % n)) && s->ucount[p / n] < 2 && s->vcount[p % n] < 2;
}
static void take(State *s, int p) {
    int u = p / n, v = p % n;
    for (int i = 0; i < nchosen; i++) shade_pair(s, p, chosen[i]);
    KILL(s, u, v);
    if (++s->ucount[u] == 2) { s->alive[u] = 0; for (int j = 0; j < n; j++) s->aliveT[j] &= ~BIT(u); }
    if (++s->vcount[v] == 2) { s->aliveT[v] = 0; for (int j = 0; j < n; j++) s->alive[j] &= ~BIT(v); }
    chosen[nchosen++] = p;
}
static void kill_orbit(State *s, int p);
static int take_orbit(State *s, int p) {   /* into a scratch copy; 0 if impossible */
    for (int j = 0; j < orbk[p]; j++) {
        if (!legal(s, orb[p][j])) return 0;
        take(s, orb[p][j]);
    }
    if (use_compat) { int a = oid[p]; const bits *cm = cmask + (size_t)a * MAXN, *cmT = cmaskT + (size_t)a * MAXN;
        for (int u = 0; u < n; u++) { s->alive[u] &= ~cm[u]; s->aliveT[u] &= ~cmT[u]; } }
    return 1;
}
static int feasible(const State *s) {
    for (int u = 0; u < n; u++) if (s->ucount[u] < 2 && POPCOUNT(orow(s, u)) < 2 - s->ucount[u]) return 0;
    for (int v = 0; v < n; v++) if (s->vcount[v] < 2 && POPCOUNT(ocol(s, v)) < 2 - s->vcount[v]) return 0;
    return 1;
}
static long alive_total(const State *s) {
    long t = 0; for (int u = 0; u < n; u++) if (s->ucount[u] < 2) t += POPCOUNT(orow(s, u)); return t;
}
static void kill_orbit(State *s, int p) {
    for (int j = 0; j < orbk[p]; j++) { int c = orb[p][j]; KILL(s, c / n, c % n); }
}

static int cmp(const void *a, const void *b);

/* ---- shaving: in small classes, drop candidates that die one step ahead ---- */
static int shave(int lv) {
    State *s = &st[lv];
    int saved = nchosen, changed = 1, rounds = 0;
    while (changed && rounds++ < 8) {
        changed = 0;
        for (int cls = 0; cls < 2 * n; cls++) {
            int need, cnt; bits b;
            if (cls < n) { need = 2 - s->ucount[cls]; if (need <= 0) continue; b = orow(s, cls); }
            else         { need = 2 - s->vcount[cls - n]; if (need <= 0) continue; b = ocol(s, cls - n); }
            cnt = POPCOUNT(b);
            if (cnt < need) return 0;
            if (cnt > need + shave_slack) continue;
            while (b) {
                int i = CTZ(b); b &= b - 1;
                int c = cls < n ? cls * n + i : i * n + (cls - n);
                State *t = &st[lv + 1]; *t = *s;
                int ok = take_orbit(t, c) && feasible(t);
                nchosen = saved;
                if (!ok) { kill_orbit(s, c); changed = 1; if (--cnt < need) return 0; }
            }
        }
    }
    return 1;
}

/* ---- search ---- */
static int search(int lv) {
    State *s = &st[lv];
    depthhist[lv]++;
    if (++nodes > nodecap) return -1;
    if (nchosen == 2 * n) {
        if (!enumerate_all) return 1;
        solutions++;
        if (getenv("PRINTALL")) { int b[2 * MAXN]; memcpy(b, chosen, sizeof(int) * nchosen); qsort(b, nchosen, sizeof(int), cmp);
            printf("sol"); for (int i = 0; i < nchosen; i++) printf(" %d", b[i]); printf("\n"); }
        return 0;
    }
    if (shave_slack >= 0 && !shave(lv)) return 0;

    int best = -1, bestcnt = 1 << 30, ties = 0;
    if (order >= 2) {
        for (int i = 0; i < n; i++) if (s->ucount[rowseq[i]] < 2) { best = rowseq[i]; break; }
    } else {
        for (int u = 0; u < n; u++) {
            if (s->ucount[u] == 2) continue;
            int cnt = POPCOUNT(orow(s, u));
            if (cnt < bestcnt) { bestcnt = cnt; best = u; ties = 1; }
            else if (cnt == bestcnt && rnd() % ++ties == 0) best = u;
        }
        if (order == 0) for (int v = 0; v < n; v++) {
            if (s->vcount[v] == 2) continue;
            int cnt = POPCOUNT(ocol(s, v));
            if (cnt < bestcnt) { bestcnt = cnt; best = n + v; ties = 1; }
            else if (cnt == bestcnt && rnd() % ++ties == 0) best = n + v;
        }
    }
    if (best < 0) return 0;

    int cand[MAXN], nc = 0;
    if (best < n) { bits b = orow(s, best); while (b) { int v = CTZ(b); b &= b - 1; cand[nc++] = best * n + v; } }
    else          { bits b = ocol(s, best - n); while (b) { int u = CTZ(b); b &= b - 1; cand[nc++] = u * n + best - n; } }
    for (int i = nc - 1; i > 0; i--) { int j = rnd() % (i + 1), t = cand[i]; cand[i] = cand[j]; cand[j] = t; }

    int saved = nchosen;
    if (value) {                              /* look ahead once, then sort */
        long score[MAXN]; int keep[MAXN], nk = 0;
        for (int i = 0; i < nc; i++) {
            State *t = &st[lv + 1]; *t = *s;
            long sc = -1;
            if (take_orbit(t, cand[i]) && feasible(t)) sc = alive_total(t);
            nchosen = saved;
            if (sc < 0) kill_orbit(s, cand[i]);
            else { keep[nk] = cand[i]; score[nk] = (value == 1 ? sc : -sc) * 4 + (long)(rnd() % 4); nk++; }
        }
        for (int i = 1; i < nk; i++) {        /* insertion sort, descending score */
            int c = keep[i]; long sc = score[i], j = i - 1;
            while (j >= 0 && score[j] < sc) { keep[j + 1] = keep[j]; score[j + 1] = score[j]; j--; }
            keep[j + 1] = c; score[j + 1] = sc;
        }
        nc = nk; for (int i = 0; i < nc; i++) cand[i] = keep[i];
    }
    for (int i = 0; i < nc; i++) {
        int c = cand[i];
        if (orow(s, c / n) & BIT(c % n)) {    /* siblings' kills may have removed it */
            State *t = &st[lv + 1]; *t = *s; trials++;
            if (take_orbit(t, c) && feasible(t)) {
                int r = search(lv + 1);
                if (r == 0) failhist[lv + 1]++;
                if (r == 1) return 1;         /* keep the book in chosen[] */
                if (r < 0) return r;          /* aborted; caller resets */
            }
            nchosen = saved;
        }
        kill_orbit(s, c);
    }
    return 0;
}

static void reset(void) {
    State *s = &st[0];
    for (int u = 0; u < n; u++) { s->alive[u] = s->aliveT[u] = (n == WORDBITS ? ~(bits)0 : (BIT(n) - 1)); s->ucount[u] = s->vcount[u] = 0; }
    if (use_compat) for (int a = 0; a < norb; a++) if (selfbad[a]) kill_orbit(s, rep[a]);
    if (sym == 8) for (int u = 0; u < n; u++) KILL(s, u, m - u);
    nchosen = 0; nodes = 0;
    for (int i = 0; i < nfixed; i++) {
        int p = fixed[i];
        if (s->alive[p / n] & BIT(p % n)) { if (!take_orbit(s, p)) { fprintf(stderr, "fixed token %d cannot be taken\n", p); exit(65); } }
        else { int j; for (j = 0; j < nchosen; j++) if (chosen[j] == p) break; if (j == nchosen) { fprintf(stderr, "fixed token %d is dead\n", p); exit(65); } }
    }
}
static int verify(void) {                 /* independent triple check, exact integers */
    for (int a = 0; a < nchosen; a++) for (int b = a + 1; b < nchosen; b++) for (int c = b + 1; c < nchosen; c++) {
        long ua = chosen[a] / n, va = chosen[a] % n, ub = chosen[b] / n, vb = chosen[b] % n, uc = chosen[c] / n, vc = chosen[c] % n;
        if ((ub - ua) * (vc - va) == (vb - va) * (uc - ua)) return 0;
    }
    return nchosen == 2 * n;
}
static int cmp(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: there n sym [seed] [seconds] [cap0] [order] [value] [growth%%] [shave]\n"); return 64; }
    n = atoi(argv[1]); m = n - 1; sym = atoi(argv[2]);
    uint64_t seed = argc > 3 ? strtoull(argv[3], 0, 10) : 1;
    tlimit = argc > 4 ? atof(argv[4]) : 60.0;
    nodecap = argc > 5 ? strtoull(argv[5], 0, 10) : 2000;
    order = argc > 6 ? atoi(argv[6]) : 0;
    value = argc > 7 ? atoi(argv[7]) : 0;
    int growth = argc > 8 ? atoi(argv[8]) : 50;
    shave_slack = argc > 9 ? atoi(argv[9]) : -1;
    enumerate_all = getenv("ALL") != NULL; if (enumerate_all) nodecap = ~(uint64_t)0 >> 1;
    if (n < 2 || n > MAXN || sym < 0 || sym > 8) return 64;
    if (sym == 8 && !(n & 1)) { printf("skip n=%d sym=8: rct4 is for odd n\n", n); return 3; }
    if (getenv("FIX")) { FILE *f = fopen(getenv("FIX"), "r"); int x; while (f && fscanf(f, "%d", &x) == 1) fixed[nfixed++] = x; if (f) fclose(f); }
    if ((sym == 2 || sym == 4 || sym == 5 || sym == 7) && (n & 1)) {
        printf("skip n=%d sym=%d: impossible for odd n\n", n, sym); return 3;
    }
    build_orbits();
    if (getenv("NOCOMPAT")) use_compat = 0;
    build_compat();
    for (int a = 0; a < MAXN; a++) for (int b = 0; b < MAXN; b++) gtab[a][b] = (a || b) ? gcd(a, b) : 1;
    for (int i = 0; i < n; i++) rowseq[i] = i;
    if (order == 3) { int k = 0; for (int d = 0; k < n; d++) { int a = (n - 1) / 2 - d, b = n / 2 + d; if (a >= 0) rowseq[k++] = a; if (b < n && b != a) rowseq[k++] = b; } }
    if (order == 4) { int k = 0; for (int d = 0; k < n; d++) { rowseq[k++] = d; if (m - d != d) rowseq[k++] = m - d; } }
    rs ^= seed * 0x9E3779B97F4A7C15ULL; for (int i = 0; i < 20; i++) rnd();
    t0 = now();
    int restarts = 0;
    for (;;) {
        reset();
        int r = search(0);
        totalnodes += nodes;
        if (r == 1) {
            if (!verify()) { printf("BUG n=%d sym=%d\n", n, sym); return 70; }
            qsort(chosen, nchosen, sizeof(int), cmp);
            printf("book n=%d sym=%d seed=%llu order=%d value=%d shave=%d restarts=%d nodes=%llu secs=%.2f :",
                   n, sym, (unsigned long long)seed, order, value, shave_slack, restarts, (unsigned long long)totalnodes, now() - t0);
            for (int i = 0; i < nchosen; i++) printf(" %d", chosen[i]);
            printf("\n");
            return 0;
        }
        if (r == 0) {
            if (enumerate_all) { printf("all n=%d sym=%d: solutions=%llu nodes=%llu secs=%.2f\n", n, sym, (unsigned long long)solutions, (unsigned long long)totalnodes, now() - t0); return solutions ? 0 : 2; }
            printf("none n=%d sym=%d: exhausted (no book with this symmetry) nodes=%llu secs=%.2f\n",
                   n, sym, (unsigned long long)totalnodes, now() - t0);
            return 2;
        }
        restarts++;
        nodecap = nodecap + nodecap * growth / 100;
        if (now() - t0 > tlimit) {
            printf("timeout n=%d sym=%d order=%d value=%d shave=%d restarts=%d nodes=%llu trials=%llu secs=%.2f\n",
                   n, sym, order, value, shave_slack, restarts, (unsigned long long)totalnodes, (unsigned long long)trials, now() - t0);
            if (getenv("HIST")) for (int d = 0; d < MAXD && depthhist[d]; d++) printf("  depth %2d: nodes=%llu failed_children=%llu\n", d, (unsigned long long)depthhist[d], (unsigned long long)failhist[d]);
            return 1;
        }
    }
}
