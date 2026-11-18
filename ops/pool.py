"""ops/pool.py: the manager's refill policy `shard_ccc.py pool RUN [FREE]` (layers/code/shard_ccc.py, version of 04:35Z 11-18),
ported with every path and input given as an argument, so the refill workflow (and the manager, for tests) can run it.
The policy is unchanged: a finished chain OR shard run is continued with ONE formula per chunk (records surface as soon as a
formula is done) and 4 shards per job; a shard run is first joined and re-sharded (workflow input reshard=1); every formula
gets 1 job and the FREE job slots go one at a time to the formula with the most predicted work left per job (cost-to-go,
open-cube count when no tree.json), capped by POOL_JMAX (6) and by its open cubes; duplicate chain families are dropped per
primary.json; a sharded formula whose every shard ended with shard_done goes to a merge job instead.

Differences from shard_ccc.py (none of them changes a decision for the same inputs):
  - inputs: --arts (artifact names of RUN), --gdir (template with {M} and {run}: where <artifact>/chunk.txt, cube/<tag>/log.jsonl,
    cube/<tag>/tree.json live), --recorded (files of recorded tags, one per line, or results.jsonl files), --primary, --cost
    (ops/cost_model.json, JSON trees instead of opt/cost_model.pkl), --votes (data/pred_votes.json), --repo (where chunk files go).
  - it never commits or dispatches: it writes the chunk files (unless --nowrite) and prints the same lines as shard_ccc.py
    ('DRY dispatch <body>' for each dispatch, in order); --plan FILE also gets them as JSON {commits, dispatches, stop, lines}.
  - ORIGINAL_MODEL_FOUND: exit code 2 and plan.stop (shard_ccc.py: sys.exit with the same message). Nothing of that run is
    dispatched by the caller (shard_ccc.py could already have dispatched an earlier wave of the same run: stricter here).
  - artifact names ending in -meta are ignored (they never matched the regex anyway: shown in the test).
  - encoder (v9 package): a wave's encoder label is read from its fetched state (cube/*/tree.json "encoder") and records
    (results.jsonl "encoder"), over all its shard folders. v7 or no label: the dispatch bodies are exactly as before (no
    "encoder" input, so produce.yml's default cegar90c). v9: the ccc and merge bodies carry "encoder": "cegar90e". Two
    different labels, or any other label (v6, ...): the wave is NOT continued (handle by hand), nothing is written for it.
Producer-side only: nothing here records, audits, deletes or closes anything."""
import sys, os, json, re, glob, shutil, argparse, math, struct

ap = argparse.ArgumentParser()
ap.add_argument('run'); ap.add_argument('free', nargs='?', default='0')
ap.add_argument('--arts', required=True, help='file: artifact names of RUN, one per line')
ap.add_argument('--gdir', required=True, help='template, e.g. layers/l{M}/gha/{run} or work/{run}')
ap.add_argument('--recorded', action='append', default=[], help='file of recorded tags (one per line) or a results.jsonl; repeatable')
ap.add_argument('--primary', default='')
ap.add_argument('--cost', default='')
ap.add_argument('--votes', default='')
ap.add_argument('--repo', required=True)
ap.add_argument('--plan', default='')
ap.add_argument('--nowrite', action='store_true', help='plan only: write no chunk/seed files')
a = ap.parse_args()
run = a.run; R = a.repo; WRITE = not a.nowrite
FREE = int(a.free) if a.free.isdigit() else 0
PLAN = {'run': run, 'free': FREE, 'commits': [], 'dispatches': [], 'stop': None, 'lines': []}

def say(s): print(s); PLAN['lines'].append(s)
def finish(code=0):
    if a.plan: json.dump(PLAN, open(a.plan, 'w'), indent=1)
    sys.exit(code)

_REC = set()
for f in a.recorded:
    if not os.path.exists(f): continue
    for l in open(f):
        l = l.strip()
        if not l: continue
        if l.startswith('{'):
            try: _REC.add(json.loads(l)['tag'])
            except Exception: pass
        else: _REC.add(l.split()[0])
