# H4 complete: curved drawings in the browser — 2026-10-16

**N3/H4 passes its complete requirement audit. Completed v1.1 milestone weight is 60%:**
H1 (15%), H3 (25%), H4 (15%) and H6 (5%). H2 and H5 remain open. This does
not complete v1.1, publish a release or establish a new competitor comparison.

[Requirement audit and exact evidence hashes](h4-depth-complete-20261016/checks.json),
[full recovered quality comparison](h4-depth-reboot-recovery-20261016.md),
[fixed scale/export sequence](h4-depth-recovered-scale-plan-20261016/plan.json).

## Quality and validity

The declared eleven-job curve subset and all 65 development jobs use 60-second
budgets, seeds 0–2, one browser worker per job and physical CCD0 cores only.
All 603 current-build outcomes independently validate, preserve every requested
quantity and agree with their saved metrics. The 195 frozen-v1 layouts remain
verified. No formerly fitting job becomes invalid; no held-out input is opened.

Native's three-seed job-median difference is **+0.000614%**, below +0.5%.

| Curve subset | Median material vs native | Worst job | Limits |
| --- | ---: | ---: | --- |
| Chrome | +0.851159% | +2.455588% | Pass: +1% median, +5% every job |
| Firefox | +0.828477% | +2.561291% | Pass: +1% median, +5% every job |

| Full 65-job development set | Median vs native | Total vs native | Original bounds |
| --- | ---: | ---: | --- |
| Chrome | +0.107768% | +0.510025% | Pass: +2% median and total, aggregate and every seed |
| Firefox | +0.150385% | +0.527068% | Pass: +2% median and total, aggregate and every seed |

## Complete scale workflows

Both browsers import, nest and export the frozen 2,000-part letters/gears drawing
with Quick initial layout enabled and automatic worker selection. The original
G5 scale workflow also passes in both browsers with Quick initial layout off.
Every resulting layout independently validates all 2,000 placements.

| Workload | Browser | Peak RSS GB | Peak private GB | Longest heartbeat gap ms | Long Task ms |
| --- | --- | ---: | ---: | ---: | ---: |
| curves | Chrome | 1.336766 | 1.125847 | 78.1 | 0.0 |
| curves | Firefox | 1.352409 | 1.275429 | 199.0 | Unavailable; heartbeat checked |
| g5 | Chrome | 0.960791 | 0.811270 | 56.1 | 0.0 |
| g5 | Firefox | 1.003975 | 0.898294 | 94.0 | Unavailable; heartbeat checked |

Every observed process-tree memory maximum is below 1.5 GB and every measured
responsiveness maximum is at most 200 ms. Memory is sampled every 200 ms;
the main-thread heartbeat runs at 20 ms, with Long Tasks checked where supported.
Import, nesting and export intervals are all included. These observations do
not provide a universal memory or latency guarantee.

The actual measured WASM has one defined, unshared memory and no imported
shared memory. Independent Web Workers do not use WASM threads. Exact source,
build, runner, input and environment-override guards remain unchanged.

## Geometry and visible output

Independent svgpathtools and ezdxf readers check every saved SVG/DXF primitive
and control point for all 2,000 curved-workload placements in each browser.
They compare original source geometry under the saved placement transforms,
including sheet-coordinate orientation, every sheet, IDs/entity counts, spline
degrees and knot vectors. The 0.01 mm bound is unchanged. No export is regenerated
or repaired. Original-geometry layout validation is a separate check.

All four actual workflow screenshots were inspected and hashed. Their visible
results, controls and previews agree with the saved workflows; complete geometry
is established by the all-placement checks. CRC, every archived member hash and
byte length are verified before raw-file consolidation.

## Interruption, provenance and remaining work

Windows servicing interrupted the first session after all 201 native and 201
Chrome outcomes completed. Firefox had started but saved no outcome; the exact
number of started worker jobs is unknown. Those files and the interrupted
session remain preserved, with all 402 completed current outcomes retained
unchanged. Only the missing 201 Firefox outcomes were recovered under the same
build, jobs, seeds, budgets and limits. The new boot/OS is recorded explicitly.
The original session is not relabelled complete and no combined continuous
wall time is claimed. Earlier failed candidates remain preserved.

Current native/CLI/MCP/browser integration and downloaded package feature checks
are separate supporting evidence. No common-line experiment enters this build.
The README retains the frozen v1 benchmark claims. Import acceptance and
common-line material use still need their H2/H5 work; this audit closes H4 only.
