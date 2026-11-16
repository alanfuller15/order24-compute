#!/usr/bin/env python3
"""grun90.py, version 6: encoder version 7 (cegar90c.py: version 6 plus the family twins, BOUNDS90.md "Version 7");
every record says "encoder": "v7", and the certificate checker gcert90d.py rebuilds each formula with the encoder its
record names. Version 5 used encoder version 6 (cegar90b.py, records "v6"), version 4 encoder version 5 (cegar90.py,
records "v5"). A lazy list found with an earlier version (checkpoint, saved progress, REUSE) is reused as it is: its
items are true for every graph of the class, and the later version's formula only has more clauses (and, where tbip or
twins add variables, the lazy auxiliary ids shift, which is harmless because rebuild() regenerates them).
Version 3 added a resumable search: `search()` is encoder version 4's CEGAR loop (cegar91.run,
the same steps and the same encoder functions) that starts from the lazy items saved by earlier stopped searches of this
formula (OUTDIR/lazy_partial.jsonl) and appends each iteration's new items there (fsync), so a search stopped by a kill
loses at most the iteration in progress (one solver call). The final formula is still rebuild(f, lazy) with lazy = the
saved items followed by the new ones, and the CNF file is compared with that rebuild before any proof is accepted, as
before. Lazy items are true for every graph of the class (9-sets that must contain an edge, 12-sets with at least 12
edges), and the certificate checker checks each one, so where the items came from plays no part in what is proved.
Version 2 (R90A should-fix 4: the checkpoint append is newline-safe; this docstring is exact).
grun90.py = grun91.py (encoder version 4, cegar91.py) plus a lazy-list checkpoint: when the search ends UNSAT, its lazy
list is appended to OUTDIR/lazy_ckpt.jsonl (fsync), and a later launch takes the lazy list of a formula found there
instead of searching again (like REUSE). The append starts with a newline when the file does not end with one, so a line
torn by a kill never swallows the next checkpoint. What a kill loses depends on where the final UNSAT came from:
- from PySAT (plain search, or the PySAT phase of the hybrid search): the checkpoint is written before the proof, which
  is a separate CaDiCaL run, so a launch killed during the proof loses only the proof;
- from the external proof-writing CaDiCaL of the hybrid search: that run makes the proof inside the search, and the
  checkpoint is written after it returns, so a launch killed during that run loses the whole search.
The producer is not trusted: the certificate checker (gcert90d.py) rebuilds every CNF from the formula and the lazy list.
Producer for edge layer 90 (certificate mode; inherited from grun92.py/grun91.py). For every formula of FORMULAS.json
not yet recorded: find the lazy list with the encoder's CEGAR search, or take it from an earlier record (REUSE) or the
checkpoint; make the LRAT proof of the final CNF with CaDiCaL 3.0.1; trim it with lrat-trim (binary LRAT); compress it
with xz into PROOFS/TAG.lrat.xz; and check the trimmed proof with cake_lpr against the CNF (the producer's own check; the
independent check is gcert90d.py, which rebuilds every CNF and checks every stored proof). Before proving, the CNF file
must equal rebuild(f, lazy).
A formula is recorded only if CaDiCaL proved it (exit 20) and cake_lpr printed exactly "s VERIFIED UNSAT" with exit 0;
the record holds the lazy list, the CNF's SHA-256 and the proof file's SHA-256. Anything else is not recorded as done:
failed_attempts.jsonl (files kept) or unknown.jsonl (budget), retried at the next launch. A model passing every
original check is recorded as ORIGINAL_MODEL_FOUND.
Search: CONF=0 is plain incremental search in PySAT, the proof made afterwards by a separate CaDiCaL run; CONF=N > 0 is
the hybrid search (N conflicts per iteration in PySAT, then the external proof-writing CaDiCaL; after an external
model the budget is multiplied by GROW, default 4).
REUSE=file: formulas recorded there as UNSAT with a lazy list (records of any earlier version) take that lazy list
instead of a new search; the formula is rebuilt by this version's encoder and proved again.
Usage: MASKS12=... [PROOFS=dir] [CONF=n] [GROW=g] [CAD_OPTS='...'] [CAKE_LOCK=path] [CAKE_SLOTS=k] [STOP_AFTER=s]
       [TODO_FILE=list] [REUSE=file] [CAD=..] [CAKE=..] [TRIM=..]
       python3 -I grun90.py FORMULAS.json OUTDIR workers budget_s [tag-prefix]"""
