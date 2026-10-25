# H5: continuous-coverage outer coordinate relaxation — 2026-10-25

**The audited outer relaxation reports `INFEASIBLE` with fixed core 0.**
Unlike the earlier inward-safe grid model, this construction covers the
recorded original continuous placement regions and deliberately permits extra
space and small overlaps. Within that original polygon/rotation model, keeping
these 18 frames and 15 cogs unchanged cannot accommodate all 12 brackets and
21 inserts at the original two-sheet material target. Different frame/cog
arrangements remain open. H2/H5 remain open at **60%** completed milestone weight.

## Coverage before the solver

Reuse the committed, independently checked zero-clearance translation regions
for core 0. All **24** queries retain all **12** permitted orientation/reflection
cases and both sheets. Their 953 outer hulls cover the complete source regions,
including unsampled positions. Normalize each orientation by its exact
quarter-turn bounding-box minimum, then add the full floor-quantization square
from -0.01 to 0 mm on each axis and 0.001 mm extra outward numerical padding.
Construction finishes in **0.532253 seconds**, within the
declared 120 seconds, with nothing pending.

The independent audit verifies 32 inherited input/query files against committed
manifests. Exact rational tests show that all **19,808** required shifted-source
and quantization vertices lie inside the expanded hulls. Convexity extends
that coverage to every continuous point. All **4,952** expanded-hull vertices
satisfy every outward-rounded halfspace and outward integer bound. The same
4,952 edge inequalities are independently re-derived with their complete
coefficient error allowances.

All **14,734** known original poses compatible with core 0 have encoded grid
representatives. The original 64-part baseline is retained as a partial
sanity check; all 500 of its cross-part rectangle-component pairs satisfy the
relaxed separation rule. It does not satisfy the model's required 66 parts.
Original floating quarter-turn transforms differ from their exact normalized
rectangles by at most 5.69e-14 mm; known translated polygons differ by at most
1.15e-13 mm, far below the original 0.2 mm clearance.

Review caught duplicated vertices in the plan's descriptive quantization-square
field. The actual construction and stated per-axis range already used the full
two-dimensional square. The field was corrected before the independent audit;
the original plan/builder and hashes of all 24 unchanged geometry files remain.
No geometry phase was regenerated or extended.

## Complete exact-count outer encoding

All 66 original parts remain mandatory: 33 fixed and 33 small parts. The model
retains **17,178** per-copy domain choices and **360** orientation/sheet modes.
Every bracket has two coupled original rectangular arms. All **978** component
pairs from distinct physical parts are constrained; a bracket's own arms
are never separated from each other.

Original nonoverlap gives an x or y order between axis-aligned rectangle
components. Their dimensions and offsets are exact grid multiples, so flooring
the two anchors preserves zero-gap order. Allowing an additional one-grid-unit
overlap only enlarges the model. Expanded stock, dropped positive clearance,
outward domains and that overlap are relaxation parameters, never acceptable
cutting settings. The original material target remains the source of the
second-sheet height limit.

Independent reconstruction checks every field of the **22,290-variable**,
**128,377-constraint** model and every solver parameter. The generated encoding
retains the previous independent checker; all template changes and hashes are
recorded. There is no objective, missing-part allowance or arbitrary pruning.

## Result and its limit

One declared 60-second, eight-worker, seed-zero call reaches search at
**1.85 seconds**. The log records `#Done 13.78s no_lp`; total elapsed time is
**13.950743 seconds**. Status is `INFEASIBLE`, with no incumbent,
170,621 branches and 32,789 conflicts. The call is neither repeated nor extended.

This is CP-SAT's result for the fully checked model, without a separately
verified LRAT proof. The conditional geometric implication relies on the
committed original-outline translation-region audit and the exact outward
coverage/encoding checks above. It excludes continuing to hold **core 0**
unchanged within that recorded geometry model. It does not establish
unrestricted impossibility when the frame/cog placements may change, close H5,
or justify different quantities, clearances or material limits.

## A guarded alternative to investigate

Saved core 5 differs from core 0 in one rotated cog. Its pair distances pass
the guarded screen, but that cog lies too close to the left and top stock
edges. A single deterministic nearest-point projection moves it by
**(+0.0125, -0.0125) mm**, preserving its rotation and every other 32 placement.
This is a new arrangement, not resumed sampling from a capped proposal list.

An independent affine-transform audit verifies all **438** same-sheet original
polygon pairs and **132** stock boundaries. Minimum pair gap is 0.2126 mm and
minimum extra stock margin is 0.0126 mm, above the source-derived compensated
separation 0.21170867250963943 mm and conversion guard 0.011444091796875 mm.
This passes a sufficient distance screen only. There is no 66-part layout or
actual native transformed-collision qualification yet.

Evaluate the independently checked guarded alternative in output/h5-guarded-alternate-core-20261025/fixed-core.json. It preserves32 placements from saved core5 and moves its one changed cog by(+0.0125,-0.0125)mm to repair the stock margin while preserving the cog orientation. First construct and audit complete zero-clearance outer translation regions for this new fixed arrangement, retaining every original bracket/insert orientation, both original stock domains, all12 brackets and21 inserts, and the same outward quantization proof. The prior source regions cannot be reused unchanged because a cog moved; reconstruct its Minkowski obstacle and the complete affected unions. Declare fresh bounded construction and a single outer feasibility call before execution. Reuse checked encoding only after independently verifying every new model/input field. If this generous fixed-core relaxation is feasible, diagnose it against all original filled polygons; never accept its overlaps or expanded bounds. If it is infeasible with verified continuous coverage, preserve that conditional exclusion and investigate more substantial frame/cog rearrangement rather than retrying completed small-part searches. Do not extend the completed core0 calls, resume capped pose lists, lower native guards, change H2 or claim a new release. Any accepted outcome still needs all66 original parts, the material target, actual native checks, original production budget and the complete13-job/two-kerf matrix.

## Repository and evidence

Engine source, all three accurate READMEs and releases are unchanged. Main
8f941426's hosted checks are captured as `in_progress` /
`pending`; the two newer domain/model checkpoints remain
local at source head cc9e8702. No native packing, production-budget run,
full H5 matrix or held-out evaluation occurs. A new release is not qualified.

Evidence: [construction plan](h5-outer-coordinate-relaxation-20261025/plan.json), [coverage audit](h5-outer-coordinate-relaxation-20261025/coverage-audit.json),
[complete model audit](h5-outer-coordinate-relaxation-20261025/model-audit.json), [solver](h5-outer-coordinate-relaxation-20261025/solver.json),
[conditional interpretation](h5-outer-coordinate-relaxation-20261025/interpretation.json),
[alternate projection](h5-outer-coordinate-relaxation-20261025/alternate-core-projection.json),
[independent alternate-core audit](h5-outer-coordinate-relaxation-20261025/alternate-core-audit.json),
[source review](h5-outer-coordinate-relaxation-20261025/source-review.json), [raw archive](h5-outer-coordinate-relaxation-20261025/raw-001.zip)
and [manifest](h5-outer-coordinate-relaxation-20261025/raw-manifest.json). All 119 canonical
members and 20 aliases retain exact bytes with
CRC and SHA-256 checks, including every region, model, source plan and solver log.
