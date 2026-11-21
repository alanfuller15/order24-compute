# RA9X10 small finite checks of geometric facts used in ChatGPT round 9 part 2 (q4 <= 3 = M1, pure Case A)
from itertools import combinations, combinations_with_replacement as cwr
I = range(9); M4 = [frozenset(c) for c in combinations(I, 4)]
def q4ok(f): return all(sum(1 for m in f if p[0] in m and p[1] in m) <= 3 for p in combinations(I, 2))
S = frozenset({4,5,6,7,8}); sub = [frozenset(c) for c in combinations(sorted(S), 4)]
ok = True
for d in (4, 5):
    g = [ms for ms in cwr(sub, d) if q4ok(ms)]
    r = all(len(set(ms)) == d for ms in g); print(f"(1) {d} low nbrs of one vertex, q4<=3 -> distinct: {r} ({len(g)} multisets)"); ok &= r
mx = max(sum(1 for m in M4 if not (m & a) and not (m & b)) for a, b in combinations(M4, 2))
print("(2) max #4-masks disjoint from two distinct 4-masks:", mx); ok &= mx <= 1
bad = [(a, b) for a, b in combinations(M4, 2) for ka in (1,2,3) for kb in (1,2,3) if ka + kb >= 4 and len(a & b) >= 2 and q4ok([a]*ka + [b]*kb)]
print("(3) distinct A,B, mult sum >= 4, q4<=3, |A&B|>=2:", len(bad)); ok &= not bad
# (4) |A&B| = 1 -> no 4-mask disjoint from both
n4 = max(sum(1 for m in M4 if not (m & a) and not (m & b)) for a, b in combinations(M4, 2) if len(a & b) == 1)
print("(4) |A&B|=1: max # masks disjoint from both:", n4); ok &= n4 == 0
# (5) A != B both disjoint from a common 4-mask -> |A&B| >= 3
v5 = [(a, b) for a, b in combinations(M4, 2) if any(not (m & a) and not (m & b) for m in M4) and len(a & b) < 3]
print("(5) A!=B with a common disjoint mask and |A&B|<3:", len(v5)); ok &= not v5
print("ALL OK" if ok else "FAILURE")
