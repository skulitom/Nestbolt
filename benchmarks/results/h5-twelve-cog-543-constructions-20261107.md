# Twelve-cog 5/4/3 constructions — 2026-11-07

Two distinct constructions close without a placement. The new independent
**5/4/3-cog row model returns UNKNOWN**. A separate staged method fixes its
deterministic source-valid row control before placing companions and returns
**grid-INFEASIBLE**. Neither result excludes a continuous layout or whole
allocation. Four fixed arrangements and all 440 whole allocations remain.
H2/H5 stay open at **60% completed milestone weight**.

## Fresh row geometry and complete joint model

The source allocation uses reference sites 0–4, 6–9 and 12–14, with the same
validated nine-part small sheet. Five, four and three cogs receive independent
translations; all twelve remaining cog identities and sixteen orthogonal
companions are retained. The earlier 4/4/4 and thirteen-cog calls remain closed.

[Exact domain readback](h5-twelve-cog-543-constructions-20261107/row-domain-audit.json) verifies all three full
stock/core-safe rectangles, nearest excluded grid points, 36 source-mode relative
domains and three row-difference domains. Twelve individual-row corner controls
plus the simultaneous 50-part reference check 7,628 same-sheet pairs. The
Cartesian product of these individual boxes is not claimed collision-free.

| Row | X shift, mm | Y shift, mm |
|---|---|---|
| 0, five cogs | -91.56 to 79.99 | 0.01 to 605.65 |
| 1, four cogs | -430.42 to -0.01 | -246.19 to 359.46 |
| 2, three cogs | -609.28 to 79.99 | -492.38 to 113.27 |

The largest horizontal row difference reaches -689.27 mm. The old 600 mm
normal-error envelope would be insufficient. [Fresh integer checks](h5-twelve-cog-543-constructions-20261107/row-integer-audit.json)
verify a 700 × 1100 mm row-difference envelope, all 9,847 halfplane implications,
24 rigid rectangles and 268 different-owner pairs. The mover-relative envelope
remains 2000 × 1500 mm and is independently checked against every new row range.

[Original-source region checks](h5-twelve-cog-543-constructions-20261107/row-source-audit.json) certify 2,099
mover/row regions and 577 row-pair regions, using 48,332 and 98,753 exact rational
support proofs. Eleven degenerate regions are disabled. All source aliases and
cross-row original pairs are covered, with minimum certified gap
0.225999999 mm. No global free-space coverage claim is made.

[The deterministic positive control](h5-twelve-cog-543-constructions-20261107/row-control-audit.json) considers
1,528 centroid grid neighbors and accepts its first adjacent-row combination.
The shifts are [-9156,1], [-8832,1269] and [-9303,2475] in 0.01 mm units.
All 50 placed originals pass 856 pair, 200 stock-edge, 58 hole and 6,122
hole-vertex checks; the sixteen orthogonal companions remain unplaced.

[Every joint-model field](h5-twelve-cog-543-constructions-20261107/joint-model-audit.json) is verified:
18,671 variables, 66,604 constraints, all 96 modes, six independent row shifts,
16,792 mover/row selectors, 577 row-pair selectors, 640 rigid coordinate links,
268 component pairs and fourteen valid identical-copy ordering constraints.
The 583-value hint specifies only the source-checked row control.

[Complete charged preparation](h5-twelve-cog-543-constructions-20261107/joint-preparation-charges.json) is
**8.301528 seconds**, including the complete model build. [Response readback](h5-twelve-cog-543-constructions-20261107/joint-response-audit.json)
verifies one UNKNOWN call with 63,657 branches and 428 conflicts, no incumbent
or assignment. Allocated/returned solve time is 46.716391 / 46.863195 seconds;
the **0.146804-second solve-slice overrun is preserved**. Preparation-inclusive
algorithm/shared totals are **56.165204 / 56.309005 seconds**, within 60/90 s.
[The process record](h5-twelve-cog-543-constructions-20261107/joint-process.json) confirms every descendant closed.

