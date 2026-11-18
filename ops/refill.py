"""ops/refill.py: one refill pass, run by .github/workflows/refill.yml (or by the manager with --dry for a test).
Moves the manager's opt/autochain.sh -> shard_ccc.py pool loop into the repo. Producer-side scheduling only: it never records,
audits, deletes, closes or cancels anything. What it does, in order:
  1. control/HOLD present -> exit 0 at once (nothing read, nothing written except the status page).
  2. lists the produce runs created after ops/config.json "cutoff"; a COMPLETED run not in ops/scanned_runs.txt is new.
  3. per new run (oldest first): downloads only its <artifact>-meta artifacts (results.jsonl, chunk.txt, logs, tree.json of every
     shard); a job without a meta artifact (dispatched before the meta step existed) is read with HTTP range requests from the
     full artifact, small members only (as layers/code/fetch_layer.py does), so no proof is ever downloaded.
  4. ORIGINAL_MODEL_FOUND anywhere (a log event, a cube ORIGINAL_MODEL_FOUND.json, a results.jsonl line, a .log line) ->
     STOP: writes ops/ALERT and control/HOLD, commits them, dispatches nothing more, exit 3 (a failed run = an alert).
  5. every finished formula (results.jsonl status UNSAT) that is not in ops/recorded.txt goes to ops/new_records.txt
     (tag, layer, run, artifact): the manager fetches, audits and records it.
  6. a successful run whose first non-meta artifact (the API lists newest first, so -meta artifacts are skipped) is a c/d/e/f chain or shard wave is continued by ops/pool.py (= shard_ccc.py pool),
     FREE = cap - (GitHub jobs in progress or queued, this refill job not counted). If the plan needs more jobs than are
     free, the run waits for the next pass (never more than `cap` jobs). Merge waves need no continuation.
  7. live: ledger + chunk files + ops/new_records.txt committed and pushed FIRST (a kill in between must never cause a second
     dispatch), then produce.yml is dispatched exactly with pool's bodies. --dry: everything except commit and dispatch.
Live needs ops/config.json "live": true; --dry or live:false always means dry (a manual dry_run=false cannot override it).
Writes $WORK/pass.json for ops/status.py."""
import os, sys, json, re, time, glob, subprocess, zipfile, io, shutil, argparse

ap = argparse.ArgumentParser()
ap.add_argument('--dry', action='store_true'); ap.add_argument('--work', default=os.environ.get('RUNNER_TEMP', '/tmp') + '/refill')
ap.add_argument('--repo-dir', default='.'); ap.add_argument('--max-runs', type=int, default=12)
a = ap.parse_args()
RD = os.path.abspath(a.repo_dir); WORK = os.path.abspath(a.work); os.makedirs(WORK, exist_ok=True)
REPO = os.environ.get('GITHUB_REPOSITORY', 'alanfuller15/order24-compute')
CFG = json.load(open(f'{RD}/ops/config.json'))
CAP = int(CFG.get('cap', 40)); DRY = a.dry or not CFG.get('live', False)
SELF_RUN = os.environ.get('GITHUB_RUN_ID', '')
T0 = time.time(); NOW = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
P = {'time': NOW, 'dry': DRY, 'result': 'ok', 'events': [], 'tags': {}, 'jobs': None, 'needs': [], 'api_remaining': None, 'plan': []}
SUMMARY = os.environ.get('GITHUB_STEP_SUMMARY')

def log(s): print(s, flush=True)
def event(s): P['events'].append(f'{time.strftime("%m-%d %H:%MZ", time.gmtime())} {s}'); log('EVENT ' + s)
def summary(s):
    if SUMMARY:
        with open(SUMMARY, 'a') as f: f.write(s + '\n')
def save_pass():
    P['seconds'] = round(time.time() - T0, 1); json.dump(P, open(f'{WORK}/pass.json', 'w'), indent=1)
