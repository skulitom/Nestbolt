# Status — 2026-10-18

## v1.1 — real shop files

**Completion: 60%.** The plan is tracked in [PLAN_V1_1.md](PLAN_V1_1.md).
Only completed gate weights count. N0/H1, N2/H3, N3/H4 and N5/H6 are complete:
the corpus and split are frozen; LightBurn preservation, browser quality/scale
and lead allowances pass their complete requirement reviews. The
[H4 completion audit](../benchmarks/results/h4-depth-complete-20261016.md)
includes full quality, four large-layout workflows and all-placement curve fidelity.
H2 and H5 remain open. N1 implementation is in progress;
explicit gap repair, layer/colour selection, segment cleanup, byte decoding,
units reports, rejection of incomplete selected cuts and the locally verified
export palette and imported stock outlines now work through the UI, CLI and MCP.
No N1 importer changes may precede the H1 freeze. LightBurn-dependent evidence is
due by 2026-11-06. v0.1.0 was released and published to the MCP Registry on
2026-10-14. On 2026-10-16 Artem authorized the next GitHub release when ready,
including a README update. [Preview v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is now published at `c36baa8`; [actual download and provenance checks](../benchmarks/results/preview-depth-published-20261016.md)
and [Windows LightBurn/lead workflows](../benchmarks/results/preview-depth-published-features-20261016.md)
pass. Stable Latest and its assets remain v0.1.0. This does not close the remaining
v1.1 gates or authorize a new final acceptance run. No new registry version was published.


**Latest browser follow-up, 2026-10-17:** [the new hosted trace](../benchmarks/results/browser-lead-budget-20261017.md)
identifies a Chromium lead-test failure: the requested one-second search expires
without a complete layout. Using the normal five-second functional-test allowance
keeps all assertions and passes the complete local suite (86 tests, four opt-in
skips, two workers, no retries). [Hosted confirmation now passes all six jobs](../benchmarks/results/browser-lead-hosted-confirmation-20261017.md), including 86 browser tests and four skips. The original
failure and diagnostics remain, and the older c36baa8 Firefox cause remains unknown.
Application source, benchmark limits and release assets are unchanged.

**Earlier hosted checks, 2026-10-17:** [both follow-up main commits pass all six checks](../benchmarks/results/reconciliation-20261017.md),
including 86 browser tests with four opt-in skips each. The original c36baa8
Firefox failure remains preserved with unknown cause. New failure diagnostics
remain enabled. Main's new plugin and translated/agent READMEs are reconciled;
application source and gate thresholds are unchanged.


**Release readiness, 2026-10-16:** candidate `aba989e` is version
`0.2.0-alpha.1`. Its [integration checks](../benchmarks/results/h4-depth-integration-20261016.md)
pass: 302 workspace tests, 75 optimized core tests, 27 CLI tests, 86 browser
tests, builds/lint and actual Windows bundle import/nest/validation/confinement.
The first bundle inventory overlapped this task saving evidence; its failure
is retained and the same-bundle check passes once competing writes stop.
The [isolated pilot](../benchmarks/results/h4-quadtree-depth-probe-20261016.md)
validates all 99 layouts and passes Chrome +0.689439% / Firefox +0.639475%.
The [full matrix](../benchmarks/results/h4-preview-depth-release-20261016/plan.json)
was interrupted by Windows servicing at 06:00 UTC after 201 native and 201
Chrome valid outcomes; Firefox saved no outcomes and scale never began.
The [recorded recovery](../benchmarks/results/h4-depth-reboot-recovery-20261016.md)
retains every completed result and the original interruption, then completes
only the missing Firefox phase under unchanged limits. All 603 current-build
and 195 frozen-v1 layouts validate. Native median is +0.000614%; curve-subset
medians are Chrome +0.851159% / Firefox +0.828477%, and every job is within +5%.
Full G5 aggregate and each-seed limits also pass. The
[complete H4 audit](../benchmarks/results/h4-depth-complete-20261016.md) now passes:
both 2,000-part workloads in both browsers stay below 1.5 GB and at most 200 ms;
all curved-workload placements pass independent saved SVG/DXF checks, and all
four screenshots are reviewed. Original interruptions and failed candidates remain preserved.
[All three downloaded packages and the Windows MCPB](../benchmarks/results/preview-depth-release-dryrun-20261016.md)
pass their checks, including actual Windows import/nest/validation/confinement.
[All six hosted checks pass for this code](../benchmarks/results/preview-depth-hosted-checks-20261016.md); reviewed evidence is pushed to main as `21835ba`. The [requirement preflight](../benchmarks/results/h4-depth-requirement-preflight-20261016.md)
confirms the original scope and unshared WASM memory. No common-line experiment
is integrated. The qualified preview is now published and verified; completed
milestone weight remains 60%. The release record above supersedes the earlier
dry-run and prepublication checkpoints.

The earlier `7eba929` [full comparison](../benchmarks/results/h4-preview-score-release-20261016.md)
retains 603 new and 195 reused valid outcomes, but Chrome's curve subset fails
at +1.032679%. Its [conditional scale sequence](../benchmarks/results/h4-preview-score-scale-plan-20261016/stopped.json)
stopped without a scale run. Its successful hosted checks and package dry run
remain tied to that earlier build. [Current-build profiles](../benchmarks/results/h4-browser-profile-20261016T040030Z.md)
motivated the shallower tree; earlier failures do not disappear when a new
candidate passes a pilot. The hosted browser remains on
[v0.1.0](https://github.com/skulitom/Nestbolt/actions/runs/38572138348), as the README explains.

The earlier `0a9fb44` candidate's [completed matrix](../benchmarks/results/h4-preview-development-20261016.md)
retains all 603 valid new layouts and Chrome's failed subset median of
+1.046217%, against +1%. The finer score bound in `7eba929` first passed its
[isolated subset and fixed-work checks](../benchmarks/results/h4-score-chunks-probe-20261016.md).
Neither earlier passing builds nor that isolated probe replaces the current full
comparison. No unchanged-build repeat or threshold change is used.

Earlier repository reconciliation (2026-10-15): [v0.1.0](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0)
is tagged at `6c462c2`, and the [registry publication](https://github.com/skulitom/Nestbolt/actions/runs/38540517654)
succeeded; the registry entry is active with the Windows MCPB. This software release
does not replace the published v1 benchmark build `75cbb32` or complete any v1.1 gate.
The [separator weight fix](../benchmarks/results/separator-weight-cap-20261014.md)
from `fix/separator-weight-cap` is integrated, preserving its original commits and
138 development results. It caps Nestbolt's own separator; delegated upstream
Sparrow remains pinned and unpatched, with an [upstream report drafted](upstream-drafts/sparrow-gls-weight-overflow.md).
The [jagua-rs 2.0 spike](../benchmarks/results/jagua-2-spike-20261014.md) is retained
as experimental evidence only; its dependency and solver port are not integrated.
Its short development runs are a performance lead for N3, not H4 evidence. Fresh [integration checks](../benchmarks/results/reconciliation-20261015.md) pass: 238 workspace tests (one ignored), 21 optimized CLI tests, two Sparrow tests, strict lint, formatting and the WASM build. Frozen integrity remains 1,181 files.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| N0 — Messy-file corpus | 15% | **H1 complete.** [Frozen corpus and split](../benchmarks/results/h1-freeze-20261013.md): 534 inputs, 338 labels, 148 renders, 1,181 attributed/checksummed files; 15 real + 10 native held out with lineage isolation |
| N1 — Import robustness | 25% | In progress: [incomplete-drawing checkpoint](../benchmarks/results/h2-completeness-checkpoint-20261013.md) across three surfaces; 245/257 training vectors match counts, 11 reject with repair instructions (including all nine negatives), the single frozen-label count discrepancy now has an approved, hash-scoped scoring exception (246 reviewed matches). Robustness 183/183 without crash/timeout. [Ten native exports and palette](../benchmarks/results/h2-lightburn-20261013T195848Z.md): saved dimensions within 0.000033 mm; eight exact rounded UI sizes, two spline display differences retained. [Cut layers](../benchmarks/results/h2-cut-layer-audit-20261013.json) match all 246 prior imports; [full vector fidelity sweep](../benchmarks/results/h2-fidelity-20261013T202338Z.md): 239 pass, 11 reject, four time out and three error; [closed-path repair](../benchmarks/results/h2-closed-retrace-checkpoint-20261013.md) now passes the ARC SVG/DXF rerun, and the [large-sheet margin repair](../benchmarks/results/h2-margin-checkpoint-20261014.md) resolves both Gherkin DXF nesting errors (358 contour comparisons below 0.000001 mm). The [complete corrected vector sweep](../benchmarks/results/h2-fidelity-20261014T012836Z.md) passes all 246 importable files and retains 11 clear rejections, with zero timeouts/errors and 5,138 matched contours (maximum SVG 0.003302 mm, DXF 0.000500 mm). All four formerly timed-out Iris files return independently valid incumbents, explicitly non-repeatable at the 240 s cooperative boundary. The [deadline repair and failed probes](../benchmarks/results/h2-work-deadline-checkpoint-20261014.md) remain documented. [Imported stock outlines](../benchmarks/results/h2-sheet-checkpoint-20261013.md) work across all surfaces; all ten labelled pre-arranged nests match their stock geometry. [Diagnostic coverage](../benchmarks/results/h2-warning-audit-20261014T015958Z.md) now passes all 246 imports and cut-layer selections, with unchanged geometry; [habit properties](../benchmarks/results/h2-habit-fuzz-20261014T015256Z.md) pass 10,000 import and 1,008 nesting cases across all 17 habits. A fresh robustness run passes all 183 files within 1.275 s. The [completed H3 audit](../benchmarks/results/h3-complete-20261015.md) now accounts for all 59 original native projects: 48 imported originals match membership, physical cut holes, fixed shapes and cutting layers; 11 original rejections remain explicit. Approved repairs supply the 122 uncached Text geometry checks. The [H2 requirement review](../benchmarks/results/h2-requirements-review-20261016.md) now accounts for all 313 training inputs and connects warning/fidelity evidence to the current source; 291 accepted imports and 22 original clear rejections remain explicit. The remaining reserved evaluation is still open. Two held-out negatives cap literal success at 92%; the held-out denominator clarification remains pending, with split unchanged |
| N2 — LightBurn round-trip | 25% | **H3 complete.** [Full requirement review](../benchmarks/results/h3-complete-20261015.md): all 59 original projects parse and preserve byte-identical no-op output; 1,749 comparable original leaves and all 477 prepared leaves pass independent geometry checks. All three reserved projects pass their once-only evaluation, including exact labels and three valid actual searches. Combined evidence includes 120 canonical diagnostic sheets and 443 independently checked units. Five native-checked layouts revalidate with unchanged settings/contents. All 295 workspace, 26 optimized CLI and 84 enabled browser tests pass. The approved uncached-text prerequisite, mixed-group rejection and L42 native repair layer change remain explicit; originals and failures are preserved |
| N3 — Curve-heavy browser | 15% | **H4 complete.** [Full requirement audit](../benchmarks/results/h4-depth-complete-20261016.md): all 603 current-build layouts and 195 frozen-v1 layouts validate; native median +0.000614%, Chrome/Firefox subset medians +0.851159%/+0.828477%, every job within +5%, full G5 aggregate/per-seed bounds pass. Four 2,000-part scale workflows pass: maximum process-tree RSS 1.352409 GB and maximum heartbeat gap 199 ms. Every saved SVG/DXF curve/control point for all 2,000 placements in both curved-workload outputs passes; four screenshots reviewed and raw archives verified. No WASM threads, unchanged geometry/guards, original failures and servicing interruption preserved. |
| N4 — Common-line cutting | 15% | In progress: [compensated geometry and native checkpoint](../benchmarks/results/h5-commonline-checkpoint-20261014.md), independent Clipper2 checks and UI/CLI/MCP parity. The optional bonus is off by default. After the retained [78-run pilot](../benchmarks/results/h5-common-bonus-checkpoint-20261015.md), the [full 60-second/three-seed comparison](../benchmarks/results/h5-cutting-development-20261015.md) validates all 234 Nestbolt layouts. Median savings **13.0311% laser / 13.1005% plasma** meet the savings condition. The two mechanical jobs still exceed +1% material: worst **+6.5085% laser / +5.5959% plasma**; all other jobs are within the guard. Normal mode uses 21/49 hole riders; common mode forbids them. Deepnest SVG comparison is complete: 35 valid runs, four no-layout outcomes, native reported merge length and actual SVG savings reported separately. H5 remains open on material. The generated request schema omission was corrected; its original CI failure is retained. No gate/default/frozen input changed |
| N5 — Lead-in allowances | 5% | **H6 complete.** [Gate evidence and material costs](../benchmarks/results/h6-complete-20261015.md): independent original-source coverage/attachment, owner/neighbour/stock checks, exact contour starts, three searched native previews and separate outer/hole/shortened settings. UI/CLI/MCP support preserving LightBurn projects plus separate SVG/DXF cutting files under Artem’s decision. The current build revalidates all 24 original native-coupon reservations unchanged; lead/core/MCP/CLI/browser checks pass. All 156 development layouts validate across 13 jobs, both kerfs and seeds 0–2. Median material cost is **+1.0696% laser / +6.0951% plasma**, with small-hole plasma flags explicitly reported. One report-order harness failure was corrected using the same saved layout and unchanged 1e-9 tolerance; all original failures remain. No new held-out/final acceptance or release claim |

**N4 material-profile candidate preparation, 2026-10-18:** [all 123 optimized tests pass](../benchmarks/results/h5-material-profile-preparation-20261018.md),
with all 117 prior tests unchanged. The candidate rejects same-inventory
trials whose exact original-geometry profiles prove unchanged charged
material. It uses the existing validator footprints and preserves every
accepted geometry/material check. Budgets and coefficients are unchanged;
profile work uses the existing vertex charge. Five proofs, 23 witness pairs
and 47 frozen-CLI checks cover geometry contexts, real gains and an invalid
overlap; 12 branch outcomes pass another 24 CLI checks. The original failing
branch regression is preserved. Strict lint/build, public parity/replay,
five harness tests and exact formatted-source reconstruction pass. The
unchanged 72-outcome method is committed before measurement. No quality,
integration or release claim; H2/H5 remain open at 60%.

**N4 exact-state early-rejection outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-exact-reject-pilot-20261018.md).
The independent filled-outer audit checks 133,535 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.349182%; m-mechanical-large-plates at 1.5 mm: +5.485080%; m-mechanical-panel-hardware at 0.2 mm: +6.767422%; m-mechanical-panel-hardware at 1.5 mm: +5.195747%; c-bracket-mixed at 0.2 mm: +1.027791%; c-bracket-mixed at 1.5 mm: +1.177346%
The candidate accepts 13/125 total exchanges, including 11/87
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 12 parts. The early exact-state and original neutral guards reject 41 same-inventory proposals without material improvement; mixed pairs account for 2/5 accepted/attempted exchanges. The neutral total includes 3 exact-state rejections before repeated validation. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

**N4 exact-state diagnosis, 2026-10-18:** [both final and all 12 saved layouts validate](../benchmarks/results/h5-exact-state-20261018.md).
1 of 6 neutral trials exactly preserve the complete internal physical state.
Independent filled-outer checks cover 111,838 same-sheet pairs.
Public pose multisets match in 1/6 pairs; exact internal comparison also
requires shared model/container identity and full float bits. All original
validators and decisions remain. This diagnostic establishes no quality gain;
the five failed pilot comparisons remain authoritative. H2/H5 stay open at 60%.

**N4 larger-return diagnosis, 2026-10-18:** [all four final and four intermediate layouts validate](../benchmarks/results/h5-larger-stage-20261018.md).
The filled-outer audits check 23,542 same-sheet pairs. Of 23 attempts, two
accept, fourteen fail source repair and seven are neutral inventory rejections.
Panel paired repairs start with zero loss; repeated validation costs 0.367 /
0.299 seconds, and no mixed pair is generated. Large-plate exchanges save only
86.418 / 40.2735 mm2 immediately; filling changes neither total and leaves
0.965 / 0.552 seconds of the original exchange opportunity. Next verify whether
neutral trials preserve exact original-item poses before considering an early
rejection. Equal inventory/material alone cannot justify skipping validation.
These instrumented observations do not replace the five failed pilot pairs;
no integration or H5 credit, and completion remains 60%.

**N4 larger-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-larger-return-pilot-20261018.md).
The independent filled-outer audit checks 133,465 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.739579%; m-mechanical-large-plates at 1.5 mm: +6.431410%; m-mechanical-panel-hardware at 0.2 mm: +6.701091%; m-mechanical-panel-hardware at 1.5 mm: +4.836540%; c-bracket-mixed at 1.5 mm: +1.989411%
The candidate accepts 13/119 total exchanges, including 10/81
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 15 parts. The unchanged neutral guard rejects 33 same-inventory proposals without material improvement; mixed pairs account for 1/4 accepted/attempted exchanges. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

**N4 larger-return candidate review, 2026-10-18:** [the first implementation is unqualified](../benchmarks/results/h5-larger-return-review-20261018.md).
The new larger-return regression first fails against unchanged runtime, then
passes after removing the paired proposal area filter. All four new tests
pass, but the complete suite reports 107 passes and four older failures.
Every original assertion, failed source and binary is preserved. Six new
actual outcomes and ten original/broader comparison observations pass 32
independent CLI validations. The broader results are equal in one case and
save 66.0529 / 266.0522 mm2 in two; the gap-filling case is 0.0388 mm2 worse
and leaves its named small part on the last sheet despite one recorded fill.
A logging-setup failure and shared-target stale executable are preserved;
recovery uses a fresh target and reuses all completed original observations.
Next inspect the intermediate fill and accepted snapshots before correcting
behavior or targeted tests. No assertion change, quality pilot, integration
or H5 credit; H2/H5 remain open at 60%.

**N4 mixed-pair diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-mixed-stage-20261018.md).
The two large-plate traces examine all 24 pair calls and 4,764 samples without
sample truncation, but retain no paired proposal. The area filter rejects
1,721 otherwise eligible samples, including 575 mixed samples. Panel traces
generate only the first same-item pair per kerf; all seven attempted paired
swaps reject unchanged inventory, and no mixed pair is generated. Their
repairs already have zero loss and each takes less than 0.0001 seconds;
remaining construction/validation time is not separately measured.
Overall, 28 attempts yield 19 failed source repairs, seven neutral rejections,
one material rejection and one accepted single swap saving 18.669 mm2
immediately. The filled-outer audit checks 18,626 pairs.
The next hypothesis targets the proposal-area filter with an authored runtime
regression; it is not a quality claim. H2/H5 remain open at 60%.

