"""Read-only extraction of a producer results.jsonl for independent review.
No solver or proof checker is run; input ZIP and extracted bytes are SHA-256 hashed.
Inputs are the standard exp.yml RUN_ID / ARTIFACT / GH_REPO / GH_TOKEN bindings.
"""
import hashlib,json,os,pathlib,urllib.request,zipfile
O=pathlib.Path('exp_out'); O.mkdir(exist_ok=True)
repo=os.environ['GH_REPO']; run=os.environ['RUN_ID']; name=os.environ['ARTIFACT']
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json'}
def get(url): return urllib.request.urlopen(urllib.request.Request(url,headers=headers))
with get(f'https://api.github.com/repos/{repo}/actions/runs/{run}/artifacts?per_page=100') as response:
 artifacts=json.load(response)['artifacts']
matching=[a for a in artifacts if a['name']==name and not a['expired']]
assert len(matching)==1, 'expected exactly one live artifact'
a=matching[0]; archive=pathlib.Path('producer.zip'); h=hashlib.sha256()
with get(a['archive_download_url']) as response, archive.open('wb') as f:
 while chunk:=response.read(1<<20): h.update(chunk); f.write(chunk)
digest='sha256:'+h.hexdigest()
assert digest==a['digest'], 'archive digest mismatch'
with zipfile.ZipFile(archive) as z:
 entries=[n for n in z.namelist() if n=='results.jsonl']
 assert len(entries)==1, 'expected one root results.jsonl'
 data=z.read(entries[0]); (O/'producer-results.jsonl').write_bytes(data)
 evidence={'repo':repo,'producer_run':run,'artifact':a,'archive_digest_verified':digest,
           'entry':entries[0],'results_sha256':hashlib.sha256(data).hexdigest(),
           'job_run':os.environ.get('GITHUB_RUN_ID'),'script_commit':os.environ.get('GITHUB_SHA')}
 (O/'extraction.json').write_text(json.dumps(evidence,indent=2)+'\n')
 print(json.dumps({k:v for k,v in evidence.items() if k!='artifact'},indent=2))
archive.unlink()
