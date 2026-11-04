# First57: full-stock obstacle packing and interaction factorization — 2026-11-04

Two new source-audited full-stock constructions close **UNKNOWN**, with no
placement. The second preserves all collision checks while removing **87.4%**
of the initial model's repeated rectangle references. It reaches search after
11.10 solver seconds and explores 2,005 branches, but finds no assignment.
Both calls remain closed. H2/H5 remain open at **60% completed milestone weight**.

The [necessary-capacity checkpoint](h5-first57-necessary-capacities-20261104.md)
still leaves 259 of the original 455 fixed-core cog selections. These two
positive constructions enumerate the original 455 choices without consuming
those capacity tables. They establish no new exclusion. All 440 whole-job
allocations remain.

## A new full-stock positive representation

The previous grouped-region construction used a top-strip anchor domain.
This approach freshly derives anchor bounds from the **full physical first
sheet**, including side spaces below that strip. Each of the 16 moving originals
retains its legal modes, original contour and identity; the direct source-valid
short9 and fixed29 remain in the complete 66-part inventory.

[The source-cover audit](h5-first57-full-stock-obstacles-20261104/obstacle-source-audit.json) verifies all 21
convex pieces of the original rotated cog across 218 horizontal bands. The
bands include every source vertex level and each 2 mm level. Independent
edge/level intersections check **702 piece-band slices** and **435 merged
horizontal intervals**. Outward rounding on the 0.01 mm grid and translation
produce **6,554 source-covering rectangles** across the 15 cog sites and fixed
core. Every rectangle extends 0.23 mm to the right and top.

A separate integer event-count replay checks all **10,998,176 mask cells**.
Their **10,497 output rectangles** have disjoint interiors and retain 43 masks
that identify the fixed sources they cover. All source boundaries are covered.
A rectangle is present when its mask names an occupied cog or includes the
mandatory fixed-core bit.

[The moving-source audit](h5-first57-full-stock-obstacles-20261104/moving-source-audit.json) independently
verifies all **12 legal modes**, **20 outward source-covering rectangles** and
**256 original-vertex stock inequalities**. Each allowed anchor retains at
least 0.025 mm stock reserve. Twenty-four rigid components represent the eight
brackets and eight inserts. Sixteen groups, each with one component per owner,
cover all **268 different-owner component pairs** at least four times.

Using 0.23 mm right/top expansions for both fixed and moving source covers
makes nonoverlap imply at least 0.23 mm original-source clearance. Same-owner
components remain free to overlap. Fixed frame holes remain filled because
common-line part-in-hole is disabled. These are conservative positive
construction proofs; they are not exhaustive infeasibility arguments.

The obstacle preparation completes in **0.678468 s**, and the fresh moving
geometry completes in **0.125355 s**. Their independent audits take
1.729216 s and 0.044422 s respectively.

## Direct obstacle model

[Every model field passes readback](h5-first57-full-stock-obstacles-20261104/direct-model-audit.json):
**324 variables and 22,065 constraints**, 96 mode selectors, 15 empty-site
selectors and 37 shared optional-obstacle literals. The remaining six masks
include the fixed core and are unconditional. Exactly three cog sites are empty.
There are no region selectors, guarded polygon planes, hints, objectives or
imported capacity cuts.

Each of the 16 packing groups includes all 10,497 fixed obstacle rectangles.
This yields **168,208 rectangle references**. The complete model-build process
takes **1.082829 s**, and all charged preparation totals **2.344497 s**.

[Independent response readback](h5-first57-full-stock-obstacles-20261104/direct-response-audit.json) verifies
one closed UNKNOWN call, **52.828850 s allocated solve time** and
**46.624458 s returned solve time**. The log reports that it stopped after
presolve, with zero branches and conflicts. Preparation-inclusive
algorithm/shared totals are **49.817690 / 49.892755 s**. There are no overruns,
incumbents, assignments, source66 checks or native calls.

## Exact interaction factorization

The repeated fixed-obstacle references can be reduced without changing the
feasible source placements. Group zero already contains one component of
every moving owner. The eight bracket components absent from that group can
share one additional group. Fixed obstacles need appear only in these two
groups; all sixteen original moving-pair groups remain.

[The independent interaction proof](h5-first57-full-stock-obstacles-20261104/interaction-factorization-audit.json)
expands the group memberships and verifies exactly the same **268 moving-pair
requirements**, all **251,928 moving/fixed pairs**, and zero same-owner pairs.
Fixed/fixed pairs are already disjoint by the exact obstacle partition.
Rectangle references fall from **168,208 to 21,258**, an **87.3621% reduction**.
The factorization is recomputed inside the complete model build.

[The revised model audit](h5-first57-full-stock-obstacles-20261104/factorized-model-audit.json) reads every field
of **324 variables and 22,066 constraints**. It has 17 packing groups, only two
of which contain fixed obstacles. Build time is **0.998697 s**, and complete
charged preparation totals **2.260366 s**.

[The revised response audit](h5-first57-full-stock-obstacles-20261104/factorized-response-audit.json) verifies
its one closed UNKNOWN call. Search begins after **11.10 solver seconds** and
records **2,005 branches and 77 conflicts**, with no incumbent or assignment.
Allocated/returned solve times are **52.947644 / 53.015465 s**. The
**0.067821 s solve-slice overrun** is preserved; preparation-inclusive
algorithm/shared totals **56.082547 / 56.165577 s** stay within the original
60/90-second limits.

The input reference reduction does not imply the same reduction after solver
presolve: the log reports 178,517 rectangle references in the transformed
model. This is retained as a limitation of the representation.

[The assignment-reader controls](h5-first57-full-stock-obstacles-20261104/assignment-reader-controls.json)
verify the independent rectangle sweep against 106 brute-force cases and four
optional-interval controls. It checks fixed/fixed as well as moving/fixed and
moving/moving interactions. The source reader is prepared to reconstruct all
66 originals, but neither call produced an assignment to read.

## Remaining work

The [next-step record](h5-first57-full-stock-obstacles-20261104/next-step.json) preserves both closed models.
Before another construction, inspect the full-stock side-pocket domains and
earlier corner-channel evidence. A new source-valid fixed placement in a
previously excluded side space could reduce the number of moving parts; that
is a hypothesis requiring fresh source checks, not an established placement.
Neither model may be restarted, reseeded or extended.

The retained necessary frontier is 259 selections; the older fixed13-cog
frontier remains two selections / three count distributions. Full66 source
checks, native/material validation, integration and the H5 matrix remain
required. H2 retains its original gate and all 22 reserved vectors remain
unopened. No release qualifies.

Main 69c10624 contains the preceding two checkpoints after the prior main run
passed all six jobs. Its
[new CI run](https://github.com/skulitom/Nestbolt/actions/runs/41915862899)
is still running at this checkpoint. This evidence waits for all six jobs and
the aggregate result before another normal push.

The [manifest](h5-first57-full-stock-obstacles-20261104/raw-manifest.json) contains 109 new canonical
members and 4,147,894 compressed bytes.
[Historical references](h5-first57-full-stock-obstacles-20261104/external-evidence.json) and
[source bindings](h5-first57-full-stock-obstacles-20261104/source-bindings.json) retain exact inputs. Independent
archive readback verifies all new/reused members, source hashes and local links.
