"""Check that a --sides candidate's slot classes (X = low slots 0..7-h and high slots s..s+h-1) are independent
(masks pairwise meet) and have sizes 8 and 7. Usage: check_sides.py candidate.json h"""
import json, sys, itertools as it
rec = json.load(open(sys.argv[1])); h = int(sys.argv[2])
m = [set(x) for x in rec['masks']]; b = sum(1 for x in m if len(x) == 5); s = 15 - b
X = [k for k in range(15) if k < 8 - h or s <= k < s + h]; Y = [k for k in range(15) if k not in X]
ind = lambda S: all(m[k] & m[l] for k, l in it.combinations(S, 2))
print(f"{sys.argv[1]}: |X|={len(X)} |Y|={len(Y)} X independent {ind(X)} Y independent {ind(Y)}")