def recorded(M): return _REC                 # tags carry their layer (L<M>_...): one set serves every layer

def wopen(p):
    if not WRITE: return open(os.devnull, 'w')
    os.makedirs(os.path.dirname(p), exist_ok=True); return open(p, 'w')
def makedirs(p):
    if WRITE: os.makedirs(p, exist_ok=True)
def commit(paths, msg): PLAN['commits'].append({'paths': paths, 'msg': msg})
def seeds(base, nxt):
    for cand in (base, re.sub(r'\d+$', '', base)):
        p = f'{R}/ckpt/{cand}.jsonl.xz'
        if os.path.exists(p):
            if WRITE: shutil.copy(p, f'{R}/ckpt/{nxt}.jsonl.xz')
            return [f'ckpt/{nxt}.jsonl.xz']
    return []

arts = [l.strip() for l in open(a.arts) if l.strip() and not l.strip().endswith('-meta')]

# ---- cost model (JSON trees; same arithmetic as sklearn GradientBoostingRegressor.predict: float32 features, sequential sum)
try:
    import numpy as np
except Exception:
    np = None
def _f32(x): return float(np.float32(x)) if np is not None else struct.unpack('f', struct.pack('f', x))[0]
try:
    CMJ = json.load(open(a.cost)); VT = json.load(open(a.votes)); CM = True
except Exception:
    CM = None
def _predict_one(x):
    x = [_f32(v) for v in x]; s = CMJ['init']; lr = CMJ['lr']
    for L, Rr, F, Th, V in CMJ['trees']:
        n = 0
        while L[n] != -1: n = L[n] if x[F[n]] <= Th[n] else Rr[n]
        s += lr * V[n]
    return s

def gh_dispatch_body(inputs): return json.dumps({'ref': 'main', 'inputs': inputs})

ENC_MOD = {'v7': 'cegar90c', 'v9': 'cegar90e'}          # encoder label (tree.json, records) -> produce.yml input `encoder`
def wave_labels(dirs):
    """the encoder labels found in the fetched state of these shard folders: every cube/*/tree.json and results.jsonl line"""
    out = set()
    for d in dirs:
        for tp in sorted(glob.glob(f'{d}/cube/*/tree.json')):
            try: out.add(json.load(open(tp)).get('encoder'))
            except ValueError: out.add('unreadable tree.json')
        if os.path.exists(f'{d}/results.jsonl'):
            for l in open(f'{d}/results.jsonl', errors='replace'):
                try: r = json.loads(l)
                except ValueError: continue
                if isinstance(r, dict) and r.get('encoder'): out.add(r['encoder'])
    return out

PRIMARY = json.load(open(a.primary)) if a.primary and os.path.exists(a.primary) else {}
waves = {}
for an in arts:
    m = re.match(r'(m(\d\d)([c-f])\S*?)-(h\d+[a-z]?)(?:k(\d+)of(\d+))?$', an)
    if m:   # 2026-11-18: merge waves (name ending in m) are read too: a merge job that hit its deadline with open cubes left no record
            # and was never continued (L81_s10a4b18c59_0001 sat 2 cubes from done for 16 h); a finished merge has its tag recorded -> nothing left
        waves.setdefault((m.group(1), int(m.group(2))), {}).setdefault(m.group(4), []).append((an, m.group(5), m.group(6)))

def state_open(dirs, tag):   # open cubes and whether every shard is done, from the fetched logs (a joined state starts with a "merged" event)
    closed = set(); split = set(); n0 = 0; alldone = True; omf = False
    for d in dirs:
        lp = f'{d}/cube/{tag}/log.jsonl'
        if not os.path.exists(lp): return None
        ev = [json.loads(l) for l in open(lp) if l.strip()]; c1 = set(); s1 = set()
        for e in ev:
            if e.get('event') == 'cubes': n0 = e.get('n', n0)
            elif e.get('event') == 'merged': n0 = e.get('open', 0); c1 = set(); s1 = set()
            elif e.get('event') == 'closed': c1.add(e['cube'])
            elif e.get('event') == 'split': s1.add(e['cube'])
        closed |= c1; split |= s1
        last = ev[-1].get('event') if ev else None
        omf |= last == 'ORIGINAL_MODEL_FOUND'; alldone &= last == 'shard_done'
    return n0 + len(split) - len(closed), alldone, omf

