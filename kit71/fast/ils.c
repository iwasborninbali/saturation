/* fast/ils.c — iterated local search on LAWFUL books: (1,k)-orbit swaps on the field F.
 *
 * Law (saturation.py): no three chosen tokens collinear. State: union of orbits under a
 * subgroup of the 8 motions, <= 2 tokens per row/column. Cost = number of collinear triples.
 * Field: F[c] = number of unordered pairs {Q,R} of state tokens whose line passes through
 * cell c (for c in the state, F[c] = T(c) + (np-1)). Maintained by walking lines.
 * This program only PROPOSES; solve.py re-enters every book through the law.
 *
 * usage: ils n group seed seconds kick_every outprefix [startfile]
 *   kick_every: plateau steps without improvement before a perturbation kick
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>

#define MAXN 128
#define MAXC (MAXN * MAXN)
#define MAXK (2 * MAXN + 8)

static int n, m, G;
static int orb[MAXC][8], orbsz[MAXC], orbrep[MAXC];
static int occ[MAXC], plist[MAXK], pos[MAXC], np;
static int rc[MAXN], cc[MAXN];
static long conf;
static int F[MAXC];
static int reps[MAXK], nreps, repidx[MAXC];
static int gcdtab[MAXN][MAXN];

static double now(void) { struct timeval tv; gettimeofday(&tv, NULL); return tv.tv_sec + tv.tv_usec * 1e-6; }
static unsigned long long rs;
static inline unsigned long long rnd(void) { rs ^= rs << 13; rs ^= rs >> 7; rs ^= rs << 17; return rs; }
static inline int rint_(int k) { return (int)(rnd() % (unsigned long long)k); }
static inline double runif(void) { return (rnd() >> 11) * (1.0 / 9007199254740992.0); }
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

/* walk the line through cells a and b (a != b), adding d to F on every grid cell of it */
static inline void walk(int a, int b, int d) {
    int au = a / n, av = a % n, bu = b / n, bv = b % n;
    int du = bu - au, dv = bv - av;
    int g = gcdtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    /* find the first cell of the line inside the grid: go backwards from a */
    int u = au, v = av;
    while (u - du >= 0 && u - du <= m && v - dv >= 0 && v - dv <= m) { u -= du; v -= dv; }
    while (u >= 0 && u <= m && v >= 0 && v <= m) { F[u * n + v] += d; u += du; v += dv; }
}

static inline int T_of(int c) { return F[c] - (np - 1); }   /* c in state */

