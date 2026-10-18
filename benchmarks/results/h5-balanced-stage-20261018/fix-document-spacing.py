from pathlib import Path
from hashlib import sha256
import json,subprocess,shutil
root=Path(__file__).resolve().parents[1]
out=root/'benchmarks/results/h5-balanced-stage-20261018'
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=root).decode().strip()
assert head.startswith('deb1efe')
prior=subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root)
benchmark=root/'BENCHMARKS.md';assert benchmark.read_bytes()==prior
with benchmark.open('a',encoding='utf-8',newline='\n') as f:
    f.write('These four observations retain their original 60-second searches; none was repeated.\n')
for name in ['docs/PLAN_V1_1.md','docs/V1_1_RESEARCH.md']:
    p=root/name;p.write_text(p.read_text(encoding='utf-8').rstrip()+'\n',encoding='utf-8',newline='\n')
assert benchmark.read_bytes().startswith(prior)
review={'original_commit':head,'initial_review':'git diff --cached --check reported new blank lines at EOF in BENCHMARKS.md, docs/PLAN_V1_1.md and docs/V1_1_RESEARCH.md.',
    'sequence':'The shell review failed but the next separately issued commit still ran. This follow-up corrects presentation without altering saved measurements.',
    'correction':'Remove terminal blank lines from the two editable plan documents; append a factual retention sentence to BENCHMARKS.md so all earlier bytes remain intact.',
    'previous_benchmark_sha256':sha256(prior).hexdigest(),'benchmark_previous_bytes_preserved':True,
    'measured_data_changed':False,'new_searches':0}
(out/'staging-review.json').write_text(json.dumps(review,indent=2)+'\n',encoding='utf-8',newline='\n')
shutil.copyfile(__file__,out/'fix-document-spacing.py')
print('Presentation corrected; every previous benchmark-log byte preserved')
