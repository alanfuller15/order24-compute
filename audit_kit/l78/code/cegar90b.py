"""Degree-free exact lazy (CEGAR) exclusion of one formula of edge layer m <= 92 (version 6, cegar90b.py: version 5,
cegar90.py SHA-256 8d65a528..., plus the families 'iso8' and 'tbip' appended at the end of the base formula, after
'swap'; with both left out the base formula is byte-identical to version 5's; BOUNDS90.md, section "Version 6").
Version 5 was version 4, cegar91.py
SHA-256 b2f00fd6..., plus the families 'b22' and 'swap' appended at the end of the base formula, after 'a22'; with
both left out (`only` without them) the base formula is byte-identical to version 4's. Reviewed by R90B; this text and
a refusal in swap() of an index that cannot occur were changed after the review, no clause changed).
Version 4 was version 3 (cegar92.py, SHA-256 63bddfbc...) plus the family 'a22'.

Setting. G is a graph on 24 vertices that is triangle-free, has alpha(G) <= 8 (hence Delta(G) <= 8) and every 12-set
spanning >= 12 edges, with e(G) = m. Two further properties are assumed (each with its own proof, outside this file):
  saturated   every two non-adjacent vertices have a common neighbour (V8 Theorem A, given that layer m + 1 has no
              such graph: otherwise G + uv would be one);
  mindeg      every vertex has degree >= 4 (V8 Theorem B, for saturated graphs; Lean four_le_degree).
(S, T) is a maximum cut of G with |S| = s <= |T| = t = 24 - s, chosen with |S| as large as possible among the maximum
cuts with |S| <= |T|. Its profile (s, a, b, c) = (|S|, e(S), e(T), e(S, T)) is one of uprofiles.profiles(m), and G[S]
is isomorphic to the catalogue graph H (triangle-free, Delta <= 4, alpha <= 8). Unlike the layer-93 encoders, the
degrees are not fixed: there is one formula per (profile, H).

Labels: S = 0..s-1 as in H; T = s..23. Every clause family below is a necessary condition for such a G, labelled
with S as in H and T in the order chosen by "lex":
  triangles   S-S-T, S-T-T and T-T-T triangles are forbidden (H is triangle-free)
  S degrees   for k in S: d_T(k) >= d_S(k) (moving k to T cannot raise the cut), d(k) >= 4, d(k) <= 8
  T degrees   for v in T: 4 <= d(v) <= 8, and d_T(v) <= d_S(v) - 1 if s <= 11 ("strict": if d_T(v) = d_S(v),
              (S + v, T - v) would be a maximum cut with s + 1 <= 23 - s, so |S| was not largest), d_T(v) <= d_S(v)
              if s = 12
  totals      e(T) = b and e(S, T) = c
  floors      e(W) >= 12 on W = S + R and W = T - R for every R in T with |R| = 12 - s; if s = 12, also on
              S - k + v and T - v + k for every k in S, v in T (both sides of every one-vertex swap)
  lex         the S-incidence columns of the T-vertices are lexicographically non-increasing (row 0 most
              significant). Sound: fix the labelling of S first (any isomorphism G[S] -> H; the 'isolates' family
              below chooses one), then label T so that the columns are sorted. Every family except 'isolates' holds
              under every relabelling of T (each lazy clause states alpha <= 8 or a floor for one set, true for every
              set; b22 speaks only of degrees and adjacency, and a relabelling of T only permutes swap's clauses: review
              R90B), and the 'isolates' clauses hold for every sorted order of T (review R3), so the sorted labelling
              satisfies them all
  saturation  every pair not forced adjacent is an edge or has a common neighbour (one auxiliary variable per
              candidate common neighbour, implying both edges)
  arithmetic  (redundant) unary counters u[j] <-> (count >= j) for d_T(v), d_S(v) (v in T) and d_T(k) (k in S), the
              per-vertex links (strict / non-strict, d <= 8, d >= 4) on them, and the double counts
              sum_T d_T(v) = 2b, sum_T d_S(v) = c, sum_S d_T(k) = c. Implied by the families above (the counters are
              defined by equivalences), so they exclude nothing; they give the solver the degree sums directly
  symmetry    (s = 12 only) inv(G[T]) >=lex inv(H), inv = (N_4, N_3, N_2, N_1), N_k = number of vertices of degree
              >= k in the side graph. Sound: when s = 12, (T, S) is also a maximum cut with |T| = 12 as large as
              possible, every family above holds for it as for (S, T) (both sides have 12 vertices and
              a = b = 12 edges; Delta <= 4 on both sides), and G[T] is triangle-free with 12 edges, Delta <= 4 and
              alpha <= 8, so it is isomorphic to a catalogue graph H'. If inv(G[T]) < inv(H), the graph G with the
              cut (T, S) satisfies the formula of H' instead, so excluding it here loses nothing. Clauses for
              s <= 11 are unchanged
  isolates    (profile (11,8,15,69) only, for templates H whose isolated vertices are exactly 0..r-1 with r >= 3:
              60 of the 204; the clauses use the counters dX, dT, so they need the arithmetic family) Degree counting
              gives sum_S (8 - d) = 3, sum_T (8 - d) = 5, and the strict condition gives d_T <= 3 on T.
              (i) d(j) >= t => d(0) >= t for every isolate j: an isolate of largest degree is labelled 0 (any
              permutation of H's isolated vertices is an automorphism of H, and S is labelled before T is sorted).
              (ii) d(0) = 8 => N(0) = T-indices 0..7 (the sort puts row 0 first), W = T-indices 8..12 is independent and
              every w in W has d_T(w) >= 3 (V11's R92-11: U = N(0) is independent, so 15 = e(T) <= sum_W d_T(w) - e(W)
              <= 15 - e(W)). (iii) r >= 4: d(0) = 8 (only 3 deficit units on S); r = 3 and d(0) <= 7: the three
              isolates have degree 7 and every other S-vertex has degree 8. Reviewed by R3 (sound)
  a22         (only when m - c = 23, i.e. beta(G) = 23 for the maximum cut) delta(G) >= 6, and for every edge xy:
              d(x) = 6 => d(y) = 8. Sound by A22 (a(22) <= 17, OEIS A389646, McKay) and Lemma V (beta(G) <=
              beta(G - v) + floor(d(v)/2)) applied twice: for all v != u, 23 = beta(G) <= 17 + floor(d(v)/2) +
              floor(d_{G-v}(u)/2), so floor(d(v)/2) + floor(d_{G-v}(u)/2) >= 6. With all degrees <= 8: d(v) <= 5
              would need d_{G-v}(u) >= 8 for every u != v (>= 10 if d(v) <= 3, impossible), and for d(v) in {4, 5}
              a neighbour u of v has d_{G-v}(u) = d(u) - 1 <= 7; so delta >= 6. If d(v) in {6, 7}, every neighbour
              u of v has d(u) - 1 = d_{G-v}(u) >= 6. Hence for an edge xy with d(x) = 6: d(y) >= 7, and taking
              v = y if d(y) = 7 gives d(x) >= 7, a contradiction; so d(y) = 8.
              Encoded with unary total-degree counters tot[x][j] <-> d(x) >= j (j <= 8): clauses tot[x][6], and
              (not xy) or tot[x][7] or tot[y][8], and (not xy) or tot[y][7] or tot[x][8]
  b22         (version 5; only when m - c = 22, i.e. beta(G) = 22 for the maximum cut) at most one vertex has degree
              <= 5; a vertex of degree 5 has all neighbours of degree >= 7; a vertex of degree 4 has all neighbours of
              degree 8. Sound by A22 and Lemma V twice, as for a22: for all v != u, 22 = beta(G) <= 17 +
              floor(d(v)/2) + floor(d_{G-v}(u)/2), so floor(d(v)/2) + floor(d_{G-v}(u)/2) >= 5. With 4 <= d <= 8:
              d(v) in {4, 5} needs d_{G-v}(u) >= 6 for every u != v, i.e. d(u) >= 7 for a neighbour u and d(u) >= 6
              for a non-neighbour (so no second vertex of degree <= 5); d(v) in {6, 7} needs d(u) >= 5 for every
              neighbour u (so a vertex of degree 4 has no neighbour of degree 6 or 7: with the line above, all its
              neighbours have degree 8); d(v) = 8 needs nothing. Conversely the three statements give the pairwise
              condition (BOUNDS90.md), so the clauses state exactly its consequence. Encoded with the total-degree
              counters tot[x][j] <-> d(x) >= j: tot[x][6] or tot[y][6] for every pair; (not xy) or tot[x][6] or
              tot[y][7], and (not xy) or tot[x][5] or tot[y][8], both ways round, for every pair not forced apart
  swap        (version 5; needs the arithmetic counters) exchanging k in S and v in T keeps |S| and so cannot raise
              the cut: (d_T(k) - d_S(k)) + (d_S(v) - d_T(v)) >= 2 [kv an edge]. With the one-vertex conditions
              (d_T(k) >= d_S(k), and d_S(v) >= d_T(v) + 1 if s <= 11, >= d_T(v) if s = 12) this excludes exactly: kv an
              edge, d_T(k) - d_S(k) = a and d_S(v) - d_T(v) = 1 - a or less, for a in {0, 1}. d_S(k) is H's degree.
              Encoded, for every k in S, v in T, a in {0, 1} (a = 1 only if s = 12) and j = d_T(v) in 0..7:
              (not kv) or [d_T(k) != d_S(k) + a] or [d_T(v) != j] or d_S(v) >= j + 2 - a
  iso8        (version 6; s <= 11; needs the arithmetic counters) for every vertex k of S isolated in H: if
              d_T(k) = 8, then U = N(k) is an independent 8-set in T (no triangle), and with W = T - U and d_T <= 3 on
              T (the strict condition and d <= 8): b = e(U, W) + e(W) = sum_W d_T(w) - e(W) <= 3|W| - e(W). So if
              b > 3(t - 8), no isolated k has d_T(k) = 8 (clause not dX[k][8]); if b = 3(t - 8), d_T(k) = 8 forces W
              independent and d_T(w) = 3 for every w in W (clauses: not dX[k][8] or kv or kw or not vw, for v, w in T;
              not dX[k][8] or kw or dT[w][3], for w in T). Nothing for b < 3(t - 8). (V22 Theorem II and V23's note
              on (10,4,18,68) use the same count.)
  tbip        (version 6; only s = 11, e(S) = 7, c >= 67, b + c >= 83) G[T] is bipartite: review V20_STUDY.md,
              T-BIPARTITE-7 (d_S(t) >= 5 from the floor on S + t; an odd cycle of length 2k + 1 in T needs
              5(2k + 1) <= 11k, so k >= 5; a 13-cycle gives c <= 66; an 11-cycle is chordless, takes exactly 55
              cross edges and leaves b + c <= 82). Encoded with a colour variable per vertex of T (the first one
              fixed true): for every pair u, v of T, (not uv) or col[u] or col[v], and (not uv) or not col[u] or
              not col[v]
  lazy        alpha(G) <= 8 (9-sets) and e(W) >= 12 (12-sets), added from the models found (CEGAR), in order
The final formula is the base formula followed by the lazy clauses; rebuild() reproduces it byte for byte from
(profile, H, lazy list).
Usage: MASKS12=... python3 -I cegar91.py FORMULAS.json TAG [outdir]"""
import sys, os, json, time, subprocess, itertools as it
import numpy as np
import networkx as nx
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

