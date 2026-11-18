#!/usr/bin/env python3
"""gcert83.py (encoder version 9 added): made by layers/code/make_gcert_v9.py from the previous gcert83.py (384a2e7c…), adding encoder version 9 (cegar90e.py, 7c416f1c…: version 7 plus the family auts) under the label v9; records may name v7, v8 or v9. Nothing else changed. The previous gcert83.py was: made by layers/code/make_gcert.py from gcert88.py (23efd4b7…) for layer 83 (formulas83_c60.json, f15403b2…, 435 formulas), adding encoder version 8 (cegar90d.py, 3c91eb94…). gcert88.py was: gcert89.py (d1b89923…) for layer 88, changed only in: the formulas pin (formulas88_c65.json,
9835d162…, 432 formulas), its own name in CODE_FILES, the run label l88. gcert89.py was: gcert90d.py for layer 89, with the formulas pin, its own name, the run label l89, v7 records only, and no V1 resume rule (R89A).
The rest of this docstring is gcert90d.py's, about layer 90. --- gcert90d.py: gcert90c.py (review R90C) with a fourth pinned encoder. A record that says "encoder": "v7" is rebuilt
with cegar90c.py (encoder version 7: version 6 plus the family twins, BOUNDS90.md "Version 7"); "v6" with cegar90b.py
(version 6: version 5 plus iso8 and tbip); "v5" with cegar90.py (version 5); no field or "v4" with cegar91.py
(version 4). Everything else is as in gcert90c.py and gcert90b.py (reviews R90C, R90B), whose description follows.
gcert90c.py: gcert90b.py with a third pinned encoder (v6).
gcert90b.py: the layer-90 certificate checker gcert90.py with two pinned encoders (BOUNDS90.md). A record that says
"encoder": "v5" is rebuilt with cegar90.py (encoder version 5: version 4 plus the families b22 and swap); a record with no
"encoder" field, or "v4", with cegar91.py (version 4), as gcert90.py does; any other value stops the run. Both encoders
are pinned (ENCODER_PINS), and each certificate shows its formula unsatisfiable under an encoding of necessary conditions,
so either kind of record excludes its formula. Every result line names the encoder used. With CHECK_RESUME=1, a line
written by gcert90.py (code SHA-256 edb0aacf..., version-4 records only, no "encoder" field) is also kept, under the same
conditions as a line of this checker.
Certificate checker for edge layer 90 (degree-free formulas, one per (profile, H)): every formula's
stored LRAT proof is checked by cake_lpr against the formula rebuilt here. No SAT solver runs in this checker.
The formulas checked are the 428 of formulas90_c67.json: the entries of formulas90.json (8,205 formulas) with cut value
c >= 67, the only ones needed once every 90-edge graph has a cut of at least 67 (L90_ROUTE.md: Corollary C22 at m = 90,
a(22) = 17 and vertex deletion twice). Encoder version 4 (unchanged from layer 91) adds the family a22 to the 322 formulas
with c = 67 (beta = 23), which also rests on a(22) <= 17; version 5 adds b22 to the 100 with c = 68 (beta = 22, the same
facts) and swap (exchanging a vertex of S and one of T cannot raise a maximum cut) to all. Both are pinned below
(ENCODER_PINS) and the checker refuses any other cegar91.py, cegar90.py, cegar90b.py or cegar90c.py.
For each record: rebuild the CNF from the formulas file and the record's lazy list and compare its SHA-256 with the record;
read PROOFS/TAG.lrat.xz (a regular file, not a link), compare its SHA-256 with the record's proof_sha256, decompress it
(xz; the proof is CaDiCaL's LRAT proof after lrat-trim, binary or text) and check it with cake_lpr. A formula passes only
if the CNF and proof hashes match and cake_lpr's stdout is exactly the one line "s VERIFIED UNSAT" with exit code 0
(cake_lpr also exits 0 when it rejects, so the line is what counts). Neither the solver nor the trimmer that made a
proof is trusted: cake_lpr accepts a proof only if it derives the empty clause from exactly the rebuilt formula.
cake_lpr runs with a 2000 MB heap and, only if it printed no "s " line at all (killed, out of space), 4000 MB
(CAKE_HEAPS, default "2000,4000"); CAKE_SLOTS (default 1) lets that many cake_lpr run at once.
Checks before any check runs (exit 1 on failure):
  - formulas90_c67.json has the pinned SHA-256 and 428 formulas, and every record agrees with its formula
    (tag, s, a, b, c, h_index); no tag repeats; every record is UNSAT and has a proof_sha256;
  - the records cover every formula exactly once (with PARTIAL_RECORDS=1 and a tag filter: every selected formula;
    such a run is partial, exit 3 at best);
  - cake_lpr has the pinned SHA-256 (ALLOW_OTHER_BINARIES=1 or ORDER24_TEST_UNIVERSE=1: exit 4 at best).
During the run (the design of gcheck93_all.py after auditor P5's findings; Linux only): the formulas file and cake_lpr
are read once, hashed and used only from memory; each worker runs cake_lpr from a sealed in-memory copy (memfd with
write, grow, shrink and seal seals) of the bytes hashed at start-up; each rebuilt formula and each decompressed proof
goes into a sealed in-memory file, and cake_lpr reads exactly those bytes (/proc/self/fd/N). Nothing that is checked
goes through the file system after it is hashed, so another process writing to PROOFS or WORKDIR during the run cannot
make a formula pass. The checker's own modules (CODE_FILES) are compiled from the source bytes hashed into
code_sha256, never from cached bytecode, and its folder is not left on sys.path. It must be started in isolated mode
(python3 -I) (ALLOW_NOT_ISOLATED=1: exit 4 at best); cake_lpr runs with an empty environment, and any LD_* variable
stops the run (ALLOW_LD_ENV=1: exit 4 at best). Trusted, as for any checker: the kernel; the launch environment and the
dynamic loader with its configuration (/etc/ld.so.preload); the shared libraries cake_lpr links (libc); the Python
interpreter process and its installed packages (PySAT with its C extensions, numpy, networkx; the lzma module); and that
no other process attaches to the checker's processes. A clean launch: an empty /etc/ld.so.preload and
env -i PATH=/usr/bin:/bin HOME=$HOME python3 -I -B gcert90d.py ...
With CHECK_RESUME=1 an existing WORKDIR/CHECK_RESULTS.jsonl is reused: a line is kept only if it reports every
success field, a run and tag of this check with the same record and proof SHA-256 (strings), the pinned cake_lpr, the
same formulas and code SHA-256 and no override; everything else is redone. Resumed lines are trusted as far as WORKDIR
is, and a run that uses any of them ends with exit 5 at best, never 0.
Exit 0 iff every formula passed in this invocation, the run was not filtered and nothing was overridden; 5 if every
formula passed but some passes were resumed; 3 if a tag filter was given and every selected one passed (partial);
4 if everything checked passed under an override; 1 otherwise. Writes WORKDIR/CHECK_RESULTS.jsonl.
Usage: python3 -I gcert90d.py formulas90_c67.json results.jsonl PROOFS WORKDIR [workers] [tag-regex]"""
import sys
if __name__ == '__main__' and not sys.flags.isolated:  # before any other import: without -I the script folder and PYTHON*
    import os                                          # variables could supply modules (P5); os is loaded at start-up anyway
    if os.environ.get('ALLOW_NOT_ISOLATED') != '1': sys.exit('run this checker as python3 -I (isolated mode)')
