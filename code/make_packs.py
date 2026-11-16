"""make_packs.py M [JOB_CORE_HOURS] : write chunks/m<M>p/qNNN.txt in the compute repo: the s >= 9 formulas of layer M packed
into GitHub Actions jobs by predicted time, longest first. Production scheduling only; plays no part in any proof.

Why: with 4 tags per job, a job lasts as long as its slowest formula and the other 3 cores idle (measured: 40% use of the
4 cores on layer-88 jobs). grun90 starts formulas in the chunk's order on 4 workers as they free up, so a job holding many
formulas sorted longest first keeps its 4 cores busy.

Prediction: a formula's time (search + resumed + proof seconds) is taken from the nearest higher layer that recorded the
same key (s, a, b, m - c, h_index) (log-correlation 0.85-0.96 between consecutive layers); unknown keys get the median of
their profile key, else 60 s. Packing: LPT over jobs (largest predicted first, to the least-loaded job), number of jobs =
ceil(total / JOB_CORE_HOURS) (default 3 core-hours, about 45 min on 4 cores), at least enough that no job holds more than
48 formulas; each job's list is written longest first."""
import sys, os, json, re, glob, math, heapq, statistics
SP = '/tmp/claude-0/-home-claude/4a72079e-a9db-5726-b10c-aeb759ad214f/scratchpad'
R = f'{SP}/gh/order24-compute'
M = int(sys.argv[1]); CAP = float(sys.argv[2]) * 3600 if len(sys.argv) > 2 else 3 * 3600
def ldir(m): return f'{SP}/l{m}' if os.path.isdir(f'{SP}/l{m}') else f'{SP}/layers/l{m}'
F = json.load(open(f'{ldir(M)}/formulas{M}_c{M - 23}.json'))
def key(t, m):
    s, a, b, c, h = map(int, re.match(r'L\d+_s(\d+)a(\d+)b(\d+)c(\d+)_(\d+)$', t).groups()); return (s, a, b, m - c, h)
pred = {}
for m in range(M + 1, 92):          # nearest higher layer first
    p = f'{ldir(m)}/run_gha/results.jsonl'
    if not os.path.exists(p): continue
    for l in open(p):
        if not l.strip(): continue
        r = json.loads(l); k = key(r['tag'], m)
        if k not in pred: pred[k] = r.get('seconds', 0) + r.get('resumed_seconds', 0) + r.get('proof_seconds', 0)
prof = {}
for k, v in pred.items(): prof.setdefault(k[:4], []).append(v)
tags = [t for t in F if key(t, M)[0] >= (int(os.environ.get('MIN_S', '9')))]
if os.environ.get('UNRECORDED'):   # only formulas with no record yet in l<M>/run_gha (a re-pack of a layer in progress)
    rp = f'{ldir(M)}/run_gha/results.jsonl'
    done = {json.loads(l)['tag'] for l in open(rp) if l.strip()} if os.path.exists(rp) else set()
    tags = [t for t in tags if t not in done]
def est(t):
    k = key(t, M)
    if k in pred: return pred[k], 1
    return (statistics.median(prof[k[:4]]) if k[:4] in prof else 60.0), 0
E = {t: est(t) for t in tags}
# HARD profiles (env HARD, default '10,4,18'): their formulas grow ~2-3x harder per layer down and run for hours, so a
# job holding one of them keeps 3 of its 4 cores idle once its other formulas are done. They get jobs of their own,
# 4 per job (one per core), named h01, h02, ...; the rest are packed as before.
HARD = {tuple(map(int, x.split(','))) for x in os.environ.get('HARD', '10,4,18').split(';') if x}
hard = sorted([t for t in tags if key(t, M)[:3] in HARD], key=lambda t: (-E[t][0], t)); tags = [t for t in tags if t not in set(hard)]
total = sum(E[t][0] for t in tags); J = max(1, math.ceil(total / CAP), math.ceil(len(tags) / 48)) if tags else 0
heap = [(0.0, j) for j in range(J)]; jobs = [[] for _ in range(J)]
for t in sorted(tags, key=lambda t: (-E[t][0], t)):
    load, j = heapq.heappop(heap); jobs[j].append(t); heapq.heappush(heap, (load + E[t][0], j))
