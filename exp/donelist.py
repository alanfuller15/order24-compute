"""donelist.py RESULTS.jsonl[,...] > a9_done.txt -- unit tags whose every leaf is UNSAT and verified (for round 2+ scheduling only;
a9check.py, not this list, decides coverage)."""
import sys, json, collections, a9run as R
recs = [json.loads(l) for p in sys.argv[1].split(',') for l in open(p)]
by = collections.defaultdict(list)
import a9core as C
for r in recs:
    k2 = C.index_of(r['case'], tuple(r['prof']))       # version-2 index (records of version 1 carry version-1 indices)
    if k2 is not None: by[R.tag_of(r['case'], k2, r['unit'])].append(r)
for t, rs in sorted(by.items()):
    if all(r['status'] == 'TIMEOUT' or r.get('cake_lpr') == 's VERIFIED UNSAT' for r in rs): print(t)
