/* RA9X16: C port of rv16.py (same algorithm, same counters), for speed.  See rv16.py for the mathematics.
   usage: rv16c PART b [--sym] [--only KEY] [--q Q] [--mult M] [--rmax R] [--thr T] [--nobudget] [--nofloor]
          [--nofull]  (skip the full exact check at Y leaves; counts every Y leaf as a survivor) */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define FULL 511
#define BM 0x00F
#define CM 0x1F0
static int PC[512], EL[512][9], NE[512], PRL[512][10], NPR[512], PIDX[9][9];
static int QMAX = 3, MMAX = 2, RMAX = 8, THR = 12, BUDGET = 1, NOFLOOR = 0, SYM = 0, NOFULL = 0;
static const char *ONLY = NULL;
static int r[9], q[36], mu[512];
static int cmpi(const void *a, const void *b) { return *(const int *)a - *(const int *)b; }
static int okm(int m, int hi) {
    if (!hi && mu[m] + 1 > MMAX) return 0;
    for (int k = 0; k < NE[m]; k++) if (r[EL[m][k]] + 1 > RMAX) return 0;
    if (!hi) for (int k = 0; k < NPR[m]; k++) if (q[PRL[m][k]] + 1 > QMAX) return 0;
    return 1;
}
static void addm(int m, int hi, int d) {
    for (int k = 0; k < NE[m]; k++) r[EL[m][k]] += d;
    if (!hi) { for (int k = 0; k < NPR[m]; k++) q[PRL[m][k]] += d; mu[m] += d; }
}
static int capm(int m) {
    int c = MMAX - mu[m];
    for (int k = 0; k < NE[m]; k++) if (RMAX - r[EL[m][k]] < c) c = RMAX - r[EL[m][k]];
    for (int k = 0; k < NPR[m]; k++) if (QMAX - q[PRL[m][k]] < c) c = QMAX - q[PRL[m][k]];
    return c < 0 ? 0 : c;
}
static int sig(const int *v, int n, int k) {
    int a[16]; memcpy(a, v, n * sizeof(int));
    for (int i = 1; i < n; i++) { int x = a[i], j = i - 1; while (j >= 0 && a[j] > x) { a[j + 1] = a[j]; j--; } a[j + 1] = x; }
    int s = 0; for (int i = 0; i < k && i < n; i++) s += a[i]; return s;
}
/* counters */
#define NCT 64
static const char *CTN[NCT] = {"Xnodes","Xcompleted","Xfloor","Xdeg3","Xfloor4","Xfloor5","Ynodes","Yleaves",
  "full_Delta","full_triangle","full_notmaximal","full_12set","full_alpha","full_PASS","Ysurvivors","cap_ok",
  "roots","roots_dead","stab","cap_0","cap_1","cap_2","cap_3","cap_4","cap_5","cap_6","cap_7","cap_8","cap_9",
  "c3_has_one_in_C", "c3_contains_0124", NULL};
static long long ct[NCT], tct[NCT];
static int cti(const char *s) { for (int i = 0; CTN[i]; i++) if (!strcmp(CTN[i], s)) return i; fprintf(stderr, "ctr %s\n", s); exit(2); }
#define CT(s) ct[cti(s)]
static int Xm[8], Xh[8], nX, Ym[7], Yh[7], nY;
static long long nsurv_print = 0;

