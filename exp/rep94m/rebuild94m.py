#!/usr/bin/env python3
"""Rebuild the certified CNF of one class byte for byte from the class template and its recorded lazy list
(the same steps as cegar95.run, in the same order, without a solver), print its SHA-256, optionally write it.
Usage: python3 -I rebuild94m.py classes94m.json SHAPE IDX LAZY.json.gz [OUT.cnf]"""
import sys, os, json, gzip, hashlib, itertools as it
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cegar_shape as C   # the audited mixed-pattern encoder, unchanged
FLOOR_C = 14              # 108 - m at m = 94: theta(W) = max(12, 14 - deficit(W)), as in cegar_shape.theta

def need(cond, msg):
    if not cond: raise ValueError(msg)          # explicit checks: not removed by python -O
from pysat.card import CardEnc, EncType

def rebuild(sh, cls, lazy):
    pool, cnf, E, defi, deg = C.build(sh, cls)
    for item in lazy:
        W = item['W']; need(W == sorted(set(W)) and all(0 <= w < 24 for w in W), ('malformed lazy set', W))
        ls = [E[p, q] for p, q in it.combinations(W, 2)]
        free = [l for l in ls if not isinstance(l, bool)]; const = sum(1 for l in ls if l is True)
        if item['kind'] == 9:
            need(const == 0 and len(W) == 9, ('bad 9-set', W)); cnf.append(free)
        else:
            need(len(W) == 12 and item['threshold'] == max(12, FLOOR_C - sum(defi[w] for w in W)), ('bad 12-set', W))
            bound = item['threshold'] - const; need(0 < bound <= len(free), ('bad bound', W))
            cnf.extend(CardEnc.atleast(free, bound=bound, vpool=pool, encoding=EncType.seqcounter).clauses)
    return cnf

if __name__ == '__main__':
    data = json.load(open(sys.argv[1])); sh = data[sys.argv[2]]; i = int(sys.argv[3])
    lazy = json.load(gzip.open(sys.argv[4]))
    cnf = rebuild(sh, sh['classes'][i], lazy)
    out = sys.argv[5] if len(sys.argv) > 5 else '/dev/stdout'
    if len(sys.argv) > 5:
        cnf.to_file(out); print(hashlib.sha256(open(out, 'rb').read()).hexdigest())
    else:
        import tempfile
        with tempfile.NamedTemporaryFile(suffix='.cnf') as t:
            cnf.to_file(t.name); print(hashlib.sha256(open(t.name, 'rb').read()).hexdigest())
