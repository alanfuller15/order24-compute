#!/usr/bin/env python3
"""ccc_merge.py (producer-side; not trusted, not part of any check): join the state folders of the shards of ONE formula
(ccc90.py run with CUBE_SHARD=i/N from a common state) into one state folder that ccc90.py (without CUBE_SHARD) then
stitches, checks with cake_lpr and records as usual.

Why it is needed. Every shard adds its own lazy items (9-sets, 12-set floors) in its own order. A 12-set floor is encoded
with a sequential counter whose auxiliary variables come from the shared variable pool, so the same item has different
auxiliary variable numbers and different clause positions in different shards. A proof segment of a closed cube refers
to clauses of the formula by position (even hints) and to variables by number (literals). Here the merged formula is
base + the items of shard 0 in its order + every other shard's new items in theirs; for each shard every variable and
clause position is mapped to the merged one (item by item: same item -> same encoding, block for block), and its
segments are rewritten. Nothing here is trusted: the final stitched proof is checked by cake_lpr in ccc90.py and later by
the independent auditor (gcert<m>.py) against the CNF rebuilt from the merged lazy list.

Usage: ENCODER=cegar90c|cegar90e MASKS12=... python3 -I -B ccc_merge.py FORMULAS.json TAG OUTSTATE SHARDSTATE [SHARDSTATE ...]"""
import sys, os, json, lzma, bisect, importlib, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
C = importlib.import_module(os.environ.get('ENCODER', 'cegar90c'))
import ccc90 as K   # helpers only (key, rv, wv, jsave, append_line, load_items); main() is not run on import

def ik(x): return (x['kind'], tuple(x['W']))

def layout(f, items):
    """(cnf, n_base_clauses, base_top, blocks): blocks[i] = (item key, clause_start, n_clauses, var_start, n_vars), 0-based
    clause starts, var_start = first aux variable (pool.top before the item)."""
    pool, cnf, E = C.build(f); nb = len(cnf.clauses); top0 = pool.top; blocks = []
    for x in items:
        c0 = len(cnf.clauses); v0 = pool.top
        cl = C.lazy_clauses(x, E, pool); cnf.extend(cl)
        blocks.append((ik(x), c0, len(cl), v0, pool.top - v0))
    return cnf, nb, top0, blocks

def mapper(src, dst):
    """functions var(v) and cls(i) (1-based clause index) from the src layout to the dst layout"""
    _, nb, top0, sb = src; _, nb2, top02, db = dst
    assert nb == nb2 and top0 == top02, 'base formulas differ'
    dpos = {b[0]: b for b in db}
    vstarts = [b[3] for b in sb]; cstarts = [b[1] for b in sb]
    def var(v):
        if v <= top0: return v
        j = bisect.bisect_right(vstarts, v - 1) - 1          # block with var_start < v <= var_start + n_vars
        k, c0, nc, v0, nv = sb[j]; assert v0 < v <= v0 + nv, ('variable outside any item block', v)
        d = dpos[k]; assert d[4] == nv, ('aux block size differs', k)
        return d[3] + (v - v0)
    def cls(i):
        if i <= nb: return i
        j = bisect.bisect_right(cstarts, i - 1) - 1
        k, c0, nc, v0, nv = sb[j]; assert c0 < i <= c0 + nc, ('clause outside any item block', i)
        d = dpos[k]; assert d[2] == nc, ('item clause count differs', k)
        return d[1] + (i - c0)
    return var, cls

def rewrite(b, var, cls):
    """a ccc90 segment (binary LRAT: own clause ids, literals 2v+s, hints: even = 2 x clause of F, odd = 2 x own + 1)"""
    out = bytearray(); p = 0; rv, wv = K.rv, K.wv
    while p < len(b):
        t = b[p]; p += 1; out.append(t)
        if t == 0x61:
            x, p = rv(b, p); wv(x, out)
            while True:
                v, p = rv(b, p)
                if v == 0: out.append(0); break
                wv(2 * var(v >> 1) + (v & 1), out)
            while True:
                v, p = rv(b, p)
                if v == 0: out.append(0); break
                wv(v if v & 1 else 2 * cls(v >> 1), out)
        elif t == 0x64:
            while True:
                v, p = rv(b, p); wv(v, out)
                if v == 0: break
        else:
            raise ValueError(f'unknown byte {t}')
    return bytes(out)

def main():
    fpath, tag, out = sys.argv[1:4]; shards = sys.argv[4:]
    assert shards and not os.path.exists(out), 'need shard folders and a new output folder'
    f = json.load(open(fpath))[tag]
    trees = [json.load(open(os.path.join(s, 'tree.json'))) for s in shards]
    for t in trees: assert t['tag'] == tag and t['encoder'] == trees[0]['encoder']
    lab = {'cegar91': 'v4', 'cegar90': 'v5', 'cegar90b': 'v6', 'cegar90c': 'v7', 'cegar90e': 'v9'}.get(C.__name__)   # v9 package
    C.need(trees[0]['encoder'] == lab, ('the shard states were made with encoder', trees[0]['encoder'], 'but ENCODER is', C.__name__))   # not an assert: kept under python -O
    items_by = [K.load_items(s, tag, None) for s in shards]
    merged_items = []; seen = set()
    for its in items_by:
        for x in its:
            if ik(x) not in seen: seen.add(ik(x)); merged_items.append(x)
    dst = layout(f, merged_items)
    os.makedirs(out); os.makedirs(os.path.join(out, 'work'))
    splits = {}; done = {}; opn = []; seq = 0
    for s, t, its in zip(shards, trees, items_by):
        var, cls = mapper(layout(f, its), dst)
        for k, x in t['splits'].items():
            assert splits.get(k, x) == x, ('shards split one cube differently', k); splits[k] = x
        roots = set(t.get('shard', {}).get('roots', [])) or None
        def mine(c, roots=roots):
            return roots is None or any(K.key(c[:n]) in roots for n in range(len(c) + 1))
        opn += [c for c in t['open'] if mine(c)]
        for k, val in t['done'].items():
            if k in done: continue                               # closed before the shards split up: same segment
            b = lzma.decompress(open(os.path.join(s, val['seg']), 'rb').read())
            nb = rewrite(b, var, cls); name = f'seg_{seq:04d}.xz'; seq += 1
            with open(os.path.join(out, name), 'wb') as fo: fo.write(lzma.compress(nb, preset=1))
            v2 = dict(val); v2['seg'] = name; v2['F_clauses'] = len(dst[0].clauses); done[k] = v2
    tree = {'tag': tag, 'encoder': trees[0]['encoder'], 'open': opn, 'splits': splits, 'done': done, 'conf': {}, 'seq': seq,
            'depth0': trees[0].get('depth0'), 'merged_from': len(shards)}
    K.jsave(os.path.join(out, 'tree.json'), tree)
    K.append_line(os.path.join(out, 'items.jsonl'), {'items': merged_items, 'from': f'merge of {len(shards)} shards', 'time': round(time.time())})
    K.append_line(os.path.join(out, 'log.jsonl'), {'event': 'merged', 'shards': len(shards), 'done': len(done), 'open': len(opn),
                                                    'items': len(merged_items), 'time': round(time.time())})
    print(f'{tag}: merged {len(shards)} shards: {len(done)} closed cubes, {len(opn)} open, {len(merged_items)} items')

if __name__ == '__main__':
    main()
