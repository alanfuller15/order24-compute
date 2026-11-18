"""enum_profiles.py [-v] -- list the certified profile lists (MATH.md section 4) and their SHA-256."""
import sys, os, json, hashlib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a9core as C
for case in 'BA':
    P = C.profiles(case); ns = C.nstrong(case); S = P[:ns]
    body = lambda p: sum(p) - (9 if case == 'A' else 0)
    print(f'Case {case}: {len(P)} profiles = {ns} strong (P1-P12) + {len(P) - ns} weak extras (pass P1-P5, fail P7 or P8); '
          f'strong body sums {min(map(body, S))}..{max(map(body, S))}; \n  sha256(json.dumps(strong list)) {hashlib.sha256(json.dumps(S).encode()).hexdigest()}'
          f'\n  sha256(json.dumps(certified list)) {hashlib.sha256(json.dumps(P).encode()).hexdigest()}')
    if '-v' in sys.argv:
        for k, p in enumerate(P): print(' ', k, 'S' if k < ns else 'w', p)
