#!/usr/bin/env python3
"""ccc90.py, version 1.10 (open-list normalisation before shard roots are chosen, see "Version 1.10" below; OPEN_NORMALIZE=0 = 1.9) /
1.9 (PRED4_MODEL: per-job choice of the pred4 model file, sha256-pinned, falls back to data/pred_model4.json; see
"Version 1.9" below; unset = 1.8) / 1.8 (cost/host telemetry, see "Version 1.8" below; TELEMETRY2=0 = 1.7) / 1.7 (telemetry: per-event UTC times and model/vote/encoder digests in log.jsonl, see "Version 1.7" below;
TELEMETRY=0 = 1.6) / 1.6 (pred4: richer pre-attempt model data/pred_model4.json, see "Version 1.6" below; PRED4=0 = 1.5) / 1.5 (on-line calibration of the hard-cube model, see "Version 1.5" below; PRED_ONLINE=0 = 1.4) / 1.1 (R90D should-fix 3-5: ORIGINAL_MODEL_FOUND also goes to OUTDIR/results.jsonl; a seed line may
hold its items under "lazy" (lazy_ckpt.jsonl); the tree keeps the depth it was made with) (producer-side; not trusted, not part of any check): cube-and-conquer CEGAR for one hard layer-90
formula, ending in ONE ordinary record with ONE LRAT proof, so that the assembler, gcert90c.py and cake_lpr are used
unchanged.

Why. A hard formula's single CaDiCaL run can be longer than a 2-hour job and cannot be resumed. Here the search space is
split into cubes (conjunctions of literals), every cube is searched and proved on its own, and all progress is saved:
the lazy items after every model, a cube's proof segment as soon as the cube is proved, the cube tree after every split.
A killed run loses at most the solver call in progress.

The record is what grun90 writes: the lazy list (9-sets that must hold an edge, 12-sets with at least 12 edges; true for
every graph of the class, and checked by the certificate checker through the CNF rebuild), the SHA-256 of
CNF = rebuild(f, lazy) with the encoder named in the record, and an LRAT proof of exactly that CNF, verified here by
cake_lpr (the producer's own check) and later by the auditor (gcert90c.py or gcert90d.py). How the lazy list and the proof were found
plays no part in correctness.

Steps.
1. Cubes. A lookahead tree to depth CUBE_DEPTH (default 3) over the edge variables of the formula (and, with encoder
   version 6 or 7 on a tight iso8 profile, the variables "d_T(k) >= 8" of the isolated S vertices, read off the iso8
   clauses): at each node the variable whose two sides propagate most (PySAT Minisat22, product of the two counts) is
   chosen; a variable one of whose sides fails at once is not chosen. The leaves are the cubes. The tree is saved.
2. For the first open cube c (in tree order):
   a. PySAT CaDiCaL 1.9.5 (one incremental solver over the base formula and all items, kept across cubes) solves under
      the assumptions c, with the cube's conflict budget (CONF, default 20000) and a time cap (PYSAT_CAP, default
      900 s; PySAT's CaDiCaL cannot be interrupted, so the cap is a conflict cap from the measured conflict rate,
      kept in the tree). A model adds the lazy items it violates (the rule of cegar91.run/grun90.search: up to 60 independent
      9-sets and the 60 sparsest 12-sets; none = ORIGINAL_MODEL_FOUND, saved, exit 2) and the cube is solved again.
   b. Otherwise (UNSAT under c, or budget or cap used up) the external CaDiCaL 3.0.1 refutes F_c, the current formula
      simplified by c (cube90.py's construction: a clause with a true cube literal is left out, false cube literals are
      removed), writing a binary LRAT proof, with a time limit (EXT_TIMEOUT, default 1500 s):
      - UNSAT: the proof is trimmed (lrat-trim) and turned into the cube's segment: every derived clause C becomes
        C or D_c (D_c = the negation of c), a hint naming F_c's clause j names that clause of F, deletions of F's
        clauses are dropped, and the empty clause becomes D_c. The segment is saved (xz) and the cube is closed.
      - SAT: the model (with c) is a model of F; its violated items are added as in a; the cube's budget is multiplied
        by GROW (default 16).
      - time limit: the cube is split by the lookahead of step 1 below c, into c + [x] and c + [-x].
3. Stitch, when every cube is closed. F = rebuild(f, items) for the final item list. Items only grow and rebuild()
   appends each item's clauses (with fresh auxiliary variables) in order, so the formula a segment was made from is a
   prefix of F, clause for clause; its hints name the same clauses in F. The segments, renumbered into one id sequence
   after F's clauses, and then the cube tree resolved bottom up (each internal node c: the clause D_c from D_{c+[x]}
   and D_{c+[-x]}, hints those two), give a binary LRAT proof of F ending in the empty clause. It is trimmed when it is
   below TRIM_MAX bytes, compressed with xz into PROOFS/TAG.lrat.xz, checked by cake_lpr against the CNF file (which
   must equal rebuild(f, lazy)), and recorded in OUTDIR/results.jsonl as grun90 records it, with
   "proof_by": "cube-and-conquer".
DEADLINE (epoch seconds): no solver call is started that could run past it; the run stops with exit 3 and resumes
from its state folder on the next start. Exit 0: recorded; 1: cake_lpr did not verify (failed_attempts.jsonl);
2: ORIGINAL_MODEL_FOUND; 3: stopped for the deadline.
Usage: MASKS12=... ENCODER=cegar90b|cegar90c|cegar90e [PROOFS=dir] [CAKE_LOCK=path] [CONF] [GROW] [CAD_OPTS] [CUBE_DEPTH] [EXT_TIMEOUT]
       [PYSAT_CAP] [DEADLINE] [TRIM_MAX] python3 -I -B ccc90.py FORMULAS.json TAG STATEDIR OUTDIR [SEED.jsonl]
SEED.jsonl (first start only): grun90 lazy_partial.jsonl or lazy_ckpt.jsonl files, comma-separated; the lines of TAG
give the seed items, in order, each item kept once."""
import sys, os, json, time, subprocess, hashlib, io, lzma, fcntl, importlib
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ENCODER_MOD = os.environ.get('ENCODER', 'cegar90b')
C = importlib.import_module(ENCODER_MOD)
ENC_LABEL = {'cegar91': 'v4', 'cegar90': 'v5', 'cegar90b': 'v6', 'cegar90c': 'v7', 'cegar90e': 'v9'}[ENCODER_MOD]   # v9: cegar90e.py (v7 + auts)
from pysat.solvers import Solver
import pysat
CAD = os.environ.get('CAD', os.path.expanduser('~/tools/cadical/build/cadical'))
TRIM = os.environ.get('TRIM', os.path.expanduser('~/tools/lrat-trim/lrat-trim'))
CAKE = os.environ.get('CAKE', os.path.expanduser('~/tools/cake_lpr/cake_lpr'))
CAD_OPTS = os.environ.get('CAD_OPTS', '--unsat').split()
CONF0 = int(os.environ.get('CONF', '20000')); GROW = int(os.environ.get('GROW', '16'))
DEPTH0 = int(os.environ.get('CUBE_DEPTH', '3')); EXT_TIMEOUT = float(os.environ.get('EXT_TIMEOUT', '1500'))
PYSAT_CAP = float(os.environ.get('PYSAT_CAP', '900')); DEADLINE = float(os.environ.get('DEADLINE', '0')) or None
# Hard-cube prediction (version 1.3, producer-side only): after the PySAT probe runs out of budget, a cube that the model
# (data/pred_model.json, trained on earlier cube logs; votes from other formulas' trees in data/pred_votes.json) predicts to hit
# EXT_TIMEOUT is split at once by the same lookahead instead of running CaDiCaL until the time limit. The cube tree, proof
# segments, stitch and checks are unchanged (a split is a split). At most one predicted split between two real attempts
# (children of a predicted split always get a CaDiCaL attempt). PREDICT=0 turns it off; PRED_TH overrides the threshold.
_HERE = os.path.dirname(os.path.abspath(__file__))
# Version 1.5 (research/pred3, producer-side only): on-line calibration of the 'pre' model inside the run. Every attempted cube
# whose p was computed adds (p, timed out?) to a window of the last PRED_W attempts of THIS state folder (rebuilt from the "pp"
# fields of log.jsonl on resume); the shipped p is shifted in logit space by b = logit((Y + A*Pm)/(N + A)) - logit(Pm) (Y timeouts,
# N attempts, Pm mean shipped p in the window; |b| <= PRED_B), so a model trained on another encoder or time scale corrects itself
# from the tree's own outcomes. Guard: with a full window, if the calibrated p's log loss is worse than the window's own constant
# rate by more than PRED_M nats per cube, the cube is attempted (plain behaviour) and the split is logged as held back. Any error in
# the model or the calibration -> plain behaviour for that cube. PRED_ONLINE=0 gives v1.4's decisions exactly (with PRED_TH as
# v1.4 used it). Only which cubes are split before an attempt changes; formula, segments, stitch and checks are untouched.
ONLINE = os.environ.get('PRED_ONLINE', '1') != '0'
# Version 1.7 (research/telemetry, producer-side only, log fields only): every cube event of log.jsonl (pysat, model, closed, split,
# predicted split) gets 'time' = UTC epoch seconds when the line is written, and every attempt outcome (closed, split, external
# model, predicted split) gets 't_dec' = UTC epoch seconds when the loop picked the cube up and decided what to do with it (before
# the PySAT probe or the model's prediction). The start event gets the sha256 of the bytes of data/pred_model.json,
# data/pred_votes.json and data/pred_model4.json as they were parsed (null when not loaded / not in use), the encoder label,
# module and sha256 of its source, and this file's sha256. Purely additive: no other field, line, file, decision, split, segment,
# proof, record or exit code changes; any error in the telemetry code drops the telemetry fields, never the run.
# TELEMETRY=0 gives version 1.6's log and code path exactly.
TELEMETRY = os.environ.get('TELEMETRY', '1') != '0'
_TEL_SHA = {}                                                    # file name -> sha256 of the bytes that were parsed
def _jload(path):
    """json.load(open(path)) (unchanged with TELEMETRY=0); with telemetry, the same text decoding of the same bytes, plus their sha256"""
    if not TELEMETRY: return json.load(open(path))
    with open(path, 'rb') as fb: raw = fb.read()
    obj = json.loads(io.TextIOWrapper(io.BytesIO(raw)).read())  # same default encoding / newline handling as open(path)
    try: _TEL_SHA[os.path.basename(path)] = hashlib.sha256(raw).hexdigest()
    except Exception: pass
    return obj
