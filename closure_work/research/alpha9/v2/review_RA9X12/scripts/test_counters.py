"""RA9X12: brute-force test of the two hand-written counters of gen_mine.py (projection semantics):
for every assignment of the input literals, the counter clauses are satisfiable (by some aux assignment)
iff the cardinality bound holds. Aux satisfiability is decided by a SAT call (minisat22) under assumptions on the inputs."""
import itertools as it, sys
from pysat.solvers import Solver

src = open(sys.argv[1]).read()
start = src.index('def atmost'); end = src.index('# (E) exact mask sizes')
ns = {}
code = "nv = 0\nC = []\ndef new():\n    global nv\n    nv += 1\n    return nv\n" + src[start:end]
bad = 0; tested = 0
for kind in ('atmost', 'atleast'):
    for N in range(1, 9):
        for K in range(-1, N + 2):
            g = {}
            exec(code, g)
            lits = [g['new']() for _ in range(N)]
            g[kind](lits, K)
            cls = g['C']; nvar = g['nv']
            aux = list(range(N + 1, nvar + 1))
            for xs in it.product([0, 1], repeat=N):
                want = (sum(xs) <= K) if kind == 'atmost' else (sum(xs) >= K)
                if kind == 'atmost' and K >= N: want = True
                if kind == 'atleast' and K <= 0: want = True
                with Solver(name='minisat22', bootstrap_with=cls) as S:
                    got = S.solve(assumptions=[(i + 1) if xs[i] else -(i + 1) for i in range(N)])
                tested += 1
                if got != want:
                    bad += 1; print('MISMATCH', kind, N, K, xs, got, want)
print(f"counter tests: {tested} cases, {bad} mismatches")
sys.exit(1 if bad else 0)
