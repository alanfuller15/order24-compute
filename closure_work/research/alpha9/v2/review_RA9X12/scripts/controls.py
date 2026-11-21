"""RA9X12 controls (non-vacuity / soundness smoke tests; not part of the exclusion).
1. Solve the threshold-0 and threshold-8 control CNFs of BOTH encodings with the repo CaDiCaL; decode the masks
   from the model and check every encoded constraint directly on the masks (independent Python check):
   sizes, Theorem-1 adjacency, degree caps, r_i <= 8, saturation, q4 <= 3 on low masks, symmetry breaking, and the
   minimum number of edges over all 11-subsets of F (must be >= threshold).
2. Cross-feed: the thr-8 model of each encoding, re-sorted into the other encoding's slot order, is fixed by unit
   clauses in the other encoding's thr-8 CNF (must be SAT) and thr-12 CNF (UNSAT expected iff its min 11-subset
   edge count is < 12).
Usage: controls.py"""
import itertools as it, subprocess, os, sys, json
SP = '/tmp/claude-0/-home-claude/4a72079e-a9db-5726-b10c-aeb759ad214f/scratchpad'
CAD = SP + '/gh/order24-compute/bin/cadical'
R = SP + '/research/alpha9/v2/review_RA9X12'
LOW = [frozenset(c) for c in it.combinations(range(9), 4)]
FULL = frozenset(range(9))

def solve(cnf, extra_units=()):
    if extra_units:
        lines = open(cnf).read().split('\n', 1)
        nv, nc = map(int, lines[0].split()[2:4])
        tmp = R + '/tmp/fix.cnf'
        with open(tmp, 'w') as fh:
            fh.write(f"p cnf {nv} {nc + len(extra_units)}\n" + lines[1])
            for u in extra_units:
                fh.write(f"{u} 0\n")
        cnf = tmp
    p = subprocess.run(['nice', '-n', '19', CAD, cnf], capture_output=True, text=True, timeout=1800)
    model = set()
    for ln in p.stdout.splitlines():
        if ln.startswith('v '):
            model.update(int(x) for x in ln[2:].split() if int(x) > 0)
    return p.returncode, model

def decode_mine(model, m):
    return [frozenset(i for i in range(9) if 9 * k + i + 1 in model) for k in range(14)]

def decode_orig(model, m):
    s = 14 - m
    out = []
    for k in range(14):
        As = [A for A in range(126) if k * 126 + A + 1 in model]
        assert len(As) == 1
        out.append(LOW[As[0]] if k < s else FULL - LOW[As[0]])
    return out

def vec(M):
    return tuple(1 if i in M else 0 for i in range(9))

def check(masks, m, thr, order):
    s = 14 - m; a = [4] * s + [5] * m
    adj = {(k, l): not (masks[k] & masks[l]) for k, l in it.combinations(range(14), 2)}
    A = lambda k, l: adj[(min(k, l), max(k, l))]
    res = {}
    res['sizes'] = all(len(masks[k]) == a[k] for k in range(14))
    res['deg'] = all(a[k] + sum(A(k, l) for l in range(14) if l != k) <= 9 for k in range(14))
    res['r_i<=8'] = all(sum(i in M for M in masks) <= 8 for i in range(9))
    res['MX'] = all(set().union(*[masks[l] for l in range(14) if l != k and A(k, l)]) == FULL - masks[k]
                    for k in range(14))
    res['q4<=3'] = all(sum(1 for k in range(s) if {i, j} <= masks[k]) <= 3 for i, j in it.combinations(range(9), 2))
    res['slot0'] = masks[0] == frozenset({0, 1, 2, 3})
    if order == 'mine':
        key = lambda M: vec(M)
        res['sorted'] = all(key(masks[k]) >= key(masks[k + 1]) for g in (range(s), range(s, 14)) for k in g if k + 1 in g)
    else:
        idx = lambda k: LOW.index(masks[k]) if k < s else LOW.index(FULL - masks[k])
        res['sorted'] = all(idx(k) <= idx(k + 1) for g in (range(s), range(s, 14)) for k in g if k + 1 in g)
    mn = min(sum(A(k, l) for k, l in it.combinations(X, 2)) for X in it.combinations(range(14), 11))
    res['min_e11'] = mn
    res['tw>=thr'] = mn >= thr
    res['ALL_OK'] = all(v for kk, v in res.items() if kk != 'min_e11')
    return res

def units(masks, m, enc):
    s = 14 - m
    if enc == 'mine':
        low = sorted(masks[:s], key=vec, reverse=True); high = sorted(masks[s:], key=vec, reverse=True)
        ms = low + high
        return [(9 * k + i + 1) if i in ms[k] else -(9 * k + i + 1) for k in range(14) for i in range(9)], ms
    low = sorted(masks[:s], key=lambda M: LOW.index(M)); high = sorted(masks[s:], key=lambda M: LOW.index(FULL - M))
    ms = low + high
    u = []
    for k in range(14):
        A = LOW.index(ms[k]) if k < s else LOW.index(FULL - ms[k])
        u.append(k * 126 + A + 1)
    return u, ms

m = 7
models = {}
for enc, dec in (('orig', decode_orig), ('mine', decode_mine)):
    for thr in (0, 8):
        cnf = f"{R}/{enc}/ctl_{enc}_m{m}_thr{thr}.cnf"
        rc, model = solve(cnf)
        print(f"{enc} thr={thr}: cadical exit {rc}", flush=True)
        if rc != 10:
            print("  CONTROL FAILED: not SAT"); continue
        masks = dec(model, m)
        r = check(masks, m, thr, enc)
        print("  masks", [sorted(M) for M in masks]); print("  check", json.dumps(r), flush=True)
        models[(enc, thr)] = masks
for src, dst in (('orig', 'mine'), ('mine', 'orig')):
    if (src, 8) not in models:
        continue
    masks = models[(src, 8)]
    u, ms = units(masks, m, dst)
    for thr in (8, 12):
        cnf = f"{R}/{dst}/ctl_{dst}_m{m}_thr8.cnf" if thr == 8 else f"{R}/{dst}/{dst}_m{m}.cnf"
        rc, _ = solve(cnf, u)
        print(f"cross-feed {src} thr8 model -> {dst} thr{thr}: cadical exit {rc} "
              f"(min_e11 of the model = {check(ms, m, 0, dst)['min_e11']})", flush=True)