def _tt():
    try: return {'time': round(time.time(), 3)} if TELEMETRY else {}
    except Exception: return {}
def _td(t):
    try: return {'t_dec': round(t, 3)} if (TELEMETRY and t is not None) else {}
    except Exception: return {}
def _sha_file(path):
    with open(path, 'rb') as fb: return hashlib.sha256(fb.read()).hexdigest()
def _tel_start():
    """the start event's telemetry fields; {} with TELEMETRY=0 or on any error"""
    if not TELEMETRY: return {}
    try:
        g = lambda name, on: _TEL_SHA.get(name) if on else None
        return {'telemetry': 1, 'ccc90_version': '1.7', 'ccc90_sha256': _sha_file(os.path.abspath(__file__)),
                'encoder': ENC_LABEL, 'encoder_module': ENCODER_MOD, 'encoder_sha256': _sha_file(C.__file__),
                'pred_model_sha256': g('pred_model.json', PRED is not None), 'pred_votes_sha256': g('pred_votes.json', PRED is not None),
                'pred_model4_sha256': g('pred_model4.json', PRED4 is not None),
                'pred_active': 'pred4' if PRED4 is not None else ('pred' if PRED is not None else None),
                'pred_th': PRED['th'] if PRED is not None else None}
    except Exception:
        return {'telemetry': 1, 'ccc90_version': '1.7', 'telemetry_error': 1}
# Version 1.8 (research/telemetry/v18, producer-side only, log fields only): cost and host telemetry for the v8 shadow engine and the
# cost-per-verified-cube metric. start: 'telemetry2', host facts, runner env, python/pysat versions, solver binary sha256, the run's
# configuration, a process nonce. Attempt outcomes (closed, timeout split, external model, predicted split): this visit's CPU seconds
# of this process and of its waited children (CaDiCaL + lrat-trim), the time limit given to CaDiCaL, CaDiCaL's raw proof bytes, the
# segment's xz bytes, and the 25 pred4 inputs when pred4 made the decision. PySAT probe lines: PySAT decisions/propagations used.
# At most once per 60 s (on a cube line that is written anyway) and on stop/shard_done/ORIGINAL_MODEL_FOUND/recorded lines: peak RSS,
# free disk of OUTDIR, process wall/CPU totals and per-process counters; the recorded line also gets the cake_lpr CPU and proof sizes.
# No telemetry value is read by any decision; every helper returns {} on error; no line is added or removed. TELEMETRY2=0 gives
# version 1.7's log exactly (TELEMETRY=0 still gives 1.6). CaDiCaL runs with -q (no statistics on its output) and its call is not
# changed, so its conflicts/decisions are not available; its CPU seconds stand in as the effort measure.
TEL2 = TELEMETRY and os.environ.get('TELEMETRY2', '1') != '0'
_T2 = {'t0': time.time() if TEL2 else None, 'last': 0.0, 'out': None, 'ext': {}, 'x4': None,
       'n': {'att': 0, 'unsat': 0, 'tmo': 0, 'pred': 0, 'sat': 0, 'seg_bytes': 0}}   # (no key equal to an event name)
_T2_ENV = ('GITHUB_RUN_ID', 'GITHUB_RUN_ATTEMPT', 'GITHUB_JOB', 'GITHUB_WORKFLOW', 'RUNNER_NAME', 'RUNNER_OS', 'RUNNER_ARCH',
           'CODESPACE_NAME', 'CHUNK', 'WAVE', 'LANE', 'LANE_ID', 'LANE_NUMBER', 'CUBE_SHARD')
def _t2clean(o):
    """drop keys/strings that the resume scans ('"split"', '"pp"') could see"""
    if isinstance(o, dict): return {k: _t2clean(v) for k, v in o.items() if k not in ('split', 'pp') and not (isinstance(v, str) and v in ('split', 'pp'))}
    if isinstance(o, list): return [_t2clean(v) for v in o if not (isinstance(v, str) and v in ('split', 'pp'))]
    return o
def _t2ru():
    import resource
    s = resource.getrusage(resource.RUSAGE_SELF); c = resource.getrusage(resource.RUSAGE_CHILDREN)
    return s.ru_utime + s.ru_stime, c.ru_utime + c.ru_stime, s.ru_maxrss, c.ru_maxrss
def _t2_mark():
    """at the decision instant: (self CPU, children CPU) so far; None with TELEMETRY2=0 or on error"""
    if not TEL2: return None
    try: _T2['x4'] = None; _T2['ext'] = {}; return _t2ru()[:2]
    except Exception: return None
def _t2_x4(f4):
    try:
        if TEL2: _T2['x4'] = [(int(v) if v.is_integer() else round(v, 4)) if v == v and abs(v) != float('inf') else None
                              for v in (float(u) for u in f4)]       # (strict JSON: no NaN / Infinity)
    except Exception: pass
def _t2_lrat(pr):
    try:
        if TEL2 and os.path.exists(pr): _T2['ext']['lrat_bytes'] = os.path.getsize(pr)
    except Exception: pass
def _t2_snap(force=False):
    """resources, at most once per 60 s unless force"""
    if not TEL2: return {}
    try:
        now = time.time()
        if not force and now - _T2['last'] < 60: return {}
        _T2['last'] = now; r = _t2ru()
        d = {'rss_mb': round(r[2] / 1024, 1), 'rss_child_mb': round(r[3] / 1024, 1), 'wall_tot': round(now - _T2['t0'], 1),
             'cpu_self_tot': round(r[0], 2), 'cpu_child_tot': round(r[1], 2)}
        try:
            if _T2['out']: v = os.statvfs(_T2['out']); d['disk_free_mb'] = v.f_bavail * v.f_frsize // 2 ** 20
        except Exception: pass
        return d
    except Exception: return {}
def _t2_att(mark, kind, extra=None):
    """an attempt outcome's fields: this visit's CPU, extra (non-None values), the periodic snapshot; counters"""
    if not TEL2 or mark is None: return {}
    try:
        r = _t2ru(); d = {'cpu_self': round(r[0] - mark[0], 2), 'cpu_child': round(r[1] - mark[1], 2)}
        for k2, v in (extra or {}).items():
            if v is not None: d[k2] = v
        if _T2['x4'] is not None: d['x4'] = _T2['x4']
        n = _T2['n']; n[kind] += 1
        if kind != 'pred': n['att'] += 1
        if d.get('seg_bytes'): n['seg_bytes'] += d['seg_bytes']
        d.update(_t2_snap()); return _t2clean(d)
    except Exception: return {}
def _t2_ps(sol, s0):
    """PySAT probe effort (decisions, propagations) since s0 = sol.accum_stats() before the call"""
    if not TEL2 or s0 is None: return {}
    try:
        s1 = sol.accum_stats(); d = {'ps_dec': s1.get('decisions', 0) - s0.get('decisions', 0), 'ps_prop': s1.get('propagations', 0) - s0.get('propagations', 0)}
        d.update(_t2_snap()); return d
    except Exception: return {}
