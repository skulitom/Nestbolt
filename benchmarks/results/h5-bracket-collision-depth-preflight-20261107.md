# Bracket collision-depth preflight — 2026-11-07

The source-derived auxiliary term passes independent geometry and derivative
checks. It supplies a separating direction for the previously flat crossed-arm
collision. This is a numerical preflight: **no augmented optimization model,
new search, full valid layout or allocation exclusion is produced**. H2/H5
remain open at **60% completed milestone weight**.

## Source geometry and fixed objective definition

[The frozen plan](h5-bracket-collision-depth-preflight-20261107/plan.json) defines the supplementary term before
measurements: coefficient **1** times the sum of squared distances from an
interior relative bracket translation to the boundary of its nominal collision
region, and zero outside or on that boundary. It is added to the existing
weighted original-plus-clearance area objective. The area terms and their
positive weights remain unchanged; auxiliary coefficients are not reweighted.

The bracket is the original six-vertex L, with area 40,000 mm² and source center
(150, 125) mm. The producer splits it into a horizontal rectangle and its
remaining vertical arm. The independent audit uses a different decomposition:
the full vertical column and remaining horizontal arm. Their exact integer
boundaries match the source under all quarter-turn/reflection modes.
[All ten mode/domain identities](h5-bracket-collision-depth-preflight-20261107/source-controls.json) remain separate,
including aliases with different legal center domains.

For each of **100 ordered mode pairs**, the producer unions four component
Minkowski-difference rectangles. The independent audit builds a rational cell
arrangement from its alternate decomposition and extracts exposed elementary
edges. [Every region](h5-bracket-collision-depth-preflight-20261107/region-controls.json) agrees in occupied area and
boundary. The audit checks **19,544** arrangement vertices, edge midpoints and
cell centers, including exterior slabs, against both exact rational distances
and direct original-polygon intersections. All values and selected gradients
at these rational controls agree exactly.

The [audit](h5-bracket-collision-depth-preflight-20261107/geometry-audit.json) covers 4,720 interior points and 14,824
boundary/exterior points, with **8,376** central derivative coordinates.
Maximum central error is 0.000050005 mm, below the frozen 0.002 tolerance.
All 4,720 selected-gradient descent controls pass, including **532** points
with distinct tied nearest features and **516** reflex-corner projections.
At ties the returned vector is a deterministic selected branch, not a claim
that a unique classical derivative exists. Zero-length edges are rejected;
all actual region boundary rings are included.

## Floating source transforms and retained acceptance

Nominal exact quarter turns are not described as identical to floating source
transforms. [The reconciliation](h5-bracket-collision-depth-preflight-20261107/floating-controls.json) derives a
binary64 arithmetic bound over every bracket hard domain, including source
center/pivot cancellation, trigonometric coefficient error and rounded relative
center subtraction. If the nominal translated shapes intersect, the actual
source distance is at most **1.557479e-11 mm**. This is below the required
**0.211708672510 mm** gap, so a source-valid gap-separated bracket pair has zero
auxiliary loss. Ninety actual source-pose corner/midpoint checks agree within
the bound; the largest observed Hausdorff error is 4.547474e-13 mm.
There are 11,216 nominal source-safe controls as well.

[Two unchanged validation cases](h5-bracket-collision-depth-preflight-20261107/objective-controls.json) retain all
**528** area pairs and add the **15** bracket terms. The original initializer
has 10.643914 mm² auxiliary loss; the saved closed candidate has 8,016.700868 mm².
Independent rational sums and both-owner gradient signs agree. Positive
existing weights remain in [1,64], so the nonnegative extra term cannot hide
an original overlap. Four corrupted pivot/mode/angle bindings are
[rejected](h5-bracket-collision-depth-preflight-20261107/negative-controls.json). Source acceptance is unchanged.

## Preserved assertion failure and correction

The first audit passes all 100 region checks, then fails an exact-equality
assertion on an arbitrary floating closest point. The
[failed process](h5-bracket-collision-depth-preflight-20261107/preserved-failed-audit-process.json) remains preserved.
[Independent rational diagnosis](h5-bracket-collision-depth-preflight-20261107/projection-diagnostic.json) finds one
projection coordinate discrepancy of **1.421085e-14 mm**, with maximum squared
value error 4.343973e-13 mm². The selected boundary segment is an exact minimizing
feature in both positive validation pairs; the geometry and kernel are sound.

[Version 2](h5-bracket-collision-depth-preflight-20261107/audit-correction.json) requires the selected segment's exact
rational projection to minimize distance, then checks its computed coordinate
against half the original 1e-6 gradient tolerance. It uses that exact projection
for the independent aggregate gradient. No kernel, geometry, case, model,
coefficient, sample or declared numerical tolerance changes. The passing
[audit process](h5-bracket-collision-depth-preflight-20261107/audit-process.json) closes in 6.153590s; the failed process
closes in 6.891152s. Both are validation only and neither launches optimization.

## Flat-collision evidence and next construction

Brackets 7 and 8 still overlap by 5,625 mm² in the saved source candidate; their
combined original/clearance term is 11,284.552900 mm² and its available pair
gradient is zero within 1e-7. [The added term](h5-bracket-collision-depth-preflight-20261107/flat-pair-controls.json)
has depth **89.536031 mm**, squared loss **8,016.700868 mm²**, and relative-y
gradient **179.072062 mm**. Both owner derivatives pass central checks.
Either moving the first bracket up 0.001 mm or the second down 0.001 mm stays
inside its hard bounds and reduces the supplementary pair loss to
8,016.521797 mm² while the area term remains flat. These are read-only probes;
the saved candidate is unchanged and is never an optimizer seed. Whole-job
improvement does not follow from pair descent.

Earlier work already used collision exclusions and nearest-boundary directions:
[October 18 contact geometry](h5-outline-contact-direction-20261018.md),
[terminal repair](h5-terminal-repair-diagnosis-20261018.md) and
[later surrogate diagnostics](h5-target-cog-repair-and-source-gradients-20261107.md).
The last records a decreasing distance surrogate with increasing true overlap.
This checkpoint therefore adds a specifically checked bracket term without
replacing exact areas or claiming a new general packing technique.

The [next step](h5-bracket-collision-depth-preflight-20261107/next-step.json) is a separately identified augmented
model, its complete independent readback and a finite charged construction
from the original unoptimized source initializer. The new
[geometry preparation](h5-bracket-collision-depth-preflight-20261107/preparation-process.json) costs **1.565239s**;
complete consumed source preparation is **11.002683s** before any
new model. It includes the 9.437444s source initializer, and excludes the
validation-only closed-candidate observations. All seven weighted calls and
all older calls remain closed. Four earlier arrangements and 440 allocations
remain unresolved. The latest search still fails 46 pairs with 28,414.189788 mm²
overlap; this preflight does not change that result.

All six jobs on main c7e4b305
[pass at review](h5-bracket-collision-depth-preflight-20261107/main-ci-at-review.json); the previous and current
checkpoints can now proceed through the ordinary guarded push. Product code,
README claims and releases remain unchanged.

[Archive verification](h5-bracket-collision-depth-preflight-20261107/archive-checks.json),
[manifest](h5-bracket-collision-depth-preflight-20261107/raw-manifest.json), [source bindings](h5-bracket-collision-depth-preflight-20261107/source-bindings.json),
[historical references](h5-bracket-collision-depth-preflight-20261107/external-evidence.json) and
[runtime pins](h5-bracket-collision-depth-preflight-20261107/runtime-bindings.json) preserve all new and reused evidence.
