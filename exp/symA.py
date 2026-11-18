#!/usr/bin/env python3
"""exp/symA.py (EXPERIMENT; research only, not part of any check, not used for records).
Question: does breaking the residual Aut(H) symmetry (swaps of the K2 components of H) speed up an H-0000 formula?
Variant V7  = cegar90c.build(f) + the formula's recorded lazy list (exactly the recorded CNF: its SHA-256 is checked).
Variant SYM = V7 + 'compswap' clauses: for consecutive K2 components (a,b), (c,d) of H (a<b<c<d, a~b and c~d edges of H
              with all four of degree 1 in H), sigma = (a c)(b d) is an automorphism of H, and the clauses state
              (d_T(a), d_T(b), row_a, row_b) >=lex (d_T(c), d_T(d), row_c, row_d)
              (degrees compared as integers; row_k = (x[k,v]) for v in T in label order). Argument: SOUNDNESS_SYM.md.
              The unary counters d_T(k) >= q are the encoder's own dX variables (same IDPool keys; checked).
Method: lookahead cube tree of V7 to depth DEPTH (ccc90.initial_tree, as production), N leaves sampled uniformly at
random (seed SEED); every sampled cube is solved under both variants by bin/cadical (cube as unit clauses, -t TIMEOUT).
Also counts the leaves (all of them) that unit propagation alone refutes under each variant (Minisat22 propagate).
Output (exp_out/): symA_runs.jsonl (one line per solve), symA_summary.json, symA_cubes.json.
Usage: python3 -I -B exp/symA.py TAG [N=48] [TIMEOUT=900] [DEPTH=8] [JOBS=4] [SEED=128]
       TAG = L87_s10a4b18c65_0000 (cheap) or L86_s10a4b18c64_0000 (hard); data exp/symA_lazy_<TAG>.json.xz"""
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

def components_k2(s, hedges):
    adj = {k: set() for k in range(s)}
    for u, v in hedges: adj[u].add(v); adj[v].add(u)
    comps = sorted((u, v) for u, v in hedges if len(adj[u]) == 1 and len(adj[v]) == 1)
    pairs = []
    E0 = {frozenset(e) for e in hedges}
    for (a, b), (c, d) in zip(comps, comps[1:]):
        sg = {a: c, c: a, b: d, d: b}; mp = lambda x: sg.get(x, x)
        C.need({frozenset((mp(u), mp(v))) for u, v in hedges} == E0, ('compswap: not an automorphism', a, b, c, d))
        pairs.append((a, b, c, d))
    return pairs

def add_compswap(f, pool, cnf, E):
    """append the compswap clauses; returns the number of clauses added"""
    s = f['s']; S = list(range(s)); T = list(range(s, 24))
    L = lambda u, v: E[min(u, v), max(u, v)]
    before = len(cnf.clauses); created = []
    def get(key):                                       # existing variable of the encoder (must exist)
        C.need(key in pool.obj2id, ('counter variable missing', key)); return pool.obj2id[key]
    def OR(p, q):
        if p is True or q is True: return True
        if p is False: return q
        if q is False: return p
        return get(('or', p, q))
    def AND(p, q):
        if p is False or q is False: return False
        if p is True: return q
        if q is True: return p
        return get(('and', p, q))
    def unary(lits):                                    # the encoder's unary(): same keys, same order
        u = [True] + [False] * 8
        for x in lits: u = [True] + [OR(u[j], AND(x, u[j - 1])) for j in range(1, 9)]
        return u
    def neg(p): return (not p) if isinstance(p, bool) else -p
    def clause(*ps):
        if any(p is True for p in ps): return
        cnf.append([p for p in ps if p is not False])
    dX = {k: unary([L(k, v) for v in T]) for k in S}
    for a, b, c, d in components_k2(s, sorted(tuple(x) for x in f['h_edges'])):
        prev = True
        def newv(tagk):
            v = pool.id(('compswap', a, c) + tagk); created.append(v); return v
        for i, j in ((a, c), (b, d)):                   # integers: prev -> d_T(i) >= d_T(j); e <- prev and equal
            for q in range(1, 9): clause(neg(prev), neg(dX[j][q]), dX[i][q])
            e = newv(('deq', i, j)); clause(-e, prev)
            for q in range(9):
                clause(e, neg(prev), neg(dX[i][q]), dX[i][q + 1] if q < 8 else False, neg(dX[j][q]), dX[j][q + 1] if q < 8 else False)
            prev = e
        for i, j in ((a, c), (b, d)):                   # rows: prev -> row_i >=lex row_j (first T vertex most significant)
            for v in T:
                xi, xj = L(i, v), L(j, v)
                clause(neg(prev), -xj, xi)
                pe = newv(('req', i, j, v)); clause(-pe, prev)
                clause(pe, neg(prev), -xi, -xj); clause(pe, neg(prev), xi, xj)
                prev = pe
    return len(cnf.clauses) - before

