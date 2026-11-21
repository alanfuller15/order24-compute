# which root filter reproduces ChatGPT's 111 / 70 orbit roots for (4^12,5^3), c = 1?
import itertools
def msk(s): return sum(1 << i for i in s)
C = msk(range(4, 9)); B = msk(range(4)); F = 511
def pc(x): return bin(x).count('1')
def pm(m, p): return sum(1 << p[i] for i in range(9) if m >> i & 1)
hc = [m for m in range(512) if pc(m) == 5 and m != C and (m & B) != B]
G0 = [list(a) + list(b) for a in itertools.permutations(range(4)) for b in itertools.permutations(range(4, 9))]
for nm, lows in (('distinct', [C & ~(1 << 7), C & ~(1 << 8)]), ('doubled', [C & ~(1 << 8)] * 2)):
    seed = [C] + lows
    G = [p for p in G0 if sorted(pm(m, p) for m in seed) == sorted(seed)]
    orbs = {}
    for combo in itertools.combinations_with_replacement(hc, 2):
        can = min(tuple(sorted(pm(m, p) for m in combo)) for p in G)
        orbs.setdefault(can, combo)
    reps = list(orbs.values())
    X = lambda combo: seed + list(combo)
    f1 = [c for c in reps if (F ^ c[0]) & (F ^ c[1])]                         # complements meet
    def deg(z, Xs): return sum(1 for x in Xs if x & z == 0)
    f2 = [c for c in f1 if all(deg(F ^ H, X(c)) <= 3 for H in c)]
    def r_ok(c):
        ms = X(c) + [B] + list(set(F ^ H for H in c))
        return all(sum(1 for m in ms if m >> i & 1) <= 8 for i in range(9))
    f3 = [c for c in f2 if r_ok(c)]
    print(nm, 'orbits', len(reps), 'complements meet', len(f1), '+deg<=3', len(f2), '+r<=8', len(f3))