WAVE = os.environ.get('WAVE', f'm{M}p'); out = f'{R}/chunks/{WAVE}'
for f in glob.glob(f'{out}/q*.txt'): os.remove(f)
os.makedirs(out, exist_ok=True)
for f in glob.glob(f'{out}/h*.txt'): os.remove(f)
for j, js in enumerate(sorted(jobs, key=lambda js: -sum(E[t][0] for t in js))):
    open(f'{out}/q{j + 1:03d}.txt', 'w').write('\n'.join(js) + '\n')
for i in range(0, len(hard), 4):
    open(f'{out}/h{i // 4 + 1:02d}.txt', 'w').write('\n'.join(hard[i:i + 4]) + '\n')
tags = tags + hard   # for the seeds below
# Seeds (worker.sh reads ckpt/<wave>.jsonl.xz, the lines of its chunk's tags, into lazy_partial.jsonl; grun90 starts the
# search with these items already in the CNF):
#  (1) resume: lazy items saved by stopped or killed searches of these formulas at this layer (run_gha/ckpt_*.jsonl);
#  (2) carried (SEED_ABOVE, default on): the final lazy list of the same key (s, a, b, m - c, h_index) at the nearest higher
#      layer. Lazy items are 9-sets that must contain an edge and 12-sets with at least 12 edges: true for every graph of
#      the class at any edge count, on the same 24 labelled vertices, and the checker rebuilds every item into the CNF, so
#      where an item came from plays no part in what is proved. Carrying them skips most CEGAR iterations.
# One line per formula: resume items in order, then carried items not already present (grun90 refuses repeated items).
sel = set(tags); res = {}
for f in sorted(glob.glob(f'{ldir(M)}/run_gha/ckpt_*.jsonl'), key=os.path.getmtime):
    for l in open(f):
        try: d = json.loads(l)
        except ValueError: continue
        if d.get('tag') in sel and isinstance(d.get('items'), list): res.setdefault(d['tag'], []).extend(d['items'])
above = {}
if os.environ.get('SEED_ABOVE', '1') == '1':
    for m in range(M + 1, 92):
        p = f'{ldir(m)}/run_gha/results.jsonl'
        if not os.path.exists(p): continue
        for l in open(p):
            if not l.strip(): continue
            r = json.loads(l); k = key(r['tag'], m)
            if k not in above and isinstance(r.get('lazy'), list) and r['lazy']: above[k] = (m, r['lazy'])
seeds = []; n_res = n_abv = 0
for t in tags:
    items = []; seen = set()
    for it in res.get(t, []) + (above[key(t, M)][1] if key(t, M) in above else []):
        k2 = (it['kind'], tuple(it['W']))
        if k2 not in seen: seen.add(k2); items.append({'kind': it['kind'], 'W': it['W']})
    if not items: continue
    n_res += t in res; n_abv += key(t, M) in above
    seeds.append(json.dumps({'tag': t, 'items': items, 'how': 'seed: ' + '+'.join(
        x for x, y in (('resume', t in res), (f'L{above[key(t, M)][0]} lazy' if key(t, M) in above else '', key(t, M) in above)) if y)}))
import lzma
for old in (f'{R}/ckpt/{WAVE}.jsonl', f'{R}/ckpt/{WAVE}.jsonl.xz'):
    if os.path.exists(old): os.remove(old)
if seeds:
    with lzma.open(f'{R}/ckpt/{WAVE}.jsonl.xz', 'wt') as fo: fo.write('\n'.join(seeds) + '\n')
loads = sorted((sum(E[t][0] for t in js) for js in jobs), reverse=True) or [0]
print(f'{WAVE}: {len(tags)} formulas ({sum(k for _, k in E.values())} predicted from a higher layer), predicted '
      f'{total / 3600:.1f} core-h, {J} jobs + {(len(hard) + 3) // 4} hard jobs ({len(hard)} formulas); predicted load per job {loads[0] / 3600:.2f}..{loads[-1] / 3600:.2f} core-h, '
      f'longest formula {max(v for v, _ in E.values()) / 60:.0f} min; seeds for {len(seeds)} formulas ({n_res} resume, {n_abv} carried from above)')
