"""Bind successful package proof into current readiness, keeping CI/quality open."""
from hashlib import sha256
from pathlib import Path
import json
import subprocess

root = Path(__file__).resolve().parents[1]
out = root/'benchmarks/results/preview-depth-release-dryrun-20261016'
checks = json.loads((out/'checks.json').read_bytes())
assert checks['all_checks_passed'] and checks['dry_run_only'] and checks['release_job_skipped']
assert checks['release_commit'] == '23442be38ee2e881669e753bc405ab3269ff1b39'
for name, row in json.loads((out/'integrity.json').read_bytes()).items():
    data = (out/name).read_bytes()
    assert sha256(data).hexdigest() == row['sha256'] and len(data) == row['bytes']
sequence = root/'output/depth-package-sequence-20261016'
assert (sequence/'completed.json').is_file() and not (sequence/'interruption.json').exists()
(out/'sequence').mkdir()
for path in sequence.iterdir():
    assert path.is_file()
    (out/'sequence'/path.name).write_bytes(path.read_bytes())
(out/'record_readiness.py').write_bytes(Path(__file__).read_bytes())
inventory = {p.relative_to(out).as_posix(): {'sha256':sha256(p.read_bytes()).hexdigest(),
             'bytes':p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}
(out/'sealed-integrity.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8',newline='\n')

path = root/'docs/RELEASE_READINESS.md'
text = path.read_text(encoding='utf-8')
before = '''- [Current hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38854287845)
  and a [tagless three-platform package dry run](https://github.com/skulitom/Nestbolt/actions/runs/38854620093)
  are underway on `23442be`, which contains the same tested product. Actual
  downloads will be checked from an isolated verifier directory. Publication
  is disabled for this dry run. The earlier `7eba929` package proof remains
  tied to its older executable.
'''
after = '''- [All three downloaded packages and the Windows MCPB pass](../benchmarks/results/preview-depth-release-dryrun-20261016.md)
  on `23442be`, which contains the same tested product. Architecture, contents,
  permissions, versions and metadata match; the actual downloaded Windows
  bundle passes import/nest/validation and confinement from an isolated copy.
  Dry-run publication was skipped. The earlier `7eba929` package proof remains
  tied to its older executable.
- [Current hosted checks](https://github.com/skulitom/Nestbolt/actions/runs/38854287845)
  remain in progress. Their completion and current quality/scale confirmation
  are still required before publishing.
'''
assert before in text
path.write_text(text.replace(before,after),encoding='utf-8',newline='\n')

path = root/'docs/STATUS.md'
text = path.read_text(encoding='utf-8')
before = '''waits for a quality pass; hosted checks and package proof remain required. No common-line experiment is
integrated. No preview tag or release exists, and completion stays 45%.
'''
after = '''waits for a quality pass. [All three downloaded packages and the Windows MCPB](../benchmarks/results/preview-depth-release-dryrun-20261016.md)
pass their checks, including actual Windows import/nest/validation/confinement.
Current hosted checks remain in progress. The [requirement preflight](../benchmarks/results/h4-depth-requirement-preflight-20261016.md)
confirms the original scope and unshared WASM memory. No common-line experiment
is integrated. No preview tag or release exists, and completion stays 45%.
'''
assert before in text
path.write_text(text.replace(before,after),encoding='utf-8',newline='\n')

path = root/'BENCHMARKS.md'
before = path.read_bytes()
assert before.startswith(subprocess.check_output(['git','show','HEAD:BENCHMARKS.md'],cwd=root))
with path.open('a',encoding='utf-8',newline='\n') as stream:
    stream.write('''

## 2026-10-16 — Current preview downloads verified

[The depth-build package proof](benchmarks/results/preview-depth-release-dryrun-20261016.md)
passes for commit `23442be` / `0.2.0-alpha.1`. All three native archives have
the expected members, documents, architectures and Unix permissions. Each
platform's runner checks both executable versions. The actual downloaded
Windows CLI/MCP versions and MCPB import, nesting, independent validation,
catalog and file-confinement checks pass locally from an isolated verifier on
CCD1. Its server bytes match the native archive, and checksum/manifest/metadata
agree. Linux/macOS binaries were not executed locally on Windows.

All build and metadata-validation jobs passed in
[38854620093](https://github.com/skulitom/Nestbolt/actions/runs/38854620093);
publication was skipped. No tag, release, attestation or registry publication
was created. Current full quality, scale, exported-curve review and hosted
checks remain required. The measured sources/builds remain frozen and the
completed milestone total stays 45%. Release notes now also distinguish the
native/MCP preview from the hosted browser, which remains on v0.1.0.
''')
assert path.read_bytes().startswith(before)
with (root/'.gitattributes').open('a',encoding='utf-8',newline='\n') as stream:
    stream.write('\nbenchmarks/results/preview-depth-release-dryrun-20261016/** -text -whitespace\n')
print('Current downloaded-package proof recorded; quality, scale and CI remain open.')