static void add_point(int c) {                 /* c not in state */
    conf += F[c];
    for (int i = 0; i < np; i++) walk(c, plist[i], +1);
    occ[c] = 1; pos[c] = np; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static void del_point(int c) {                 /* c in state */
    int i = pos[c], last = plist[--np];
    plist[i] = last; pos[last] = i; occ[c] = 0; rc[c / n]--; cc[c % n]--;
    for (int k = 0; k < np; k++) walk(c, plist[k], -1);
    conf -= F[c];
}
static int orbit_free(int r) {                 /* cells free + capacities (counting the orbit's own cells) */
    int k = orbsz[r];
    static int ru[8], rv[8];
    for (int j = 0; j < k; j++) {
        int c = orb[r][j];
        if (occ[c]) return 0;
        ru[j] = c / n; rv[j] = c % n;
    }
    for (int j = 0; j < k; j++) {
        int cu = 0, cv = 0;
        for (int i = 0; i < k; i++) { if (ru[i] == ru[j]) cu++; if (rv[i] == rv[j]) cv++; }
        if (rc[ru[j]] + cu > 2 || cc[rv[j]] + cv > 2) return 0;
    }
    return 1;
}
static void insert_orbit(int r) { for (int j = 0; j < orbsz[r]; j++) add_point(orb[r][j]); repidx[r] = nreps; reps[nreps++] = r; }
static void remove_orbit(int r) {
    for (int j = 0; j < orbsz[r]; j++) del_point(orb[r][j]);
    int i = repidx[r], last = reps[--nreps]; reps[i] = last; repidx[last] = i; repidx[r] = -1;
}
/* cost of inserting orbit r (exact, via insertion then removal) */
static long insert_cost(int r) {
    long before = conf; insert_orbit(r); long d = conf - before; remove_orbit(r); return d;
}
static long full_conf(void) {
    long t = 0;
    for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) for (int k = j + 1; k < np; k++) {
        int a = plist[i], b = plist[j], c = plist[k];
        long ua = a / n, va = a % n, ub = b / n, vb = b % n, uc = c / n, vc = c % n;
        if ((ub - ua) * (vc - va) == (vb - va) * (uc - ua)) t++;
    }
    return t;
}
static void write_tokens(const char *path) {
    FILE *f = fopen(path, "w"); if (!f) return;
    int tmp[MAXK]; for (int i = 0; i < np; i++) tmp[i] = plist[i];
    qsort(tmp, np, sizeof(int), cmpint);
    for (int i = 0; i < np; i++) fprintf(f, "%d%c", tmp[i], i + 1 < np ? ' ' : '\n');
    fclose(f);
}
static int add_random_orbit(int tries) {
    for (int t = 0; t < tries; t++) {
        int r = orbrep[rint_(n * n)];
        if (repidx[r] >= 0) continue;
        if (orbit_free(r)) { insert_orbit(r); return 1; }
    }
    return 0;
}
/* add the orbit with the least insertion cost among a sample of free reps */
static int add_best_orbit(int sample) {
    int bestr = -1; long bestc = 1L << 40;
    for (int t = 0; t < sample; t++) {
        int r = orbrep[rint_(n * n)];
        if (repidx[r] >= 0 || !orbit_free(r)) continue;
        long p = 0; for (int j = 0; j < orbsz[r]; j++) p += F[orb[r][j]];
        if (p < bestc) { bestc = p; bestr = r; }
    }
    if (bestr < 0) return 0;
    insert_orbit(bestr); return 1;
}


static int adm[MAXC];   /* admissible orbit reps after a removal */
static int nadm;

/* collect admissible orbit reps: all cells F==0, free, capacity ok; excludes 'excl' */
static void collect_admissible(int excl) {
    nadm = 0;
    for (int c = 0; c < n * n; c++) {
        if (orbrep[c] != c || c == excl || repidx[c] >= 0) continue;
        int ok = 1;
        for (int j = 0; j < orbsz[c]; j++) { int x = orb[c][j]; if (F[x] != 0 || occ[x]) { ok = 0; break; } }
        if (!ok || !orbit_free(c)) continue;
        adm[nadm++] = c;
    }
}
/* insert admissible orbits greedily in random order (re-checking F==0 after each insertion); returns count inserted */
static int insert_admissible_greedy(void) {
    int cnt = 0;
    /* shuffle */
    for (int i = nadm - 1; i > 0; i--) { int j = rint_(i + 1); int t = adm[i]; adm[i] = adm[j]; adm[j] = t; }
    for (int i = 0; i < nadm; i++) {
        int c = adm[i];
        if (repidx[c] >= 0) continue;
        int ok = 1;
        for (int j = 0; j < orbsz[c]; j++) { int x = orb[c][j]; if (F[x] != 0 || occ[x]) { ok = 0; break; } }
        if (!ok || !orbit_free(c)) continue;
        insert_orbit(c); cnt++;
        if (conf != 0) { remove_orbit(c); cnt--; }   /* internal collinearity of the orbit with itself+state */
    }
    return cnt;
}
/* greedy fill of the whole grid with admissible orbits (random order) */
static int fill_admissible(void) { collect_admissible(-1); return insert_admissible_greedy(); }

/* kick: insert a random non-admissible orbit, then evict the most conflicting orbits until lawful */
static void kick(void) {
    for (int t = 0; t < 10000; t++) {
        int c = orbrep[rint_(n * n)];
        if (repidx[c] >= 0 || !orbit_free(c)) continue;
        insert_orbit(c);
        break;
    }
    while (conf > 0) {
        int worst = -1; long wt = -1;
        for (int i = 0; i < nreps; i++) {
            int r = reps[i]; long t = 0;
            for (int j = 0; j < orbsz[r]; j++) t += T_of(orb[r][j]);
            if (t > wt || (t == wt && (rnd() & 1))) { wt = t; worst = r; }
        }
        remove_orbit(worst);
    }
}

