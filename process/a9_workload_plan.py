#!/usr/bin/env python3
"""Read-only deterministic A9 replay scheduler; NOT a proof checker.

Mirrors a9check.py's ordered UNSAT occurrence list and full input digest.
Writes a complete, disjoint hypothetical schedule for NEXT-GENERATION runs.
Never prints a verified/covered verdict and does not modify A9 production data.
"""
from __future__ import annotations

import argparse
import hashlib
import heapq
import json
import math
import pathlib

SCHEMA = 'a9-workload-plan-v1-experimental'


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_records(paths):
    """Reproduce the final verifier's input digest and UNSAT occurrence order."""
    h = hashlib.sha256()
    unsat, other = [], []
    for file_index, path in enumerate(paths):
        raw = pathlib.Path(path).read_bytes()
        h.update(hashlib.sha256(raw).digest())
        for line_index, line in enumerate(raw.splitlines(keepends=True), start=1):
            if not line.strip():
                continue
            record = json.loads(line)
            status = record.get('status')
            if status != 'UNSAT':
                other.append((file_index, line_index, status))
                continue
            i = len(unsat)
            unsat.append(dict(
                index=i,
                file_index=file_index,
                line=line_index,
                record_sha256=sha(line),
                cnf_sha256=record.get('cnf_sha256'),
                tag=record.get('tag'),
                case=record.get('case'),
                predicted_cost=estimate_cost(record),
            ))
    return h.hexdigest(), unsat, other


def positive(value, default=0.):
    try:
        value = float(value)
        return value if math.isfinite(value) and value >= 0 else default
    except (ValueError, TypeError):
        return default


def estimate_cost(record):
    """Heuristic only. Produces units of predicted relative effort, NOT seconds."""
    cad = positive(record.get('cadical_seconds'))
    cake = positive(record.get('cake_seconds'))
    # A previously observed Cake time is much better than predicting from bytes.
    proof_mib = positive(record.get('proof_bytes')) / (1024 * 1024)
    fallback_cake = 0.25 * proof_mib
    return round(1.0 + cad + (cake if cake > 0 else fallback_cake), 3)


def allocate(unsat, n, mode):
    if n <= 0:
        raise ValueError('parts must be positive')
    if mode == 'striped':
        out = [[] for _ in range(n)]
        for rec in unsat:
            out[rec['index'] % n].append(rec['index'])
        return out
    if mode != 'weighted':
        raise ValueError('mode must be striped or weighted')
    heap = [(0., part) for part in range(n)]
    heapq.heapify(heap)
    out = [[] for _ in range(n)]
    for rec in sorted(unsat, key=lambda r: (-r['predicted_cost'], r['index'])):
        load, part = heapq.heappop(heap)
        out[part].append(rec['index'])
        heapq.heappush(heap, (load + rec['predicted_cost'], part))
    for part in out:
        part.sort()
    return out


def split_chunks(part, unsat, max_records, target_cost):
    if max_records <= 0 or target_cost <= 0:
        raise ValueError('chunk capacities must be positive')
    chunks, cur, load = [], [], 0.
    for i in part:
        cost = unsat[i]['predicted_cost']
        if cur and (len(cur) >= max_records or load + cost > target_cost):
            chunks.append(cur)
            cur, load = [], 0.
        cur.append(i)
        load += cost
    if cur:
        chunks.append(cur)
    return chunks


