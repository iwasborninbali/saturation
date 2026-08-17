/* fast/mcw.c — min-conflicts with LINE WEIGHTS (breakout): the field is doubled — F (pairs) and
 * Fw (weighted pairs, weight of the pair's line). Lines that stay violated at stagnation points
 * get heavier, reshaping the plateau. True triples (unweighted) decide lawfulness; weighted
 * triples steer the walk. Only proposes; solve.py re-enters through saturation.the_law.
 *
 * usage: mcw n K group seed seconds T noise outprefix [grow] [startfile]
 * env: P2 (two-orbit move prob), TABU (tenure), STAG (iterations w/o weighted improvement before a bump),
 *      DECAY (bumps between halvings), RELOAD/DRIFT (return to best lawful when conf > DRIFT)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <sys/time.h>

#define MAXN 128
#define MAXC (MAXN * MAXN)
#define MAXK (2 * MAXN + 8)
#define HBITS 22
#define HSIZE (1 << HBITS)

static int n, m, G;
static int orb[MAXC][8], orbsz[MAXC], orbrep[MAXC];
static int occ[MAXC], plist[MAXK], pos[MAXC], np;
static int rc[MAXN], cc[MAXN];
static long conf, wconf;
static int F[MAXC];
static long Fw[MAXC];
static int reps[MAXK], nreps, repidx[MAXC];
static int gcdtab[MAXN][MAXN];
static long tabu_until[MAXC];
static long TABU = 0;

/* line weights: open-addressing hash, key -> weight (absent = 1) */
static unsigned int hkey[HSIZE];
static int hval[HSIZE];
static int hused = 0;

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

/* line key of the line through cells a, b */
static inline unsigned int line_key(int a, int b) {
    int au = a / n, av = a % n, bu = b / n, bv = b % n;
    int du = bu - au, dv = bv - av;
    int g = gcdtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    if (du < 0 || (du == 0 && dv < 0)) { du = -du; dv = -dv; }
    int o = du * av - dv * au + 2 * n * n;               /* offset, shifted positive */
    return (unsigned int)(((du + n) * (2 * n + 1) + (dv + n)) * (4 * n * n + 1) + o);
}
static inline unsigned int hslot(unsigned int key) { return (key * 2654435761u) >> (32 - HBITS); }
static inline int wget(unsigned int key) {
    unsigned int s = hslot(key);
    while (hkey[s]) { if (hkey[s] == key) return hval[s]; s = (s + 1) & (HSIZE - 1); }
    return 1;
}
static inline void wset(unsigned int key, int w) {
    unsigned int s = hslot(key);
    while (hkey[s]) { if (hkey[s] == key) { hval[s] = w; return; } s = (s + 1) & (HSIZE - 1); }
    if (hused > HSIZE / 2) { fprintf(stderr, "weight table full\n"); exit(4); }
    hkey[s] = key; hval[s] = w; hused++;
}

/* walk the line through a and b adding d to F and d*w to Fw */
static inline void walk(int a, int b, int d, long dw) {
    int au = a / n, av = a % n, bu = b / n, bv = b % n;
    int du = bu - au, dv = bv - av;
    int g = gcdtab[abs(du)][abs(dv)];
    du /= g; dv /= g;
    int u = au, v = av;
    while (u - du >= 0 && u - du <= m && v - dv >= 0 && v - dv <= m) { u -= du; v -= dv; }
    while (u >= 0 && u <= m && v >= 0 && v <= m) { int c = u * n + v; F[c] += d; Fw[c] += dw; u += du; v += dv; }
}
static inline int T_of(int c) { return F[c] - (np - 1); }

