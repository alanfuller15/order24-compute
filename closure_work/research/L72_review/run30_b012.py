"""Run the remaining m=30 degree sequences with at most two degree-5 vertices (the hand proof's b in {0,1,2} cases)."""
import json, sys, time
sys.argv = ['x']
src = open('cpsat_degsplit.py').read().split('for m in map(int')[0]
exec(src)
done = {tuple(json.loads(l)['seq']) for l in open('degsplit_30_partial.jsonl')}
S = [q for q in seqs(n, 60, 6) if q[0] + q[1] - 1 <= 9 and q not in done and q.count(5) <= 2]
for q in S:
    t0 = time.time(); st = solve(30, q, 300)
    print(json.dumps({'m': 30, 'seq': q, 'status': st, 'secs': round(time.time() - t0, 2)}), flush=True)
