# H5: individual frames and all small families — 2026-10-23

**Best checked result: 64/66 original parts, missing
{"bracket": 2}.** One new bounded model frees every
original frame pose individually while selecting cogs, brackets and inserts
together. The original target and full inventory are unchanged. It returns
`FEASIBLE`; full original target witness: `False`.
Native margins, production-budget qualification and the complete H5 matrix
remain required. H2/H5 remain open at **60%** completed milestone weight.

## Changed scope and independent geometry

The prior model selected one of 29 complete frame groups. This model removes
that construction restriction and retains all **35,488** independently checked
source poses: 2,499 frames, 12,317 brackets, 13,968 inserts and 6,704 cogs.
It adds 2,358 individual frame choices and 3,358 small choices relative to the
previous group model. Both original 64-part layouts map exactly by pose identity.
No new geometry is generated. All original reserved frame holes remain filled
for spacing checks; the 22 reserved evaluation vectors are not opened.

The fresh graph checks all family pair types, including frame/frame and
frame/small edges absent from the earlier group-filtered graph. Construction
takes 115.035364 seconds and checks 45,076,754
expanded-bound pairs. An independent sequential bounds scan covers
439,198,896 same-sheet possibilities and
45,075,283 exact distances. Both methods agree on all
**38,969,399 edges** and every binary adjacency row. All 35,488 original
poses reconstruct directly from source vertices with zero distance and area
error; stock bounds, permitted rotations and mirror flags pass. Both seeds'
3,042 same-sheet pairs pass independently.

All 86,944 original four-family count combinations preserve true filled-area
ordering under the integer objective. The seed floor is **4,401,740,785** and
full inventory requires **4,481,740,785**. Even all other families plus 17 frames
reach only **4,324,240,785**, so exactly 18 frames is already implied by the
original floor. The explicit frame equality strengthens propagation without
excluding any qualifying count combination. Original job, library, request,
target and family caps remain unchanged.

## Fresh reduction and bounded selection

The new same-family substitution pass performs 48,105,038 comparisons
in 30.000143 seconds, with its original 30-second / 50-million limits;
limit reached: `True`. It retains 25,752 choices
and removes 9,736 only with original neighbor inclusion
and a retained adjacent replacement. Independent certificates enumerate
13,746,181 neighbor relationships.
Both complete 64-part counts and area scores survive mapping. Every unprocessed
choice remains; no earlier reduction or capped list is resumed.

The exact induced graph has 27,098,196 conflicts. A fresh 20-second
first-fit cover yields 3,655 cliques and retains every
one of 8,159,356 residual edges. Full graph reconstruction passes.
The hint pass completes 1,960/1,960 new four-family relocation
starts in its 30-second allowance, retaining 0 pending
cases. Each completed case passes full-graph, count and objective checks; the
original score floor remains feasible.

Every model and parameter field is independently reconstructed. Larger cliques
and 25,652 aggregated residual implications retain every edge.
The final model has 25,752 variables and 29,312
constraints, no frame-group restriction, and explicit original family caps.
One eight-worker, seed-zero call has a **60-second allowance**, with CP model
presolve disabled as motivated by the preceding recorded diagnosis. It returns
`FEASIBLE` after **68.642298 wall seconds**, with 1
callbacks and reported bound 4481740785.0. Every soft overrun and full log
is preserved. This model is not repeated or extended.

All 3 original layouts are checked, including
the starting hint and each returned distinct final result. Original filled
outlines, permitted transforms, target stock, all pair distances, quantities
and the frozen CLI are verified: 2 fresh CLI calls
and 1 exact-layout reuses. The detailed layout
table retains every missing-quantity violation. The best checked filled area
is 4401740.784069742 mm², charged material 4988890.203494999
mm², and minimum separation 0.201100000000 mm.

Generation, reduction and solve timers are separate from graph serialization,
certificate enumeration and independent audits. These are development
diagnostics, not production-budget or full H5 quality measurements.

## Fixed-layout gap check and a different repair neighborhood

The distinct final layout also has 64 parts and minimum separation
0.201000000000 mm. Its frame poses differ from the original
wide seed by at most 0.069155043200
mm; nearest matching is bijective. The cogs match within
4.55e-13 mm. These are
small placement changes, not evidence of a different packing arrangement.

