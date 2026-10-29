# H5: short-sheet capacity and original cog separation

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight. No new release qualifies.

Two distinct, fully audited extensions of the global short-sheet model return
**UNKNOWN**, with no incumbent or assignment. Both calls are closed. Neither
result establishes source feasibility or excludes the allocation. All thirteen
short-sheet originals remain mandatory and movable, and their complementary
53 first-sheet identities remain required. The valid 64-part layout and
444 necessary allocation survivors are unchanged.

## Whole-sheet propagation

The [previous checkpoint](h5-global-short-core-searches-20261029.md) prepared
sixteen disjoint source-contained rectangles per cog. The new model adds those
32 pieces to a second, 48-piece global NoOverlap2D constraint and adds two
cumulative constraints. All 1,438 parent variables, 1,424 parent constraints
and 775 parent hints are retained unchanged.

Capacity constants are derived from every active mode's actual anchor domain
and local rectangle, including coarse rounding and the expanded stock bounds.
The [independent envelope audit](h5-short-strip-capacity-and-source-pair-20261029/capacity-bound-audit.json) checks
36 mode/piece envelopes and 576 exact anchor/local corners. The common box is
`[6502,6502,1493498,319398]` micrometres. Its height, 312,896 micrometres, bounds
the summed heights of rectangles active at any X; its width, 1,486,996
micrometres, similarly bounds summed widths at any Y. Absent owners consume
no capacity. These constraints follow from existing core non-overlap.

An independent midpoint sweep checks 113 slabs. The positive source-derived
11-part control peaks at 309,988 micrometres in summed height and 1,258,976
in width, passing both capacities. The negative control peaks at 2,346,384
and 2,865,760 respectively, failing both. See the
[capacity controls](h5-short-strip-capacity-and-source-pair-20261029/capacity-controls.json).

The resulting model has **1,566 variables and 1,619 constraints**. Its
[exhaustive audit](h5-short-strip-capacity-and-source-pair-20261029/strip-model-audit.json) checks the unchanged parent
protobuf and every new variable, link, optional interval, owner, demand,
capacity and hint. The positive control fails only its two explicit missing
mandatory-original requirements; disabling exactly those two makes every
constraint pass. The negative control fails 37 constraints. No solver is used
to evaluate controls.

## Stronger original-source cog bound

The model's filled-core separation is weaker than the previously proved
original-cog separation. A fresh exact replay verifies the original proof
before reuse: **720 angle cells, 28,840 robust segments, 2,307,200 capsule/edge
checks and 518,400 ordered angle pairs**. All pass in 17.212621 seconds.
The proof covers arbitrary independent real cog rotations, using exact bounds
for pi, trigonometric intervals, source-edge distances and full-circle coverage.
No rotational tooth symmetry is assumed.

The [replayed proof](h5-short-strip-capacity-and-source-pair-20261029/all-angle-necessity-proof.json) establishes original
center distance at least **254.3 mm**. Its old micrometre-flooring bound is not
copied into the new model. Instead, the
[new mapping audit](h5-short-strip-capacity-and-source-pair-20261029/coarse-source-pair-audit.json) exactly matches all
80 source vertices and accounts for both the rational-center change and the
100-micrometre rounding. It bounds relative center displacement below
141.424 micrometres, giving a safe rounded distance lower bound of
254,158 micrometres.

The complete rounded center-Y domain permits a maximum difference of 34,400
micrometres. Exact squared-distance comparisons then require ordered center-X
distance of at least **2,519 grid steps, or 251.9 mm**. The existing within-family
ordering supplies the direction. The [bound](h5-short-strip-capacity-and-source-pair-20261029/coarse-source-pair-bound.json)
is necessary for source layouts; it does not preserve every earlier core-only
assignment.

A separate original-source positive pair at phase 7 degrees and 258.86 mm
center spacing passes stock, pair-gap and identity checks, then passes the
new rounded bound. A coincident source pair is rejected by both checks.
Both are independently reconstructed from the original cog geometry.
These two-part controls are not a new thirteen-part placement.

The second model retains all **1,566 parent variables and 1,619 constraints**
and adds only the guarded source-pair inequality, for **1,620 constraints**.
The [full extension audit](h5-short-strip-capacity-and-source-pair-20261029/source-pair-model-audit.json) verifies the
parent byte semantics, unchanged hints, identities, guard, coefficient and
lower bound. The positive control still fails only its two missing originals;
the negative control now fails 38 constraints.

## Closed calls

| Quantity | Strip/capacity model | Source-pair extension |
|---|---:|---:|
| Search starts | 0.24 s | 0.24 s |
| Allocated solve time | 56.300016000 s | 56.361162900 s |
| Returned solve time | 56.403445900 s | 56.434332600 s |
| Allocated solve overrun | 0.103429900 s | 0.073169700 s |
| Algorithm time | 57.114791400 s | 57.082501300 s |
| Shared time | 57.190961300 s | 57.143790600 s |
| Returned response branches | 2,321,228 | 128,915 |
| Returned response conflicts | 270,721 | 111,573 |
| Status | UNKNOWN | UNKNOWN |

Both calls use four workers, seed zero, the declared three-second source
validation reserve and no retry. The returned counters are not sums across
all workers. Small allocated-solve overruns are preserved; both overall
60-second algorithm and 90-second shared budgets pass.

The [strip response audit](h5-short-strip-capacity-and-source-pair-20261029/strip-response-audit.json) and
[source-pair response audit](h5-short-strip-capacity-and-source-pair-20261029/source-pair-response-audit.json) verify
the exact model bytes, parameters, raw protobuf responses and absence of
incumbents, assignments and candidate-check invocations. The unused candidate
readers retain the corrected Fraction parsing and 100-micrometre scaling;
their complete source pipelines have not been exercised. There are no native
calls, new source13 placements or complete source66 layouts.

The [next step](h5-short-strip-capacity-and-source-pair-20261029/next-step.json) investigates the prior directed
source-reference distances across all part families. Their old flooring,
reference offsets, mode correspondence and possible order changes must be
proved compatible before any bound can enter a new model. Legacy constants
cannot be copied unchanged. No such mapping or further search is prepared.

## Publication

Main remains `d3b652b6`, with the preceding `d876e610` checkpoint queued locally.
At the fresh [CI 40795603963 snapshot](https://github.com/skulitom/Nestbolt/actions/runs/40795603963),
five jobs pass and Windows checks are still running. This checkpoint also
queues until all six pass; no live run is cancelled. Production, all three
READMEs, upstream heads/releases and Nestbolt's stable `v0.1.0` and preview
`v0.2.0-alpha.1` remain unchanged. H2 keeps its original gate and all 22 reserved
vectors remain unopened.

The [manifest](h5-short-strip-capacity-and-source-pair-20261029/raw-manifest.json) preserves 4101 canonical members,
847 identical-content aliases and 30207802 compressed bytes. It includes
the complete models, logs, responses, source controls, exact certificate
replay, capacity proof, helpers and recursive input bindings.
