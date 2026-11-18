#!/usr/bin/env python3
"""a9gate.py LOG [DIR ...] -- job gate for a9shard.sh / a9verify.sh / a9final.sh (RA9C item 5).
Exit 1 (job fails) if any DIR (searched recursively) contains MODEL_FOUND.json, or if LOG has no line
"checked n leaves: m pass" or has one with n != m, or LOG contains "MODEL FOUND" / "A MODEL RECORD IS PRESENT".
With LOG = '-' only the MODEL_FOUND.json search is done. Prints one line GATE: PASS / GATE: FAIL (reason)."""
import sys, os, re
def gate(log, dirs):
    for d in dirs:
        for root, _, files in os.walk(d):
            if 'MODEL_FOUND.json' in files: return 'MODEL_FOUND.json in ' + root
    if log != '-':
        txt = open(log, errors='replace').read() if os.path.exists(log) else ''
        if 'MODEL FOUND' in txt or 'A MODEL RECORD IS PRESENT' in txt: return 'model reported in ' + log
        m = re.findall(r'^checked (\d+) leaves: (\d+) pass', txt, re.M)
        if not m: return 'no "checked n leaves: m pass" line in ' + log
        n, k = map(int, m[-1])
        if n != k: return f'{n - k} of {n} replayed leaves failed'
    return None
if __name__ == '__main__':
    why = gate(sys.argv[1], sys.argv[2:])
    print('GATE: PASS' if why is None else 'GATE: FAIL (' + why + ')')
    sys.exit(0 if why is None else 1)
