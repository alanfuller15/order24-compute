"""Mechanical check of every numeric step of CLAIM_L72 (given the hand-proved improvements)."""
from math import ceil
R = {3: 6, 4: 9, 7: 23}  # R(3,k) used
L = {12: 12}
for n in range(13, 25):
    rec = -(-n * L[n-1] // (n - 2))
    L[n] = rec
    if n == 17: L[n] = 31   # hand lemma
    if n in (19, 22, 23, 24): pass
    # structural +1 steps: assume m = rec edges and replay the claim's inequalities
    if n in (19, 22):
        m = rec; D = m - L[n-1]; x = 2*m - (D-1)*n   # min # vertices of degree D
        ok = x >= 2 and m - 2*D < L[n-2]
        print(n, 'rec', rec, 'Dmax', D, 'min#deg D', x, 'delete 2 nonadj ->', m-2*D, '< L', L[n-2], ok); assert ok; L[n] = rec + 1
    elif n == 23:
        m = rec; D = m - L[n-1]; x = 2*m - (D-1)*n
        ok = x >= R[4] and m - 4*D < L[n-4]
        print(n, 'rec', rec, 'Dmax', D, 'min#deg D', x, 'delete 4 ->', m-4*D, '< L', L[n-4], ok); assert ok; L[n] = rec + 1
    elif n == 24:
        m = rec; D = m - L[n-1]; deficit = D*n - 2*m
        s = 7*D - (deficit - 1)
        ok = D == 6 and deficit == 2 and m - s < L[17]
        print(n, 'rec', rec, 'Dmax', D, 'deficit', deficit, '7-set sum >=', s, 'delete ->', m - s, '< L17', L[17], ok); assert ok; L[n] = rec + 1
    else:
        print(n, 'rec', rec, '->', L[n])
print(L)
# layer 72
m = 72
print('L72 Dmax', m - L[23], '| 6-regular 7-set delete', m-42, '<', L[17], '| 9 deg7 -> 4-set delete', m-28, '<', L[20], '| 7-set sum <=', m - L[17])
