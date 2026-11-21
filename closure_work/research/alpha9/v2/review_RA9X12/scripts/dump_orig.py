"""RA9X12: dump the exact static clause set of exp_A9_A_1nines/model_1nines.py as DIMACS.
Executes the reviewed file's source verbatim up to (not including) the line that creates the Solver,
then writes `cls` (the full static clause list that was handed to the solver via bootstrap_with).
Since the reported runs were UNSAT at iteration 1, no lazy clause was ever added; this is the exact UNSAT set.
Usage: dump_orig.py MODEL_PY m out.cnf [--thr T]"""
import sys, hashlib
src_path, m, out = sys.argv[1], sys.argv[2], sys.argv[3]
extra = sys.argv[4:]
src = open(src_path).read()
cut = src.index("solver = Solver(name='cadical153', bootstrap_with=cls)")
code = src[:cut]
sys.argv = [src_path, m] + extra
g = {'__name__': '__dump__'}
exec(compile(code, src_path, 'exec'), g)
cls, pool = g['cls'], g['pool']
nv = pool.top
for c in cls:
    for l in c:
        assert l != 0 and abs(l) <= nv
with open(out, 'w') as fh:
    fh.write(f"p cnf {nv} {len(cls)}\n")
    for c in cls:
        fh.write(' '.join(map(str, c)) + ' 0\n')
print(f"m={m} vars={nv} clauses={len(cls)} empty={sum(1 for c in cls if not c)} static11={g['n_static']} thr={g['THR']}")
