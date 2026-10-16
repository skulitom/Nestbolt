from hashlib import sha256
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'benchmarks/results/preview-release-dryrun-20261016'
checks=json.loads((OUT/'checks.json').read_bytes())
assert checks['all_checks_passed']
table='\n'.join(f"| {r['target']} | {r['bytes']:,} | `{r['sha256']}` |" for r in checks['archives'])
report=f'''# Preview release packaging dry run — 2026-10-16

**Windows x64, Linux x64 and macOS arm64 packages all pass.**
[Release workflow 38830004706]({checks['workflow_url']}) completed successfully
for candidate commit `0a9fb44`, version `0.2.0-alpha.1`. The actual release job
was skipped as required for a tagless dry run. No release or registry entry
was published.

[Downloaded-artifact checks](preview-release-dryrun-20261016/checks.json)
verify each archive's six entries, executable architecture and exact documentation
from that commit. Unix archives retain executable permissions. Both executable
versions are checked on their own native CI runner. Linux/macOS binaries were
not executed locally on Windows.

| Target | Downloaded bytes | SHA-256 |
| --- | ---: | --- |
{table}

The downloaded Windows archive's CLI and MCP server also pass local version
checks. Both are x64 PE executables without a Visual C++ runtime dependency.
The MCPB contains the exact same server bytes as that archive; its checksum file
and generated metadata agree on SHA-256
`{checks['MCPB_sha256']}`. The version and version-specific download URL agree.

The actual downloaded MCPB passes import, nesting, independent validation,
tool-catalog agreement, file-output and write-confinement regression checks.
The unchanged repository verifier runs from an isolated copy of its scripts
and Cargo version file, on CCD1. Its inventory therefore cannot mistake the
active benchmark's new outputs for server writes. Temporary extraction paths
stay inside that isolated workspace; this is a regression check, not an OS
sandbox. The root product, binaries and active performance plan are untouched.

CI additionally passes MCPB 2.1.2 validation and checksum-pinned
`mcp-publisher` metadata validation. Validation does not publish to the registry.
Dry runs do not create provenance attestations; attestation and the published
Windows download must still be verified after the authorized GitHub release.

The earlier local [production checks](preview-integration-20261016.md) pass.
Current-build H4 quality/scale checks and green release-commit CI remain required.
If a later commit changes packaged contents, its final package hashes must be
recorded separately; these hashes apply only to this dry run. No quality gate,
held-out split or completed milestone weight changes here.
'''
(ROOT/'benchmarks/results/preview-release-dryrun-20261016.md').write_text(report,encoding='utf-8',newline='\n')
(OUT/'report.py').write_bytes(Path(__file__).read_bytes())
inventory={p.relative_to(OUT).as_posix():{'sha256':sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in sorted(OUT.rglob('*')) if p.is_file()}
(OUT/'integrity.json').write_text(json.dumps(inventory,indent=2)+'\n',encoding='utf-8',newline='\n')
p=ROOT/'docs/RELEASE_READINESS.md'; text=p.read_text(encoding='utf-8')
text=text.replace('  the native packaging dry run remains required before pushing a tag.',
    '  the [three-platform dry run](../benchmarks/results/preview-release-dryrun-20261016.md)\n  now passes for `0a9fb44`, including the actual downloaded Windows package checks.')
text=text.replace('- Run the packaging dry run for Windows x64, Linux x64 and macOS arm64. Verify\n  archives, Windows MCPB, version agreement, checksums and provenance. Verify\n  the downloaded Windows bundle after publication.',
    '- Windows x64, Linux x64 and macOS arm64 packaging passes on `0a9fb44`.\n  Downloaded archive contents, architectures, versions and Windows MCPB checksum\n  agree. If the final release commit changes package contents, record its own\n  dry run. Published provenance and the downloaded Windows bundle still need\n  verification after publication.')
p.write_text(text,encoding='utf-8',newline='\n')
with (ROOT/'BENCHMARKS.md').open('a',encoding='utf-8',newline='\n') as f:
    f.write('''

## 2026-10-16 — Preview package download verification and H2 evidence review

[Three-platform dry run](benchmarks/results/preview-release-dryrun-20261016.md)
passes for `0a9fb44` / `0.2.0-alpha.1`. All downloaded archives have their expected
architectures, permissions and exact documents; native CI checks both executable
versions. Downloaded Windows archive and MCPB additionally pass local version and
import/nest/validate checks. Bundle bytes match the archive server and generated
checksum/metadata. MCPB and registry metadata validators pass. The release job
is skipped; no tag, release, attestation or registry publication is created.
Published-download provenance remains required after the authorized release.

[H2 requirement review](benchmarks/results/h2-requirements-review-20261016.md)
accounts for all 313 labelled training files: 291 imports and 22 original clear
rejections, preserving the reviewed R43 exception. Product source comparison
confirms unchanged ordinary vector readers/exporters, native preserving writer,
public adapters, validator and all third-party lock records since the vector
replay. The current core equals the 56-project native diagnostic candidate.
This is a saved-evidence review, not a new import/timing/desktop measurement.
Twenty-two reserved vectors and the original denominator clarification remain
pending. No reserved geometry/labels reopened; H2 remains open and weight 45%.
''')
print('Dry-run report, release checklist and append-only evidence updated')
