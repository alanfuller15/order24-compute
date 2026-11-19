#!/usr/bin/env python3
"""exp/recake.py -- re-check of a cube-and-conquer formula whose stitch finished but whose producer cake_lpr check gave no
verdict (ccc90.py exit 1, "NOT VERIFIED: CakeML heap space exhausted"; line in failed_attempts.jsonl). Producer-side,
not trusted, approves nothing: it makes the record line ccc90.py would have made, so that the auditors check it with the
pinned gcert<M>.py like any other record (audit.yml with run_id = this exp run, artifact = its name).

Usage (exp.yml, RUN_ID + ARTIFACT + TAG + GH_TOKEN + GH_REPO from its inputs):
  python3 -I -B exp/recake.py FORMULAS_JSON CNF_SHA256 PROOF_SHA256 [HEAP_MB]
RECAKE_IN=<dir> (local tests): read the producer artifact's files from <dir> instead of downloading them.

Steps.
 1. From the producer artifact (ranged reads of its zip; nothing else of it): failed_attempts.jsonl, cube/TAG/items.jsonl,
    TAG.cnf and proofs/TAG.lrat.xz. The last failed line of TAG must name exactly CNF_SHA256 and PROOF_SHA256, and the
    xz file must hash to PROOF_SHA256.
 2. The CNF is rebuilt as ccc90.py's stitch does it: rebuild(f, items) with the record's encoder (v7 = cegar90c, v9 =
    cegar90e), items = every line of items.jsonl in order (ccc90.load_items); its SHA-256 must be CNF_SHA256 and equal
    the artifact's TAG.cnf.
 3. A: the proof exactly as recorded (xz -> the stitched LRAT, size proof_raw_bytes) is checked by cake_lpr with HEAP_MB
    (default 12000) -- the check of the exact hashes above.
 4. B: lrat-trim -q --no-check (ccc90.py's call; address space capped at 14.5 GB) on it, xz -1 -T1, cake_lpr with
    2000 then 4000 MB (the auditors' gcert heaps, next heap only without an "s " line), then HEAP_MB.
 5. Record: ccc90.py's line (the failed line's fields in its order, "lazy" = items after "tag") with the proof that is
    best for the audit: B if it verified (smaller; the pinned checker's heaps are 2000/4000 MB), else A.
    Its proof_* and cake_* fields are those of that proof and check; nothing else changes. exp_out/results.jsonl +
    exp_out/proofs/TAG.lrat.xz; exp_out/recake.json has both checks. Verified = cake_lpr stdout is exactly
    "s VERIFIED UNSAT" and its exit code 0 (ccc90.py's rule). Nothing verified: no results.jsonl, GATE_FAIL.
"""
import sys, os, io, json, time, hashlib, subprocess, shutil, zipfile, resource, importlib, urllib.request, urllib.error
R = os.getcwd(); O = os.path.join(R, 'exp_out'); os.makedirs(O, exist_ok=True)
GF = os.path.join(O, 'GATE_FAIL'); open(GF, 'w').write('incomplete: recake.py did not reach its clean end\n')
sys.path.insert(0, os.path.join(R, 'code'))
CAKE = os.path.join(R, 'bin', 'cake_lpr'); TRIM = os.path.join(R, 'bin', 'lrat-trim')
CAKE_SHA = '29e02af756c1f0fc4ccac78e9a908e0d8ef01201786f257f1b27b26603390798'
fpath, want_cnf, want_proof = sys.argv[1:4]; HEAP = int(sys.argv[4]) if len(sys.argv) > 4 else 12000
TAG = os.environ['TAG']; RUN_ID = os.environ.get('RUN_ID', ''); ART = os.environ.get('ARTIFACT', '')
REPO = os.environ.get('GH_REPO', ''); LOCAL = os.environ.get('RECAKE_IN', '')
info = {'tag': TAG, 'run': RUN_ID, 'artifact': ART, 'heap_mb': HEAP, 'job_run': os.environ.get('GITHUB_RUN_ID', 'local'),
        'commit': os.environ.get('GITHUB_SHA', 'local'), 'steps': []}
