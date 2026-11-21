"""exp:A9-A-1nines task (b): finite model for the 8 pure Case A profiles 4^s 5^m 9 (n_9 = 1, s + m = 14).
Written from scratch (standard library + pysat). Supporting evidence only: never a SAT certificate, never a
profile_ok level, never coverage credit.

Setting (Case A, MATH.md section 1 (R3)): v has degree 9, I = N(v) is an independent 9-set, O = V \\ I,
F = O \\ {v} = 14 vertices: s low (a = 4) and m high (a = 5) vertices; each vertex x of F is given by its mask
M_x = N_I(x) (a 4- or 5-subset of I = {0..8}).

Constraints, each PROVED in MATH.md (section cited); nothing from round 9 is used here:
 [G1] I independent, v ~ every i in I                                    (R3, Case A)
 [G2] v has no neighbour in O                                            (P11, first sentence)
 [G3] N(i) subset of O for i in I                                        (F4)
 [G4] x ~ y for x, y in F  <=>  M_x and M_y disjoint                     (Theorem 1, 4b.2; uses (F1))
      => G is determined by the 14 masks; F is triangle-free automatically (three disjoint 4-sets need 12 > 9
      elements); a = 5 vertices are pairwise non-adjacent ((S1)), and an a = 5 vertex is adjacent exactly to the
      copies of its complementary 4-mask.
 [D1] deg(x) <= 9 for every vertex: d_O <= 5 (a = 4), d_O <= 4 (a = 5)   (R3: Delta <= D = 9)
 [D2] r_i := #{x in F : i in M_x} <= 8                                   (F5)
 [MX] saturation identity: for x in F, the union of the masks of its F-neighbours equals I \\ M_x
                                                                         ((MAX) + (F4), section 4 review items,
                                                                          clause family (C9); "subset" is (F1))
      (all other (MAX) pairs are automatic: (i,j) -> v; (x,v) -> any i in M_x; non-adjacent x,y in F share an i.)
 [M1] q4_ij := #{low x : {i,j} subset M_x} <= 3                          (4c.2; 4d "M1 in Case A": the proof is
      verbatim for every pure 4/5/9 profile: final independent set (s-4) + m + n_9 = 11 > 9.)  Redundant given
      [TW]+[AL]; added only as a static helper.
 [TW] 12-set condition: every 12-set of V spans >= 12 edges               (section 1, definition of the family)
      checked for EVERY 12-set: S = X u I' (u {v}) with X subset of F; static part: all 11-subsets X with v
      (e(X) >= 12); every other 12-set is checked exactly on each candidate and added lazily as the linear
      constraint e(X) + sum_{x in X, i in I'} [i in M_x] (+ |I'| if v in S) >= 12 for that (X, I', v).
 [AL] alpha(G) <= 9: no independent set X u U (u {v}) of size 10        ((R1)/(T); redundant given [TW], lazy)
Symmetry reduction: slots of the same kind are interchangeable -> masks sorted within low and within high slots;
S_9 acts transitively on 4-sets -> WLOG the smallest low mask is {0,1,2,3}.
Because [G1]-[G4] determine G and [D1], [MX], [TW], [AL] are the defining properties (triangle-free,
edge-maximal, alpha = 9, 12-set rule), a candidate passing every check would be an actual order-24 graph of
the target family: the script then STOPS and prints it (stop rule of the A2 approval).

Usage: model_1nines.py m [--thr T]   (T = 12-set threshold; default 12; T < 12 is a non-vacuity control only)
"""
import itertools as it
import sys
import time
import json
from pysat.formula import IDPool
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

t0 = time.time()
args = sys.argv[1:]
m = int(args[0])
THR = 12
if '--thr' in args:
    THR = int(args[args.index('--thr') + 1])
s = 14 - m
n = 14
FULL = (1 << 9) - 1
LOW = [sum(1 << i for i in c) for c in it.combinations(range(9), 4)]   # 126, index order = lex order
NT = len(LOW)
assert LOW[0] == 0b1111


def mask(k, A):
    return LOW[A] if k < s else FULL ^ LOW[A]   # high slot: type A = complementary low type, mask I \ A


pool = IDPool()
cls = []
X = [[pool.id(('x', k, A)) for A in range(NT)] for k in range(n)]
E = [[pool.id(('e', k, i)) for i in range(9)] for k in range(n)]
Y = {}
for k, l in it.combinations(range(n), 2):
    if k >= s and l >= s:
        continue                      # two a = 5 vertices are never adjacent ([G4], (S1))
    Y[(k, l)] = pool.id(('y', k, l))


