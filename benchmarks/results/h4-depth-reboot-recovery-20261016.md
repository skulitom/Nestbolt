# Integrated tree-depth preview: recovered full H4 comparison — 2026-10-16

**All quality comparisons pass.**
603/603 completed current-build layouts and 195 frozen-v1 layouts validate. These are
the originally planned outcomes for candidate `aba989e`; no unchanged-build
repeat, changed threshold or selected subset replaces a failed observation.
Scale and complete requirement review are separate, so this report alone
does not close H4 or change completed milestone weight.

[Results](h4-depth-reboot-recovery-20261016/results.json), [verification](h4-depth-reboot-recovery-20261016/verification.json),
[committed plan](h4-depth-reboot-recovery-20261016/plan.json).

## Method

The union of 65 development jobs and the eleven-job curve subset contains
67 jobs. Each engine covers all 67 at 60 seconds and seeds 0–2.
The 201 native and 201 Chrome outcomes completed before the servicing reboot
and are retained unchanged alongside 195 frozen-v1 outcomes. The recovery
runs only the 201 missing Firefox outcomes. The original Firefox batch had
started but saved no outcomes; its precise number of started jobs is unknown.
The interrupted session remains interrupted. There are no held-out jobs,
final seeds or competitor claims.
One browser worker per job, at most eight physical CCD0 cores; separate
functional checks/builds use CCD1. Source, executable, site, runner, inputs
and original environment-override guards stay unchanged. The new boot and OS
environment are recorded separately in the recovery plan.

The Firefox recovery took 27.451 minutes, below its one-hour cap.
This is not the elapsed time of all three engines; no continuous complete
session is claimed and the original four-hour session is not extended.
Every layout hash, requested quantity and independent metric is checked.
Standalone and saved metrics agree exactly, including original-library
validation of the public examples. Original Chrome and recovered Firefox
batch execution and affinity records are preserved in their respective archives.

## Full development comparisons

Positive differences mean more material. Three-seed job medians are used.
Native retains +0.5% median; browser G5 retains +2% median and total, also
checked separately for each seed.

| Comparison | Median | Total | Worst job | Result |
| --- | ---: | ---: | ---: | --- |
| Native vs frozen v1 | +0.000614% | +0.019783% | +2.897407% | pass |
| Chrome vs native | +0.107768% | +0.510025% | +3.722850% | pass |
| Firefox vs native | +0.150385% | +0.527068% | +3.714667% | pass |

| Browser | Seed | Median | Total | Result |
| --- | ---: | ---: | ---: | --- |
| Chrome | 0 | +0.198675% | +0.756203% | pass |
| Chrome | 1 | +0.273220% | +0.529344% | pass |
| Chrome | 2 | +0.020372% | +0.060152% | pass |
| Firefox | 0 | +0.140442% | +0.569495% | pass |
| Firefox | 1 | +0.119809% | +0.499914% | pass |
| Firefox | 2 | +0.011138% | +0.123186% | pass |

## Curve subset

Both browsers must stay at or below +1% median and +5% for every job.

| Browser | Valid | Median | Worst job | Total | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| Chrome | 33/33 | +0.851159% | +2.455588% | +0.826574% | pass |
| Firefox | 33/33 | +0.828477% | +2.561291% | +0.778015% | pass |

## Retained evidence and next step

The original `0a9fb44` [failed comparison](h4-preview-development-20261016.md)
and the `7eba929` [failed comparison](h4-preview-score-release-20261016.md)
remain preserved. This candidate lowers the separator-window base collision
tree depth from four to three, retaining exact geometry, aspect scaling,
leaf threshold and budgets. Its [isolated subset](h4-quadtree-depth-probe-20261016.md)
and [integration checks](h4-depth-integration-20261016.md) are separate evidence.
No general speed gain follows from these wall-clock quality outcomes.

Run the already specified current-build scale workflows, then review every H4 requirement.
H2/H5 remain open independently. No tag, release or registry entry is created
by this report, and frozen v1 claims remain unchanged.

The [raw archive](h4-depth-reboot-recovery-20261016/raw.zip) contains 1,047 members,
7,622,447 bytes, SHA-256 `4defe62adedbcb4de239a9daa709434ef7cf2d7416fe556397893f6f38a02454`.
It preserves every recovery outcome, validation, plan and browser/process record,
including the original interrupted-session archive and exact measured build.
The nested original archive preserves every completed native/Chrome outcome
and the interrupted first Firefox batch. CRC, member sizes and SHA-256 checks
all pass. Frozen-v1 bytes remain in their verified preceding archive.
