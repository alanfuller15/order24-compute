#!/usr/bin/env python3
"""exp/unionB.py (EXPERIMENT; research only, not part of any check, not used for records).
Question: is ONE formula for an H across several layers ("union over c") cheaper than the per-layer formulas?
Per-layer F_c = cegar90c.build(f_c) + that formula's recorded lazy list (SHA-256 checked against its record).
Union U    = cegar90c.build(f_cmin) with the three exact counts that are c (e(S,T) = c, sum_T d_S = c, sum_S d_T = c)
             replaced by cmin <= . <= cmax, plus the union of the per-layer lazy lists. Nothing else in build() depends on
             c for s = 10, (a, b) = (4, 18) (m - c = 22 for all, so the gates are equal); argument: SOUNDNESS_UNION.md.
             The replacement is made by wrapping CardEnc while build() runs; the script checks that exactly the 3 + 3
             count calls were changed and that cmin = cmax gives the per-layer formula clause for clause.
Cubes: the shared cube sample in the data file (cube keys closed in all six recorded trees; canonical form: edge
literal, or index of a d_T(k) >= 8 variable), plus EXTRA random root-to-leaf paths of the lookahead (ccc90.best_split)
on U to depth DEPTH. Each cube is solved under every F_c and under U (bin/cadical, cube as units).
Output (exp_out/): unionB_runs.jsonl, unionB_summary.json.
Usage: python3 -I -B exp/unionB.py [DATA=unionB_h0003_L80_85.json.xz] [TO=1200] [TOU=3600] [EXTRA=5] [DEPTH=10] [JOBS=4] [SEED=128]"""
import sys, os, json, lzma, time, random, hashlib, io, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, 'code'))
os.environ.setdefault('ENCODER', 'cegar90c'); os.environ.setdefault('MASKS12', os.path.join(R, 'data', 'masks12.npy'))
os.environ.setdefault('PREDICT', '0')
import xrun as X
import cegar90c as C, ccc90 as K
from pysat.solvers import Solver

FF = {80: 'formulas80_c57.json', 81: 'formulas81_c58.json', 82: 'formulas82_c59.json', 83: 'formulas83_c60.json',
      84: 'formulas84_c61.json', 85: 'formulas85_c62.json', 86: 'formulas86_c63.json', 87: 'formulas87_c64.json'}

def build_union(f, cmin, cmax):
    """cegar90c.build(f) with bound c replaced by the range [cmin, cmax] in the 3 atleast and 3 atmost count calls"""
    real = C.CardEnc; hits = {'atleast': 0, 'atmost': 0}; c = f['c']
    C.need(c == cmin and f['m'] - c == 22 and (f['s'], f['a'], f['b']) == (10, 4, 18), 'union: profile')
    class Wrap:
        @staticmethod
        def atleast(lits, bound=1, **kw):
            if bound == c: hits['atleast'] += 1; bound = cmin
            return real.atleast(lits, bound=bound, **kw)
        @staticmethod
        def atmost(lits, bound=1, **kw):
            if bound == c: hits['atmost'] += 1; bound = cmax
            return real.atmost(lits, bound=bound, **kw)
    C.CardEnc = Wrap
    try: pool, cnf, E = C.build(f)
    finally: C.CardEnc = real
    C.need(hits == {'atleast': 3, 'atmost': 3}, ('union: unexpected count calls', hits))
    return pool, cnf, E

def sha_of(cnf):
    buf = io.StringIO(); cnf.to_fp(buf); return hashlib.sha256(buf.getvalue().encode('ascii')).hexdigest()