import os, io, re, json, time, types, hashlib, shutil, subprocess, fcntl, tempfile, stat, lzma, multiprocessing as mp
HERE = os.path.dirname(os.path.abspath(__file__))
CODE_FILES = ('gcert83.py', 'cegar91.py', 'cegar90.py', 'cegar90b.py', 'cegar90c.py', 'cegar90d.py', 'cegar90e.py')
SRC = {f: open(os.path.join(HERE, f), 'rb').read() for f in CODE_FILES}    # the bytes hashed are the bytes compiled
ENCODER_PINS = {'cegar91.py': 'b2f00fd670c5ee7f359692b28811dd50ef07d3ccb1813008ceb6406c8dd4cd7b',   # version 4 (R91B, R90A)
                'cegar90.py': '8d65a5287baf11e7ccf92e72cd5fc69f385967f30b41b8f0982a72aed8a912ec',   # version 5 (BOUNDS90.md, R90B)
                'cegar90b.py': '6e2f884b5b018137aba941182ffa3ba26f653452b434a6457ad03028fb980a88',   # version 6 (R90C)
                'cegar90c.py': '7699f39b78d7703cfb65691f5d7e8cd5f149f6a587400596bbbfb6122ffa86b9',   # version 7 (BOUNDS90.md)
                'cegar90d.py': '3c91eb94a2c3bbef04e6521eac6940cd12ed1bd3571125e7e6028d858ed43c82',   # version 8: version 7 accepting s = 8 (layers <= 87)
                'cegar90e.py': '7c416f1c6e33c6b95ebea72210ecfc0afa8f3b9ec7e29fa844145c118828de8e'}   # version 9: version 7 plus auts (SYM_V9.md)
