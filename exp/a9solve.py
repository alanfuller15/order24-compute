"""a9solve.py -- CEGAR for one cube (case, profile, cube literals): base formula + lazy floors / 10-set clauses.
Returns status UNSAT / MODEL / TIMEOUT and the lazy list (which, with (case, profile, cube), determines the final CNF)."""
import os, sys, time, itertools as it
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import a9core as C
from pysat.solvers import Cadical153

_M = None; _B = None
MODE = os.environ.get('A9MODE', 'K')    # selection of lazy floors (heuristic; does not affect soundness)
def masks():
    global _M, _B
    if _M is None:
        for p in (os.path.join(HERE, 'masks12.npy'), os.path.join(HERE, '..', 'data', 'masks12.npy'),
                  os.path.join(HERE, '..', '..', '..', 'masks12.npy')):
            if os.path.exists(p): _M = np.load(p).astype(np.uint32); break
        else:
            _M = np.fromiter((sum(1 << v for v in c) for c in it.combinations(range(24), 12)), dtype=np.uint32, count=2704156)
        assert len(_M) == 2704156
        _B = [((_M >> np.uint32(b)) & np.uint32(1)).astype(np.uint8) for b in range(24)]
        global _NK
        _NK = sum(_B[b] for b in range(9))            # |S cap I|
    return _M, _B

def ind10(E):
    """all independent 10-sets (as sorted lists), up to 200."""
    adj = [0] * 24
    for u, v in E: adj[u] |= 1 << v; adj[v] |= 1 << u
    out = []
    def rec(cur, cand, start):
        if len(out) >= 200: return
        if len(cur) == 10: out.append(list(cur)); return
        c = cand >> start << start
        if len(cur) + bin(c).count('1') < 10: return
        v = start
        while c >> v:
            if c >> v & 1: rec(cur + [v], cand & ~adj[v], v + 1)
            v += 1
    rec([], (1 << 24) - 1, 0)
    return out

def violated(E, batch):
    M, B = masks()
    cnt = np.zeros(len(M), dtype=np.uint8)
    for u, v in E: cnt += B[u] & B[v]
    bad = np.nonzero(cnt < 12)[0]
    nb = len(bad)
    if nb > batch:
        if MODE == 'K':      # prefer sets with many I-vertices (short, strong encodings); among those the most violated
            key = cnt[bad].astype(np.int32) - 16 * _NK[bad].astype(np.int32)
            bad = bad[np.argsort(key, kind='stable')[:batch]]
        elif MODE == 'V':    # the most violated first
            bad = bad[np.argsort(cnt[bad].astype(np.int32) * 16 - _NK[bad], kind='stable')[:batch]]
        else:                # 'M': half and half
            k1 = np.argsort(cnt[bad].astype(np.int32) - 16 * _NK[bad].astype(np.int32), kind='stable')[:batch // 2]
            k2 = np.argsort(cnt[bad].astype(np.int32) * 16 - _NK[bad], kind='stable')[:batch]
            sel = list(k1); s1 = set(k1.tolist())
            for j in k2:
                if len(sel) >= batch: break
                if int(j) not in s1: sel.append(j)
            bad = bad[np.array(sel)]
    out = []
    for j in bad:
        m = int(M[j]); out.append([b for b in range(24) if m >> b & 1])
    return nb, int(cnt.min()), out

def run(case, prof, cube=(), budget=600, batch=300, log=None, lazy0=()):
    t0 = time.time(); f = C.build(case, prof, cube); NE = C.forced_nonedges(prof)
    S = Cadical153(bootstrap_with=f.cl); done = len(f.cl); lazy = []
    def push(item):
        C.add_lazy(f, prof, item, NE); lazy.append(item)
    for item in lazy0: push(item)
    itn = 0; st = None
    while True:
        for c in f.cl[done:]: S.add_clause(c)
        done = len(f.cl); itn += 1
        if time.time() - t0 > budget: st = 'TIMEOUT'; break
        ts = time.time(); r = S.solve(); ts = time.time() - ts
        if not r: st = 'UNSAT'; break
        mod = set(l for l in S.get_model()[:C.NEDGEVARS] if l > 0); E = C.edges_of_model(mod)
        tens = ind10(E); nb, mn, viol = violated(E, batch)
        if not tens and nb == 0: st = 'MODEL'; break
        for s in tens[:50]: push(['I', s])
        for s in viol: push(['F', s])
        if log: log(f'  it {itn}: solve {ts:.1f}s, {len(E)} edges, min {mn}, {nb} violated, {len(tens)} ind10, lazy {len(lazy)}, clauses {len(f.cl)}, t={time.time()-t0:.0f}')
    S.delete()
    return {'status': st, 'iters': itn, 'seconds': round(time.time() - t0, 1), 'lazy': lazy, 'nv': f.nv, 'ncl': len(f.cl),
            'edges': E if st == 'MODEL' else None}, f

if __name__ == '__main__':
    case = sys.argv[1]; idx = int(sys.argv[2]); budget = float(sys.argv[3]); batch = int(sys.argv[4]) if len(sys.argv) > 4 else 300
    P = C.profiles(case); prof = P[idx]; print(case, idx, prof, flush=True)
    r, f = run(case, prof, (), budget, batch, log=lambda s: print(s, flush=True))
    print(r['status'], r['iters'], r['seconds'], len(r['lazy']), r['ncl'], r['edges'])
