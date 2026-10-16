# Downloaded preview: LightBurn and lead workflows — 2026-10-16

**The actual downloaded Windows CLI and MCPB pass the new-feature workflow.**
This exercises the packages from dry-run commit `23442be`; it does not build
new executables, repeat quality measurements or reopen reserved inputs.
[Checks](preview-depth-features-20261016/checks.json) and
[raw evidence](preview-depth-features-20261016/raw.zip) retain all commands,
JSON replies, expected rejection messages, authored inputs and output files.

| Check | Downloaded CLI | Downloaded MCPB |
| --- | --- | --- |
| Uncached text gives the required LightBurn repair instruction, without a partial library | Pass | Pass |
| Mixed active/Tool group gives the regrouping instruction, without a partial library | Pass | Pass |
| Supported project imports after the rejections | Pass | Pass |
| Two copies of a rigid editable group nest and independently validate | Pass | Pass |
| Lead coverage: ten expected contours, eight reserved, two explicitly flagged | Pass | Pass |
| Preserved `.lbrn2` plus separate SVG/DXF cutting files with LEADIN guides | Pass | Pass |
| Independent validation retains the same lead report; repeated export files are byte-identical | Pass | Pass |
| Original editable children, starts, settings, notes, unknown elements and fixed Tool shape survive | Pass | Pass |

The XML check separately compares parsed trees, including all group descendants,
against the authored source. Only each outer group transform and an optional
added stock outline are outside that preservation comparison. Both saved layouts
contain the requested two copies. This functional fixture does not replace the
complete H3 geometry or H6 reservation evidence.

The downloaded bundle runs with its actual manifest through the existing stdio
client. Its extracted files and all input fixtures stay unchanged; its owned
working, home and temporary directories stay empty. The earlier package smoke
already checked the broader write-confinement contract. All operations here run
on CCD1, separately from the active H4 measurements. Production digest remains
`8505a0bbce2c8f150799d3a6823611e21cbc33abb027b79bf095e43dc9ae7e88`.

The three inputs are original MIT test fixtures pinned to the package commit.
Expected errors are retained as successful rejection checks, not hidden import
successes. This adds actual-download feature evidence to the
[three-platform package proof](preview-depth-release-dryrun-20261016.md).
Full current quality/scale/export review and hosted checks remain required.
No release, registry publication or milestone closure occurs; completion is 45%.

Raw archive SHA-256: `946af3690e20d646bc312ac89679dc4216836832a64af3c5940911d1ba423a27` (2,874,665 bytes,
57 members). CRC, every member hash and byte length were verified.