**N4 larger-return witness, 2026-10-18:** [a valid mixed pair exchange](../benchmarks/results/h5-larger-return-witness-20261018.md)
returns 2,790 mm2 of parts after removing 2,700 mm2, while keeping all seven
parts and every material metric unchanged at 19,700 mm2. Frozen CLI and
independent filled-outer checks validate both authored layouts. Eight
conservative height bounds exclude either selected incoming part moving
alone while one filler stays on each sheet. The current pair-area filter
excludes this complete return set. This proves a limitation of that filter,
with zero optimizer runs; an actual runtime regression and full candidate
checks remain necessary. It does not establish mechanical quality or H5.

**N4 mixed-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-mixed-exchange-pilot-20261018.md).
The independent filled-outer audit checks 133,299 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +6.069459%; m-mechanical-large-plates at 1.5 mm: +6.160993%; m-mechanical-panel-hardware at 0.2 mm: +6.770269%; m-mechanical-panel-hardware at 1.5 mm: +5.607046%
The candidate accepts 12/132 total exchanges, including 1/69
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 19 parts. The new guard rejects 49 same-inventory proposals without material improvement; mixed pairs account for 0/11 accepted/attempted exchanges. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

**N4 mixed-assignment witness, 2026-10-18:** [two distinct incoming rectangles](../benchmarks/results/h5-mixed-exchange-witness-20261018.md)
(30x40 and 30x50 mm) can exchange with three 30x30 mm squares. Both authored
layouts preserve all seven parts and exactly 19,700 mm2 material; frozen CLI
and independent filled-outer checks pass. Eight conservative height bounds
rule out either chosen incoming part moving alone while one filler remains
on each sheet, even if it moves. The two incoming parts have different IDs
and dimensions, so the current same-original-item selector cannot pair them.
This is a scoped geometric witness, with zero optimizer runs. It neither
proves global impossibility nor mechanical quality. The next candidate still
requires an original-runtime regression, allowed-pose/rollback tests and the
unchanged H5 quality gates. Production stays unchanged; H2/H5 remain open at 60%.