for _f, _p in ENCODER_PINS.items():
    if hashlib.sha256(SRC[_f]).hexdigest() != _p: sys.exit(f'{_f} is not the pinned encoder')
V1_CODE_SHA = 'edb0aacfd9035f09921534b8f4f39de29c9af9cc4accd6b43ff0aadc9342d67d'   # gcert90.py + cegar91.py (A90 G1)

def from_source(name):
    """compile a module of this folder from its bytes in SRC (P5: a planted __pycache__ file must not run instead)"""
    mod = types.ModuleType(name); mod.__file__ = os.path.join(HERE, name + '.py'); sys.modules[name] = mod
    exec(compile(SRC[name + '.py'], mod.__file__, 'exec'), mod.__dict__)
    return mod

_path = list(sys.path)
C4 = from_source('cegar91')                                                     # encoder version 4; imports numpy, networkx, PySAT
C5 = from_source('cegar90')                                                     # encoder version 5
C6 = from_source('cegar90b')                                                    # encoder version 6
C7 = from_source('cegar90c')                                                    # encoder version 7
C8 = from_source('cegar90d')                                                    # encoder version 8
C9 = from_source('cegar90e')                                                    # encoder version 9
ENC = {'v4': C4, 'v5': C5, 'v6': C6, 'v7': C7, 'v8': C8, 'v9': C9}
sys.path[:] = _path
FORMULAS_PIN = 'f15403b2edb588166563d2d7aed95c0ccc173379719fd7fc1d3e51bb9d77af73'; N_FORMULAS = 435   # formulas83_c60.json
CAKE = os.environ.get('CAKE', os.path.expanduser('~/tools/cake_lpr/cake_lpr'))
CAKE_SLOTS = int(os.environ.get('CAKE_SLOTS', '1'))
PIN = {'cake_lpr': '29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798'}
F_ADD_SEALS = getattr(fcntl, 'F_ADD_SEALS', 1033); F_GET_SEALS = getattr(fcntl, 'F_GET_SEALS', 1034)   # linux/fcntl.h
SEALS = 0x1 | 0x2 | 0x4 | 0x8            # F_SEAL_SEAL | F_SEAL_SHRINK | F_SEAL_GROW | F_SEAL_WRITE

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()

def fd_sha(fd):
    h = hashlib.sha256(); off = 0
    while True:
        b = os.pread(fd, 1 << 20, off)
        if not b: return h.hexdigest()
        h.update(b); off += len(b)

def sealed(data, name):
    """A read-only descriptor of a sealed in-memory file holding exactly `data`: its bytes can no longer change, so the
    bytes hashed are the bytes read or executed through /proc/self/fd/N."""
    fd = os.memfd_create(name, os.MFD_ALLOW_SEALING | os.MFD_CLOEXEC)
    try:
        v = memoryview(data)
        while v: v = v[os.write(fd, v):]
        fcntl.fcntl(fd, F_ADD_SEALS, SEALS)
        ro = os.open(f'/proc/self/fd/{fd}', os.O_RDONLY | os.O_CLOEXEC)
    finally:
        os.close(fd)                                     # no writable descriptor is left (needed to execute it)
    if fcntl.fcntl(ro, F_GET_SEALS) & SEALS != SEALS or fd_sha(ro) != hashlib.sha256(data).hexdigest():
        raise RuntimeError(f'the sealed copy of {name} is not as written')
    return ro

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