import sys, os, json, subprocess, hashlib, time, fcntl, lzma, traceback, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import cegar90x as C                                 # EXPERIMENTAL: encoder v8 + hfloor (timing test)
ENCODER = 'v9x'
import pysat
CAD = os.environ.get('CAD', os.path.expanduser('~/tools/cadical/build/cadical'))
CAKE = os.environ.get('CAKE', os.path.expanduser('~/tools/cake_lpr/cake_lpr'))
CAKE_SLOTS = int(os.environ.get('CAKE_SLOTS', '1'))
TRIM = os.environ.get('TRIM', os.path.expanduser('~/tools/lrat-trim/lrat-trim'))
CONF = int(os.environ.get('CONF', '20000')); GROW = int(os.environ.get('GROW', '4')); CAD_OPTS = os.environ.get('CAD_OPTS', '').split()

def cake_slot(path, slots):
    """Take one of `slots` cake_lpr slots (lock files path.0 .. path.N-1; the single file `path` when slots == 1, as
    before). The slots only bound how many cake_lpr run at once (memory); they play no part in what counts as verified."""
    names = [path] if slots <= 1 else [f'{path}.{i}' for i in range(slots)]
    while True:
        for n in names:
            fd = os.open(n, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600)
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | (fcntl.LOCK_NB if len(names) > 1 else 0))
                return fd
            except BlockingIOError:
                os.close(fd)
        time.sleep(0.2)

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for blk in iter(lambda: f.read(1 << 20), b''): h.update(blk)
    return h.hexdigest()

_F = {}
def formulas(path):                               # loaded once per worker process
    if path not in _F: _F[path] = json.load(open(path))
    return _F[path]

_R = {}
def reuse():                                      # version-1 records whose lazy list is reused (loaded once per worker)
    if not _R and os.environ.get('REUSE'):
        for l in open(os.environ['REUSE']):
            if l.strip():
                o = json.loads(l)
                if o.get('status') == 'UNSAT' and isinstance(o.get('lazy'), list): _R[o['tag']] = o['lazy']   # R2 #9
    return _R

def ckpt_lazy(out, tag):                         # grun90: the last checkpointed lazy list of this formula, if any
    p = os.path.join(out, 'lazy_ckpt.jsonl'); lz = None
    if os.path.exists(p):
        for l in open(p):
            if l.strip():
                try: o = json.loads(l)
                except ValueError: continue          # a torn last line after a kill
                if o.get('tag') == tag and isinstance(o.get('lazy'), list): lz = o['lazy']
    return lz

def ckpt_write(out, tag, lazy, seconds):
    p = os.path.join(out, 'lazy_ckpt.jsonl'); lead = ''
    if os.path.exists(p) and os.path.getsize(p) > 0:   # R90A should-fix 4: a line torn by a kill must stay its own line
        with open(p, 'rb') as fi:
            fi.seek(-1, os.SEEK_END)
            if fi.read(1) != b'\n': lead = '\n'
    with open(p, 'a') as fo:
        fo.write(lead + json.dumps({'tag': tag, 'lazy': lazy, 'search_seconds': seconds}) + '\n'); fo.flush(); os.fsync(fo.fileno())

def append_line(p, obj):
    """append one JSON line with fsync; a newline first if the file does not end with one (a line torn by a kill)"""
    lead = ''
    if os.path.exists(p) and os.path.getsize(p) > 0:
        with open(p, 'rb') as fi:
            fi.seek(-1, os.SEEK_END)
            if fi.read(1) != b'\n': lead = '\n'
    with open(p, 'a') as fo:
        fo.write(lead + json.dumps(obj) + '\n'); fo.flush(); os.fsync(fo.fileno())

def partial_lazy(out, tag):
    """grun90 v3: the lazy items saved by earlier stopped searches of this formula, in order; their total search seconds;
    the conflict budget of the last saved iteration (None if nothing is saved)"""
    p = os.path.join(out, 'lazy_partial.jsonl'); items = []; secs = 0.0; conf = None
    if os.path.exists(p):
        for l in open(p, 'rb'):
            if not l.strip(): continue
            try: o = json.loads(l)
            except ValueError: continue                  # a line torn by a kill: that iteration is redone
            if isinstance(o, dict) and o.get('tag') == tag and isinstance(o.get('items'), list):
                items += o['items']; secs += o.get('seconds') or 0; conf = o.get('conf', conf)
    return items, secs, conf

