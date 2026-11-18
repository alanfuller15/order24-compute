#!/usr/bin/env python3
"""a9check.py RESULTS.jsonl[,more.jsonl...] LAZYDIR[,more...] WORKDIR [tag-regex]   (one lazy dir per results file, same order) -- independent replay of the certificates.
1. coverage: the records' leaves cover every (case, profile index) of a9core.profiles, each by a complete binary
   cube tree (no TIMEOUT leaf left unsplit, no MODEL);
2. per UNSAT leaf: rebuild the CNF from (case, idx, cube, lazy list) with a9core alone, compare SHA-256 with the
   record, run CaDiCaL (LRAT) and cake_lpr on the rebuilt file; pass only on the exact line "s VERIFIED UNSAT".
Exit 0 iff coverage holds and every (selected) leaf passes."""
import sys, os, re, json, gzip, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import a9core as C, a9run as R

def tool(name, env, home):
    for p in (os.environ.get(env), os.path.expanduser(home), os.path.join(HERE, '..', 'bin', name)):
        if p and os.path.exists(p): return p
    raise SystemExit('missing tool ' + name)

def complete(cubes):
    """the cubes (lists of literals) are exactly the leaves of a binary tree branching on one variable per node"""
    if len(cubes) == 1: return cubes[0] == []
    if any(not c for c in cubes): return False
    v = abs(cubes[0][0])
    pos = [c[1:] for c in cubes if c[0] == v]; neg = [c[1:] for c in cubes if c[0] == -v]
    return len(pos) + len(neg) == len(cubes) and bool(pos) and bool(neg) and complete(pos) and complete(neg)

def rebuild(rec, lazy):
    prof = tuple(rec['prof'])          # any profile can be rebuilt; membership in the certified list matters only for coverage
    if not (len(prof) == 15 and list(prof) == sorted(prof)): raise ValueError('malformed profile')
    if not all(isinstance(l, int) and 1 <= abs(l) <= C.NEDGEVARS for l in rec['cube']): raise ValueError('bad cube')
    f = C.build(rec['case'], prof, rec['cube'])
    for item in lazy: C.add_lazy(f, prof, item)
    return C.dimacs(f)

if __name__ == '__main__':
    rpaths, ldirs = sys.argv[1].split(','), sys.argv[2].split(',')
    if len(rpaths) != len(ldirs): raise SystemExit('give one lazy directory per results file, in the same order')
    recs = []
    for p, d in zip(rpaths, ldirs):        # each record remembers its own lazy directory (tags of list versions 1 and 2 may coincide)
        for l in open(p): r = json.loads(l); r['_lazydir'] = d; recs.append(r)
    work = sys.argv[3]; rx = re.compile(sys.argv[4]) if len(sys.argv) > 4 else None
    os.makedirs(work, exist_ok=True)
    CAD = tool('cadical', 'CAD', '~/tools/cadical/build/cadical'); CAKE = tool('cake_lpr', 'CAKE', '~/tools/cake_lpr/cake_lpr')
    cover = True
    if any(r['status'] == 'MODEL' for r in recs): print('A MODEL RECORD IS PRESENT'); cover = False
    seen = {}
    for r in recs:                                   # a cube solved twice (re-run shards): keep the first record
        seen.setdefault((r['case'], tuple(r['prof']), tuple(r['cube']), r['status']), r)
    recs = list(seen.values())
    leaves = [r for r in recs if r['status'] == 'UNSAT']
    # records are matched to the certified (version-2) list by profile tuple; their 'idx' is the index of the list
    # version they were produced with (version 1 for records without 'list_version'), used only in their tag
    extra_ev = [r for r in leaves if C.index_of(r['case'], tuple(r['prof'])) is None]
    if extra_ev: print(f'{len(extra_ev)} leaves of profiles excluded by (P9)-(P12): kept as extra evidence, checked, not needed for coverage')
    if any(r['tag'] != R.tag_of(r['case'], r['idx'], r['cube']) for r in recs): print('TAG MISMATCH'); cover = False
    missing = []
    for case in 'BA':
        for k in range(len(C.profiles(case))):
            pk = C.profiles(case)[k]
            cs = [r['cube'] for r in leaves if r['case'] == case and tuple(r['prof']) == pk]
            if not cs or not complete(cs): cover = False; missing.append('%s%03d' % (case, k))
    if missing: print('NOT COVERED:', len(missing), 'profiles (version-2 indices):', ' '.join(missing))
    print('coverage of all', sum(len(C.profiles(c)) for c in 'BA'), 'profiles of the certified list (version 2) by complete cube trees:', cover, f'({len(leaves)} leaves)', flush=True)
    n = ok = 0
    for r in leaves:
        if rx and not rx.search(r['tag']): continue
        n += 1; f = os.path.join(work, r['tag'] + '.cnf'); p = os.path.join(work, r['tag'] + '.lrat')
        lz = os.path.join(r['_lazydir'], r['tag'] + '.json.gz')
        lazy = json.load(gzip.open(lz, 'rt'))
        b = rebuild(r, lazy); match = C.sha(b) == r['cnf_sha256']; res = {'tag': r['tag'], 'cnf_match': match}
        if match:
            open(f, 'wb').write(b)
            cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=false', f, p], capture_output=True); res['cadical_exit'] = cp.returncode
            ck = subprocess.run([CAKE, '--CML_HEAP_SIZE=' + os.environ.get('A9_CAKE_HEAP', '3000'), '--CML_STACK_SIZE=256', f, p], capture_output=True, text=True)
            res['cake_lpr'] = 's VERIFIED UNSAT' if 's VERIFIED UNSAT' in ck.stdout.splitlines() else 'NOT VERIFIED'
            for x in (f, p):
                if os.path.exists(x): os.remove(x)
        res['pass'] = match and res.get('cadical_exit') == 20 and res.get('cake_lpr') == 's VERIFIED UNSAT'
        ok += res['pass']; print(json.dumps(res), flush=True)
    print(f'checked {n} leaves: {ok} pass' + ('  (PARTIAL: tag filter)' if rx else ''))
    sys.exit(0 if cover and ok == n and not rx else 1)