def cost_to_go(dirs, tag):
    """predicted core-hours left for this formula: sum over its open cubes of the cost model (None if no tree.json)"""
    if CM is None: return None
    own = VT['tags'].index(tag) if tag in VT['tags'] else -1; X = []; seen = set()
    for d in dirs:
        tp = f'{d}/cube/{tag}/tree.json'
        if not os.path.exists(tp): return None
        t = json.load(open(tp)); roots = set(t.get('shard', {}).get('roots', [])) or None
        split_by_time = set()
        for l in open(f'{d}/cube/{tag}/log.jsonl'):
            if '"split"' in l:
                e = json.loads(l)
                if e.get('event') == 'split' and 'predicted' not in e: split_by_time.add(e['cube'])
        for c in t['open']:
            k = ' '.join(map(str, c))
            if k in seen or not (roots is None or any(' '.join(map(str, c[:n])) in roots for n in range(len(c) + 1))): continue
            seen.add(k); o = [x for gg, x in VT['votes'].get(k, []) if gg != own]
            X.append([int(' '.join(map(str, c[:-1])) in split_by_time), int(' '.join(map(str, c[:-2])) in split_by_time), len(c), (sum(o) / len(o)) if o else -1, min(len(o), 20)])
    if not X: return 0.0
    ys = [math.expm1(_predict_one(x)) for x in X]
    tot = float(np.array(ys).sum()) if np is not None else math.fsum(ys)
    return CMJ.get('calib', 2.0) * tot / 3600   # x2: calibration on mid-run snapshots of finished formulas (median actual/predicted 1.96)

