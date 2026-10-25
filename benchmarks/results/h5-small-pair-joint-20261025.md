# H5: contacts from coordinated small-part pair releases — 2026-10-25

**No improvement on the checked 63-part area result.** The new global search
returns 11 brackets, 19 inserts, all 18 frames and all 15 cogs. One bracket
and two inserts remain missing. Both earlier 64-part baselines are preserved.
The full bound remains unresolved; H2/H5 remain open at **60%** completed weight.
Generation and graph audits finished on October 23. After the interruption,
their saved results were verified and reduction/search completed on October 25.
No completed generation or search was restarted.

## Updated repository and stop rules

Main added the [Inkbolt key-rack example](https://github.com/skulitom/Nestbolt/commit/4045822eb1fce0bb9253d637ca56df8b22cc8b6e)
and related website links. All six checks and its Pages deployment pass.
Merge **55835d7c** preserves all nine incoming files and all 37 files from local
checkpoint **23cb3074** byte for byte. The merge and checkpoint were pushed
normally to main. The merge's own run 40228140192 is captured as
`in_progress` / `pending`.
The engine/benchmark source digest and all three READMEs remain unchanged.

The [published Studio description](https://sparrowstudio.app/) still explicitly
excludes fixed-sheet allocation and placing parts in holes. GitHub API evidence
confirms unchanged Sparrow head 1fe3e314, latest v0.3.0 and Studio head c0bb9e86.
The cached browser release page was stale; the saved current API response is
the release evidence. No stop rule fires. Preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain current; this diagnostic work does not qualify a new release.

## Fresh pair-conditioned contacts

Both distinct 63-part layouts from the previous search are retained exactly.
A complete census measures **582** same-sheet small-part pairs. The declared
25 mm adjacency rule selects **60** pairs. Each neighborhood temporarily
releases its pair and fixes the remaining 61 original placements. Ten permitted
orientation/reflection classes are queried on the released sheet. The other
sheet is unchanged from the previously checked empty full-layout insertion
regions. These pair restrictions generate geometry only: the later global
model can move every small part across any of the seven original fixed cores.

All **600 queries** finish in **9.041197 seconds** within
90 seconds; 438 regions are empty. Every one of 150 cached obstacle first uses
agrees with a direct global original-outline calculation. The verified explicit
128-sided offset provides 0.0126 mm construction padding against the remaining
parts and stock. It does not qualify the unchanged cores for the native guard.

The separate 90-second proposal phase finishes in 1.933677
seconds. It records 6,330 events: **3,435 new positions** (1,435 brackets and
2,000 inserts) and 2,895 exact duplicates. All bracket lists finish. The insert
cap leaves **27 deferred lists**, preserved with exact cursors. None is resumed.
Every new pose is blocked by at least one released part; no valid simple
append opportunity is found in either original 63-part layout.

Independent verification in **9.990301 seconds** matches 15 source
members to committed manifests; reconstructs the complete pair census, ordering,
all regions/proposals and the capped queue; and checks 306,525 original fixed-part
relationships plus 12,660 released-part relationships. All **24,045** new
position/core memberships agree between individual-part and complete core-union
distances. The audit checks 144,240 distinct core-part distances and 3,066 core
pairs, retaining all 14,046 old memberships only after exact mapping/hash checks.
Both 64-part and both 63-part baselines pass all 5,976 same-sheet pair checks.

## Global graph, reduction and one bounded search

The complete graph includes **17,481 choices**: 7,632 brackets and 9,849 inserts.
The unchanged old graph contributes 19,719,151 geometric conflicts. Fresh
construction adds **9,256,960** new-old/new-new conflicts, for **28,976,111**
total. No derived cog clique or compatibility-based conflict omission is used.
Construction takes 63.271440 seconds. Independent reconstruction takes
35.267519 seconds, considers 34,797,215 same-sheet possibilities and
checks 11,260,927 exact distances. Every row matches and every old-old row remains
unchanged; all four baseline mappings stay valid.

Fresh same-family substitutions require adjacency, every conflict neighbor
and a superset of compatible cores. They finish in **17.815479 seconds**
and 14,517,128 comparisons within 30 seconds / 50 million comparisons, retaining
**5,182** choices. Independent certificates enumerate 33,296,614 neighbor
relationships and 68,589 core memberships. The induced 4,497,418-edge graph
compresses completely into 10,073 cliques in **7.896664
seconds**, within 20 seconds. Every edge reconstructs; there are no residuals.
All four baselines retain their original counts and area. No extra greedy search
is run. Retained choices include **426 new positions** (178 brackets and 248
inserts). Every core retains some compatible new positions. Of the 3,009 removed
new choices, 1,067 have certified old replacements and 1,942 have new replacements;
311 old choices have certified new replacements.

Every binary model and parameter field independently reconstructs. The model
has **5,189 variables** (5,182 poses plus seven cores) and
**15,224 constraints**. The original area floor remains 815,800,000;
the 63-part hint scores 816,200,000 and full inventory requires 895,800,000.
Exactly one 18-frame/15-cog core and the original 12-bracket/21-insert caps apply.
The higher-area hint does not exclude the two 64-part baseline solutions.

One eight-worker, seed-zero, presolve-disabled call uses the declared 60-second
allowance. Actual wall time is **61.691101 seconds**, preserving the soft
overrun. The hint appears at 0.164122 seconds and search starts at 0.22 seconds;
worker logs show 1,206,401 branches for the core worker. One callback and a
distinct final result retain score 816,200,000 in core 3. Status is `FEASIBLE`,
with full bound 895,800,000 unresolved. The call is not repeated or extended.

All **3** returned/hint layouts pass original
transforms, stock, material and all 1,467 same-sheet pair checks apiece. Two
fresh frozen-CLI checks and one exact-layout reuse fail only the original
missing quantities. Filled area remains 4402140.784069743 mm² and
material 4988890.203494999 mm². Minimum separation is
0.200122540483 mm; native-margin qualification remains absent.
The final uses five new pair-contact positions. No production quality run,
native packing call or held-out evaluation occurs.

## Next geometry question

Assess a continuous geometric area relaxation for all seven fixed 33-part cores before another pose-enrichment search. Use all original permitted bracket and insert orientations/reflections, both unchanged stock domains and zero-clearance translation regions as an intentional relaxation of the positive-clearance requirement. Construct conservative outer covers of every possible occupied point, with explicit numerical padding and coverage checks, then compare combined and per-family area bounds with the full 12-bracket/21-insert inventory. Verify every known compatible pose and both 64-part and both 63-part seeds are contained before drawing any conditional conclusion. A bound above the required area is inconclusive; a finite candidate failure is not a geometric impossibility proof. Declare bounds and preserve partial work before execution. Do not repeat or extend the completed pair-contact solve, resume its 27 deferred insert lists or the older 1,950 member lists, weaken counts, or lower the native guard. All 66 original parts, original material target and production budget, native qualification and all 13 jobs at both kerfs remain required.

Evidence: [generation](h5-small-pair-joint-20261025/generation.json), [original geometry](h5-small-pair-joint-20261025/geometry.json),
[graph](h5-small-pair-joint-20261025/graph.json), [independent graph audit](h5-small-pair-joint-20261025/audit.json),
[reduction](h5-small-pair-joint-20261025/reduction.json), [model](h5-small-pair-joint-20261025/model.json),
[solver](h5-small-pair-joint-20261025/solver.json), [original layouts](h5-small-pair-joint-20261025/layouts.json),
[final layout](h5-small-pair-joint-20261025/final-layout.json), [retained positions](h5-small-pair-joint-20261025/retention.json),
[merge/stop-rule audit](h5-small-pair-joint-20261025/reconciliation.json), [source review](h5-small-pair-joint-20261025/source-review.json),
raw evidence [part 1](h5-small-pair-joint-20261025/raw-001.zip), and [manifest](h5-small-pair-joint-20261025/raw-manifest.json).
All 863 canonical members and 53
aliases are byte-verified, with CRC and SHA-256 checks. Each ZIP part is
independently readable and below 50 MiB.