**N4 productive-exchange diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-productive-stage-20261018.md).
Of 28 attempts, 18 fail source repair, seven reject unchanged
inventory, one expires after repair, one fails the material guard and one
is accepted without immediate material/extent reduction. All eight paired
attempts preserve inventory; all twenty single attempts return more recorded
item area than they remove. The large-plate source's largest item has only
one copy, excluding it from the same-item pair selector. Requested source
windows range from -0.003617 to 0.398944 seconds, with 4 already
nonpositive. Timings do not prove minimum repair time or impossibility.
The independent outer audit checks 18,669 pairs. The
next hypothesis is bounded mixed-item pairs with authored correctness checks;
budgets and every geometry/material limit remain. No integration or H5 credit;
H2/H5 remain open at 60%.

**N4 productive-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-productive-exchange-pilot-20261018.md).
The independent filled-outer audit checks 133,603 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.483065%; m-mechanical-large-plates at 1.5 mm: +5.402498%; m-mechanical-panel-hardware at 0.2 mm: +7.022646%; m-mechanical-panel-hardware at 1.5 mm: +5.298801%
The candidate accepts 12/121 total exchanges, including 1/62
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 11 parts. The new guard rejects 45 same-inventory proposals without material improvement; these counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

**N4 post-exchange gap-fill outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-post-exchange-fill-pilot-20261018.md).
The independent filled-outer audit checks 133,374 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.484564%; m-mechanical-large-plates at 1.5 mm: +5.388338%; m-mechanical-panel-hardware at 0.2 mm: +6.386542%; m-mechanical-panel-hardware at 1.5 mm: +5.563315%
The candidate accepts 19/42 total exchanges, including 12/24
two-part exchanges. The post-exchange gap-fill step runs 19 times and moves 14 parts; these counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