def main():
    a = sys.argv[1:]
    tag = a[0]; N = int(a[1]) if len(a) > 1 else 48; TO = float(a[2]) if len(a) > 2 else 900
    DEPTH = int(a[3]) if len(a) > 3 else 8; JOBS = int(a[4]) if len(a) > 4 else 4; SEED = int(a[5]) if len(a) > 5 else 128
    out = os.path.join(os.getcwd(), 'exp_out'); os.makedirs(out, exist_ok=True)
    runs = os.path.join(out, 'symA_runs.jsonl'); work = tempfile.mkdtemp(prefix='symA_')
    CAD = os.environ.get('CAD', os.path.join(R, 'bin', 'cadical'))
    L = int(tag[1:3]); f = json.load(open(os.path.join(R, 'data', FF[L])))[tag]
    d = json.load(lzma.open(os.path.join(HERE, f'symA_lazy_{tag}.json.xz'), 'rt')); C.need(d['tag'] == tag, 'data tag')
    lazy = d['lazy']
    pool, cnf, E = C.build(f)
    for x in lazy: cnf.extend(C.lazy_clauses(x, E, pool))
    buf = io.StringIO(); cnf.to_fp(buf); sha = hashlib.sha256(buf.getvalue().encode('ascii')).hexdigest(); del buf
    C.need(sha == d['cnf_sha256'], ('V7 CNF differs from the recorded one', sha, d['cnf_sha256']))
    n7 = len(cnf.clauses); v7_top = pool.top
    pool2, cnf2, E2 = C.build(f)
    for x in lazy: cnf2.extend(C.lazy_clauses(x, E2, pool2))
    C.need(cnf2.clauses == cnf.clauses and E2 == E, 'rebuild differs')
    nadd = add_compswap(f, pool2, cnf2, E2)
    C.need(cnf2.clauses[:n7] == cnf.clauses and nadd > 0, 'SYM must extend V7')
    X.say(f'{tag}: {len(lazy)} lazy items; V7 {n7} clauses / {v7_top} vars (sha ok); SYM +{nadd} clauses / {pool2.top} vars; '
          f'K2 swaps {components_k2(f["s"], sorted(tuple(x) for x in f["h_edges"]))}')
    cand, d8 = K.candidates(f, cnf, E); t0 = time.time()
    leaves, splits = K.initial_tree(cnf.clauses, cand, DEPTH); tcube = time.time() - t0
    X.say(f'{len(leaves)} leaves at depth <= {DEPTH} ({len(cand)} candidates) in {tcube:.0f} s')
    triv = {}
    for name, cls in (('V7', cnf.clauses), ('SYM', cnf2.clauses)):
        sv = Solver(name='minisat22', bootstrap_with=cls)
        triv[name] = [not sv.propagate(assumptions=c)[0] for c in leaves]; sv.delete()
    X.say(f'trivially UNSAT leaves (unit propagation): V7 {sum(triv["V7"])}, SYM {sum(triv["SYM"])} of {len(leaves)}')
    idx = sorted(random.Random(SEED).sample(range(len(leaves)), min(N, len(leaves))))
    json.dump({'tag': tag, 'depth': DEPTH, 'leaves': leaves, 'sample': idx, 'triv_V7': triv['V7'], 'triv_SYM': triv['SYM']},
              open(os.path.join(out, 'symA_cubes.json'), 'w'))
    var = {'V7': X.Variant('V7', v7_top, cnf.clauses, work), 'SYM': X.Variant('SYM', pool2.top, cnf2.clauses, work)}
    del cnf2
    jobs = [{'i': i, 'v': v} for i in idx for v in ('V7', 'SYM')]
    def fn(j):
        st, dt = X.solve(CAD, var[j['v']], leaves[j['i']], TO, work, f"{j['i']}{j['v']}")
        r = {'tag': tag, 'cube_index': j['i'], 'cube': leaves[j['i']], 'variant': j['v'], 'status': st, 'seconds': dt,
             'trivial': triv[j['v']][j['i']]}
        X.say(f"cube {j['i']} {j['v']}: {st} {dt} s"); return r
    res = X.run_jobs(jobs, fn, JOBS, runs)
    by = {}
    for r in res: by.setdefault(r['cube_index'], {})[r['variant']] = r
    both = [i for i in idx if i in by and all(by[i].get(v, {}).get('status') in ('UNSAT', 'SAT', 'TIMEOUT') for v in ('V7', 'SYM'))]
    tsum = {v: round(sum(by[i][v]['seconds'] for i in both), 1) for v in ('V7', 'SYM')}
    tos = {v: sum(1 for i in both if by[i][v]['status'] == 'TIMEOUT') for v in ('V7', 'SYM')}
    sat = {v: [i for i in both if by[i][v]['status'] == 'SAT'] for v in ('V7', 'SYM')}
    mismatch = [i for i in both if {by[i]['V7']['status'], by[i]['SYM']['status']} == {'SAT', 'UNSAT'}]
    nl = len(leaves); est = {v: round(tsum[v] / max(1, len(both)) * nl / 3600, 2) for v in ('V7', 'SYM')}
    ratios = sorted(round(by[i]['SYM']['seconds'] / max(0.5, by[i]['V7']['seconds']), 3) for i in both)
    summ = {'tag': tag, 'depth': DEPTH, 'leaves': nl, 'cubing_seconds': round(tcube), 'sampled': len(idx), 'completed_pairs': len(both),
            'timeout_s': TO, 'sum_seconds': tsum, 'timeouts': tos, 'ratio_SYM_over_V7': round(tsum['SYM'] / max(1e-9, tsum['V7']), 3),
            'median_per_cube_ratio': ratios[len(ratios) // 2] if ratios else None, 'est_total_hours_at_this_depth': est,
            'trivial_leaves': {v: sum(triv[v]) for v in triv}, 'trivial_in_sample': {v: sum(triv[v][i] for i in idx) for v in triv},
            'SAT_cubes': sat, 'SAT_UNSAT_mismatch': mismatch, 'stopped': X.STOP.is_set(),
            'note': 'timeouts are counted at the limit (lower bound); est = mean sampled seconds x number of leaves'}
    json.dump(summ, open(os.path.join(out, 'symA_summary.json'), 'w'), indent=1)
    X.say('SUMMARY ' + json.dumps(summ))
    for v in var.values():
        try: os.remove(v.body)
        except OSError: pass

if __name__ == '__main__':
    main()