def _t2_end(extra=None):
    """stop / shard_done / ORIGINAL_MODEL_FOUND / recorded: totals of this process and its counters"""
    if not TEL2: return {}
    try:
        d = _t2_snap(True); d['n_proc'] = dict(_T2['n'])
        for k2, v in (extra or {}).items():
            if v is not None: d[k2] = v
        return _t2clean(d)
    except Exception: return {}
def _t2_ext(to, segpath):
    """the CaDiCaL attempt's limit, raw proof bytes and segment xz bytes"""
    if not TEL2: return {}
    try:
        d = {'ext_to': round(float(to), 1), 'lrat_bytes': _T2['ext'].get('lrat_bytes')}
        if segpath and os.path.exists(segpath): d['seg_bytes'] = os.path.getsize(segpath)
        return d
    except Exception: return {}
def _t2_rec(cmark, ncubes, rawb, trimb, tree, state):
    """the recorded line: cake_lpr CPU, the verified proof's sizes, all segments' bytes, totals"""
    if not TEL2: return {}
    try:
        e = {'n_cubes': ncubes, 'proof_raw_bytes': rawb, 'proof_trim_bytes': trimb if trimb is not None else rawb}
        try: e['cake_cpu'] = round(_t2ru()[1] - cmark[1], 2)
        except Exception: pass
        try: e['seg_bytes_tree'] = sum(os.path.getsize(os.path.join(state, v['seg'])) for v in tree['done'].values())
        except Exception: pass
        return _t2_end(e)
    except Exception: return {}
