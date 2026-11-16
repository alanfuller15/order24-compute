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
tags = [t for t in F if key(t, M)[0] >= 9]
def est(t):
    k = key(t, M)
    if k in pred: return pred[k], 1
    return (statistics.median(prof[k[:4]]) if k[:4] in prof else 60.0), 0
E = {t: est(t) for t in tags}
total = sum(v for v, _ in E.values()); J = max(math.ceil(total / CAP), math.ceil(len(tags) / 48))
heap = [(0.0, j) for j in range(J)]; jobs = [[] for _ in range(J)]
for t in sorted(tags, key=lambda t: (-E[t][0], t)):
    load, j = heapq.heappop(heap); jobs[j].append(t); heapq.heappush(heap, (load + E[t][0], j))
out = f'{R}/chunks/m{M}p'
for f in glob.glob(f'{out}/q*.txt'): os.remove(f)
os.makedirs(out, exist_ok=True)
for j, js in enumerate(sorted(jobs, key=lambda js: -sum(E[t][0] for t in js))):
    open(f'{out}/q{j + 1:03d}.txt', 'w').write('\n'.join(js) + '\n')
loads = sorted((sum(E[t][0] for t in js) for js in jobs), reverse=True)
print(f'm{M}p: {len(tags)} formulas ({sum(k for _, k in E.values())} predicted from a higher layer), predicted '
      f'{total / 3600:.1f} core-h, {J} jobs; predicted load per job {loads[0] / 3600:.2f}..{loads[-1] / 3600:.2f} core-h, '
      f'longest formula {max(v for v, _ in E.values()) / 60:.0f} min')