def search(f, out, budget_s=None, hybrid=None, per_iter=60):
    """cegar91.run with a resumable lazy list (grun90 v3; see the docstring). Same loop, same encoder functions."""
    t0 = time.time(); pool, cnf, E = C.build(f); tag = f['tag']
    base = len(cnf.clauses); pp = os.path.join(out, 'lazy_partial.jsonl')
    seed, seed_secs, seed_conf = partial_lazy(out, tag)
    lazy = []; seen = set(); n9 = n12 = 0
    for item in seed:                                 # the saved items, in the order they were found
        key = (item['kind'], tuple(item['W']))
        C.need(key not in seen, ('a saved lazy item repeats', key)); seen.add(key)
        cnf.extend(C.lazy_clauses(item, E, pool)); lazy.append(item)
        if item['kind'] == 9: n9 += 1
        else: n12 += 1
    sol = C.Solver(name='cadical195', bootstrap_with=cnf.clauses)
    M = C.masks12(); itn = 0; log = []
    conf = (seed_conf or hybrid['conf']) if hybrid else None
    while True:
        itn += 1
        if budget_s and time.time() - t0 > budget_s: res = {'status': 'UNKNOWN_BUDGET'}; break
        ti = time.time()
        if hybrid:
            sol.conf_budget(conf); ans = sol.solve_limited()
        else:
            ans = sol.solve()
        how = 'pysat'
        if ans is None:
            os.makedirs(out, exist_ok=True)
            st, mdl = C.external_solve(hybrid['cad'], cnf, os.path.join(out, f'{tag}.cnf'),
                                       os.path.join(out, f'{tag}.lrat'), hybrid.get('opts', ()))
            ans = st == 'SAT'; how = 'external'
            if ans: conf *= hybrid.get('grow', 4)
        log.append((how, round(time.time() - ti, 2)))
        if not ans:
            res = {'status': 'UNSAT'}
            if how == 'external': res['proof'] = os.path.join(out, f'{tag}.lrat')
            break
        if how == 'pysat': mdl = set(l for l in sol.get_model() if l > 0)
        adj = [k for k, l in E.items() if l is True or (not isinstance(l, bool) and l in mdl)]
        am = [0] * 24
        for u, v in adj: am[u] |= 1 << v; am[v] |= 1 << u
        C.need(all(am[u] & am[v] == 0 for u, v in adj), 'triangle in a model')
        g = C.nx.Graph(); g.add_nodes_from(range(24)); g.add_edges_from(adj); new = []
        for clq in C.nx.find_cliques(C.nx.complement(g)):
            if len(clq) >= 9:
                new.append({'kind': 9, 'W': sorted(clq)[:9]})
                if len(new) >= per_iter: break
        cnt = C.np.zeros(len(M), dtype=C.np.int16)
        for v in range(24): cnt += (((M >> v) & 1) * C.np.bitwise_count(M & C.np.uint32(am[v]))).astype(C.np.int16)
        cnt //= 2; bad = C.np.nonzero(cnt < 12)[0]
        for idx in bad[C.np.argsort(cnt[bad], kind='stable')][:per_iter]:
            mk = int(M[idx]); new.append({'kind': 12, 'W': [v for v in range(24) if mk >> v & 1]})
        if not new: res = {'status': 'ORIGINAL_MODEL_FOUND', 'edges': sorted(adj)}; break
        for item in new:
            key = (item['kind'], tuple(item['W']))
            C.need(key not in seen, 'a lazy constraint was violated after it was added'); seen.add(key)
            cl = C.lazy_clauses(item, E, pool)
            for k in cl: sol.add_clause(k)
            cnf.extend(cl); lazy.append(item)
            if item['kind'] == 9: n9 += 1
            else: n12 += 1
        append_line(pp, {'tag': tag, 'items': new, 'iteration': itn, 'how': how, 'conf': conf,
                         'seconds': round(time.time() - ti, 2), 'time': round(time.time())})
    sol.delete()
    res.update({'tag': tag, 'iterations': itn, 'floors_added': n12, 'nine_added': n9, 'base_clauses': base,
                'final_vars': pool.top, 'final_clauses': len(cnf.clauses), 'seconds': round(time.time() - t0, 2),
                'iteration_log': log, 'resumed_items': len(seed), 'resumed_seconds': round(seed_secs, 2)})
    if res['status'] == 'UNSAT': res['lazy'] = lazy
    if out and res['status'] == 'UNSAT' and 'proof' not in res:
        os.makedirs(out, exist_ok=True); cnf.to_file(os.path.join(out, f'{tag}.cnf'))
    return res

