"""Preserve the current requirement preflight without implying a gate pass."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/h4-depth-requirement-preflight-20261016'
checks = json.loads((out/'checks.json').read_bytes())
assert checks['candidate'] == 'aba989e1173f64ca1f273af1c839bd990d8cea05'
assert checks['product_digest'] == '8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88'
assert checks['declared_subset_exact'] and checks['no_imported_or_shared_WASM_memory']
assert checks['full_development_jobs'] == 65 and not checks['H4_complete']
helpers = out/'prepared-followups'
helpers.mkdir(exist_ok=False)
for name in ['prepare_depth_review_helpers.py', 'finish_h5_obstruction_set_pilot.py',
             'prepare_depth_scale_sealer.py', 'h4_depth_scale_report.py']:
    (helpers/name).write_bytes((root/'output'/name).read_bytes())
(out/'record.py').write_bytes(Path(__file__).read_bytes())
inventory = {p.relative_to(out).as_posix(): {'sha256':sha256(p.read_bytes()).hexdigest(),
             'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}
(out/'integrity.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8',newline='\n')

path = root/'docs/RELEASE_READINESS.md'
text = path.read_text(encoding='utf-8')
before = '- Current-build scale and independent checks of every saved SVG/DXF curve for\n'
assert before in text
text = text.replace(before, '''- [Current requirement preflight](../benchmarks/results/h4-depth-requirement-preflight-20261016.md)
  verifies the eleven subset cases, all 65 development jobs, original budgets,
  seeds and physical cores, and the exact current WASM's unshared memory.
  This confirms scope and the threading constraint, not quality or scale.
'''+before)
before = '''- Fresh hosted checks and three-platform package/download verification are
  required for this changed candidate. The earlier `7eba929` package dry run
  does not certify the new executable.
'''
assert before in text
text = text.replace(before, '''- [Current hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38854287845)
  and a [tagless three-platform package dry run](https://github.com/skulitom/Nestbolt/actions/runs/38854620093)
  are underway on `23442be`, which contains the same tested product. Actual
  downloads will be checked from an isolated verifier directory. Publication
  is disabled for this dry run. The earlier `7eba929` package proof remains
  tied to its older executable.
''')
path.write_text(text,encoding='utf-8',newline='\n')

path = root/'BENCHMARKS.md'
before = path.read_bytes()
assert before.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with path.open('a',encoding='utf-8',newline='\n') as stream:
    stream.write('''

## 2026-10-16 — Current depth-build scope and package preflight

[The current requirement preflight](benchmarks/results/h4-depth-requirement-preflight-20261016.md)
verifies all eleven subset cases, the complete 65-job development set, unchanged
60-second budgets/seeds/physical cores and the actual measured WASM memory
declaration. Candidate `aba989e`, product digest
`8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88`,
has one unshared, non-imported memory. No measurement was repeated and no
reserved geometry was opened. The full matrix and conditional scale/export
sequence remain running/pending; this preflight does not close H4.

The next scale sealer is prepared to require both complete scale workflows,
independent checks of all 2,000 exported placements in each browser, and all
four screenshot reviews. A different valid sheet arrangement is assessed by
original-curve fidelity, not assumed byte equality with a previous solver.
The separate common-line pilot's original-archive verifier is also prepared;
its committed measurement remains unopened until H4 measurements finish.

Commit `23442be` is on main. Hosted checks and tagless package dry run
[38854620093](https://github.com/skulitom/Nestbolt/actions/runs/38854620093)
are underway; downloaded packages will be tested from an isolated directory.
No preview tag, release or registry publication is created by this work.
Completed milestone weight remains 45%.
''')
assert path.read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as stream:
    stream.write('\nbenchmarks/results/h4-depth-requirement-preflight-20261016/** -text -whitespace\n')
print('Recorded current preflight and pending checks; no milestone or release change.')
