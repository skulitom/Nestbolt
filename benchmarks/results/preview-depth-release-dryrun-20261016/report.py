"""Record the current downloaded packages without changing the release decision."""
from hashlib import sha256
from pathlib import Path
import json

root = Path(__file__).resolve().parents[1]
folder = 'preview-depth-release-dryrun-20261016'
out = root / 'benchmarks/results' / folder
checks = json.loads((out / 'checks.json').read_bytes())
assert checks['all_checks_passed']
assert checks['release_commit'] == '23442be38ee2e881669e753bc405ab3269ff1b39'
assert checks['dry_run_only'] and checks['release_job_skipped']
table = '\n'.join(f"| {r['target']} | {r['bytes']:,} | `{r['sha256']}` |" for r in checks['archives'])
report = f'''# Current preview package verification — 2026-10-16

**All three downloaded native packages and the Windows MCPB pass.**
[Dry-run workflow 38854620093]({checks['workflow_url']}) built commit
`23442be`, version `0.2.0-alpha.1`, including the integrated `aba989e` depth
change. All build and metadata-validation jobs succeeded; publication was
skipped. The dry run created no tag, release or registry publication.

[Exact checks]({folder}/checks.json) verify all six archive members,
architectures, executable permissions on Unix and exact documentation from
`23442be`. Each platform's native CI runner checked both executable versions.
Linux/macOS executables were not executed locally on Windows.

| Target | Bytes | SHA-256 |
| --- | ---: | --- |
{table}

The downloaded Windows CLI and MCP server pass local version checks. Both are
x64 executables without a Visual C++ runtime dependency. The MCPB server bytes
equal the native archive server; manifest, checksum and generated metadata
agree on the version and version-specific download URL. Bundle SHA-256:
`{checks['MCPB_sha256']}`.

The actual downloaded MCPB passes import, nesting, independent validation,
tool-catalog, file-output and write-confinement checks. The unchanged verifier
runs from an isolated copy on CCD1; concurrent H4 evidence writes are outside
its inventory. This is a regression check, not an OS sandbox. Production
source, measured executables and browser assets remain unchanged.

CI also passes pinned MCPB and registry metadata validators. Validation does
not publish registry metadata. Dry runs do not produce provenance attestations;
the actual published downloads, checksums and attestations must be checked
after release.

The [local integration](h4-depth-integration-20261016.md) and
[scope/memory preflight](h4-depth-requirement-preflight-20261016.md) pass.
This package proof does not replace current full quality, scale, exported-curve
fidelity, screenshot review or hosted checks. The release-readiness document
tracks their later completion. No gate closes here; completed milestone weight
remains 45%. Earlier package proofs and failed quality comparisons stay intact.
'''
(out.parent / (folder + '.md')).write_text(report, encoding='utf-8', newline='\n')
(out / 'report.py').write_bytes(Path(__file__).read_bytes())
for helper in ['prepare_depth_dryrun_verification.py', 'continue_depth_package_checks.py']:
    (out / helper).write_bytes((root / 'output' / helper).read_bytes())
inventory = {p.relative_to(out).as_posix(): {'sha256': sha256(p.read_bytes()).hexdigest(),
             'bytes': p.stat().st_size} for p in sorted(out.rglob('*')) if p.is_file()}
(out / 'integrity.json').write_text(json.dumps(inventory, indent=2)+'\n', encoding='utf-8', newline='\n')
print('Recorded current downloaded package proof; no tag, release or registry publication.')
