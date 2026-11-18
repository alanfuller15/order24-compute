"""a9core.py -- alpha = 9 case of Erdos #128 at order 24: profiles, deterministic CNF builder, lazy constraints.
Every clause family is justified in MATH.md (section numbers in the comments).  No pysat encoders are used for the
CNF: the bytes of a formula depend only on this file, the cube record and the lazy list.

Labels: I = vertices 0..8 (the independent 9-set), outside vertex number x (0..14) is graph vertex 9 + x.
Outside vertices are sorted by incidence a_x non-decreasing; in Case A the vertex v is x = 14 (a = 9).
Variables: m(x, i) = 1 + 9 x + i  (x adjacent to i);  e(x, y), x < y: 136 + index of the pair; then auxiliaries.
"""
import itertools as it, hashlib, math, functools

NI, NO = 9, 15
def mv(x, i): return 1 + 9 * x + i
_EP = {p: 136 + k for k, p in enumerate(it.combinations(range(NO), 2))}
def ev(x, y): return _EP[(x, y) if x < y else (y, x)]
NEDGEVARS = 240

# ---------------------------------------------------------------- profiles (MATH.md section 4)
def profile_ok(case, prof, weak=False, level=12):
    """prof: sorted tuple of the 15 incidence values (Case A: last entry is v, value 9).
    weak=True: (P1)-(P5) only.  level=8: (P1)-(P8) (the first strong list, 26/110).  level=12 (default): (P1)-(P12)
    ("strong", 16/84; (P9)-(P12) = MATH.md section 4a, from the second ChatGPT review, accepted by RA9X)."""
    D = 8 if case == 'B' else 9                       # degree cap of an outside vertex
    n = {a: prof.count(a) for a in range(0, 10)}
    if case == 'B' and any(a < 2 or a > 7 for a in prof): return False
    if case == 'A' and (prof[-1] != 9 or any(a < 2 or a == 8 for a in prof)): return False
    body = prof if case == 'B' else prof[:-1]         # vertices other than v
    if sum(body) > 72: return False                                   # (P3)
    nH = sum(1 for a in prof if a >= 5)                               # |H| (v counted in Case A)
    if nH > 9: return False                                           # (P2)
    if n[2] > 1 or n[2] + n[3] > 2 or (n[2] == 1 and n[3] > 0): return False   # (P4)
    if n[7] > 0 and n[2] != 1: return False                           # (P5)
    if n[6] > 0 and n[3] == 0: return False                           # (P5)
    if weak: return True                                               # (P1)-(P5) only
    l = n[2] + n[3] + n[4]
    if n[2] == 1 and l - 2 + n[7] > D - 2: return False               # (P7)
    if n[3] == 1 and l - 3 + n[6] > D - 3: return False
    if n[3] == 2 and l - 2 + (n[6] + 1) // 2 > D - 3: return False
    if n[7] > 0:                                                      # (P8)
        if 7 * n[7] + sum(a - 2 for a in body if a != 7) > 56: return False
    if level <= 8: return True
    if case == 'B':
        if nH == 9 and (n[2] == 1 or n[3] >= 1): return False         # (P9)  = review 3.4
        if prof == (4,) * 6 + (5,) * 9: return False                  # (P10) = review 3.3
    else:
        if n[9] >= 4: return False                                    # (P11) = review A1
        if nH == 9 and n[3] == 2: return False                        # (P12a) = review A2
        if nH == 9 and n[2] == 1 and (n[9] >= 2 or n[7] >= 3): return False   # (P12b) = review A3
    return True

@functools.lru_cache(maxsize=None)
def profiles(case):
    """The certified profile list (version 2): first the profiles passing (P1)-(P12) ("strong", indices
    0..nstrong-1), then the profiles passing (P1)-(P5) but failing (P7) or (P8) ("weak extras", the same 115/215 as
    in version 1).  Every profile passing (P1)-(P5) is in this list or is excluded by (P9)-(P12), which are applied
    only to profiles passing (P1)-(P8), i.e. in the setting in which they were proved and reviewed (MATH.md 4, 4a, 7).
    Indices differ from version 1 (archive_v1/); records are matched by profile tuple, not by index."""
    vals = range(2, 8) if case == 'B' else [2, 3, 4, 5, 6, 7, 9]
    k = 15 if case == 'B' else 14
    strong, extra = [], []
    for c in it.combinations_with_replacement(vals, k):
        p = tuple(c) + ((9,) if case == 'A' else ())
        if profile_ok(case, p): strong.append(p)
        elif profile_ok(case, p, weak=True) and not profile_ok(case, p, level=8): extra.append(p)
    return tuple(strong + extra)

