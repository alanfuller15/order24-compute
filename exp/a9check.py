#!/usr/bin/env python3
"""a9check.py (version 4) -- coverage check and independent replay of the alpha = 9 certificates.

Usage
  a9check.py RESULTS[,RESULTS...] LAZYDIR[,LAZYDIR...] WORKDIR [REGEX] [options]
    RESULTS may be written LABEL=path; records of one label form one SOURCE (default label: "main").
    One lazy directory per results file, in the same order.
  Options
    --final          strict mode: replay EVERY UNSAT leaf (no filter), compute coverage from the replay-passed leaves
                     only, print one line "A9 FINAL VERDICT: ...", exit 0 only if coverage is True, every replayed
                     leaf passed and no MODEL record is present.
    --part K/N       with --final: only the profiles with (position in the certified list) mod N == K are checked
                     (their leaves replayed, their coverage required); the verdict line carries the input digest, and
                     the final claim is N part runs with the same digest, all COVERED. Default 0/1 (everything).
    --partition profiles|leaves (default profiles). leaves partitions the ordered UNSAT record list, not
                     whole profiles. In this mode coverage in each part is CONDITIONAL on all other parts
                     replaying their assigned leaves successfully. Only the conjunction of ALL N verdicts,
                     with identical code/input digests and partition mode, establishes the final claim.
                     Every UNSAT record, including duplicates and extra profiles, is replayed exactly once.
    --coverage-only  no replay; coverage from record-level flags (a summary only, never a verdict).
    --workers W      parallel replays (default 1); cake_lpr runs one at a time (file lock in WORKDIR).
    REGEX            (non-final) replay only the leaves whose tag matches.

Which leaves count (fix of RA9C item 4):
  * In profile partition mode a leaf counts only if its record has cadical_exit == 20 and cake_lpr == "s VERIFIED UNSAT", and, if it was
    replayed in this run, only if the replay passed (rebuilt CNF SHA-256 equal to the record, CaDiCaL exit 20 on the
    rebuilt CNF, cake_lpr prints exactly "s VERIFIED UNSAT"). In --final every leaf is replayed, so coverage uses
    exactly the replay-passed set. In leaf partition mode foreign leaves are provisional until all parts pass;
    the conjunction then uses exactly the same replay-passed set (see --partition above).
  * selection, no unions: for each profile the FIRST source (label, in command-line order) whose counting leaves
    give a complete cube tree is used; inside that source each unit (the record's 'unit' cube) is taken from the
    first results file whose counting leaves form a complete tree below that unit, and the profile's tree is then
    checked again as a whole (a9check.complete). Leaves from different sources are never combined.
Exit codes: --final: 0 = verdict COVERED AND VERIFIED, 1 otherwise. Non-final: 0 iff every replayed leaf passed and no
MODEL record is present (coverage is reported, not required), 1 otherwise."""
import sys, os, re, json, gzip, subprocess, hashlib, fcntl, argparse, multiprocessing as mp, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import a9core as C, a9run as R

VER = 's VERIFIED UNSAT'
TRIM = next((x for x in (os.environ.get('TRIM'), os.path.join(HERE, '..', 'bin', 'lrat-trim')) if x and os.path.exists(x)), None)

def leaf_part(records, k, n):
    """Stable, disjoint exhaustive slices of the SAME ordered input on every part."""
    return records[k::n]


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

def record_ok(r):
    return r.get('status') == 'UNSAT' and r.get('cadical_exit') == 20 and r.get('cake_lpr') == VER