**N4 pair-identity diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-balanced-stage-20261018.md).
There are 11 attempts and 3 accepted exchanges, including
2 pairs. 2 accepted exchanges return the
same original part types and quantities as they take; per-sheet inventory is
unchanged in those cases, although poses may change. Immediate material falls
in 0 accepted exchanges and last-sheet occupied
extent falls in 0. These traces do not reconstruct
the earlier pilot or prove a later benefit/harm from rearrangement. Retained
proposal identities, losses, material and extent are preserved. The independent
filled-outer audit checks 18,569 pairs. No gate relaxation,
production change, reserved-file access or H5 credit. H2/H5 remain open at 60%.
Source inspection also confirms that accepting an exchange short-circuits
the following gap-fill and relocation calls in that window. The next isolated
change should test whether gap filling after an accepted exchange can use its
new arrangement, while preserving the total search limit and normal-mode
behavior. This identifies a missed execution path, not a measured quality gain.


**N4 balanced-pair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-balanced-group-pilot-20261018.md).
The independent filled-outer audit checks 133,456 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.188368%; m-mechanical-large-plates at 1.5 mm: +5.469920%; m-mechanical-panel-hardware at 0.2 mm: +6.652162%; m-mechanical-panel-hardware at 1.5 mm: +5.589744%; c-bracket-mixed at 0.2 mm: +1.501017%
The candidate accepts 19/41 total exchanges, including 13/25
two-part exchanges. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

**N4 reuse-stage diagnosis, 2026-10-18:** [four diagnostic outputs validate](../benchmarks/results/h5-return-reuse-stage-diagnosis-20261018.md).
All 24 complete-obstruction exchanges repair the receiver, then fail source
repair. Sixteen resume a compatible saved state; seven reduce loss further,
none reaches zero, and none reaches final material/geometry acceptance.
The reader verifies original inventories and exact restored loss across each
reuse. The issue is incomplete repair, not observed cache-state corruption.
Each case spends 0.903–1.054 seconds in source repairs within the existing
early-call budget. Available windows shrink after successive attempts; three
late attempts reach source repair with an already-expired pair deadline and
return their unchanged state. These observed durations are not minimum required
repair times and do not prove that a larger allowance would solve H5.
Production and all failed results remain unchanged. H2/H5 remain open at 60%.

**N4 source-repair reuse outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-return-reuse-pilot-20261018.md).
The independent filled-outer audit checks 133,470 same-sheet
pairs across all 48 common-mode layouts, retaining hole reservation and kerf.
There are 6 failed material pairs out of eight under the original +1%
limit. m-mechanical-large-plates at 0.2 mm: +5.607522%; m-mechanical-large-plates at 1.5 mm: +5.124968%; m-mechanical-panel-hardware at 0.2 mm: +6.668421%; m-mechanical-panel-hardware at 1.5 mm: +5.745273%; c-bracket-mixed at 0.2 mm: +2.419752%; c-bracket-mixed at 1.5 mm: +1.016169%
The candidate records 11 accepted exchanges from 73 attempts and
37 compatible source-repair reuses. Reuse counts do not establish repair
completion or explain remaining failures. Reject this candidate for integration; do not open the full 13-job gate for it. Production, prior failures
and frozen inputs remain unchanged. H2/H5 remain open at 60%.

**N4 assignment feasibility, 2026-10-18:** [three independently valid source packings](../benchmarks/results/h5-assignment-repack-20261018.md)
fit the unchanged saved boundaries and quantities: both large-plate cases and
the 0.2 mm panel case. The 1.5 mm panel case remains unresolved after six retained
rounds. This proves only source-assignment feasibility, not whole-job material
improvement. Earlier traces repeat eight distinct assignments over 25 attempts
(17 repeats after first occurrence). Next test retained compatible repair progress
within the existing shared budget, preserving geometry/orientation identities,
tracker-key consistency, rollback and independent acceptance. No production change
or relaxed gate; H2/H5 remain open at 60%.

**N4 capacity diagnosis, 2026-10-18:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-capacity-diagnosis-20261017.md)
record 25 complete reciprocal attempts. Independent geometry checks confirm
clear repaired receivers and overlapping repaired return sheets. Source area
occupancy is 75.281–85.554% of the actual shortened search boundary: area alone
does not prove infeasibility, and occupancy alone does not prove a packing exists.
Next seek a complete, independently valid repack of fixed saved assignments with
their original boundary and legal orientations before changing repair. Preserve
all failed outcomes; no production change, relaxed limit or H5 credit. 60% complete.

**N4 return-frame diagnosis, 2026-10-17:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-frame-stage-diagnosis-20261017.md)
record 23 complete-set attempts. Every reciprocal frame is permitted and every
receiving-sheet repair succeeds, but all return-sheet repairs fail. None reaches
the final geometry/material guard. Orientation fallback is not the immediate
cause in these observations. Next inspect source capacity and placement of the
larger returned groups; area ratios alone do not prove impossibility. A [balanced two-to-three authored example now validates](../benchmarks/results/h5-balanced-exchange-witness-20261017.md)
at identical material; its scoped stacking bound explains why those single-incoming
choices cannot work. Mechanical source capacity/placement remains unproved.
Original results/limits remain; no production change or H5 closure. Completion 60%.

**N4 preceding return-frame outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-return-frame-pilot-20261017.md),
with an independent hole-reservation audit of 133,535 same-sheet
pairs across all 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.208689%; m-mechanical-large-plates at 1.5 mm: +4.649005%; m-mechanical-panel-hardware at 0.2 mm: +5.475484%; m-mechanical-panel-hardware at 1.5 mm: +5.886483%
There are 11 accepted exchanges from 71 attempts.
Reject this candidate for integration; do not open the full 13-job gate for it. Production remains unchanged. Counters alone do not establish the
remaining repair bottleneck or impossibility. H2/H5 remain open at 60%.

**N4 preceding diagnostic, 2026-10-17:** [four traced outputs validate](../benchmarks/results/h5-complete-stage-diagnosis-20261017.md),
but all 23 complete-set attempts fail return-sheet repair after the receiving
sheet succeeds. Investigate return-group initialization/repair within the
existing budget and material guard. This locates a stage, not an impossibility
proof or quality gain; the failed paired comparison remains the outcome.

**N4 preceding complete-set outcome, 2026-10-17:** [all 72 complete-set pilot outcomes validate](../benchmarks/results/h5-complete-set-pilot-20261017.md),
but all four mechanical pairs still fail the +1% material limit, at +5.433792%
to +6.521291%. All four control pairs pass the material limit. The separate
filled-outer audit confirms all 48 common-mode outputs keep holes reserved.
There are 74 exchange attempts and eleven acceptances, none on panel hardware.
The candidate is rejected for integration; the full 13-job gate is not started.
Original results/limits remain; H2/H5 are open at 60%.

**N4 diagnosis, 2026-10-17:** [four current-candidate traces](../benchmarks/results/h5-obstruction-stage-diagnosis-20261017.md)
validate all layouts but show zero complete blocker-set proposals: 620 sampled
sets fail the smaller-area heuristic. All 29 attempted exchanges are partial;
27 fail receiving-sheet repair and two succeed. An [independently validated
authored witness](../benchmarks/results/h5-area-witness-20261017.md) demonstrates
that returning more combined part area can preserve both validity and material.
The first incorrectly oriented witness is retained with its failed material
assertion. This motivates a separately tested complete-set eligibility change;
it proves no mechanical feasibility or quality gain. Production stays unchanged,
and H2/H5 remain open at 60% completed weight.