MINDEG = 4

def need(cond, msg):
    if not cond: raise ValueError(msg)                 # explicit checks, not removed by python -O

_M = None
def masks12():
    global _M
    if _M is None:
        p = os.environ.get('MASKS12', '/nonexistent')
        if os.path.exists(p): _M = np.load(p)
        else: _M = np.fromiter((sum(1 << v for v in c) for c in it.combinations(range(24), 12)), dtype=np.uint32, count=2704156)
        need(len(_M) == 2704156, 'mask table')
    return _M

def check_formula(f):
    """explicit consistency checks of one formula record (profile, H)"""
    s, a, b, c, m = f['s'], f['a'], f['b'], f['c'], f['m']
    e = [tuple(x) for x in f['h_edges']]
    need(isinstance(s, int) and 9 <= s <= 12 and a + b + c == m, 'bad profile')
    need(all(0 <= u < v < s for u, v in e) and len(set(e)) == len(e) == a, 'bad H edges')
    adj = [set() for _ in range(s)]
    for u, v in e: adj[u].add(v); adj[v].add(u)
    need(all(len(x) <= 4 for x in adj), 'H has a vertex of degree > 4')
    need(not any(adj[u] & adj[v] for u, v in e), 'H has a triangle')

FAMILIES = ('triangles', 'sdeg', 'tdeg', 'totals', 'floors', 'lex', 'saturation', 'arith', 'symmetry', 'isolates', 'a22', 'b22', 'swap',
            'iso8', 'tbip')
