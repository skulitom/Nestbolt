# Frame orientations and fixed-core capacity — 2026-11-07

**Seventeen source-valid 48-part cores** emerge from three declared frame
patterns. An independently checked necessary-area proof excludes **five** of
those exact cores; **twelve remain unresolved**. No optimizer runs. There is no
new full 66-part layout and the preserved valid 64-part result remains best. H2/H5 remain open at
**60% completed milestone weight**.

[The complete orientation census](h5-orientation-roof-capacity-20261107/orientation-classes.json) enumerates
all 4^6 quarter-turn vectors for each of two checked 39-owner model scopes.
Identical nominal occupied frame outlines and effective hard domains reduce
them to 64 ordered binary vectors and seven orientation-count classes.
Their multiplicities are 64 times the corresponding binomial coefficients.
The [four closed calls](h5-orientation-roof-capacity-20261107/historical-closed-calls.json) used turned counts
4, 4, 4 and 0. The fixed source geometry and frame domains match exactly after
copy labels are ignored. This classification concerns occupied outlines;
original holes remain preserved and are not nesting space. Earlier broader
models are bound in the archive: no class is claimed globally untested or
excluded merely because these four calls failed.

[Fresh source construction](h5-orientation-roof-capacity-20261107/source-plan.json) reads only the original
job and [unchanged normal acceptance metrics](h5-orientation-roof-capacity-20261107/benchmark-target.json)
as numeric inputs. Twelve turned base frames and the six-bracket/nine-insert
short-sheet modules are reconstructed. Above the base, three unturned frames
form the first roof row. The second roof row has one, two or three turned
frames, with the other frames unturned. One cog phase is derived from source
tooth vertices; all convex-piece difference hulls determine one outward axis
pitch. There is no phase or pitch sweep, old coordinate seed or resumed call.

The one-turned pattern uses 15 cog sites. The two- and three-turned patterns
each propose 16 sites, with every single-site omission checked. Thus all
**33 declared cases** receive complete original-source readback. [Independent
source checks](h5-orientation-roof-capacity-20261107/source-audit.json) replay all 33 cases, **882 axis sections**
using a separate hull/line calculation, **1,191 direct pool/frame distances**
and **1,980 original holes across the cases**. The one-turned case and all 16
two-turned cases pass. The three-turned pool has collided pairs 3/14 and 7/15;
deleting one site cannot remove both collisions. All 16 failures are preserved.
The smallest passing cog/cog gap is **0.301548 mm**.

[Necessary covers](h5-orientation-roof-capacity-20261107/necessary-cover-plan.json) consider all eight allowed
bracket orientations over the entire physical first stock. Source-contained
inner rectangles induce open forbidden center rectangles at zero clearance.
Every axis boundary point and intervening open interval is represented.
Cog-site masks produce all omission cases together; fixed frames cannot be
omitted. These are necessary outer covers, not sufficient placement domains.

[Independent proof readback](h5-orientation-roof-capacity-20261107/necessary-cover-audit.json) verifies
**2,423 source-contained rectangles** and **40,376,496 continuous classes**
using signed corner counts and prefix sums instead of the producer's slice
assignment. Every retained class is covered with its correct mask. Exact
integer unions of outward occupied rectangles bound all possible bracket
footprints. A conservative **39,999 mm²** per bracket includes the checked
floating area allowance; six brackets are required.

| Exact fixed core | Occupied-cover area (mm²) | Brackets at most | Outcome |
|---|---:|---:|---|
| One turned roof frame, all 15 sites | 99,544.864275 | 2 | Cannot extend to 66 parts |
| Two turned roof frames, omit site 2 | 158,995.726128 | 3 | Cannot extend to 66 parts |
| Two turned roof frames, omit site 4 | 158,995.726128 | 3 | Cannot extend to 66 parts |
| Two turned roof frames, omit site 5 | 158,995.726128 | 3 | Cannot extend to 66 parts |
| Two turned roof frames, omit site 6 | 158,995.726128 | 3 | Cannot extend to 66 parts |
| Other twelve two-turned cases | 260,889.014200–341,336.756218 | 6–8 | Unresolved |

[Every exact case and bound](h5-orientation-roof-capacity-20261107/fixed-core-capacities.json) is retained.
A bound of six or more does not establish feasibility. Moving a frame or cog
changes the fixed-core problem; no orientation class or whole allocation is
excluded. Four earlier arrangements and 440 allocations remain unresolved.

[Source preparation](h5-orientation-roof-capacity-20261107/orientation-roofs-process.json) takes **1.557235 s**,
and [necessary-cover preparation](h5-orientation-roof-capacity-20261107/orientation-roof-covers-process.json)
**10.629206 s**: **12.186441 s** total if consumed. Full source and proof audits
take **1.920012 s** and **11.192307 s**, separately. The census takes 0.226364 s.
Each bounded Job Object closes all three processes under the 2 GiB cap, logical
CPUs 16–31 and single BLAS/OMP/MKL threads. No time limit is relaxed and no
closed computation is restarted.

[Next](h5-orientation-roof-capacity-20261107/next-step.json), compute source-necessary insert covers and
combine them with the bracket covers for the remaining twelve exact cases.
Only a case surviving the coupled screen can justify a complete companion
model and bounded search. Full source/native/material validity, product
integration, UI/CLI/MCP parity and the original H5 matrix are still required.

[Main a45826d3](h5-orientation-roof-capacity-20261107/prior-main-push-receipt.json) contains the earlier two
checkpoints, pushed ordinarily after all six prior checks passed with 52
protected files intact. Its [current CI snapshot](h5-orientation-roof-capacity-20261107/main-ci-at-review.json)
has **5 passed / 1 live jobs**. The subsequent six-unturned checkpoint
and this evidence checkpoint await the ordinary main push gate. Product code,
README and releases are unchanged.

[Archive checks](h5-orientation-roof-capacity-20261107/archive-checks.json), [manifest](h5-orientation-roof-capacity-20261107/raw-manifest.json),
[source bindings](h5-orientation-roof-capacity-20261107/source-bindings.json), [historical references](h5-orientation-roof-capacity-20261107/external-evidence.json)
and [runtime pins](h5-orientation-roof-capacity-20261107/runtime-bindings.json) preserve inputs and outcomes.
