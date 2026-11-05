# Direct short9 and grouped first57 construction — 2026-11-04

**A new explicit short-sheet layout passes, but its matching first sheet remains
unresolved.** The sole new first57 call closes UNKNOWN with no assignment.
All 455 twelve-cog site choices and all 440 whole-job allocation candidates
remain. H2/H5 stay open at **60% completed milestone weight**.

## Direct source construction

The [short9 source layout](h5-direct-short9-and-grouped-first57-20261104/short9-source.json) is generated from
[two explicit modules](h5-direct-short9-and-grouped-first57-20261104/short9-module-spec.json), each containing two
turned L-brackets and one insert, beside a straight row of three original
cogs. Each module measures 330.46 × 310.46 mm; the declared module/insert gap
is 0.23 mm. Cogs use their exact original outlines at 7 degrees and 258.86 mm
pitch. No old optimized short-sheet placement or repair result is read.

[Independent original-source replay](h5-direct-short9-and-grouped-first57-20261104/direct-short9-audit.json)
passes all **36 pairs, 36 stock edges, 17 cutouts and 2,308 hole vertices**.
Minimum pair clearance is **0.214826983624 mm** and extra stock clearance
**0.025 mm**, above the unchanged required guards. Complete preparation,
including source checks and inventory construction, takes **0.296828 s**.
The historical valid short sheets and their closed searches remain unchanged.

The complementary [inventory](h5-direct-short9-and-grouped-first57-20261104/inventory.json) contains **57 first-sheet
originals**: 18 frames, 8 brackets, 19 inserts and 12 cogs. The existing 29-part
frame/side-insert core stays fixed; all **8 brackets and 8 remaining inserts**
are mandatory and independently movable. A separate 44-part reference control
checks the fixed29 plus all 15 candidate cog sites: 946 pairs, 176 stock edges,
44 cutouts and 4,414 hole vertices pass. This reference certifies each possible
twelve-site subset; it is not combined with short9 or claimed as a full layout.
All 66 source identities are accounted for exactly once in the target split.

## Fresh three-empty-site geometry

Unlike the earlier thirteen-cog construction, this allocation permits three
empty sites among fifteen: **all 455 triples** remain available. Every placement
region records which cog sites must be empty. Fresh preparation produces
490 nonempty masks and **3,941 convex regions** in **3.665490 s complete
process time**. The older two-empty-site bounds are not transferred.

[Source certification](h5-direct-short9-and-grouped-first57-20261104/source-region-audit.json) checks all 12
orthogonal modes and all 15 original cog poses. It verifies **158,834 exact
rational support proofs**, including 2,990 whole-cog-hull fallbacks to original
convex pieces. Minimum certified mover/cog clearance is **0.225999998970 mm**.
No rounded region degenerates. This proves retained-region safety, not complete
continuous free-space coverage.

The [integer and grouping audit](h5-direct-short9-and-grouped-first57-20261104/integer-and-pair-cover-audit.json)
reproves **16,157 inward integer-plane implications**, using local origin
(0,2100) mm, a 0.01 mm position grid and 100,000 normal scale. The absolute error
envelope is 1500 × 900 mm, with at least 0.0000001 mm inward reserve.
All20 source component-mode rectangles are rounded outward by less than 0.01 mm.
Complete integer/group preparation takes **1.365936 s**.

## Grouped packing model

The model uses hierarchical geometry/mask/region equations so each empty-site
implication is shared by all regions of that mask. Every original still selects
exactly one legal source mode and one matching source-safe region.

The 24 rigid components have **268 different-owner pairs**. The
[sixteen pair-cover groups](h5-direct-short9-and-grouped-first57-20261104/pair-cover-groups.json) each contain exactly
one component per original, and every different-owner pair appears in at least
four groups. A global NoOverlap2D constraint on each group enforces all pair
requirements without adding same-owner spacing. Extending each component's
right/top interval endpoint by 0.23 mm enforces the required component separation.
Independent exhaustive group coverage proves equivalence to all 268 pair tests.

[The complete model audit](h5-direct-short9-and-grouped-first57-20261104/model-audit.json) reads every field of
**35,735 variables and 143,671 constraints**. This includes 96 source-mode
selectors, 3,920 mask selectors, 31,528 region selectors, 129,256 guarded planes,
9,440 empty-site implications, 640 rigid coordinate links, 48 interval equations,
48 size equalities and 16 global packing constraints. All455 cog-site triples
remain available. There is no objective, hint or count-capacity pruning.

## Sole bounded response

[The final ledger](h5-direct-short9-and-grouped-first57-20261104/preparation-charges.json) charges **9.606485 s**:
intrinsic fixed-mode/site/rectangle preparation; complete direct-short9,
three-site-mask and integer/group processes; and **4.117213 s complete model
build**. The narrower internal build timestamp is preserved and replaced by
the complete process charge.

[Response verification](h5-direct-short9-and-grouped-first57-20261104/response-audit.json) checks 5,534 recursive
input bindings and the sole closed UNKNOWN response. It records **51,988
branches and 15,497 conflicts**, no incumbent and no assignment. Allocated/
returned solver time is **45.176238 / 45.325758 s**, preserving the
**0.149519 s** solver-slice overrun. Complete preparation-inclusive algorithm/
shared totals are **56.166951 / 56.264559 s**, within 60/90 s. No full66 source
reader, native validator or quality matrix is run.

The call will not be repeated, reseeded or extended. The grid, fixed cog sites
and conservative construction regions prevent any global negative conclusion.
[The next method](h5-direct-short9-and-grouped-first57-20261104/next-step.json) is to assess a necessary continuous
source-domain cover using exact source-contained rectangles, then prove any
capacity restrictions independently. The current positive regions cannot supply
that negative evidence. No such necessary cover or new exclusion is prepared.

Full66 original-source, native and material checks, integration and the complete
H5 matrix remain required. H2 retains its original gate and unopened reserved
vectors. Production and releases are unchanged; no new release qualifies.
Main f13dfba5 has three completed successful jobs and three active jobs in
[CI41908888838](https://github.com/skulitom/Nestbolt/actions/runs/41908888838)
at review; this checkpoint waits for all six jobs and the aggregate run before
a normal guarded push.

[The raw manifest](h5-direct-short9-and-grouped-first57-20261104/raw-manifest.json) contains 94 new canonical
members and 8,051,515 compressed bytes. [External references](h5-direct-short9-and-grouped-first57-20261104/external-evidence.json)
and [source bindings](h5-direct-short9-and-grouped-first57-20261104/source-bindings.json) preserve all historical
inputs. The independent archive reader verifies every new/reused member,
input binding and local report link.
