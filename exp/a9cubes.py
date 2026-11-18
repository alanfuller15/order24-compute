"""a9cubes.py -- splitting of a cube: binary tree over the incidence bits m(x, i) of the given columns x, in order,
skipping bits fixed by unit propagation of base + cube.  Returned leaves: (cube, kind), kind 'open' (all bits of the
columns decided) or 'closed' (unit propagation already fails).  Both kinds are leaves of one binary tree below the
starting cube, so together they are complete (MATH.md section 7); closed leaves are certified like any other leaf.
The propagation solver (Glucose3) only steers the choice of branching variables; it is not trusted for anything."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import a9core as C
from pysat.solvers import Glucose3

def gen(case, prof, cols, cube0=()):
    g = Glucose3(bootstrap_with=C.build(case, prof).cl)
    order = [C.mv(x, i) for x in cols for i in range(C.NI)]
    out = []
    def rec(cube):
        st, lits = g.propagate(assumptions=cube)
        if not st: out.append((list(cube), 'closed')); return
        fixed = {abs(l) for l in lits}
        v = next((v for v in order if v not in fixed), None)
        if v is None: out.append((list(cube), 'open')); return
        rec(cube + [v]); rec(cube + [-v])
    rec(list(cube0))
    g.delete(); return out

def next_split(case, prof, cube):
    """children of a cube that timed out: split on the next column that still has a free bit (else on one variable)."""
    g = Glucose3(bootstrap_with=C.build(case, prof).cl); st, lits = g.propagate(assumptions=list(cube)); g.delete()
    fixed = {abs(l) for l in lits} | {abs(l) for l in cube}
    for x in range(1, C.NO):
        if any(C.mv(x, i) not in fixed for i in range(C.NI)):
            ch = [c for c, _ in gen(case, prof, [x], cube)]
            if len(ch) >= 2: return ch
    v = next(v for v in range(136, C.NEDGEVARS + 1) if v not in fixed)
    return [list(cube) + [v], list(cube) + [-v]]

if __name__ == '__main__':
    case, idx, ncols = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
    L = gen(case, C.profiles(case)[idx], range(1, ncols + 1))
    print(case, idx, ncols, 'open', sum(1 for _, k in L if k == 'open'), 'closed', sum(1 for _, k in L if k == 'closed'))