INV_DEGREES = (4, 3, 2, 1)

def side_invariant(deg):
    """(N_4, N_3, N_2, N_1), N_k = number of vertices of degree >= k: an isomorphism invariant of a side graph
    (degrees <= 4 on both sides when s = 12), compared lexicographically"""
    return tuple(sum(1 for d in deg if d >= k) for k in INV_DEGREES)

def build(f, only=None):
    """the base formula; `only` (a set of family names, for validation) keeps just those families, in the same order"""
    check_formula(f)
    on = (lambda fam: True) if only is None else (lambda fam: fam in only)
    s, b, c = f['s'], f['b'], f['c']; strict = s <= 11
    S = list(range(s)); T = list(range(s, 24))
    sedges = {tuple(x) for x in f['h_edges']}
    hadj = {k: sorted(w for w in S if (min(k, w), max(k, w)) in sedges) for k in S}
    sdeg = [len(hadj[k]) for k in S]
    pool = IDPool(); cnf = CNF(); E = {}
    for u, v in it.combinations(S, 2): E[u, v] = (u, v) in sedges
    for k in S:
        for v in T: E[k, v] = pool.id(('x', k, v))
    for u, v in it.combinations(T, 2): E[u, v] = pool.id(('e', u, v))
    L = lambda u, v: E[min(u, v), max(u, v)]
    def card(lits, lo=None, hi=None):
        need(all(not isinstance(l, bool) for l in lits), 'constant in a cardinality constraint')
        if lo is not None and lo > 0:
            if lo > len(lits): cnf.append([]); return
            cnf.extend(CardEnc.atleast(lits, bound=lo, vpool=pool, encoding=EncType.seqcounter).clauses)
        if hi is not None and hi < len(lits):
            if hi < 0: cnf.append([]); return
            cnf.extend(CardEnc.atmost(lits, bound=hi, vpool=pool, encoding=EncType.seqcounter).clauses)
    # triangles
    if on('triangles'):
        for k1, k2 in sorted(sedges):
            for v in T: cnf.append([-L(k1, v), -L(k2, v)])
        for u, v in it.combinations(T, 2):
            for k in S: cnf.append([-L(u, v), -L(k, u), -L(k, v)])
        for u, v, w in it.combinations(T, 3): cnf.append([-L(u, v), -L(v, w), -L(u, w)])
    # S degrees
    for k in (S if on('sdeg') else []):
        card([L(k, v) for v in T], max(sdeg[k], MINDEG - sdeg[k]), 8 - sdeg[k])
    # T degrees
    tl = {v: [L(v, w) for w in T if w != v] for v in T}
    for v in (T if on('tdeg') else []):
        card([L(k, v) for k in S] + tl[v], MINDEG, 8)
        card(tl[v] + [-L(k, v) for k in S], None, s - 1 if strict else s)     # d_T(v) + (s - d_S(v)) <= s - [strict]
    # totals
    if on('totals'):
        card([L(u, v) for u, v in it.combinations(T, 2)], b, b)
        card([L(k, v) for k in S for v in T], c, c)
    # floors
    def floor12(W):
        ls = [L(p, q) for p, q in it.combinations(sorted(W), 2)]
        card([l for l in ls if not isinstance(l, bool)], 12 - sum(1 for l in ls if l is True))
    for R in (it.combinations(T, 12 - s) if on('floors') else []):
        floor12(S + list(R)); floor12([v for v in T if v not in R])
    if s == 12 and on('floors'):
        for k in S:
            for v in T:
                floor12([w for w in S if w != k] + [v]); floor12([w for w in T if w != v] + [k])
    # lex-leader on the S-incidence columns of T
    for v, w in (zip(T, T[1:]) if on('lex') else []):
        eq_prev = None
        for k in S:
            xv, xw = L(k, v), L(k, w)
            cnf.append(([-eq_prev] if eq_prev else []) + [-xw, xv])
            eq = pool.id(('lexeq', v, w, k))
            if eq_prev: cnf.append([-eq, eq_prev])
            cnf.append([-eq, -xv, xw]); cnf.append([-eq, xv, -xw])
            cnf.append([eq] + ([-eq_prev] if eq_prev else []) + [-xv, -xw])
            cnf.append([eq] + ([-eq_prev] if eq_prev else []) + [xv, xw])
            eq_prev = eq
    # saturation
    def conj(p, q, key):
        z = pool.id(key); cnf.append([-z, p]); cnf.append([-z, q]); return z
    sat_on = on('saturation')
    for x, y in (it.combinations(S, 2) if sat_on else []):
        if (x, y) in sedges or set(hadj[x]) & set(hadj[y]): continue
        cnf.append([conj(L(x, v), L(y, v), ('sat_ss', x, y, v)) for v in T])
    for x in (S if sat_on else []):
        for v in T:
            cl = [L(x, v)] + [L(w, v) for w in hadj[x]]
            cl += [conj(L(x, z), L(z, v), ('sat_st', x, z, v)) for z in T if z != v]
            cnf.append(cl)
    for v, w in (it.combinations(T, 2) if sat_on else []):
        cl = [L(v, w)] + [conj(L(x, v), L(x, w), ('sat_tts', x, v, w)) for x in S]
        cl += [conj(L(v, z), L(w, z), ('sat_ttt', z, v, w)) for z in T if z != v and z != w]
        cnf.append(cl)
    # arithmetic (redundant)
    def OR(p, q):
        if p is True or q is True: return True
        if p is False: return q
        if q is False: return p
        z = pool.id(('or', p, q)); cnf.extend([[-z, p, q], [-p, z], [-q, z]]); return z
    def AND(p, q):
        if p is False or q is False: return False
        if p is True: return q
        if q is True: return p
        z = pool.id(('and', p, q)); cnf.extend([[-z, p], [-z, q], [-p, -q, z]]); return z
    def unary(lits):                                   # u[j] <-> (number of true literals >= j), j = 0..8
        u = [True] + [False] * 8
        for x in lits: u = [True] + [OR(u[j], AND(x, u[j - 1])) for j in range(1, 9)]
        return u
    def neg(p): return (not p) if isinstance(p, bool) else -p
    def clause(*ps):
        if any(p is True for p in ps): return
        cnf.append([p for p in ps if p is not False])
    def a22():                                         # version 4: beta(G) = 23 (m - c = 23); A22 and Lemma V twice
        if f['m'] - c != 23 or not on('a22'): return
        V = S + T
        tot = {x: unary([L(x, y) for y in V if y != x]) for x in V}     # tot[x][j] <-> d(x) >= j, j = 0..8
        for x in V: clause(tot[x][6])                                    # delta >= 6
        for x, y in it.combinations(V, 2):
            if L(x, y) is False: continue
            clause(neg(L(x, y)), tot[x][7], tot[y][8])                   # d(x) = 6 and xy an edge => d(y) = 8
            clause(neg(L(x, y)), tot[y][7], tot[x][8])
    def b22():                                         # version 5: beta(G) = 22 (m - c = 22); A22 and Lemma V twice
        if f['m'] - c != 22 or not on('b22'): return
        V = S + T
        tot = {x: unary([L(x, y) for y in V if y != x]) for x in V}     # tot[x][j] <-> d(x) >= j, j = 0..8
        for x, y in it.combinations(V, 2):
            clause(tot[x][6], tot[y][6])                                 # at most one vertex of degree <= 5
            if L(x, y) is False: continue
            clause(neg(L(x, y)), tot[x][6], tot[y][7])                   # d(x) <= 5 and xy an edge => d(y) >= 7
            clause(neg(L(x, y)), tot[y][6], tot[x][7])
            clause(neg(L(x, y)), tot[x][5], tot[y][8])                   # d(x) <= 4 and xy an edge => d(y) = 8
            clause(neg(L(x, y)), tot[y][5], tot[x][8])
    def tbip():                                        # version 6: G[T] bipartite (V20 T-BIPARTITE-7)
        if not (on('tbip') and s == 11 and f['a'] == 7 and c >= 67 and b + c >= 83): return
        col = {v: pool.id(('tcol', v)) for v in T}
        clause(col[T[0]])
        for u, v in it.combinations(T, 2):
            clause(neg(L(u, v)), col[u], col[v]); clause(neg(L(u, v)), -col[u], -col[v])
    def swap():                                        # version 5: exchanging k in S and v in T cannot raise the cut
        if not (on('swap') and on('arith')): return
        for k in S:
            for v in T:
                for a in ((0,) if strict else (0, 1)):
                    lo = sdeg[k] + a                                     # d_T(k) = lo exactly
                    need(lo + 1 <= 8, 'swap: counter index out of range')   # R90B should-fix 1 (lo <= 5 at m = 90)
                    for j in range(8):                                   # d_T(v) = j exactly
                        need_s = j + 2 - a                               # then d_S(v) >= j + 2 - a
                        clause(neg(L(k, v)), neg(dX[k][lo]), dX[k][lo + 1],
                               neg(dT[v][j]), dT[v][j + 1], dS[v][need_s] if need_s <= 8 else False)
    if not (on('arith') or on('symmetry')):
        a22(); b22(); tbip(); return pool, cnf, E
    dT = {v: unary(tl[v]) for v in T}                  # shared by the arithmetic and symmetry families
    if on('arith'):
        dS = {v: unary([L(k, v) for k in S]) for v in T}
        dX = {k: unary([L(k, v) for v in T]) for k in S}
        for v in T:
            for j in range(1, 9):
                nd = j + 1 if strict else j
                clause(neg(dT[v][j]), dS[v][nd] if nd <= 8 else False)          # d_T >= j -> d_S >= j + [strict]
                clause(neg(dT[v][j]), neg(dS[v][9 - j]))                          # d_T + d_S <= 8
            for j in range(MINDEG):
                clause(dT[v][j + 1], dS[v][MINDEG - j])                           # d_T <= j -> d_S >= 4 - j
        def total(us, n):
            ls = [x for u in us for x in u[1:] if not isinstance(x, bool)]
            card(ls, n - sum(1 for u in us for x in u[1:] if x is True), n - sum(1 for u in us for x in u[1:] if x is True))
        total([dT[v] for v in T], 2 * b)
        total([dS[v] for v in T], c)
        total([dX[k] for k in S], c)
    # isolates (profile (11,8,15,69) only; uses the counters dX and dT; V11's R92-11 and its degree count)
    iso = [k for k in S if sdeg[k] == 0]
    if (s, f['a'], b, c) == (11, 8, 15, 69) and on('isolates') and on('arith') and len(iso) >= 3 and iso == list(range(len(iso))):
        for j in iso[1:]:                                # an isolate of largest degree is labelled 0
            for t in range(1, 9): clause(neg(dX[j][t]), dX[0][t])
        A = dX[0][8]                                     # branch A: vertex 0 has degree 8 (all in T)
        Wt = T[8:]
        for j, v in enumerate(T): clause(neg(A), L(0, v) if j < 8 else neg(L(0, v)))    # lex puts N(0) first
        for u, v in it.combinations(Wt, 2): clause(neg(A), neg(L(u, v)))                 # W independent
        for w in Wt: clause(neg(A), dT[w][3])                                            # W cubic in T
        if len(iso) >= 4: clause(A)                      # deficit 3 < number of isolates: one isolate is regular
        else:                                            # branch B: three isolates of degree 7, all others regular
            for j in iso: clause(A, dX[j][7])
            for k in S:
                if sdeg[k]: clause(A, dX[k][8 - sdeg[k]])
    # symmetry (s = 12 only; uses the counters dT)
    if s == 12 and on('symmetry'):
        need(f['a'] == b, 'symmetry needs e(S) = e(T)')
        hinv = side_invariant(sdeg)
        def unary_all(lits):                           # w[j] <-> (number of true literals >= j), j = 0..len
            w = [True] + [False] * len(lits)
            for x in lits: w = [True] + [OR(w[j], AND(x, w[j - 1])) for j in range(1, len(lits) + 1)]
            return w
        prefix = []
        for k, ck in zip(INV_DEGREES, hinv):
            w = unary_all([dT[v][k] for v in T])      # w[j] <-> N_k(G[T]) >= j
            clause(*prefix, w[ck])                     # earlier levels equal -> N_k(G[T]) >= N_k(H)
            prefix.append(w[ck + 1] if ck + 1 < len(w) else False)
    def iso8():                                        # version 6: an isolated S vertex of T-degree 8
        if not (on('iso8') and on('arith') and strict): return
        W8 = len(T) - 8
        for k in S:
            if sdeg[k] != 0: continue
            if b > 3 * W8: clause(neg(dX[k][8])); continue
            if b < 3 * W8: continue
            for u, w in it.combinations(T, 2): clause(neg(dX[k][8]), L(k, u), L(k, w), neg(L(u, w)))
            for w in T: clause(neg(dX[k][8]), L(k, w), dT[w][3])
    a22(); b22(); swap(); iso8(); tbip()
    return pool, cnf, E

