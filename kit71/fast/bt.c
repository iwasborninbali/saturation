/* fast/bt.c — exhaustive backtracking for saturated books (2n tokens, no three collinear)
 * fixed under a chosen subgroup of the 8 motions. Row by row: the first incomplete row gets its
 * missing tokens in increasing column order; each token drags its whole orbit; a cell is
 * forbidden when it is collinear with two chosen tokens (field F > 0). Prunes on rows/columns
 * that cannot reach 2 tokens. Prints every solution as a token list, and the trace numbers
 * (nodes, solutions, seconds) needed to replay the exhaustion.
 *
 * usage: bt n group [maxseconds] [maxsolutions] [order]
 *   group: id | rot2 | diag | adiag | v2 | h | v | hv | c4 | d4
 *   order: 0 = rows 0..n-1, 1 = outside-in (0, n-1, 1, n-2, ...)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/time.h>

#define MAXN 96
#define MAXC (MAXN * MAXN)
#define MAXK (2 * MAXN + 8)

static int n, m, G;
static int orb[MAXC][8], orbsz[MAXC], orbrep[MAXC];
static int occ[MAXC], plist[MAXK], np;
static int rc[MAXN], cc[MAXN];
static int F[MAXC];
static int gcdtab[MAXN][MAXN];
static int roworder[MAXN];
static long long nodes = 0, sols = 0, maxsols = -1;
static double maxsec = 1e18, t0;
static int timed_out = 0;

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static int gcd(int a, int b) { while (b) { int t = a % b; a = b; b = t; } return a; }
static int cmpint(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }

static void motion(int g, int u, int v, int *pu, int *pv) {
    switch (g) {
        case 0: *pu = u; *pv = v; break;
        case 1: *pu = v; *pv = m - u; break;
        case 2: *pu = m - u; *pv = m - v; break;
        case 3: *pu = m - v; *pv = u; break;
        case 4: *pu = v; *pv = u; break;
        case 5: *pu = m - u; *pv = v; break;
        case 6: *pu = u; *pv = m - v; break;
        default: *pu = m - v; *pv = m - u; break;
    }
}
static void build_group(const char *name) {
    int gl[8], k = 0;
    if (!strcmp(name, "id")) { gl[k++] = 0; }
    else if (!strcmp(name, "rot2")) { gl[k++] = 0; gl[k++] = 2; }
    else if (!strcmp(name, "diag")) { gl[k++] = 0; gl[k++] = 4; }
    else if (!strcmp(name, "adiag")) { gl[k++] = 0; gl[k++] = 7; }
    else if (!strcmp(name, "v2")) { gl[k++] = 0; gl[k++] = 2; gl[k++] = 4; gl[k++] = 7; }
    else if (!strcmp(name, "h")) { gl[k++] = 0; gl[k++] = 5; }
    else if (!strcmp(name, "v")) { gl[k++] = 0; gl[k++] = 6; }
    else if (!strcmp(name, "hv")) { gl[k++] = 0; gl[k++] = 2; gl[k++] = 5; gl[k++] = 6; }
    else if (!strcmp(name, "c4")) { gl[k++] = 0; gl[k++] = 1; gl[k++] = 2; gl[k++] = 3; }
    else if (!strcmp(name, "d4")) { for (int i = 0; i < 8; i++) gl[k++] = i; }
    else { fprintf(stderr, "unknown group %s\n", name); exit(2); }
    G = k;
    for (int c = 0; c < n * n; c++) {
        int u = c / n, v = c % n, tmp[8], t = 0;
        for (int i = 0; i < G; i++) {
            int uu, vv; motion(gl[i], u, v, &uu, &vv);
            int x = uu * n + vv, dup = 0;
            for (int j = 0; j < t; j++) if (tmp[j] == x) dup = 1;
            if (!dup) tmp[t++] = x;
        }
        qsort(tmp, t, sizeof(int), cmpint);
        orbsz[c] = t; for (int j = 0; j < t; j++) orb[c][j] = tmp[j]; orbrep[c] = tmp[0];
    }
}
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
    occ[c] = 1; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static void del_point(int c) {          /* c must be the last added */
    np--; occ[c] = 0; rc[c / n]--; cc[c % n]--;
    for (int i = 0; i < np; i++) walk(c, plist[i], -1);
}
/* place orbit r if all its cells are free, unforbidden, and capacities hold; returns cells placed (0 = fail) */
static int place_orbit(int r) {
    int k = orbsz[r];
    for (int j = 0; j < k; j++) {
        int c = orb[r][j];
        if (occ[c] || F[c] > 0 || rc[c / n] >= 2 || cc[c % n] >= 2) {
            for (int i = j - 1; i >= 0; i--) del_point(orb[r][i]);
            return 0;
        }
        add_point(c);
    }
    return k;
}
static void unplace_orbit(int r) { for (int j = orbsz[r] - 1; j >= 0; j--) del_point(orb[r][j]); }

