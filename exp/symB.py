#!/usr/bin/env python3
"""exp/symB.py (EXPERIMENT; research only, not part of any check, not used for records).
Question: how much does encoder v9 (family 'auts', in the BASE formula: the production layout) speed up one formula,
for H 0001-type formulas (residual factor 2: one swap of the two K2 components) and, as a layout check, for H 0000?
Variant V7 = cegar90c.rebuild(f, lazy): exactly the recorded CNF (its SHA-256 is checked against the record).
Variant V9 = cegar90e.rebuild(f, lazy) with the candidate v9 encoder exp/cegar90e.py (a copy of research/v9/repo/code/
             cegar90e.py; its SHA-256 is printed and checked against V9_SHA if set). V9's base formula = V7's base
             formula + the 'auts' clauses (checked: prefix), then the same lazy items.
Method as exp/symA.py: lookahead cube tree of V7 to depth DEPTH (ccc90.initial_tree), N leaves sampled (SEED), every
sampled cube solved under both variants by bin/cadical with -t TIMEOUT; leaves refuted by unit propagation counted.
Output (exp_out/): symB_runs.jsonl, symB_summary.json, symB_cubes.json.
Usage: python3 -I -B exp/symB.py TAG [N=48] [TIMEOUT=900] [DEPTH=8] [JOBS=4] [SEED=128]
       data: exp/symB_lazy_<TAG>.json.xz (tag, lazy, cnf_sha256 of the v7 record)"""
import sys, os, json, lzma, time, random, hashlib, io, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, 'code'))
os.environ.setdefault('ENCODER', 'cegar90c'); os.environ.setdefault('MASKS12', os.path.join(R, 'data', 'masks12.npy'))
os.environ.setdefault('PREDICT', '0')
import xrun as X
import cegar90c as C, ccc90 as K
import importlib.util
_sp = importlib.util.spec_from_file_location('cegar90e', os.path.join(HERE, 'cegar90e.py'))   # exp/'s copy, explicitly
C9 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C9)
from pysat.solvers import Solver

FF = {80: 'formulas80_c57.json', 81: 'formulas81_c58.json', 82: 'formulas82_c59.json', 83: 'formulas83_c60.json',
      84: 'formulas84_c61.json', 85: 'formulas85_c62.json', 86: 'formulas86_c63.json', 87: 'formulas87_c64.json'}

def main():
    a = sys.argv[1:]
    tag = a[0]; N = int(a[1]) if len(a) > 1 else 48; TO = float(a[2]) if len(a) > 2 else 900
    DEPTH = int(a[3]) if len(a) > 3 else 8; JOBS = int(a[4]) if len(a) > 4 else 4; SEED = int(a[5]) if len(a) > 5 else 128
    out = os.path.join(os.getcwd(), 'exp_out'); os.makedirs(out, exist_ok=True)
    runs = os.path.join(out, 'symB_runs.jsonl'); work = tempfile.mkdtemp(prefix='symB_')
    CAD = os.environ.get('CAD', os.path.join(R, 'bin', 'cadical'))
    L = int(tag[1:3]); f = json.load(open(os.path.join(R, 'data', FF[L])))[tag]
    d = json.load(lzma.open(os.path.join(HERE, f'symB_lazy_{tag}.json.xz'), 'rt')); C.need(d['tag'] == tag, 'data tag')
    lazy = d['lazy']
    pool, cnf, E = C.build(f)
    for x in lazy: cnf.extend(C.lazy_clauses(x, E, pool))
    buf = io.StringIO(); cnf.to_fp(buf); sha = hashlib.sha256(buf.getvalue().encode('ascii')).hexdigest(); del buf
    C.need(sha == d['cnf_sha256'], ('V7 CNF differs from the recorded one', sha, d['cnf_sha256']))
    n7 = len(cnf.clauses); v7_top = pool.top
    v9sha = hashlib.sha256(open(C9.__file__, 'rb').read()).hexdigest()
    C.need(not os.environ.get('V9_SHA') or os.environ['V9_SHA'] == v9sha, ('exp/cegar90e.py is not the expected file', v9sha))
    p7b, c7b, _ = C.build(f); p9b, c9b, _ = C9.build(f); nb7 = len(c7b.clauses)
    C.need(c9b.clauses[:nb7] == c7b.clauses, 'V9 base must extend V7 base'); nadd = len(c9b.clauses) - nb7; del p7b, c7b, p9b, c9b
    cnf2 = C9.rebuild(f, lazy); top2 = max(abs(l) for cl in cnf2.clauses for l in cl)
    C.need(nadd > 0, 'no auts clauses for this formula')
    X.say(f'{tag}: {len(lazy)} lazy items; V7 {n7} clauses / {v7_top} vars (sha ok); V9 base +{nadd} clauses, total {len(cnf2.clauses)} clauses; '
          f'cegar90e {v9sha}; generators {C9.residual_generators(f["s"], sorted(tuple(x) for x in f["h_edges"]))}')
    cand, d8 = K.candidates(f, cnf, E); t0 = time.time()
    leaves, splits = K.initial_tree(cnf.clauses, cand, DEPTH); tcube = time.time() - t0
    X.say(f'{len(leaves)} leaves at depth <= {DEPTH} ({len(cand)} candidates) in {tcube:.0f} s')
    triv = {}
    for name, cls in (('V7', cnf.clauses), ('SYM', cnf2.clauses)):   # SYM = V9
        sv = Solver(name='minisat22', bootstrap_with=cls)
        triv[name] = [not sv.propagate(assumptions=c)[0] for c in leaves]; sv.delete()
    X.say(f'trivially UNSAT leaves (unit propagation): V7 {sum(triv["V7"])}, SYM {sum(triv["SYM"])} of {len(leaves)}')
    idx = sorted(random.Random(SEED).sample(range(len(leaves)), min(N, len(leaves))))
    json.dump({'tag': tag, 'depth': DEPTH, 'leaves': leaves, 'sample': idx, 'triv_V7': triv['V7'], 'triv_SYM': triv['SYM']},
              open(os.path.join(out, 'symB_cubes.json'), 'w'))
    var = {'V7': X.Variant('V7', v7_top, cnf.clauses, work), 'SYM': X.Variant('SYM', top2, cnf2.clauses, work)}
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
            'cegar90e_sha256': v9sha, 'v9_base_extra_clauses': nadd,
            'note': 'SYM = encoder v9 (production layout). Timeouts are counted at the limit (lower bound); est = mean sampled seconds x number of leaves'}
    json.dump(summ, open(os.path.join(out, 'symB_summary.json'), 'w'), indent=1)
    X.say('SUMMARY ' + json.dumps(summ))
    for v in var.values():
        try: os.remove(v.body)
        except OSError: pass

if __name__ == '__main__':
    main()
