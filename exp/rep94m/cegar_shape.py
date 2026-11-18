"""Exact lazy (CEGAR) exclusion of one S-class of a residual maximum-cut shape (generalises cegar_general.py / G11).

Frame (shape R*, from enumerate_shapes.py): G in F has a MAXIMUM cut (S, T) with |S| = s <= |T| = t = 24 - s,
the deficient vertices placed as the shape says, e(S) = e_S, e(T) = e_T, and G[S] equal (after relabelling) to the
class template. Every clause below is a necessary condition for such a G:
  labels      S = 0..s-1 (marked S-vertices first: a, b, c as present), T = s..23 (deficient T-vertices first, in
              the order a, b, c, then the regular T-vertices)
  triangles   S-S-T, S-T-T and T-T-T triangles are forbidden (S-S-S: the template is triangle-free)
  degrees     exact S-rows r(k) = d(k) - d_S(k); exact degrees of T-vertices
  local max   d_T(v) <= floor(d(v)/2) for v in T (maximum cut; the S side is enforced by the class filter N2)
  e(T)        exactly e_T
  floors      theta(W) = max(12, 14 - deficit(W)) on the 12-sets  S + (12 - s vertices of T)  and
              T - (t - 12 vertices of T)  (natural floors; all others lazily)
  lex         the regular T-vertices are interchangeable (degree 8, unmarked, every clause is invariant under
              permuting them): their S-incidence columns are lexicographically non-increasing (sound: sort them)
  lazy        alpha(G) <= 8 (9-sets) and every 12-set floor, added from the models found (CEGAR)
Usage: python3 -I cegar_shape.py CLASSES.json SHAPE IDX [outdir]
"""
import sys, os, json, time, itertools as it
import numpy as np
import networkx as nx
from pysat.formula import IDPool, CNF
from pysat.card import CardEnc, EncType
from pysat.solvers import Solver

DEGM = {'a': 6, 'b': 7, 'c': 7}

_M = None
def masks12():
    global _M
    if _M is None:
        p = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'lowcheck', 'masks12.npy')
        if os.path.exists(p): _M = np.load(p)
        else:   # package: regenerate (itertools.combinations order; identical to the original file, checked 2026-11-08)
            _M = np.fromiter((sum(1 << v for v in c) for c in it.combinations(range(24), 12)), dtype=np.uint32, count=2704156)
        assert len(_M) == 2704156
    return _M

def labels(s, marks):
    deg = [8] * 24; inS = sorted(marks); outS = [m for m in 'abc' if m not in marks]
    for i, m in enumerate(inS): deg[i] = DEGM[m]
    for j, m in enumerate(outS): deg[s + j] = DEGM[m]
    reg_T = list(range(s + len(outS), 24))
    return deg, reg_T

def theta(W, defi):
    return max(12, 14 - sum(defi[w] for w in W))