The [completed obstruction-set pilot](../benchmarks/results/h5-obstruction-set-recovered-pilot-20261016.md) validates all 72 outcomes but fails five of eight material pairs. All four mechanical pairs remain +4.663095% to +5.962959% above ordinary mode; mixed-bracket laser is +1.540301%. There are 147 exchange attempts and ten acceptances, none on panel hardware. The candidate is rejected for integration; all failed outcomes and original limits remain preserved. H5 stays open.

### Earlier v1.1 checkpoints

The following entries preserve the state at each checkpoint, including failed
candidates and work that was then outstanding. Their completion percentages
and release plans are historical; the milestone table and dated updates above
describe the current state. Source evidence and original results remain unchanged.

Earlier N4 experiment: the [isolated directed exchange](../benchmarks/results/h5-directed-exchange-functional-20261016.md)
passes six focused tests, 80 core tests (one existing ignored), six common-line
geometry tests and eight authored public-CLI checks. It returns a smaller actual
obstruction and repairs both sheets before independent whole-job acceptance.
Original failures are retained. The [completed paired pilot](../benchmarks/results/h5-exchange-pilot-v2-20261016.md)
has 72 valid outcomes, but all four mechanical/kerf medians still fail the +1%
material limit, at +4.175294% to +5.869406%. None of its 24 candidate runs attempts
an exchange. Two [debug path observations](../benchmarks/results/h5-exchange-path-20261016.md)
also validate and show that neither reaches the exchange call. The candidate
remains unintegrated. A [new isolated early call point](../benchmarks/results/h5-early-exchange-preparation-20261016.md)
now passes seven focused checks, 82 optimized core tests and authored API/CLI
repeatability checks. Its full-window test reaches and accepts an exchange;
ordinary mode remains exact except elapsed wall time. A [new paired pilot](../benchmarks/results/h5-early-exchange-pilot-20261016/plan.json)
has now [completed with all 72 layouts valid](../benchmarks/results/h5-early-exchange-pilot-20261016.md).
It reaches 179 proposals and accepts ten exchanges, but every mechanical/kerf pair
still fails the +1% material guard (+5.324324% to +6.390250%). The laser bracket
control also fails at +1.251430%. The candidate is rejected for integration;
the full 13-job gate is not started. Earlier call reachability does not establish
sufficient material improvement. An [isolated stage observer](../benchmarks/results/h5-exchange-diagnosis-preparation-20261016.md)
passes its build, 82 core tests and three trace checks. Its [completed diagnosis](../benchmarks/results/h5-exchange-diagnosis-20261016.md)
validates all four layouts: 35 of 37 attempts fail receiver repair, all with two
or three blockers when only one is removed. The two accepted exchanges do not
establish a quality gain. Moving a complete smaller obstruction set is a possible
next hypothesis. An [isolated obstruction-set candidate](../benchmarks/results/h5-obstruction-set-preparation-20261016.md)
now passes 85 core tests, strict lint and authored public comparisons; no new
quality run or integration has occurred. Its [committed 72-attempt pilot](../benchmarks/results/h5-obstruction-set-pilot-20261016/plan.json)
waits for the entire current H4 sequence. Original reader/report failures and
all measured outcomes remain.
The original unopened pilot, revised scheduling rationale,
shared-target cache failure and all measured outcomes remain preserved. H5 stays
open; no material limit changes. Only the proven score-bound change is selected
for the next release candidate.

Earlier N2 checkpoint: [H3 completed](../benchmarks/results/h3-complete-20261015.md). The plan was committed before the three reserved projects were opened; all passed with 199 leaves / 247 contours, a maximum point difference below 0.000500 mm, nine allowed canonical sheet comparisons and exact validation metrics. The five native-checked layouts revalidate on the current build; all 298 original native evidence files and 1,181 frozen inventory files retain their hashes. Milestone completion is now 45%. H2 import acceptance, H4 browser/native performance and H5 material use remain open.

Earlier N3 checkpoint: the [complete integrated score-bound matrix](../benchmarks/results/h4-preview-score-release-20261016.md)
is sealed with 603 new and 195 reused valid layouts. Native median material is
+0.000681% versus frozen v1; full G5 Chrome is +0.091358% median/+0.384971% total,
and Firefox +0.026372%/+0.346902%. All individual-seed G5 checks pass. The curve
subset remains the failure: Chrome +1.032679% versus +1%; Firefox +0.881781% passes.
No scale run or release follows. [Current CPU profiles](../benchmarks/results/h4-browser-profile-20261016T040030Z.md)
identify traversal as the main sampled cost; a shallower collision tree is the next isolated hypothesis. The [requirement preflight](../benchmarks/results/h4-requirement-preflight-20261016.md)
and [independent export-checker preparation](../benchmarks/results/h4-export-fidelity-preparation-20261016.md)
remain supporting evidence, not H4 closure. Completion stays 45%.

Earlier N1 export verification: [current public replay](../benchmarks/results/h2-export-replay-20261015.md) re-imports all 246 accepted training vectors with identical geometry and validates/exports their saved layouts without new searches. Of 492 outputs, 491 are byte-identical. One SVG retains a failed byte comparison but passes a separate unchanged-limit geometry check: endpoint movement below 0.000001 mm bounds its source fidelity at 0.000491918 mm, below 0.01 mm. All original failures and 3,942 raw members are preserved. Native diagnostic fixes are now integrated and verified below; the remaining reserved evaluation still prevents H2 closure.

Earlier N1 review: the [earlier native diagnostic audit](../benchmarks/results/h2-native-warning-review-20261015.md) retained 45 imports and eleven clear rejections across 56 training records. It identified twelve missing bounding-rectangle explanations, L28’s missing line-fallback message and L40’s missing cached-text explanation; geometry and preservation evidence stayed intact. An [isolated diagnostic candidate](../benchmarks/results/h2-native-diagnostics-candidate-20261016.md) now passes all 56 training checks and 23 focused tests: all 45 libraries retain exact geometry/XML and all eleven errors remain identical. The first failed wording check and dependency-inventory preflight remain preserved. The [subsequent surface review and training audit](../benchmarks/results/native-diagnostics-surfaces-20261016.md) remove repeated warnings and pass all 56 records plus CLI/MCP/both-browser tests. The candidate is now integrated and production checks pass. The [H2 requirement review](../benchmarks/results/h2-requirements-review-20261016.md) connects current source to the warning and fidelity evidence for all 313 training inputs. Reserved acceptance and the denominator clarification remain open; H2 stays open.

Earlier N4 inspection: [saved final-sheet assignments](../benchmarks/results/h5-last-sheet-inspection-20261015.md) show that one failed large-plates assignment cannot meet the material guard by compression alone. This supports investigating exchanges between sheets, not a whole-problem impossibility claim or a gate change. No new H5 searches ran.

The [historical relocation-counter review](../benchmarks/results/h5-relocation-inspection-20261016.md)
verifies all 36 archived schedule results. Default-schedule trials already have
12 successful and 180 failed separated insertions; ordinary receiver insertion
is active. A directed exchange that also returns a blocker to the last sheet
remains a distinct, unmeasured hypothesis. No new search or H5 credit.

