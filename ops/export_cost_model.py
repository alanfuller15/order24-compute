"""export_cost_model.py PKL OUT.json (manager side; run after opt/cost_build.py, e.g. at the end of opt/retrain.sh).
Writes the cost-to-go model (sklearn GradientBoostingRegressor, squared error) as plain JSON trees so the refill workflow
can evaluate it without sklearn and without unpickling anything: ops/cost_model.json
  {version, kind, features, init, lr, trees: [[left, right, feature, threshold, value], ...], trained, calib}
Evaluation (ops/pool.py, ops/costmodel.py): s = init + lr * sum(value[leaf]); a feature is compared as float32 (as sklearn does).
Producer-side steering only: nothing about soundness depends on it."""
import sys, json, pickle, hashlib, time
pkl, out = sys.argv[1], sys.argv[2]
raw = open(pkl, 'rb').read()
m = pickle.loads(raw)   # the manager's own file (opt/cost_model.pkl), never a downloaded one
assert type(m).__name__ == 'GradientBoostingRegressor' and m.loss == 'squared_error', type(m)
assert m.estimators_.shape[1] == 1
trees = []
for est in m.estimators_[:, 0]:
    t = est.tree_
    trees.append([t.children_left.tolist(), t.children_right.tolist(), t.feature.tolist(),
                  [float(x) for x in t.threshold], [float(v[0][0]) for v in t.value]])
d = {'version': 1, 'kind': 'gbr_log1p_seconds',
     'features': ['parent_to', 'grand_to', 'depth', 'vote', 'n_vote'],
     'init': float(m.init_.constant_[0][0]), 'lr': float(m.learning_rate), 'trees': trees,
     'calib': 2.0, 'source_sha256': hashlib.sha256(raw).hexdigest()}   # deterministic: same pickle -> same bytes (no timestamp)
json.dump(d, open(out, 'w'), separators=(',', ':'))
print(f'{out}: {len(trees)} trees, init {d["init"]:.4f}, lr {d["lr"]}')
