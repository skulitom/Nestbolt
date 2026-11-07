# Source strip capacities and weighted models — 2026-11-07

Sixteen independently verified strip-capacity inequalities add geometric
information beyond the pairwise conflict models. Every strengthened model
passes a full audit, but **all four bounded calls stop at the proof-size limit**.
No further fixed arrangement or whole allocation is excluded and no placement
is produced. The frontier remains **four of 455 fixed arrangements**, with 451
excluded at original 0.2 mm clearance and 427 even at zero clearance. All 440
whole allocations remain; H2/H5 stay open at **60% completed milestone weight**.

## Necessary constraints involving multiple parts

A certified source-inner rectangle crosses a common horizontal line for every
anchor in a closed cell when its highest possible bottom is at or below that
line and its lowest possible top is at or above it. Its whole possible horizontal
extent must also lie inside one strip [L,U]. At most one component per cell is
used. For k selected parts, their disjoint line intervals of widths w_i require
at least the original 200 micrometre clearance between adjacent intervals:

`sum(w_i + 200) <= U - L + 200`.

The vertical construction is symmetric. Downward division by a fixed positive
quantum yields a weaker necessary integer inequality. No validator tolerance or
increased clearance is used, and the argument covers every closed anchor cell.

[The first probe audit](h5-strip-capacity-models-20261107/first-capacity-audit.json) checks 9,054 source
members and 76 nonconflicting pairs in four selected counterexamples. Each
selection obeys all graph pair clauses but violates its source strip bound.
These are **partial counterexamples to pair clauses alone**, not full-model
witnesses or valid placements. The complete preparation/audit processes take
0.692667/0.368121 seconds.

[The deterministic capacity set](h5-strip-capacity-models-20261107/capacity-set-audit.json) retains those
four bounds and adds three source-certified inequalities per case. Candidate
lines and strips are frozen before preparation; a deterministic overlap-aware
selection chooses diverse bounds. All **19,589 source members and 16 inequalities**
pass independent geometric readback. Complete preparation/audit processes take
1.503837/0.447901 seconds. [The exact constraints](h5-strip-capacity-models-20261107/capacity-constraints.json)
preserve original cell indices, source weights and strip definitions.

## Weighted Boolean encoding

Cells with the same weight are grouped only inside an already verified complete
conflict clique. Each class has an explicit OR variable. Since at most one cell
in the full clique can be selected, the class weighted sum equals the original
selected-cell weighted sum. Dividing all weights by their gcd and flooring the
bound is exact for that integer sum.

An acyclic prefix circuit represents `Y[i,j] = (weighted prefix i >= j)` by
`previous[j] OR (selector[i] AND previous[j-weight[i]])`. A final negative unit
forbids threshold bound+1. Every local gate truth table, source class, clause,
variable index and final unit is checked independently; all original pair
conflicts and both eight-part family requirements are preserved.

[Exhaustive small controls](h5-strip-capacity-models-20261107/encoding-controls.json) cover 121 weight
vectors, 14,930 selector/bound assignments and 216,260 exact weighted-prefix
checks. [The complete research-model audit](h5-strip-capacity-models-20261107/frontier-audit.json) verifies
659 weight classes, 77,267 weighted gates, 2,968,117 total clauses, all 15,208,033
original graph conflicts and all 33,803,472 graph pairs. Source cell-capacity
proofs cover all 16,267 cells. Every case includes new source information; the
closed earlier models are not called again.

## Four closed limited results

[The batch](h5-strip-capacity-models-20261107/batch-process.json) closes in **138.118836 seconds**.
Each call preserves the frozen 60-second search, one-million-conflict, 64 MiB
proof and 2 GiB aggregate-memory limits, complete process limits and Windows
Job Object descendant closure. [All four results](h5-strip-capacity-models-20261107/case-results.json)
stop at the proof-byte cap, with no accepted proof, assignment or active child.
The first [read-only stream inspections](h5-strip-capacity-models-20261107/stream-inspection.json) find
no complete prefix ending in an added empty clause; all streams retain their
truncated endings. No checker call or exclusion follows. These calls remain
closed and will not be repeated, reseeded or extended.

The remaining empty-site triples are [0,5,10], [5,10,11], [10,11,12] and
[11,12,13]. [The next constructive hypothesis](h5-strip-capacity-models-20261107/next-step.json) frees
12 cog positions with the validated nine-part small sheet. The earlier
[independent-row constructions](h5-expanded-joint-and-staged-row-constructions-20261104.md)
used 13 cogs with an 11-part small sheet. Their closed results do not establish
this new source domain. Fresh stock/core domains, mover/row and row/row regions,
source identity controls and complete preparation charges must precede a new
bounded construction. No full66 source/native/material validation, 60/90-second
construction claim or production integration is asserted here.

Production, READMEs and release assets remain unchanged. All failed and limited
bytes are preserved. [The manifest](h5-strip-capacity-models-20261107/raw-manifest.json) contains
208 new canonical members in 2
ZIP parts, totaling 65,357,241 bytes.
[Historical references](h5-strip-capacity-models-20261107/external-evidence.json) and
[source bindings](h5-strip-capacity-models-20261107/source-bindings.json) retain the earlier evidence.
Independent archive verification is required before commit.
