# Independent placement around the staggered core — 2026-10-28

The changed-core construction passes its geometry and serialized-model checks,
but its sole search closes **UNKNOWN**. No complete 66-part placement or
infeasibility result follows. H2/H5 remain open at **60% completed milestone
weight**, and the previous valid64 remains the best partial layout.

The saved staggered arrangement contains 18 frames, three brackets and five
inserts on the first sheet, plus six brackets and nine inserts on the short
sheet. Independent original-source readback reconfirms these 41 parts, 430
same-sheet pairs, 164 stock edges and all 59 holes. All 25 remaining originals
are mandatory: brackets 5, 6 and 9; inserts 13–19; cogs 0–14. The gross material
target remains 4,988,890.353495 mm². Part-in-hole remains off.

Every fixed-neighbour placement region is rebuilt against the changed 26-part
first-sheet core. Only the exact unchanged source modes and 66 intrinsic pair
displacement domains are reused. The independent reader verifies 286 fixed
neighbour relations, 13,299 Minkowski hulls, all 77 domains, 1,153 convex cells
and 4,163 conservative integer halfplanes. The cog phase of 7° is a constructive
subset; brackets retain all eight legal modes and inserts both outer classes.
The old staggered 2,000-pose finite-pool exclusion is not resumed or broadened.

A positive control places fifteen cogs in three aligned rows at 258.90 mm pitch
above the fixed core, with independent anchors rounded to one micrometre.
Original-source verification passes **925 pairs, 224 stock edges and 74 holes /
8,074 hole vertices**, plus 15 occupied free cells and 105 relative cells.
Minimum gap is 0.224800281 mm and extra stock clearance 0.024800286 mm.
This is a 56-part control only; three brackets and seven inserts remain unplaced.

The placement model has **47,272 variables and 170,594 constraints**, including
50 independent coordinates, all 300 mover pairs, 1,287 mode-pair groups and
13,245 valid partial hints. It imposes no lattice or fixed mover coordinates.
The independent reader accounts for every variable, constraint and hint, and
checks all 66 copy identities across fixed and moving inventories.

Necessary source capacities add 2,942 interval constraints and two cumulatives,
for **173,538 total constraints**. The source proof checks 139 contained
rectangles, 7,592 source segments and 4,197 same-owner component pairs. Fixed
L brackets use two strictly contained components each; no bounding-box exclusion
is substituted for their source geometry. All 1,471 rectangle options and the
complete unchanged model prefix are audited. The valid control has 1,409 active
components and X/Y capacity slack of 107,517 / 7,024 µm.

Only the complete formulation is solved, once, with four workers, seed zero,
a 60-second solver limit and 90-second shared-process limit. It returns
**UNKNOWN**, 82,996 returned branches and 13,173 conflicts. Solver time is
60.052929 s, returned time 60.076915 s and shared time 61.555241 s. The returned
soft overrun of **0.076915 s** is retained. The response, parameters, model hashes,
log and timings are independently read back. There is no assignment to validate
and no native call.

A separate bounded diagnostic keeps this control fixed and constructs the ten
non-cog free regions. All eight bracket regions are empty under the conservative
construction; both insert regions are nonempty. An independent oracle checks
their source-clearance containment against 82 neighbour relations and 2,410
Minkowski hulls. Empty conservative regions are **not** an actual placement
exclusion. They do show why this particular control does not directly supply
the missing brackets through this construction.

The next step changes the core construction: independently move all 18 frames,
three L brackets and five inserts to reduce their current 2,167.875 mm top.
This differs from the closed height search for the 18-frame/11-insert core.
Review prior mixed-core attempts first, retain the actual short15 allocation,
prove coverage of correctly partitioned expanded L geometry, and validate the
entire model plus the saved positive core before any new bounded call. A better
partial core would still leave all 25 other originals as explicit obligations.

Main d71c9c85 now has **all six jobs passing** in run 40728382102. The previously
verified capacity/height commit 116b16d7 and this checkpoint may be pushed after
fresh remote-reference and live-run guards. Production and all READMEs are
unchanged. Sparrow remains 6f7b9d35 / v0.3.0; Studio remains c0bb9e86 without a
release. No stop rule fires, no reserved H2 vector is evaluated, and no new
release qualifies.

Evidence: [source regions](h5-staggered-core-independent-placement-20261028/source-region-audit.json),
[source control](h5-staggered-core-independent-placement-20261028/source-control-audit.json),
[complete model](h5-staggered-core-independent-placement-20261028/complete-model-audit.json),
[response](h5-staggered-core-independent-placement-20261028/response-audit.json),
[residual regions](h5-staggered-core-independent-placement-20261028/residual-region-audit.json),
[next construction](h5-staggered-core-independent-placement-20261028/next-step.json),
[raw manifest](h5-staggered-core-independent-placement-20261028/raw-manifest.json).
The archive contains 273 canonical files and
261 identical-byte aliases in 10,778,295
compressed bytes, including all source inputs, helpers, models and closed-call
records. Earlier evidence and failed attempts remain preserved.