static void add_point(int c) {
    conf += F[c]; wconf += Fw[c];
    for (int i = 0; i < np; i++) { int q = plist[i]; int w = wget(line_key(c, q)); walk(c, q, +1, +w); }
    occ[c] = 1; pos[c] = np; plist[np++] = c; rc[c / n]++; cc[c % n]++;
}
static void del_point(int c) {
    int i = pos[c], last = plist[--np];
    plist[i] = last; pos[last] = i; occ[c] = 0; rc[c / n]--; cc[c % n]--;
    for (int k = 0; k < np; k++) { int q = plist[k]; int w = wget(line_key(c, q)); walk(c, q, -1, -w); }
    conf -= F[c]; wconf -= Fw[c];
}
static int orbit_free(int r) {
    int k = orbsz[r]; static int ru[8], rv[8];
    for (int j = 0; j < k; j++) { int c = orb[r][j]; if (occ[c]) return 0; ru[j] = c / n; rv[j] = c % n; }
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
static int add_best_orbit(int sample) {
    int bestr = -1; long bestc = 1L << 60;
    for (int t = 0; t < sample; t++) {
        int r = orbrep[rint_(n * n)];
        if (repidx[r] >= 0 || !orbit_free(r)) continue;
        long p = 0; for (int j = 0; j < orbsz[r]; j++) p += F[orb[r][j]];
        if (p < bestc) { bestc = p; bestr = r; }
    }
    if (bestr < 0) return 0;
    insert_orbit(bestr); return 1;
}

/* rebuild Fw and wconf from scratch (after weight decay) */
static void rebuild_weighted(void) {
    for (int c = 0; c < n * n; c++) Fw[c] = 0;
    for (int i = 0; i < np; i++) for (int j = i + 1; j < np; j++) {
        int w = wget(line_key(plist[i], plist[j]));
        walk(plist[i], plist[j], 0, +w);
    }
    /* wconf = sum over points of weighted pairs-through-point / 3, computed via directions */
    static int cntd[(2 * MAXN - 1) * (2 * MAXN - 1)];
    static int touched[MAXK];
    long total = 0;
    int W = 2 * n - 1;
    for (int i = 0; i < np; i++) {
        int c = plist[i], u = c / n, v = c % n, nt = 0;
        for (int j = 0; j < np; j++) {
            if (j == i) continue;
            int q = plist[j];
            int du = q / n - u, dv = q % n - v;
            int g = gcdtab[abs(du)][abs(dv)]; du /= g; dv /= g;
            if (du < 0 || (du == 0 && dv < 0)) { du = -du; dv = -dv; }
            int d = (du + m) * W + (dv + m);
            if (cntd[d] == 0) touched[nt++] = d;
            cntd[d]++;
        }
        for (int k = 0; k < nt; k++) {
            int d = touched[k], kd = cntd[d];
            if (kd >= 2) {
                /* find a point in this direction to get the line key */
                int du = d / W - m, dv = d % W - m;
                int q = -1;
                for (int j = 0; j < np && q < 0; j++) {
                    if (j == i) continue;
                    int qq = plist[j]; int eu = qq / n - u, ev = qq % n - v;
                    int g = gcdtab[abs(eu)][abs(ev)]; eu /= g; ev /= g;
                    if (eu < 0 || (eu == 0 && ev < 0)) { eu = -eu; ev = -ev; }
                    if (eu == du && ev == dv) q = qq;
                }
                total += (long)wget(line_key(c, q)) * kd * (kd - 1) / 2;
            }
            cntd[d] = 0;
        }
    }
    wconf = total / 3;
}

/* bump: +1 weight to every line with >= 3 state points; returns number of lines bumped */
static int bump_violated(void) {
    static unsigned int keys[4096]; int nk = 0;
    static int cntd[(2 * MAXN - 1) * (2 * MAXN - 1)];
    static int touched[MAXK];
    int W = 2 * n - 1;
    for (int i = 0; i < np; i++) {
        int c = plist[i];
        if (T_of(c) <= 0) continue;
        int u = c / n, v = c % n, nt = 0;
        for (int j = 0; j < np; j++) {
            if (j == i) continue;
            int q = plist[j];
            int du = q / n - u, dv = q % n - v;
            int g = gcdtab[abs(du)][abs(dv)]; du /= g; dv /= g;
            if (du < 0 || (du == 0 && dv < 0)) { du = -du; dv = -dv; }
            int d = (du + m) * W + (dv + m);
            if (cntd[d] == 0) touched[nt++] = d;
            cntd[d]++;
        }
        for (int k = 0; k < nt; k++) {
            int d = touched[k], kd = cntd[d];
            if (kd >= 2) {
                int du = d / W - m, dv = d % W - m;
                int q = -1;
                for (int j = 0; j < np && q < 0; j++) {
                    if (j == i) continue;
                    int qq = plist[j]; int eu = qq / n - u, ev = qq % n - v;
                    int g = gcdtab[abs(eu)][abs(ev)]; eu /= g; ev /= g;
                    if (eu < 0 || (eu == 0 && ev < 0)) { eu = -eu; ev = -ev; }
                    if (eu == du && ev == dv) q = qq;
                }
                unsigned int key = line_key(c, q);
                int dup = 0; for (int x = 0; x < nk; x++) if (keys[x] == key) dup = 1;
                if (!dup && nk < 4096) {
                    keys[nk++] = key;
                    int kpts = kd + 1;                       /* points on the line */
                    int w = wget(key); wset(key, w + 1);
                    long pairs = (long)kpts * (kpts - 1) / 2;
                    walk(c, q, 0, pairs);                    /* every cell on the line gains 'pairs' */
                    wconf += (long)kpts * (kpts - 1) * (kpts - 2) / 6;
                }
            }
            cntd[d] = 0;
        }
    }
    return nk;
}
static void decay_weights(void) {
    for (unsigned int s = 0; s < HSIZE; s++) if (hkey[s]) { hval[s] = hval[s] > 1 ? (hval[s] + 1) / 2 : 1; }
    rebuild_weighted();
}

int main(int argc, char **argv) {
    if (argc < 9) { fprintf(stderr, "usage: mcw n K group seed seconds T noise outprefix [grow] [startfile]\n"); return 2; }
    n = atoi(argv[1]); m = n - 1;
    int K = atoi(argv[2]);
    const char *gname = argv[3];
    rs = 0x9E3779B97F4A7C15ULL ^ ((unsigned long long)atoll(argv[4]) * 0x2545F4914F6CDD1DULL + 4242);
    for (int i = 0; i < 20; i++) rnd();
    double seconds = atof(argv[5]);
    double T = atof(argv[6]);
    double noise = atof(argv[7]);
    const char *outprefix = argv[8];
    int grow = argc > 9 ? atoi(argv[9]) : 0;
    const char *startfile = argc > 10 ? argv[10] : NULL;
    double p2 = getenv("P2") ? atof(getenv("P2")) : 0.3;
    TABU = getenv("TABU") ? atol(getenv("TABU")) : 0;
    long STAG = getenv("STAG") ? atol(getenv("STAG")) : 50;
    long DECAY = getenv("DECAY") ? atol(getenv("DECAY")) : 200;
    long RELOAD = getenv("RELOAD") ? atol(getenv("RELOAD")) : 0;
    long DRIFT = getenv("DRIFT") ? atol(getenv("DRIFT")) : 6;
    for (int a = 0; a < n; a++) for (int b = 0; b < n; b++) gcdtab[a][b] = gcd(a, b);
    build_group(gname);
    for (int c = 0; c < n * n; c++) repidx[c] = -1;

    if (startfile) {
        FILE *f = fopen(startfile, "r"); if (!f) { fprintf(stderr, "cannot open %s\n", startfile); return 2; }
        int t;
        while (fscanf(f, "%d", &t) == 1) {
            if (t < 0 || t >= n * n) continue;
            int r = orbrep[t]; if (repidx[r] >= 0) continue;
            if (orbit_free(r)) insert_orbit(r);
        }
        fclose(f);
        fprintf(stderr, "start: %d tokens, %ld triples\n", np, conf);
    }
    { long guard = 0;
      while (np < K && guard < 20000000L) { guard++; if (!add_random_orbit(64)) { if (nreps > 0) remove_orbit(reps[rint_(nreps)]); } }
      fprintf(stderr, "initial: %d tokens, %ld triples\n", np, conf); }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at start\n"); return 3; }

    double t0 = now(), tlast = t0;
    long it = 0, acc = 0, best_conf = conf; int best_lawful = 0;
    long minconf_written = -1, stag = 0, bumps = 0, wbest = wconf;
    char path[512];
    static int cand[MAXC]; int ncand;
    int confl[MAXK];
    static int best_tokens[MAXK]; int nbest_tokens = 0;

    for (;;) {
        it++;
        if ((it & 255) == 0) {
            double el = now() - t0;
            if (el > seconds) break;
            if (now() - tlast > 5.0) {
                tlast = now();
                fprintf(stderr, "[%6.0fs] it=%ld K=%d conf=%ld wconf=%ld best_conf=%ld acc=%ld bumps=%ld lines=%d lawful_best=%d\n",
                        el, it, np, conf, wconf, best_conf, acc, bumps, hused, best_lawful);
                acc = 0;
            }
        }
        if (conf == 0) {
            if (np > best_lawful) {
                best_lawful = np;
                nbest_tokens = np; for (int i = 0; i < np; i++) best_tokens[i] = plist[i];
                snprintf(path, sizeof path, "%s_lawful_%d.txt", outprefix, np);
                write_tokens(path);
                fprintf(stderr, "LAWFUL %d tokens -> %s (%.0fs)\n", np, path, now() - t0);
                if (np == 2 * n) { fprintf(stderr, "SATURATED n=%d\n", n); printf("SATURATED %s\n", path); fflush(stdout); return 0; }
            }
            if (grow) { if (add_best_orbit(400) || add_random_orbit(1000)) { K = np; best_conf = conf; wbest = wconf; } }
        }
        if (conf < best_conf) {
            best_conf = conf;
            if (conf != minconf_written) { minconf_written = conf; snprintf(path, sizeof path, "%s_minconf.txt", outprefix); write_tokens(path); }
        }
        if (RELOAD && nbest_tokens > 0 && (it % RELOAD) == 0 && conf > DRIFT) {
            while (nreps > 0) remove_orbit(reps[nreps - 1]);
            for (int i = 0; i < nbest_tokens; i++) { int r = orbrep[best_tokens[i]]; if (repidx[r] < 0 && orbit_free(r)) insert_orbit(r); }
            K = np; best_conf = conf; wbest = wconf;
            continue;
        }
        if (np < K) add_random_orbit(4);
        if (nreps < 2) continue;

        /* stagnation -> bump weights of violated lines */
        if (wconf < wbest) { wbest = wconf; stag = 0; } else stag++;
        if (STAG > 0 && stag >= STAG && conf > 0) {
            bump_violated(); bumps++; stag = 0; wbest = wconf;
            if (DECAY > 0 && bumps % DECAY == 0) decay_weights();
        }

        int nc = 0;
        for (int i = 0; i < nreps; i++) {
            int rr = reps[i], bad = 0;
            for (int j = 0; j < orbsz[rr]; j++) if (T_of(orb[rr][j]) > 0) { bad = 1; break; }
            if (bad) confl[nc++] = rr;
        }
        int r1 = (nc > 0 && runif() > noise * 0.5) ? confl[rint_(nc)] : reps[rint_(nreps)];
        int two = (np >= 2 * n) || (runif() < p2);
        int r2 = -1;
        if (two) { do { r2 = reps[rint_(nreps)]; } while (r2 == r1); }

        long before = wconf;
        remove_orbit(r1);
        if (two) remove_orbit(r2);

        int ins[2], nins = 0;
        for (int step = 0; step < (two ? 2 : 1); step++) {
            int chosen = -1;
            if (runif() < noise) {
                for (int t = 0; t < 4000 && chosen < 0; t++) {
                    int c = orbrep[rint_(n * n)];
                    if (c == r1 || repidx[c] >= 0 || !orbit_free(c)) continue;
                    chosen = c;
                }
            } else {
                long bestp = 1L << 60; ncand = 0;
                for (int c = 0; c < n * n; c++) {
                    if (orbrep[c] != c || c == r1 || repidx[c] >= 0) continue;
                    if (!orbit_free(c)) continue;
                    long p = 0; for (int j = 0; j < orbsz[c]; j++) p += Fw[orb[c][j]];
                    if (TABU && tabu_until[c] > it && p > 0) continue;
                    if (p < bestp) { bestp = p; ncand = 0; }
                    if (p == bestp && ncand < MAXC) cand[ncand++] = c;
                }
                if (ncand > 0) chosen = cand[rint_(ncand)];
            }
            if (chosen < 0) break;
            insert_orbit(chosen); ins[nins++] = chosen;
        }
        long delta = wconf - before;
        int complete = (nins == (two ? 2 : 1));
        if (complete && (delta <= 0 || runif() < exp(-delta / T))) {
            acc++;
            if (TABU) { tabu_until[r1] = it + TABU + rint_((int)TABU + 1); if (two) tabu_until[r2] = it + TABU + rint_((int)TABU + 1); }
        } else {
            for (int i = nins - 1; i >= 0; i--) remove_orbit(ins[i]);
            if (two) insert_orbit(r2);
            insert_orbit(r1);
        }
    }
    if (full_conf() != conf) { fprintf(stderr, "conf mismatch at end\n"); return 3; }
    fprintf(stderr, "done: it=%ld K=%d conf=%ld best_conf=%ld lawful_best=%d bumps=%ld\n", it, np, conf, best_conf, best_lawful, bumps);
    printf("DONE n=%d K=%d best_conf=%ld lawful_best=%d\n", n, np, best_conf, best_lawful);
    return 0;
}
