"""ops/status.py: writes STATUS.md + status.json (the one-commit 'status' branch; refill.yml pushes it every pass).
The repo is PUBLIC: only production facts (counts, tags, run ids, ages). No names, accounts, e-mail, tokens, chat links.
Inputs: --pass $WORK/pass.json (this refill pass; may be missing), --prev previous status.json (events and per-formula state
carry over), the checkout (ops/recorded.txt, ops/new_records.txt, ops/primary.json, ops/needs_user.txt, control/HOLD,
ops/ALERT, data/formulas<M>_c<M-23>.json) and the lane heartbeat refs refs/remotes/origin/lane-status-* (fetched by refill.yml)."""
import os, sys, json, re, time, subprocess, argparse, calendar
ap = argparse.ArgumentParser()
ap.add_argument('--repo-dir', default='.'); ap.add_argument('--pass', dest='pass_', default=''); ap.add_argument('--prev', default='')
ap.add_argument('--out', required=True); ap.add_argument('--layers', default='80-85')
a = ap.parse_args(); RD = os.path.abspath(a.repo_dir); os.makedirs(a.out, exist_ok=True)
now = time.time(); NOW = time.strftime('%Y-%m-%d %H:%MZ', time.gmtime(now))
def rd(p, d=None):
    try: return json.load(open(p))
    except Exception: return d
def lines(p): return [l.rstrip('\n') for l in open(p)] if os.path.exists(p) else []
P = rd(a.pass_, {}) or {}; S = rd(a.prev, {}) or {}
lo, hi = (int(x) for x in a.layers.split('-'))
tags_state = S.get('tags', {}); tags_state.update(P.get('tags', {}))
events = (S.get('events', []) + P.get('events', []))[-50:]
recorded = {l.split()[0] for l in lines(f'{RD}/ops/recorded.txt') if l.strip()}
waiting = {}
for l in lines(f'{RD}/ops/new_records.txt'):
    if l.strip() and not l.startswith('#'): f = l.split('\t'); waiting[f[0]] = f[2] if len(f) > 2 else '?'
primary = rd(f'{RD}/ops/primary.json', {}) or {}

def git(*x): return subprocess.run(['git', *x], cwd=RD, capture_output=True, text=True).stdout.strip()
for st in tags_state.values(): st.pop('lanes', None)              # lane numbers are re-read every pass
lanes = []; lane_flags = []
for ref in git('for-each-ref', '--format=%(refname:short)', 'refs/remotes/origin/lane-status-*').split():
    n = ref.rsplit('-', 1)[1]; ts = git('log', '-1', '--format=%ct', ref)
    age = int((now - int(ts)) / 60) if ts.isdigit() else None
    txt = git('show', f'{ref}:status.txt'); alive = re.search(r'^ALIVE=(\d+)', txt, re.M)
    lanes.append((int(n) if n.isdigit() else 999, n, age, alive.group(1) if alive else '?'))
    for t, c, o, rr in re.findall(r'^(L\d+_\S+) closed=(\d+) open=(\d+) recorded=(\S+)', txt, re.M):
        if c == '0' and o == '0' and rr in ('no', '0'): continue           # solver not started there yet
        st = tags_state.setdefault(t, {}); lb = st.setdefault('lanes', {}); lb[n] = f'{c}/{o}'
        if rr not in ('no', '0'): lane_flags.append(f'lane {n}: {t} recorded={rr} (ingest its result branch)')
    if re.search(r'ORIGINAL_MODEL_FOUND(?!=0|=no)', txt): lane_flags.append(f'lane {n}: ORIGINAL_MODEL_FOUND in its status: examine it')
lanes.sort()

