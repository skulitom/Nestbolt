# H5: joint selection with continuous cog contacts — 2026-10-23

**Best checked result remains 64/66, missing two brackets.** One fresh
conditional model includes all 4,000 verified new cog poses together with the
16,058 old variable choices and the same 30 fixed cores. The 60-second search
returns `FEASIBLE` at the original area floor; the full upper bound remains
unresolved. No returned layout uses a new cog pose. This is neither an
optimality proof nor H5 acceptance. H2/H5 remain open at **60%** completed weight.

## Complete constraints and provenance

All 20,058 choices are retained before fresh reduction. Eleven source members
match their committed evidence manifests, including the unchanged unreduced
old graph and independently audited new geometry. Original pool records, core
positions, compatibility and all 30 mapped 64-part baselines remain intact.

The old graph contributes **17,012,982 geometric edges**.
A fresh spatial-tree construction adds **6,917,176**
new cog/bracket or cog/insert conflicts. An independent sequential bounds scan
checks 37,181,052 same-sheet possibilities
and 7,602,455 exact distances, finding the
same new conflicts. Construction and serialization take 66.136551
seconds; the independent graph audit takes 36.453262 seconds.

The original job requires 15 cogs and each of the 30 fixed cores already has
14. The variable cog cap is therefore exactly one. An explicitly declared
complete clique on **5,462** variable cog choices is already implied by that
unchanged count cap. Its **14,913,991** edges are
count-derived mutual exclusions, including geometrically disjoint and
different-sheet pairs; they are not reported as measured collisions.
Of these, 244,993 old geometric edges
already existed; **14,668,998** are additional
constraint edges. The total graph has **38,599,156**
edges, and every row independently reconstructs. Zero variable cogs remain
permitted when the original area floor is met.

## Fresh reduction and bounded search

Same-family substitutions require an adjacent retained replacement, inclusion
of every verified constraint neighbor and a superset of compatible cores.
The pass completes in **13.705953 seconds** and 17,392,850
comparisons within its 30-second / 50-million allowance. It removes
13,250 choices and retains **6,808**.
Independent certificates enumerate 49,423,500
neighbor relationships and 213,661
core memberships. All 30 baselines keep their counts and area.

The exact induced graph has **5,197,983** constraint edges.
Compression first records the verified clique on the retained
**990** cogs, then performs first-fit expansion.
It completes in **6.835164 seconds**, including the seeded
clique, within the 20-second limit. All 13,152 cliques
reconstruct every edge; **no residual edges remain**. No additional greedy
hint search occurs, and no earlier reduction or capped proposal list is resumed.

Every binary model and parameter field independently reconstructs. The model
has **6,838** variables (6,808 pose choices and
30 core choices) and **19,906** constraints. The original variable
area floor is 865,862,719 and full inventory requires 945,862,719. A single
seed-zero, eight-worker solve uses a 60-second allowance with CP model presolve
disabled, as previously diagnosed. It runs for **60.505673 wall seconds**;
the soft overrun is preserved. The baseline appears at 0.237882 seconds and
search starts at 0.30 seconds. Worker logs record active search, including
1,045,013 branches for the core worker; zero aggregate counters do not mean
there was no search.

One callback and a distinct final layout retain the same score. The final
chooses core 15 and original cog 17355; it uses none of the new cog poses.
The bound remains 945,862,719. This completed call is not repeated or extended.

## Original layouts and next geometry to inspect

All **3** layouts, including the starting hint,
pass original geometry, transform, stock and all 1,521 same-sheet pair checks.
Each has 18 frames, 15 cogs, 10 brackets and 21 inserts. There are
2 fresh frozen-CLI calls and
1 exact-layout reuse; each result fails only the
original two-bracket quantity requirement. Best checked filled area is
4401740.784069743 mm² and material is
4988890.203494999 mm². Hint/callback separation is 0.2001 mm and final
separation is 0.201 mm; none is native-margin qualified.

The retained pool still contains **197 new cog poses** and
6,611 old poses. Of the 3,803 removed new poses,
2,082 have a certified old replacement and 1,721 a certified new replacement;
10 old poses have certified new replacements. The retained families are
2,660 brackets, 3,158 inserts and 990 cogs. **172** retained new cogs expose old
bracket choices, but none has a positive net count of gained minus lost old
bracket candidates in its generating core. These counts reflect the old
candidate pool, not geometric capacity or achievable part quantities.

A transparent recorded ranking selects at most one such pose per generating
core, up to six; **five** distinct review cores exist. Each fixes 18 frames
and all 15 cogs. All **2,190** original
same-sheet pairs pass. Their net old-bracket candidate changes are -24, -28,
-72, -615 and -694. They are explicit choices for inspecting new bracket and
insert contact positions, not improved or qualified layouts. The ranking,
all selected poses and both failed quantity checks remain preserved.

Investigate fresh bracket and insert contact positions around the five independently checked review cores in retention/review-cores.json, while retaining both original 64-part baseline cores. Each review core fixes 18 frames and all 15 cogs; generate new small-part contacts with the verified explicit clearance polygon, including coupled bracket/insert arrangements where useful. The recorded ranking selects different geometry for investigation; its candidate-count gains and losses are not inventory or material scores. Declare new generation and selection limits before execution, preserve pending lists, and do not resume the 60 prior cog proposal lists. A future conditional model must keep the original 12-bracket/21-insert inventory, both full baseline mappings, exact group compatibility and all relevant mutual conflicts; original variable-area floor is 815800000 and full small-part area is 895800000 for a 33-part fixed core. Do not retry or extend the completed continuous-cog solve, infer impossibility from its unresolved bound, or count any partial result as H5. All 66 parts, the original material target, native guard, original production budget and full 13-job/two-kerf matrix remain required.

No native packing, production-budget qualification, complete H5 matrix or
held-out evaluation occurs. All 66 copies, the original material target,
native guard, production budget and all 13 jobs at both kerfs remain required.
Source and all three accurate READMEs remain unchanged; preview v0.2.0-alpha.1
and stable Latest v0.1.0 remain current. Main facf0f38 run 39984899040 is saved
as `in_progress` / `pending`; 5e88ac91 is committed
locally and waits for main's remaining checks before the next normal push.

Evidence: [graph](h5-continuous-cog-joint-20261023/graph.json), [independent audit](h5-continuous-cog-joint-20261023/audit.json),
[provenance](h5-continuous-cog-joint-20261023/provenance.json), [reduction](h5-continuous-cog-joint-20261023/reduction.json),
[encoding](h5-continuous-cog-joint-20261023/encoding.json), [model](h5-continuous-cog-joint-20261023/model.json), [solver](h5-continuous-cog-joint-20261023/solver.json),
[original layouts](h5-continuous-cog-joint-20261023/layouts.json), [best layout](h5-continuous-cog-joint-20261023/best-layout.json),
[final layout](h5-continuous-cog-joint-20261023/final-layout.json), [retained geometry](h5-continuous-cog-joint-20261023/retention.json),
[review cores](h5-continuous-cog-joint-20261023/review-cores.json), [source review](h5-continuous-cog-joint-20261023/source-review.json),
raw evidence [part 1](h5-continuous-cog-joint-20261023/raw-001.zip), and [manifest](h5-continuous-cog-joint-20261023/raw-manifest.json). All
77 canonical members and 36
aliases are byte-verified, with archive CRCs and SHA-256 hashes checked.
Every ZIP part is independently readable and below 50 MiB.
