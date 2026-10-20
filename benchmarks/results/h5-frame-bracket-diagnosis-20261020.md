# H5: new frame arrangements and bracket capacity — 2026-10-20

**Four new complete frame arrangements fail because too few brackets can
coexist.** Exact rational certificates bound their bracket counts at **7, 7, 10
and 10**, below the original 12. No complete layout or improved partial is found.
The next construction must choose frames and brackets together. H2/H5 remain
open at 60%; no release or product change is qualified.

## Whole frames with fractional smaller parts

Following the [previous diagnosis](h5-whole-group-diagnosis-20261020.md), four
mixed-integer feasibility models fix one original complete cog arrangement,
require 18 whole frames, and retain the exact 12-bracket and 21-insert sums while
relaxing those smaller parts to fractions. All original conflicts and audited
local area capacities remain. The 26 reviewed exact frame sets are excluded:
nine receive explicit sum-at-most-17 rows and seventeen already contain a pose
absent from the model. Only the 2,213 frame variables are integral, among 6,786
variables. Every row, bound, exclusion and integrality change is independently
checked before solving.

Each case has one declared **30-second limit**, eight workers and seed zero.
All four expire without an incumbent; slight solver cleanup overruns are
preserved. No suffix is retried and no fractional or physical layout is returned.

| Cog case | Seconds | Outcome |
| --- | ---: | --- |
| 0 | 30.524422900 | Time limit, no incumbent |
| 1 | 30.085924400 | Time limit, no incumbent |
| 2 | 30.092550400 | Time limit, no incumbent |
| 3 | 30.152175600 | Time limit, no incumbent |

These are bounded failed constructions, not infeasibility proofs.

## A changed frame-only construction

A separate declared model selects exactly 18 whole frames compatible with the
fixed cog arrangement, retaining all frame conflicts and excluding all 26 old
sets. It ranks frames by how few existing smaller-part poses each blocks. The
integer cost is proportional to the sum of normalized blocked bracket and
insert fractions. Shared blocked positions may be counted more than once;
this is explicitly a heuristic, with no area or completion guarantee.

All four Boolean models and every cost are independently reconstructed from the
original conflict cliques. Each case declares **10 seconds**, eight workers and
seed zero, without a retry. All four reach the heuristic optimum:

| Cog case | Seconds | Returned incumbents | Heuristic cost |
| --- | ---: | ---: | ---: |
| 0 | 1.118507400 | 8 | 6049707 |
| 1 | 1.154241300 | 8 | 6116660 |
| 2 | 0.904616300 | 1 | 6614864 |
| 3 | 0.889440000 | 2 | 6706531 |

All **19 returned frame/cog proposals** pass original filled-outer geometry,
allowed rotation, stock, margin and clearance checks. Each has all 18 frames and
15 cogs. Each case's final frame set is new, and the four final sets are distinct.
Only those four final sets proceed to completion. This stage places no brackets
or inserts and has no full-job credit.

## Exact completion and the reason for failure

Four new completion models fix those final frame/cog groups, require 12 whole
brackets and maximize inserts up to 21. Their surviving candidate counts are
308, 452, 695 and 754. Every model is independently reconstructed, and 46,017
original same-sheet pairs between fixed parts and surviving candidates are
checked before solving. The adapter starts from hash-verified sealed scripts;
every scope change is retained explicitly.

Each completion has one declared **20-second limit**, eight workers and seed
zero. All four return `INFEASIBLE` in 0.0183, 0.0176, 0.1979 and 0.3066 seconds.
They return no incumbent, so no new frozen CLI validation is claimed.

To identify the obstructing quantity, a further necessary relaxation removes
every insert and maximizes the simultaneous bracket sum, retaining every
bracket conflict and unit variable bound. Four declared ten-second LPs finish
in under 0.01 seconds each. Their saved duals are converted into exact rational
upper bounds and independently reconstructed using Python `Fraction`:

| Cog case | Individually available bracket poses | Exact bound, decimal display | Integer bracket upper bound |
| --- | ---: | ---: | ---: |
| 0 | 104 | 7.448898678414 | **7** |
| 1 | 111 | 7.708333333333 | **7** |
| 2 | 290 | 10.985347985348 | **10** |
| 3 | 340 | 10.818681318681 | **10** |

For minimization of minus the bracket sum, any nonpositive inequality
multipliers give a lower bound from their row totals plus the minimum reduced
cost over each unit interval. All coefficients and right-hand sides are integers;
binary64 multipliers are interpreted as exact dyadic rationals. This avoids
rounding a solver objective into a proof. Exact numerators and denominators,
all primal/dual vectors and both arithmetic reconstructions are saved.

Thus these fixed frame/cog groups cannot fit the required 12 brackets **from
their finite original pose pools**, even without inserts. The certificates do
not bound arbitrary continuous arrangements. Counting individual available
poses had concealed their mutual conflicts; the frame-only ranking is rejected
as a sufficient construction criterion.

## Next work and repository state

The four heuristic frame arrangements fail the exact 12-bracket quantity even when all inserts are removed: their independently certified integer bracket upper bounds are 7, 7, 10 and 10. Reject this additive pose-availability score as a sufficient construction criterion. Next build a bounded construction that selects all 18 frames and 12 brackets simultaneously with one full cog arrangement, preserving their original conflict cliques and exact quantities. Insert availability may guide ranking but cannot replace a separate exact 21-insert completion test. Exclude the 26 previously reviewed exact frame sets and retain all failed cases and any returned groups. Declare limits before solving; do not extend the four expired mixed models or rerun these rejected fixed groups unchanged. Any full original 66-copy layout still needs the frozen CLI, independent filled-outer geometry, native margins and unchanged full H5 material/cutting gates. H2 remains open under Artem’s original-denominator decision.

The original candidate geometry, stock, targets and all gate thresholds remain
unchanged. There is no held-out access, native packing, quality run, full new
layout, runtime change or new release. All three README hashes still match the
current hosted-preview description. Main remains at pushed **f6edfb7**, with its
separate [hosted check snapshot](h5-frame-bracket-diagnosis-20261020/main-ci-f6edfb7.json) retained. This
diagnostic checkpoint is local until a subsequent recorded push.

[Checks](h5-frame-bracket-diagnosis-20261020/checks.json), [mixed outcomes](h5-frame-bracket-diagnosis-20261020/mixed-results.json),
[frame audit](h5-frame-bracket-diagnosis-20261020/frame-results.json), [completion audit](h5-frame-bracket-diagnosis-20261020/completion-results.json),
[exact bounds](h5-frame-bracket-diagnosis-20261020/bracket-bounds.json), [source review](h5-frame-bracket-diagnosis-20261020/source-review.json),
[raw models, certificates and bounded results](h5-frame-bracket-diagnosis-20261020/raw.zip), and
[verified manifest](h5-frame-bracket-diagnosis-20261020/raw-manifest.json).
All 206 archive members, CRCs and byte hashes verify.
