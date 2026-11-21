/* RA9X10: C port of model_n9_2.py (same search, same assumptions, same counters; see the .py header).
   usage: ./model_n9_2 m [cap]     cap = q4 cap (3 = M1; larger = NEGATIVE CONTROL)
   Validated against the Python version: identical stats on m = 0, 1, 2 (see run log). */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#define FREE (-1)
static int m, CAP, TH = 12, LC = 5; /* LC: a=4 F-degree cap (5 real; 6 = NEGATIVE CONTROL) */
static int LCY = 5; /* cap on Y-low F-degree only (control knob; default = LC) */
static int NOPRUNE = 0; /* 1: disable the derived prunes (3-sum consequences); leaf checks unchanged */
/* TCUT = largest t with t + t + LC < TH: two X vertices of degree <= TCUT plus any third (<= LC) violate the 3-sum rule,
   so at most one X vertex has degree <= TCUT.  TH = 12, LC = 5: TCUT = 3 (i.e. at most one X vertex below 4). */
static int TCUT(void) { int t = -1; while (2 * (t + 1) + LC < TH) t++; return t; }
static int CAPLOW_OK(void) { return !NOPRUNE && TCUT() >= 0; }
/* TH: 10-set edge threshold (12 = the real rule; 11 = NEGATIVE CONTROL) */
static int M4[126], n4 = 0, subC[5], A = 0xF;
static int PI[512][6];           /* pair indices of a 4-mask */
static int pairid[9][9];
static long long st_nreps, st_ysets, st_xnodes, st_xleaves, st_attach, st_deg, st_three, st_ten, st_alpha, st_r, st_surv;
static int printed = 0;
static int popc(int x) { return __builtin_popcount(x); }
static int q4ok(const int *fam, int n) {
    int cnt[36] = {0};
    for (int k = 0; k < n; k++) for (int t = 0; t < 6; t++) if (++cnt[PI[fam[k]][t]] > CAP) return 0;
    return 1;
}
/* ---------- leaf ---------- */
static int XLv[6], nXL; static int YLv[7], nYL; static int Yh[7], nYh; static int Xh[6], nXh; static int curd;
static int adjm[6][7];
static int matchY[7];
static int augp(int u, int *seen, int nx) {
    for (int w = 0; w < 7; w++) if (adjm[u][w] && !seen[w]) {
        seen[w] = 1;
        if (matchY[w] < 0 || augp(matchY[w], seen, nx)) { matchY[w] = u; return 1; }
    }
    return 0;
}
static void fmt(int M, char *b) { int k = 0; for (int i = 0; i < 9; i++) if (M >> i & 1) b[k++] = '0' + i; b[k] = 0; }
static int leaf_checks(void) {
    /* X vertices: XL (low) then Xh (a=5, T or FREE); Y: YL then Yh */
    int xt[6], xm[6], yt[7], ym[7];
    int nx = 0, ny = 0;
    for (int k = 0; k < nXL; k++) { xt[nx] = 0; xm[nx++] = XLv[k]; }
    for (int k = 0; k < nXh; k++) { xt[nx] = 1; xm[nx++] = Xh[k]; }
    for (int k = 0; k < nYL; k++) { yt[ny] = 0; ym[ny++] = YLv[k]; }
    for (int k = 0; k < nYh; k++) { yt[ny] = 1; ym[ny++] = Yh[k]; }
    if (nx != 6 || ny != 7) { fprintf(stderr, "size bug %d %d\n", nx, ny); exit(2); }
    int degX[6] = {0}, degY[7] = {0};
    for (int i = 0; i < 6; i++) for (int j = 0; j < 7; j++) {
        int a;
        if (!xt[i] && !yt[j]) a = (xm[i] & ym[j]) == 0;
        else if (xt[i] && yt[j]) a = 0;
        else if (xt[i]) a = xm[i] != FREE && xm[i] == ym[j];
        else a = ym[j] != FREE && ym[j] == xm[i];
        adjm[i][j] = a; degX[i] += a; degY[j] += a;
    }
    for (int i = 0; i < 6; i++) if (degX[i] > curd || (xt[i] && degX[i] > 4)) { st_deg++; return 0; }
    for (int j = 0; j < 7; j++) if ((!yt[j] && degY[j] > LCY) || (yt[j] && degY[j] > 4)) { st_deg++; return 0; }
    int s[6]; memcpy(s, degX, sizeof s);
    for (int i = 0; i < 6; i++) for (int j = i + 1; j < 6; j++) if (s[j] < s[i]) { int t = s[i]; s[i] = s[j]; s[j] = t; }
    if (s[0] + s[1] + s[2] < TH) { st_three++; return 0; }
    int deg[13], e = 0;
    for (int i = 0; i < 6; i++) { deg[i] = degX[i]; e += degX[i]; }
    for (int j = 0; j < 7; j++) deg[6 + j] = degY[j];
    #define ADJ(a, b) ((a) < 6 && (b) >= 6 ? adjm[a][(b) - 6] : ((b) < 6 && (a) >= 6 ? adjm[b][(a) - 6] : 0))
    for (int a = 0; a < 13; a++) for (int b = a + 1; b < 13; b++) for (int c = b + 1; c < 13; c++) {
        int eR = ADJ(a, b) + ADJ(a, c) + ADJ(b, c);
        if (e - (deg[a] + deg[b] + deg[c] - eR) < TH) { st_ten++; return 0; }
    }
    for (int j = 0; j < 7; j++) matchY[j] = -1;
    int mm = 0;
    for (int u = 0; u < 6; u++) { int seen[7] = {0}; if (augp(u, seen, 6)) mm++; }
    if (13 - mm > 7) { st_alpha++; return 0; }
    int r[9] = {0};
    for (int i = 0; i < 6; i++) { int S = xt[i] ? (xm[i] == FREE ? 0 : 511 ^ xm[i]) : xm[i]; for (int t = 0; t < 9; t++) r[t] += S >> t & 1; }
    for (int j = 0; j < 7; j++) { int S = yt[j] ? (ym[j] == FREE ? 0 : 511 ^ ym[j]) : ym[j]; for (int t = 0; t < 9; t++) r[t] += S >> t & 1; }
    for (int t = 0; t < 9; t++) if (r[t] > 7) { st_r++; return 0; }
    return 1;
}
/* ---------- attach a=5 vertices ---------- */
static int yopts[16], nyo, xopts[16], nxo, f_, mX_, hA_;
static void attachX(int start, int left) {
    if (left == 0) {
        st_attach++;
        if (leaf_checks()) {
            st_surv++;
            if (printed < 10) {
                printed++; char b[12];
                printf(" SURV X lows"); for (int k = 0; k < nXL; k++) { fmt(XLv[k], b); printf(" %s", b); }
                printf(" X a5 T"); for (int k = 0; k < nXh; k++) { if (Xh[k] == FREE) printf(" *"); else { fmt(Xh[k], b); printf(" %s", b); } }
                printf(" | Y lows"); for (int k = 0; k < nYL; k++) { fmt(YLv[k], b); printf(" %s", b); }
                printf(" Y a5 T"); for (int k = 0; k < nYh; k++) { if (Yh[k] == FREE) printf(" *"); else { fmt(Yh[k], b); printf(" %s", b); } }
                printf("\n");
            }
        }
        return;
    }
    for (int i = start; i < nxo; i++) { Xh[nXh++] = xopts[i]; attachX(i, left - 1); nXh--; }
}
static void attachY(int start, int left) {
    if (left == 0) { nXh = 0; attachX(0, mX_); return; }
    for (int i = start; i < nyo; i++) { Yh[nYh++] = yopts[i]; attachY(i, left - 1); nYh--; }
}
static int inarr(int v, const int *a, int n) { for (int k = 0; k < n; k++) if (a[k] == v) return 1; return 0; }
static void process(void) {
    st_xleaves++;
    /* Xtypes / Ytypes */
    int xty[6], nxt = 0, yty[7], nyt = 0;
    for (int k = 0; k < nXL; k++) if (!inarr(XLv[k], xty, nxt)) xty[nxt++] = XLv[k];
    for (int k = 0; k < nYL; k++) if (!inarr(YLv[k], yty, nyt)) yty[nyt++] = YLv[k];
    nyo = 0; for (int k = 0; k < nxt; k++) if (xty[k] != A && !inarr(xty[k], yty, nyt)) yopts[nyo++] = xty[k];
    yopts[nyo++] = FREE;
    nxo = 0; for (int k = 0; k < nyt; k++) if (!inarr(yty[k], xty, nxt)) xopts[nxo++] = yty[k];
    xopts[nxo++] = FREE;
    nYh = 0; for (int k = 0; k < hA_; k++) Yh[nYh++] = A;
    attachY(0, f_);
}
/* ---------- X DFS ---------- */
static int cB[126], cpot[126], cbase[126], nc, kX, Ytypes_has[512];
static void dfs(int start, int lowc, int *ydeg, int *cnt, int need) {
    st_xnodes++;
    if (nXL - 1 == kX) { process(); return; }
    for (int ci = start; ci < nc; ci++) {
        int B = cB[ci], pot = cpot[ci], bad = 0;
        for (int k = 1; k < nXL; k++) if ((B & XLv[k]) == 0) { bad = 1; break; }
        if (bad) continue;
        int nl = lowc + (pot <= TCUT());
        if (CAPLOW_OK() && nl > 1) continue;
        int nd[7];
        for (int j = 0; j < nYL; j++) { nd[j] = ydeg[j] + ((B & YLv[j]) == 0); if (nd[j] > LCY) bad = 1; }
        if (bad) continue;
        int nn = need;
        int already = 0; for (int k = 1; k < nXL; k++) if (XLv[k] == B) already = 1;
        if (!NOPRUNE && !already && B != A && !Ytypes_has[B]) { int lo = TH - 2 * LC; nn = need + (cbase[ci] < lo ? lo - cbase[ci] : 0); if (nn > f_) continue; }
        int c2[36]; memcpy(c2, cnt, sizeof c2);
        for (int t = 0; t < 6; t++) if (++c2[PI[B][t]] > CAP) { bad = 1; break; }
        if (bad) continue;
        XLv[nXL++] = B;
        dfs(ci, nl, nd, c2, nn);
        nXL--;
    }
}
/* ---------- canonical reps of N(x) multisets under S5 on C ---------- */
static int perms[120][5], nperm = 0;
static void genperm(int *p, int k, int used) {
    if (k == 5) { memcpy(perms[nperm++], p, 5 * sizeof(int)); return; }
    for (int i = 0; i < 5; i++) if (!(used >> i & 1)) { p[k] = i; genperm(p, k + 1, used | 1 << i); }
}
static int act(int M, const int *p) { int r = M & A; for (int i = 0; i < 5; i++) if (M >> (4 + i) & 1) r |= 1 << (4 + p[i]); return r; }
static int cmpint(const void *a, const void *b) { return *(int *)a - *(int *)b; }
static int is_canon(const int *ms, int n) {  /* ms sorted ascending; canonical iff lexicographically minimal sorted image */
    for (int q = 0; q < nperm; q++) {
        int im[8]; for (int k = 0; k < n; k++) im[k] = act(ms[k], perms[q]);
        qsort(im, n, sizeof(int), cmpint);
        for (int k = 0; k < n; k++) { if (im[k] < ms[k]) return 0; if (im[k] > ms[k]) break; }
    }
    return 1;
}
/* ---------- main search ---------- */
static int Ynb[5], ndl, ycand[126], nyc, eY, mY_;
static void with_YL(void) {
    if (!q4ok(YLv, nYL)) return;
    st_ysets++;
    memset(Ytypes_has, 0, sizeof Ytypes_has);
    int maxmult = 0;
    for (int k = 0; k < nYL; k++) { Ytypes_has[YLv[k]] = 1; int c = 0; for (int l = 0; l < nYL; l++) c += YLv[l] == YLv[k]; if (c > maxmult) maxmult = c; }
    nc = 0;
    for (int q = 0; q < 126; q++) {
        int B = M4[q]; if (!(B & A)) continue;
        int b = 0; for (int j = 0; j < nYL; j++) b += (B & YLv[j]) == 0;
        int pot;
        if (B == A) { b += hA_; pot = b; } else pot = b + (Ytypes_has[B] ? 0 : f_);
        if (b > curd || (!NOPRUNE && pot < TH - 2 * LC)) continue;   /* min X-degree >= TH - LC - LC */
        cB[nc] = B; cpot[nc] = pot; cbase[nc] = b; nc++;
    }
    int low_init = (maxmult <= TCUT()) ? mX_ : 0;
    if (CAPLOW_OK() && low_init > 1) return;
    int ydeg0[7]; for (int j = 0; j < nYL; j++) ydeg0[j] = (A & YLv[j]) == 0;
    int cnt0[36] = {0};
    for (int k = 0; k < nYL; k++) for (int t = 0; t < 6; t++) cnt0[PI[YLv[k]][t]]++;
    for (int t = 0; t < 6; t++) cnt0[PI[A][t]]++;
    for (int t = 0; t < 36; t++) if (cnt0[t] > CAP) return;
    nXL = 1; XLv[0] = A;
    dfs(0, low_init, ydeg0, cnt0, 0);
}
static void yext(int start, int left) {
    if (left == 0) { with_YL(); return; }
    for (int i = start; i < nyc; i++) {
        int M = ycand[i], bad = 0;
        for (int k = ndl; k < nYL; k++) if ((M & YLv[k]) == 0) { bad = 1; break; }
        if (bad) continue;
        YLv[nYL++] = M; yext(i, left - 1); nYL--;
    }
}
static int nb[8];
static void nbrs(int start, int k, int dl, int hA) {
    if (k == dl) {
        if (!q4ok(nb, dl)) return;
        if (!is_canon(nb, dl)) return;
        st_nreps++;
        for (int mY = hA; mY <= m; mY++) {
            int mX = m - mY; int e = 7 - mY - dl;
            if (e < 0 || 6 - mX < 1) continue;
            f_ = mY - hA; kX = 5 - mX; mX_ = mX; hA_ = hA; mY_ = mY; eY = e;
            nyc = 0;
            for (int q = 0; q < 126; q++) {
                int M = M4[q], ok = (M & A) != 0;
                for (int j = 0; j < dl && ok; j++) if (!(M & nb[j])) ok = 0;
                if (hA > 0 && M == A) ok = 0;
                if (ok) ycand[nyc++] = M;
            }
            nYL = dl; memcpy(YLv, nb, dl * sizeof(int)); ndl = dl;
            yext(0, e);
        }
        return;
    }
    for (int i = start; i < 5; i++) { nb[k] = subC[i]; nbrs(i, k + 1, dl, hA); }
}
int main(int argc, char **argv) {
    m = atoi(argv[1]); CAP = argc > 2 ? atoi(argv[2]) : 3; TH = argc > 3 ? atoi(argv[3]) : 12; LC = argc > 4 ? atoi(argv[4]) : 5; NOPRUNE = argc > 5 ? atoi(argv[5]) : 0; LCY = argc > 6 ? atoi(argv[6]) : LC;
    clock_t t0 = clock();
    int k = 0;
    for (int i = 0; i < 9; i++) for (int j = i + 1; j < 9; j++) pairid[i][j] = k++;
    for (int M = 0; M < 512; M++) if (popc(M) == 4) {
        M4[n4++] = M; int t = 0;
        for (int i = 0; i < 9; i++) for (int j = i + 1; j < 9; j++) if ((M >> i & 1) && (M >> j & 1)) PI[M][t++] = pairid[i][j];
    }
    /* M4 in increasing integer order; subC = 4-subsets of {4..8}, ascending */
    int ns = 0; for (int q = 0; q < 126; q++) if ((M4[q] & A) == 0) subC[ns++] = M4[q];
    int p[5]; genperm(p, 0, 0);
    for (int d = LC; d >= 4; d--) for (int dl = 0; dl <= d; dl++) {
        int hA = d - dl; if (hA > m) continue;
        curd = d;
        nbrs(0, 0, dl, hA);
    }
    printf("profile 4^%d 5^%d 9^2  q4 cap=%d  10-set threshold=%d  low deg cap=%d%s\n", 13 - m, m, CAP, TH, LC, (CAP == 3 && TH == 12 && LC == 5 && LCY == 5 && !NOPRUNE) ? " (REAL RUN)" : " (NEGATIVE CONTROL)");
    printf("stats: nreps=%lld ysets=%lld xnodes=%lld xleaves=%lld attach=%lld deg=%lld three=%lld ten=%lld alpha=%lld r=%lld surv=%lld\n",
           st_nreps, st_ysets, st_xnodes, st_xleaves, st_attach, st_deg, st_three, st_ten, st_alpha, st_r, st_surv);
    printf("noprune=%d Ylowcap=%d\nF-level survivors: %lld\n", NOPRUNE, LCY, st_surv);
    printf("time %.1fs cpu\n", (double)(clock() - t0) / CLOCKS_PER_SEC);
    return 0;
}
