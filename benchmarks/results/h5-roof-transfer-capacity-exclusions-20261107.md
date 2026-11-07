# One-cog transfer: fixed-layout capacity exclusions — 2026-11-07

**All 120 exact one-cog-transfer layouts are now excluded** as completions to
66 parts. The previously verified 44-part partials remain valid, but their
remaining space cannot hold six brackets and sixteen inserts. No optimizer
runs and no whole allocation or orientation class is excluded. H2/H5 remain
open at **60% completed milestone weight**; the preserved valid 64-part layout
remains best.

[Complete two-empty-site covers](h5-roof-transfer-capacity-exclusions-20261107/two-empty-cover-plan.json) reuse the
independently audited full bit-mask matrices for the source frame/cog pool.
They do not reuse the earlier retained covers, which allowed only one empty
site. All eight bracket and four insert modes include every continuous
boundary point and open interval with no fixed-frame conflict and at most two
cog conflicts. Each of the 120 empty pairs selects its eligible labels.

[Independent readback](h5-roof-transfer-capacity-exclusions-20261107/two-empty-cover-audit.json) reconciles every prior
source/mask audit input, then verifies **26,070,912 continuous classes** and
exactly once-only coverage of the **5,483,907 retained classes** by **2,225
closed boxes**. A separate integer bit-count classification checks the
producer's bit operations. Every family and combined occupied union for all
120 cases is recomputed using two-dimensional count grids instead of the
producer's interval sweep.

The conservative remaining-body requirement is **556,778 mm²**:
six times 39,999 plus sixteen times 19,799. [The first area screen](h5-roof-transfer-capacity-exclusions-20261107/all120-capacities.json)
excludes **113 cases**, including three already excluded by bracket count.
All insert-only bounds remain above the required sixteen. Seven cases survive
this necessary screen; a passing bound is not feasibility.

[The tighter construction](h5-roof-transfer-capacity-exclusions-20261107/component-area-plan.json) sweeps the two
original rectangular components of each L-shaped bracket over every eligible
center box. Inserts retain their single component. The resulting occupied
union is clipped to an outward-relaxed stock rectangle. Source-contained
rectangles belonging to the eighteen fixed frames and fourteen occupied cog
sites are then removed: valid companion bodies cannot occupy those interiors.
This covers every possible companion placement while reducing the earlier
whole-bounding-box overestimate.

[Independent source and area readback](h5-roof-transfer-capacity-exclusions-20261107/component-area-audit.json) verifies
**20 transformed component bounds across 12 modes**, the exact source L
partition, outward stock containment and all selected fixed obstacles. It
reconstructs every occupied region and checks **21 exact union-minus-union
areas** with one-dimensional signed interval events, separately from the
producer's two-dimensional prefix grids. Overlap, duplicate-obstacle and
boundary-touch controls pass. Original holes remain preserved and are not
nesting space.

| Empty cog sites | Available occupied area at most (mm²) | Required (mm²) |
|---|---:|---:|
| 0, 7 | 426,561.493588 | 556,778 |
| 0, 14 | 466,620.516415 | 556,778 |
| 3, 13 | 435,318.836582 | 556,778 |
| 7, 12 | 418,232.634983 | 556,778 |
| 7, 13 | 439,333.553550 | 556,778 |
| 7, 14 | 437,872.214797 | 556,778 |
| 12, 14 | 458,291.657810 | 556,778 |

[All seven final proofs](h5-roof-transfer-capacity-exclusions-20261107/final-seven-capacities.json) exclude their exact
fixed 44-part layouts. Even the largest remaining area is short by
**90,157.483585 mm²**. Together with the preceding 113, no case in this finite
120-layout construction remains. The source-valid short sheet containing six
brackets, five inserts and one cog remains usable in a different construction.

[Complete cover preparation](h5-roof-transfer-capacity-exclusions-20261107/two-empty-covers-process.json) takes
**1.175224 s**, with its separate [audit](h5-roof-transfer-capacity-exclusions-20261107/two-empty-covers-audit-process.json)
at **1.379273 s**. [Component-area preparation](h5-roof-transfer-capacity-exclusions-20261107/component-area-process.json)
takes **0.572615 s**, and its [audit](h5-roof-transfer-capacity-exclusions-20261107/component-area-audit-process.json)
**0.640942 s**. Retaining all **17.107266 s** prior preparation gives
**18.855104 s** if consumed by a successor. Each bounded Job Object closes all
three processes under the unchanged 2 GiB and CPU/thread controls. No failed
or closed solver is repeated, reseeded or extended.

[Next](h5-roof-transfer-capacity-exclusions-20261107/next-step.json), assess source-derived roof arrangements with
five and six turned upper frames while retaining the valid one-cog short sheet.
Each proposed source pool must pass complete pair, stock and identity checks
before any necessary-cover or complete model. Changed frame geometry invalidates
the old obstacle masks; those cannot be reused as if the frames were unchanged.
The selected historical 39-owner calls used zero or four turned upper frames,
but broader models exist, so no class is claimed globally untested.

Four earlier fixed arrangements and all 440 whole-job allocations remain.
Full 66-part source/native/material validation, product integration,
UI/CLI/MCP parity and the original H5 matrix still need completion.

[Main be9c79d6 contains both earlier checkpoints](h5-roof-transfer-capacity-exclusions-20261107/prior-main-push-receipt.json),
pushed ordinarily after all six prior checks passed with 52 protected files
intact. [Fresh CI](h5-roof-transfer-capacity-exclusions-20261107/main-ci-at-review.json) has **5 passed / 1 live jobs**.
The coupled-transfer checkpoint and this evidence await the next ordinary push.
Product code, README and releases are unchanged.

[Archive checks](h5-roof-transfer-capacity-exclusions-20261107/archive-checks.json), [manifest](h5-roof-transfer-capacity-exclusions-20261107/raw-manifest.json),
[source bindings](h5-roof-transfer-capacity-exclusions-20261107/source-bindings.json), [historical references](h5-roof-transfer-capacity-exclusions-20261107/external-evidence.json)
and [runtime pins](h5-roof-transfer-capacity-exclusions-20261107/runtime-bindings.json) preserve all evidence.