def main():
    a = sys.argv[1:]
    dname = a[0] if len(a) > 0 else 'unionB_h0003_L80_85.json.xz'; TO = float(a[1]) if len(a) > 1 else 1200
    TOU = float(a[2]) if len(a) > 2 else 3600; EXTRA = int(a[3]) if len(a) > 3 else 5; DEPTH = int(a[4]) if len(a) > 4 else 10
    JOBS = int(a[5]) if len(a) > 5 else 4; SEED = int(a[6]) if len(a) > 6 else 128
    out = os.path.join(os.getcwd(), 'exp_out'); os.makedirs(out, exist_ok=True)
    runs = os.path.join(out, 'unionB_runs.jsonl'); work = tempfile.mkdtemp(prefix='unionB_')
    CAD = os.environ.get('CAD', os.path.join(R, 'bin', 'cadical'))
    D = json.load(lzma.open(os.path.join(HERE, dname), 'rt')); Ls = [int(x) for x in D['layers']]
    var = {}; maps = {}; E0 = None; fs = {}
    for L in Ls:
        t = D['tags'][str(L)] if str(L) in D['tags'] else D['tags'][L]
        f = json.load(open(os.path.join(R, 'data', FF[L])))[t]; fs[L] = f
        pool, cnf, E = C.build(f)
        if L == Ls[0]:                                  # the range build with cmin = cmax = c is the per-layer build
            pu, cu, Eu = build_union(f, f['c'], f['c']); C.need(cu.clauses == cnf.clauses and pu.top == pool.top, 'union(c,c) != F_c')
        for x in D['lazy'][t]: cnf.extend(C.lazy_clauses(x, E, pool))
        C.need(sha_of(cnf) == D['cnf_sha256'][t], ('F_c differs from the recorded CNF', t))
        ed = {k: v for k, v in E.items() if not isinstance(v, bool)}
        if E0 is None: E0 = ed
        C.need(ed == E0, 'edge variables differ between layers')
        cand, d8 = K.candidates(f, cnf, E); maps[L] = d8
        var[L] = X.Variant(f'F{L}', pool.top, cnf.clauses, work)
        X.say(f'{t}: c={f["c"]} {len(D["lazy"][t])} items, {len(cnf.clauses)} clauses, {pool.top} vars, sha ok, d8 {d8}')
        del cnf
    cmin = min(fs[L]['c'] for L in Ls); cmax = max(fs[L]['c'] for L in Ls)
    C.need(sorted(fs[L]['c'] for L in Ls) == list(range(cmin, cmax + 1)), 'layers must give consecutive c')
    f0 = fs[min(Ls, key=lambda L: fs[L]['c'])]
    C.need(all(fs[L]['h_edges'] == f0['h_edges'] for L in Ls), 'H differs between layers')
    fu = dict(f0); fu['tag'] = f'U_{D["h"]}_c{cmin}-{cmax}'
    pool, cnf, E = build_union(fu, cmin, cmax)
    seen = set(); uitems = []
    for L in Ls:
        for x in D['lazy'][D['tags'][str(L)] if str(L) in D['tags'] else D['tags'][L]]:
            kk = (x['kind'], tuple(x['W']))
            if kk not in seen: seen.add(kk); uitems.append(x)
    for x in uitems: cnf.extend(C.lazy_clauses(x, E, pool))
    candU, d8U = K.candidates(fu, cnf, E); maps['U'] = d8U
    C.need({k: v for k, v in E.items() if not isinstance(v, bool)} == E0, 'union edge variables differ')
    X.say(f'{fu["tag"]}: {len(uitems)} union items, {len(cnf.clauses)} clauses, {pool.top} vars, d8 {d8U}')
    cubes = [dict(c, source='shared') for c in D['cubes']]
    if EXTRA:
        sv = Solver(name='minisat22', bootstrap_with=cnf.clauses); rnd = random.Random(SEED); ev = set(E0.values()); t0 = time.time()
        def canon(l):
            return ['e', l] if abs(l) in ev else ['d', d8U.index(abs(l)), 1 if l > 0 else -1]
        for _ in range(EXTRA):
            pre = []
            for _d in range(DEPTH):
                x = K.best_split(sv, pre, candU)
                if x is None: break
                pre.append(x if rnd.random() < 0.5 else -x)
            cubes.append({'cube': [canon(l) for l in pre], 'source': f'random path depth {len(pre)}'})
        sv.delete(); X.say(f'{EXTRA} random lookahead paths in {time.time() - t0:.0f} s')
    uvar = X.Variant('U', pool.top, cnf.clauses, work); del cnf
    def lits(cube, key):
        return [x[1] if x[0] == 'e' else x[2] * maps[key][x[1]] for x in cube]
    json.dump({'cubes': cubes, 'maps': {str(k): v for k, v in maps.items()}}, open(os.path.join(out, 'unionB_cubes.json'), 'w'))
    jobs = [{'i': i, 'v': v} for i in range(len(cubes)) for v in ['U'] + Ls]
    def fn(j):
        v = j['v']; cube = lits(cubes[j['i']]['cube'], v)
        st, dt = X.solve(CAD, uvar if v == 'U' else var[v], cube, TOU if v == 'U' else TO, work, f"{j['i']}_{v}")
        r = {'cube_index': j['i'], 'variant': str(v), 'status': st, 'seconds': dt, 'cube': cube, 'source': cubes[j['i']]['source']}
        X.say(f"cube {j['i']} {v}: {st} {dt} s"); return r
    res = X.run_jobs(jobs, fn, JOBS, runs)
    by = {}
    for r in res: by.setdefault(r['cube_index'], {})[r['variant']] = r
    keys = ['U'] + [str(L) for L in Ls]; per = []
    for i in range(len(cubes)):
        b = by.get(i, {})
        if not all(b.get(k, {}).get('status') in ('UNSAT', 'SAT', 'TIMEOUT') for k in keys): continue
        sl = sum(b[k]['seconds'] for k in keys[1:])
        per.append({'cube_index': i, 'source': cubes[i]['source'], 'sum_layers_s': round(sl, 1), 'union_s': b['U']['seconds'],
                    'ratio': round(b['U']['seconds'] / max(0.5, sl), 3), 'max_layer_s': max(b[k]['seconds'] for k in keys[1:]),
                    'timeouts': [k for k in keys if b[k]['status'] == 'TIMEOUT'], 'sat': [k for k in keys if b[k]['status'] == 'SAT'],
                    'logged_cad_seconds': cubes[i].get('logged_cad_seconds')})
    su = sum(p['union_s'] for p in per); sl = sum(p['sum_layers_s'] for p in per)
    rs = sorted(p['ratio'] for p in per)
    summ = {'data': dname, 'layers': Ls, 'c_range': [cmin, cmax], 'union_items': len(uitems), 'cubes': len(cubes), 'completed': len(per),
            'timeout_layer_s': TO, 'timeout_union_s': TOU, 'sum_union_s': round(su, 1), 'sum_layers_s': round(sl, 1),
            'ratio_union_over_sum': round(su / max(1e-9, sl), 3), 'median_ratio': rs[len(rs) // 2] if rs else None,
            'union_vs_max_layer': round(su / max(1e-9, sum(p['max_layer_s'] for p in per)), 3),
            'cubes_with_timeouts': [p['cube_index'] for p in per if p['timeouts']], 'cubes_with_SAT': [p['cube_index'] for p in per if p['sat']],
            'per_cube': per, 'stopped': X.STOP.is_set(), 'note': 'timeouts counted at the limit; ratio < 0.5 = go, > 1 = no-go'}
    json.dump(summ, open(os.path.join(out, 'unionB_summary.json'), 'w'), indent=1)
    X.say('SUMMARY ' + json.dumps({k: v for k, v in summ.items() if k != 'per_cube'}))
    for v in list(var.values()) + [uvar]:
        try: os.remove(v.body)
        except OSError: pass

if __name__ == '__main__':
    main()