W = {}
def init(F, cake, binsha, proofs, lock):                 # pool initializer: runs once in each worker
    W['F'] = F; W['proofs'] = proofs; W['lock'] = lock
    W['cake'] = sealed(cake, 'cake_lpr')
    if fd_sha(W['cake']) != binsha['cake_lpr']:
        raise RuntimeError('the sealed cake_lpr differs from the bytes hashed at start-up')

def read_proof(tag):
    """the bytes of PROOFS/TAG.lrat.xz, opened without following a link and only if it is a regular file"""
    fd = os.open(os.path.join(W['proofs'], tag + '.lrat.xz'), os.O_RDONLY | os.O_NOFOLLOW | os.O_CLOEXEC | os.O_NONBLOCK)   # R2 #1: a FIFO must not block
    try:
        if not stat.S_ISREG(os.fstat(fd).st_mode): raise OSError('not a regular file')
        parts = []
        while True:
            b = os.read(fd, 1 << 22)
            if not b: return b''.join(parts)
            parts.append(b)
    finally:
        os.close(fd)

def code_sha():                                # each file framed by its name and length (P5: no concatenation ambiguity)
    h = hashlib.sha256()
    for f in CODE_FILES:
        b = SRC[f]
        h.update(f.encode() + b'\0' + str(len(b)).encode() + b'\0' + b)
    return h.hexdigest()

def one(a):
    kind, rec, meta = a
    tag = rec['tag']; f = W['F'][tag]
    enc = rec.get('encoder', 'v4')
    out = dict({'tag': tag, 'run': kind, 'cnf_sha256': rec['cnf_sha256'], 'proof_sha256': rec.get('proof_sha256'), 'encoder': enc}, **meta)
    try:
        buf = io.StringIO(); ENC[enc].rebuild(f, rec['lazy']).to_fp(buf)
        data = buf.getvalue().encode('ascii')            # the bytes CNF.to_file writes
        out['cnf_match'] = hashlib.sha256(data).hexdigest() == rec['cnf_sha256']
    except ValueError as e:
        out['cnf_match'] = False; out['rebuild_error'] = str(e)[:200]
    proof = None
    if out['cnf_match']:
        try:
            xz = read_proof(tag)
            out['proof_match'] = isinstance(rec.get('proof_sha256'), str) and hashlib.sha256(xz).hexdigest() == rec['proof_sha256']
            if out['proof_match']: proof = lzma.decompress(xz)
        except (OSError, lzma.LZMAError, MemoryError) as e:
            out['proof_match'] = False; out['proof_error'] = str(e)[:200]
    if proof is not None:
        fc = sealed(data, tag); fp = sealed(proof, tag + '.lrat'); del proof
        try:
            for heap in os.environ.get('CAKE_HEAPS', '2000,4000').split(','):
                lk = cake_slot(W['lock'], CAKE_SLOTS)     # P5: O_NOFOLLOW, no symlink
                try:
                    ck = subprocess.run([f'/proc/self/fd/{W["cake"]}', f'--CML_HEAP_SIZE={heap}', '--CML_STACK_SIZE=256',
                                         f'/proc/self/fd/{fc}', f'/proc/self/fd/{fp}'], pass_fds=(W['cake'], fc, fp),
                                        capture_output=True, text=True, env={})
                finally:
                    os.close(lk)
                if any(l.startswith('s ') for l in ck.stdout.splitlines()): break      # a verdict was printed: no retry
        finally:
            os.close(fc); os.close(fp)
        out['cake_exit'] = ck.returncode; out['cake_heap_mb'] = int(heap)
        good = ck.stdout.splitlines() == ['s VERIFIED UNSAT'] and ck.returncode == 0
        out['cake_lpr'] = 's VERIFIED UNSAT' if good else 'NOT VERIFIED'
        if not good: out['cake_tail'] = (ck.stdout + ck.stderr)[-300:]
    out['pass'] = bool(out['cnf_match'] and out.get('proof_match') is True and out.get('cake_lpr') == 's VERIFIED UNSAT'
                       and out.get('cake_exit') == 0)
    return out

