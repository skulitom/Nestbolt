# H6 material-cost preparation and repeated lead checks — 2026-10-15

The 13-job H5/H6 development set is frozen, and the public CLI measurement
pipeline now passes its eight-case pilot. The full 60 s, three-seed material
comparison remains pending. **H6 is open; milestone completion stays 15%.**

## Dataset and measurement

The [manifest](../datasets/cutting/manifest.json) references the eight prescribed
maker jobs and five new MIT rectangle/bracket jobs. Its SHA-256 is
`922d36732c6e7624b1c5501c8320effb12b33f37d7361cc5d5856b28d19ca814`.
Every original polygon ring becomes an exact line contour, with no new
simplification or flattening. Each derived job is checked against its frozen
source, allowing only the requested kerf clearance to differ.

Both measured arms use common-line mode, bonus off, with the same 0.2 or 1.5 mm
kerf. The lead arm adds default line leads (3 mm, 45° outer, 90° holes). This
isolates the allowance in a common-line job. H5 bonus-on savings and the Deepnest
comparison remain separate. Original maker geometry, quantities, stock,
rotations, mirrors and margins are unchanged. No held-out geometry is read.

`scripts/h6_material_cost.py` retains every outcome and a ZIP of its raw inputs,
search, validation, exports and logs. It revalidates every successful layout
through the public API and records coverage/flags. Invalid and timed-out pairs
receive no cost score. The [protocol](../datasets/cutting/README.md) fixes the
full measurement at 60 wall-clock search seconds, seeds 0–2, both kerfs and all
13 jobs, using one physical CCD0 core per run and at most eight runs.

## Retained failures and bounded optimization

The [first pilot](h6-material-pilot-20261015T123025Z/results.json) checked four
of twelve runs. Seven reports were rejected by an overly strict harness equality
check: JSON round trips change some floating sums at their last decimal place.
The corrected comparator requires identical structures/discrete values and no
more than 1e-9 absolute numeric difference. This does not change any geometry
gate. The remaining large plasma run had no completed layout in two seconds.

The [corrected five-second pilot](h6-material-pilot-corrected-20261015T123221Z/results.json)
checked seven of eight runs. The 500-part plasma lead case reached a warm layout
but timed out at the external 185 s boundary before producing its final report.
Its original runner, failure and incomplete outputs remain.

After stopping that run, final planning gained a cache of local owner-fit
booleans. Its lifetime is one preparation/finalization with fixed source
geometry, options and units. The key identifies the part, contour, source
segment/parameter and exact trial length. Rigid copies share these local
results. Checks involving previous leads, shared-edge exclusions, neighbours,
stock and the independent final validator are still performed for each copy.
Rejected local trials also avoid building an unused second envelope.

The [same five-second pilot after the change](h6-material-pilot-owner-cache-20261015T124539Z/results.json)
passes **8/8 runs**. The 500-part plasma lead run completes in **16.78 s**, plus
**5.18 s** for fresh validation. It reserves 500 outer contours and explicitly
flags 3,800 small-hole contours. The laser counterpart reserves all 4,300
contours and takes 22.56 s plus 7.85 s for validation. Search budgets are the
same; wall-clock search can produce different incumbents. These are development
pilots, not a controlled speed benchmark or the full material-cost result.

## Verification

The new regression compares cached and fresh plans while changing copy-specific
acceptance and exclusions, then restoring them, for both line and arc leads.
It covers both accepted and rejected local trials. It passes in optimized and
debug builds. All 18 lead unit/property tests, four core integration tests, two
MCP lead tests, all 23 optimized CLI feature tests and four focused
Chromium/Firefox cases pass. Strict lint, formatting and production browser/WASM
build pass. The previous complete workspace suite belongs to `1619370`; it is
not represented as a new full-suite run for this cache change.

The [three original native-previewed coupons](h6-material-checks-20261015T124147Z/coupons/checks.json)
now revalidate through the current public pipeline, with independent source,
coverage and owner checks: 24/24 reserved contours, no flags, identical local
plans and CUT SVG attributes. The two separate outer/hole settings layouts also
revalidate with unchanged plans/exports. No new native session was needed.

[Check logs and provenance](h6-material-checks-20261015T124147Z/checks.json)
include all 1,181 unchanged frozen hashes. Builds/tests use CCD1; solver and
revalidation processes use one assigned physical CCD0 core. The available
between-session heat reading was ACPI 16.9°C and CPU clock 4,201 MHz; ACPI is a
coarse platform signal, not a CPU die-temperature measurement.

No release, final acceptance run or published v1 quality result changes.