def say(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
def save(): json.dump(info, open(os.path.join(O, 'recake.json'), 'w'), indent=1)
def die(msg): info['error'] = msg; save(); open(GF, 'w').write(msg + '\n'); say('FAIL:', msg); sys.exit(1)
def fsha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 24), b''): h.update(b)
    return h.hexdigest()
def avail(p): return shutil.disk_usage(p).free >> 30
def meminfo():
    try: return {l.split(':')[0]: int(l.split()[1]) >> 10 for l in open('/proc/meminfo') if l.split(':')[0] in ('MemTotal', 'MemAvailable', 'SwapTotal')}
    except OSError: return {}

# work folder: the bigger disk of a hosted runner (/mnt), else ./work
W = os.path.join(R, 'work')
if os.environ.get('GITHUB_ACTIONS') == 'true' and os.path.isdir('/mnt'):
    subprocess.run(['sudo', 'mkdir', '-p', '/mnt/recake']); subprocess.run(['sudo', 'chown', str(os.getuid()), '/mnt/recake'])
    if os.access('/mnt/recake', os.W_OK) and avail('/mnt') > avail(R): W = '/mnt/recake'
os.makedirs(W, exist_ok=True); IN = os.path.join(W, 'in'); os.makedirs(IN, exist_ok=True)
info.update({'work': W, 'disk_free_gb': avail(W), 'mem_mb': meminfo(), 'nproc': os.cpu_count()})
if fsha(CAKE) != CAKE_SHA: die('bin/cake_lpr is not the pinned binary')
info['cake_sha256'] = CAKE_SHA; info['trim_sha256'] = fsha(TRIM); save()

