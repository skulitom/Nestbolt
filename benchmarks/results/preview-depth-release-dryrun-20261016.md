# Current preview package verification — 2026-10-16

**All three downloaded native packages and the Windows MCPB pass.**
[Dry-run workflow 38854620093](https://github.com/skulitom/Nestbolt/actions/runs/38854620093) built commit
`23442be`, version `0.2.0-alpha.1`, including the integrated `aba989e` depth
change. All build and metadata-validation jobs succeeded; publication was
skipped. The dry run created no tag, release or registry publication.

[Exact checks](preview-depth-release-dryrun-20261016/checks.json) verify all six archive members,
architectures, executable permissions on Unix and exact documentation from
`23442be`. Each platform's native CI runner checked both executable versions.
Linux/macOS executables were not executed locally on Windows.

| Target | Bytes | SHA-256 |
| --- | ---: | --- |
| x86_64-unknown-linux-gnu | 5,490,468 | `376d5c9b74c0db58fe02f9cc0838d4c5133dcf89f6712cc8c1c7b0df73c26ce5` |
| aarch64-apple-darwin | 5,038,377 | `6431620e77ccafbc1a872acbae040aede11da4d5034eb9bd5943be7a287678f9` |
| x86_64-pc-windows-msvc | 5,332,820 | `4c96f3c7681edea9abb3798b189d309323854bc596d17bc53412a3668363278f` |

The downloaded Windows CLI and MCP server pass local version checks. Both are
x64 executables without a Visual C++ runtime dependency. The MCPB server bytes
equal the native archive server; manifest, checksum and generated metadata
agree on the version and version-specific download URL. Bundle SHA-256:
`72786ffd7ca4935832253c9618bbb5d50a5d02d1c9a6779aa709e82d9e4e6328`.

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