int main(int argc, char **argv) {
    if (argc < 7) { fprintf(stderr, "usage: ils n group seed seconds kick_every outprefix [startfile]\n"); return 2; }
    n = atoi(argv[1]); m = n - 1;
    const char *gname = argv[2];
    rs = 0x9E3779B97F4A7C15ULL ^ ((unsigned long long)atoll(argv[3]) * 0x2545F4914F6CDD1DULL + 999);
    for (int i = 0; i < 20; i++) rnd();
    double seconds = atof(argv[4]);
    long kick_every = atol(argv[5]);
    const char *outprefix = argv[6];
    const char *startfile = argc > 7 ? argv[7] : NULL;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = gcd(a, b);
    build_group(gname);
    for (int c = 0; c < n * n; c++) repidx[c] = -1;
    if (startfile) {
        FILE *f = fopen(startfile, "r"); if (!f) { fprintf(stderr, "cannot open %s\n", startfile); return 2; }
        int t;
        while (fscanf(f, "%d", &t) == 1) {
            if (t < 0 || t >= n * n) continue;
            int r = orbrep[t]; if (repidx[r] >= 0) continue;
            if (orbit_free(r)) { insert_orbit(r); if (conf) { remove_orbit(r); } }
        }
        fclose(f);
        fprintf(stderr, "start: %d tokens, %ld triples\n", np, conf);
    }
    fill_admissible();
    fprintf(stderr, "initial lawful: %d tokens\n", np);
    if (full_conf() != conf || conf != 0) { fprintf(stderr, "conf mismatch at start\n"); return 3; }

    double t0 = now(), tlast = t0;
    long it = 0, plateau = 0, kicks = 0, improvements = 0;
    int best = 0; int best_tokens[MAXK]; int nbest = 0;
    char path[512];
    for (;;) {
        it++;
        if ((it & 255) == 0) {
            double el = now() - t0;
            if (el > seconds) break;
            if (now() - tlast > 5.0) {
                tlast = now();
                fprintf(stderr, "[%6.0fs] it=%ld K=%d best=%d plateau=%ld kicks=%ld impr=%ld\n", el, it, np, best, plateau, kicks, improvements);
            }
        }
        if (np > best) {
            best = np; nbest = np; for (int i = 0; i < np; i++) best_tokens[i] = plist[i];
            snprintf(path, sizeof path, "%s_lawful_%d.txt", outprefix, np);
            write_tokens(path);
            fprintf(stderr, "LAWFUL %d tokens -> %s (%.0fs)\n", np, path, now() - t0);
            if (np == 2 * n) { fprintf(stderr, "SATURATED n=%d\n", n); printf("SATURATED %s\n", path); fflush(stdout); return 0; }
            plateau = 0;
        }
        if (nreps < 1) { fill_admissible(); continue; }
        /* (1,k)-swap: remove a random orbit, reinsert admissible orbits greedily (excluding the removed one first) */
        int r = reps[rint_(nreps)];
        int before = np;
        remove_orbit(r);
        collect_admissible(r);
        int k = insert_admissible_greedy();
        if (np > before) { improvements++; plateau = 0; continue; }
        if (np == before) { plateau++; }
        else {
            /* nothing else admissible: put r back (or, rarely, accept the loss to move) */
            if (rnd() % 1000 == 0) { collect_admissible(-1); insert_admissible_greedy(); }
            else { insert_orbit(r); }
            plateau++;
        }
        (void)k;
        if (kick_every > 0 && plateau >= kick_every) {
            kick(); fill_admissible(); kicks++; plateau = 0;
        }
    }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at end\n"); return 3; }
    fprintf(stderr, "done: it=%ld K=%d best=%d kicks=%ld impr=%ld\n", it, np, best, kicks, improvements);
    printf("DONE n=%d best=%d\n", n, best);
    (void)nbest; (void)best_tokens;
    return 0;
}
