"""exp:B4 - exact finite model for the 4 open Case B profiles 4^(15-b) 5^b, b = 0..3 (v1 B16-B19).
Adapted from exp_A9_A_1nines/model_1nines.py. Supporting evidence only: never a SAT certificate, never a
profile_ok level, never coverage credit (until separately reviewed and LRAT-checked).

Setting (Case B, MATH.md 1 (R3)): Delta(G) <= 8, I = {0..8} an independent 9-set, O = V \\ I = 15 vertices:
s = 15 - b low (a = 4) and b high (a = 5) vertices; each x in O is given by its mask M_x = N_I(x).

Constraints. Each is a PROVED, accepted statement of MATH.md (section cited). Nothing from ChatGPT round 10 is used.
 [G1] I independent                                                       (R3, Case B: I an independent 9-set)
 [G3] N(i) subset of O for i in I                                         (F4)
 [G4] x ~ y for x, y in O  <=>  M_x, M_y disjoint                         (Theorem 1, 4b.2, Cases A and B)
      => G is determined by the 15 masks; G is triangle-free automatically (no i in two disjoint masks; three
      pairwise disjoint masks of size >= 4 need 12 > 9 elements); two a = 5 vertices are never adjacent ((S1)).
 [DL] d_O(x) <= 4 for a = 4                                               (R3: Delta <= D = 8)
 [DH] d_O(x) <= 2 for a = 5      (4g.2(a) / 4e.1: neighbours are copies of I \\ M_x, which occurs <= 2 times by N3;
                                  R3 alone gives <= 3)
 [D2] r_i := #{x in O : i in M_x} <= 8                                    (F5, Case B: deg(i) <= 8)
 [MX] saturation identity: for x in O, the union of the masks of its O-neighbours equals I \\ M_x
                                                   ((MAX) + (F4), section 4 review items, clause family (C9))
 [C8] every pair {i, j} of I lies in some mask (q_ij >= 1)                ((MAX) for i, j; (F4); clause (C8); 4c.4)
      (the remaining (MAX) pairs are automatic: non-adjacent x, y in O have meeting masks (Theorem 1).)
 [M1] q4_ij := #{low x : {i, j} subset M_x} <= 3                          (4c.2 Lemma M1, valid for every b)
 [N3] every low mask occurs at most twice                                 (4d.1 Lemma N3, b = 0..6)
 [FL] e(O) >= 20                                (4d.1(ii): averaging the 12-subsets of O; redundant given [TW])
      and Q := e(L) >= 20, 18, 16, 14 for b = 0, 1, 2, 3  (4f.1 "Consequence": the averaged 12-set inequality of 4e.1
      with E <= 2b (N3); redundant given [TW] and [N3]) [added in v2 of this script; model_B4_v1.py lacks it]
 [TW] 12-set rule: every 12-set S = X u I' (X subset of O, I' subset of I) spans >= 12 edges
                                                  (section 1, definition of the family; (F2) is the case |X| = 3)
      static part: all C(15,12) = 455 12-subsets of O (e(X) >= 12); every other 12-set is checked EXACTLY on each
      candidate (all 2^15 subsets X, I' = the 12 - |X| least frequent elements) and added lazily as the linear
      constraint e(X) + sum_{x in X, i in I'} [i in M_x] >= 12.
 [AL] alpha(G) <= 9: no independent set X u U of size 10 (X subset of O, U subset of I \\ union of masks of X)
                                                  ((R1)/(T): alpha = 9; exact, lazy)
 Optional second run (--bip, labelled "+4g.2"): [BP] G[O] has a bipartition into independent classes of sizes 8 and 7
      (4f.1 consequence: G[O] bipartite for b = 0..3; 4g.2: every bipartition has sizes {8, 7}). Side variables
      sigma_x, sigma_x != sigma_y on every edge, exactly 8 vertices with sigma = 1 (swap the classes if needed).

--sides h (v3; implies the +4g.2 run): case split on h = number of high vertices in the 8-class X (h = 0..b). By
4g.2 there is a bipartition with |X| = 8, |Y| = 7; the slots are pre-assigned: low slots 0..7-h and high slots
s..s+h-1 form X, the others Y (valid after permuting slots within blocks). Same-class pairs are non-adjacent, i.e.
their masks meet (Theorem 1); every cross pair keeps its edge variable. The 12-sets X u U (U 4-subset of Y),
Y u W (W 5-subset of X), X u J (J 4-subset of I), Y u J (J 5-subset of I) are added statically (instances of [TW]).
Symmetry inside a case: as below with the four groups (block, class) in place of the two blocks (the (SYM) proof
of section 5 applies verbatim to labellings closed under I-permutations and permutations inside each group);
copies of a low mask are twins of positive degree ([MX]), hence in one class, hence consecutive.
Symmetry reduction, default (--sym dlex, v2): MATH.md section 5 (SYM) PROVED: among labellings (I permuted
arbitrarily, outside vertices ordered by a and permuted within blocks of equal a) take the one with lex-least
incidence matrix read row by row; then rows are lex non-decreasing, columns are lex non-decreasing inside each
block, and column 0 is {5,6,7,8} ((C13), a_0 = 4). Column sorting makes equal masks consecutive, so [N3] is again
"slot k and slot k+2 differ". Symmetry reduction v1 (--sym v1, used by model_B4_v1.py) (sound): (i) the s low slots are interchangeable, as are the b high slots (the constraints are
invariant under permuting slots of equal a), so we require the mask index (lex order of the 4-set; a high slot is
indexed by its complementary 4-set I \\ M_x) to be non-decreasing within the low slots and within the high slots.
(ii) S_9 acts on I and preserves every constraint; it is transitive on 4-sets, so some permutation maps a chosen low
mask to {0,1,2,3}, which is the lex-least 4-set (index 0); after re-sorting, low slot 0 has mask {0,1,2,3}.
Applying (ii) then (i) to any graph of the family gives an assignment satisfying both. [N3] is encoded as
"not (slot k and slot k+2 have the same mask)" for low slots, which is equivalent to multiplicity <= 2 under (i).

Exactness: [G1]-[G4] determine G; a candidate passing [DL], [DH] (implies Delta <= 8 together with [D2]), [MX],
[C8], [TW] and [AL] is triangle-free, edge-maximal (every non-adjacent pair has a common neighbour), has alpha = 9
(I) and every 12-set spans >= 12 edges, with Delta <= 8: an actual order-24 graph of (T), Case B. The script then
STOPS and prints it.

Unsat-core bookkeeping: every static family (and the lazy items, as one family) is guarded by a selector literal
assumed true; on UNSAT the solver's core over these selectors is reported (a sufficient set of families; not
minimised). Symmetry clauses are not guarded (always on; sound by the argument above).

Usage: model_B4.py b [--thr T] [--bip | --sides h] [--drop FAM,FAM,...] [--nocore]
   T = 12-set threshold (default 12; T < 12 is a non-vacuity control only, NOT the family);
   --drop removes the named static families (ablation; still sound as a relaxation; --drop TW makes every 12-set
   lazy, which is still exact); --nocore fixes the selectors as unit clauses (plain solve, no core report).
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
b = int(args[0])
THR = 12
if '--thr' in args:
    THR = int(args[args.index('--thr') + 1])
BIP = '--bip' in args or '--sides' in args
SIDES = int(args[args.index('--sides') + 1]) if '--sides' in args else None
DROP = set()
if '--drop' in args:
    DROP = set(args[args.index('--drop') + 1].split(','))
s = 15 - b
n = 15
if SIDES is not None:
    assert 0 <= SIDES <= b and 8 - SIDES <= s
    INX = [k < 8 - SIDES or s <= k < s + SIDES for k in range(n)]   # True = slot in the 8-class X
FULL = (1 << 9) - 1
LOW = [sum(1 << i for i in c) for c in it.combinations(range(9), 4)]   # 126, index order = lex order
NT = len(LOW)
assert LOW[0] == 0b1111


def mask(k, A):
    return LOW[A] if k < s else FULL ^ LOW[A]


pool = IDPool()
FAMS = ['DL', 'DH', 'D2', 'MX', 'C8', 'M1', 'N3', 'FL', 'TW', 'LAZY'] + (['BP'] if BIP else [])
SEL = {f: pool.id(('sel', f)) for f in FAMS}
cls = []          # hard clauses (structure, symmetry)
cur = [None]      # current family (None = hard)


def add(c):
    if cur[0] is None:
        cls.append(c)
    else:
        cls.append(c + [-SEL[cur[0]]])


X = [[pool.id(('x', k, A)) for A in range(NT)] for k in range(n)]
E = [[pool.id(('e', k, i)) for i in range(9)] for k in range(n)]
Y = {}
for k, l in it.combinations(range(n), 2):
    if k >= s and l >= s:
        continue
    if SIDES is not None and INX[k] == INX[l]:
        continue                      # same class: never adjacent (handled under family BP below)
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
            add([])
            return
        enc = CardEnc.atleast(lits, bound=bound, vpool=pool, encoding=EncType.totalizer)
    else:
        enc = CardEnc.equals(lits, bound=bound, vpool=pool, encoding=EncType.seqcounter)
    for c in enc.clauses:
        add(c)


# ---- hard structure: one mask per slot, membership, [G4]
for k in range(n):
    card(X[k], 1, 'equals')
    for A in range(NT):
        mk = mask(k, A)
        for i in range(9):
            add([-X[k][A], E[k][i] if mk >> i & 1 else -E[k][i]])
for (k, l), v_ in Y.items():
    for i in range(9):
        add([-v_, -E[k][i], -E[l][i]])
    for A in range(NT):
        mk = mask(k, A)
        add([-X[k][A], v_] + [E[l][i] for i in range(9) if mk >> i & 1])
# ---- symmetry (hard)
GROUPS = [list(range(0, s)), list(range(s, n))]
if SIDES is not None:
    GROUPS = [g for g in ([k for k in range(s) if INX[k]], [k for k in range(s) if not INX[k]],
                          [k for k in range(s, n) if INX[k]], [k for k in range(s, n) if not INX[k]]) if g]
SYM = 'dlex' if '--sym' not in args else args[args.index('--sym') + 1]


def lex_le(a, c, tagname):
    """a <=lex c (lists of literals, 1 > 0): eq_t means 'equal on the first t positions'; only the forcing
    direction is encoded (eq_t and a_t = c_t imply eq_{t+1}), which is sound and complete for <=lex."""
    eq = [None] + [pool.id((tagname, t)) for t in range(1, len(a))]
    for t in range(len(a)):
        pre = [] if t == 0 else [-eq[t]]
        add(pre + [-a[t], c[t]])
        if t + 1 < len(a):
            add(pre + [a[t], c[t], eq[t + 1]])
            add(pre + [-a[t], -c[t], eq[t + 1]])


if SYM == 'v1':
    for grp in GROUPS:
        for k in grp:
            G = [pool.id(('g', k, A)) for A in range(NT)]   # G[A] <-> type(k) <= A
            for A in range(NT):
                prev = [G[A - 1]] if A else []
                add([-G[A], X[k][A]] + prev)
                add([G[A], -X[k][A]])
                if A:
                    add([G[A], -G[A - 1]])
            if k + 1 in grp:
                for A in range(NT):
                    add([-X[k + 1][A], G[A]])
    add([X[0][0]])
else:
    # MATH.md section 5 (SYM)(a),(b) and (C13): the lex-least labelling of the 9 x 15 incidence matrix
    # M[i][x] = E[x][i] (outside vertices ordered by a, i.e. low block then high block) has rows non-decreasing
    # in lex order, columns non-decreasing in lex order within each block of equal a, and column 0 = {9-a_0..8}.
    for i in range(8):
        lex_le([E[k][i] for k in range(n)], [E[k][i + 1] for k in range(n)], ('rowlex', i))
    for grp in GROUPS:
        for k in grp[:-1]:
            lex_le([E[k][i] for i in range(9)], [E[k + 1][i] for i in range(9)], ('collex', k))
    for i in range(9):
        add([E[0][i]] if i >= 5 else [-E[0][i]])
# pair indicators p(k,i,j) <-> E[k][i] & E[k][j] (hard definitions)
P = {}
for k in range(n):
    for i, j in it.combinations(range(9), 2):
        p = pool.id(('p', k, i, j))
        P[(k, i, j)] = p
        add([-E[k][i], -E[k][j], p])
        add([-p, E[k][i]])
        add([-p, E[k][j]])


def fam(f):
    cur[0] = None if f in DROP else f
    return f not in DROP


if fam('DL'):
    for k in range(s):
        card([y(k, l) for l in range(n) if l != k and y(k, l)], 4, 'atmost')
if fam('DH'):
    for k in range(s, n):
        card([y(k, l) for l in range(n) if l != k and y(k, l)], 2, 'atmost')
if fam('D2'):
    for i in range(9):
        card([E[k][i] for k in range(n)], 8, 'atmost')
if fam('MX'):
    for k in range(n):
        for i in range(9):
            zs = []
            for l in range(n):
                if l == k or not y(k, l):
                    continue
                z = pool.id(('z', k, l, i))
                add([-z, y(k, l)])
                add([-z, E[l][i]])
                zs.append(z)
            add([E[k][i]] + zs)
if fam('C8'):
    for i, j in it.combinations(range(9), 2):
        add([P[(k, i, j)] for k in range(n)])
if fam('M1'):
    for i, j in it.combinations(range(9), 2):
        card([P[(k, i, j)] for k in range(s)], 3, 'atmost')
if fam('N3'):
    for k in range(s - 2):
        for A in range(NT):
            add([-X[k][A], -X[k + 2][A]])
if fam('FL') and THR >= 12:
    card(list(Y.values()), 20, 'atleast')
    card([v_ for (k, l), v_ in Y.items() if l < s], [20, 18, 16, 14][b], 'atleast')
n_static = 0
if fam('TW'):
    for Xs in it.combinations(range(n), 12):
        card([y(k, l) for k, l in it.combinations(Xs, 2) if y(k, l)], THR, 'atleast')
        n_static += 1
if SIDES is not None and fam('BP'):
    # same-class low pairs: masks must meet (no edge inside a class; Theorem 1 then forces a common element)
    for k, l in it.combinations(range(s), 2):
        if INX[k] == INX[l]:
            for A in range(NT):
                add([-X[k][A]] + [E[l][i] for i in range(9) if LOW[A] >> i & 1])
    XS = [k for k in range(n) if INX[k]]
    YS = [k for k in range(n) if not INX[k]]
    # instances of [TW] for the class structure (static, exact): X u U (U 4-subset of Y), Y u W (W 5-subset of X),
    # X u J (J 4-subset of I), Y u J (J 5-subset of I)
    for U in it.combinations(YS, 4):
        card([y(u, x) for u in U for x in XS if y(u, x)], THR, 'atleast')
    for W in it.combinations(XS, 5):
        card([y(w, z) for w in W for z in YS if y(w, z)], THR, 'atleast')
    for J in it.combinations(range(9), 4):
        card([E[x][i] for x in XS for i in J], THR, 'atleast')
    for J in it.combinations(range(9), 5):
        card([E[z][i] for z in YS for i in J], THR, 'atleast')
elif BIP and fam('BP'):
    SG = [pool.id(('sigma', k)) for k in range(n)]
    for (k, l), v_ in Y.items():
        add([-v_, SG[k], SG[l]])
        add([-v_, -SG[k], -SG[l]])
    card(SG, 8, 'equals')
cur[0] = None

NOCORE = '--nocore' in args
assum = [SEL[f] for f in FAMS if f not in DROP]
if NOCORE:                      # selectors fixed true as unit clauses: no assumptions, no core report
    cls.extend([[a] for a in assum])
    assum = []
solver = Solver(name='cadical153', bootstrap_with=cls)
tag = f"4^{s} 5^{b} (b={b}, thr {THR}{', +4g.2 bipartite 8+7' if BIP else ''}{f', sides: {SIDES} high in the 8-class' if SIDES is not None else ''}{', drop ' + ','.join(sorted(DROP)) if DROP else ''})"
print(f"profile {tag}: vars {pool.top}, clauses {len(cls)}, static 12-subsets of O {n_static}, "
      f"build {time.time()-t0:.1f}s", flush=True)


def check(masks):
    """Exact check of a full candidate: returns (static violations, 12-set violations, alpha violations)."""
    viol = []
    nbr = [0] * n
    for k, l in it.combinations(range(n), 2):
        if masks[k] & masks[l] == 0:
            nbr[k] |= 1 << l
            nbr[l] |= 1 << k
    for k in range(n):
        d = bin(nbr[k]).count('1')
        a = bin(masks[k]).count('1')
        if a + d > 8:
            viol.append(('deg', k))
        u = 0
        for l in range(n):
            if nbr[k] >> l & 1:
                u |= masks[l]
        if u != FULL ^ masks[k]:
            viol.append(('MX', k))
    for i in range(9):
        if sum(masks[k] >> i & 1 for k in range(n)) > 8:
            viol.append(('D2', i))
    for i, j in it.combinations(range(9), 2):
        if not any(masks[k] >> i & 1 and masks[k] >> j & 1 for k in range(n)):
            viol.append(('C8', (i, j)))
    N = 1 << n
    ecount = [0] * N
    freq = [None] * N
    freq[0] = (0,) * 9
    vecs = [tuple((masks[k] >> i) & 1 for i in range(9)) for k in range(n)]
    tw, al = [], []
    for S in range(1, N):
        k = (S & -S).bit_length() - 1
        R = S ^ (1 << k)
        ecount[S] = ecount[R] + bin(nbr[k] & R).count('1')
        f = tuple(a + c for a, c in zip(freq[R], vecs[k]))
        freq[S] = f
        c = bin(S).count('1')
        e = ecount[S]
        if 3 <= c <= 12:
            order = sorted(range(9), key=lambda i: f[i])
            Ip = order[:12 - c]
            val = e + sum(f[i] for i in Ip)
            if val < THR:
                tw.append((val, S, tuple(Ip)))
        if e == 0:
            unc = [i for i in range(9) if f[i] == 0]
            if c + len(unc) >= 10:
                al.append((S, tuple(unc[:10 - c])))
    tw.sort()
    return viol, tw, al


def add_tw(S, Ip):
    Xs = [k for k in range(n) if S >> k & 1]
    lits = [y(k, l) for k, l in it.combinations(Xs, 2) if y(k, l)]
    lits += [E[k][i] for k in Xs for i in Ip]
    enc = CardEnc.atleast(lits, bound=THR, vpool=pool, encoding=EncType.totalizer)
    for c in enc.clauses:
        solver.add_clause(c + [-SEL['LAZY']])


def add_al(S, U):
    Xs = [k for k in range(n) if S >> k & 1]
    cl = [y(k, l) for k, l in it.combinations(Xs, 2) if y(k, l)]
    cl += [E[k][i] for k in Xs for i in U]
    solver.add_clause(cl + [-SEL['LAZY']])


it_n = n_tw = n_al = 0
PER = 40
while True:
    it_n += 1
    ts = time.time()
    res = solver.solve(assumptions=assum)
    st = time.time() - ts
    if not res:
        core = 'n/a (--nocore)' if NOCORE else sorted(f for f in FAMS if f not in DROP and SEL[f] in set(solver.get_core() or []))
        print(f"UNSAT after {it_n} iterations; learned 12-set constraints {n_tw}, alpha clauses {n_al}; "
              f"last solve {st:.1f}s; total {time.time()-t0:.1f}s; core families {core}", flush=True)
        print(json.dumps({'profile': [4] * s + [5] * b, 'b': b, 'thr': THR, 'bip': BIP, 'sides': SIDES, 'drop': sorted(DROP),
                          'survivors': 0, 'iterations': it_n, 'learned_tw': n_tw, 'learned_alpha': n_al,
                          'core': core, 'seconds': round(time.time() - t0, 1)}), flush=True)
        break
    model = set(l for l in solver.get_model() if l > 0)
    types = [next(A for A in range(NT) if X[k][A] in model) for k in range(n)]
    masks = [mask(k, types[k]) for k in range(n)]
    viol, tw, al = check(masks)
    if viol and not DROP:
        print("ENCODING ERROR: static constraint violated", viol, masks, flush=True)
        sys.exit(2)
    if not tw and not al and not viol:
        rec = {'profile': [4] * s + [5] * b, 'thr': THR, 'bip': BIP,
               'masks': [sorted(i for i in range(9) if mk >> i & 1) for mk in masks]}
        if THR >= 12:
            print("CANDIDATE PASSES EVERY CHECK -- STOP (possible actual order-24 graph; preserve and verify)", flush=True)
        else:
            print(f"control candidate (12-set threshold lowered to {THR}; NOT a graph of the family)", flush=True)
        print(json.dumps(rec), flush=True)
        with open(f"candidate_b{b}_thr{THR}{'_bip' if BIP else ''}{'' if SIDES is None else f'_sides{SIDES}'}.json", 'w') as fh:
            json.dump(rec, fh)
        sys.exit(3)
    if viol and not tw and not al:
        print("ablation run: candidate violates only dropped static families", viol, flush=True)
        sys.exit(4)
    seen = set()
    added = 0
    for val, S, Ip in tw:
        if S in seen:
            continue
        seen.add(S)
        add_tw(S, Ip)
        n_tw += 1
        added += 1
        if added >= PER:
            break
    for S, U in al[:10]:
        add_al(S, U)
        n_al += 1
    if it_n % 25 == 0 or it_n <= 3:
        print(f"  it {it_n}: solve {st:.2f}s, {len(tw)} 12-set violations (min edges {tw[0][0] if tw else '-'}), "
              f"{len(al)} alpha; learned {n_tw}/{n_al}; t={time.time()-t0:.0f}s", flush=True)
