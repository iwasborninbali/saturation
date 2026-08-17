/* fast/polish.c — exact (r, r+1)-swap search on a LAWFUL book, r = 1, 2, 3.
 * Remove r tokens, add r+1 mutually compatible cells that were blocked only by the removed
 * tokens. Repeats until no such swap exists (then the book is (r,r+1)-swap-optimal for the
 * chosen r). Only proposes; solve.py re-enters the result through saturation.the_law.
 *
 * usage: polish n tokenfile outfile [maxr] [seconds]
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#define MAXN 128
#define MAXC (MAXN * MAXN)
#define MAXK (2 * MAXN + 8)

static int n, m;
static int occ[MAXC], plist[MAXK], pos[MAXC], np;
static int rc[MAXN], cc[MAXN];
static int F[MAXC];
static int gcdtab[MAXN][MAXN];
static int W;
static int dirtab_du[(2 * MAXN - 1) * (2 * MAXN - 1)], dirtab_dv[(2 * MAXN - 1) * (2 * MAXN - 1)];

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

static inline void walk(int a, int b, int d) {
    int au = a / n, av = a % n, bu = b / n, bv = b % n;
    int du = bu - au, dv = bv - av;
    int g = gcdtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    int u = au, v = av;
    while (u - du >= 0 && u - du <= m && v - dv >= 0 && v - dv <= m) { u -= du; v -= dv; }
    while (u >= 0 && u <= m && v >= 0 && v <= m) { F[u * n + v] += d; u += du; v += dv; }
}
static void add_point(int c) {
    for (int i = 0; i < np; i++) walk(c, plist[i], +1);
    occ[c] = 1; pos[c] = np; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static void del_point(int c) {
    int i = pos[c], last = plist[--np];
    plist[i] = last; pos[last] = i; occ[c] = 0; rc[c / n]--; cc[c % n]--;
    for (int k = 0; k < np; k++) walk(c, plist[k], -1);
}
static inline int collinear(int a, int b, int c) {
    long ua = a / n, va = a % n, ub = b / n, vb = b % n, uc = c / n, vc = c % n;
    return (ub - ua) * (vc - va) == (vb - va) * (uc - ua);
}
/* the state pairs collinear with free cell c: fills pairs[][2], returns count (<= cap) */
static int pairs_through(int c, int (*pairs)[2], int cap) {
    static int cnt[(2 * MAXN - 1) * (2 * MAXN - 1)], first[(2 * MAXN - 1) * (2 * MAXN - 1)];
    static int touched[MAXK];
    int u = c / n, v = c % n, nt = 0, k = 0;
    for (int i = 0; i < np; i++) {
        int q = plist[i];
        int du = q / n - u, dv = q % n - v;
        int g = gcdtab[abs(du)][abs(dv)]; du /= g; dv /= g;
        if (du < 0 || (du == 0 && dv < 0)) { du = -du; dv = -dv; }
        int d = (du + m) * W + (dv + m);
        if (cnt[d] == 0) { touched[nt++] = d; first[d] = q; }
        else { /* every earlier point in this direction pairs with q */
            /* to enumerate all pairs we need all earlier points; keep it simple: only up to 3 points/direction */
        }
        cnt[d]++;
    }
    /* second pass: collect pairs (all combinations per direction) */
    for (int t = 0; t < nt; t++) {
        int d = touched[t];
        if (cnt[d] >= 2) {
            int du = d / W - m, dv = d % W - m;
            int mem[8], nm = 0;
            for (int i = 0; i < np && nm < 8; i++) {
                int q = plist[i]; int eu = q / n - u, ev = q % n - v;
                int g = gcdtab[abs(eu)][abs(ev)]; eu /= g; ev /= g;
                if (eu < 0 || (eu == 0 && ev < 0)) { eu = -eu; ev = -ev; }
                if (eu == du && ev == dv) mem[nm++] = q;
            }
            for (int i = 0; i < nm; i++) for (int j = i + 1; j < nm; j++) if (k < cap) { pairs[k][0] = mem[i]; pairs[k][1] = mem[j]; k++; }
        }
        cnt[d] = 0;
    }
    return k;
}

/* candidate cell record */
typedef struct { int cell; int npairs; int pairs[4][2]; } Cand;
static Cand cands[MAXC]; static int ncands;