def lazy_clauses(item, E, pool):
    W = item['W']
    need(W == sorted(set(W)) and all(isinstance(w, int) and 0 <= w < 24 for w in W), ('malformed lazy set', W))
    ls = [E[p, q] for p, q in it.combinations(W, 2)]
    free = [l for l in ls if not isinstance(l, bool)]; const = sum(1 for l in ls if l is True)
    if item['kind'] == 9:
        need(len(W) == 9 and const == 0, ('bad 9-set', W))
        return [free]
    need(item['kind'] == 12 and len(W) == 12, ('bad 12-set', W))
    bound = 12 - const
    need(0 < bound <= len(free), ('bad bound', W))
    return CardEnc.atleast(free, bound=bound, vpool=pool, encoding=EncType.seqcounter).clauses

def rebuild(f, lazy):
    pool, cnf, E = build(f)
    for item in lazy: cnf.extend(lazy_clauses(item, E, pool))
    return cnf

def external_solve(cad, cnf, path, proof, opts=()):
    """solve the formula with an external CaDiCaL that writes an LRAT proof: ('UNSAT', None) or ('SAT', model set)"""
    cnf.to_file(path)
    p = subprocess.run([cad, '-q', '--lrat=true'] + list(opts) + [path, proof], capture_output=True, text=True, env={})
    if p.returncode == 20: return 'UNSAT', None
    need(p.returncode == 10, ('external solver failed', p.returncode, p.stderr[-200:]))
    mdl = set()
    for line in p.stdout.splitlines():
        if line.startswith('v '): mdl.update(int(x) for x in line[2:].split() if int(x) > 0)
    if os.path.exists(proof): os.remove(proof)
    return 'SAT', mdl