## Separately defined staged construction

The staged method fixes the first deterministic row control before examining
companion placements. [Point-domain readback](h5-twelve-cog-543-constructions-20261107/staged-packet-audit.json)
binds the twelve fixed cogs, fixed29 and short9 to the independent 50-part source
control. The two compatibility coordinates are constants X=Y=0. The staged
input graph contains **no joint model, joint search or joint response**.

Fresh combined obstacles replace the three independent row disjunctions.
[Source certification](h5-twelve-cog-543-constructions-20261107/staged-source-audit.json) verifies 208 rounded
regions with 7,712 exact support proofs against all twelve cog poses and every
source-mode alias. [Integer readback](h5-twelve-cog-543-constructions-20261107/staged-integer-audit.json) verifies
737 conservative halfplane implications, all original world bounds and all
24 rigid components. No prior fixed-cog capacity result is consumed.

[The complete staged model](h5-twelve-cog-543-constructions-20261107/staged-model-audit.json) has 2,962 variables
and 8,386 constraints, all sixteen original movers and 96 modes, 1,664 unary
region selectors, 5,896 unary planes, 640 rigid links and 268 different-owner
pairs. It has no objective or hint. The only free coordinates belong to the
sixteen orthogonal parts; the packet remains fixed.

[Its full preparation ledger](h5-twelve-cog-543-constructions-20261107/staged-preparation-charges.json) charges
**7.286199 seconds**. This includes all four stage-one domain/region/integer/control
processes, source geometry/sites/rectangles, direct short9, the new point-packet
preflight, combined geometry, integer conversion and complete model build.
Stage one receives no free cached placement preparation. Independent verification
processes are retained separately.

[Response readback](h5-twelve-cog-543-constructions-20261107/staged-response-audit.json) verifies one grid-INFEASIBLE
call: 153,249 branches, 38,769 conflicts, no incumbent or assignment.
It returns in 7.508641 seconds against 48.081655 seconds allocated. Complete
algorithm/shared totals are **15.441594 / 15.510424 seconds**, without overruns.
[Every process descendant closes](h5-twelve-cog-543-constructions-20261107/staged-process.json). No independent
continuous UNSAT certificate is claimed. Both calls remain closed and will not
be repeated, reseeded or extended.

## Preserved corrections and remaining scope

A [helper-generation syntax failure](h5-twelve-cog-543-constructions-20261107/helper-failure.json) occurred before
any model builder was created or process started. The malformed source remains
unchanged; a versioned corrected generator creates the audited staged model.
The prior 4/4/4 integer producer also used the same local-name reuse described
in its preserved audit-report correction: it reported component count 268 in
the row-region field. Its actual source/model audits cover all 583 regions and
model bytes remain unchanged. This new producer and audit both check the exact
577 row-region count separately from 268 component pairs.

[The next prospective construction](h5-twelve-cog-543-constructions-20261107/next-step.json) uses 5/5/2 rows from
reference sites 0–9, 13 and 14, corresponding to still-unresolved empty sites
[10,11,12]. Fresh source domains, interaction certificates, coordinate error
envelopes and complete preparation charges are required before any new call.
No such call is prepared here. Full66 source/native/material validation,
production integration and the full H5 matrix remain open.

Main remains 9e878243; the preceding twelve-cog checkpoint and this checkpoint
await the normal push condition. At review,
[CI42328915911](https://github.com/skulitom/Nestbolt/actions/runs/42328915911)
has five successful jobs and a live Windows check. No run is cancelled. Production,
READMEs and release assets are unchanged; no new release qualifies.

[The manifest](h5-twelve-cog-543-constructions-20261107/raw-manifest.json) contains 273
new canonical members in 1 ZIP parts, totaling
7,619,956 bytes. [Historical references](h5-twelve-cog-543-constructions-20261107/external-evidence.json)
and [source bindings](h5-twelve-cog-543-constructions-20261107/source-bindings.json) preserve exact inputs and
failed bytes. Independent archive verification is required before commit.
