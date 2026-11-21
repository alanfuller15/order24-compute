# RA9X9 diagnostics / negative controls for model_4_13_9_2.py
import runpy, sys, collections
src = open('model_4_13_9_2.py').read()
# control 1: drop q4/mult filter at the leaves (keep it on Y prefilter) -> what kills leaves?
c1 = src.replace("if not q4ok(fam) or not multok(fam): stats['q4'] += 1; continue", "pass")
c1 = c1.replace("res = full_check(fam)", "res = 'skipped'")
c1 = c1.replace("if not q4ok(Y) or not multok(Y): continue", "pass")
c1 = c1.replace("print(\"time", "import collections as _c\nprint('mult patterns of leaves:', _c.Counter(tuple(sorted(collections.Counter(f).values(), reverse=True)) for f,_ in survivors).most_common(8))\nprint(\"time")
c1 = "import collections\n" + c1
print("== control 1: no q4/mult filters anywhere ==")
exec(compile(c1, 'c1', 'exec'), {'__name__': '__main__'})