# ---- 1. inputs
NAMES = ['failed_attempts.jsonl', f'cube/{TAG}/items.jsonl', f'{TAG}.cnf', f'proofs/{TAG}.lrat.xz']
class Ranged(io.RawIOBase):
    """seekable reader of an artifact zip through HTTP Range requests on its signed blob URL (ops/refill.py's method)"""
    def __init__(s, aid): s.aid = aid; s.url = s._blob(); s.pos = 0; s.size = int(urllib.request.urlopen(urllib.request.Request(s.url, method='HEAD'), timeout=60).headers['Content-Length'])
    def _blob(s):
        class NR(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *x, **k): return None
        try: urllib.request.build_opener(NR).open(urllib.request.Request(f'https://api.github.com/repos/{REPO}/actions/artifacts/{s.aid}/zip', headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN']}), timeout=60)
        except urllib.error.HTTPError as e:
            if e.headers.get('Location'): return e.headers['Location']
            raise
        raise RuntimeError('artifact zip: no redirect')
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.pos
    def seek(s, o, w=0): s.pos = o if w == 0 else (s.pos + o if w == 1 else s.size + o); return s.pos
    def readinto(s, b):
        n = min(len(b), s.size - s.pos, 64 << 20)
        if n <= 0: return 0
        for t in range(6):
            try: d = urllib.request.urlopen(urllib.request.Request(s.url, headers={'Range': f'bytes={s.pos}-{s.pos + n - 1}'}), timeout=300).read(); break
            except Exception:
                if t == 5: raise
                time.sleep(10 * (t + 1)); s.url = s._blob()
        b[:len(d)] = d; s.pos += len(d); return len(d)
t0 = time.time()
if LOCAL:
    for n in NAMES:
        os.makedirs(os.path.dirname(os.path.join(IN, n)) or IN, exist_ok=True); shutil.copyfile(os.path.join(LOCAL, n), os.path.join(IN, n))
else:
    import urllib.parse
    req = urllib.request.Request(f'https://api.github.com/repos/{REPO}/actions/runs/{RUN_ID}/artifacts?per_page=100', headers={'Authorization': 'Bearer ' + os.environ['GH_TOKEN']})
    arts = [a for a in json.load(urllib.request.urlopen(req, timeout=60))['artifacts'] if a['name'] == ART and not a['expired']]
    if len(arts) != 1: die(f'{len(arts)} live artifacts named {ART} in run {RUN_ID}')
    info['artifact_id'] = arts[0]['id']; info['artifact_bytes'] = arts[0]['size_in_bytes']
    zf = zipfile.ZipFile(io.BufferedReader(Ranged(arts[0]['id']), buffer_size=64 << 20))
    have = set(zf.namelist())
    for n in NAMES:
        if n not in have: die(f'artifact has no {n}')
        p = os.path.join(IN, n); os.makedirs(os.path.dirname(p), exist_ok=True)
        with zf.open(n) as fi, open(p, 'wb') as fo: shutil.copyfileobj(fi, fo, 64 << 20)
        say('fetched', n, os.path.getsize(p))
info['steps'].append({'step': 'fetch', 'seconds': round(time.time() - t0, 1)})
fl = [json.loads(l) for l in open(os.path.join(IN, 'failed_attempts.jsonl')) if l.strip()]
fl = [x for x in fl if x.get('tag') == TAG]
if not fl: die('no failed_attempts line for the tag')
F = fl[-1]; info['failed_line'] = F
if F.get('cnf_sha256') != want_cnf or F.get('proof_sha256') != want_proof: die('the failed line names other hashes')
if F.get('status') != 'UNSAT' or F.get('proof_by') != 'cube-and-conquer' or 'lazy' in F: die('not a ccc90 stitch line')
xzp = os.path.join(IN, 'proofs', TAG + '.lrat.xz')
if fsha(xzp) != want_proof or os.path.getsize(xzp) != F['proof_xz_bytes']: die('proof file does not match PROOF_SHA256 / proof_xz_bytes')

# ---- 2. CNF
enc = {'v7': 'cegar90c', 'v9': 'cegar90e'}.get(F.get('encoder'))
if not enc: die(f"encoder {F.get('encoder')!r} not handled")
os.environ.setdefault('MASKS12', os.path.join(R, 'data', 'masks12.npy'))
C = importlib.import_module(enc)
f = json.load(open(fpath))[TAG]
items = []
for l in open(os.path.join(IN, 'cube', TAG, 'items.jsonl'), 'rb'):
    try: o = json.loads(l)
    except ValueError: continue
    items += o['items']
fresh = C.rebuild(f, items); buf = io.StringIO(); fresh.to_fp(buf); data = buf.getvalue().encode('ascii'); del buf, fresh
csha = hashlib.sha256(data).hexdigest(); cnfp = os.path.join(W, TAG + '.cnf')
with open(cnfp, 'wb') as fo: fo.write(data)
del data
info.update({'encoder_module': enc, 'items': len(items), 'cnf_rebuilt_sha256': csha, 'cnf_artifact_sha256': fsha(os.path.join(IN, TAG + '.cnf'))})
if csha != want_cnf or info['cnf_artifact_sha256'] != want_cnf: save(); die('rebuilt CNF SHA-256 differs')
os.remove(os.path.join(IN, TAG + '.cnf')); save(); say('cnf rebuilt', csha, len(items), 'items')

def cake(proof, heaps, label):
    """ccc90.py's cake loop: next heap only if no "s " line; verified = stdout exactly 's VERIFIED UNSAT' and exit 0"""
    res = []
    for h in heaps:
        t = time.time(); r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
        ck = subprocess.run([CAKE, f'--CML_HEAP_SIZE={h}', '--CML_STACK_SIZE=256', cnfp, proof], capture_output=True, text=True, env={})
        r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
        e = {'check': label, 'heap_mb': h, 'exit': ck.returncode, 'seconds': round(time.time() - t, 1), 'cpu': round(r1.ru_utime + r1.ru_stime - r0.ru_utime - r0.ru_stime, 1),
             'maxrss_mb_children': r1.ru_maxrss >> 10, 'stdout': ck.stdout[-400:], 'stderr': ck.stderr[-400:],
             'verified': ck.stdout.splitlines() == ['s VERIFIED UNSAT'] and ck.returncode == 0}
        res.append(e); info['steps'].append(e); save(); say(label, 'heap', h, 'exit', ck.returncode, repr(ck.stdout.strip()[-80:]), repr(ck.stderr.strip()[-80:]), e['seconds'], 's')
        if any(l.startswith('s ') for l in ck.stdout.splitlines()): break
    return res

# ---- 3. A: the recorded proof
raw = os.path.join(W, TAG + '.lrat'); t = time.time()
if subprocess.run(f'xz -dc -T1 "{xzp}" > "{raw}"', shell=True).returncode != 0: die('xz -d failed')
rawb = os.path.getsize(raw); info['steps'].append({'step': 'unxz', 'bytes': rawb, 'seconds': round(time.time() - t, 1)})
if rawb != F['proof_raw_bytes']: die('decompressed size differs from proof_raw_bytes')
A = cake(raw, [HEAP], 'A_recorded')[-1]

# ---- 4. B: trimmed
tb = raw + '.trim'; t = time.time()
def cap(): resource.setrlimit(resource.RLIMIT_AS, (int(14.5 * (1 << 30)),) * 2)
tr = subprocess.run([TRIM, '-q', '--no-check', raw, tb], capture_output=True, env={}, preexec_fn=cap)
info['steps'].append({'step': 'trim', 'exit': tr.returncode, 'seconds': round(time.time() - t, 1), 'stderr': tr.stderr[-300:].decode(errors='replace'),
                      'maxrss_mb_children': resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss >> 10}); save()
B = None; trimb = None
if tr.returncode == 0 and os.path.exists(tb):
    trimb = os.path.getsize(tb); os.remove(raw); txz = tb + '.xz'; t = time.time()
    if subprocess.run(f'xz -1 -T1 -c "{tb}" > "{txz}"', shell=True).returncode == 0:
        info['steps'].append({'step': 'trim_xz', 'trim_bytes': trimb, 'xz_bytes': os.path.getsize(txz), 'seconds': round(time.time() - t, 1)})
        # the bytes checked must be the bytes recorded: decompress the xz again and compare with the trimmed file
        if subprocess.run(f'xz -dc "{txz}" | cmp - "{tb}"', shell=True).returncode != 0: die('trimmed xz does not decompress to the trimmed proof')
        Bs = cake(tb, [2000, 4000], 'B_trimmed')
        if not Bs[-1]['verified'] and not any(l.startswith('s ') for l in Bs[-1]['stdout'].splitlines()) and HEAP > 4000: Bs += cake(tb, [HEAP], 'B_trimmed')
        B = Bs[-1]
else:
    say('lrat-trim failed', tr.returncode)

# ---- 5. record
choice = 'B' if B and B['verified'] else ('A' if A['verified'] else None)
info['choice'] = choice
if choice is None: die('cake_lpr verified neither the recorded nor the trimmed proof')
if choice == 'B': pfile = tb + '.xz'; ck = B; ptrim = True
else: pfile = xzp; ck = A; ptrim = False
psha = fsha(pfile); pxz = os.path.getsize(pfile)
r = {}
for k, v in F.items():
    r[k] = v
    if k == 'tag': r['lazy'] = items
r.update({'proof_raw_bytes': rawb, 'proof_trim_bytes': trimb if ptrim else rawb, 'proof_trimmed': ptrim, 'proof_sha256': psha,
          'proof_xz_bytes': pxz, 'cake_exit': ck['exit'], 'cake_heap_mb': ck['heap_mb'], 'cake_seconds': ck['seconds'], 'cake_lpr': 's VERIFIED UNSAT'})
os.makedirs(os.path.join(O, 'proofs'), exist_ok=True)
shutil.move(pfile, os.path.join(O, 'proofs', TAG + '.lrat.xz'))
if fsha(os.path.join(O, 'proofs', TAG + '.lrat.xz')) != psha: die('moved proof changed')
with open(os.path.join(O, 'results.jsonl'), 'w') as fo: fo.write(json.dumps(r) + '\n')
info['record'] = {k: v for k, v in r.items() if k != 'lazy'}; info['record_sha256'] = fsha(os.path.join(O, 'results.jsonl'))
info['verdict'] = f"{TAG}: s VERIFIED UNSAT ({'trimmed' if ptrim else 'recorded'} proof {psha}, cnf {csha}, heap {ck['heap_mb']} MB)"
info['A_verified'] = A['verified']; info['B_verified'] = bool(B and B['verified']); save()
say(info['verdict']); os.remove(GF)