def done(code, result=None):
    if result: P['result'] = result
    try:   # review M6: measure this token's budget per pass (rate_limit itself is free): limit, left, used by this pass
        rl = json.loads(subprocess.run(['gh', 'api', 'rate_limit'], capture_output=True, timeout=30).stdout)['resources']['core']
        P['api_limit'] = rl['limit']; P['api_left_end'] = rl['remaining']
        if P.get('api_remaining') is not None: P['api_used'] = P['api_remaining'] - rl['remaining']
        summary(f'\nAPI (this token): limit {rl["limit"]}/h, {rl["remaining"]} left, this pass used ~{P.get("api_used", "?")}'
                + ' (other workflows of the repo, e.g. produce Restore steps, share it)')
    except Exception: pass
    save_pass(); sys.exit(code)

def gh(path, method='GET', body=None, raw_out=None):
    cmd = ['gh', 'api', '-X', method, path]
    if body is not None: cmd += ['--input', '-']
    for tries in range(3):
        r = subprocess.run(cmd, input=body.encode() if body is not None else None,
                           stdout=raw_out if raw_out else subprocess.PIPE, stderr=subprocess.PIPE)
        if r.returncode == 0: return None if raw_out or method == 'POST' else json.loads(r.stdout or b'null')
        err = r.stderr.decode()[:300]
        if method == 'POST' or tries == 2 or '404' in err or '403' in err: raise RuntimeError(f'gh api {method} {path}: {err}')
        time.sleep(5 * (tries + 1))
def git(*args, check=True): return subprocess.run(['git', *args], cwd=RD, check=check, capture_output=True, text=True).stdout
def lines(p): return [l.strip() for l in open(p)] if os.path.exists(p) else []

# ---- 1. kill switch
if os.path.exists(f'{RD}/control/HOLD'):
    event('control/HOLD present: refill did nothing'); P['result'] = 'HOLD'; done(0)

# ---- rate limit (the rate_limit endpoint itself is free)
try:
    rl = gh('rate_limit')['resources']['core']; P['api_remaining'] = rl['remaining']; P['api_limit'] = rl['limit']
    if rl['remaining'] < int(CFG.get('min_api_remaining', 150)):
        event(f'API budget low ({rl["remaining"]} left until {time.strftime("%H:%MZ", time.gmtime(rl["reset"]))}): refill skipped'); done(0, 'skipped: API budget')
except RuntimeError as e: log(f'rate_limit: {e}')

# ---- 2. runs, slots
def all_runs(path, stop_before):
    out = []
    for page in range(1, 11):
        d = gh(f'{path}{"&" if "?" in path else "?"}per_page=100&page={page}')['workflow_runs']; out += d
        if len(d) < 100 or d[-1]['created_at'] < stop_before: break
    return out
def count_jobs():
    """jobs not completed in all non-completed runs of the repo (this refill workflow's own runs excluded): (busy, unknown_runs)"""
    busy = 0; unknown = []; per = {}
    active = {}
    for st in ('in_progress', 'queued'):   # review M6: only these two listings (not the last 100 runs of every status)
        for r in gh(f'repos/{REPO}/actions/runs?status={st}&per_page=100')['workflow_runs']: active[r['id']] = r
    for r in active.values():
        if r['status'] == 'completed' or r.get('path', '').endswith('/refill.yml') or str(r['id']) == SELF_RUN: continue
        n = 0; page = 1; listed = 0
        while True:
            d = gh(f'repos/{REPO}/actions/runs/{r["id"]}/jobs?per_page=100&page={page}')
            n += sum(1 for j in d['jobs'] if j['status'] != 'completed'); listed += len(d['jobs'])
            if len(d['jobs']) < 100: break
            page += 1
        if listed == 0: unknown.append(r['id'])
        busy += n; per[r['id']] = (r['name'], n)
    return busy, unknown, per
cutoff = CFG['cutoff']
runs = [r for r in all_runs(f'repos/{REPO}/actions/workflows/produce.yml/runs', cutoff) if r['created_at'] > cutoff]
scanned = set(lines(f'{RD}/ops/scanned_runs.txt')); handled = set(lines(f'{RD}/ops/handled_runs.txt'))
new = sorted((r for r in runs if r['status'] == 'completed' and str(r['id']) not in scanned and str(r['id']) not in handled), key=lambda r: r['id'])
busy, unknown, per = count_jobs()
for _ in range(2):
    if not unknown: break
    time.sleep(10); busy, unknown, per = count_jobs()