@functools.lru_cache(maxsize=None)
def nstrong(case):
    return sum(1 for p in profiles(case) if profile_ok(case, p))

@functools.lru_cache(maxsize=None)
def index_of(case, prof):
    """version-2 index of a profile tuple (None: not in the certified list, e.g. excluded by (P9)-(P12))."""
    P = profiles(case); prof = tuple(prof)
    return P.index(prof) if prof in P else None

# ---------------------------------------------------------------- cardinality encoders (own, deterministic)
class F:
    def __init__(self): self.cl = []; self.nv = NEDGEVARS
    def new(self): self.nv += 1; return self.nv
    def add(self, c): self.cl.append(list(c))
    def atmost(self, lits, k):
        """Sinz sequential counter: at most k of lits true."""
        n = len(lits)
        if k >= n: return
        if k < 0: self.add([]); return
        if k == 0:
            for l in lits: self.add([-l])
            return
        s = [[self.new() for _ in range(k)] for _ in range(n - 1)]
        self.add([-lits[0], s[0][0]])
        for j in range(1, k): self.add([-s[0][j]])
        for i in range(1, n - 1):
            self.add([-lits[i], s[i][0]]); self.add([-s[i - 1][0], s[i][0]])
            for j in range(1, k):
                self.add([-lits[i], -s[i - 1][j - 1], s[i][j]]); self.add([-s[i - 1][j], s[i][j]])
            self.add([-lits[i], -s[i - 1][k - 1]])
        self.add([-lits[n - 1], -s[n - 2][k - 1]])
    def atleast(self, lits, b):
        """at least b of lits true; three deterministic encodings chosen by size."""
        n = len(lits)
        if b <= 0: return
        if b > n: self.add([]); return
        if b == n:
            for l in lits: self.add([l])
            return
        if b == 1: self.add(lits); return
        if math.comb(n, n - b + 1) <= 70:                 # every (n-b+1)-subset contains a true literal
            for c in it.combinations(lits, n - b + 1): self.add(c)
            return
        if b <= n - b:                                    # counter of true literals: t[i][j] => at least j+1 true among lits[0..i]
            t = [[self.new() if j <= i else None for j in range(b)] for i in range(n)]
            for i in range(n):
                for j in range(b):
                    if t[i][j] is None: continue
                    up = t[i - 1][j] if i >= 1 and t[i - 1][j] is not None else None     # still j+1 without lits[i]
                    c1 = [-t[i][j], lits[i]] + ([up] if up else [])
                    self.add(c1)
                    if j >= 1:
                        dn = t[i - 1][j - 1] if i >= 1 else None                         # j among the first i
                        self.add([-t[i][j]] + ([up] if up else []) + ([dn] if dn else []))
            self.add([t[n - 1][b - 1]])
            return
        self.atmost([-l for l in lits], n - b)
    def lex_le(self, A, B):
        """A <=lex B (first position most significant)."""
        eq = None
        for k in range(len(A)):
            self.add(([-eq] if eq else []) + [-A[k], B[k]])
            if k == len(A) - 1: break
            ne = self.new(); pre = [-eq] if eq else []
            self.add(pre + [A[k], B[k], ne]); self.add(pre + [-A[k], -B[k], ne]); eq = ne

# ---------------------------------------------------------------- base formula (MATH.md section 5)
def blocks(prof):
    b = []; s = 0
    for x in range(1, NO + 1):
        if x == NO or prof[x] != prof[s]: b.append((s, x)); s = x
    return b

def forced_nonedges(prof):
    """outside pairs that cannot be edges: a_x + a_y >= 10 (F1)."""
    return {(x, y) for x, y in it.combinations(range(NO), 2) if prof[x] + prof[y] >= 10}

