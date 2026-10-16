"""Record downloaded package verification for the integrated score candidate."""
from hashlib import sha256
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
folder = 'preview-score-release-dryrun-20261016'
out = root / 'benchmarks/results' / folder
checks = json.loads((out / 'checks.json').read_bytes())
assert checks['all_checks_passed']
assert checks['release_commit'] == '7eba929420d218d04169c1fdf24481051c8afae5'
table = '\n'.join(f"| {r['target']} | {r['bytes']:,} | `{r['sha256']}` |" for r in checks['archives'])
report = f'''# Integrated preview package verification — 2026-10-16

**All three downloaded native packages and the Windows MCPB pass.**
[Dry-run workflow 38840747735]({checks['workflow_url']}) built candidate
`7eba929`, version `0.2.0-alpha.1`. All build and metadata-validation jobs
succeeded; the publication job was skipped. No tag, release or registry entry
was created by this dry run.

[Checks]({folder}/checks.json) verify the six expected archive entries,
architectures, executable permissions on Unix and exact documentation from
`7eba929`. Each platform's CI runner checked both executable versions.
Linux/macOS executables were not run locally on Windows.

| Target | Bytes | SHA-256 |
| --- | ---: | --- |
{table}

The downloaded Windows CLI and MCP server also pass local version checks.
Both are x64 PE executables without a Visual C++ runtime dependency. The MCPB
server bytes equal those in the native archive; its manifest, checksum file and
generated registry metadata agree on the version and version-specific URL.
Bundle SHA-256: `{checks['MCPB_sha256']}`.

The actual downloaded MCPB passes import, nesting, independent validation,
tool-catalog, file-output and write-confinement checks. The unchanged repository
verifier ran from an isolated copy on CCD1, so the active H4 matrix's writes
could not affect the verifier's file inventory. This is a regression check,
not an OS sandbox. Root source, measured binaries and the matrix were unchanged.

CI also passed the pinned MCPB and registry metadata validators. Validation
does not publish metadata. Dry runs do not produce provenance attestations;
published downloads and their attestations must be checked after publication.

[Local application checks](h4-score-integration-20261016.md) pass for this
candidate. Full current-build H4 quality/scale confirmation and green candidate
CI remain required before tagging. These package checks do not close any gate
or change the 45% completed milestone weight. The original candidate's
[earlier package proof](preview-release-dryrun-20261016.md) remains preserved.
'''
(out.parent / (folder + '.md')).write_text(report, encoding='utf-8', newline='\n')
(out / 'report.py').write_bytes(Path(__file__).read_bytes())
inventory = {p.relative_to(out).as_posix(): {'sha256': sha256(p.read_bytes()).hexdigest(),
             'bytes': p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}
(out / 'integrity.json').write_text(json.dumps(inventory, indent=2)+'\n', encoding='utf-8', newline='\n')

path = root / 'docs/STATUS.md'
text = path.read_text(encoding='utf-8')
before = 'confirmation and hosted CI remain outstanding. Its package workflow dry run\npasses; downloaded-artifact checks are separate. No release/tag is created.'
assert before in text
text = text.replace(before, 'confirmation and hosted CI remain outstanding. Its\n[three-platform package dry run and downloaded Windows checks](../benchmarks/results/' + folder + '.md)\npass, including actual bundle import/nest/validation. No release/tag is created.')
path.write_text(text, encoding='utf-8', newline='\n')

path = root / 'docs/RELEASE_READINESS.md'
text = path.read_text(encoding='utf-8')
before = 'pass. Its own committed full comparison is starting; current scale checks and\ngreen hosted CI remain required.'
assert before in text
text = text.replace(before, 'pass. Its own committed full comparison is running; current scale checks and\ngreen hosted CI remain required. Its [three-platform package dry run and\ndownloaded Windows package verification](../benchmarks/results/' + folder + '.md)\nalso pass.')
path.write_text(text, encoding='utf-8', newline='\n')
with (root / 'BENCHMARKS.md').open('a', encoding='utf-8', newline='\n') as stream:
    stream.write('''

## 2026-10-16 — Downloaded packages for integrated candidate 7eba929

[The new package dry run](benchmarks/results/preview-score-release-dryrun-20261016.md)
passes for `7eba929` / `0.2.0-alpha.1`: all three native archives have the
expected entries, architectures, permissions and exact documents. Native CI
checks executable versions. The downloaded Windows archive and actual MCPB
also pass local version, import, nesting, validation, catalog and confinement
checks from an isolated verifier on CCD1. Bundle/server/checksum/metadata bytes
agree. Release publication was skipped. No tag, release, attestation or registry
publication was created; published download/provenance checks remain required.
The current H4 full matrix is running against frozen root source/builds. These
package checks do not change its inputs, thresholds or the 45% completion weight.
''')
with (root / '.gitattributes').open('a', encoding='utf-8', newline='\n') as stream:
    stream.write('\nbenchmarks/results/' + folder + '/** -text -whitespace\n')
print('Recorded downloaded package proof and updated readiness.')