static unsigned adj[24];
static int mis_best;
static void mis(unsigned P, int sz) {
    if (sz + __builtin_popcount(P) <= mis_best) return;
    if (!P) { if (sz > mis_best) mis_best = sz; return; }
    int v = 31 - __builtin_clz(P);
    mis(P & ~adj[v] & ~(1u << v), sz + 1); mis(P & ~(1u << v), sz);
}
static unsigned char eO[1 << 15]; static unsigned char rS[1 << 15][9];
static const char *fullcheck(void) {
    int O[15], n = 24;
    for (int k = 0; k < 8; k++) O[k] = Xm[k];
    for (int k = 0; k < 7; k++) O[8 + k] = Ym[k];
    memset(adj, 0, sizeof adj);
    for (int k = 0; k < 15; k++) for (int i = 0; i < 9; i++) if (O[k] >> i & 1) { adj[i] |= 1u << (9 + k); adj[9 + k] |= 1u << i; }
    for (int k = 0; k < 15; k++) for (int l = k + 1; l < 15; l++) if (!(O[k] & O[l])) { adj[9 + k] |= 1u << (9 + l); adj[9 + l] |= 1u << (9 + k); }
    for (int u = 0; u < n; u++) if (__builtin_popcount(adj[u]) > 8) return "Delta";
    for (int u = 0; u < n; u++) for (int v = u + 1; v < n; v++) {
        if (adj[u] >> v & 1) { if (adj[u] & adj[v]) return "triangle"; }
        else if (!(adj[u] & adj[v])) return "notmaximal";
    }
    eO[0] = 0; memset(rS[0], 0, 9);
    for (int S = 1; S < (1 << 15); S++) {
        int low = S & -S, k = __builtin_ctz(S), R = S ^ low;
        eO[S] = eO[R] + __builtin_popcount((adj[9 + k] >> 9) & R);
        for (int i = 0; i < 9; i++) rS[S][i] = rS[R][i] + (O[k] >> i & 1);
    }
    for (int S = 0; S < (1 << 15); S++) {
        int s = __builtin_popcount(S); if (s > 12) continue;
        int v[9]; for (int i = 0; i < 9; i++) v[i] = rS[S][i];
        if (eO[S] + sig(v, 9, 12 - s) < 12) return "12set";
    }
    mis_best = 0; mis((1u << 24) - 1, 0);
    if (mis_best > 9) return "alpha";
    return "PASS";
}
static void print_conf(const char *tag) {
    printf("  %s X:", tag);
    for (int k = 0; k < nX; k++) { printf(" %s{", Xh[k] ? "H" : ""); for (int i = 0; i < 9; i++) if (Xm[k] >> i & 1) printf("%d", i); printf("}"); }
    printf(" Y:");
    for (int k = 0; k < nY; k++) { printf(" %s{", Yh[k] ? "H" : ""); for (int i = 0; i < 9; i++) if (Ym[k] >> i & 1) printf("%d", i); printf("}"); }
    printf("\n");
}
/* ---------------- Y search ---------------- */
static int cm[300], chi[300], cd[300], ncand;
static int dYx[8], Ydeg[7], nhY, hiYtarget, dtarget, yfound;
static int dXof(int m) { int d = 0; for (int k = 0; k < nX; k++) if (!(Xm[k] & m)) d++; return d; }
static void yrec(int start, int left) {
    CT("Ynodes")++;
    if (left == 0) {
        if (nhY != hiYtarget) return;
        if (sig(Ydeg, nY, 4) < THR) return;
        int rY[9] = {0}; for (int k = 0; k < nY; k++) for (int i = 0; i < 9; i++) rY[i] += Ym[k] >> i & 1;
        if (sig(rY, 9, 5) < THR) return;
        CT("Yleaves")++;
        if (NOFULL) { yfound++; if (nsurv_print < 5) { nsurv_print++; print_conf("leaf"); } return; }
        const char *res = fullcheck();
        char nm[40]; sprintf(nm, "full_%s", res); CT(nm)++;
        if (!strcmp(res, "PASS")) { yfound++; print_conf("FULLPASS"); }
        else if (nsurv_print < 5) { nsurv_print++; printf("  (leaf failing full check: %s)", res); print_conf(""); }
        return;
    }
    for (int t = start; t < ncand; t++) {
        int m = cm[t], hi = chi[t], d = cd[t];
        if (dtarget < 0) { int tmp[7]; memcpy(tmp, Ydeg, nY * sizeof(int)); for (int j = 0; j < left; j++) tmp[nY + j] = d;
            if (sig(tmp, nY + left, 4) < THR) break; }
        if (hi && nhY >= hiYtarget) continue;
        int bad = 0;
        for (int k = 0; k < nY; k++) if (!(m & Ym[k])) { bad = 1; break; }
        if (bad || !okm(m, hi)) continue;
        for (int j = 0; j < nX; j++) if (!(Xm[j] & m) && dYx[j] + 1 > (Xh[j] ? 2 : 4)) { bad = 1; break; }
        if (bad) continue;
        addm(m, hi, 1); Ym[nY] = m; Yh[nY] = hi; Ydeg[nY] = d; nY++; nhY += hi;
        for (int j = 0; j < nX; j++) if (!(Xm[j] & m)) dYx[j]++;
        yrec(t, left - 1);
        for (int j = 0; j < nX; j++) if (!(Xm[j] & m)) dYx[j]--;
        addm(m, hi, -1); nY--; nhY -= hi;
    }
}
static int ysearch(int need, int hiY, int dt) {
    /* Y[0..nY) fixed and charged */
    for (int j = 0; j < nX; j++) { dYx[j] = 0; for (int k = 0; k < nY; k++) if (!(Xm[j] & Ym[k])) dYx[j]++; }
    nhY = 0; for (int k = 0; k < nY; k++) { Ydeg[k] = dXof(Ym[k]); nhY += Yh[k]; }
    hiYtarget = hiY; dtarget = dt; yfound = 0;
    yrec(0, need);
    return yfound;
}
static int xfloors(const int *Z, int nz) {
    if (NOFLOOR) return 1;
    int rX[9] = {0}; for (int k = 0; k < nX; k++) for (int i = 0; i < 9; i++) rX[i] += Xm[k] >> i & 1;
    for (int sub = 0; sub < (1 << nz); sub++) {
        int j = __builtin_popcount(sub); if (j > 3) continue;
        int rr[9]; memcpy(rr, rX, sizeof rr); int ds = 0;
        for (int t = 0; t < nz; t++) if (sub >> t & 1) { ds += dXof(Z[t]); for (int i = 0; i < 9; i++) rr[i] += Z[t] >> i & 1; }
        if (ds + sig(rr, 9, 4 - j) < THR) return 0;
    }
    return 1;
}
/* ---------------- X completion ---------------- */
static int (*leaf_fn)(void); static int (*fy_fn)(int);
static int hXglob;
static int lcand[8][130];
static void rec_lo(int depth, const int *cl, int ncl, int left) {
    CT("Xnodes")++;
    int cb = 0; for (int k = 0; k < nX; k++) cb += PC[Xm[k] & CM];
    if (BUDGET && cb + left > 20 + hXglob) return;
    if (left == 0) { CT("Xcompleted")++; leaf_fn(); return; }
    for (int t = 0; t < ncl; t++) {
        int m = cl[t];
        if (!okm(m, 0) || !fy_fn(m)) continue;
        addm(m, 0, 1); Xm[nX] = m; Xh[nX] = 0; nX++;
        int n2 = 0; for (int u = t; u < ncl; u++) if (cl[u] & m) lcand[depth + 1][n2++] = cl[u];
        rec_lo(depth + 1, lcand[depth + 1], n2, left - 1);
        nX--; addm(m, 0, -1);
    }
}
static void start_lo(int need_lo) {
    int n = 0;
    for (int m = 0; m < 512; m++) if (PC[m] == 4 && (m & BM)) {
        int ok = 1; for (int k = 0; k < nX; k++) if (!(m & Xm[k])) { ok = 0; break; }
        if (ok) lcand[0][n++] = m;
    }
    rec_lo(0, lcand[0], n, need_lo);
}
static int hcand[130], nhc;
static void rec_hi(int start, int left, int need_lo) {
    if (left == 0) { start_lo(need_lo); return; }
    for (int t = start; t < nhc; t++) {
        int m = hcand[t], ok = 1;
        for (int k = 0; k < nX; k++) if (!(m & Xm[k])) { ok = 0; break; }
        if (!ok || !okm(m, 1)) continue;
        addm(m, 1, 1); Xm[nX] = m; Xh[nX] = 1; nX++;
        rec_hi(t, left - 1, need_lo);
        nX--; addm(m, 1, -1);
    }
}
static void reset(void) { memset(r, 0, sizeof r); memset(q, 0, sizeof q); memset(mu, 0, sizeof mu); nX = nY = 0; }
static int sub_(int e) { return CM & ~(1 << e); }
static void report(const char *key, clock_t t0) {
    printf("%s {", key);
    for (int i = 0; CTN[i]; i++) if (ct[i]) printf(" %s:%lld", CTN[i], ct[i]);
    printf(" } %.1fs\n", (double)(clock() - t0) / CLOCKS_PER_SEC); fflush(stdout);
    for (int i = 0; i < NCT; i++) { tct[i] += ct[i]; ct[i] = 0; }
}
/* ---------------- part 1 ---------------- */
static int P1hY;
static int fy_true(int m) { (void)m; return 1; }
static int leaf1(void) {
    int forced[4], nf = 0;
    for (int k = 0; k < nX; k++) if (Xh[k] && Xm[k] != CM) {
        int z = FULL ^ Xm[k], dup = 0; for (int t = 0; t < nf; t++) if (forced[t] == z) dup = 1;
        if (!dup) forced[nf++] = z;
    }
    for (int t = 0; t < nf; t++) { if (!(forced[t] & BM)) return 0; for (int u = t + 1; u < nf; u++) if (!(forced[t] & forced[u])) return 0; }
    int Z[1] = {BM};
    if (!xfloors(Z, 1)) return 0;
    CT("Xfloor")++;
    /* Y fixed: y (B, already charged) + forced */
    nY = 0; Ym[nY] = BM; Yh[nY] = 0; nY++;
    int added = 0, good = 1;
    for (int t = 0; t < nf; t++) {
        if (dXof(forced[t]) > 4 || !okm(forced[t], 0)) { good = 0; break; }
        addm(forced[t], 0, 1); added++; Ym[nY] = forced[t]; Yh[nY] = 0; nY++;
    }
    if (good) for (int j = 0; j < nX; j++) { int d = 0; for (int k = 0; k < nY; k++) if (!(Xm[j] & Ym[k])) d++; if (d > (Xh[j] ? 2 : 4)) good = 0; }
    if (good) {
        ncand = 0;
        int tm[300], th[300], td[300], nt = 0;
        for (int m = 0; m < 512; m++) if (PC[m] == 4) {
            int ok = 1; for (int k = 0; k < nY; k++) if (!(m & Ym[k])) ok = 0;
            if (ok) { int d = dXof(m); if (d <= 4) { tm[nt] = m; th[nt] = 0; td[nt] = d; nt++; } }
        }
        int seenL[512]; memset(seenL, 0, sizeof seenL);
        for (int k = 0; k < nX; k++) if (!Xh[k] && !seenL[Xm[k]]) {
            seenL[Xm[k]] = 1; int H = FULL ^ Xm[k], ok = 1;
            for (int u = 0; u < nY; u++) if (!(H & Ym[u])) ok = 0;
            if (ok) { tm[nt] = H; th[nt] = 1; td[nt] = dXof(H); nt++; }
        }
        /* sort by degree desc, then hi asc, then mask asc */
        int keys[300]; for (int t = 0; t < nt; t++) keys[t] = (4 - td[t]) * 1024 + th[t] * 512 + tm[t];
        qsort(keys, nt, sizeof(int), cmpi);
        for (int t = 0; t < nt; t++) { cm[ncand] = keys[t] & 511; chi[ncand] = (keys[t] >> 9) & 1; cd[ncand] = 4 - (keys[t] >> 10); ncand++; }
        if (ysearch(7 - nY, P1hY, -1)) CT("Ysurvivors")++;
    }
    for (int t = 0; t < added; t++) addm(forced[t], 0, -1);
    nY = 0;
    return 0;
}
static void part1(int b) {
    static const int seeds[4][2][5] = { /* [c][pattern] = count, missing elements... */
        {{4, 4, 5, 6, 7}, {-1}}, {{3, 6, 7, 8}, {3, 8, 8, 7}}, {{2, 7, 8}, {2, 8, 8}}, {{1, 8}, {-1}} };
    static const char *names[4][2] = {{"1111", 0}, {"111", "21"}, {"11", "2"}, {"1", 0}};
    for (int hX = 0; hX <= b; hX++) for (int c = 0; c <= hX && c <= 3; c++) for (int pt = 0; pt < 2; pt++) {
        if (seeds[c][pt][0] < 0) continue;
        char key[80]; sprintf(key, "b%d_hX%d_hY%d_c%d_%s", b, hX, b - hX, c, names[c][pt]);
        if (ONLY && !strstr(key, ONLY)) continue;
        clock_t t0 = clock(); reset(); addm(BM, 0, 1);
        int ok = 1;
        for (int k = 0; k < c; k++) { if (!okm(CM, 1)) ok = 0; addm(CM, 1, 1); Xm[nX] = CM; Xh[nX] = 1; nX++; }
        for (int k = 1; k <= seeds[c][pt][0]; k++) { int m = sub_(seeds[c][pt][k]); if (!okm(m, 0)) ok = 0; addm(m, 0, 1); Xm[nX] = m; Xh[nX] = 0; nX++; }
        if (!ok) { printf("%s seed violates caps\n", key); continue; }
        nhc = 0; for (int m = 0; m < 512; m++) if (PC[m] == 5 && m != CM && (m & BM) != BM) hcand[nhc++] = m;
        P1hY = b - hX; hXglob = hX; leaf_fn = leaf1; fy_fn = fy_true;
        rec_hi(0, hX - c, 4 - (hX - c));
        report(key, t0);
    }
}
/* ---------------- part 2 ---------------- */
static int comp[4], ncomp;
static int fy2(int m) {
    int dy = 0;
    for (int t = 0; t < ncomp; t++) if (!(comp[t] & m)) { dy++; if (dXof(comp[t]) + 1 > 3) return 0; }
    return dy <= 4;
}
static int leaf2(void) {
    for (int t = 0; t < ncomp; t++) if (dXof(comp[t]) != 3) return 0;
    CT("Xdeg3")++;
    if (hXglob == 3 && nX == 8) { int one = 0; for (int k = 0; k < nX; k++) if (!Xh[k] && PC[Xm[k] & CM] == 1) one = 1;
        int c3 = 1; for (int k = 0; k < 3; k++) if (!(Xh[k] && Xm[k] == CM)) c3 = 0;
        if (c3 && one) CT("c3_has_one_in_C")++;
        int has = 0; for (int k = 0; k < nX; k++) if (!Xh[k] && Xm[k] == 0x17) has = 1;
        if (c3 && has) CT("c3_contains_0124")++; }
    if (!xfloors(comp, 0)) return 0;
    CT("Xfloor4")++;
    if (!xfloors(comp, ncomp)) return 0;
    CT("Xfloor5")++;
    int dYc[8]; for (int j = 0; j < nX; j++) { dYc[j] = 0; for (int t = 0; t < ncomp; t++) if (!(Xm[j] & comp[t])) dYc[j]++; }
    int capsum = 0; ncand = 0;
    for (int m = 0; m < 512; m++) if (PC[m] == 4) {
        int ok = 1; for (int t = 0; t < ncomp; t++) if (!(m & comp[t])) ok = 0;
        if (!ok || dXof(m) != 3) continue;
        int cp = capm(m);
        for (int j = 0; j < nX; j++) if (!(Xm[j] & m)) { int c2 = (Xh[j] ? 2 : 4) - dYc[j]; if (c2 < cp) cp = c2; }
        if (cp < 0) cp = 0;
        if (cp > 0) { cm[ncand] = m; chi[ncand] = 0; cd[ncand] = 3; ncand++; capsum += cp; }
    }
    int need = 7 - ncomp;
    char nm[16]; sprintf(nm, "cap_%d", capsum > 9 ? 9 : capsum); CT(nm)++;
    if (capsum >= need) CT("cap_ok")++;
    nY = 0; for (int t = 0; t < ncomp; t++) { Ym[nY] = comp[t]; Yh[nY] = 0; nY++; }
    if (ysearch(need, 0, 3)) CT("Ysurvivors")++;
    nY = 0;
    return 0;
}
static int perm_mask(int m, const int *p) { int x = 0; for (int i = 0; i < 9; i++) if (m >> i & 1) x |= 1 << p[i]; return x; }
static int G[2880][9], nG;
static void stabiliser(const int *seed, int ns) {
    int key[8]; memcpy(key, seed, ns * sizeof(int)); qsort(key, ns, sizeof(int), cmpi);
    int pb[4] = {0, 1, 2, 3}, pcC[5];
    nG = 0;
    /* iterate all permutations of B (24) and C (120) */
    int idx[9];
    for (int a = 0; a < 24; a++) {
        int el[4] = {0, 1, 2, 3}, aa = a, used[4] = {0}, pa[4];
        for (int i = 0; i < 4; i++) { int f = 1; for (int j = 1; j < 4 - i; j++) f *= j; int s = aa / f; aa %= f;
            int cnt = -1; for (int j = 0; j < 4; j++) if (!used[j] && ++cnt == s) { pa[i] = el[j]; used[j] = 1; break; } }
        for (int c = 0; c < 120; c++) {
            int cc = c, usedc[5] = {0};
            for (int i = 0; i < 5; i++) { int f = 1; for (int j = 1; j < 5 - i; j++) f *= j; int s = cc / f; cc %= f;
                int cnt = -1; for (int j = 0; j < 5; j++) if (!usedc[j] && ++cnt == s) { pcC[i] = 4 + j; usedc[j] = 1; break; } }
            for (int i = 0; i < 4; i++) idx[i] = pa[i];
            for (int i = 0; i < 5; i++) idx[4 + i] = pcC[i];
            int im[8]; for (int k = 0; k < ns; k++) im[k] = perm_mask(seed[k], idx);
            qsort(im, ns, sizeof(int), cmpi);
            if (!memcmp(im, key, ns * sizeof(int))) { memcpy(G[nG], idx, sizeof idx); nG++; }
        }
    }
    (void)pb;
}
static int is_canon(const int *combo, int k) {
    /* combo sorted ascending; canonical iff lexicographically minimal sorted image under G */
    for (int g = 0; g < nG; g++) {
        int im[3]; for (int t = 0; t < k; t++) im[t] = perm_mask(combo[t], G[g]);
        qsort(im, k, sizeof(int), cmpi);
        for (int t = 0; t < k; t++) { if (im[t] < combo[t]) return 0; if (im[t] > combo[t]) break; }
    }
    return 1;
}
static void part2(int b) {
    static const int seeds[4][2][3] = {{{-1}}, {{2, 7, 8}, {2, 8, 8}}, {{1, 8}, {-1}}, {{0}, {-1}}};
    static const char *names[4][2] = {{0, 0}, {"distinct", "doubled"}, {"one", 0}, {"none", 0}};
    for (int c = 1; c <= b; c++) for (int pt = 0; pt < 2; pt++) {
        if (seeds[c][pt][0] < 0) continue;
        char key[80]; sprintf(key, "b%d_c%d_%s%s", b, c, names[c][pt], SYM ? "_sym" : "_nosym");
        if (ONLY && !strstr(key, ONLY)) continue;
        clock_t t0 = clock();
        int seed[8], ns = 0;
        for (int k = 0; k < c; k++) seed[ns++] = CM;
        for (int k = 1; k <= seeds[c][pt][0]; k++) seed[ns++] = sub_(seeds[c][pt][k]);
        stabiliser(seed, ns); CT("stab") = nG;
        nhc = 0; for (int m = 0; m < 512; m++) if (PC[m] == 5 && m != CM && (m & BM) != BM) hcand[nhc++] = m;
        int ne = b - c, combo[3];
        int tot_combos = 1; for (int t = 0; t < ne; t++) tot_combos *= nhc;
        for (int code = 0; code < tot_combos; code++) {
            int cc = code, okc = 1;
            for (int t = 0; t < ne; t++) { combo[t] = hcand[cc % nhc]; cc /= nhc; }
            for (int t = 1; t < ne; t++) if (combo[t] < combo[t - 1]) okc = 0;   /* multisets, ascending */
            if (!okc) continue;
            if (SYM && !is_canon(combo, ne)) continue;
            CT("roots")++;
            reset(); addm(BM, 0, 1);
            int ok = 1;
            for (int k = 0; k < ns; k++) { int hi = seed[k] == CM; for (int u = 0; u < nX; u++) if (!(seed[k] & Xm[u])) ok = 0;
                if (!okm(seed[k], hi)) ok = 0; addm(seed[k], hi, 1); Xm[nX] = seed[k]; Xh[nX] = hi; nX++; }
            for (int t = 0; t < ne; t++) { for (int u = 0; u < nX; u++) if (!(combo[t] & Xm[u])) ok = 0;
                if (!okm(combo[t], 1)) ok = 0; addm(combo[t], 1, 1); Xm[nX] = combo[t]; Xh[nX] = 1; nX++; }
            ncomp = 0; comp[ncomp++] = BM;
            for (int t = 0; t < ne; t++) { int z = FULL ^ combo[t], dup = 0; for (int u = 0; u < ncomp; u++) if (comp[u] == z) dup = 1;
                if (!dup) { if (!okm(z, 0)) ok = 0; addm(z, 0, 1); comp[ncomp++] = z; } }
            for (int t = 0; t < ncomp; t++) { for (int u = t + 1; u < ncomp; u++) if (!(comp[t] & comp[u])) ok = 0; if (dXof(comp[t]) > 3) ok = 0; }
            if (!ok) { CT("roots_dead")++; continue; }
            hXglob = b; leaf_fn = leaf2; fy_fn = fy2;
            start_lo(5 - ne);
        }
        report(key, t0);
    }
}
int main(int argc, char **argv) {
    for (int m = 0; m < 512; m++) { PC[m] = __builtin_popcount(m); NE[m] = 0; for (int i = 0; i < 9; i++) if (m >> i & 1) EL[m][NE[m]++] = i; }
    int t = 0; for (int i = 0; i < 9; i++) for (int j = i + 1; j < 9; j++) PIDX[i][j] = t++;
    for (int m = 0; m < 512; m++) { NPR[m] = 0; for (int a = 0; a < NE[m]; a++) for (int b2 = a + 1; b2 < NE[m]; b2++) if (NPR[m] < 10) PRL[m][NPR[m]++] = PIDX[EL[m][a]][EL[m][b2]]; }
    if (argc < 3) { fprintf(stderr, "usage\n"); return 2; }
    int part = atoi(argv[1]), b = atoi(argv[2]);
    for (int i = 3; i < argc; i++) {
        if (!strcmp(argv[i], "--sym")) SYM = 1;
        else if (!strcmp(argv[i], "--nobudget")) BUDGET = 0;
        else if (!strcmp(argv[i], "--nofloor")) NOFLOOR = 1;
        else if (!strcmp(argv[i], "--nofull")) NOFULL = 1;
        else if (!strcmp(argv[i], "--only")) ONLY = argv[++i];
        else if (!strcmp(argv[i], "--q")) QMAX = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--mult")) MMAX = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--rmax")) RMAX = atoi(argv[++i]);
        else if (!strcmp(argv[i], "--thr")) THR = atoi(argv[++i]);
        else { fprintf(stderr, "bad arg %s\n", argv[i]); return 2; }
    }
    printf("args part=%d b=%d sym=%d q=%d mult=%d rmax=%d thr=%d budget=%d nofloor=%d nofull=%d only=%s\n", part, b, SYM, QMAX, MMAX, RMAX, THR, BUDGET, NOFLOOR, NOFULL, ONLY ? ONLY : "-");
    if (part == 1) part1(b); else part2(b);
    printf("TOTAL {"); for (int i = 0; CTN[i]; i++) if (tct[i]) printf(" %s:%lld", CTN[i], tct[i]); printf(" }\n");
    return 0;
}
