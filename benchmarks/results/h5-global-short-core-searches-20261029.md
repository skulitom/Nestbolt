# H5: two closed global short-sheet core searches

Date: 2026-10-29. Evidence and documentation only. H2/H5 remain open at
60% completed milestone weight; no new release qualifies.

## Result

Both independently audited global short-sheet searches closed **UNKNOWN**,
with no incumbent, assignment, candidate source check or native call. Neither
result excludes a source layout or establishes a feasible allocation. Each
study made its sole declared call and stayed within its 60-second algorithm
and 90-second shared budgets. Small overruns of their shorter allocated solve
times are preserved below. Neither call was extended or retried.

The target remains five brackets, six inserts and two cogs on the short
sheet, with 53 specified original identities still requiring first-sheet
placements. All 66 identities are accounted for. The existing valid 64-part
layout and 444 necessary allocation survivors remain unchanged.

## Models and controls

The [prior source preflight](h5-fixed-nine-triple-and-global-short-preflight-20261029.md)
proved the exact source-contained cores, symbolic separation facets and
micrometre rounding map. The first model makes all 13 owners mandatory and
all 26 anchor coordinates independently movable. It retains eight bracket
modes, four insert modes, sixteen orthogonal core pieces in one global
NoOverlap2D constraint, 32 cog/rectangle predicates and one cog/cog predicate.
There are 1,438 variables and 1,414 constraints. No pose is fixed and no
objective, extra clearance or symmetry ordering is imposed.

An [exhaustive protobuf audit](h5-global-short-core-searches-20261029/micrometre-model-audit.json) checks every
variable domain, constraint, table entry, guard, interval, facet coefficient
and hint. The 11-part source control fails only the two explicit requirements
for missing cog 0 and insert 0. Disabling precisely those requirements makes
every constraint pass. The full negative 13-part control fails 34 constraints,
including all 33 cog separation choices and the global rectangle constraint;
it has 95 orthogonal piece collisions. Controls are evaluated without a solver.

The distinct second model uses **100-micrometre anchor steps**, while retaining
exact micrometre rectangle geometry and facet constants. The
[source mapping proof](h5-global-short-core-searches-20261029/coarse-source-mapping-proof.json) bounds each
part's rounding displacement below 70.711 micrometres and pairwise relative
displacement below 141.422 micrometres. The unchanged required source gap is
211.70867250963943 micrometres, leaving more than 70.286 micrometres. Expanded
stock bounds include every rounded source anchor. This preserves the original
source-feasible set through the mapping; it does not preserve every arbitrary
witness of the previous core-only model.

Ten adjacent x-order constraints remove permutations of identical copies
within each family. Relabeling complete poses preserves their geometry,
cutouts, stock conditions and selected identity set. No ordering crosses
families. All original transformations remain available. The
[coarse preflight audit](h5-global-short-core-searches-20261029/coarse-preflight-audit.json) independently
checks rounding, 13 stock-bound conversions, identities and the controls.

The coarse model still has 1,438 variables and now has 1,424 constraints.
Its [exhaustive model audit](h5-global-short-core-searches-20261029/coarse-model-audit.json) additionally
checks every factor of 100 in anchor-to-world links and cog facet terms,
all ten copy orders, and both complete control assignments. The positive
control again fails only the two missing mandatory originals; the negative
control retains the same 34 failed constraints and 95 orthogonal collisions.

## Closed calls

| Quantity | Micrometre model | Coarse model |
|---|---:|---:|
| Search starts | 0.17 s | 0.16 s |
| Allocated solve time | 56.316769500 s | 56.408515300 s |
| Returned solve time | 56.454143000 s | 56.463758700 s |
| Allocated solve overrun | 0.137373500 s | 0.055243400 s |
| Algorithm time | 57.144284900 s | 57.065867400 s |
| Shared time | 57.202691800 s | 57.121788700 s |
| Returned response branches | 767,489 | 328,821 |
| Returned response conflicts | 53,009 | 57,477 |
| Status | UNKNOWN | UNKNOWN |

The branch/conflict counts are returned response counters, not sums over
all workers. Both calls use four workers, seed zero and the declared source
validation reserve. The [micrometre response audit](h5-global-short-core-searches-20261029/micrometre-response-audit.json)
and [coarse response audit](h5-global-short-core-searches-20261029/coarse-response-audit.json) verify model
bytes, parameters, protobuf responses, timings and the absence of candidates.
The saved models, raw logs and empty incumbent inventories remain preserved.

An [unused checker defect](h5-global-short-core-searches-20261029/unused-reader-defect.json) was found after
the first call: direct float conversion rejects the rational source-center
string `69861871/500000`. It was never exercised because no assignment existed.
The closed script remains unchanged. The distinct coarse checker uses Fraction
before conversion; its actual corrected expression evaluates to the expected
center. Its grid scaling and tuple-normalized expected identities are reviewed.
The [reader review](h5-global-short-core-searches-20261029/coarse-reader-review.json) explicitly leaves the
unused candidate pipeline unverified end to end. It also preserves a failed
script-generation assertion and the separate helper that completed only the
missing files before model construction.

## Next preparation

The current global rectangle constraint covers only the brackets and inserts;
cogs are handled by separate exact facet disjunctions. A new preparation adds
16 disjoint interior rectangles per cog to expose more occupied area to global
propagation. Each set covers 33,589,747,308 square micrometres of the existing
37,162,458,716 square-micrometre cog core. The rectangles share their original
owner and anchor; all current cog facet predicates must remain.

The [independent strip audit](h5-global-short-core-searches-20261029/cog-strip-audit.json) verifies 2,048 exact
corner/edge inequalities and all 120 internal rectangle pairs. The positive
11-part control yields 31 pieces and no overlap across 465 pairs. The negative
13-part control yields 48 pieces and 341 overlapping pairs out of 1,128.
The [necessity argument](h5-global-short-core-searches-20261029/cog-strip-necessity-proof.json) explains why
these subset rectangles can join the global constraint without excluding a
feasible current core assignment.

No model or search using these strips has been opened. Before any cumulative
constraints are added, a common bounding box must be proved to contain every
possible model rectangle, including the stock expansion and coarse rounding.
Original stock dimensions cannot simply be substituted as capacity constants.
The [next step](h5-global-short-core-searches-20261029/next-step.json) requires that audit and a complete model
audit before another declared call. A core solution would still need original
source geometry, first-sheet placements and all-66 validation before native use.

## Publication

The [push receipt](h5-global-short-core-searches-20261029/prior-main-push-receipt.json) confirms the normal
atomic fast-forward of main and the working branch from `6b0a1d0b` to
`d3b652b6`, publishing both prior queued checkpoints after all six preceding
checks passed. At this checkpoint's
[CI 40795603963 snapshot](https://github.com/skulitom/Nestbolt/actions/runs/40795603963),
four jobs have passed and the Ubuntu/Windows checks are running. This new
checkpoint queues until all six pass; no live run is cancelled.

Production, all three READMEs, upstream heads/releases and Nestbolt's
`v0.1.0` stable / `v0.2.0-alpha.1` preview releases remain unchanged.
H2 retains its original gate and 22 unopened vector files.
The [manifest](h5-global-short-core-searches-20261029/raw-manifest.json) preserves 3374 canonical members,
729 identical-content aliases and 14670156 compressed bytes, including
both models and responses, controls, failed unused checker, script-generation
failure, new strip geometry, push receipt and recursive source bindings.