A fresh conservative insertion check fixes this exact final layout and checks
all 16 bracket rotation/reflection/sheet combinations in
10.760249 seconds. Every padded region is empty, with
no pending queries, proposals or added brackets. All original 1,521 pairs pass
and the exact unchanged CLI result is reused. Conservative padding makes this
a failed insertion diagnostic, not an impossibility proof.

The next repair neighborhood releases one cog together with every bracket
and insert. Each of the two exact checked layouts supplies 15 fixed cores,
each with 18 frames and 14 cogs: 30 distinct cores in total. Every fixed-core
pair passes. All 989,670 variable/core
memberships agree between the complete original graph and independent
distances to the filled core unions. Fixed poses are explicitly excluded from
variable choices, because graph diagonals are zero. This retains
16,058 choices: 6,176 brackets, 8,420 inserts and
1,462 cogs. All 30 complete 64-part starting layouts map back exactly.

The variable-area floor is 865,862,719; full quantities require 945,862,719.
The future conditional model must select exactly one core, retain all
compatible choices and conflicts, and cap variable counts at 12 brackets,
21 inserts and one cog. A zero-cog choice must remain allowed when it meets
the area floor. Coverage took 13.321599 seconds; no conditional
graph reduction or solver call is included yet. The full original 66-copy
requirement, material target and native/production qualifications remain.

## Next action

Build a fresh conditional selection model from the 30 independently checked one-cog-release cores. Project the audited unconditioned four-family graph onto all 16,058 eligible variable poses, retaining every relevant conflict and independently reconstructing the projection. Use only a fresh same-family substitution that preserves core compatibility as well as every conflict; retain all unprocessed choices. Preserve all 30 mapped 64-part seeds. Select exactly one 18-frame/14-cog core and allow up to one variable cog, 12 brackets and 21 inserts. Use one predeclared bounded solve with presolve disabled, as justified by the recorded presolve diagnosis. Recheck any changed original layout with the frozen CLI. Do not repeat the complete four-family solve, extend its limits, resume prior capped lists, infer native clearance qualification, open held-out vectors or start production quality evaluation without a full original 66-part witness.

## Repository and evidence

All six hosted checks pass for main 955cc87e. The queued 752b1c60 checkpoint
was then pushed normally to main; its run 39976658315 is saved as
`in_progress` / `pending`. No unobserved pass
is inferred. Production source and all three READMEs remain unchanged, with
preview v0.2.0-alpha.1 and stable Latest v0.1.0 still accurately described.
No new release, registry publication, held-out evaluation, native packing or
full H5 quality run occurs in this diagnostic checkpoint.

Evidence: [geometry and graph](h5-individual-frame-joint-20261023/audit.json), [reduction](h5-individual-frame-joint-20261023/reduction.json),
[hints](h5-individual-frame-joint-20261023/hints.json), [encoding](h5-individual-frame-joint-20261023/encoding.json), [model](h5-individual-frame-joint-20261023/model.json),
[solver](h5-individual-frame-joint-20261023/solver.json), [original layouts](h5-individual-frame-joint-20261023/layouts.json),
[best checked layout](h5-individual-frame-joint-20261023/best-layout.json), [original validation](h5-individual-frame-joint-20261023/best-public.json),
[distinct final layout](h5-individual-frame-joint-20261023/alternate-final-layout.json),
[fixed-layout gaps](h5-individual-frame-joint-20261023/bracket-gap-checks.json),
[one-cog coverage](h5-individual-frame-joint-20261023/one-cog-coverage-checks.json),
[seed comparison](h5-individual-frame-joint-20261023/seed-comparison.json),
[source review](h5-individual-frame-joint-20261023/source-review.json), raw evidence [part 1](h5-individual-frame-joint-20261023/raw-001.zip), [part 2](h5-individual-frame-joint-20261023/raw-002.zip), [part 3](h5-individual-frame-joint-20261023/raw-003.zip),
and [manifest](h5-individual-frame-joint-20261023/raw-manifest.json). All 110 canonical
members, 46 aliases, archive CRCs and byte hashes
verify. Complete ZIP parts remain below 50 MiB each; all original paths remain
represented through explicit verified aliases for identical input bytes.