def replay(a):
    """returns (key, result dict); never raises"""
    started = time.monotonic()
    key, r, work, CAD, CAKE = a
    res = {'tag': r['tag'], 'source': r['_label'], 'file': r['_file']}
    base = os.path.join(work, '%d_%s' % (key, r['tag'])); f = base + '.cnf'; p = base + '.lrat'; t = base + '.trim.lrat'
    try:
        lazy = json.load(gzip.open(os.path.join(r['_lazydir'], r['tag'] + '.json.gz'), 'rt'))
        b = rebuild(r, lazy); res['cnf_match'] = C.sha(b) == r.get('cnf_sha256')
        if res['cnf_match']:
            with open(f, 'wb') as fh: fh.write(b)
            del b
            cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=false', f, p], capture_output=True)
            res['cadical_exit'] = cp.returncode
            if cp.returncode == 20 and TRIM:
                # Untrusted speed-up only: lrat-trim drops unused proof steps (about 5x smaller, cake_lpr about 3x
                # faster on real B011/A072 leaves). cake_lpr still checks the trimmed proof against the SHA-matched CNF;
                # a bad trim can only make a leaf fail, never pass. Without the binary the full proof is checked.
                tr = subprocess.run([TRIM, '-q', '-a', f, p, t], capture_output=True)
                res['trim_exit'] = tr.returncode
                if tr.returncode in (0, 20) and os.path.exists(t): os.replace(t, p)
            if cp.returncode == 20:
                with open(os.path.join(work, '.cake.lock'), 'w') as lk:
                    fcntl.flock(lk, fcntl.LOCK_EX)
                    ck = subprocess.run([CAKE, '--CML_HEAP_SIZE=' + os.environ.get('A9_CAKE_HEAP', '3000'), '--CML_STACK_SIZE=256', f, p],
                                        capture_output=True, text=True)
                res['cake_lpr'] = VER if VER in ck.stdout.splitlines() else 'NOT VERIFIED'
    except Exception as e:                                      # missing/corrupt lazy file, malformed record, ...
        res['error'] = repr(e)[:200]
    finally:
        for x in (f, p, t):
            if os.path.exists(x): os.remove(x)
    res['pass'] = bool(res.get('cnf_match')) and res.get('cadical_exit') == 20 and res.get('cake_lpr') == VER
    res['seconds'] = round(time.monotonic() - started, 3)
    return key, res