def validate(plan, paths):
    input_digest, unsat, other = load_records(paths)
    if plan['schema'] != SCHEMA or input_digest != plan['input_digest']:
        raise ValueError('schema/input digest mismatch')
    if len(unsat) != plan['total_unsat']:
        raise ValueError('UNSAT occurrence count changed')
    if plan['other_statuses'] != [list(x) for x in other]:
        raise ValueError('non-UNSAT record accounting changed')
    if plan['records'] != unsat:
        raise ValueError('occurrence identities, costs, or record hashes changed')
    parts = plan['parts']
    if len(parts) != plan['nparts']:
        raise ValueError('wrong number of parts')
    actual = []
    for pidx, part in enumerate(parts):
        if part['part'] != pidx:
            raise ValueError('wrong part id')
        flattened = [i for chunk in part['chunks'] for i in chunk]
        if flattened != part['indices']:
            raise ValueError('chunk mismatch')
        if not all(isinstance(i, int) and 0 <= i < len(unsat) for i in flattened):
            raise ValueError('invalid occurrence index')
        actual += flattened
        expected_load = round(sum(unsat[i]['predicted_cost'] for i in flattened), 3)
        if not math.isclose(part['cost'], expected_load, abs_tol=0.001):
            raise ValueError('wrong cost accounting')
    if sorted(actual) != list(range(len(unsat))):
        raise ValueError('missing or repeated UNSAT occurrence')
    expected = allocate(unsat, plan['nparts'], plan['mode'])
    for pidx, part in enumerate(parts):
        if part['indices'] != expected[pidx]:
            raise ValueError('schedule has been changed')
        if part['chunks'] != split_chunks(part['indices'], unsat, plan['max_records'], plan['target_cost']):
            raise ValueError('chunk schedule has been changed')
    return True


def create_plan(paths, n=32, mode='weighted', max_records=100, target_cost=500.):
    digest, unsat, other = load_records(paths)
    # Encountering a potential counterexample is not an input suitable for certificate planning.
    if any(status == 'MODEL' for _, _, status in other):
        raise ValueError('MODEL record present: do not schedule an UNSAT final claim')
    allocation = allocate(unsat, n, mode)
    parts = []
    for part_id, indices in enumerate(allocation):
        parts.append(dict(
            part=part_id,
            cost=round(sum(unsat[i]['predicted_cost'] for i in indices), 3),
            indices=indices,
            chunks=split_chunks(indices, unsat, max_records, target_cost),
        ))
    plan = dict(schema=SCHEMA, input_digest=digest, files=[str(p) for p in paths],
                total_unsat=len(unsat), other_statuses=[list(x) for x in other],
                records=unsat, nparts=n, mode=mode, max_records=max_records,
                target_cost=target_cost, parts=parts,
                warning='SCHEDULING ONLY: no UNSAT claim and no checkpoint can bypass CakeML.')
    validate(plan, paths)
    return plan


def summary(plan):
    loads = [p['cost'] for p in plan['parts']]
    avg = sum(loads) / len(loads) if loads else 0
    return {
        'mode': plan['mode'], 'input_digest': plan['input_digest'],
        'unsat_occurrences': plan['total_unsat'], 'parts': len(loads),
        'total_chunks': sum(len(p['chunks']) for p in plan['parts']),
        'average_predicted_load': round(avg, 2),
        'max_predicted_load': max(loads, default=0),
        'max_to_average': round(max(loads) / avg, 3) if avg else 0,
        'empty_parts': sum(not p['indices'] for p in plan['parts']),
    }


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('results', nargs='+', help='ordered results.jsonl files, in SAME order as a9check.py')
    ap.add_argument('--mode', choices=['striped', 'weighted'], default='weighted')
    ap.add_argument('--parts', type=int, default=32)
    ap.add_argument('--max-records', type=int, default=100)
    ap.add_argument('--target-cost', type=float, default=500.)
    ap.add_argument('--output', required=True)
    ap.add_argument('--compare', action='store_true', help='compare striped and weighted, using same input data')
    a = ap.parse_args()
    plan = create_plan(a.results, a.parts, a.mode, a.max_records, a.target_cost)
    pathlib.Path(a.output).write_text(json.dumps(plan, sort_keys=True, separators=(',', ':')) + '\n')
    print(json.dumps(summary(plan), sort_keys=True))
    if a.compare:
        other = create_plan(a.results, a.parts, 'striped' if a.mode == 'weighted' else 'weighted', a.max_records, a.target_cost)
        print('comparison: '+json.dumps(summary(other), sort_keys=True))
    print('PLAN ONLY; do not use as a certificate or change current final-run partition semantics.')


if __name__ == '__main__':
    main()