def build(case, prof, cube=(), skip=()):
    """skip: names of clause families to leave out (used only by tests.py; certified formulas use skip=())."""
    f = F(); A = prof; NE = forced_nonedges(prof)
    D = 8 if case == 'B' else 9
    for l in cube: f.add([l])                                                    # the cube
    for p in sorted(NE): f.add([-ev(*p)])                                        # (C1) F1
    for x, y in it.combinations(range(NO), 2):                                   # (C2) triangles I-O-O
        if (x, y) in NE: continue
        for i in range(NI): f.add([-ev(x, y), -mv(x, i), -mv(y, i)])
    for x, y, z in it.combinations(range(NO), 3):                                # (C3) triangles O-O-O
        if (x, y) in NE or (x, z) in NE or (y, z) in NE: continue
        f.add([-ev(x, y), -ev(x, z), -ev(y, z)])
    for x in range(NO):                                                          # (C4) profile: exactly a_x
        ls = [mv(x, i) for i in range(NI)]
        f.atleast(ls, A[x]); f.atmost(ls, A[x])
    for i in range(NI):                                                          # (C5) degree of i at most D
        if 'DEG' in skip: break
        f.atmost([mv(x, i) for x in range(NO)], D)
    for x in range(NO):                                                          # (C6) degree of x at most D
        if 'DEG' in skip: break
        f.atmost([ev(x, y) for y in range(NO) if y != x and (min(x, y), max(x, y)) not in NE], D - A[x])
    for x, y, z in it.combinations(range(NO), 3):                                # (C7) triples I + X
        if 'C7' in skip: break
        need = 12 - A[x] - A[y] - A[z]
        ls = [ev(*p) for p in ((x, y), (x, z), (y, z)) if p not in NE]
        if need >= 1: f.atleast(ls, need)
    def andv(a, b):
        t = f.new(); f.add([-t, a]); f.add([-t, b]); return t
    for i, j in it.combinations(range(NI), 2):                                   # (C8) saturation I-I
        f.add([andv(mv(x, i), mv(x, j)) for x in range(NO)])
    for x in range(NO):                                                          # (C9) saturation O-I
        for i in range(NI):
            f.add([mv(x, i)] + [andv(ev(x, y), mv(y, i)) for y in range(NO)
                                if y != x and (min(x, y), max(x, y)) not in NE])
    for x, y in it.combinations(range(NO), 2):                                   # (C10) saturation O-O
        c = [] if (x, y) in NE else [ev(x, y)]
        c += [andv(mv(x, i), mv(y, i)) for i in range(NI)]
        c += [andv(ev(x, z), ev(y, z)) for z in range(NO) if z not in (x, y)
              and (min(x, z), max(x, z)) not in NE and (min(y, z), max(y, z)) not in NE]
        f.add(c)
    if 'SYM' in skip: return f
    for i in range(NI - 1):                                                      # (C11) rows of the incidence matrix
        f.lex_le([mv(x, i) for x in range(NO)], [mv(x, i + 1) for x in range(NO)])
    for s, t in blocks(prof):                                                    # (C12) columns inside a block
        for x in range(s, t - 1):
            f.lex_le([mv(x, i) for i in range(NI)], [mv(x + 1, i) for i in range(NI)])
    for i in range(NI):                                                          # (C13) column 0 is 0..01..1 (from C11 + C4)
        f.add([mv(0, i)] if i >= NI - A[0] else [-mv(0, i)])
    return f

# ---------------------------------------------------------------- lazy constraints (MATH.md section 6)
def add_lazy(f, prof, item, NE=None):
    """item = ['F', [12 graph vertices]] (floor) or ['I', [10 graph vertices]] (no independent 10-set)."""
    if NE is None: NE = forced_nonedges(prof)
    kind, S = item
    if not (S == sorted(set(S)) and all(0 <= s < 24 for s in S)): raise ValueError('bad set')
    K = [s for s in S if s < 9]; Y = [s - 9 for s in S if s >= 9]
    el = [ev(x, y) for x, y in it.combinations(Y, 2) if (x, y) not in NE]
    if kind == 'I':
        if len(S) != 10: raise ValueError('bad 10-set')
        f.add(el + [mv(y, i) for y in Y for i in K]); return
    if kind != 'F' or len(S) != 12: raise ValueError('bad item')
    J = [i for i in range(NI) if i not in K]
    if len(J) <= 4:      # complementary form: e(Y) + #{(y, j): j in J, y not adjacent to j} >= 12 - sum a_y + |Y||J|
        f.atleast(el + [-mv(y, j) for y in Y for j in J], 12 - sum(prof[y] for y in Y) + len(Y) * len(J))
    else:
        f.atleast(el + [mv(y, i) for y in Y for i in K], 12)

def dimacs(f):
    return ('p cnf %d %d\n' % (f.nv, len(f.cl)) + ''.join(' '.join(map(str, c)) + ' 0\n' for c in f.cl)).encode()

def sha(b): return hashlib.sha256(b).hexdigest()

def edges_of_model(model):
    """model: set of true variables (edge variables) -> edge list on graph vertices 0..23."""
    E = []
    for x in range(NO):
        for i in range(NI):
            if mv(x, i) in model: E.append((i, 9 + x))
    for x, y in it.combinations(range(NO), 2):
        if ev(x, y) in model: E.append((9 + x, 9 + y))
    return E