P['jobs'] = {'busy': busy, 'cap': CAP, 'runs': {str(k): v for k, v in per.items()}}
log(f'{len(runs)} produce runs since {cutoff}; {len(new)} completed and not scanned; jobs busy {busy}/{CAP}' + (f'; runs without jobs yet: {unknown}' if unknown else ''))

recorded = set(l.split()[0] for l in lines(f'{RD}/ops/recorded.txt') if l)
nr_path = f'{RD}/ops/new_records.txt'; listed_new = {l.split('\t')[0] for l in lines(nr_path) if l and not l.startswith('#')}

# ---- 3. small data of a run
class Ranged(io.RawIOBase):
    """seekable reader of an artifact zip through HTTP Range requests on its signed blob URL (fetch_layer.py's method)"""
    def __init__(s, aid):
        import urllib.request; s.aid = aid; s.url = s._blob(); s.pos = 0
        s.size = int(urllib.request.urlopen(urllib.request.Request(s.url, method='HEAD'), timeout=60).headers['Content-Length'])
    def _blob(s):
        import urllib.request, urllib.error
        class NR(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *x, **k): return None
        tok = os.environ.get('GH_TOKEN', '')
        try: urllib.request.build_opener(NR).open(urllib.request.Request(f'https://api.github.com/repos/{REPO}/actions/artifacts/{s.aid}/zip', headers={'Authorization': f'Bearer {tok}'}), timeout=60)
        except urllib.error.HTTPError as e:
            if e.headers.get('Location'): return e.headers['Location']
            raise
        raise RuntimeError('artifact zip: no redirect')
    def seekable(s): return True
    def readable(s): return True
    def tell(s): return s.pos
    def seek(s, o, w=0): s.pos = o if w == 0 else (s.pos + o if w == 1 else s.size + o); return s.pos
    def readinto(s, b):
        import urllib.request
        n = min(len(b), s.size - s.pos)
        if n <= 0: return 0
        for tries in range(4):
            try: d = urllib.request.urlopen(urllib.request.Request(s.url, headers={'Range': f'bytes={s.pos}-{s.pos + n - 1}'}), timeout=120).read(); break
            except Exception:
                if tries == 3: raise
                s.url = s._blob()
        b[:len(d)] = d; s.pos += len(d); return len(d)
SMALL = re.compile(r'^(results\.jsonl|chunk\.txt|ccc\.log|cube/[^/]+\.log|cube/[^/]+/(log\.jsonl|tree\.json|ORIGINAL_MODEL_FOUND\.json))$')
def safe_extract(zf, names, dst):
    for n in names:
        if n.startswith('/') or '..' in n.split('/'): continue
        p = os.path.join(dst, n); os.makedirs(os.path.dirname(p), exist_ok=True)
        with zf.open(n) as fi, open(p, 'wb') as fo: shutil.copyfileobj(fi, fo)
def fetch_small(run, arts):
    """-> (G, artifact names, how many read from meta / by range, artifacts whose small data could not be read)"""
    G = f'{WORK}/gha/{run}'; shutil.rmtree(G, ignore_errors=True); os.makedirs(G)
    names = [x['name'] for x in arts if not x['name'].endswith('-meta')]
    nm = nr = 0
    for x in arts:
        if not x['name'].endswith('-meta') or x.get('expired'): continue
        zp = f'{WORK}/meta.zip'
        try:
            with open(zp, 'wb') as fo: gh(f'repos/{REPO}/actions/artifacts/{x["id"]}/zip', raw_out=fo)
            with zipfile.ZipFile(zp) as zf:   # meta zip: <wave>-<shard chunk>/<small files>, one folder per shard of the job
                safe_extract(zf, [n for n in zf.namelist() if '/' in n and SMALL.match(n.split('/', 1)[1])], G)
            nm += 1
        except Exception as e: log(f'run {run}: {x["name"]}: meta read failed ({e}): ranged read of its shards instead')
        if os.path.exists(zp): os.remove(zp)
    for x in arts:
        n = x['name']
        if n.endswith('-meta') or x.get('expired') or not re.match(r'm\d\d', n) or os.path.exists(f'{G}/{n}/chunk.txt'): continue
        try:
            zf = zipfile.ZipFile(io.BufferedReader(Ranged(x['id']), buffer_size=4 << 20))
            safe_extract(zf, [i.filename for i in zf.infolist() if SMALL.match(i.filename)], f'{G}/{n}'); nr += 1
        except Exception as e: log(f'run {run}: {n}: ranged read failed: {e}')
    bad = [x['name'] for x in arts if not x['name'].endswith('-meta') and not x.get('expired') and re.match(r'm\d\d', x['name']) and not os.path.exists(f'{G}/{x["name"]}/chunk.txt')]
    return G, names, nm, nr, bad