def build(shape, cls, floors=True, lex=True, localmax=True):
    s, marks, eS, eT = shape['s'], shape['marks_in_S'], shape['e_S'], shape['e_T']
    S = list(range(s)); T = list(range(s, 24)); t = 24 - s
    deg, REG = labels(s, marks); defi = [8 - d for d in deg]
    sedges = {tuple(sorted(e)) for e in cls['edges']}; assert len(sedges) == eS
    sdeg = [sum(1 for e in sedges if k in e) for k in S]
    assert [deg[k] - sdeg[k] for k in S] == cls['rows']
    pool = IDPool(); cnf = CNF(); E = {}
    for u, v in it.combinations(S, 2): E[u, v] = (u, v) in sedges
    for k in S:
        for v in T: E[k, v] = pool.id(('x', k, v))
    for u, v in it.combinations(T, 2): E[u, v] = pool.id(('e', u, v))
    L = lambda u, v: E[min(u, v), max(u, v)]
    for (k1, k2) in sedges:
        for v in T: cnf.append([-L(k1, v), -L(k2, v)])                     # S-S-T
    for u, v in it.combinations(T, 2):
        for k in S: cnf.append([-L(u, v), -L(k, u), -L(k, v)])             # S-T-T
    for u, v, w in it.combinations(T, 3): cnf.append([-L(u, v), -L(v, w), -L(u, w)])   # T-T-T
    def card(lits, lo=None, hi=None):
        assert all(not isinstance(l, bool) for l in lits)
        if lo is not None and lo > 0:
            if lo > len(lits): cnf.append([]); return
            cnf.extend(CardEnc.atleast(lits, bound=lo, vpool=pool, encoding=EncType.seqcounter).clauses)
        if hi is not None and hi < len(lits):
            if hi < 0: cnf.append([]); return
            cnf.extend(CardEnc.atmost(lits, bound=hi, vpool=pool, encoding=EncType.seqcounter).clauses)
    for k in S:
        r = deg[k] - sdeg[k]; card([L(k, v) for v in T], r, r)               # exact rows
    tl = {v: [L(v, w) for w in T if w != v] for v in T}
    for v in T:
        card([L(k, v) for k in S] + tl[v], deg[v], deg[v])                   # exact degree
        if localmax: card(tl[v], None, deg[v] // 2)                          # local maximality on T
    card([L(u, v) for u, v in it.combinations(T, 2)], eT, eT)                # e(T)
    for R in (it.combinations(T, 12 - s) if floors else []):                 # floors S + R
        lits = [L(k, v) for v in R for k in S] + [L(u, v) for u, v in it.combinations(R, 2)]
        card(lits, theta(S + list(R), defi) - eS)
    for D in (it.combinations(T, t - 12) if floors else []):                 # floors T - D
        Wc = [v for v in T if v not in D]
        lits = [L(u, v) for u, v in it.combinations(T, 2) if u in D or v in D]
        card(lits, None, eT - theta(Wc, defi))
    for v, w in (zip(REG, REG[1:]) if lex else []):                          # lex-leader on regular T columns
        eq_prev = None
        for k in S:
            xv, xw = L(k, v), L(k, w)
            cnf.append(([-eq_prev] if eq_prev else []) + [-xw, xv])
            eq = pool.id(('lexeq', v, w, k))
            if eq_prev: cnf.append([-eq, eq_prev])
            cnf.append([-eq, -xv, xw]); cnf.append([-eq, xv, -xw])
            cnf.append([eq] + ([-eq_prev] if eq_prev else []) + [-xv, -xw])
            cnf.append([eq] + ([-eq_prev] if eq_prev else []) + [xv, xw])
            eq_prev = eq
    return pool, cnf, E, defi, deg

def run(shape, cls, outdir=None, tag='X', per_iter=60, budget_s=None):
    t0 = time.time(); pool, cnf, E, defi, deg = build(shape, cls)
    base = len(cnf.clauses); sol = Solver(name='cadical195', bootstrap_with=cnf.clauses)
    M = masks12(); dvec = np.zeros(len(M), dtype=np.int16)
    for v in range(24):
        if defi[v]: dvec += ((M >> v) & 1).astype(np.int16) * defi[v]
    thr = np.maximum(12, 14 - dvec); lazy = []; n9 = n12 = 0; itn = 0
    while True:
        itn += 1
        if budget_s and time.time() - t0 > budget_s: res = {'status': 'UNKNOWN_BUDGET'}; break
        if not sol.solve(): res = {'status': 'UNSAT'}; break
        mdl = set(l for l in sol.get_model() if l > 0)
        adj = [k for k, l in E.items() if l is True or (not isinstance(l, bool) and l in mdl)]
        g = nx.Graph(); g.add_nodes_from(range(24)); g.add_edges_from(adj); new = []
        for clq in nx.find_cliques(nx.complement(g)):
            if len(clq) >= 9:
                W = sorted(clq)[:9]; new.append(('9', W))
                if len(new) >= per_iter: break
        am = [0] * 24
        for u, v in adj: am[u] |= 1 << v; am[v] |= 1 << u
        cnt = np.zeros(len(M), dtype=np.int16)
        for v in range(24): cnt += (((M >> v) & 1) * np.bitwise_count(M & np.uint32(am[v]))).astype(np.int16)
        cnt //= 2; bad = np.nonzero(cnt < thr)[0]
        for idx in bad[np.argsort((cnt - thr)[bad])][:per_iter]:
            m = int(M[idx]); new.append(('12', [v for v in range(24) if m >> v & 1], int(thr[idx])))
        if not new: res = {'status': 'ORIGINAL_MODEL_FOUND', 'edges': sorted(adj)}; break
        for item in new:
            W = item[1]; ls = [E[p, q] for p, q in it.combinations(W, 2)]
            free = [l for l in ls if not isinstance(l, bool)]; const = sum(1 for l in ls if l is True)
            if item[0] == '9':
                assert const == 0
                sol.add_clause(free); cnf.append(free); n9 += 1; lazy.append({'kind': 9, 'W': W})
            else:
                bound = item[2] - const; assert 0 < bound <= len(free)
                cl = CardEnc.atleast(free, bound=bound, vpool=pool, encoding=EncType.seqcounter).clauses
                for k in cl: sol.add_clause(k)
                cnf.extend(cl); n12 += 1; lazy.append({'kind': 12, 'W': W, 'threshold': item[2]})
    res.update({'tag': tag, 'iterations': itn, 'floors_added': n12, 'nine_added': n9, 'base_clauses': base,
                'final_vars': pool.top, 'final_clauses': len(cnf.clauses), 'seconds': round(time.time() - t0, 2)})
    if outdir and res['status'] == 'UNSAT':
        os.makedirs(outdir, exist_ok=True); cnf.to_file(os.path.join(outdir, f'{tag}.cnf'))
        json.dump(lazy, open(os.path.join(outdir, f'{tag}.lazy.json'), 'w'))
    return res

if __name__ == '__main__':
    data = json.load(open(sys.argv[1])); sh = data[sys.argv[2]]; i = int(sys.argv[3])
    r = run(sh, sh['classes'][i], sys.argv[4] if len(sys.argv) > 4 else None, tag=f'{sys.argv[2]}_{i:04d}')
    print(json.dumps({k: v for k, v in r.items() if k != 'edges'}))
    if r['status'] == 'ORIGINAL_MODEL_FOUND': json.dump(r, open(f'MODEL_{sys.argv[2]}_{i}.json', 'w'))
