# First57: valid edge controls and a twelve-part companion — 2026-11-04

New original-source controls fix **two brackets and two inserts** around the
existing frame/insert core. This reduces a restricted first57 construction from
16 to **12 moving originals: six brackets and six inserts**. The companion
model's single bounded call closes **UNKNOWN**, with no complete placement.
H2/H5 remain open at **60% completed milestone weight**.

These positive controls do not change the [necessary frontier of 259 site
selections](h5-first57-necessary-capacities-20261104.md) or the 440 whole-job
allocations. The new construction deliberately omits cog sites 4 and 10 and
chooses twelve of the remaining thirteen sites. Its 13 choices are a
construction restriction, not a new negative exclusion.

## Direct edge brackets and adjoining inserts

The earlier [corner-channel experiment](h5-corner-channel-construction-20261104.md)
selected sites [5,10] for a different thirteen-cog/top-strip construction.
The new bracket control omits the rightmost cog in the lowest source row,
site 4, selected directly from its transform. It retains all fourteen other
reference cogs.

For every bracket mode, the preparer fixes X at either physical stock edge and
projects the audited positive obstacle cover onto integer Y intervals. It
chooses the lowest available Y on each edge, breaking ties by mode index.
[Independent endpoint-event replay](h5-first57-edge-controls-and-companion-20261104/bracket-control-audit.json)
checks all **16 edge/mode domains** and **32,950 projected obstacle intervals**.
Original-source readback then validates the two brackets with fixed29 and all
fourteen reference cogs: **45 parts, 990 same-sheet pairs, 180 stock edges,
49 cutouts and 4,946 hole vertices**.

| New fixed original | Mode | Lower-left anchor, mm |
| --- | ---: | --- |
| Bracket 0, left edge | 3 | (6.53, 2680.45) |
| Bracket 1, right edge | 2 | (1193.47, 1989.01) |

The right bracket starts below the previous top-strip lower bound. The source
control includes its entire original contour and all three cutouts.
[The saved bracket transforms](h5-first57-edge-controls-and-companion-20261104/selected-brackets.json) are retained.

A second direct control additionally omits the leftmost cog in the highest
source row, site 10. It places one rotated insert in the left bracket's
concavity and another above the right bracket, using source-covering component
bounds and 0.23 mm offsets:

| New fixed original | Mode | Lower-left anchor, mm |
| --- | ---: | --- |
| Insert 6 | 1 (90°) | (81.76, 2680.68) |
| Insert 7 | 0 (0°) | (1193.70, 2239.25) |

[Independent reconstruction](h5-first57-edge-controls-and-companion-20261104/insert-control-audit.json) verifies the
formulas, [saved insert transforms](h5-first57-edge-controls-and-companion-20261104/selected-inserts.json), and all
**46 reference parts, 1,035 pairs, 184 stock edges, 50 cutouts and 4,990 hole
vertices**. Removing any one of the thirteen reference cogs preserves those
checks. The [fixed33 originals](h5-first57-edge-controls-and-companion-20261104/fixed33.json), twelve required cog
identities and twelve remaining mover identities form first57 exactly once,
disjoint from source-valid short9.

Neither reference control is a full66 layout. Their complete preparation
processes take **0.409560 s** and **0.321232 s**, with independent audits of
0.215976 s and 0.082076 s.

## Preserved coverage failure and exact correction

The first companion preparation added integer anchor coordinates to rounded
mode-relative component boxes. Exact readback of the **saved binary64 world
transforms** finds nine vertices outside those nominal unexpanded boxes across
all six new fixed components, at coordinate-rounding boundaries.
[That failed coverage check](h5-first57-edge-controls-and-companion-20261104/fixed-source-cover-failure.json) is
preserved. The original-source 46-part layout remains valid; the failed
prepared obstacle cover was never used in a model.

The corrected version recomputes the six fixed boxes from exact rational
representations of the saved world transforms and rounds them outward before
the 0.23 mm right/top expansion.
[Independent geometry readback](h5-first57-edge-controls-and-companion-20261104/corrected-geometry-audit.json) checks
all **24 original component vertices**, **5,690 source-covering rectangles**
and **11,075,160 mask cells**. The **9,054 output obstacle boxes** have disjoint
interiors and cover every source boundary. Sites 4 and 10 have no obstacle bit.

All twelve legal full-stock mover modes and their source rectangles are
byte-identical to the preceding audited geometry. Eighteen moving components
represent the six brackets and six inserts. Eight groups cover all **147
different-owner component pairs**; a ninth group supplies the complementary
bracket components for fixed-obstacle interactions. Every moving component
occurs with the fixed obstacles exactly once, with no same-owner pair.

The failed and corrected preparation processes take **0.549594 s** and
**0.975217 s**. Both are preserved, and **both are charged** to the construction.
The corrected geometry audit takes 1.571512 s.

## Audited model and sole closed call

[Every field of the model passes readback](h5-first57-edge-controls-and-companion-20261104/model-audit.json):
**250 variables and 18,918 constraints**, 72 legal mode selectors, 15 empty-site
selectors, two mandatory empty-site equations, 31 optional obstacle-mask
literals, 480 rigid coordinate links and nine packing groups. Exactly three
cog sites are empty in total. There are **18,210 rectangle references** and
ten same-family ordering constraints. No capacity table, objective or hint is
consumed.

The complete model build takes **1.027785 s**.
[The final ledger](h5-first57-edge-controls-and-companion-20261104/preparation-charges.json) charges **4.545057 s**,
including source geometry, the direct short sheet, obstacle/mover preparation,
both edge controls, the failed and corrected companion preparations and the
complete model build. The original 60/90-second limits and four-second source
validation reserve remain fixed.

[Independent response readback](h5-first57-edge-controls-and-companion-20261104/response-audit.json) verifies the
single closed **UNKNOWN** call. Search begins after **6.63 solver seconds**;
the response records **4,234 branches and 623 conflicts**, with no incumbent,
assignment, source66 check or native call. Allocated/returned solve times are
**50.746847 / 50.771479 s**. The **0.024632 s solve-slice overrun** is retained.
Preparation-inclusive algorithm/shared totals are **56.039587 / 56.107026 s**,
with no overall overrun. This call will not be restarted, reseeded or extended.

## Remaining construction

The [next-step record](h5-first57-edge-controls-and-companion-20261104/next-step.json) proposes checking a direct row
of the six remaining inserts along the top stock edge, to the right of the
upper-left bracket. This is only a hypothesis. It needs original-source
validation, then necessary bracket-capacity checks for the resulting fixed
layout before any further solver call: fixing the top shelf may consume
space needed by the brackets.

The necessary frontier remains 259 selections; the older fixed13-cog frontier
remains two selections / three count distributions. Full66 source checks,
native/material validation, integration and the H5 matrix remain required.
H2 retains its original gate, and all 22 reserved vectors remain unopened.
No release qualifies.

All six jobs and the aggregate run for
[main 69c10624](https://github.com/skulitom/Nestbolt/actions/runs/41915862899)
now pass. Local checkpoint daa0689f and this evidence are ready for a guarded
normal push after archive and staged-file verification.

The [manifest](h5-first57-edge-controls-and-companion-20261104/raw-manifest.json) contains 100 new canonical
members and 1,833,082 compressed bytes.
[Historical references](h5-first57-edge-controls-and-companion-20261104/external-evidence.json) and
[source bindings](h5-first57-edge-controls-and-companion-20261104/source-bindings.json) retain exact inputs. Independent
archive readback verifies every new/reused member, source hash and local link.