for (wave, M), chunks in sorted(waves.items()):
    rec = recorded(M); G = a.gdir.format(M=M, run=run); fam = re.match(r'(m\d\d[c-f])', wave).group(1)
    sharded = any(k is not None for v in chunks.values() for _, k, _ in v)
    cont = []; merge_chunks = {}; bad = False
    for ch, lst in sorted(chunks.items()):
        if sharded:
            N = int(lst[0][2]); have = {int(k) for _, k, _ in lst}
            if have != set(range(N)): say(f'{wave}-{ch}: shards missing {sorted(set(range(N)) - have)}: NOT continued (handle by hand)'); bad = True; continue
        dirs = [f'{G}/{x}' for x, _, _ in lst]
        if any(not os.path.exists(f'{d}/chunk.txt') for d in dirs): say(f'{wave}-{ch}: not fetched: nothing done for this wave'); bad = True; break
        tags = open(f'{dirs[0]}/chunk.txt').read().split(); left = [t for t in tags if t not in rec]
        for idx, t in enumerate(tags):
            if t in rec: continue
            keep = PRIMARY.get(t)
            if keep is not None and not any(wave.startswith(kp) for kp in keep): say(f'{wave}-{ch} {t}: family {fam} dropped (kept: {keep})'); continue
            so = state_open(dirs, t)
            if so is None: say(f'{wave}-{ch} {t}: no fetched log: NOT continued'); bad = True; continue
            nopen, alldone, omf = so
            if omf:
                PLAN['stop'] = f'{t}: ORIGINAL_MODEL_FOUND: STOP'; PLAN['stop_layer'] = M; print(PLAN['stop'], file=sys.stderr); finish(2)
            nb = ch if (len(tags) == 1 or re.search(r'[a-z]$', ch)) else ch + 'abcdefgh'[idx]
            if sharded and alldone: merge_chunks.setdefault(ch, []).append(t)
            else: cont.append((nb, t, nopen, cost_to_go(dirs, t)))
    if bad and not cont and not merge_chunks: continue
    labs = wave_labels([f'{G}/{x}' for lst in chunks.values() for x, _, _ in lst])
    if (cont or merge_chunks) and (len(labs) > 1 or not labs <= set(ENC_MOD)):
        say(f'{wave}: encoder labels {sorted(map(str, labs))}: NOT continued (handle by hand)'); continue
    enc = ENC_MOD.get(next(iter(labs)), 'cegar90c') if len(labs) == 1 else 'cegar90c'
    encin = {} if enc == 'cegar90c' else {'encoder': enc}   # v7: bodies unchanged (produce.yml default cegar90c)
    if sharded:
        k = int(re.search(r'n(\d+)$', wave).group(1)) + 1 if re.search(r'n\d+$', wave) else 2
        stem = re.sub(r'n\d+$', '', wave); nw = f'{stem}n{k}'; mw = f'{stem}m'
    else: nw = f'{wave}s4'
    if merge_chunks:
        makedirs(f'{R}/chunks/{mw}')
        for ch, ts in merge_chunks.items():
            with wopen(f'{R}/chunks/{mw}/{ch}.txt') as fo: fo.write('\n'.join(ts) + '\n')
        commit([f'chunks/{mw}'], f'chunks {mw}: merge the finished shards of {wave} (run {run})')
        body = gh_dispatch_body({'wave': mw, 'mode': 'merge', 'chunks': json.dumps(sorted(merge_chunks)), 'formulas': f'formulas{M}_c{M - 23}.json',
                                 'grun': 'grun90.py', 'par': str(len(merge_chunks)), 'prev_run': str(run), 'prev_wave': wave, 'tune': '1500,60', 'fan': '1', **encin})
        PLAN['dispatches'].append({'body': body, 'jobs': len(merge_chunks), 'layer': M, 'wave': mw}); say('DRY dispatch ' + body)
    if cont:
        makedirs(f'{R}/chunks/{nw}'); names = []; extra = max(0, FREE - len(cont))
        JMAX = int(os.environ.get('POOL_JMAX', '6'))
        Jof = {nb: 1 for nb, _, _, _ in cont}; budget = extra
        def need(item): nb, t, nopen, cost = item; return (cost if cost is not None else nopen) / Jof[nb]
        while budget > 0:
            cand = [it for it in cont if Jof[it[0]] < min(JMAX, -(-max(it[2], 1) // 4))]
            if not cand: break
            Jof[max(cand, key=need)[0]] += 1; budget -= 1
        for nb, t, nopen, cost in cont:
            J = Jof[nb]
            N = max(1, min(4 * J, nopen))                                          # never more shards than open cubes
            for i in range(N):
                nm = f'{nb}k{i}of{N}'
                with wopen(f'{R}/chunks/{nw}/{nm}.txt') as fo: fo.write(t + '\n')
                if i % 4 == 0: names.append(nm)
            say(f'{nw}-{nb}: {t} {nopen} open cubes, cost-to-go {cost if cost is None else round(cost, 1)} core-h -> {N} shards in {J} job(s)')
        with wopen(f'{R}/chunks/{nw}/FAN') as fo: fo.write('all\n')
        commit([f'chunks/{nw}'] + seeds(wave, nw), f'chunks {nw}: pool {wave} (run {run}): one formula per chunk, 4 shards per job' + (', shards joined and re-sharded' if sharded else ''))
        body = json.dumps({'ref': 'main', 'inputs': {'wave': nw, 'mode': 'ccc', 'chunks': json.dumps(names), 'formulas': f'formulas{M}_c{M - 23}.json', 'grun': 'grun90.py',
                                                     'par': str(len(names)), 'prev_run': str(run), 'prev_wave': wave, 'tune': '3600,60' if M % 2 else '1500,60', 'fan': 'all', 'reshard': '1' if sharded else '',
                                                     'window': os.environ.get('POOL_WINDOW', '9000'), **encin}})
        PLAN['dispatches'].append({'body': body, 'jobs': len(names), 'layer': M, 'wave': nw}); say('DRY dispatch ' + body)
    if not cont and not merge_chunks: say(f'{wave}: nothing left')
finish(0)
