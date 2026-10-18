"""Repair only this turn's verified documentation encoding error."""
from pathlib import Path
from hashlib import sha256
import ast,json,subprocess
root=Path(__file__).resolve().parents[1];out=root/'benchmarks/results/h5-larger-return-preparation-20261018'
helper=root/'output/record_h5_larger_return_v2.py'
tree=ast.parse(helper.read_text(encoding='utf-8'))
note=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and isinstance(n.targets[0],ast.Name) and n.targets[0].id=='note')
marker='**N4 larger-return candidate review, 2026-10-18:**'
before=subprocess.check_output(['git','show','HEAD:docs/STATUS.md'],cwd=root)
path=root/'docs/STATUS.md';broken=path.read_bytes()
assert broken==before.decode('cp1252').replace(marker,note+'\n'+marker).encode('utf-8')
fixed=before.decode('utf-8').replace(marker,note+'\n'+marker).encode('utf-8')
path.write_bytes(fixed)
record={'error':'The record helper used the Windows default cp1252 encoding for STATUS.md, then wrote UTF-8.',
    'detected_before_stage':True,'broken_sha256':sha256(broken).hexdigest(),'fixed_sha256':sha256(fixed).hexdigest(),
    'verified_exact_difference':'HEAD bytes plus only the intended qualification note; all existing content is byte-identical.'}
(out/'documentation-repair.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8',newline='\n')
(out/'documentation-repair.py').write_bytes(Path(__file__).read_bytes())
print('Existing STATUS bytes restored exactly; only the new note remains.')
