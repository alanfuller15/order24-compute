#!/usr/bin/env python3
"""exp/symC.py (EXPERIMENT; research only, not part of any check, not used for records).
Question: how much does encoder v10 (cegar90f: v9 + the a22 clauses at m - c = 22, family 'a22c', in the base formula)
speed up the remaining H-0000 formulas with m - c = 22 (L84_s10a4b18c62_0000, L85_s10a4b18c63_0000) against encoder
v9 (cegar90e, the encoder of the running m84f9/m85f9 trees)?
Variant V9  = code/cegar90e.py rebuild(f, items) (installed encoder v9; its SHA-256 is checked: 7c416f1c...).
Variant V10 = exp/cegar90f.py rebuild(f, items) (candidate v10, research copy; SHA-256 printed and checked against V10_SHA
              if set). Checked: V10 = V9 base + the a22c clauses + V9's lazy block, byte for byte (no new variable).
items = the seed items of TAG in ckpt/<WAVE>.jsonl.xz (the seeds the v9 trees m84f9/m85f9 started from; each item once).
Method as exp/symB.py: lookahead cube tree of V9 to depth DEPTH (ccc90.initial_tree with ENCODER=cegar90e, as
production), N leaves sampled (SEED), every sampled cube solved under both variants by bin/cadical with -t TIMEOUT;
leaves refuted by unit propagation counted. In the output 'V7' is V9 and 'SYM' is V10 (names kept from symB).
Output (exp_out/): symC_runs.jsonl, symC_summary.json, symC_cubes.json.
Usage: python3 -I -B exp/symC.py TAG WAVE [N=64] [TIMEOUT=900] [DEPTH=8] [JOBS=4] [SEED=128]"""
import sys, os, json, lzma, time, random, hashlib, io, tempfile
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, 'code'))
os.environ['ENCODER'] = 'cegar90e'   # ccc90's cube candidates as for the v9 production trees; os.environ.setdefault('MASKS12', os.path.join(R, 'data', 'masks12.npy'))
os.environ.setdefault('PREDICT', '0')
import xrun as X
import cegar90e as C, ccc90 as K
assert hashlib.sha256(open(C.__file__, 'rb').read()).hexdigest() == '7c416f1c6e33c6b95ebea72210ecfc0afa8f3b9ec7e29fa844145c118828de8e', 'code/cegar90e.py is not encoder v9'
import importlib.util
_sp = importlib.util.spec_from_file_location('cegar90f', os.path.join(HERE, 'cegar90f.py'))   # exp/'s copy, explicitly
C9 = importlib.util.module_from_spec(_sp); _sp.loader.exec_module(C9)
from pysat.solvers import Solver

FF = {80: 'formulas80_c57.json', 81: 'formulas81_c58.json', 82: 'formulas82_c59.json', 83: 'formulas83_c60.json',
      84: 'formulas84_c61.json', 85: 'formulas85_c62.json', 86: 'formulas86_c63.json', 87: 'formulas87_c64.json'}

def main():
    a = sys.argv[1:]
    tag = a[0]; wave = a[1]; N = int(a[2]) if len(a) > 2 else 64; TO = float(a[3]) if len(a) > 3 else 900
    DEPTH = int(a[4]) if len(a) > 4 else 8; JOBS = int(a[5]) if len(a) > 5 else 4; SEED = int(a[6]) if len(a) > 6 else 128
    out = os.path.join(os.getcwd(), 'exp_out'); os.makedirs(out, exist_ok=True)
    runs = os.path.join(out, 'symC_runs.jsonl'); work = tempfile.mkdtemp(prefix='symC_')
    CAD = os.environ.get('CAD', os.path.join(R, 'bin', 'cadical'))
    L = int(tag[1:3]); f = json.load(open(os.path.join(R, 'data', FF[L])))[tag]
    C.need(f['m'] - f['c'] == 22, 'symC is for formulas with m - c = 22')
    lazy = []; seen = set()
    for l in lzma.open(os.path.join(R, 'ckpt', f'{wave}.jsonl.xz'), 'rt'):
        d = json.loads(l)
        if d.get('tag') != tag: continue
        for x in d.get('lazy') or d.get('items') or []:
            k = (x['kind'], tuple(x['W']))
            if k not in seen: seen.add(k); lazy.append(x)
    C.need(lazy, ('no seed items for', tag, 'in ckpt', wave))
    pool, cnf, E = C.build(f); nb9 = len(cnf.clauses); t9 = pool.top
    for x in lazy: cnf.extend(C.lazy_clauses(x, E, pool))
    n7 = len(cnf.clauses); v7_top = pool.top
    v10sha = hashlib.sha256(open(C9.__file__, 'rb').read()).hexdigest()
    C.need(not os.environ.get('V10_SHA') or os.environ['V10_SHA'] == v10sha, ('exp/cegar90f.py is not the expected file', v10sha))
    p10, c10, _ = C9.build(f); nb10 = len(c10.clauses); nadd = nb10 - nb9
    C.need(c10.clauses[:nb9] == cnf.clauses[:nb9] and p10.top == t9 and nadd > 0, 'V10 base must be V9 base + clauses, same variables')
    cnf2 = C9.rebuild(f, lazy); top2 = max(abs(l) for cl in cnf2.clauses for l in cl)
    C.need(cnf2.clauses[:nb10] == c10.clauses and cnf2.clauses[nb10:] == cnf.clauses[nb9:], 'V10 must be V10 base + V9 lazy block unchanged')
    del p10, c10
    X.say(f'{tag}: {len(lazy)} seed items from ckpt/{wave}; V9 {n7} clauses / {v7_top} vars; V10 base +{nadd} clauses (a22c), '
          f'same variables, lazy block identical; cegar90f {v10sha}')
    cand, d8 = K.candidates(f, cnf, E); t0 = time.time()
    leaves, splits = K.initial_tree(cnf.clauses, cand, DEPTH); tcube = time.time() - t0
    X.say(f'{len(leaves)} leaves at depth <= {DEPTH} ({len(cand)} candidates) in {tcube:.0f} s')
    triv = {}
    for name, cls in (('V7', cnf.clauses), ('SYM', cnf2.clauses)):   # V7 = v9, SYM = v10
        sv = Solver(name='minisat22', bootstrap_with=cls)
        triv[name] = [not sv.propagate(assumptions=c)[0] for c in leaves]; sv.delete()
    X.say(f'trivially UNSAT leaves (unit propagation): V7 {sum(triv["V7"])}, SYM {sum(triv["SYM"])} of {len(leaves)}')
    idx = sorted(random.Random(SEED).sample(range(len(leaves)), min(N, len(leaves))))
    json.dump({'tag': tag, 'depth': DEPTH, 'leaves': leaves, 'sample': idx, 'triv_V7': triv['V7'], 'triv_SYM': triv['SYM']},
              open(os.path.join(out, 'symC_cubes.json'), 'w'))
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
            'cegar90f_sha256': v10sha, 'v10_base_extra_clauses': nadd, 'items': len(lazy), 'wave': wave, 'V7_is': 'encoder v9', 'SYM_is': 'encoder v10',
            'note': 'V7 = encoder v9, SYM = encoder v10 (names kept from symB). Timeouts are counted at the limit (lower bound); est = mean sampled seconds x number of leaves'}
    json.dump(summ, open(os.path.join(out, 'symC_summary.json'), 'w'), indent=1)
    X.say('SUMMARY ' + json.dumps(summ))
    for v in var.values():
        try: os.remove(v.body)
        except OSError: pass

if __name__ == '__main__':
    main()