def _t2_start(outdir):
    """the start event's version 1.8 fields; {} with TELEMETRY2=0, partial on errors"""
    if not TEL2: return {}
    d = {'telemetry2': 1, 'ccc90_version': '1.10'}
    try: _T2['out'] = outdir
    except Exception: pass
    try: d.update({'pred4_model_path': _P4_INFO['path'], 'pred4_model_override': bool(_P4_INFO['override']),   # version 1.9
                   'pred4_model_fallback_reason': _P4_INFO['reason']})
    except Exception: pass
    try: import uuid; d['proc_uid'] = uuid.uuid4().hex[:16]; d['t_proc0'] = round(_T2['t0'], 3)
    except Exception: pass
    try:
        h = {'nproc': os.cpu_count()}
        try: h['nproc_avail'] = len(os.sched_getaffinity(0))
        except Exception: pass
        try: h['node'] = os.uname().nodename[:64]
        except Exception: pass
        try:
            with open('/proc/cpuinfo') as fi: h['cpu'] = next((l.split(':', 1)[1].strip()[:80] for l in fi if l.startswith('model name')), None)
        except Exception: pass
        try:
            with open('/proc/meminfo') as fi: h['mem_mb'] = next((int(l.split()[1]) // 1024 for l in fi if l.startswith('MemTotal:')), None)
        except Exception: pass
        d['host'] = h
    except Exception: pass
    try: d['runner_env'] = {k2: os.environ[k2][:100] for k2 in _T2_ENV if os.environ.get(k2)}
    except Exception: pass
    try: import platform; d['python_version'] = platform.python_version(); d['pysat_version'] = pysat.__version__
    except Exception: pass
    for name, path in (('cadical_sha256', CAD), ('trim_sha256', TRIM), ('cake_sha256', CAKE)):
        try: d[name] = _sha_file(path)
        except Exception: d[name] = None
    try:
        d['cfg'] = {'ext_timeout': EXT_TIMEOUT, 'pysat_cap': PYSAT_CAP, 'conf0': CONF0, 'grow': GROW, 'cube_depth': DEPTH0,
                    'cad_opts': ' '.join(CAD_OPTS), 'trim_max': TRIM_MAX, 'margin': MARGIN, 'cake_heaps': os.environ.get('CAKE_HEAPS', '2000,4000'),
                    'predict': os.environ.get('PREDICT', '1'), 'pred4': os.environ.get('PRED4', '1'), 'pred_online': int(ONLINE)}
    except Exception: pass
    try: d.update(_t2_snap(True))
    except Exception: pass
    try: return _t2clean(d)
    except Exception: return {'telemetry2': 1, 'ccc90_version': '1.10', 'telemetry_error': 2}
PRED_W = int(os.environ.get('PRED_W', '40')); PRED_A = float(os.environ.get('PRED_A', '10'))
PRED_B = float(os.environ.get('PRED_B', '3')); PRED_M = float(os.environ.get('PRED_M', '0.1'))
def _load_pred():
    if os.environ.get('PREDICT', '1') == '0': return None
    try:
        m = _jload(os.path.join(_HERE, '..', 'data', 'pred_model.json'))
        v = _jload(os.path.join(_HERE, '..', 'data', 'pred_votes.json'))
        m['th'] = float(os.environ.get('PRED_TH', m.get('threshold', 0.2))); m['votes'] = v['votes']; m['tags'] = v['tags']
        import math
        q = _pred_p(m, [1, 1, 6, 0.5, 5])                        # version 1.5: a malformed model fails here, not mid-run
        if not (0.0 <= q <= 1.0 and math.isfinite(q)) or not isinstance(m['votes'], dict) or not isinstance(m['tags'], list): return None
        return m
    except Exception:
        return None
def _pred_p(M, x):
    import math
    s = M['init']
    for L, R, F, Th, V in M['trees']:
        n = 0
        while L[n] != -1: n = L[n] if x[F[n]] <= Th[n] else R[n]
        s += M['lr'] * V[n]
    return 1 / (1 + math.exp(-s))
PRED = _load_pred()
def pred_p(x): return _pred_p(PRED, x)
# Version 1.6 (research/pred4_jepa, producer-side only): a second 'pre' model, data/pred_model4.json, same tree format, 25 inputs known
# before the attempt: the five of version 1.4, the formula (layer, c, H index, log10 of the time limit), the cube's last two literals
# and its negative literals, and the outcomes of relatives ALREADY attempted in this state folder's log (sibling, uncle, every cube
# under the same grand-parent, the parent's log-seconds). PRED4=0 (or PREDICT=0, or a missing/malformed file, or any error while
# computing the inputs) -> the version 1.5 model decides, exactly as before. PRED4_ENC_GATE=0 keeps other encoders' votes (default:
# votes recorded under another encoder than this run's are ignored by the new model; all 13 false splits on v9 trees came from them).
P4_NAMES = ['parent_to', 'grand_to', 'depth', 'vote', 'n_vote', 'layer', 'c', 'hidx', 'logT', 'last_sign', 'last_var', 'n_neg', 'frac_neg',
            'prev_sign', 'prev_var', 'sib_known', 'sib_to', 'sib_ls', 'unc_known', 'unc_to', 'unc_ls', 'cous_n', 'cous_rate', 'cous_mls', 'par_ls']
def _p4_ls(s): import math; return math.log10(max(float(s), 0.1))
def p4_feats(tag, cube, T, timed_out, seen, o):
    """the 25 inputs of pred_model4.json. cube: list of literals; T: time limit in seconds; timed_out: set of cube keys; seen: {cube key:
    (timed out, log10 seconds)} of the cubes attempted so far in this log whose parent was not a predicted split; o: votes (0/1) of
    other formulas for this cube key. Mirrors research/pred4_jepa/build_data.py (checked by install/test/test_feats.py)."""
    import math, re
    key = lambda c: ' '.join(map(str, c))                         # (the module's key() is defined further down)
    li = [int(v) for v in cube]; n = len(li); k = key(li); par = key(li[:-1]); gp = key(li[:-2]); sib = key(li[:-1] + [-li[-1]])
    unc = key(li[:-2] + [-li[-2]]) if n >= 2 else None
    m = re.match(r'L(\d+)_s(\d+)a(\d+)b(\d+)c(\d+)_(\d+)', tag); logT = math.log10(max(100.0, round(float(T), -2)))
    pto = int(par in timed_out); gto = int(gp in timed_out); neg = sum(v < 0 for v in li)
    cous = [seen[q] for q in seen if q.startswith(gp + ' ') and q != k] if gp else []
    s_ = seen.get(sib); u_ = seen.get(unc) if unc else None; p_ = seen.get(par)
    return [pto, gto, n, (sum(o) / len(o)) if o else -1.0, min(len(o), 20), int(m.group(1)), int(m.group(5)), int(m.group(6)), logT,
            1.0 if li[-1] > 0 else 0.0, abs(li[-1]), neg, neg / n, (1.0 if li[-2] > 0 else 0.0) if n > 1 else 0.5, abs(li[-2]) if n > 1 else 0,
            float(s_ is not None), float(s_[0]) if s_ else 0.0, s_[1] if s_ else 1.0, float(u_ is not None), float(u_[0]) if u_ else 0.0, u_[1] if u_ else 1.0,
            math.log10(1 + len(cous)), (sum(c[0] for c in cous) + 0.26) / (len(cous) + 2), (sum(c[1] for c in cous) / len(cous)) if cous else 1.0,
            p_[1] if p_ else (logT if pto else 1.0)]
# Version 1.9 (research/ccc90_v19, producer-side only): PRED4_MODEL=<path> (relative to the repository root, or absolute) names
# another file in pred_model4.json's format: the same tree format over the same 25 inputs (P4_NAMES), computed by the same p4_feats
# and evaluated by the same _pred_p; only the file changes. PRED4_MODEL_SHA256=<64 hex> is required with it and must equal the
# sha256 of the file's bytes. A missing or invalid pin, an unreadable file, a sha256 mismatch, malformed JSON, features != P4_NAMES,
# stage != 'pre', a malformed tree (checked node by node: children after their parent, feature index in range, finite thresholds
# and leaf values, |init| + |lr| * sum of max |leaf| <= 700, so that no input can make _pred_p fail later) or a failed probe ->
# a warning on stderr and in the start line, and data/pred_model4.json is loaded exactly as in 1.8 (if that fails too, the 1.5
# model decides, as in 1.8). PRED4_MODEL unset or empty -> 1.8's code path. The start line (with TELEMETRY2) gets pred4_model_path
# (the file pred4 uses; null when pred4 is not in use), pred4_model_override (true only when the named file is in use) and
# pred4_model_fallback_reason (null, or why the named file is not used); pred_model4_sha256 is the sha256 of the bytes in use.
_P4_INFO = {'path': None, 'override': False, 'reason': None}
class _P4Bad(Exception): pass
def _p4_tree_ok(m):
    """raise _P4Bad unless every tree of m can be walked by _pred_p for every input vector of 25 numbers"""
    import math
    fin = lambda v: type(v) in (int, float) and math.isfinite(v)
    if not (fin(m.get('init')) and fin(m.get('lr')) and isinstance(m.get('trees'), list) and m['trees']):
        raise _P4Bad('init / lr / trees missing or not finite')
    bound = abs(m['init'])
    for j, t in enumerate(m['trees']):
        if not (isinstance(t, list) and len(t) == 5 and all(isinstance(a, list) for a in t)): raise _P4Bad(f'tree {j}: not [L, R, F, Th, V]')
        L, R, F, Th, V = t; n = len(L)
        if n == 0 or any(len(a) != n for a in t): raise _P4Bad(f'tree {j}: list lengths differ')
        vmax = 0.0
        for i in range(n):
            if type(L[i]) is int and L[i] == -1:
                if not fin(V[i]): raise _P4Bad(f'tree {j} node {i}: leaf value not finite')
                vmax = max(vmax, abs(V[i]))
            elif not (type(L[i]) is int and type(R[i]) is int and i < L[i] < n and i < R[i] < n and type(F[i]) is int
                      and 0 <= F[i] < len(P4_NAMES) and fin(Th[i])):
                raise _P4Bad(f'tree {j} node {i}: bad split node')
        bound += abs(m['lr']) * vmax
    if not bound <= 700: raise _P4Bad('score bound > 700')
def _p4_override(alt):
    """version 1.9: the model PRED4_MODEL names, or None (after a warning) when it must not be used"""
    import math, re
    try:
        want = os.environ.get('PRED4_MODEL_SHA256', '').strip().lower()
        if not re.fullmatch(r'[0-9a-f]{64}', want): raise _P4Bad('PRED4_MODEL_SHA256 missing or not 64 hex digits')
        try:
            with open(alt if os.path.isabs(alt) else os.path.join(_HERE, '..', alt), 'rb') as fb: raw = fb.read()
        except Exception as ex: raise _P4Bad(f'file unreadable ({type(ex).__name__})')
        h = hashlib.sha256(raw).hexdigest()
        if h != want: raise _P4Bad(f'sha256 mismatch (file {h}, pinned {want})')
        try: m = json.loads(io.TextIOWrapper(io.BytesIO(raw)).read())   # same decoding as _jload / json.load(open(path))
        except Exception: raise _P4Bad('malformed JSON')
        if not isinstance(m, dict): raise _P4Bad('not a JSON object')
        if m.get('features') != P4_NAMES: raise _P4Bad('features != the 25 pred4 inputs (missing, extra or reordered)')
        if m.get('stage') != 'pre': raise _P4Bad("stage != 'pre'")
        _p4_tree_ok(m)
        q = _pred_p(m, p4_feats('L87_s10a4b18c65_0000', [8, -22, 36], 1500.0, {'8 -22'}, {'8 -22': (True, 3.2), '8 -22 -36': (False, 1.0)}, [1, 0]))
        if not (0.0 <= q <= 1.0 and math.isfinite(q)): raise _P4Bad('probe p not in [0, 1]')
    except Exception as ex:
        why = str(ex) if isinstance(ex, _P4Bad) else f'error ({type(ex).__name__})'
        try: _P4_INFO['reason'] = why[:200]; print(f'ccc90 warning: PRED4_MODEL={alt[:200]} not used: {why}; falling back to data/pred_model4.json', file=sys.stderr, flush=True)
        except Exception: pass
        return None
    _P4_INFO.update(path=alt, override=True)
    if TELEMETRY: _TEL_SHA['pred_model4.json'] = h
    return m
def _load_pred4():
    if PRED is None or PRED.get('stage') != 'pre' or os.environ.get('PRED4', '1') == '0': return None
    if os.environ.get('PRED4_MODEL', ''):                        # version 1.9; unset or empty -> 1.8 below
        m = _p4_override(os.environ['PRED4_MODEL'])
        if m is not None: return m
    try:
        import math
        m = _jload(os.path.join(_HERE, '..', 'data', 'pred_model4.json'))
        if m.get('features') != P4_NAMES or m.get('stage') != 'pre': return None
        q = _pred_p(m, p4_feats('L87_s10a4b18c65_0000', [8, -22, 36], 1500.0, {'8 -22'}, {'8 -22': (True, 3.2), '8 -22 -36': (False, 1.0)}, [1, 0]))
        return m if 0.0 <= q <= 1.0 and math.isfinite(q) else None
    except Exception:
        return None
PRED4 = _load_pred4()
if PRED4 is not None and not _P4_INFO['override']: _P4_INFO['path'] = 'data/pred_model4.json'   # version 1.9 (log field only)
elif PRED4 is None and os.environ.get('PRED4_MODEL', '') and _P4_INFO['reason'] is None:
    _P4_INFO['reason'] = 'pred4 not in use (PREDICT=0, PRED4=0 or no pre model)'
P4_GATE = os.environ.get('PRED4_ENC_GATE', '1') != '0'
def _lg(p): import math; p = min(max(p, 1e-6), 1 - 1e-6); return math.log(p / (1 - p))
def _sg(z): import math; return 1 / (1 + math.exp(-max(-50.0, min(50.0, z))))
def calibrate(hist, p):
    """(q, b, ok): calibrated p, the logit shift, and False when the guard holds the split back (version 1.5)"""
    import math
    if not hist: return p, 0.0, True
    n = len(hist); Y = sum(h[1] for h in hist); Pm = sum(h[0] for h in hist) / n
    b = max(-PRED_B, min(PRED_B, _lg((Y + PRED_A * Pm) / (n + PRED_A)) - _lg(Pm))); ok = True
    if n >= PRED_W:
        base = (Y + 1) / (n + 2); cl = lambda q, y: -math.log(min(max(q if y else 1 - q, 1e-4), 1.0))
        lm = sum(cl(h[2], h[1]) for h in hist) / n; lc = sum(cl(base, h[1]) for h in hist) / n
        ok = lm <= lc + PRED_M
    return _sg(_lg(p) + b), b, ok
TRIM_MAX = int(os.environ.get('TRIM_MAX', str(3 << 30))); MARGIN = 90

def say(*a): print(time.strftime('%H:%M:%S'), *a, flush=True)
def left(): return (DEADLINE - time.time()) if DEADLINE else 1e18
def key(cube): return ' '.join(map(str, cube))
# Version 1.10 (producer-side only; nothing here is trusted): a state joined by ccc_merge.py before its fix could list one open cube
# many times (a shard that owned no roots was read as owning every cube, and the joined open list was never de-duplicated), or list a
# cube that a shard had already split or closed. 'Every N-th of the sorted open list' then gave every shard the same roots, and all
# N shards attempted the same cubes. At start the open list is normalised: one entry per cube (the first, order kept), no cube that
# lies on or under a closed cube (the stitch stops at a closed cube), and no split cube whose two sub-cubes are both accounted for
# (open, closed, under a closed cube, or split with both of theirs accounted for). A split cube whose sub-cubes are not all
# accounted for stays on the list, so the run re-attempts it exactly as 1.9 would and the stitch never meets a hole that 1.9 would
# not have met. A list that changes is saved and logged as {'event': 'open_normalized', 'before', 'after'}; an unchanged list is
# not touched (no log line, no save), so a run without such entries is 1.9 byte for byte. OPEN_NORMALIZE=0 skips the step (= 1.9).
OPEN_NORMALIZE = os.environ.get('OPEN_NORMALIZE', '1') != '0'
def normalize_open(opn, splits, done):
    """version 1.10: the open list without repeats, without cubes on or under a closed cube, and without split cubes whose
    sub-cubes are accounted for (see above)"""
    ks = {key(c) for c in opn}; memo = {}
    def under_done(c): return any(key(c[:n]) in done for n in range(len(c) + 1))
    def ok(c):                                                     # cube c is settled even if it is not itself kept on the list
        k = key(c)
        if k not in memo:
            memo[k] = False                                        # (a cube cannot lie below itself; guard only)
            memo[k] = under_done(c) or k in ks or (k in splits and sub(c))
        return memo[k]
    def sub(c): x = splits[key(c)]; return ok(c + [x]) and ok(c + [-x])
    out, seen = [], set()
    for c in opn:
        k = key(c)
        if k in seen or under_done(c) or (k in splits and sub(c)): continue
        seen.add(k); out.append(c)
    return out
def rv(b, p):
    x = 0; s = 0
    while True:
        c = b[p]; p += 1; x |= (c & 0x7f) << s; s += 7
        if c < 0x80: return x, p
def wv(x, out):
    while x >= 0x80: out.append((x & 0x7f) | 0x80); x >>= 7
    out.append(x)
def enc(l): return 2 * abs(l) + (1 if l < 0 else 0)
def jsave(p, o):
    with open(p + '.tmp', 'w') as fo: json.dump(o, fo); fo.flush(); os.fsync(fo.fileno())
    os.replace(p + '.tmp', p)
def append_line(p, obj):
    lead = ''
    if os.path.exists(p) and os.path.getsize(p) > 0:
        with open(p, 'rb') as fi:
            fi.seek(-1, os.SEEK_END)
            if fi.read(1) != b'\n': lead = '\n'
    with open(p, 'a') as fo: fo.write(lead + json.dumps(obj) + '\n'); fo.flush(); os.fsync(fo.fileno())

# ---------------------------------------------------------------- items
def load_items(state, tag, seed_path):
    p = os.path.join(state, 'items.jsonl')
    if not os.path.exists(p):
        seed = []; got = set()
        for sp in (seed_path.split(',') if seed_path else []):
            for l in open(sp, 'rb'):
                try: o = json.loads(l)
                except ValueError: continue                 # a line torn by a kill
                its = o.get('items', o.get('lazy')) if isinstance(o, dict) else None     # lazy_partial / lazy_ckpt lines
                if isinstance(its, list) and o.get('tag') == tag:
                    for x in its:
                        kk = (x['kind'], tuple(x['W']))
                        if kk not in got: got.add(kk); seed.append(x)   # a repeat (two searches) is kept once
        append_line(p, {'items': seed, 'from': f'seed {seed_path}', 'time': round(time.time())})
    items = []
    for l in open(p, 'rb'):
        try: o = json.loads(l)
        except ValueError: continue                     # a line torn by a kill: those items are found again
        items += o['items']
    return items

def violated(E, M, mdl, per_iter=60):
    """the items a model violates: the rule of cegar91.run and grun90.search, unchanged"""
    np, nx = C.np, C.nx
    adj = [k for k, l in E.items() if l is True or (not isinstance(l, bool) and l in mdl)]
    am = [0] * 24
    for u, v in adj: am[u] |= 1 << v; am[v] |= 1 << u
    C.need(all(am[u] & am[v] == 0 for u, v in adj), 'triangle in a model')
    g = nx.Graph(); g.add_nodes_from(range(24)); g.add_edges_from(adj); new = []
    for clq in nx.find_cliques(nx.complement(g)):
        if len(clq) >= 9:
            new.append({'kind': 9, 'W': sorted(clq)[:9]})
            if len(new) >= per_iter: break
    cnt = np.zeros(len(M), dtype=np.int16)
    for v in range(24): cnt += (((M >> v) & 1) * np.bitwise_count(M & np.uint32(am[v]))).astype(np.int16)
    cnt //= 2; bad = np.nonzero(cnt < 12)[0]
    for idx in bad[np.argsort(cnt[bad], kind='stable')][:per_iter]:
        mk = int(M[idx]); new.append({'kind': 12, 'W': [v for v in range(24) if mk >> v & 1]})
    return new, sorted(adj)

# ---------------------------------------------------------------- cubes
def candidates(f, cnf, E):
    """the edge variables, and (version 6, tight iso8 profile) the variables d_T(k) >= 8 of the isolated S vertices,
    read off the iso8 clauses (not dX[k][8] or kv or kw or not vw)"""
    cand = sorted(l for l in E.values() if not isinstance(l, bool))
    s = f['s']; T = list(range(s, 24)); ev = set(cand); d8 = set()
    if ENC_LABEL in ('v6', 'v7', 'v9') and f['b'] == 3 * (len(T) - 8):     # v9 has v7's iso8 clauses, in the same place
        deg = [0] * s
        for u, v in f['h_edges']: deg[u] += 1; deg[v] += 1
        for k in (k for k in range(s) if deg[k] == 0):
            u, w = T[0], T[1]; want = {E[k, u], E[k, w], -E[min(u, w), max(u, w)]}
            for cl in cnf.clauses:
                if len(cl) == 4 and want <= set(cl):
                    (d,) = set(cl) - want
                    if d < 0 and -d not in ev: d8.add(-d)
                    break
    return cand + sorted(d8), sorted(d8)

def best_split(s, prefix, cand):
    """the candidate variable whose two sides propagate most below `prefix` (product of the two counts), or None;
    s is a Minisat22 holding the formula"""
    ok, base = s.propagate(assumptions=prefix)
    if not ok: return None
    fixed = {abs(l) for l in base}; best = None
    for x in cand:
        if x in fixed: continue
        ok1, p1 = s.propagate(assumptions=prefix + [x]); ok0, p0 = s.propagate(assumptions=prefix + [-x])
        if not ok1 or not ok0: continue
        sc = (len(p1) - len(base) + 1) * (len(p0) - len(base) + 1)
        if best is None or sc > best[1]: best = (x, sc)
    return best[0] if best else None

def lookahead(clauses, prefix, cand):
    s = Solver(name='minisat22', bootstrap_with=clauses)
    try: return best_split(s, prefix, cand)
    finally: s.delete()

def initial_tree(clauses, cand, depth):
    leaves = []; splits = {}; s = Solver(name='minisat22', bootstrap_with=clauses)
    def rec(prefix, d):
        ok, _ = s.propagate(assumptions=prefix)
        x = best_split(s, prefix, cand) if ok and d < depth else None
        if x is None: leaves.append(prefix); return
        splits[key(prefix)] = x
        rec(prefix + [x], d + 1); rec(prefix + [-x], d + 1)
    try: rec([], 0)
    finally: s.delete()
    return leaves, splits

# ---------------------------------------------------------------- one cube with the external solver
def ext_cube(clauses, nv, cube, work, timeout, segpath):
    """('UNSAT', info) with the segment written to segpath; ('SAT', model set); ('TIMEOUT', None)"""
    true = set(cube); false = {-l for l in cube}; Denc = [enc(-l) for l in cube]
    cmap = [0]; empty_from = None
    fc = os.path.join(work, 'cube.cnf'); pr = os.path.join(work, 'cube.lrat'); tr = pr + '.trim'
    for x in (fc, pr, tr):
        if os.path.exists(x): os.remove(x)
    lines = []
    for i, cl in enumerate(clauses, 1):
        if any(l in true for l in cl): continue
        red = [l for l in cl if l not in false]
        if not red: empty_from = i; break
        cmap.append(i); lines.append(' '.join(map(str, red)) + ' 0\n')
    t0 = time.time(); buf = bytearray()
    if empty_from is not None:                                         # D_c in one step from a clause of F
        buf.append(0x61); wv(1, buf)
        for v in Denc: wv(v, buf)
        buf.append(0); wv(2 * empty_from, buf); buf.append(0)
        with open(segpath + '.tmp', 'wb') as fo: fo.write(lzma.compress(bytes(buf), preset=1)); fo.flush(); os.fsync(fo.fileno())
        os.replace(segpath + '.tmp', segpath)
        return 'UNSAT', {'n': 1, 'D': 1, 'F_clauses': len(clauses), 'cad_seconds': 0.0, 'trim_bytes': 0, 'falsified_clause': empty_from}
    with open(fc, 'w') as fo: fo.write(f'p cnf {nv} {len(lines)}\n'); fo.writelines(lines)
    del lines
    try:
        cp = subprocess.run([CAD, '-q', '--lrat=true', '--binary=true'] + CAD_OPTS + [fc, pr], capture_output=True, text=True,
                            env={}, timeout=timeout)
    except subprocess.TimeoutExpired:
        _t2_lrat(pr)                                                   # version 1.8: log field only
        for x in (fc, pr):
            if os.path.exists(x): os.remove(x)
        return 'TIMEOUT', None
    cad_s = time.time() - t0
    if cp.returncode == 10:
        mdl = set(l for l in cube if l > 0)
        for line in cp.stdout.splitlines():
            if line.startswith('v '): mdl.update(int(x) for x in line[2:].split() if int(x) > 0 and -int(x) not in true)
        for x in (fc, pr):
            if os.path.exists(x): os.remove(x)
        return 'SAT', mdl
    C.need(cp.returncode == 20, ('external CaDiCaL failed', cp.returncode, cp.stderr[-200:]))
    os.remove(fc); _t2_lrat(pr)                                        # version 1.8: log field only
    tp = subprocess.run([TRIM, '-q', '--no-check', pr, tr], capture_output=True, env={})
    C.need(tp.returncode == 0 and os.path.exists(tr), ('lrat-trim failed', tp.returncode))
    os.remove(pr); b = open(tr, 'rb').read(); os.remove(tr)
    nc = len(cmap) - 1; idmap = {}; alive = set(); p = 0; j = 0; last = None
    while p < len(b):
        t = b[p]; p += 1
        if t == 0x61:
            i, p = rv(b, p); i >>= 1; lits = []; hints = []
            while True:
                v, p = rv(b, p)
                if v == 0: break
                lits.append(v)
            while True:
                v, p = rv(b, p)
                if v == 0: break
                hints.append(v)
            j += 1; idmap[i] = j; alive.add(j); last = (j, not lits)
            buf.append(0x61); wv(j, buf)
            for v in lits: wv(v, buf)
            for v in Denc: wv(v, buf)
            buf.append(0)
            for h in hints:
                C.need(not h & 1, 'a RAT hint')
                hid = h >> 1
                wv(2 * cmap[hid] if hid <= nc else 2 * idmap[hid] + 1, buf)   # even: a clause of F; odd: own clause
            buf.append(0)
        elif t == 0x64:
            ids = []
            while True:
                v, p = rv(b, p)
                if v == 0: break
                hid = v >> 1
                if hid <= nc: continue                                  # F's clauses stay whole for the next cube
                ids.append(idmap[hid]); alive.discard(idmap[hid])
            if ids:
                buf.append(0x64)
                for x in ids: wv(x, buf)
                buf.append(0)
        else:
            raise ValueError(f'unknown byte {t} in the binary LRAT proof')
    C.need(last is not None and last[1], 'the proof does not end with the empty clause')
    alive.discard(last[0])
    if alive:
        buf.append(0x64)
        for x in sorted(alive): wv(x, buf)
        buf.append(0)
    with open(segpath + '.tmp', 'wb') as fo: fo.write(lzma.compress(bytes(buf), preset=1)); fo.flush(); os.fsync(fo.fileno())
    os.replace(segpath + '.tmp', segpath)
    return 'UNSAT', {'n': j, 'D': last[0], 'F_clauses': len(clauses), 'cad_seconds': round(cad_s, 1), 'trim_bytes': len(b)}

# ---------------------------------------------------------------- stitch
def stitch(n, tree, state, outp):
    """segments renumbered after F's n clauses (segment clause x of the i-th closed cube -> base_i + x), then the
    cube tree resolved bottom up to the empty clause; returns the number of cubes"""
    done = tree['done']; splits = {k: v for k, v in tree['splits'].items()}; D = {}; base = n; order = []
    def walk(prefix):
        k = key(prefix)
        if k in done: order.append(prefix); return
        C.need(k in splits, ('the cube tree has a hole at', prefix))
        x = splits[k]; walk(prefix + [x]); walk(prefix + [-x])
    walk([])
    with open(outp, 'wb') as out:
        for cube in order:
            info = done[key(cube)]; b = lzma.decompress(open(os.path.join(state, info['seg']), 'rb').read())
            C.need(info['F_clauses'] <= n, 'a segment was made from a formula that is not a prefix')
            p = 0; buf = bytearray(); off = base
            while p < len(b):
                t = b[p]; p += 1
                if t == 0x61:
                    x, p = rv(b, p); buf.append(0x61); wv(2 * (off + x), buf)
                    while True:
                        v, p = rv(b, p); wv(v, buf)
                        if v == 0: break
                    while True:
                        v, p = rv(b, p)
                        if v == 0: buf.append(0); break
                        wv(v if not v & 1 else 2 * (off + (v >> 1)), buf)
                else:
                    buf.append(0x64)
                    while True:
                        v, p = rv(b, p)
                        if v == 0: buf.append(0); break
                        wv(2 * (off + v), buf)
                if len(buf) > 1 << 24: out.write(buf); buf = bytearray()
            out.write(buf); D[key(cube)] = off + info['D']; base = off + info['n']; del b
        nxt = [base + 1]
        def resolve(prefix):
            k = key(prefix)
            if k in D: return D[k]
            x = splits[k]; a = resolve(prefix + [x]); bb = resolve(prefix + [-x])
            ni = nxt[0]; nxt[0] += 1; buf = bytearray(); buf.append(0x61); wv(2 * ni, buf)
            for l in prefix: wv(enc(-l), buf)
            buf.append(0); wv(2 * a, buf); wv(2 * bb, buf); buf.append(0)
            buf.append(0x64); wv(2 * a, buf); wv(2 * bb, buf); buf.append(0); out.write(buf)
            D[k] = ni
            return ni
        resolve([])
    return len(order)

def cake_slot(path):
    fd = os.open(path, os.O_RDWR | os.O_CREAT | os.O_NOFOLLOW | os.O_CLOEXEC, 0o600); fcntl.flock(fd, fcntl.LOCK_EX); return fd

# ---------------------------------------------------------------- main
def main():
    fpath, tag, state, outdir = sys.argv[1:5]; seed_path = sys.argv[5] if len(sys.argv) > 5 else None
    os.makedirs(state, exist_ok=True); os.makedirs(outdir, exist_ok=True); work = os.path.join(state, 'work')
    os.makedirs(work, exist_ok=True)
    f = json.load(open(fpath))[tag]; logp = os.path.join(state, 'log.jsonl')
    items = load_items(state, tag, seed_path); seen = set()
    for x in items:
        kk = (x['kind'], tuple(x['W'])); C.need(kk not in seen, ('a saved item repeats', kk)); seen.add(kk)
    pool, cnf, E = C.build(f)
    for x in items: cnf.extend(C.lazy_clauses(x, E, pool))
    treep = os.path.join(state, 'tree.json')
    tree = json.load(open(treep)) if os.path.exists(treep) else None
    cand, d8 = candidates(f, cnf, E)
    append_line(logp, {'event': 'start', 'time': round(time.time()), 'pid': os.getpid(), 'items': len(items),
                       'clauses': len(cnf.clauses), 'deadline': DEADLINE, **_tel_start(), **_t2_start(outdir)})
    if tree is None:
        t0 = time.time(); leaves, splits = initial_tree(cnf.clauses, cand, DEPTH0)
        tree = {'tag': tag, 'encoder': ENC_LABEL, 'open': leaves, 'splits': splits, 'done': {}, 'conf': {}, 'seq': 0, 'depth0': DEPTH0}
        jsave(treep, tree)
        append_line(logp, {'event': 'cubes', 'n': len(leaves), 'depth': DEPTH0, 'd8': d8, 'seconds': round(time.time() - t0, 1)})
        say(f'{tag}: {len(leaves)} cubes (depth {DEPTH0}; {len(cand)} candidates, {len(d8)} of them d_T >= 8) in {time.time() - t0:.0f} s')
    C.need(tree['tag'] == tag and tree['encoder'] == ENC_LABEL, 'the state folder belongs to another formula or encoder')
    # CUBE_SHARD=i/N (version 1.2): work only on the open cubes this shard owns (every N-th of the open list sorted by key
    # when the shard first started, and all their sub-cubes), then exit 4 without stitching; ccc_merge.py joins the shards.
    shard = os.environ.get('CUBE_SHARD', ''); mine = None
    if OPEN_NORMALIZE:                                             # version 1.10 (see "Version 1.10" above)
        _o = normalize_open(tree['open'], tree['splits'], tree['done'])
        if len(_o) != len(tree['open']):
            append_line(logp, {'event': 'open_normalized', 'before': len(tree['open']), 'after': len(_o), 'time': round(time.time())})
            say(f'{tag}: open list normalised: {len(tree["open"])} -> {len(_o)} entries'); tree['open'] = _o; jsave(treep, tree)
    if shard:
        si, sn = map(int, shard.split('/')); C.need(0 <= si < sn, ('bad CUBE_SHARD', shard))
        if 'shard' not in tree:
            roots = sorted(key(c) for c in tree['open'])
            tree['shard'] = {'i': si, 'N': sn, 'roots': [k for j, k in enumerate(roots) if j % sn == si]}; jsave(treep, tree)
        C.need(tree['shard']['i'] == si and tree['shard']['N'] == sn, 'the state folder belongs to another shard')
        mine = set(tree['shard']['roots']); lens = sorted({len(k.split()) if k else 0 for k in mine})
        append_line(logp, {'event': 'shard', 'i': si, 'N': sn, 'roots': len(mine), 'time': round(time.time())})
    def is_mine(c): return mine is None or any(key(c[:n]) in mine for n in lens if n <= len(c))
    M = C.masks12(); sol = Solver(name='cadical195', bootstrap_with=cnf.clauses)
    def add(new, note):
        for x in new:
            kk = (x['kind'], tuple(x['W']))
            C.need(kk not in seen, 'a lazy constraint was violated after it was added'); seen.add(kk)
            for cl in C.lazy_clauses(x, E, pool): sol.add_clause(cl); cnf.append(cl)
        items.extend(new); append_line(os.path.join(state, 'items.jsonl'), {'items': new, 'from': note, 'time': round(time.time())})
    def stop(why):
        append_line(logp, {'event': 'stop', 'why': why, 'time': round(time.time()), 'items': len(items),
                           'open': len(tree['open']), 'done': len(tree['done']), **_t2_end()})
        say(f'stopped ({why}); {len(tree["done"])} cubes closed, {len(tree["open"])} open, {len(items)} items'); sys.exit(3)
    def original(cube, edges):
        jsave(os.path.join(state, 'ORIGINAL_MODEL_FOUND.json'), {'tag': tag, 'cube': cube, 'edges': edges})
        append_line(logp, {'event': 'ORIGINAL_MODEL_FOUND', 'cube': key(cube), 'time': round(time.time()), **_t2_end()})
        append_line(os.path.join(outdir, 'results.jsonl'), {'status': 'ORIGINAL_MODEL_FOUND', 'tag': tag, 'edges': edges, 'cube': cube,
                    's': f['s'], 'a': f['a'], 'b': f['b'], 'c': f['c'], 'h_index': f['h_index'], 'encoder': ENC_LABEL})
        say('ORIGINAL_MODEL_FOUND'); sys.exit(2)
    timed_out, predicted = set(), set()
    import collections; hist = collections.deque(maxlen=max(1, PRED_W))   # version 1.5: (shipped p, timed out, calibrated p)
    if os.path.exists(logp):
        for _l in open(logp):
            if '"split"' in _l:
                try: _e = json.loads(_l)
                except ValueError: continue                     # version 1.5: a line torn by a kill is skipped (was: crash)
                if _e.get('event') == 'split': (predicted if 'predicted' in _e else timed_out).add(_e['cube'])
            if '"pp"' in _l:
                try:
                    _e = json.loads(_l)
                    if _e.get('event') in ('closed', 'split') and 'predicted' not in _e:
                        hist.append((float(_e['pp']), _e['event'] == 'split', float(_e.get('pq', _e['pp']))))
                except (ValueError, KeyError, TypeError): pass
    own = PRED['tags'].index(tag) if PRED and tag in PRED['tags'] else -1
    seen4 = {}                                                   # version 1.6: {cube key: (timed out, log10 seconds)}, in log order
    def note4(k4, to4, s4):
        try:
            if PRED4 is not None and ' '.join(k4.split()[:-1]) not in predicted: seen4[k4] = (bool(to4), _p4_ls(s4))
        except Exception: pass
    if PRED4 is not None and os.path.exists(logp):
        for _l in open(logp):
            if '"closed"' in _l or '"split"' in _l:
                try:
                    _e = json.loads(_l)
                    if _e.get('event') == 'closed': note4(_e['cube'], False, _e.get('cad_seconds') or 0)
                    elif _e.get('event') == 'split' and 'predicted' not in _e: note4(_e['cube'], True, _e.get('seconds') or 0)
                except (ValueError, KeyError, TypeError): pass
    def hard_p(cube, dt, used):
        if PRED is None or len(cube) < 2: return None
        par, gp = key(cube[:-1]), key(cube[:-2])
        if par in predicted: return None                       # children of a predicted split always get a real attempt
        o = [t for g, t in PRED['votes'].get(key(cube), []) if g != own]
        v = [(sum(o) / len(o)) if o else -1.0, min(len(o), 20)]
        if PRED.get('stage') == 'pre':
            if PRED4 is not None:                                  # version 1.6; any error -> the version 1.5 model below
                try:
                    import math
                    o4 = o if (not P4_GATE or PRED4.get('votes_encoder') in (None, ENC_LABEL)) else []
                    f4 = p4_feats(tag, cube, EXT_TIMEOUT, timed_out, seen4, o4)
                    q4 = _pred_p(PRED4, f4)
                    if 0.0 <= q4 <= 1.0 and math.isfinite(q4): _t2_x4(f4); return q4
                except Exception: pass
            return pred_p([int(par in timed_out), int(gp in timed_out), len(cube)] + v)
        x = [int(par in timed_out), int(gp in timed_out), len(cube), dt, used / max(1.0, dt)] + v
        return pred_p(x)
    PRE = PRED is not None and PRED.get('stage') == 'pre'          # version 1.4: decide before any attempt, no PySAT probe
    while True:
        idx = next((j for j, c in enumerate(tree['open']) if is_mine(c)), None)
        if idx is None: break
        cube = tree['open'][idx]; k = key(cube); conf = tree['conf'].get(k, CONF0)
        if left() < MARGIN + 60: stop('deadline')
        pfx = {}
        tdec = time.time() if TELEMETRY else None                # version 1.7: decision time of this visit (log field only)
        mark = _t2_mark()                                        # version 1.8: CPU so far (log fields only)
        if PRE:
            # version 1.4: the PySAT probe never shortened a proof (a cube it refuted still needs CaDiCaL's LRAT segment), so with a
            # pre-attempt model it is skipped; predicted-hard cubes are split at once, all others go straight to CaDiCaL
            try: hp = hard_p(cube, 0.0, 0)
            except Exception: hp = None                          # version 1.5: a model error -> plain behaviour, never a crash
            hq, hb, hok = hp, 0.0, True
            if hp is not None and ONLINE:
                try: hq, hb, hok = calibrate(hist, hp)
                except Exception: hq, hb, hok = hp, 0.0, False  # calibration error -> plain behaviour (attempt)
            if hq is not None and hq >= PRED['th'] and hok:
                x = lookahead(cnf.clauses, cube, cand)
                if x is not None:
                    tree['splits'][k] = x; tree['open'][idx:idx + 1] = [cube + [x], cube + [-x]]
                    for c2 in tree['open'][idx:idx + 2]: tree['conf'][key(c2)] = conf
                    tree['conf'].pop(k, None); jsave(treep, tree); predicted.add(k)
                    ev = {'event': 'split', 'cube': k, 'var': x, 'seconds': 0, 'predicted': round(hq, 3)}
                    if ONLINE: ev.update({'p0': round(hp, 3), 'b': round(hb, 3)})
                    ev.update(_tt()); ev.update(_td(tdec)); ev.update(_t2_att(mark, 'pred'))
                    append_line(logp, ev)
                    say(f'cube [{k}] split on {x} (predicted hard before any attempt, p = {hq:.2f})')
                    continue
            # version 1.5: the attempt's log line carries pp (shipped p) and pq (calibrated p) for the on-line window
            pfx = {} if hp is None or not ONLINE else {'pp': round(hp, 4), 'pq': round(hq, 4), **({} if hok else {'held': 1})}
            ans = None; hp = None
        # a. PySAT under the cube's assumptions. PySAT's CaDiCaL cannot be interrupted, so the time cap is a conflict
        #    cap from the measured conflict rate
        if not PRE:
          rate = tree.get('rate', 1000.0); cap = min(PYSAT_CAP, left() - MARGIN)
          budget = max(1000, min(conf, int(rate * cap)))
          c0 = sol.accum_stats().get('conflicts', 0); ps0 = sol.accum_stats() if TEL2 else None; t0 = time.time()
          sol.conf_budget(budget); ans = sol.solve_limited(assumptions=cube)
          dt = time.time() - t0; used = sol.accum_stats().get('conflicts', 0) - c0
          if dt > 5 and used > 0: tree['rate'] = round(0.6 * rate + 0.4 * used / dt, 1)
          if ans is True:
              new, edges = violated(E, M, set(l for l in sol.get_model() if l > 0))
              if not new: original(cube, edges)
              add(new, f'pysat, cube [{k}]')
              append_line(logp, {'event': 'model', 'how': 'pysat', 'cube': k, 'seconds': round(dt, 1), 'conflicts': used,
                                 'new': len(new), 'items': len(items), **_tt(), **_t2_ps(sol, ps0)})
              continue
          append_line(logp, {'event': 'pysat', 'cube': k, 'result': 'UNSAT' if ans is False else 'budget', 'budget': budget,
                             'conflicts': used, 'seconds': round(dt, 1), **_tt(), **_t2_ps(sol, ps0)})
          if ans is None and left() < MARGIN + 60: stop('deadline')
          hp = hard_p(cube, dt, used) if ans is None else None
          if hp is not None and hp >= PRED['th']:
              x = lookahead(cnf.clauses, cube, cand)
              if x is not None:
                  tree['splits'][k] = x; tree['open'][idx:idx + 1] = [cube + [x], cube + [-x]]
                  for c2 in tree['open'][idx:idx + 2]: tree['conf'][key(c2)] = conf
                  tree['conf'].pop(k, None); jsave(treep, tree); predicted.add(k)
                  append_line(logp, {'event': 'split', 'cube': k, 'var': x, 'seconds': 0, 'predicted': round(hp, 3), **_tt(), **_td(tdec), **_t2_att(mark, 'pred')})
                  say(f'cube [{k}] split on {x} (predicted hard, p = {hp:.2f})')
                  continue
        # b. the external proof-writing CaDiCaL on F_c
        to = min(EXT_TIMEOUT, left() - MARGIN)
        if to < min(60, EXT_TIMEOUT): stop('deadline')
        seg = f'seg_{tree["seq"]:04d}.xz'; t0 = time.time()
        st, val = ext_cube(cnf.clauses, pool.top, cube, work, to, os.path.join(state, seg))
        dt = time.time() - t0
        if st == 'UNSAT':
            val.update({'seg': seg, 'pysat': 'skipped' if PRE else ('UNSAT' if ans is False else 'budget')})
            tree['seq'] += 1; tree['done'][k] = val; tree['open'].pop(idx); jsave(treep, tree)
            append_line(logp, {'event': 'closed', 'cube': k, 'seconds': round(dt, 1), **val, **pfx, **_tt(), **_td(tdec),
                               **_t2_att(mark, 'unsat', _t2_ext(to, os.path.join(state, seg)))})
            note4(k, False, val.get('cad_seconds') or 0)
            if pfx: hist.append((pfx['pp'], False, pfx['pq']))
            say(f'cube [{k}] closed: {val["n"]} clauses, CaDiCaL {val["cad_seconds"]} s; {len(tree["done"])} closed, {len(tree["open"])} open')
        elif st == 'SAT':
            new, edges = violated(E, M, val)
            if not new: original(cube, edges)
            add(new, f'external, cube [{k}]'); tree['conf'][k] = conf * GROW; jsave(treep, tree)
            append_line(logp, {'event': 'model', 'how': 'external', 'cube': k, 'seconds': round(dt, 1), 'new': len(new), 'items': len(items),
                               **_tt(), **_td(tdec), **_t2_att(mark, 'sat', _t2_ext(to, None))})
        else:
            if to < EXT_TIMEOUT: stop('deadline')
            x = lookahead(cnf.clauses, cube, cand)
            C.need(x is not None, ('no variable to split', k))
            tree['splits'][k] = x; tree['open'][idx:idx + 1] = [cube + [x], cube + [-x]]
            for c2 in tree['open'][idx:idx + 2]: tree['conf'][key(c2)] = conf
            tree['conf'].pop(k, None); jsave(treep, tree)
            append_line(logp, {'event': 'split', 'cube': k, 'var': x, 'seconds': round(dt, 1), **pfx, **_tt(), **_td(tdec),
                               **_t2_att(mark, 'tmo', _t2_ext(to, None))})
            timed_out.add(k); note4(k, True, round(dt, 1))
            if pfx: hist.append((pfx['pp'], True, pfx['pq']))
            say(f'cube [{k}] split on {x} after {dt:.0f} s')
    sol.delete()
    if mine is not None:
        append_line(logp, {'event': 'shard_done', 'time': round(time.time()), 'done': len(tree['done']), 'open': len(tree['open']), 'items': len(items),
                           **_t2_end()})
        say(f'shard {shard} done: {len(tree["done"])} cubes closed in this state, {len(tree["open"])} open (other shards)'); sys.exit(4)
    # 3. stitch, check, record
    if left() < MARGIN + 600: stop('deadline before the stitch')
    cnfp = os.path.join(outdir, tag + '.cnf'); fresh = C.rebuild(f, items)
    buf = io.StringIO(); fresh.to_fp(buf); data = buf.getvalue().encode('ascii'); del buf
    cnf_sha = hashlib.sha256(data).hexdigest()
    C.need(fresh.clauses == cnf.clauses, 'the rebuilt formula differs from the searched one')
    with open(cnfp, 'wb') as fo: fo.write(data)
    del data
    raw = os.path.join(outdir, tag + '.lrat'); tb = raw + '.trim'; t0 = time.time()
    ncubes = stitch(len(fresh.clauses), tree, state, raw); del fresh
    rawb = os.path.getsize(raw); use = raw; trimb = None
    if rawb < TRIM_MAX:
        tr = subprocess.run([TRIM, '-q', '--no-check', raw, tb], capture_output=True, env={})
        if tr.returncode == 0 and os.path.exists(tb): use = tb; trimb = os.path.getsize(tb)
    data = open(use, 'rb').read(); xz = lzma.compress(data, preset=1); del data
    proofs = os.environ.get('PROOFS', os.path.join(outdir, 'proofs')); os.makedirs(proofs, exist_ok=True)
    dst = os.path.join(proofs, tag + '.lrat.xz')
    with open(dst + '.tmp', 'wb') as fo: fo.write(xz); fo.flush(); os.fsync(fo.fileno())
    os.replace(dst + '.tmp', dst); psha = hashlib.sha256(xz).hexdigest(); pxz = len(xz); del xz
    t1 = time.time(); cmark = _t2_mark()                         # version 1.8: children CPU before cake_lpr (log field only)
    for heap in os.environ.get('CAKE_HEAPS', '2000,4000').split(','):
        lk = cake_slot(os.environ.get('CAKE_LOCK', os.path.join(outdir, '.cake.lock')))
        try:
            ck = subprocess.run([CAKE, f'--CML_HEAP_SIZE={heap}', '--CML_STACK_SIZE=256', cnfp, use], capture_output=True, text=True, env={})
        finally:
            os.close(lk)
        if any(l.startswith('s ') for l in ck.stdout.splitlines()): break
    good = ck.stdout.splitlines() == ['s VERIFIED UNSAT'] and ck.returncode == 0
    n9 = sum(1 for x in items if x['kind'] == 9)
    r = {'status': 'UNSAT', 'tag': tag, 'lazy': items, 'reused_lazy': False, 'proof_by': 'cube-and-conquer',
         'cubes': ncubes, 'cube_splits': len(tree['splits']), 'cube_depth0': tree.get('depth0', DEPTH0), 'floors_added': len(items) - n9,
         'nine_added': n9, 's': f['s'], 'a': f['a'], 'b': f['b'], 'c': f['c'], 'h_index': f['h_index'],
         'pysat_version': pysat.__version__, 'encoder': ENC_LABEL, 'cnf_sha256': cnf_sha, 'cadical_exit': 20,
         'proof_raw_bytes': rawb, 'proof_trim_bytes': trimb if trimb is not None else rawb, 'proof_trimmed': trimb is not None,
         'proof_sha256': psha, 'proof_xz_bytes': pxz, 'stitch_seconds': round(t1 - t0, 1), 'cake_exit': ck.returncode,
         'cake_heap_mb': int(heap), 'cake_seconds': round(time.time() - t1, 1),
         'cake_lpr': 's VERIFIED UNSAT' if good else 'NOT VERIFIED: ' + (ck.stdout + ck.stderr)[-160:],
         'cube_cad_seconds': round(sum(v.get('cad_seconds', 0) for v in tree['done'].values()), 1)}
    if good:
        append_line(os.path.join(outdir, 'results.jsonl'), r)
        for x in (cnfp, raw, tb):
            if os.path.exists(x): os.remove(x)
        append_line(logp, {'event': 'recorded', 'time': round(time.time()), 'proof_xz_bytes': pxz, **_t2_rec(cmark, ncubes, rawb, trimb, tree, state)})
        say(f'{tag} recorded: {ncubes} cubes, stitched proof verified by cake_lpr ({pxz} bytes xz)')
    else:
        append_line(os.path.join(outdir, 'failed_attempts.jsonl'), {k2: v for k2, v in r.items() if k2 != 'lazy'})
        say(f'{tag}: cake_lpr did NOT verify the stitched proof'); sys.exit(1)

if __name__ == '__main__':
    main()