attn = []
if os.path.exists(f'{RD}/control/HOLD'): attn.append('control/HOLD is set: the refill dispatches nothing')
if os.path.exists(f'{RD}/ops/ALERT'): attn.append('ops/ALERT exists: ' + (lines(f'{RD}/ops/ALERT') or [''])[0][:160])
if str(P.get('result', 'ok')).startswith(('STOP', 'errors')): attn.append(f'last refill: {P["result"]}')
stale = [f'{n} ({age} min)' for _, n, age, _ in lanes if age is not None and age > 15]
if stale: attn.append('lane heartbeat stale: ' + ', '.join(stale))
if any('ORIGINAL_MODEL_FOUND' in f for f in lane_flags): attn.append('a lane reports ORIGINAL_MODEL_FOUND')
jb = P.get('jobs') or {}
if jb and jb.get('busy_after', jb.get('busy', 40)) < 30: attn.append(f'GitHub jobs low: {jb.get("busy_after", jb.get("busy"))}/{jb.get("cap", 40)}')
needs_user = [l for l in lines(f'{RD}/ops/needs_user.txt') if l.strip() and not l.startswith('#')]
needs_mgr = list(P.get('needs', [])) + [f'finished, to fetch/audit/record: {t} (run {r})' for t, r in sorted(waiting.items()) if t not in recorded] + lane_flags
if needs_user: attn.append(f'{len(needs_user)} item(s) need the user')

o = []
o.append(f'# Production status\n')
o.append(f'**{"ATTENTION" if attn else "OK"}** - updated {NOW} by refill' + (' (dry run)' if P.get('dry') else '') + '\n')
for x in attn: o.append(f'- {x}')
o.append('\n## Layers (recorded / formulas; unrecorded formulas with their open cubes)\n')
o.append('| layer | recorded | unrecorded: GitHub tree open cubes (cost-to-go core-h, shards) / lanes closed/open |')
o.append('|---|---|---|')
for M in range(hi, lo - 1, -1):
    F = rd(f'{RD}/data/formulas{M}_c{M - 23}.json', {}) or {}
    tags = sorted(F) if isinstance(F, dict) else []
    rec = [t for t in tags if t in recorded]; un = [t for t in tags if t not in recorded]
    cells = []
    for t in un:
        st = tags_state.get(t, {}); short = t.split('_')[-1]
        g = f'{st["open"]} open ({st.get("cost_h", "?")} h, {st.get("shards", "?")} sh, {st.get("wave", "")})' if 'open' in st else ('not in the GitHub pool' if primary.get(t) == [] else 'no GitHub data yet')
        ln = ' lanes ' + ','.join(f'{k}:{v}' for k, v in sorted(st.get('lanes', {}).items())) if st.get('lanes') else ''
        fin = ' **finished, waiting for the manager**' if t in waiting else ''
        cells.append(f'{short}: {g}{ln}{fin}')
    o.append(f'| L{M} | {len(rec)}/{len(tags)} | {"<br>".join(cells) if cells else "all recorded"} |')
o.append('\n## Compute\n')
if jb:
    o.append(f'- GitHub jobs running+queued at the start of the pass: {jb.get("busy")}/{jb.get("cap", 40)} (refill job not counted)'
             + (f'; after its dispatches: {jb["busy_after"]}' + (' (dry run: not dispatched)' if P.get('dry') else '') if jb.get('busy_after', jb.get('busy')) != jb.get('busy') else ''))
o.append(f'- last refill: {P.get("result", "?")} at {P.get("time", "?")}, {P.get("seconds", "?")} s' + (f', API (refill token) {P.get("api_left_end", P["api_remaining"])}/{P.get("api_limit", "?")} left this hour, this pass used ~{P.get("api_used", "?")}' if P.get('api_remaining') is not None else ''))
o.append('- lanes (heartbeat age; ALIVE): ' + ('; '.join(f'lane {n} {age if age is not None else "?"}m ALIVE={al}' for _, n, age, al in lanes) or 'none'))
o.append('\n## Needs the user\n')
o += [f'- {x}' for x in needs_user] or ['- nothing']
o.append('\n## Needs the manager\n')
o += [f'- {x}' for x in needs_mgr[:30]] or ['- nothing']
o.append('\n## Last 10 events\n')
o += [f'- {e}' for e in events[-10:][::-1]] or ['- none']
o.append('\n<sub>Generated by ops/status.py. Production facts only. Records are approved only by an independent audit, never here.</sub>')
open(f'{a.out}/STATUS.md', 'w').write('\n'.join(o) + '\n')
json.dump({'updated': NOW, 'attention': attn, 'needs': needs_user + needs_mgr[:30], 'events': events, 'tags': tags_state, 'last_pass': {k: P.get(k) for k in ('time', 'result', 'dry', 'jobs', 'seconds')}},
          open(f'{a.out}/status.json', 'w'), indent=1)
print(f'{"ATTENTION" if attn else "OK"}: {len(attn)} reason(s); {len(events)} events kept')