def run(f, outdir=None, per_iter=60, budget_s=None, hybrid=None):
    """CEGAR to UNSAT. Without `hybrid`, every iteration is solved by PySAT's CaDiCaL 1.9.5 (incremental), as before.
    With hybrid = {'cad': path, 'conf': N, 'opts': [...], 'grow': g} each iteration first gets N conflicts in PySAT; if
    that is not enough, the current formula is written to OUTDIR/TAG.cnf and solved by the external CaDiCaL with an LRAT
    proof (OUTDIR/TAG.lrat): a model continues the loop (and the budget is multiplied by g, default 4, so that this
    formula's later model-finding iterations stay in the incremental solver), UNSAT ends it and res['proof'] names the
    proof of exactly the final formula. This avoids solving the hard last iteration twice (once here, once for the proof). How the lazy list is
    found plays no part in correctness: rebuild() regenerates the final formula from it, and the proof is checked."""
    t0 = time.time(); pool, cnf, E = build(f); tag = f['tag']
    base = len(cnf.clauses); sol = Solver(name='cadical195', bootstrap_with=cnf.clauses)
    M = masks12(); lazy = []; n9 = n12 = 0; itn = 0; seen = set(); log = []; conf = hybrid['conf'] if hybrid else None
    while True:
        itn += 1
        if budget_s and time.time() - t0 > budget_s: res = {'status': 'UNKNOWN_BUDGET'}; break
        ti = time.time()
        if hybrid:
            sol.conf_budget(conf); ans = sol.solve_limited()
        else:
            ans = sol.solve()
        how = 'pysat'
        if ans is None:
            os.makedirs(outdir, exist_ok=True)
            st, mdl = external_solve(hybrid['cad'], cnf, os.path.join(outdir, f'{tag}.cnf'),
                                     os.path.join(outdir, f'{tag}.lrat'), hybrid.get('opts', ()))
            ans = st == 'SAT'; how = 'external'
            if ans: conf *= hybrid.get('grow', 4)
        log.append((how, round(time.time() - ti, 2)))
        if not ans:
            res = {'status': 'UNSAT'}
            if how == 'external': res['proof'] = os.path.join(outdir, f'{tag}.lrat')
            break
        if how == 'pysat': mdl = set(l for l in sol.get_model() if l > 0)
        adj = [k for k, l in E.items() if l is True or (not isinstance(l, bool) and l in mdl)]
        am = [0] * 24
        for u, v in adj: am[u] |= 1 << v; am[v] |= 1 << u
        need(all(am[u] & am[v] == 0 for u, v in adj), 'triangle in a model')
        g = nx.Graph(); g.add_nodes_from(range(24)); g.add_edges_from(adj); new = []
        for clq in nx.find_cliques(nx.complement(g)):
            if len(clq) >= 9:
                new.append({'kind': 9, 'W': sorted(clq)[:9]})
                if len(new) >= per_iter: break
        cnt = np.zeros(len(M), dtype=np.int16)
        for v in range(24): cnt += (((M >> v) & 1) * np.bitwise_count(M & np.uint32(am[v]))).astype(np.int16)
        cnt //= 2; bad = np.nonzero(cnt < 12)[0]
        for idx in bad[np.argsort(cnt[bad], kind='stable')][:per_iter]:
            mk = int(M[idx]); new.append({'kind': 12, 'W': [v for v in range(24) if mk >> v & 1]})
        if not new: res = {'status': 'ORIGINAL_MODEL_FOUND', 'edges': sorted(adj)}; break
        for item in new:
            key = (item['kind'], tuple(item['W']))
            need(key not in seen, 'a lazy constraint was violated after it was added'); seen.add(key)
            cl = lazy_clauses(item, E, pool)
            for k in cl: sol.add_clause(k)
            cnf.extend(cl); lazy.append(item)
            if item['kind'] == 9: n9 += 1
            else: n12 += 1
    sol.delete()
    res.update({'tag': tag, 'iterations': itn, 'floors_added': n12, 'nine_added': n9, 'base_clauses': base,
                'final_vars': pool.top, 'final_clauses': len(cnf.clauses), 'seconds': round(time.time() - t0, 2),
                'iteration_log': log})
    if res['status'] == 'UNSAT': res['lazy'] = lazy
    if outdir and res['status'] == 'UNSAT' and 'proof' not in res:
        os.makedirs(outdir, exist_ok=True); cnf.to_file(os.path.join(outdir, f'{tag}.cnf'))
    return res

if __name__ == '__main__':
    F = json.load(open(sys.argv[1])); f = F[sys.argv[2]]
    r = run(f, sys.argv[3] if len(sys.argv) > 3 else None)
    print(json.dumps({k: v for k, v in r.items() if k not in ('edges', 'lazy')}), flush=True)
    if r['status'] == 'ORIGINAL_MODEL_FOUND': json.dump(r, open(f"MODEL_{sys.argv[2]}.json", 'w'))