def work(arg):
    try: return work1(arg)
    except Exception as e:                        # C1 S4: one formula's error must not stop the pass
        return {'tag': arg[1], 'status': 'ERROR', 'error': traceback.format_exc()[-600:]}

def work1(arg):
    path, tag, out, budget = arg
    f = formulas(path)[tag]; proofs = os.environ.get('PROOFS', os.path.join(out, 'proofs'))
    cnf = os.path.join(out, tag + '.cnf'); p = os.path.join(out, tag + '.lrat'); tb = p + '.trim'
    lz = reuse().get(tag); src = 'REUSE'
    if lz is None: lz = ckpt_lazy(out, tag); src = 'checkpoint'
    if lz is not None:
        t0 = time.time(); C.rebuild(f, lz).to_file(cnf)
        r = {'status': 'UNSAT', 'tag': tag, 'lazy': lz, 'reused_lazy': True, 'lazy_from': src, 'seconds': round(time.time() - t0, 2)}
    else:
        hyb = {'cad': CAD, 'conf': CONF, 'grow': GROW, 'opts': CAD_OPTS + ['--binary=true']} if CONF > 0 else None
        r = search(f, out, budget_s=budget, hybrid=hyb)  # v3: resumable; CONF=0: plain search, proof made afterwards
        if r['status'] == 'UNSAT' and isinstance(r.get('lazy'), list): ckpt_write(out, tag, r['lazy'], r.get('seconds'))
    if r['status'] != 'ORIGINAL_MODEL_FOUND': r.pop('edges', None)
    r.update({'s': f['s'], 'a': f['a'], 'b': f['b'], 'c': f['c'], 'h_index': f['h_index'], 'pysat_version': pysat.__version__,
              'encoder': ENCODER})
    if r['status'] != 'UNSAT': return r
    r['cnf_sha256'] = sha(cnf); t1 = time.time()
    import io                                     # R2 #3: the file must be exactly what rebuild() makes from the record
    buf = io.StringIO(); C.rebuild(f, r['lazy']).to_fp(buf)
    if hashlib.sha256(buf.getvalue().encode('ascii')).hexdigest() != r['cnf_sha256']:
        r['status'] = 'ERROR'; r['error'] = 'the CNF file differs from rebuild(f, lazy)'; return r
    if r.pop('proof', None):
        r['cadical_exit'] = 20; r['proof_by'] = 'search'
    else:
        cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=true'] + CAD_OPTS + [cnf, p], capture_output=True, env={})
        r['cadical_exit'] = cp.returncode; r['proof_by'] = 'separate run'
    r['proof_seconds'] = round(time.time() - t1, 1)
    if r['cadical_exit'] != 20 or not os.path.exists(p): return r
    r['proof_raw_bytes'] = os.path.getsize(p); t1 = time.time()
    tr = subprocess.run([TRIM, '-q', '--no-check', p, tb], capture_output=True, env={})
    if tr.returncode != 0 or not os.path.exists(tb): r['trim_exit'] = tr.returncode; return r
    data = open(tb, 'rb').read(); r['proof_trim_bytes'] = len(data)
    xz = lzma.compress(data, preset=1); del data
    os.makedirs(proofs, exist_ok=True); dst = os.path.join(proofs, tag + '.lrat.xz')
    with open(dst + '.tmp', 'wb') as fo: fo.write(xz); fo.flush(); os.fsync(fo.fileno())
    os.replace(dst + '.tmp', dst)
    r['proof_sha256'] = hashlib.sha256(xz).hexdigest(); r['proof_xz_bytes'] = len(xz); del xz
    r['trim_seconds'] = round(time.time() - t1, 1); t1 = time.time()
    for heap in os.environ.get('CAKE_HEAPS', '2000,4000').split(','):
        lk = cake_slot(os.environ.get('CAKE_LOCK', os.path.join(out, '.cake.lock')), CAKE_SLOTS)
        try:
            ck = subprocess.run([CAKE, f'--CML_HEAP_SIZE={heap}', '--CML_STACK_SIZE=256', cnf, tb], capture_output=True, text=True, env={})
        finally:
            os.close(lk)
        if any(l.startswith('s ') for l in ck.stdout.splitlines()): break      # a verdict was printed: no retry
    good = ck.stdout.splitlines() == ['s VERIFIED UNSAT'] and ck.returncode == 0
    r['cake_exit'] = ck.returncode; r['cake_heap_mb'] = int(heap); r['cake_seconds'] = round(time.time() - t1, 1)
    r['cake_lpr'] = 's VERIFIED UNSAT' if good else 'NOT VERIFIED: ' + (ck.stdout + ck.stderr)[-160:]
    if good:
        for x in (cnf, p, tb): os.remove(x)
    return r

