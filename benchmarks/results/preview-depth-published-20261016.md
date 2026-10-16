# Published preview verification — 2026-10-16

**[v0.2.0-alpha.1 is published](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)**
as a prerelease at `c36baa8145e9e7b51e5667f4e4eaa0242256fc6e`.
The [five release jobs](https://github.com/skulitom/Nestbolt/actions/runs/38882959832)
pass. [Downloaded-package checks](preview-depth-published-20261016/checks.json),
[publication and provenance verification](preview-depth-published-20261016/publication-verification.json)
and [actual Windows feature checks](preview-depth-published-features-20261016.md)
all pass. Stable Latest remains v0.1.0, including the same release ID and every
asset ID, name, size and digest. No registry version was published.

The tag preflight binds the release to the tested product, complete H4 review,
local integration, previous six-job hosted checks and successful dry-run packages.
Only documented evidence and release notes differ from those tested commits.
The [publication audit](preview-depth-publication-audit-20261016/completion.json)
retains that preflight, tag push and ordinary main push, original sequence,
launch error, recovery scripts and byte inventories.

## Published downloads

All three native archives have exactly the expected six members, target
architecture, documents, executable permissions where applicable, and versions.
Linux/macOS executable version checks ran on their native hosted runners; their
binaries were not executed locally. Every release download matches SHA256SUMS
and GitHub's recorded digest. The published Windows MCPB matches its workflow
artifact and native server executable; generated registry metadata validates.

The actual downloaded Windows CLI and MCPB each pass import, nesting, independent
layout validation and the applicable write-confinement checks. Authored LightBurn
fixtures also pass explicit text-repair and mixed-group rejections, then import,
nest and export two rigid editable groups. Lead coverage is ten expected, eight
reserved and two flagged. XML contents/settings/fixed shapes are preserved;
separate SVG/DXF cutting files and repeat exports match. These are functional
checks on CCD1, without a new quality measurement or reserved input evaluation.

All four binary assets have verified GitHub-hosted build provenance, constrained
to this repository, release workflow, exact source commit and tag. Verification
rejects self-hosted runners. Full verifier output and checksums are retained.

## Preserved verification interruptions

The original launcher tried to execute a Python file directly on Windows and
failed with WinError 193 before any package test started. The recovery supplies
the explicit interpreter and uses the unchanged checker and original downloads.
Package tests then pass. Three of four concurrent provenance commands fail
while opening/renaming GitHub CLI's shared Sigstore cache; the fourth succeeds.
Sequential verification of all four assets passes with the same provenance
policy. Original failures remain at their original paths. No package test,
quality search, publication or asset upload is repeated to replace a failure.

Before the authored-feature check starts, its wrapper is adapted to omit obsolete
dry-run documentation edits and to describe the actual published commit. Both
wrapper versions are retained; feature checks and archive integrity checks are
unchanged apart from package/output paths and the pinned commit.

H1, H3, H4 and H6 remain complete: **60% of v1.1**. H2 import acceptance and H5
common-line material use remain open. Release notes disclose those limits. The
hosted browser remains on v0.1.0, and the frozen v1 benchmark claims are unchanged.
