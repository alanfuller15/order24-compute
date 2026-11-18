"""exp/xrun.py (EXPERIMENT helper; research only, nothing here is part of any check or record).
Shared pieces of exp/symA.py and exp/unionB.py: CNF files written once per variant, per-cube solves by bin/cadical with
the cube as unit clauses, up to JOBS solver processes, clean stop on SIGINT/SIGTERM, JSON-lines output."""
import os, sys, json, time, signal, shutil, subprocess, threading
from concurrent.futures import ThreadPoolExecutor, wait, FIRST_COMPLETED

STOP = threading.Event()
def _stop(sig, frm):
    if not STOP.is_set(): print(f'signal {sig}: stopping (running solvers are killed, summary is written)', flush=True)
    STOP.set()
signal.signal(signal.SIGINT, _stop); signal.signal(signal.SIGTERM, _stop)

def say(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)

class Variant:
    """one formula: its clauses written once to BODY (no header); a solve writes header + body + cube units"""
    def __init__(self, name, nvars, clauses, work):
        self.name, self.nvars, self.ncl = name, nvars, len(clauses)
        self.body = os.path.join(work, f'{name}.body')
        with open(self.body, 'w') as fo:
            buf = []
            for cl in clauses:
                buf.append(' '.join(map(str, cl)) + ' 0\n')
                if len(buf) >= 100000: fo.writelines(buf); buf = []
            fo.writelines(buf)

def solve(cad, var, cube, timeout, work, label, opts=()):
    """('UNSAT'|'SAT'|'TIMEOUT'|'STOPPED'|'ERROR', seconds)"""
    p = os.path.join(work, f'run_{label}.cnf')
    with open(p, 'w') as fo:
        fo.write(f'p cnf {var.nvars} {var.ncl + len(cube)}\n')
        with open(var.body) as fi: shutil.copyfileobj(fi, fo, 1 << 22)
        for l in cube: fo.write(f'{l} 0\n')
    t0 = time.time()
    pr = subprocess.Popen([cad, '-q', '-n', '-t', str(int(timeout))] + list(opts) + [p],
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env={})
    st = None
    while st is None:
        try:
            rc = pr.wait(timeout=1.0)
            st = {10: 'SAT', 20: 'UNSAT'}.get(rc, 'TIMEOUT' if time.time() - t0 >= timeout - 2 else f'ERROR{rc}')
        except subprocess.TimeoutExpired:
            if STOP.is_set(): pr.kill(); pr.wait(); st = 'STOPPED'
            elif time.time() - t0 > timeout + 60: pr.kill(); pr.wait(); st = 'TIMEOUT'
    dt = round(time.time() - t0, 2)
    try: os.remove(p)
    except OSError: pass
    return st, dt

def run_jobs(jobs, fn, jobsn, outp):
    """jobs: list of dicts; fn(job) -> result dict; results appended to outp as JSON lines as they finish"""
    res = []
    with ThreadPoolExecutor(jobsn) as ex:
        pend = set(); it = iter(jobs)
        def fill():
            while len(pend) < jobsn and not STOP.is_set():
                j = next(it, None)
                if j is None: return
                pend.add(ex.submit(fn, j))
        fill()
        while pend:
            done, _ = wait(pend, timeout=2.0, return_when=FIRST_COMPLETED)
            for d in done:
                pend.discard(d); r = d.result(); res.append(r)
                with open(outp, 'a') as fo: fo.write(json.dumps(r) + '\n')
            fill()
    return res