def y(k, l):
    return Y.get((min(k, l), max(k, l)))


def card(lits, bound, kind):
    if kind == 'atmost':
        if bound >= len(lits):
            return
        enc = CardEnc.atmost(lits, bound=bound, vpool=pool, encoding=EncType.seqcounter)
    elif kind == 'atleast':
        if bound <= 0:
            return
        if bound > len(lits):
            cls.append([])
            return
        enc = CardEnc.atleast(lits, bound=bound, vpool=pool, encoding=EncType.totalizer)
    else:
        enc = CardEnc.equals(lits, bound=bound, vpool=pool, encoding=EncType.seqcounter)
    cls.extend(enc.clauses)


# one mask per slot; e = membership
for k in range(n):
    card(X[k], 1, 'equals')
    for A in range(NT):
        mk = mask(k, A)
        for i in range(9):
            cls.append([-X[k][A], E[k][i] if mk >> i & 1 else -E[k][i]])
# [G4] adjacency <=> disjoint masks
for (k, l), v_ in Y.items():
    for i in range(9):
        cls.append([-v_, -E[k][i], -E[l][i]])
    for A in range(NT):
        mk = mask(k, A)
        cls.append([-X[k][A], v_] + [E[l][i] for i in range(9) if mk >> i & 1])
# [D1] degree caps
for k in range(n):
    nb = [y(k, l) for l in range(n) if l != k and y(k, l)]
    card(nb, 5 if k < s else 4, 'atmost')
# [D2] r_i <= 8
for i in range(9):
    card([E[k][i] for k in range(n)], 8, 'atmost')
# [M1] q4_ij <= 3 over low slots (redundant helper)
for i, j in it.combinations(range(9), 2):
    ps = []
    for k in range(s):
        p = pool.id(('p', k, i, j))
        cls.append([-E[k][i], -E[k][j], p])
        ps.append(p)
    card(ps, 3, 'atmost')
# [MX] saturation identity
for k in range(n):
    for i in range(9):
        zs = []
        for l in range(n):
            if l == k or not y(k, l):
                continue
            z = pool.id(('z', k, l, i))
            cls.append([-z, y(k, l)])
            cls.append([-z, E[l][i]])
            zs.append(z)
        cls.append([E[k][i]] + zs)
# symmetry: sorted masks within low slots and within high slots; WLOG low slot 0 has {0,1,2,3}
for grp in (range(0, s), range(s, n)):
    grp = list(grp)
    for k in grp:
        G = [pool.id(('g', k, A)) for A in range(NT)]   # G[A] <-> type(k) <= A
        for A in range(NT):
            prev = [G[A - 1]] if A else []
            cls.append([-G[A], X[k][A]] + prev)
            cls.append([G[A], -X[k][A]])
            if A:
                cls.append([G[A], -G[A - 1]])
        if k + 1 in grp:
            for A in range(NT):
                cls.append([-X[k + 1][A], G[A]])
cls.append([X[0][0]])
# [TW] static: every 11-subset of F with v is a 12-set (v isolated: [G2]); e(X) >= THR
n_static = 0
for Xs in it.combinations(range(n), 11):
    lits = [y(k, l) for k, l in it.combinations(Xs, 2) if y(k, l)]
    card(lits, THR, 'atleast')
    n_static += 1

solver = Solver(name='cadical153', bootstrap_with=cls)
print(f"profile 4^{s} 5^{m} 9 (thr {THR}): vars {pool.top}, clauses {len(cls)}, static 11-subset constraints {n_static}, "
      f"build {time.time()-t0:.1f}s", flush=True)

FREQ = [[(LOW[A] >> i) & 1 for i in range(9)] for A in range(NT)]


