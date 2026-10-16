# Integrated preview package verification — 2026-10-16

**All three downloaded native packages and the Windows MCPB pass.**
[Dry-run workflow 38840747735](https://github.com/skulitom/Nestbolt/actions/runs/38840747735) built candidate
`7eba929`, version `0.2.0-alpha.1`. All build and metadata-validation jobs
succeeded; the publication job was skipped. No tag, release or registry entry
was created by this dry run.

[Checks](preview-score-release-dryrun-20261016/checks.json) verify the six expected archive entries,
architectures, executable permissions on Unix and exact documentation from
`7eba929`. Each platform's CI runner checked both executable versions.
Linux/macOS executables were not run locally on Windows.

| Target | Bytes | SHA-256 |
| --- | ---: | --- |
| x86_64-unknown-linux-gnu | 5,490,414 | `74fe137d0be6b0ebbd2a865558fdc63ea454fa95131d8f7e227b00ef2ad0a23b` |
| aarch64-apple-darwin | 5,038,330 | `9b283611e5d6c4a6fad772b8bd776c54114eef34ec209ebeb789a2e15ab32f58` |
| x86_64-pc-windows-msvc | 5,332,730 | `f72e62cc5c563a98dd9801c1b42b8146b5a4f06c631157f384c895405648cc83` |

The downloaded Windows CLI and MCP server also pass local version checks.
Both are x64 PE executables without a Visual C++ runtime dependency. The MCPB
server bytes equal those in the native archive; its manifest, checksum file and
generated registry metadata agree on the version and version-specific URL.
Bundle SHA-256: `fb6a196d6c42e0fbc18cd527671387f646d353d9c1114b47f7ff8d3fb8b47c61`.

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
