# Mixed frame roof and finite contact construction — 2026-11-07

The changed frame arrangement leaves **17 mutually compatible cog sites**.
However, the complete finite model cannot select the required fifteen sites
together with six brackets and twelve inserts from its sampled contact pool:
the one declared call returns **INFEASIBLE** after **2.227445 s**. This is the
solver's result on a finite pool, not a continuous or whole-allocation exclusion.
There is no complete candidate, native call or H5 credit. H2/H5 remain open at
**60% completed milestone weight**.

## Changed fixed geometry and source control

The large sheet fixes sixteen quarter-turned frames in a four-by-four base,
then two unturned frames along the left side of its top edge. The resulting
step differs from both the closed 5/5/4/4 all-turned frame construction and the
three-column core. The short sheet retains the audited six-bracket/nine-insert
arrangement. All **33 fixed originals** pass source checks.

The left region above the frames admits a three-by-three cog grid and the right
region a two-by-four grid. Both use the exact source-contact phase near 6.75°
and 261.766 mm pitches. Seventeen denotes candidate sites; the job still requires
exactly fifteen cog copies. [Independent source readback](h5-mixed-roof-contact-construction-20261107/source-audit.json)
checks every one of 136 site pairs and 306 site/frame pairs. Minimum original
clearances are **0.301547629 mm** between sites and **0.268862770 mm** to frames,
above the unchanged required 0.211708673 mm.

[All eighteen frame recipes](h5-mixed-roof-contact-construction-20261107/frame-controls.json) are independently
reconstructed. Their nominal rectangles pass 153 exact rational axis-separation
checks; the actual trigonometric bounds differ by less than 1e-9 mm. One control
using exactly the first fifteen sites contains **48 original parts**, passes
633 pair checks and 192 stock edges, and retains 60 holes with 6,366 vertices.
Six brackets and twelve inserts are missing. It is not a new best partial or
full66 result. Complete consumed source preparation is **4.136496 s**.

Historical contact pools, source Minkowski regions and mixed component searches
are acknowledged and bound as inputs. No claim that contact sampling or finite
cog pools are unprecedented is made; the fixed obstacle geometry is changed.

## Finite contacts and complete conflict graph

For each of the **136 choices of two unused sites**, the generator considers
eight bracket modes and two physically distinct insert modes. Source convex-piece
Minkowski obstacles, expanded by a 0.23 mm square, give conservative free regions
against the frames and the fifteen selected cogs. Each free polygon contributes
a representative point and all boundary vertices. Centers are rounded once to
0.000001 mm and independently checked using actual original outlines.

[The contact audit](h5-mixed-roof-contact-construction-20261107/contact-audit.json) replays **1,360 contexts and all
4,445 unique contacts**, including 155,575 original checks against fixed frames
and cog sites. All are individually source-safe after omitting their recorded
conflicting sites. Maximum distance-replay difference is 5.68435e-13 mm. A frozen
round-robin rule retains **1,024 brackets and 1,024 inserts**; no arbitrary
post-result expansion or thinning occurs. The conservative regions and finite
samples do not claim complete continuous coverage.

[Independent full graph readback](h5-mixed-roof-contact-construction-20261107/graph-audit.json) checks every one of
**2,096,128 unordered candidate pairs** without geometric pruning. It reproduces
all **231,343 conflict edges** and **3,167 pose-to-cog-site conflicts**. All source
quantities and mappings remain unchanged. Complete consumed contact and graph
preparation totals are **7.893946 s** and **9.665682 s**, respectively.

## Exact inventory model and closed solve

The model has **2,065 Boolean variables and 234,513 constraints**. It selects
exactly six brackets, twelve inserts and fifteen cog sites, adding them to the
33 fixed originals. Every candidate conflict and pose/site conflict is present.
There is no objective, hint, relaxed count or partial-inventory acceptance.

[Independent protobuf reconstruction](h5-mixed-roof-contact-construction-20261107/model-audit.json) checks every
saved variable and constraint field. [Five deliberate corruptions](h5-mixed-roof-contact-construction-20261107/negative-controls.json)
are rejected, and [two tiny synthetic tool controls](h5-mixed-roof-contact-construction-20261107/synthetic-tool-controls.json)
confirm the installed OR-Tools 9.15.6755 behavior. These synthetic tests are
separate from the one original placement call. Complete preparation, including
all consumed source lineage and full model construction, is **11.631014 s**.

The declared solver uses four workers, seed zero, `fj` excluded, and at most
40 solve seconds within preparation-inclusive 60/90-second algorithm/shared
limits. It returns no assignment or incumbent. The saved response reports
2,594 branches and two conflicts; these are response counters, not a sum of
all portfolio workers. [Independent response readback](h5-mixed-roof-contact-construction-20261107/response-audit.json)
verifies exact parameters, source hashes, raw status, log, no hidden candidate
or native check, and all process limits.

Algorithm/shared totals are **14.700575/14.803571 s**, with no solve or overall
overrun. Peak aggregate committed memory is **186,945,536 bytes**; [all three
search processes close](h5-mixed-roof-contact-construction-20261107/closed-process.json). The call remains closed
despite unused time. Its finite-pool INFEASIBLE status does not prove that this
frame arrangement, allocation, or unrestricted original job is impossible.

## Next source scope and repository

[The next source preflight](h5-mixed-roof-contact-construction-20261107/next-step.json) assesses continuous original
cog centers and angles, together with the six brackets and twelve inserts,
against the changed fixed frame roof. Every legal orientation needs independently
certified hard source-safe cells. Multiple cog cells must be represented in mode
bindings, equivalence and neighbor enumeration. No successor continuous geometry,
complete initializer or optimizer call is prepared. All consumed preparation
must be charged and all current calls remain closed.

Four earlier fixed arrangements and **440 whole allocations** remain unresolved.
Full66 source/native/material checks, production parity and the unchanged H5
matrix remain required. H2 keeps its original gate and reserved vectors.
Production, README and releases are unchanged; no release qualifies.

[The previous two checkpoints reached main 6b81bf9d](h5-mixed-roof-contact-construction-20261107/prior-main-push-receipt.json)
after all six prior checks and aggregate CI passed, preserving all 52 remote
files. [Fresh main CI is running at review](h5-mixed-roof-contact-construction-20261107/main-ci-at-review.json).

[The raw manifest](h5-mixed-roof-contact-construction-20261107/raw-manifest.json) and [source bindings](h5-mixed-roof-contact-construction-20261107/source-bindings.json)
preserve source evidence and exact prior archive references. Four installed
runtime files are [separately pinned by hash](h5-mixed-roof-contact-construction-20261107/runtime-bindings.json),
including the Python executable and OR-Tools wrapper/native/protobuf modules;
vendor runtime bytes are not bundled into this evidence archive.
