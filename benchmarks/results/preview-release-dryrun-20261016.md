# Preview release packaging dry run — 2026-10-16

**Windows x64, Linux x64 and macOS arm64 packages all pass.**
[Release workflow 38830004706](https://github.com/skulitom/Nestbolt/actions/runs/38830004706) completed successfully
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
| x86_64-unknown-linux-gnu | 5,490,138 | `0c6dd4a9c1554a24db64248553af1412542f8c428e930a1a26e1eadc2a327e86` |
| aarch64-apple-darwin | 5,038,556 | `32b224edeeb6bea83c5c6bad4767412e300fce2f95fa655e025a790712db191c` |
| x86_64-pc-windows-msvc | 5,332,556 | `a7870dc8b437d752bf381df6f1cafc05c17112a1c3164df612e86497e7f30c2e` |

The downloaded Windows archive's CLI and MCP server also pass local version
checks. Both are x64 PE executables without a Visual C++ runtime dependency.
The MCPB contains the exact same server bytes as that archive; its checksum file
and generated metadata agree on SHA-256
`2f85d57dd0119b46268568e0595ba141fafc5d355b83bd7e6d39490c5d0898f3`. The version and version-specific download URL agree.

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
