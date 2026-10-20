# H5: coordinated placements and cog-contact selection — 2026-10-20

**The expanded construction still returns 58 of the required 66 parts, missing
eight inserts.** Its selected positions are exactly the same as the previous
insert-completion attempt. No full target layout, native qualification or H5
completion is claimed. Completed milestone weight remains **60%**.

This checkpoint seals the unfinished October 18 selection evidence and the
October 20 contact-extension audit and search. All original shapes, quantities,
rotation permissions, margins, reserved frame holes and 0.2 mm clearance remain.
The last-sheet height target is 325.92690233 mm, corresponding to
4,988,890.353495 mm² of charged material. These are offline constructions.

## Coordinated pool and retained searches

The [previous checkpoint](h5-aligned-pockets-and-rows-20261018.md) supplies
24 retained partial layouts and 24 frame-only arrangements. Exact binary64
pose identity, without rounding, adds 261 candidates to the old 8,798-entry pool:
97 frames, 63 brackets, 66 inserts and 35 cogs. All 1,790 source events and the
entire original prefix are preserved. Independent enumeration of 1,901,998
added same-sheet pairs verifies all 132,531 new conflicts and their 2,277-clique
representation. Previously sealed hashes bind the unchanged original graph.

The four distinct complete fifteen-cog arrangements can also be treated as
selectable groups. Direct original-geometry checks cover 204,964 compatibility
pairs; all 4,522 eligible non-cog positions remain selectable. No frame is fixed.
Every variable domain, constraint and hint in both exact-inventory models is
independently consumed and checked.

| Finite construction | Variables | Constraints | Result | Seconds |
| --- | ---: | ---: | --- | ---: |
| All 9,059 poses, exact original inventory | 9,059 | 19,378 | UNKNOWN | 120.538773300 |
| Four cog arrangements, exact remaining inventory | 4,526 | 16,002 | UNKNOWN | 120.147449100 |
| Same cog arrangements, maximize inserts from 13 to 21 | 4,526 | 16,002 | FEASIBLE, 13 inserts | 120.110410700 |
| New cog-contact positions, maximize inserts from 13 to 21 | 6,786 | 24,750 | FEASIBLE, 13 inserts | 121.154159100 |

Each run was declared before execution with seed 0, eight offline workers and
a 120-second solver limit. Measured soft overruns are retained above. UNKNOWN
means no complete selection was returned. The two optimization models allow
partial construction only; original-job acceptance still requires all 21 inserts.
Their complete feasible hints contain 58 original parts, including 13 inserts,
and neither search improves its hint. Both retain an insert upper bound of 21,
so neither proves a maximum of 13 or rules out a full arrangement. Portfolio
search activity remains in the full logs; zero counters in the winning-hint
response summary do not mean no search occurred.

## Contacts against all fifteen cogs

The saved generator computes free translation regions against each whole cog
arrangement, using original sheets and allowed quarter-turns/reflections.
It caches 32 zero-translation exclusion shapes and translates them by the
original cog positions. Across 112 queries, it retains 6,173 region points;
16 queries are empty. Empty conservative regions are not global impossibility
proofs. A declared round-robin selection cap gives **2,260 new exact poses**:
460 frames, 900 brackets and 900 inserts. The original 9,059 poses remain exact.

Independent original-vertex checks verify every retained contact's provenance,
stock bounds, allowed rotation and physical clearance. They cover 22,778 contact
versus cog pairs and 299,308 pairs for compatibility with all four arrangements.
There are **6,782 eligible non-cog positions**. Exhaustive enumeration of all
**10,571,998 added same-sheet pairs**, with 840,208 direct distances after an
independent bounding-box screen, reproduces exactly **774,312 new conflicts**.
The combined 21,788 cliques cover the complete graph, with no false conflicts.
The full 6,786-variable model, including all 24,750 constraints, objective and
complete zero/one hint, is independently checked before solving.

Both returned partials pass all 1,212 original filled-outer pair checks, but
the frozen CLI rejects each solely for `insert: expected 21, found 13`.
Charged material is 4,985,103.45 mm²; reporting that value does not make an
incomplete layout acceptable. Filled area is 4,323,340.784070 mm², still below
the earlier 63-part partial's 4,331,552.627256 mm². The old bracket arrangement's
minimum gap is about 0.2011 mm, which is not qualified for the native solver's
additional geometric margin. No production candidate is integrated.

## Decision and next work

Artem [keeps H2's original denominator and leaves H2 open](h2-gate-decision-20261020.md).
The original 95% requirement, negative fixtures and split remain unchanged;
the previously pending question is resolved. No reserved vector is opened.

The added exact contacts do not improve the known feasible partial. Do not repeat these four models or increase their time limits. Before another packing run, inspect the relaxation rather than add further arbitrary poses: derive necessary local stock-area capacities from original filled-outline intersections with a predeclared finite set of horizontal and vertical slabs. Conservative integer rounding must never exclude a physically valid selection. Independently reconstruct every coefficient, bound and whole-cog contribution before using any strengthened model, and retain the complete feasible 58-part hint. First test whether these necessary bounds sharpen the finite-pool insert upper bound; a bound of 21 still leaves all eight inserts unresolved. Any later full 66-part selection requires original CLI and filled-outer validation, native-margin qualification and unchanged H5 quality gates. No finite-pool failure proves the unrestricted geometry impossible. H2 is explicitly left open under Artem’s unchanged-denominator decision.

[Checks](h5-coordinated-contact-selection-20261020/checks.json), [source review](h5-coordinated-contact-selection-20261020/source-review.json),
[raw attempts, failures, inputs and audit scripts](h5-coordinated-contact-selection-20261020/raw.zip), and
[verified archive manifest](h5-coordinated-contact-selection-20261020/raw-manifest.json).
All 293 archive members, CRCs and hashes verify.

All six checks on [main c9b0176](h5-coordinated-contact-selection-20261020/main-ci-c9b0176.json) pass.
The previous documentation checkpoint is pushed as c824e5a; its new CI state
is recorded separately. Product source, preview assets and the accurate English,
Japanese and Chinese READMEs stay unchanged.

The [upstream availability check](h5-coordinated-contact-selection-20261020/upstream-status.json) records
Sparrow Studio's published site as strip-only, without part-in-part; its repository
still describes the replacement app as unpublished. The plan's shipment stop
rule is not triggered. This is an availability check, not a performance comparison.
The [source attribution and exact-revision MIT notices](h5-coordinated-contact-selection-20261020/upstream-attribution.json)
accompany the preserved upstream documentation.
