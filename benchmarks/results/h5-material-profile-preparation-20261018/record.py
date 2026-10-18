from pathlib import Path
import json,shutil,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-material-profile-preparation-20261018'
assert json.loads((out/'checks.json').read_bytes())['all_functional_checks_pass']
assert (root/'benchmarks/results/h5-material-profile-pilot-20261018/plan.json').exists()
note='**N4 material-profile candidate preparation, 2026-10-18:** [all 123 optimized tests pass](../benchmarks/results/h5-material-profile-preparation-20261018.md),\nwith all 117 prior tests unchanged. The candidate rejects same-inventory\ntrials whose exact original-geometry profiles prove unchanged charged\nmaterial. It uses the existing validator footprints and preserves every\naccepted geometry/material check. Budgets and coefficients are unchanged;\nprofile work uses the existing vertex charge. Five proofs, 23 witness pairs\nand 47 frozen-CLI checks cover geometry contexts, real gains and an invalid\noverlap; 12 branch outcomes pass another 24 CLI checks. The original failing\nbranch regression is preserved. Strict lint/build, public parity/replay,\nfive harness tests and exact formatted-source reconstruction pass. The\nunchanged 72-outcome method is committed before measurement. No quality,\nintegration or release claim; H2/H5 remain open at 60%.\n'
def append(p,s):
    with p.open('a',encoding='utf-8',newline='\n') as f:f.write(s)
p=root/'docs/STATUS.md';text=p.read_text(encoding='utf-8');needle='**N4 exact-state early-rejection outcome, 2026-10-18:**';assert text.count(needle)==1
p.write_text(text.replace(needle,note+'\n'+needle),encoding='utf-8',newline='\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:append(root/name,'\n\n'+note)
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root);assert (root/'BENCHMARKS.md').read_bytes()==prior
append(root/'BENCHMARKS.md','\n\n## 2026-10-18 — Qualify exact material-profile early rejection\n\n'+note.replace('../benchmarks/','benchmarks/'))
assert (root/'BENCHMARKS.md').read_bytes().startswith(prior)
shutil.copyfile(__file__,out/'record.py');print('Recorded qualified candidate and unchanged pilot scope.')