def select(prof, case, leaves_by_label, labels):
    """first label whose counting leaves cover the profile; inside it, per unit the first file with a complete subtree.
    Returns (label, list of chosen leaves) or (None, [])."""
    for lab in labels:
        L = leaves_by_label.get(lab, [])
        L = [r for r in L if r['case'] == case and tuple(r['prof']) == prof]
        if not L: continue
        files = []
        for r in L:
            if r['_file'] not in files: files.append(r['_file'])
        units = []
        for r in L:
            u = tuple(r.get('unit', []))
            if u not in units: units.append(u)
        chosen = []
        for u in units:
            for fl in files:
                S = [r for r in L if r['_file'] == fl and tuple(r.get('unit', [])) == u]
                if S and all(r['cube'][:len(u)] == list(u) for r in S) and complete([r['cube'][len(u):] for r in S]):
                    chosen += S; break
        if chosen and complete([r['cube'] for r in chosen]): return lab, chosen
    return None, []

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('results'); ap.add_argument('lazydirs'); ap.add_argument('work'); ap.add_argument('regex', nargs='?')
    ap.add_argument('--final', action='store_true'); ap.add_argument('--coverage-only', action='store_true')
    ap.add_argument('--partition', choices=('profiles', 'leaves'), default='profiles')
    ap.add_argument('--part', default='0/1'); ap.add_argument('--workers', type=int, default=1)
    a = ap.parse_args()
    try:
        K, N = map(int, a.part.split('/'))
    except ValueError:
        print(f'bad --part {a.part!r}: expected K/N with integers'); sys.exit(2)
    if not (N >= 1 and 0 <= K < N):
        print(f'bad --part {a.part}: need N >= 1 and 0 <= K < N'); sys.exit(2)
    if a.final and (a.regex or a.coverage_only): raise SystemExit('--final takes no filter and always replays')
    if a.partition == 'leaves' and not a.final: raise SystemExit('--partition leaves requires --final')
    rspecs, ldirs = a.results.split(','), a.lazydirs.split(',')
    if len(rspecs) != len(ldirs): raise SystemExit('give one lazy directory per results file, in the same order')
    recs, labels, dig = [], [], hashlib.sha256()
    for spec, d in zip(rspecs, ldirs):
        lab, path = spec.split('=', 1) if '=' in spec else ('main', spec)
        if lab not in labels: labels.append(lab)
        with open(path, 'rb') as fh: raw = fh.read()
        dig.update(hashlib.sha256(raw).digest())
        for l in raw.decode().splitlines():
            if not l.strip(): continue
            r = json.loads(l); r['_lazydir'] = d; r['_label'] = lab; r['_file'] = path; recs.append(r)
    digest = dig.hexdigest()[:16]
    os.makedirs(a.work, exist_ok=True)
    model = [r for r in recs if r.get('status') == 'MODEL']
    if model: print('A MODEL RECORD IS PRESENT:', [r['tag'] for r in model])
    tagbad = [r['tag'] for r in recs if r.get('tag') != R.tag_of(r['case'], r['idx'], r['cube'])]
    if tagbad: print('TAG MISMATCH:', tagbad[:5])
    allP = [(c, k, p) for c in 'BA' for k, p in enumerate(C.profiles(c))]
    mine = {(c, p) for j, (c, k, p) in enumerate(allP) if j % N == K}
    if a.partition == 'leaves': mine = {(c, p) for c, k, p in allP}
    unsat = [r for r in recs if r.get('status') == 'UNSAT']
    extra = [r for r in unsat if C.index_of(r['case'], tuple(r['prof'])) is None]
    if extra: print(f'{len(extra)} leaves of profiles outside the certified list (extra evidence; replayed with --final, not used for coverage)')
    # which leaves are replayed
    if a.final:
        todo = [r for r in unsat if (r['case'], tuple(r['prof'])) in mine or (N > 1 and K == 0 and C.index_of(r['case'], tuple(r['prof'])) is None)]
        if N == 1: todo = unsat
        if a.partition == 'leaves': todo = leaf_part(unsat, K, N)
        print(f'partition={a.partition}-v1 part={K}/{N} assigned={len(todo)} total_unsat={len(unsat)}', flush=True)
    elif a.coverage_only:
        todo = []
    else:
        todo = [r for r in unsat if not a.regex or re.search(a.regex, r['tag'])]
    replayed = {}
    if todo:
        CAD = tool('cadical', 'CAD', '~/tools/cadical/build/cadical'); CAKE = tool('cake_lpr', 'CAKE', '~/tools/cake_lpr/cake_lpr')
        jobs = [(j, r, a.work, CAD, CAKE) for j, r in enumerate(todo)]
        with mp.Pool(max(1, a.workers)) as pool:
            for j, res in pool.imap_unordered(replay, jobs):
                replayed[id(todo[j])] = res; print(json.dumps(res), flush=True)
    npass = sum(1 for v in replayed.values() if v['pass'])
    # counting leaves
    def counts(r):
        if not record_ok(r): return False
        if id(r) in replayed: return replayed[id(r)]['pass']
        # In leaf mode these flags are provisional: ALL N parts must pass.
        # Then every UNSAT record has a successful replay, making this identical
        # to the unpartitioned replay-passed coverage computation.
        return not a.final or a.partition == 'leaves'
    by_label = {}
    for r in unsat:
        if counts(r): by_label.setdefault(r['_label'], []).append(r)
    missing, used = [], {}
    for c, k, p in allP:
        if (c, p) not in mine: continue
        lab, ch = select(p, c, by_label, labels)
        if lab is None: missing.append('%s%03d' % (c, k))
        else: used[lab] = used.get(lab, 0) + 1
    cover = not missing and not model and not tagbad
    if missing: print('NOT COVERED:', len(missing), 'profiles (version-2 indices):', ' '.join(missing))
    print(f'profiles covered per source: {used}')
    if a.final and a.partition == 'leaves':
        print('CONDITIONAL COVERAGE: requires ALL parts with identical input/code digests and partition=leaves-v1', flush=True)
    kind = 'provisional foreign flags + this part replays; requires ALL parts' if a.final and a.partition == 'leaves' else ('replay-verified leaves' if a.final else ('record-level flags only' if a.coverage_only or not replayed else 'record flags + replays of this run'))
    print(f'coverage of {len(mine)} of the {len(allP)} profiles of the certified list (part {K}/{N}) by complete cube trees '
          f'({kind}): {cover}', flush=True)
    print(f'checked {len(replayed)} leaves: {npass} pass' + ('  (PARTIAL: tag filter)' if a.regex else ''))
    if a.final:
        good = cover and npass == len(replayed) and not model
        print(f'A9 FINAL VERDICT (part {K}/{N}, input digest {digest}, {len(replayed)} leaves replayed, partition {a.partition}-v1): '
              + ('COVERED AND VERIFIED' if good else 'NOT ESTABLISHED'
                 + f' (coverage {cover}, failed replays {len(replayed) - npass}, model records {len(model)})'))
        sys.exit(0 if good else 1)
    sys.exit(0 if npass == len(replayed) and not model else 1)

if __name__ == '__main__':
    main()
