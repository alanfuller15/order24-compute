"""Partition/coverage regressions; no SAT oracle or cached replay results are trusted."""
import contextlib
import io
import gzip
import hashlib
import json
import subprocess
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
import a9check as check


class FakePool:
    def __init__(self, *_): pass
    def __enter__(self): return self
    def __exit__(self, *_): pass
    def imap_unordered(self, fn, jobs):
        for job in reversed(jobs):
            yield fn(job)


class FinalPartitionTests(unittest.TestCase):
    def run_claim(self, records, n, failed=(), mode='leaves'):
        seen = []
        outcomes = []
        p = (4,) * 15
        def replay(job):
            key, r, *_ = job
            seen.append((r['_file'], r['tag']))
            return key, {'pass': r['tag'] not in failed}
        with tempfile.TemporaryDirectory() as d:
            file = Path(d) / 'results.jsonl'
            file.write_text(''.join(json.dumps(r) + '\n' for r in records))
            for k in range(n):
                args = ['a9check', 'gh=' + str(file), d, d, '--final', '--part', f'{k}/{n}', '--partition', mode]
                with patch.object(sys, 'argv', args), \
                     patch.object(check.C, 'profiles', side_effect=lambda c: (p,) if c == 'B' else ()), \
                     patch.object(check.C, 'index_of', side_effect=lambda c, prof: 0 if c == 'B' and prof == p else None), \
                     patch.object(check.mp, 'Pool', FakePool), patch.object(check, 'replay', replay), \
                     patch.object(check, 'tool', return_value='/bin/true'), \
                     contextlib.redirect_stdout(io.StringIO()):
                    try: check.main()
                    except SystemExit as e: outcomes.append(e.code)
        return outcomes, seen

    def record(self, cube, case='B', idx=0, unit=None):
        return dict(status='UNSAT', case=case, idx=idx, prof=[4]*15,
                    cube=cube, unit=unit or [], tag=check.R.tag_of(case, idx, cube),
                    cadical_exit=20, cake_lpr=check.VER)

    def test_every_duplicate_and_extra_replayed_once_and_balanced(self):
        records = [self.record([1]), self.record([-1])] + [self.record([], 'A', 999)]*33
        outcomes, seen = self.run_claim(records, 32)
        self.assertEqual(outcomes, [0]*32)
        self.assertEqual(len(seen), len(records))
        self.assertEqual(sorted(tag for _, tag in seen), sorted(r['tag'] for r in records))
        loads = [len(check.leaf_part(records, k, 32)) for k in range(32)]
        self.assertLessEqual(max(loads)-min(loads), 1)

    def test_conjunction_matches_whole_check(self):
        good = [self.record([1]), self.record([-1])]
        bad_flag = json.loads(json.dumps(good)); bad_flag[0]['cake_lpr'] = 'NOT VERIFIED'
        bad_tag = json.loads(json.dumps(good)); bad_tag[0]['tag'] = 'tampered'
        model = dict(self.record([]), status='MODEL')
        # Complete tree, missing branch, bad flag/tag, model, failed independent replay.
        for records, failures in [(good, ()), (good[:1], ()), (bad_flag, ()), (bad_tag, ()),
                                  (good+[model], ()), (good, (good[0]['tag'],))]:
            with self.subTest(records=records, failures=failures):
                whole, _ = self.run_claim(records, 1, failures, 'profiles')
                parts, _ = self.run_claim(records, 4, failures)
                self.assertEqual(all(x == 0 for x in parts), whole == [0])

    def test_failure_of_foreign_leaf_rejects_its_owner(self):
        records = [self.record([1]), self.record([-1])]
        parts, seen = self.run_claim(records, 4, (records[1]['tag'],))
        self.assertNotEqual(parts[1], 0)
        self.assertEqual(len(seen), 2)
        self.assertFalse(all(x == 0 for x in parts))

    def test_replay_retains_hash_sat_and_exact_certificate_checks(self):
        cnf = b'p cnf 1 2\n1 0\n-1 0\n'
        for match, cad, cake, expected in [(False,20,check.VER,False), (True,10,check.VER,False),
                                            (True,20,'prefix '+check.VER,False), (True,20,check.VER,True)]:
            with self.subTest(match=match,cad=cad,cake=cake), tempfile.TemporaryDirectory() as d:
                r = dict(self.record([]), _label='gh', _file='records', _lazydir=d,
                         cnf_sha256=hashlib.sha256(cnf).hexdigest() if match else 'wrong')
                with gzip.open(Path(d,r['tag']+'.json.gz'),'wt') as f: json.dump([],f)
                calls = [subprocess.CompletedProcess([],cad,b'',b''),
                         subprocess.CompletedProcess([],0,cake+'\n','')]
                with patch.object(check,'rebuild',return_value=cnf), patch.object(check.subprocess,'run',side_effect=calls) as proc:
                    _, result = check.replay((0,r,d,'CAD','CAKE'))
                self.assertEqual(result['pass'],expected)
                self.assertEqual(proc.call_count,0 if not match else (1 if cad != 20 else 2))

    def test_wrapper_fails_closed_before_starting_any_work(self):
        script = Path(__file__).resolve().with_name('a9final.sh')
        with tempfile.TemporaryDirectory() as d:
            result = subprocess.run(['bash', str(script), 'invalid', '4'], cwd=d, capture_output=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertTrue(Path(d, 'exp_out/GATE_FAIL').exists())

    def test_no_union_of_sources_or_incomplete_units(self):
        p = (4,)*15
        pos = dict(self.record([1]), _file='x', _label='one')
        neg = dict(self.record([-1]), _file='y', _label='two')
        self.assertEqual(check.select(p, 'B', {'one':[pos], 'two':[neg]}, ['one','two']), (None, []))
        self.assertEqual(check.select(p, 'B', {'one':[pos,dict(neg, _label='one')]}, ['one']), (None, []))


if __name__ == '__main__':
    unittest.main()