def load(path):
    return [json.loads(l) for l in open(path) if l.strip()]

if __name__ == '__main__':
    fpath, rpath, proofs, work = sys.argv[1:5]; proofs = os.path.abspath(proofs)
    nw = int(sys.argv[5]) if len(sys.argv) > 5 else 2; rx = re.compile(sys.argv[6]) if len(sys.argv) > 6 else None
    partial = os.environ.get('PARTIAL_RECORDS') == '1'
    if partial and not rx: sys.exit('PARTIAL_RECORDS=1 needs a tag filter (a partial check)')
    if not hasattr(os, 'memfd_create'): sys.exit('this checker needs Linux (sealed in-memory files, memfd_create)')
    os.makedirs(work, exist_ok=True); work = os.path.abspath(work)
    override = []
    if not sys.flags.isolated: override.append('NOT ISOLATED: started without python3 -I')   # checked at the top
    ld = sorted(k for k in os.environ if k.startswith('LD_'))
    if ld:                                       # the dynamic loader's variables reach every process started from here
        if os.environ.get('ALLOW_LD_ENV') != '1': sys.exit(f'{", ".join(ld)} is set; unset it (ALLOW_LD_ENV=1 goes on, exit 4 at best)')
        override.append('LD ENVIRONMENT: ' + ', '.join(ld))
    rawF = open(fpath, 'rb').read()              # the bytes checked here are the bytes used
    if hashlib.sha256(rawF).hexdigest() != FORMULAS_PIN or os.environ.get('ORDER24_TEST_UNIVERSE') == '1':
        if os.environ.get('ORDER24_TEST_UNIVERSE') != '1': sys.exit('the formulas file is not the pinned formulas83_c60.json')
        override.append('TEST UNIVERSE: formulas file not checked against the pin')
    F = json.loads(rawF)
    recs = [('l83', r) for r in load(rpath)]
    tags = [r['tag'] for _, r in recs]
    if len(set(tags)) != len(tags): sys.exit('a tag repeats')
    for _, r in recs:
        if r['tag'] not in F: sys.exit(f"record {r['tag']!r} is not a formula of the formulas file")
        f = F[r['tag']]
        if any(r.get(k) != f[k] for k in ('s', 'a', 'b', 'c', 'h_index')): sys.exit(f"record {r['tag']} does not match its formula")
        if r['status'] != 'UNSAT': sys.exit(f"record {r['tag']} is not UNSAT")
        if not isinstance(r.get('proof_sha256'), str): sys.exit(f"record {r['tag']} names no proof")
        enc = r.get('encoder', 'v4')
        if enc not in ('v7', 'v8', 'v9'): sys.exit(f"record {r['tag']} does not name encoder v7, v8 or v9 (layer 83 accepts v7, v8 and v9 records only)")
    if partial:
        sel = {t for t in F if rx.search(t)}
        if not sel <= set(tags): sys.exit('the results do not cover every selected formula')
        print(f'PARTIAL_RECORDS: {len(recs)} records; {len(sel)} formulas selected', flush=True)
    elif set(tags) != set(F): sys.exit('the results do not cover every formula exactly once')
    if not override and len(F) != N_FORMULAS: sys.exit('the pinned formulas file must have 435 formulas')
    if not partial: print(f'coverage: {len(F)} formulas, each exactly once', flush=True)
    bins = {}; binsha = {}
    for name, path in (('cake_lpr', CAKE),):
        b = open(path, 'rb').read(); h = hashlib.sha256(b).hexdigest(); bins[name] = b; binsha[name] = h
        print(f'{name}: {path} sha256 {h}' + ('' if h == PIN[name] else '  (differs from the pinned binary)'))
        if h != PIN[name]:
            if os.environ.get('ALLOW_OTHER_BINARIES') != '1': sys.exit(f'{name} is not the pinned binary')
            override.append(f'OTHER BINARY: {name}')
    for x in os.listdir(work):                   # private folders of earlier runs
        q = os.path.join(work, x)
        if x.startswith('.run-') and os.path.isdir(q) and not os.path.islink(q): shutil.rmtree(q)
    import pysat
    meta = {'bin_sha256': binsha, 'formulas_sha256': hashlib.sha256(rawF).hexdigest(), 'code_sha256': code_sha(),
            'pysat_version': pysat.__version__, 'overrides': list(override)}
    todo = [x for x in recs if not rx or rx.search(x[1]['tag'])]
    outp = os.path.join(work, 'CHECK_RESULTS.jsonl'); resume = os.environ.get('CHECK_RESUME') == '1'
    prev = {}
    if resume and os.path.exists(outp):          # keep earlier passes (a run cut by a time limit); redo the rest
        cur = {(k, r['tag']): (r['cnf_sha256'], r['proof_sha256'], r.get('encoder', 'v4')) for k, r in todo}
        for line in open(outp):
            try: o = json.loads(line)
            except ValueError: break             # a line cut by a killed run: drop it and everything after
            key = (o.get('run'), o.get('tag')) if isinstance(o, dict) else None
            ok_line = (key is not None and all(isinstance(x, str) for x in key) and key in cur
                       and isinstance(o.get('cnf_sha256'), str) and isinstance(o.get('proof_sha256'), str)
                       and (o['cnf_sha256'], o['proof_sha256']) == cur[key][:2]
                       and o.get('pass') is True and o.get('cnf_match') is True and o.get('proof_match') is True
                       and o.get('cake_lpr') == 's VERIFIED UNSAT' and o.get('cake_exit') == 0
                       and o.get('bin_sha256') == PIN and binsha == PIN and o.get('overrides') == [] and not override
                       and o.get('formulas_sha256') == meta['formulas_sha256']
                       and ((o.get('code_sha256') == meta['code_sha256'] and o.get('encoder') == cur[key][2])))
            if ok_line: prev[o['tag']] = o       # same record, binaries, formulas and code: the earlier pass applies
        with open(outp, 'w') as fo:
            for o in prev.values(): fo.write(json.dumps(o) + '\n')
        for x in os.listdir(work):               # leftovers of versions that wrote formulas and proofs into WORKDIR
            if x.endswith('.cnf') or x.endswith('.lrat'): os.remove(os.path.join(work, x))
        print(f'resuming: {len(prev)} passing results kept from an earlier run in {work}', flush=True)
    rest = [x for x in todo if x[1]['tag'] not in prev]
    n = ok = len(prev); pm = 0                   # R2 #4: count proof files read in this run only
    priv = tempfile.mkdtemp(prefix='.run-', dir=work)
    ctx = mp.get_context('fork')
    try:
        with ctx.Pool(nw, initializer=init, initargs=(F, bins['cake_lpr'], binsha, proofs,
                      os.environ.get('CAKE_LOCK', os.path.join(work, '.cake.lock')))) as pool, \
                open(outp, 'a' if resume else 'w') as fo:
            for o in pool.imap_unordered(one, [(k, r, meta) for k, r in rest], chunksize=4):
                n += 1; ok += o['pass']; pm += bool(o.get('proof_match')); fo.write(json.dumps(o) + '\n'); fo.flush()
                if not o['pass']: print('FAIL', json.dumps(o)[:400], flush=True)
    finally:
        shutil.rmtree(priv, ignore_errors=True)
    print(f'checked {n} formulas (of {len(F)}): {ok} pass; proof files read and matching the record in this run: {pm}')
    if prev: print(f'RESUMED: {len(prev)} of these passes were taken from earlier runs in {work} (not re-verified now; '
                   f'trusted as far as that folder is); {n - len(prev)} were verified in this run')
    for o in override: print('OVERRIDE IN FORCE:', o)
    if rx:
        print(f'PARTIAL RUN: {n} of {len(F)} formulas selected by the tag filter; this is not a full check')
    if ok != n or (not rx and n != len(F)) or n == 0: sys.exit(1)                                  # R2 #5: nothing checked is a failure
    sys.exit(4 if override else (3 if rx else (5 if prev else 0)))
