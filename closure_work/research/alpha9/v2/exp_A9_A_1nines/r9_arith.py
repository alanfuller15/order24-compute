"""exp:A9-A-1nines task (a): exact re-check of ChatGPT round 9 part 1, section 1, arithmetic only.
Profile 4^s 5^m 9^t, s + m + t = 15, F = the 15 - t non-nine vertices.
(1) averaging bound: every (|F| - (12 - t))... precisely: t = 1: every 11-subset of F spans >= 12 edges
    (with the a = 9 vertex v it is a 12-set; v is isolated in G[O] by (P11)); t = 2: every 10-subset.
    An edge lies in C(n-2, k-2) of the C(n, k) k-subsets, so e(F) >= ceil(12 C(n,k) / C(n-2,k-2)).
(2) the nonbipartite upper bound 9 + floor(r^2/4) + m*max(1, r), r = s - 9, for every m with s >= 9.
Fractions are exact (fractions.Fraction)."""
from fractions import Fraction
from math import comb, ceil

ok = True
for t in (1, 2):
    n = 15 - t
    k = 12 - t
    frac = Fraction(comb(n - 2, k - 2), comb(n, k))
    lb = Fraction(12) / frac
    elb = -(-lb.numerator // lb.denominator)
    print(f"t={t}: |F|={n}, {k}-subsets: edge fraction {comb(n-2,k-2)}/{comb(n,k)} = {frac}; 12/frac = {lb} = {float(lb):.4f}; e(F) >= {elb}")
    claimed = {1: 20, 2: 21}[t]
    ok &= (elb == claimed)
    rows = []
    for m in range(0, 15 - t):
        s = 15 - t - m
        if s < 9:
            break
        r = s - 9
        b = 9 + r * r // 4 + m * max(1, r)
        rows.append((m, s, r, b))
        print(f"   m={m}: s={s}, r={r}: 9 + {r*r//4} + {m}*{max(1,r)} = {b}  ({'<' if b < elb else '>='} {elb})")
    mx = max(b for *_, b in rows)
    claimed_max = {1: 17, 2: 14}[t]
    print(f"   largest bound {mx} (claimed {claimed_max}); all < {elb}: {mx < elb}; m range 0..{rows[-1][0]} (claimed 0..{ {1:5,2:4}[t] })")
    ok &= (mx == claimed_max) and mx < elb and rows[-1][0] == {1: 5, 2: 4}[t]
print("ARITHMETIC OF ROUND 9 SECTION 1 CONFIRMED" if ok else "ARITHMETIC MISMATCH")