def check(masks):
    """Exact check of a full candidate. Returns list of violations (kind, data), most violated first."""
    viol = []
    nbr = [0] * n
    for k, l in it.combinations(range(n), 2):
        if masks[k] & masks[l] == 0:
            nbr[k] |= 1 << l
            nbr[l] |= 1 << k
    # D1, D2, MX (encoded statically; re-checked here)
    for k in range(n):
        d = bin(nbr[k]).count('1')
        a = bin(masks[k]).count('1')
        if a + d > 9:
            viol.append(('D1', k))
        u = 0
        for l in range(n):
            if nbr[k] >> l & 1:
                u |= masks[l]
        if u != FULL ^ masks[k]:
            viol.append(('MX', k))
    for i in range(9):
        if sum(masks[k] >> i & 1 for k in range(n)) > 8:
            viol.append(('D2', i))
    N = 1 << n
    ecount = [0] * N
    freq = [None] * N
    freq[0] = (0,) * 9
    vecs = [tuple((masks[k] >> i) & 1 for i in range(9)) for k in range(n)]
    tw = []
    al = []
    for S in range(1, N):
        k = (S & -S).bit_length() - 1
        R = S ^ (1 << k)
        ecount[S] = ecount[R] + bin(nbr[k] & R).count('1')
        f = tuple(a + b for a, b in zip(freq[R], vecs[k]))
        freq[S] = f
        c = bin(S).count('1')
        order = sorted(range(9), key=lambda i: f[i])
        e = ecount[S]
        if 3 <= c <= 12:
            Ip = order[:12 - c]
            val = e + sum(f[i] for i in Ip)
            if val < THR:
                tw.append((val, S, tuple(Ip), 0))
        if 2 <= c <= 11:
            Ip = order[:11 - c]
            val = e + sum(f[i] for i in Ip) + len(Ip)
            if val < THR:
                tw.append((val, S, tuple(Ip), 1))
        if e == 0:
            unc = [i for i in range(9) if f[i] == 0]
            if c + len(unc) >= 10:
                al.append((S, tuple(unc[:10 - c]), 0))
            if c + 1 >= 10:
                al.append((S, (), 1))
    tw.sort()
    return viol, tw, al


def add_tw(S, Ip, withv):
    Xs = [k for k in range(n) if S >> k & 1]
    lits = [y(k, l) for k, l in it.combinations(Xs, 2) if y(k, l)]
    lits += [E[k][i] for k in Xs for i in Ip]
    bound = THR - (len(Ip) if withv else 0)
    enc = CardEnc.atleast(lits, bound=bound, vpool=pool, encoding=EncType.totalizer)
    for c in enc.clauses:
        solver.add_clause(c)


def add_al(S, U, withv):
    Xs = [k for k in range(n) if S >> k & 1]
    cl = [y(k, l) for k, l in it.combinations(Xs, 2) if y(k, l)]
    cl += [E[k][i] for k in Xs for i in U]
    solver.add_clause(cl)


it_n = 0
n_tw = n_al = 0
PER = 40
while True:
    it_n += 1
    ts = time.time()
    res = solver.solve()
    st = time.time() - ts
    if not res:
        print(f"UNSAT after {it_n} iterations; learned 12-set constraints {n_tw}, alpha clauses {n_al}; "
              f"last solve {st:.1f}s; total {time.time()-t0:.1f}s", flush=True)
        print(json.dumps({'profile': [4] * s + [5] * m + [9], 'm': m, 'thr': THR, 'survivors': 0,
                          'iterations': it_n, 'learned_tw': n_tw, 'learned_alpha': n_al,
                          'seconds': round(time.time() - t0, 1)}), flush=True)
        break
    model = set(l for l in solver.get_model() if l > 0)
    types = [next(A for A in range(NT) if X[k][A] in model) for k in range(n)]
    masks = [mask(k, types[k]) for k in range(n)]
    viol, tw, al = check(masks)
    if viol:
        print("ENCODING ERROR: static constraint violated", viol, masks, flush=True)
        sys.exit(2)
    if not tw and not al:
        rec = {'profile': [4] * s + [5] * m + [9], 'thr': THR,
               'masks': [sorted(i for i in range(9) if mk >> i & 1) for mk in masks]}
        if THR >= 12:
            print("CANDIDATE PASSES EVERY CHECK -- STOP (possible actual order-24 graph; preserve and verify)", flush=True)
        else:
            print(f"control candidate (12-set threshold lowered to {THR}; NOT a graph of the family)", flush=True)
        print(json.dumps(rec), flush=True)
        with open(f"candidate_m{m}_thr{THR}.json", 'w') as fh:
            json.dump(rec, fh)
        sys.exit(3)
    seen = set()
    added = 0
    for val, S, Ip, wv in tw:
        if S in seen:
            continue
        seen.add(S)
        add_tw(S, Ip, wv)
        n_tw += 1
        added += 1
        if added >= PER:
            break
    for S, U, wv in al[:10]:
        add_al(S, U, wv)
        n_al += 1
    if it_n % 25 == 0 or it_n <= 3:
        print(f"  it {it_n}: solve {st:.2f}s, {len(tw)} 12-set violations (min edges {tw[0][0] if tw else '-'}), "
              f"{len(al)} alpha; learned {n_tw}/{n_al}; t={time.time()-t0:.0f}s", flush=True)