def interleave(tags, F):
    """the profiles with e(S) + e(T) <= 23 first (they would be all of layer 92 if every triangle-free graph on 24
    vertices could be made bipartite with 23 deletions), then those with e(S) + e(T) = 24; round robin over the
    profiles inside each group, so that every profile progresses"""
    out = []
    for group in (lambda a, b: a + b <= 23, lambda a, b: a + b > 23):
        by = {}
        for t in tags:
            if group(F[t]['a'], F[t]['b']): by.setdefault((F[t]['s'], F[t]['a'], F[t]['b'], F[t]['c']), []).append(t)
        qs = [by[k] for k in sorted(by)]
        while any(qs):
            for q in qs:
                if q: out.append(q.pop(0))
    return out

if __name__ == '__main__':
    path, out = sys.argv[1], sys.argv[2]; nw = int(sys.argv[3]); budget = float(sys.argv[4])
    pref = sys.argv[5] if len(sys.argv) > 5 else ''
    os.makedirs(out, exist_ok=True); res_path = os.path.join(out, 'results.jsonl')
    done = set()
    if os.path.exists(res_path):                  # a line cut by a killed run is dropped (that formula is redone)
        good = []
        for l in open(res_path, 'rb').read().split(b'\n'):
            if not l.strip(): continue
            try: o = json.loads(l)
            except ValueError: break
            good.append(l); done.add(o['tag'])
        with open(res_path, 'wb') as fo:
            for l in good: fo.write(l + b'\n')
    F = json.load(open(path))
    keep = None
    if os.environ.get('TODO_FILE'):                 # run only the formulas listed there, in that order
        keep = [l.strip() for l in open(os.environ['TODO_FILE']) if l.strip()]
        bad = [t for t in keep if t not in F]
        if bad: sys.exit(f'TODO_FILE names {len(bad)} unknown formulas, e.g. {bad[0]}')
        if len(set(keep)) != len(keep): sys.exit('TODO_FILE repeats a tag')                       # C1 S7
        todo = [t for t in keep if t.startswith(pref) and t not in done]
    else:
        todo = interleave([t for t in sorted(F) if t.startswith(pref) and t not in done], F)
    print(f'{len(todo)} formulas to do ({len(done)} already recorded)', flush=True)
    stop_after = float(os.environ.get('STOP_AFTER', '0')); t_start = time.time()   # seconds: no new formula after this
    def results(pool):
        it_todo = iter(todo); pending = []
        def submit():
            if stop_after and time.time() - t_start > stop_after: return
            t = next(it_todo, None)
            if t is not None: pending.append(pool.apply_async(work, ((path, t, out, budget),)))
        for _ in range(nw): submit()
        while pending:
            ready = [p for p in pending if p.ready()]
            if not ready: time.sleep(1); continue
            for p in ready:
                pending.remove(p); yield p.get(); submit()
        if stop_after and next(it_todo, None) is not None:
            print(f'STOP_AFTER reached: no new formulas started after {stop_after:.0f} s; relaunch to continue', flush=True)
    with mp.Pool(nw, maxtasksperchild=int(os.environ.get('TASKS_PER_CHILD', '20'))) as pool, open(res_path, 'a') as fo:
        for r in results(pool):
            ok = (r['status'] == 'UNSAT' and r.get('cake_lpr') == 's VERIFIED UNSAT' and r.get('cadical_exit') == 20
                  and isinstance(r.get('proof_sha256'), str))
            if ok or r['status'] == 'ORIGINAL_MODEL_FOUND':
                fo.write(json.dumps(r) + '\n'); fo.flush()
            else:
                dest = 'unknown.jsonl' if r['status'] == 'UNKNOWN_BUDGET' else 'failed_attempts.jsonl'
                with open(os.path.join(out, dest), 'a') as fx: fx.write(json.dumps(r) + '\n')
            if not ok: print('ATTENTION', json.dumps({k: v for k, v in r.items() if k not in ('lazy', 'iteration_log')})[:600], flush=True)