def scan(G):
    """-> (omf list, finished records [(tag, artifact)])"""
    omf = []; fin = []
    for p in glob.glob(f'{G}/*/cube/*/ORIGINAL_MODEL_FOUND.json'): omf.append(p[len(G) + 1:])
    for p in glob.glob(f'{G}/*/cube/*/log.jsonl') + glob.glob(f'{G}/*/cube/*.log') + glob.glob(f'{G}/*/ccc.log'):
        if 'ORIGINAL_MODEL_FOUND' in open(p, errors='replace').read(): omf.append(p[len(G) + 1:])
    for p in glob.glob(f'{G}/*/results.jsonl'):
        art = p[len(G) + 1:].split('/')[0]
        for l in open(p, errors='replace'):
            if not l.strip(): continue
            if 'ORIGINAL_MODEL_FOUND' in l: omf.append(f'{art}/results.jsonl'); continue
            try: r = json.loads(l)
            except ValueError: continue
            if r.get('status') == 'UNSAT' and r.get('tag'): fin.append((r['tag'], art))
    return sorted(set(omf)), fin

# ---- git helpers (live only)
def commit_push(paths, msg):
    git('add', '--', *paths)
    if subprocess.run(['git', 'diff', '--cached', '--quiet'], cwd=RD).returncode == 0: log('nothing to commit'); return
    git('-c', 'user.name=github-actions[bot]', '-c', 'user.email=41898282+github-actions[bot]@users.noreply.github.com', 'commit', '-q', '-m',
        msg + '\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\nClaude-Session: https://claude.ai/code/session_01MTjZowtCtrDAyKuAmKSoH2')
    for tries in range(4):
        if subprocess.run(['git', 'push', '-q', 'origin', 'HEAD:main'], cwd=RD, capture_output=True).returncode == 0: break
        r = subprocess.run(['git', 'pull', '-q', '--rebase', 'origin', 'main'], cwd=RD, capture_output=True)
        if r.returncode != 0:   # conflict: HEAD would sit at origin/main and a later push would be "up to date" (review H1)
            subprocess.run(['git', 'rebase', '--abort'], cwd=RD, capture_output=True)
            raise RuntimeError('rebase onto main failed (conflict): nothing dispatched')
        if os.path.exists(f'{RD}/control/HOLD'): raise RuntimeError('control/HOLD appeared on main: nothing dispatched')
        time.sleep(3 * (tries + 1))
    else: raise RuntimeError('push to main failed 4 times')
    git('fetch', '-q', 'origin', 'main')   # the ledger commit must be ON main (HEAD == origin/main, or a later writer on top of it)
    if subprocess.run(['git', 'merge-base', '--is-ancestor', 'HEAD', 'origin/main'], cwd=RD).returncode != 0: raise RuntimeError('ledger commit not on main after the push: nothing dispatched')
    if subprocess.run(['git', 'status', '--porcelain', '--untracked-files=no'], cwd=RD, capture_output=True, text=True).stdout.strip().startswith(('UU', 'AA')): raise RuntimeError('unmerged files: nothing dispatched')
def stop(M, what, run):
    txt = (f'ORIGINAL_MODEL_FOUND in layer {M} (run {run}): {what}\nrefill stopped and control/HOLD created at {NOW}.\n'
           'A model is examined by the manager, never resumed past. Remove control/HOLD only after that.\n')
    P['result'] = f'STOP: ORIGINAL_MODEL_FOUND L{M} run {run}'; P['needs'].append(P['result']); event(P['result'])
    summary('## STOP\n```\n' + txt + '```')
    if not DRY:
        os.makedirs(f'{RD}/control', exist_ok=True)
        open(f'{RD}/ops/ALERT', 'a').write(txt); open(f'{RD}/control/HOLD', 'w').write(txt)
        commit_push(['ops/ALERT', 'control/HOLD'], f'control/HOLD: ORIGINAL_MODEL_FOUND in layer {M} (run {run}); refill stopped')
    done(3)