Earlier N3 follow-up: the [isolated compiler pilot](../benchmarks/results/h4-lto-probe-20261015.md) validates all 44 layouts and eight additional example library/request checks. Fat LTO gives a small Chrome improvement but worse Firefox material and charged-work rate; it is not integrated. The production build, original failed quality subset and H4 thresholds are unchanged. Completion remains 45%.

The following earlier checkpoint notes retain the completion percentages and failures recorded at their dates. The current total is the 45% stated above.

Earlier N4 follow-up: [48 material diagnostics](../benchmarks/results/h5-material-probes-20261015.md) all validate, but extra warm-start time and rigid bracket pairing worsen every mechanical-job/kerf median. Both remain unintegrated; H5 stays open and completion remains 20%.

Earlier N3 quality measurement: [all 99 subset layouts validate](../benchmarks/results/h4-quality-checkpoint-20261015.md). Firefox passes with +0.486636% median material; Chrome narrowly fails at +1.014665% against +1%. Every individual job is within +5%. The full G5 and 195-run native comparisons remain outstanding. No threshold, held-out allocation or published result changes; completion stays 20%.

Earlier N3 checkpoint: [automatic worker selection](../benchmarks/results/h4-worker-policy-20261015.md) passes the curve-heavy scale workflow in both browsers and preserves the original G5 scale settings and pass. Actual worker lifetimes confirm one search worker for H4 and two for G5. Independent native checks agree exactly, and the H4 layout and cutting-file bytes remain unchanged. The worker threshold is a heuristic; H4 quality and native gates remain open. All 80 enabled browser tests pass; completion is 20%.

Earlier N3 checkpoint: [collision-layout lifetimes](../benchmarks/results/h4-layout-lifetimes-20261015.md) remove redundant collision-index copies and release a temporary layout before search. Both actual browsers pass the scale limits with one selected worker, with unchanged layout/export bytes. The default two-worker setting still fails: working sets 1.573/1.543 GB, private peaks 1.789/1.611 GB, and Firefox heartbeat 290 ms. All raw successes and failures remain; worker defaults have not changed. Repeatable comparisons, all 287 workspace tests and 74 browser tests pass. H4 remains open and completion is 20%.

Earlier N3 checkpoint: [Quick initial layout](../benchmarks/results/h4-quick-start-20261015.md) is available through UI, CLI and MCP, off by default. All six isolated incumbent probes and the complete native run validate. Both actual browser workflows now finish and export, but exceed memory and responsiveness limits. Original validator-binary guard failure and separate saved-artifact rechecks are retained. All 287 workspace tests, 24 optimized CLI tests and 60 enabled browser tests pass; final source preflight tests, strict lint, schema consistency and builds pass. Next work targets preview costs, download assembly and worker memory. H4 is incomplete and completion remains 20%.

Earlier N3 baseline: the [frozen 2,000-part letters/gears scale baseline](../benchmarks/results/h4-curve-scale-baseline-20261015.md)
fails initial packing in both Chrome and Firefox at 60 seconds. Memory peaks at
0.87/0.92 GB and observed responsiveness remains below 200 ms before failure;
export is not reached. Native also fails at 60 seconds, but a 300-second
diagnostic completes with all 2,000 placements valid on three sheets. Its first
warm layout arrives at 138.21 seconds. An independent shelf layout also validates,
so a fast conservative starting layout is a concrete next experiment. No solver
change is integrated, H4 remains open and completion stays 20%.

Earlier N1 checkpoint: [complete vector fidelity, shop-habit fuzzing and diagnostic coverage](../benchmarks/results/h2-habits-checkpoint-20261014.md).
All 246 importable vectors re-export within 0.01 mm; the other 11 reject clearly.
The new 10,000 import and 1,008 nesting cases pass, and expected diagnostics and
cut layers match every import. Undefined DXF layers and duplicate handles now
warn without changing geometry. Independent Gherkin analysis confirms a retained
closed-path retrace, with no label exception. All 205 workspace, 20 optimized CLI
and 48 browser tests pass (one existing ignored, four opt-in browser cases skipped).
H2/H3 remain incomplete; milestone total stays 15%.