static int released_by(const Cand *cd, const int *rem, int nrem) {   /* every pair of cd meets rem */
    for (int p = 0; p < cd->npairs; p++) {
        int hit = 0;
        for (int i = 0; i < nrem; i++) if (cd->pairs[p][0] == rem[i] || cd->pairs[p][1] == rem[i]) hit = 1;
        if (!hit) return 0;
    }
    return 1;
}
static int in_rem(int q, const int *rem, int nrem) { for (int i = 0; i < nrem; i++) if (rem[i] == q) return 1; return 0; }

/* are the new cells (already known to be individually released) mutually compatible given rem removed? */
static int compatible(const int *cells, int nc, const int *rem, int nrem) {
    /* capacities */
    for (int i = 0; i < nc; i++) {
        int u = cells[i] / n, v = cells[i] % n, ru = rc[u], cv = cc[v];
        for (int k = 0; k < nrem; k++) { if (rem[k] / n == u) ru--; if (rem[k] % n == v) cv--; }
        for (int j = 0; j < nc; j++) { if (cells[j] / n == u) ru++; if (cells[j] % n == v) cv++; }
        if (ru > 2 || cv > 2) return 0;
    }
    /* no line through two new cells contains a remaining state point or a third new cell */
    for (int i = 0; i < nc; i++) for (int j = i + 1; j < nc; j++) {
        for (int k = 0; k < nc; k++) if (k != i && k != j && collinear(cells[i], cells[j], cells[k])) return 0;
        for (int t = 0; t < np; t++) { int q = plist[t]; if (in_rem(q, rem, nrem)) continue; if (collinear(cells[i], cells[j], q)) return 0; }
    }
    return 1;
}
static void apply_swap(const int *rem, int nrem, const int *cells, int nc) {
    for (int i = 0; i < nrem; i++) del_point(rem[i]);
    for (int i = 0; i < nc; i++) add_point(cells[i]);
}
static int lawful_check(void) {
    for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) for (int k = j + 1; k < np; k++)
        if (collinear(plist[i], plist[j], plist[k])) return 0;
    return 1;
}
static void write_tokens(const char *path) {
    FILE *f = fopen(path, "w"); if (!f) return;
    int tmp[MAXK]; for (int i = 0; i < np; i++) tmp[i] = plist[i];
    qsort(tmp, np, sizeof(int), cmpint);
    for (int i = 0; i < np; i++) fprintf(f, "%d%c", tmp[i], i + 1 < np ? ' ' : '\n');
    fclose(f);
}
/* build candidate list: free cells with 1 <= F <= maxF and capacity-plausible */
static void build_cands(int maxF) {
    ncands = 0;
    for (int c = 0; c < n * n; c++) {
        if (occ[c] || F[c] == 0 || F[c] > maxF) continue;
        Cand *cd = &cands[ncands];
        cd->cell = c;
        cd->npairs = pairs_through(c, cd->pairs, 4);
        if (cd->npairs != F[c] || cd->npairs > 4) continue;   /* skip degenerate cases */
        ncands++;
    }
}
static int fill_free(void) {
    int added = 0, changed = 1;
    while (changed) {
        changed = 0;
        for (int c = 0; c < n * n; c++) if (!occ[c] && F[c] == 0 && rc[c / n] < 2 && cc[c % n] < 2) { add_point(c); added++; changed = 1; }
    }
    return added;
}
/* try all (r, r+1) swaps for the given r; returns 1 if applied one */
static int try_swaps(int r, double deadline) {
    build_cands(r);
    /* index: for each state point, candidates that mention it */
    static int idx[MAXC][64]; static int nidx[MAXC];
    for (int i = 0; i < np; i++) nidx[plist[i]] = 0;
    for (int i = 0; i < ncands; i++) for (int p = 0; p < cands[i].npairs; p++) for (int s = 0; s < 2; s++) {
        int q = cands[i].pairs[p][s];
        int dup = 0; for (int t = 0; t < nidx[q]; t++) if (idx[q][t] == i) dup = 1;
        if (!dup && nidx[q] < 64) idx[q][nidx[q]++] = i;
    }
    int rem[3], pool[256], npool;
    int cells[4];
    if (r == 1) {
        for (int a = 0; a < np; a++) {
            rem[0] = plist[a];
            npool = 0;
            for (int t = 0; t < nidx[rem[0]]; t++) { int i = idx[rem[0]][t]; if (released_by(&cands[i], rem, 1)) pool[npool++] = cands[i].cell; }
            for (int i = 0; i < npool; i++) for (int j = i + 1; j < npool; j++) {
                cells[0] = pool[i]; cells[1] = pool[j];
                if (compatible(cells, 2, rem, 1)) { apply_swap(rem, 1, cells, 2); return 1; }
            }
        }
        return 0;
    }
    if (r == 2) {
        for (int a = 0; a < np; a++) for (int b = a + 1; b < np; b++) {
            if (now() > deadline) return 0;
            rem[0] = plist[a]; rem[1] = plist[b];
            npool = 0;
            for (int s = 0; s < 2; s++) for (int t = 0; t < nidx[rem[s]]; t++) {
                int i = idx[rem[s]][t];
                int dup = 0; for (int x = 0; x < npool; x++) if (pool[x] == cands[i].cell) dup = 1;
                if (!dup && npool < 256 && released_by(&cands[i], rem, 2)) pool[npool++] = cands[i].cell;
            }
            if (npool < 3) continue;
            for (int i = 0; i < npool; i++) for (int j = i + 1; j < npool; j++) {
                cells[0] = pool[i]; cells[1] = pool[j];
                if (!compatible(cells, 2, rem, 2)) continue;
                for (int k = j + 1; k < npool; k++) {
                    cells[2] = pool[k];
                    if (compatible(cells, 3, rem, 2)) { apply_swap(rem, 2, cells, 3); return 1; }
                }
            }
        }
        return 0;
    }
    if (r == 3) {
        for (int a = 0; a < np; a++) for (int b = a + 1; b < np; b++) for (int c = b + 1; c < np; c++) {
            if (now() > deadline) return 0;
            rem[0] = plist[a]; rem[1] = plist[b]; rem[2] = plist[c];
            npool = 0;
            for (int s = 0; s < 3; s++) for (int t = 0; t < nidx[rem[s]]; t++) {
                int i = idx[rem[s]][t];
                int dup = 0; for (int x = 0; x < npool; x++) if (pool[x] == cands[i].cell) dup = 1;
                if (!dup && npool < 256 && released_by(&cands[i], rem, 3)) pool[npool++] = cands[i].cell;
            }
            if (npool < 4) continue;
            for (int i = 0; i < npool; i++) for (int j = i + 1; j < npool; j++) {
                cells[0] = pool[i]; cells[1] = pool[j];
                if (!compatible(cells, 2, rem, 3)) continue;
                for (int k = j + 1; k < npool; k++) {
                    cells[2] = pool[k];
                    if (!compatible(cells, 3, rem, 3)) continue;
                    for (int l = k + 1; l < npool; l++) {
                        cells[3] = pool[l];
                        if (compatible(cells, 4, rem, 3)) { apply_swap(rem, 3, cells, 4); return 1; }
                    }
                }
            }
        }
        return 0;
    }
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 4) { fprintf(stderr, "usage: polish n tokenfile outfile [maxr] [seconds]\n"); return 2; }
    n = atoi(argv[1]); m = n - 1; W = 2 * n - 1;
    int maxr = argc > 4 ? atoi(argv[4]) : 2;
    double seconds = argc > 5 ? atof(argv[5]) : 600;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = gcd(a, b);
    FILE *f = fopen(argv[2], "r"); if (!f) { fprintf(stderr, "cannot open\n"); return 2; }
    int t;
    while (fscanf(f, "%d", &t) == 1) if (t >= 0 && t < n * n && !occ[t]) add_point(t);
    fclose(f);
    if (!lawful_check()) { fprintf(stderr, "input not lawful\n"); return 3; }
    int start = np;
    double deadline = now() + seconds;
    fprintf(stderr, "start: %d tokens\n", np);
    int improved = 1;
    while (improved && now() < deadline) {
        improved = 0;
        int a = fill_free();
        if (a) { fprintf(stderr, "fill +%d -> %d\n", a, np); improved = 1; continue; }
        for (int r = 1; r <= maxr; r++) {
            if (try_swaps(r, deadline)) { fprintf(stderr, "(%d,%d)-swap -> %d tokens\n", r, r + 1, np); improved = 1; break; }
        }
    }
    if (!lawful_check()) { fprintf(stderr, "BUG: result not lawful\n"); return 3; }
    write_tokens(argv[3]);
    printf("POLISH start=%d end=%d maxr=%d complete=%d\n", start, np, maxr, now() < deadline);
    return 0;
}