# ---- 4-7. per run
summary(f'## refill {NOW} ({"DRY RUN: no commit, no dispatch" if DRY else "live"})\n\njobs busy {busy}/{CAP}; {len(new)} new completed produce runs\n')
errors = 0; free_known = not unknown
for r in new[:a.max_runs]:
    run = str(r['id']); arts = []; page = 1
    while True:
        d = gh(f'repos/{REPO}/actions/runs/{run}/artifacts?per_page=100&page={page}'); arts += d['artifacts']
        if len(d['artifacts']) < 100: break
        page += 1
    if time.time() - T0 > 60 * float(CFG.get('max_pass_minutes', 12)):   # review L3: leave time to dispatch before timeout-minutes
        event(f'pass time limit reached: {run} and later runs wait for the next pass'); break
    G, names, nm, nrg, bad = fetch_small(run, arts)
    if bad:   # review M4: never mark a run whose data was not read: the next pass retries it
        event(f'run {run}: small data of {len(bad)} artifact(s) unreadable ({", ".join(bad[:3])}): not marked, retried next pass')
        P['needs'].append(f'run {run}: {len(bad)} artifact(s) unreadable by the refill (retried every pass; check the run)'); continue
    first = names[0] if names else ''
    lm = re.match(r'm(\d\d)', first); M = int(lm.group(1)) if lm else 0
    log(f'run {run} ({r["conclusion"]}): {len(names)} artifacts, first {first or "-"}; small data from {nm} meta + {nrg} ranged')
    omf, fin = scan(G)
    if omf: stop(M, '; '.join(omf[:5]), run)
    added = []
    for tag, art in fin:
        if tag in recorded or tag in listed_new: continue
        lm2 = re.match(r'L(\d+)_', tag)
        added.append(f'{tag}\tL{lm2.group(1) if lm2 else "?"}\t{run}\t{art}\t{NOW}'); listed_new.add(tag)
    for l in added: event(f'FINISHED (to fetch, audit, record): {l.split(chr(9))[0]} run {run} artifact {l.split(chr(9))[3]}')
    paths = ['ops/scanned_runs.txt']; dispatches = []; plan_note = ''
    if r['conclusion'] == 'success' and run not in handled:
        if re.search(r's\d.*m-', first): plan_note = 'merge wave, no continuation'
        elif re.match(r'm\d\d[c-f]', first):
            if not free_known:
                log(f'run {run}: job count unknown (a new run lists no jobs yet): continued next pass')
                P['needs'].append(f'run {run}: not continued this pass: job count unknown (runs without jobs: {unknown})'); continue
            free = max(0, CAP - busy)
            open(f'{WORK}/arts_{run}.txt', 'w').write('\n'.join(names) + '\n')
            recf = f'{WORK}/recorded_{run}.txt'
            open(recf, 'w').write('\n'.join(sorted(recorded | listed_new | {t for t, _ in fin})) + '\n')
            base = ['python3', '-I', f'{RD}/ops/pool.py', run, str(free), '--arts', f'{WORK}/arts_{run}.txt', '--gdir', G, '--recorded', recf,
                    '--primary', f'{RD}/ops/primary.json', '--cost', f'{RD}/ops/cost_model.json', '--votes', f'{RD}/data/pred_votes.json', '--repo', RD]
            env = dict(os.environ, POOL_JMAX=str(CFG.get('jmax', 6)), POOL_WINDOW=str(CFG.get('window', 9000)))
            pp = subprocess.run(base + ['--nowrite', '--plan', f'{WORK}/plan_{run}.json'], capture_output=True, text=True, env=env)
            pl = json.load(open(f'{WORK}/plan_{run}.json')) if os.path.exists(f'{WORK}/plan_{run}.json') else {}
            if pp.returncode == 2 or pl.get('stop'): stop(pl.get('stop_layer', M), pl.get('stop') or pp.stderr[-300:], run)
            if pp.returncode != 0: event(f'pool.py failed on run {run}: {pp.stderr.strip()[-200:]}'); P['needs'].append(f'pool.py failed on run {run}'); errors += 1; continue
            need = sum(x['jobs'] for x in pl['dispatches'])
            if busy + need > CAP:
                event(f'run {run}: plan needs {need} jobs, {CAP - busy} free: waits for the next pass')
                P['needs'].append(f'run {run}: waits: plan needs {need} jobs, {CAP - busy} free' + (' (more than the cap: it can never fit; continue it by hand)' if need > CAP else '')); continue
            pp = subprocess.run(base + ['--plan', f'{WORK}/plan_{run}.json'], capture_output=True, text=True, env=env)
            pl = json.load(open(f'{WORK}/plan_{run}.json'))
            if pp.returncode != 0 or pl.get('stop'): event(f'pool.py second pass failed on run {run}'); errors += 1; continue
            for ln in pl['lines']:
                m = re.match(r'(\S+)-(h\S+): (L\S+) (\d+) open cubes, cost-to-go (\S+) core-h -> (\d+) shards in (\d+) job', ln)
                if m: P['tags'][m.group(3)] = {'open': int(m.group(4)), 'cost_h': m.group(5), 'wave': m.group(1), 'shards': int(m.group(6)), 'jobs': int(m.group(7)), 'run': run, 'time': NOW}
            dispatches = pl['dispatches']
            for c in pl['commits']: paths += c['paths']
            if not dispatches and not any(('nothing left' in l or 'dropped' in l) for l in pl['lines']):
                P['needs'].append(f'run {run} ({first}): pool did nothing - continue it by hand (shard_ccc.py next / chain_ccc.py)')
            plan_note = '; '.join(pl['lines'])[:600]
            P['plan'].append({'run': run, 'free': free, 'lines': pl['lines'], 'commits': pl['commits'], 'dispatches': [x['body'] for x in dispatches]})
            paths.append('ops/handled_runs.txt')
        else: plan_note = 'not a ccc run'
    summary(f'### run {run} ({r["conclusion"]}, first artifact `{first}`)\n```\n{plan_note or "scanned only"}\n' + ''.join(f'DRY dispatch {x["body"]}\n' for x in dispatches if DRY) + '```')
    if DRY:
        for x in dispatches: log('DRY dispatch ' + x['body']); event(f'DRY: would dispatch {x["wave"]} ({x["jobs"]} jobs) from run {run}')
        busy += sum(x['jobs'] for x in dispatches); scanned.add(run); handled.add(run); continue
    # live: ledger first, then dispatch
    with open(f'{RD}/ops/scanned_runs.txt', 'a') as fo: fo.write(run + '\n')
    if 'ops/handled_runs.txt' in paths:
        with open(f'{RD}/ops/handled_runs.txt', 'a') as fo: fo.write(run + '\n')
    if added:
        with open(nr_path, 'a') as fo: fo.write(''.join(l + '\n' for l in added))
        paths.append('ops/new_records.txt')
    waves = ', '.join(x['wave'] for x in dispatches)
    try: commit_push(sorted(set(paths)), f'refill: run {run}' + (f': chunks {waves} (pool)' if waves else ': scanned') + (f'; {len(added)} finished formula(s) for the manager' if added else ''))
    except Exception as e:
        event(f'commit/push failed for run {run}: {e}: nothing dispatched'); errors += 1
        P['needs'].append(f'run {run}: ledger push failed ({e}); nothing dispatched; the next pass retries it'); break
    for x in dispatches:
        try:
            gh(f'repos/{REPO}/actions/workflows/produce.yml/dispatches', method='POST', body=x['body'])
            busy += x['jobs']; event(f'dispatched {x["wave"]} ({x["jobs"]} jobs) from run {run}')
        except Exception as e:
            event(f'DISPATCH FAILED {x["wave"]} from run {run}: {e}'); P['needs'].append(f'dispatch of {x["wave"]} (run {run}) failed: dispatch it by hand: {x["body"]}'); errors += 1
if len(new) > a.max_runs: event(f'{len(new) - a.max_runs} more runs left for the next pass')
P['jobs']['busy_after'] = busy
done(1 if errors else 0, 'errors' if errors else None)
