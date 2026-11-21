"""RA9X12 independent re-encoding (standard library only; written from MATH.md, not from model_1nines.py).

Profile 4^s 5^m 9 (Case A, n_9 = 1, s + m = 14). I = {0..8} = N(v). F = the 14 outside vertices other than v,
slots 0..s-1 low (a = 4), slots s..13 high (a = 5).
Variables: e(k,i) = [i in M_k]; y(k,l) = [k ~ l] for EVERY pair k < l in F (high-high pairs included, not
assumed absent). Constraints (each necessary for a real G of the profile, with the MATH.md source):
 (E)  |M_k| = a_k                                          profile definition (section 4)
 (T1) y(k,l) <-> M_k, M_l disjoint                         Theorem 1, 4b.2  (=> by (F1), <= by (MAX),(S2),(S3))
 (DG) a_k + #{l : y(k,l)} <= 9                             (R3) Delta <= 9; v not adjacent to F ((P11) isolation
                                                           of a = 9 vertices), N(i) in O (F4) so deg(k)=a_k+d_F(k)
 (RI) #{k : e(k,i)} <= 8                                   (F5): deg(i) <= 9 and i ~ v
 (MX) for i notin M_k some F-neighbour l of k has i in M_l  (MAX) for the non-adjacent pair (k,i), common
                                                           neighbour w in O (F4), w != v (v has no O-neighbour)
 (Q4) #{low k : {i,j} subset M_k} <= 3                     4h.1 (M1 in pure Case A)
 (TW) for every 11-subset X of F: e(X) >= THR (=12)        12-set rule for X u {v}: v isolated from O, so
                                                           e(X u {v}) = e(X)  (section 1 + (P11))
 (SB) symmetry: within the low slots and within the high slots the 0/1 vectors (e(k,0),...,e(k,8)) are
      lexicographically NON-INCREASING (1 > 0, position 0 first); low slot 0 = {0,1,2,3}.
      Sound: S_9 acts on I and preserves (E)-(TW); slots of equal a are interchangeable. Map any low mask to
      {0,1,2,3}; this is the lex-largest 4-set in this order (any other 4-set first differs from it at a
      position <= 3 where it has a 0), so after sorting it is slot 0.
Cardinality constraints: own Sinz sequential counters (at-most: upward-implied counter; at-least: downward).
Usage: gen_mine.py m out.cnf [--thr T] [--fix JSONMASKS]
"""
import itertools as it, sys, json

m = int(sys.argv[1]); out = sys.argv[2]
THR = int(sys.argv[sys.argv.index('--thr') + 1]) if '--thr' in sys.argv else 12
FIX = json.load(open(sys.argv[sys.argv.index('--fix') + 1])) if '--fix' in sys.argv else None
s = 14 - m; n = 14
a = [4] * s + [5] * m
nv = 0
def new():
    global nv
    nv += 1
    return nv
C = []
e = [[new() for i in range(9)] for k in range(n)]
y = {}
for k, l in it.combinations(range(n), 2):
    y[(k, l)] = new()
def Y(k, l):
    return y[(min(k, l), max(k, l))]

def atmost(lits, K):
    """sum(lits) <= K. r[j][c] (c = 1..K+1) is forced true when >= c of lits[0..j] are true."""
    N = len(lits)
    if K >= N:
        return
    if K < 0:
        C.append([]); return
    r = [[new() for c in range(K + 2)] for j in range(N)]   # index c used for 1..K+1
    for j in range(N):
        x = lits[j]
        C.append([-x, r[j][1]])
        if j > 0:
            for c in range(1, K + 2):
                C.append([-r[j - 1][c], r[j][c]])
                if c >= 2:
                    C.append([-x, -r[j - 1][c - 1], r[j][c]])
    C.append([-r[N - 1][K + 1]])

def atleast(lits, K):
    """sum(lits) >= K. t[j][c] (c = 1..K) implies >= c of lits[0..j] are true."""
    N = len(lits)
    if K <= 0:
        return
    if K > N:
        C.append([]); return
    t = [[new() for c in range(K + 1)] for j in range(N)]
    for j in range(N):
        x = lits[j]
        for c in range(1, K + 1):
            if j == 0:
                C.append([-t[0][c], x] if c == 1 else [-t[0][c]])
            else:
                C.append([-t[j][c], t[j - 1][c], x])
                if c >= 2:
                    C.append([-t[j][c], t[j - 1][c], t[j - 1][c - 1]])
                else:
                    pass   # t[j][1] -> t[j-1][1] or x : covered by the first clause
    C.append([t[N - 1][K]])

# (E) exact mask sizes, direct encoding
for k in range(n):
    for S in it.combinations(range(9), a[k] + 1):
        C.append([-e[k][i] for i in S])
    for S in it.combinations(range(9), 9 - a[k] + 1):
        C.append([e[k][i] for i in S])
# (T1)
for (k, l), v_ in y.items():
    ws = []
    for i in range(9):
        C.append([-v_, -e[k][i], -e[l][i]])
        w = new(); C.append([-w, e[k][i]]); C.append([-w, e[l][i]]); ws.append(w)
    C.append([v_] + ws)
# (DG)
for k in range(n):
    atmost([Y(k, l) for l in range(n) if l != k], 9 - a[k])
# (RI)
for i in range(9):
    atmost([e[k][i] for k in range(n)], 8)
# (MX)
for k in range(n):
    for i in range(9):
        zs = []
        for l in range(n):
            if l == k:
                continue
            z = new(); C.append([-z, Y(k, l)]); C.append([-z, e[l][i]]); zs.append(z)
        C.append([e[k][i]] + zs)
# (Q4)
for i, j in it.combinations(range(9), 2):
    ps = []
    for k in range(s):
        p = new(); C.append([-e[k][i], -e[k][j], p]); ps.append(p)
    atmost(ps, 3)
# (TW)
for X in it.combinations(range(n), 11):
    atleast([Y(k, l) for k, l in it.combinations(X, 2)], THR)
# (SB)
def lex_ge(A, B):
    eq = new(); C.append([eq])
    for t in range(9):
        C.append([-eq, A[t], -B[t]])
        if t < 8:
            nx = new()
            C.append([-eq, -A[t], -B[t], nx])
            C.append([-eq, A[t], B[t], nx])
            eq = nx
for grp in (range(0, s), range(s, n)):
    g = list(grp)
    for k1, k2 in zip(g, g[1:]):
        lex_ge(e[k1], e[k2])
if FIX is None:
    for i in range(9):
        C.append([e[0][i]] if i < 4 else [-e[0][i]])
else:
    for k in range(n):
        for i in range(9):
            C.append([e[k][i]] if i in FIX[k] else [-e[k][i]])
with open(out, 'w') as fh:
    fh.write(f"p cnf {nv} {len(C)}\n")
    for c in C:
        fh.write(' '.join(map(str, c)) + ' 0\n')
print(f"mine m={m} thr={THR} fix={'yes' if FIX else 'no'} vars={nv} clauses={len(C)} empty={sum(1 for c in C if not c)}")
