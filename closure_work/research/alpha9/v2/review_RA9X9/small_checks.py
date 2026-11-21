# RA9X9 small finite checks for ChatGPT round 9 part 1 (standard library only)
from itertools import combinations, combinations_with_replacement as cwr
from math import comb
I = range(9)
M4 = [frozenset(c) for c in combinations(I, 4)]
def q4ok(fam):
    for p in combinations(I, 2):
        if sum(1 for m in fam if p[0] in m and p[1] in m) > 3: return False
    return True
ok = True
A = frozenset({0,1,2,3}); C = frozenset({4,5,6,7,8})
subC = [frozenset(c) for c in combinations(sorted(C), 4)]
# (1) multisets of 5 / 4 four-subsets of C with q4<=3 are all-distinct
for d in (5, 4):
    good = [ms for ms in cwr(subC, d) if q4ok(ms)]
    dist = all(len(set(ms)) == d for ms in good)
    print(f"d={d}: multisets {comb(5+d-1,d)}, q4<=3: {len(good)}, all distinct: {dist}")
    ok &= dist
# (2) d=5: all pairs of C covered exactly 3 times; any further mask with q4<=3 meets C in <=1, has >=3 in A
fam5 = subC
extra = [m for m in M4 if q4ok(fam5 + [m])]
print("d=5: masks addable keeping q4<=3:", len(extra), "all |m&C|<=1:", all(len(m & C) <= 1 for m in extra))
ok &= all(len(m & C) <= 1 and len(m & A) >= 3 for m in extra)
ok &= all(len(a & b) >= 1 for a in extra for b in extra)
print("  pairwise meeting:", all(len(a & b) >= 1 for a in extra for b in extra))
# (3) for every set of 4 distinct 4-subsets of C and every mask != A: disjoint from <= 1 of them
viol = 0
for ys in combinations(subC, 4):
    for m in M4:
        if m != A and sum(1 for y in ys if not (m & y)) > 1: viol += 1
print("(3) violations of 'mask != A disjoint from <=1 of y1..y4':", viol); ok &= viol == 0
# (4) two distinct masks B != C: number of 4-masks disjoint from both <= 1
mx = max(sum(1 for m in M4 if not (m & B) and not (m & Cc)) for B, Cc in combinations(M4, 2))
print("(4) max # masks disjoint from two distinct masks:", mx); ok &= mx <= 1
# (5) claim 1 table
print("(5) claim-1 bound table:")
for t, need in ((2, 21), (1, 20)):
    for m in range(0, 16):
        s = 15 - t - m
        if s < 9: break
        r = s - 9
        bnd = 9 + r*r//4 + m*max(1, r)
        bnd2 = 9 + r*r//4 + m*max(1, min(r, 3))
        print(f"  t={t} m={m} s={s} r={r}: bound {bnd} (with M1 cap {bnd2}) vs need {need}: {'ok' if bnd < need else 'FAIL'}")
        ok &= bnd < need
# averaging numbers
import fractions
e1 = fractions.Fraction(12*comb(14,11), comb(12,9)); e2 = fractions.Fraction(12*comb(13,10), comb(11,8))
print("(6) averaging: t=1 e>=", e1, float(e1), " t=2 e>=", e2, float(e2))
print("(7) t=2 triples of 6-class: 10 e >= 240 ->", 240/10)
# (8) M2-style: tripled mask in 4^13 9^2 -> other masks meet A in <=1, pairwise meet
fam3 = [A, A, A]
ext = [m for m in M4 if q4ok(fam3 + [m])]
pm = all(len(a & b) >= 1 for a in ext for b in ext)
print("(8) masks addable to a tripled A:", len(ext), "all |m&A|<=1:", all(len(m & A) <= 1 for m in ext), "pairwise meeting:", pm,
      "-> independent set 10 + 2 = 12 > 9")
ok &= pm
print("ALL OK" if ok else "FAILURE")