/* every row/column must still be able to reach 2 tokens */
static int feasible(void) {
    for (int u = 0; u < n; u++) {
        int need = 2 - rc[u];
        if (need <= 0) continue;
        int avail = 0;
        for (int v = 0; v < n && avail < need; v++) {
            int c = u * n + v;
            if (!occ[c] && F[c] == 0 && cc[v] < 2) avail++;
        }
        if (avail < need) return 0;
    }
    for (int v = 0; v < n; v++) {
        int need = 2 - cc[v];
        if (need <= 0) continue;
        int avail = 0;
        for (int u = 0; u < n && avail < need; u++) {
            int c = u * n + v;
            if (!occ[c] && F[c] == 0 && rc[u] < 2) avail++;
        }
        if (avail < need) return 0;
    }
    return 1;
}
static void print_solution(void) {
    int tmp[MAXK]; for (int i = 0; i < np; i++) tmp[i] = plist[i];
    qsort(tmp, np, sizeof(int), cmpint);
    printf("SOL");
    for (int i = 0; i < np; i++) printf(" %d", tmp[i]);
    printf("\n"); fflush(stdout);
}
static void dfs(void) {
    nodes++;
    if ((nodes & 0xFFFF) == 0) {
        if (now() - t0 > maxsec) { timed_out = 1; }
    }
    if (timed_out) return;
    if (np == 2 * n) { sols++; print_solution(); return; }
    /* first incomplete row in the chosen order */
    int u = -1;
    for (int i = 0; i < n; i++) if (rc[roworder[i]] < 2) { u = roworder[i]; break; }
    if (u < 0) return;
    if (!feasible()) return;
    /* explicit choices in row u in increasing column order: the last explicit column is tracked
       via a static per-depth stack (lastv) */
    static int lastv[MAXK]; static int depth = 0;
    int start = (depth > 0 && lastv[depth - 1] / n == u) ? lastv[depth - 1] % n + 1 : 0;
    for (int v = start; v < n; v++) {
        int c = u * n + v;
        if (occ[c] || F[c] > 0 || cc[v] >= 2) continue;
        int r = orbrep[c];
        /* orbit rep must be this cell's orbit; the explicit token is c itself; skip if some orbit cell in row u has a smaller column
           than v and is not yet placed (it would be the explicit choice instead) — handled by ordering: allowed only if c is the
           smallest-column cell of its orbit within row u among cells not yet occupied */
        int ok = 1;
        for (int j = 0; j < orbsz[r]; j++) { int cc2 = orb[r][j]; if (cc2 / n == u && cc2 % n < v && !occ[cc2]) ok = 0; }
        if (!ok) continue;
        if (!place_orbit(r)) continue;
        lastv[depth] = c; depth++;
        dfs();
        depth--;
        unplace_orbit(r);
        if (timed_out) return;
        if (maxsols >= 0 && sols >= maxsols) return;
    }
}

int main(int argc, char **argv) {
    if (argc < 3) { fprintf(stderr, "usage: bt n group [maxseconds] [maxsolutions] [order]\n"); return 2; }
    n = atoi(argv[1]); m = n - 1;
    const char *gname = argv[2];
    if (argc > 3) maxsec = atof(argv[3]);
    if (argc > 4) maxsols = atoll(argv[4]);
    int order = argc > 5 ? atoi(argv[5]) : 0;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = gcd(a, b);
    build_group(gname);
    if (order == 0) { for (int i = 0; i < n; i++) roworder[i] = i; }
    else { int lo = 0, hi = n - 1, i = 0; while (lo <= hi) { roworder[i++] = lo++; if (lo <= hi) roworder[i++] = hi--; } }
    t0 = now();
    dfs();
    double el = now() - t0;
    printf("TRACE n=%d group=%s order=%d nodes=%lld solutions=%lld seconds=%.2f complete=%d\n",
           n, gname, order, nodes, sols, el, !timed_out && (maxsols < 0 || sols < maxsols));
    return 0;
}
