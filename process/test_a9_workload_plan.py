import copy
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
import a9_workload_plan as P


class WorkloadTests(unittest.TestCase):
    def make(self, d, weights, nfiles=2, with_model=False):
        paths=[]
        for k in range(nfiles):
            f=Path(d)/f'r{k}.jsonl'
            with f.open('w') as out:
                for i in range(k,len(weights),nfiles):
                    # deliberately repeat tags, profiles and hashes: occurrence index MUST stay unique
                    out.write(json.dumps(dict(status='UNSAT',tag='same',case='B',cnf_sha256='same',
                                              cadical_seconds=weights[i]-1,cake_seconds=0))+'\n')
                if with_model and k==0: out.write('{"status":"MODEL","tag":"contradiction"}\n')
            paths.append(str(f))
        return paths

    def test_exhaustive(self):
        with TemporaryDirectory() as d:
            paths=self.make(d,[1+i%7 for i in range(237)],3)
            for n in [1,2,3,10,32,256]:
                for mode in ['striped','weighted']:
                    plan=P.create_plan(paths,n,mode,max_records=6,target_cost=17)
                    self.assertTrue(P.validate(plan,paths))
                    self.assertEqual(P.summary(plan)['unsat_occurrences'],237)
                    self.assertEqual(len(plan['parts']),n)

    def test_duplicates_not_deduplicated(self):
        with TemporaryDirectory() as d:
            paths=self.make(d,[20]*65)
            plan=P.create_plan(paths,32)
            self.assertEqual(len([i for p in plan['parts'] for i in p['indices']]),65)

    def test_tamper_fails_closed(self):
        with TemporaryDirectory() as d:
            paths=self.make(d,list(range(1,41)))
            good=P.create_plan(paths,10,max_records=3,target_cost=15)
            tampered=copy.deepcopy(good)
            tampered['parts'][0]['indices'].append(tampered['parts'][0]['indices'][0])
            with self.assertRaises(ValueError):P.validate(tampered,paths)
            tampered=copy.deepcopy(good)
            tampered['parts'][0]['chunks'].clear()
            with self.assertRaises(ValueError):P.validate(tampered,paths)
            with open(paths[0], 'a') as out: out.write('\n')
            with self.assertRaises(ValueError):P.validate(good,paths)

    def test_model_blocks_final_planning(self):
        with TemporaryDirectory() as d:
            paths=self.make(d,[1,2,3],with_model=True)
            with self.assertRaisesRegex(ValueError,'MODEL'):
                P.create_plan(paths,8)

    def test_determinism(self):
        with TemporaryDirectory() as d:
            paths=self.make(d,[1+i%23 for i in range(400)])
            x=P.create_plan(paths,32,'weighted')
            y=P.create_plan(paths,32,'weighted')
            self.assertEqual(x,y)

    def test_weighted_breaks_cost_collision(self):
        with TemporaryDirectory() as d:
            # Heavy costs cluster at every 32nd occurrence in the file's parsed order.
            # The scheduler operates on the actual loaded occurrence sequence.
            paths=self.make(d,[100 if i % 32 == 11 else 1 for i in range(640)],1)
            old=P.create_plan(paths,32,'striped')
            new=P.create_plan(paths,32,'weighted')
            self.assertLess(P.summary(new)['max_predicted_load'],P.summary(old)['max_predicted_load'] / 3)

if __name__ == '__main__':
    unittest.main()
