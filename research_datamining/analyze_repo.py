#!/usr/bin/env python3
"""Offline, read-only audit of order24-compute formula, vote, ledger, and meta-artifact data.

Usage:
  python analyze_repo.py --repo /path/to/order24-compute --meta /path/to/*_meta.zip --out metrics.json
No SAT solver is invoked. No closure claim is made. Never interprets an UNSAT record as an independently accepted certificate.
"""
from __future__ import annotations
import argparse, collections, glob, hashlib, json, pathlib, re, zipfile

def key_of(f):
    return (int(f['s']), int(f['a']), int(f['b']), int(f['h_index']), tuple(map(tuple, f['h_edges'])))

def load_formulas(repo):
    rows, errors = [], []
    for path in sorted((repo/'data').glob('formulas*_c*.json')):
        m = re.fullmatch(r'formulas(\d+)_c(\d+)\.json', path.name)
        if m is None: continue
        layer, cutoff = map(int, m.groups())
        if layer - cutoff != 23: errors.append(f'{path}: expected c_min=m-23')
        records = json.loads(path.read_text())
        for tag, f in records.items():
            if f['tag'] != tag: errors.append(f'{path}: tag mismatch {tag}')
            if f['m'] != layer or f['a'] + f['b'] + f['c'] != layer:
                errors.append(f'{path}: arithmetic mismatch {tag}')
            rows.append((layer, tag, key_of(f)))
    return rows, errors

def vote_stats(path, focus_tags):
    if not path.is_file(): return None
    obj = json.loads(path.read_text())
    tags = obj['tags']; idx = {tag:i for i,tag in enumerate(tags)}
    stats = {'tags':len(tags),'cube_keys':len(obj['votes']), 'observations':0,
             'duplicate_observations':0,'conflicting_tag_cube_pairs':0, 'keys_with_duplicates':0,
             'affected_prediction_keys':{tag:0 for tag in focus_tags if tag in idx}}
    for cube, obs in obj['votes'].items():
        stats['observations'] += len(obs)
        seen = set(); bytag = collections.defaultdict(set)
        for tagid,outcome in obs:
            if not (isinstance(tagid,int) and 0 <= tagid < len(tags) and outcome in (0,1)):
                raise ValueError(f'malformed observation for {cube}')
            if (tagid,outcome) in seen: stats['duplicate_observations'] += 1
            seen.add((tagid,outcome));bytag[tagid].add(outcome)
        stats['conflicting_tag_cube_pairs'] += sum(len(v)==2 for v in bytag.values())
        if len(seen)<len(obs):stats['keys_with_duplicates'] += 1
        for tag in stats['affected_prediction_keys']:
            own=idx[tag];old=[outcome for tagid,outcome in obs if tagid!=own]
            unique=[outcome for tagid,outcome in seen if tagid!=own]
            vote_old=sum(old)/len(old) if old else -1
            vote_new=sum(unique)/len(unique) if unique else -1
            if abs(vote_old-vote_new)>1e-12 or min(len(old),20)!=min(len(unique),20):
                stats['affected_prediction_keys'][tag] += 1
    return stats

def meta_stats(paths):
    meta=[]; bank=[]
    for p in paths:
        with zipfile.ZipFile(p) as z:
            names=[n for n in z.namelist() if n.endswith('results.jsonl')]
            for name in names:
                for lineno,line in enumerate(z.read(name).splitlines(),1):
                    if not line.strip():continue
                    r=json.loads(line)
                    items=r.get('lazy',[])
                    valid=[]
                    for item in items:
                        kind,W=item['kind'],item['W']
                        if kind not in (9,12) or len(W)!=kind or any(type(v)!=int or v<0 or v>=24 for v in W) or sorted(set(W))!=W:
                            raise ValueError(f'invalid set in {p}:{name}:{lineno}')
                        valid.append((kind,tuple(W)))
                    if len(set(valid))!=len(valid): raise ValueError(f'duplicate lazy items in {p}:{name}:{lineno}')
                    record={'tag':r.get('tag'),'status':r.get('status'),'encoder':r.get('encoder'),
                      'reused_lazy':r.get('reused_lazy'),'source_meta':p.name,
                      'source_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                      'full_proof_sha256':r.get('proof_sha256'),'cnf_sha256':r.get('cnf_sha256'),
                      'lazy_counts':dict(collections.Counter(str(k) for k,_ in valid)),
                      'lazy_total':len(valid),'cube_cad_seconds':r.get('cube_cad_seconds'),
                      'cake_seconds':r.get('cake_seconds'),'proof_xz_bytes':r.get('proof_xz_bytes')}
                    meta.append(record)
                    bank.append((record['tag'],valid))
    overlaps=[]
    for i in range(len(bank)):
        for j in range(i+1,len(bank)):
            a,b=bank[i],bank[j];A=set(a[1]);B=set(b[1]);
            overlaps.append({'tags':[a[0],b[0]],'intersection':len(A&B),
                             'jaccard':round(len(A&B)/len(A|B),6) if A or B else 0,
                             'same_12':len({w for k,w in A if k==12}&{w for k,w in B if k==12})})
    return meta,overlaps,bank

def analyze(root, metas):
    formulas,errors=load_formulas(root)
    recorded=set((root/'ops/recorded.txt').read_text().splitlines())
    family=collections.defaultdict(list);unrecorded=[]
    for m,tag,key in formulas:
        family[key].append(m)
        if tag not in recorded: unrecorded.append({'layer':m,'tag':tag,'family':repr(key)})
    layers=collections.Counter(m for m,_,_ in formulas)
    focus=[x['tag'] for x in unrecorded]
    votes=vote_stats(root/'data/pred_votes.json', focus)
    meta,overlaps,bank=meta_stats(metas)
    return {'n_formula_slots':len(formulas),'n_recorded_slots':len(formulas)-len(unrecorded),
      'n_distinct_labeled_H_templates':len(family),'layer_counts':dict(sorted(layers.items())),
      'unrecorded':unrecorded,'catalogue_errors':errors,'historical_votes':votes,
      'meta_records':meta,'meta_lazy_overlap':overlaps},bank

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--repo',required=True,type=pathlib.Path)
    ap.add_argument('--meta',nargs='*',default=[]);ap.add_argument('--out',default='mining_metrics.json');ap.add_argument('--bank',default='')
    args=ap.parse_args();paths=sorted({pathlib.Path(p) for pat in args.meta for p in glob.glob(pat)})
    report,bank=analyze(args.repo,paths)
    pathlib.Path(args.out).write_text(json.dumps(report,indent=2)+'\n')
    if args.bank:
        with open(args.bank,'w') as f:
            for tag,items in bank:
                f.write(json.dumps({'source':tag,'lazy':[{'kind':k,'W':list(W)} for k,W in items]},separators=(',',':'))+'\n')
    print('slots',report['n_formula_slots'],'recorded',report['n_recorded_slots'],'unrecorded',len(report['unrecorded']))
    print('unique H templates',report['n_distinct_labeled_H_templates'],'votes',report['historical_votes'])
    print('metadata',[(x['tag'],x['lazy_total']) for x in report['meta_records']])
if __name__=='__main__':main()
