#!/usr/bin/env python3
"""exp/test_sym.py (EXPERIMENT check, research only): for random S x T incidence matrices M (H = H_0000 labelling),
compute the labelling of largest key over Aut(H) x Sym(T) by brute force (key = (d_T(0..s-1), matrix row by row)) and
check (1) it satisfies lex, twins and compswap as properties, (2) the compswap CLAUSES built by symA.add_compswap are
satisfied by it (auxiliary variables set to their intended definitions), and (3) the clauses reject the
property-violating images (encoding is not weaker than stated). Usage: python3 -I -B exp/test_sym.py TAG [TRIALS]"""
import sys, os, json, random, itertools as it
HERE = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(HERE)
sys.path.insert(0, HERE); sys.path.insert(0, os.path.join(R, 'code'))
os.environ.setdefault('ENCODER', 'cegar90c'); os.environ.setdefault('PREDICT', '0')
import cegar90c as C, symA
from networkx.algorithms.isomorphism import GraphMatcher
import networkx as nx
tag = sys.argv[1]; trials = int(sys.argv[2]) if len(sys.argv) > 2 else 500
L = int(tag[1:3]); f = json.load(open(os.path.join(R, 'data', symA.FF[L])))[tag]; s = f['s']; S = range(s); T = list(range(s, 24))
he = sorted(tuple(x) for x in f['h_edges']); g = nx.Graph(); g.add_nodes_from(S); g.add_edges_from(he)
auts = [m for m in GraphMatcher(g, g).isomorphisms_iter()]
pool, cnf, E = C.build(f); n0 = len(cnf.clauses); symA.add_compswap(f, pool, cnf, E); new = cnf.clauses[n0:]
swaps = symA.components_k2(s, he); twins = C.twin_pairs(s, he)
def key(M): return tuple(sum(r) for r in M) + tuple(x for r in M for x in r)
def sortT(M):
    cols = sorted(zip(*M), reverse=True); return [list(r) for r in zip(*cols)]
def canon(M):
    best = None
    for m in auts:
        P = [None] * s
        for k in S: P[m[k]] = M[k]                     # vertex k becomes m[k]
        Q = sortT(P); kq = key(Q)
        if best is None or kq > best[0]: best = (kq, Q)
    return best[1]
def lexge(a, b): return tuple(a) >= tuple(b)
def props(M):
    d = [sum(r) for r in M]
    lexok = all(lexge(c1, c2) for c1, c2 in zip(list(zip(*M)), list(zip(*M))[1:]))
    twok = all(d[i] > d[j] or (d[i] == d[j] and lexge(M[i], M[j])) for i, j in twins)
    swok = all(lexge([d[a], d[b]] + M[a] + M[b], [d[c], d[dd]] + M[c] + M[dd]) for a, b, c, dd in swaps)
    return lexok, twok, swok
def assign(M):
    val = {}
    for k in S:
        for j, v in enumerate(T): val[E[k, v]] = bool(M[k][j])
    def ev(x):
        if isinstance(x, bool): return x
        if x < 0: return not ev(-x)
        if x in val: return val[x]
        o = pool.id2obj[x]
        if o[0] == 'or': r = ev(o[1]) or ev(o[2])
        elif o[0] == 'and': r = ev(o[1]) and ev(o[2])
        else: raise KeyError(o)
        val[x] = r; return r
    d = [sum(r) for r in M]
    for a, b, c, dd in swaps:                          # intended aux values: prefix equal so far
        prev = True
        for i, j in ((a, c), (b, dd)):
            prev = prev and d[i] == d[j]; val[pool.obj2id[('compswap', a, c, 'deq', i, j)]] = prev
        for i, j in ((a, c), (b, dd)):
            for n, v in enumerate(T):
                prev = prev and M[i][n] == M[j][n]; val[pool.obj2id[('compswap', a, c, 'req', i, j, v)]] = prev
    return lambda cl: any(ev(l) for l in cl)
rnd = random.Random(7); bad = 0; rej_ok = 0; rej_n = 0; viol = 0
for t in range(trials):
    base = [[int(rnd.random() < 0.35) for _ in T] for _ in S]
    for k in S:                                        # many ties: copy rows / zero rows; cap d_T <= 8
        if rnd.random() < 0.4: base[k] = list(base[rnd.randrange(s)])
        while sum(base[k]) > 8: base[k][[j for j, x in enumerate(base[k]) if x][0]] = 0
    M = canon(base); lp, tp, sp = props(M); sat = assign(M)
    ok = lp and tp and sp and all(sat(cl) for cl in new)
    if not ok: bad += 1; print('FAIL', t, lp, tp, sp)
    P = sortT(base); _, _, sp2 = props(P)             # an arbitrary (T-sorted) labelling: clauses must agree with property
    sat2 = assign(P); cl_ok = all(sat2(cl) for cl in new); rej_n += 1; rej_ok += (cl_ok == sp2); viol += (not sp2)
print(json.dumps({'tag': tag, 'trials': trials, 'aut': len(auts), 'swaps': swaps, 'twins': twins, 'canonical_failures': bad,
                  'clauses_equal_property': f'{rej_ok}/{rej_n}', 'of_which_property_false': viol}))
sys.exit(1 if bad or rej_ok != rej_n else 0)