The [Linux CI search-fuzz panic](../benchmarks/results/ci-search-panic-20261013.json) at `540c867` is [fixed and locally verified](../benchmarks/results/ci-quadtree-fix-20261013.md): reject separator moves whose actual outline misses the collision grid, even when their bounds overlap it. All 189 workspace tests pass (one existing test ignored), including the saved case; the optimized regression, strict Clippy and WASM check also pass. The `f496ae5` Windows run was cancelled by the next push after its other jobs passed. Its successor at `36670a3` has passed Linux, web, both corpus rebuilds and benchmark smoke in [CI](https://github.com/skulitom/Nestbolt/actions/runs/38482331099); Windows checks remain in progress as of this checkpoint.

Earlier N2 surface checkpoint: 194 workspace tests pass (one existing ignored),
19 optimized CLI feature tests and 46 enabled browser tests pass. LightBurn import,
real search, per-sheet LBRN2 and ZIP exports work through CLI/MCP/UI; native H3
acceptance and the documented remaining format cases are still open.

Earlier N2 format checkpoint: [legacy conversion and native T1 ordering](../benchmarks/results/h3-legacy-20261013T235803Z.md).
The native identity save matches the entire native-converted project; 37 independent
leaf comparisons pass within 0.000497 mm. A six-unit search exports one validated
sheet, including T1 after the ordering fix. Initial failures and generated Tool
default normalization remain documented. 198 workspace tests pass (one ignored),
the final 18 focused core tests and two optimized CLI LightBurn tests pass, and
four focused browser tests pass. H3 remains incomplete; milestone weight stays 15%.

Earlier N2 native checkpoint: [five actual searched projects](../benchmarks/results/h3-lightburn-20261014T001636Z.md) open
without warnings in LightBurn Pro 2.1.01, using default and top-right device
origins. All original settings remain exact, all 16 units match native position
and size fields within 0.003652 mm, and 409 native leaf comparisons pass. The
initial incomplete observation and identical-copy association failures remain
recorded. Device settings and the hidden desktop were restored. Frozen integrity
is unchanged at 1,181 files. This completes the five-project native requirement,
not H3 as a whole; the goal remains active at 15%.

CI for `cded7fe` has passed all six jobs: Linux and Windows checks, web, both
corpus rebuilds and benchmark smoke
([run](https://github.com/skulitom/Nestbolt/actions/runs/38488685177)).

## v1 — accepted

**Completion: 100% on Artem's acceptance (plan decision 5, 2026-10-13).** M0-M4 met their gates. M5 closed when Artem accepted the published final run: G1, G3, G4 and G2 at 300 s are met; G2 at 60 s is not met as written (85.7% wins or ties against the 90% required, two jobs more than 1% worse, every loss against Sparrow).
Percentages count completed milestones only. Development results do not establish the final acceptance gates. All failures and earlier trials remain in
[BENCHMARKS.md](../BENCHMARKS.md). The ten held-out maker jobs were used once, in the final acceptance run, and never for tuning.

| Milestone | Weight | State / next requirement |
| --- | ---: | --- |
| M0 — Groundwork and reproduction | 5% | Complete: 39 valid runs; all 13 means within the frozen 1% threshold |
| M1 — Baseline | 15% | Complete: all 1,878 declared slots audited; [target frozen at 10.77231474%](M1_BASELINE.md) |
| M2 — Sheet optimiser | 25% | Complete: [development matrix](../benchmarks/results/sheets-m2-60s-s0-20261012T144634Z-10b9520f.md) 225/225 valid at 60 s and 300 s; G3 strip parity median −0.039%, worst +1.65%; G4 8/9 (88.9%). 60 s medians: 48/52 wins/ties, median 8.44% (G2 is M5) |
| M3 — Part-in-part and import/export | 15% | Complete: [fidelity](../benchmarks/results/g6-fidelity-20261012T161009Z-310d54b1.md) on 196 real drawings within 0.0005 mm, curves kept, mm and inch correct; Inkscape and LibreCAD open the exports; [LightBurn 2.1.01](../benchmarks/results/g6-lightburn-20261012T170036Z.md) imports all five at the exact placed sizes |
| M4 — Browser app and MCP | 20% | Complete: [Pages app](https://skulitom.github.io/Nestbolt/) with five examples and a live view; G5 [quality](../benchmarks/results/g5-browser-60s-s0-20261012T182218Z-032f0985.md) (WebAssembly vs native at 60 s on 65 jobs: median +0.02% Chrome 154, +0.07% Firefox 157, total +0.9%), [scale and responsiveness](../benchmarks/results/g5-scale-20261012T192645Z-39d0cca0.md) (2,000 parts imported, nested and exported, peak 1.05/1.16 GB, longest task 106 ms), hosting re-checked live; G7 real Claude Code run, CLI and UI end-to-end tests for every v1 item, MCPB and `mcp-publisher` validation in a [release dry run](https://github.com/skulitom/Nestbolt/actions/runs/38300373491) |
| M5 — Final gates | 20% | **Closed on Artem's acceptance (decision 5); G2 at 60 s not met as written.** [Final acceptance run](https://skulitom.github.io/Nestbolt/results/) (2026-10-13, seeds 1000-1004, held-out jobs, build `75cbb32`): G1 every layout valid (375/375 at 60 s, 60/60 at 300 s, 60/60 at 30 s, 65/65 strips); G2 at 300 s met (median 9.61%, 11/11, worst +0.84%); G2 at 60 s median 8.52% but 48/56 wins or ties (85.7%) and two jobs more than 1% worse (m-garment-bruce-1 −2.37%, b-jakobs1-strip-sheet −2.09%), all eight losses against Sparrow, seven on one-sheet jobs Nestbolt delegates to Sparrow; G3 median −0.002%, worst +0.72%; G4 10/11; G8 one command and the results page from those records. The first final run (`484ce8b`) crashed on one job (G1); [its page](https://skulitom.github.io/Nestbolt/results/final-484ce8b/) stays published |

| Evidence | Current result | Next step |
| --- | --- | --- |
| Published Sparrow reproduction | 39/39 layouts valid; 13/13 instance means pass; worst absolute difference 0.986671% | [Final proof](../benchmarks/results/m0-published-20261011T215820Z-10a30c6f.md) |
| Frozen datasets | 13 strip, 35 sheet, 40 maker jobs; 10 maker jobs held out | Use only development cases for tuning |
| LBF development matrix | 450/450 attempts; 283 valid, 5 invalid, 162 unsupported | Complete; [table](../benchmarks/results/comparison-session-20261011T221209Z-ce35672e.md) |
| SVGnest | All 450 development slots complete. At 60 s: sheets 103/105 identical and 85/105 expanded valid; makers 1/90 identical and 0/90 expanded. At 300 s: sheets 18/18 and 15/18; makers 3/12 and 0/12 | [Final expanded sheet table](../benchmarks/results/comparison-batches-20261012T021336Z-74941dfd.md), [final expanded maker table](../benchmarks/results/comparison-batches-20261012T023246Z-a5cc0290.md); no further development runs |
| Deepnest | All 450 development slots complete: 330 valid, 30 invalid, 88 no layout, two timeouts. At 300 s: both sheet settings 18/18 valid; makers identical 4/12, clearance-safe 9/12 | [Final maker identical](../benchmarks/results/comparison-batches-20261012T032935Z-846373a4.md), [clearance-safe](../benchmarks/results/comparison-batches-20261012T033500Z-e03868ab.md) |
| Current Sparrow | All 528 development slots accounted for: 127 valid, 43 invalid, 358 unsupported; both settings, both budgets, three seeds | [Complete coverage](../benchmarks/results/sparrow-development-20261012T0048.md); final-seed comparisons remain for M5 |
| Nestbolt search | All 65 development layouts valid. Repeated compression improves one sheet score (1.69%) and four maker scores (up to 0.30%) over v13, with zero regressions. Skipping unsuccessful repeats preserves every score | [35 sheets](../benchmarks/results/repack-sheet-20261012T035142Z-a7b22154.md), [30 makers](../benchmarks/results/repack-maker-20261012T035142Z-54130739.md); fixed-work diagnostics, no equal-time gate |
| Longer search | Up to 1,024 passes, preserving the first finished 64-pass block. A four-job 512-pass pilot improves Jakobs1 by 2.46% and Marques by 4.20%; the other two retain their 64-pass result | [All four cases](../benchmarks/results/progressive-pilot-20261012T0433.md); 80M query allowance and 60 s safety deadline, selected cases with extra work |
| Placement diversity | Combining original and varied placement strategies reduces Blaz1 from 12 sheets to 10 (16.28% less material), improves Bruce by 2.99%, and retains the preceding Jakobs1 and Marques scores. All four layouts independently valid | [Four-case evidence and rejected trial](../benchmarks/results/placement-diversity-20261012T045248Z.md); up to 1,024 passes, same 80M-query/60 s controls; broaden development coverage next |
| Repair collisions | The first broad run had two invalid late repairs (Shapes0/Shapes1, nearly coincident parts), caught by the independent checker before export. Repair now unions interior-pole and polygon collisions; both exact fixtures pass and replay identically | [Regression evidence](../benchmarks/results/repair-pole-collisions-20261012T052215Z.md); [original failures](../benchmarks/results/search-coverage-20261012T050634Z.md) retained |
| Native strip parity | 39/39 outputs valid at 60 s, seeds 0/1/2. Median regression −0.0390%; worst +1.6493%, against the better Sparrow setting per job. Development thresholds pass | [Audited comparison](../benchmarks/results/strip-development-20261012T040418Z-961c9a96.md), [adapter scope](STRIP_PARITY.md); final-seed G3 acceptance remains |
| Repeatability and rollback | Two compression replays have identical complete outputs. Tests preserve the full repacking history, other sheets and the valid incumbent when interrupted | [Compression replay](../benchmarks/results/compression-replay-20261012T0326.json); previous [blaz1 repair replay](../benchmarks/results/shallow-replay-20261012T0255.json) |
| Quality triage | Combined search on all 65 development jobs (seed 0, up to 1,024 passes / 80M queries / 60 s): 65/65 valid; vs 52 finite 60 s competitor medians 27 wins/ties, 15 more than 1% worse, median reduction 0.396716%. Thirteen jobs have no finite competitor | [Corrected coverage](../benchmarks/results/search-coverage-20261012T051749Z.md); the frozen G2 target is 10.77231474%, so sheet search needs a much stronger separator |
| Sheet separator | `nestbolt sheets`: warm start, then the last twelve sheets as one walled strip; the last sheet's free end is a pinned blocker (several sheets) or a shrinking container (one sheet). Three development seeds, 60 s, pinned CPUs: 195/195 valid; per-job median 48/52 wins/ties (92.3%); one job more than 1% worse (jakobs1 strip-sheet, -1.7%); median reduction **8.2619%** | [Seed 0](../benchmarks/results/sheets-eval-fixed-s0-20261012T125826Z-fd1af61e.md), [1](../benchmarks/results/sheets-eval-fixed-s1-20261012T130725Z-ece55c03.md), [2](../benchmarks/results/sheets-eval-fixed-s2-20261012T131624Z-24a17328.md); all earlier and interrupted batches in BENCHMARKS.md. All four losses are single-sheet jobs where Sparrow leads |
| Speed (G4-style) | 30 s runs vs the frozen 300 s competitor medians, three seeds, with the rectangle warm start: 195/195 valid; **8 of the 9** jobs with a finite 300 s median reached (88.9%); m-box-mini ties at 0.6660, jakobs2 strip-sheet misses by 2.7% | [Seed 0](../benchmarks/results/sheets-ab-rects-30s-s0-20261012T142836Z-c9d2a6d1.md), [1](../benchmarks/results/sheets-ab-rects-30s-s1-20261012T143305Z-524036e1.md), [2](../benchmarks/results/sheets-ab-rects-30s-s2-20261012T143733Z-b0a39fa9.md); previous build 7/9 |
| Browser app | Same engine in WebAssembly Web Workers, several seeds in parallel; five bundled examples, live view of the best layout, offcut and bounding box per sheet; import, nest, export, defects, remnant outlines, several sheet sizes, fill modes, IndexedDB and ZIP projects | 22 Playwright tests (11 × Chromium and Firefox) in CI; [G5 quality](../benchmarks/results/g5-browser-60s-s0-20261012T182218Z-032f0985.md) and [scale](../benchmarks/results/g5-scale-20261012T192645Z-39d0cca0.md) pass; the four detailed-gear jobs remain 16-30% worse in one browser worker (half the native search rate) |
| MCP server and packaging | Five tools, workspace confinement, no overwrites, repeatable work budgets; end-to-end stdio test. JSON Schemas for library, request and report. MCPB bundle, native archives and release/registry workflows (dispatch or tag only) | 20 Node packaging tests pass, including a real bundle import-nest-validate smoke test; [v0.1.0 released](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0) on 2026-10-14 |
| Export fidelity (G6) | 196 drawings (fixtures, example parts, 192 boxes.py examples): imported, nested, exported to SVG and DXF and re-imported; 29,308 contours, none unmatched, largest distance 0.0005 mm (SVG) and 0.0000045 mm (DXF) | [Passing report](../benchmarks/results/g6-fidelity-20261012T161009Z-310d54b1.md); `python scripts/g6_fidelity.py`. It found and fixed self-touching boxes.py outlines, DXF chaining and single-precision collisions |
| Export opening (G6) | Fidelity fixtures (mm SVG with arcs, ellipses and Béziers; inch DXF with bulges, holes and arcs) nested and exported; Inkscape 1.4.4 (SVG and DXF) and LibreCAD 2.2.1.5 (DXF) report the placed drawing size within 0.04-0.27 mm | [Passing report](../benchmarks/results/g6-open-20261012T144206Z-4e0d95be.md); two earlier method failures retained; `python scripts/g6_open_check.py` |
| Real MCP client (G7) | Claude Code 2.1.280, `claude -p --mcp-config <file> --strict-mcp-config`, Nestbolt tools only: lists the tools, imports an SVG, nests with a 10 s budget, exports; the independent validator accepts the layout | [Passing report](../benchmarks/results/g7-claude-20261012T145002Z-3180a8d5.md); two earlier attempts retained; `python scripts/g7_claude.py` |
| Search limits | 1,000-part job returns a valid incumbent in 15.094 s under a 15 s cooperative deadline; two fixed-work replays produce identical results | [Stop and replay evidence](../benchmarks/results/search-control-20261012T0114.md); calibrate time-to-work mapping and wire browser/MCP cancellation |
| Compaction | All 65 layouts valid; seven sheet and ten maker improvements retained. Bounded relocation preserves every material score and reduces collision queries by 24% overall; original-geometry guard prevents material regression | [Sheet trial](../benchmarks/results/compact-b-20261012T013650Z-e3423fac.md), [maker trial](../benchmarks/results/compact-m-20261012T013654Z-fb5e8bfa.md); remains optional while stronger sheet repair is developed |
| Constructor speed diagnostic | Stable cost order cuts 1,000-part collision checks from 9.33M to 4.39M; last matched-CPU pair uses 61.8% less CPU time with identical output | [All ten timing attempts](../benchmarks/results/construct-profile-20261012T0042.md); four-circle experiment reverted; no G4 claim |
| Independent checker speed | Reusing clearance outlines cuts validation CPU by a further 17.0% on the gear job and 13.8% on the 1,000-part job. Full-search outputs and all 104 retained validation reports remain identical | [Reuse timings](../benchmarks/results/clearance-cache-20261012T0433.md), [preceding distance-pruning trial](../benchmarks/results/validator-speed-20261012T0420.md); no G4 claim |
| Repository and hosted checks | [Public repository](https://github.com/skulitom/Nestbolt) since 2026-10-12, Pages live | [v0.1.0 release](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0) and [registry publication](https://github.com/skulitom/Nestbolt/actions/runs/38540517654) completed on 2026-10-14 |

The [complete baseline audit](../benchmarks/results/baseline-gap-20261012T033547Z-e9539412.md)
measures competitor reductions over LBF of **17.09% at 60 s** and **21.54% at 300 s**.
The target frozen from it (10.77231474%) was waived by Artem on 2026-10-12
([plan decision 4](PLAN.md)); the G2 median condition is the base 5%.
Missing finite comparisons remain explicit and never earn free wins.

Final acceptance (2026-10-13). The competitors ran first (Deepnest 870/870 slots,
SVGnest 870/870, Sparrow 1,000/1,000; one Deepnest harness fault before solving was
replaced and logged). Nestbolt's frozen `484ce8b` then crashed on b-albano-strip-sheet
(seed 1004, 60 s): a repacking trial its own check rejected was treated as fatal. The
fix (`75cbb32`, regression test) was frozen before any G2 number of the final run was
seen, and Nestbolt's final run was repeated in full against the same competitor
records. Both runs are published. G2 at 60 s is not met by either, with every loss
against Sparrow: on seven one-sheet jobs Nestbolt hands Sparrow's own problem to
Sparrow after its first layout, so Sparrow runs with slightly less time. Further
tuning against these results would use the held-out jobs, which the plan forbids. On
2026-10-13 Artem accepted the results as published (plan decision 5), which closes M5.
Next work is in [PLAN_V1_1.md](PLAN_V1_1.md); any new benchmark claim needs a new final
run with a fresh held-out set.

[Ties, failure coverage and the baseline-gap formula](../benchmarks/STATISTICS.md)
are now explicit. No competitor result means no free win. The [verified 10.6417% single-seed gap](../benchmarks/results/pilot-gap-feedback-20261011.md)
is superseded by the complete three-seed M1 audit. Both 60 s and 300 s G2
populations must pass separately.

The independent checker covers original geometry, spacing, quantities, units,
stock, margins, defects, rotations, mirroring and fill mode. The latest full local
checks passed 112 workspace tests, four stock-helper tests, both WASM builds,
source/schema/notices checks, 94 Python tests, 20 Node packaging tests and the
6 browser tests (3 each in Chromium and Firefox). Five Node tests cover CPU
selection and native process cleanup.

[Competitors were rechecked](UPSTREAM_REVIEW.md) before M2. The Sparrow Studio
stop condition was not triggered at that review. v0.1.0 was subsequently released
and published to the MCP Registry on 2026-10-14.
