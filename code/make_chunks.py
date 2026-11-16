"""make_chunks.py M [M ...]: write chunks/m<M>a and chunks/m<M>b (q001.txt, ...) in the compute repo for layer M.
Production bookkeeping only (which formulas a GitHub Actions job attempts); plays no part in any proof.
Scheme (the one used for m80..m88): the s >= 9 tags of formulas<M>_c<M-23>.json, highest index suffix first
(ties by tag); alternate positions go to waves a and b; 4 tags per chunk. s = 8 tags are in chunks/s8/m<M>.txt."""
import sys, os, json, re
SP = '/tmp/claude-0/-home-claude/4a72079e-a9db-5726-b10c-aeb759ad214f/scratchpad'
R = f'{SP}/gh/order24-compute'
for M in map(int, sys.argv[1:]):
    D = f'{SP}/l{M}' if os.path.isdir(f'{SP}/l{M}') else f'{SP}/layers/l{M}'
    F = json.load(open(f'{D}/formulas{M}_c{M - 23}.json'))
    tags = [t for t in F if int(re.match(rf'L{M}_s(\d+)a', t).group(1)) >= 9]
    tags.sort(key=lambda t: (-int(t.rsplit('_', 1)[1]), t))
    for w, part in (('a', tags[0::2]), ('b', tags[1::2])):
        out = f'{R}/chunks/m{M}{w}'; os.makedirs(out, exist_ok=True)
        for i in range(0, len(part), 4):
            open(f'{out}/q{i // 4 + 1:03d}.txt', 'w').write('\n'.join(part[i:i + 4]) + '\n')
    print(M, len(tags), 'tags;', (len(tags[0::2]) + 3) // 4, '+', (len(tags[1::2]) + 3) // 4, 'chunks')
