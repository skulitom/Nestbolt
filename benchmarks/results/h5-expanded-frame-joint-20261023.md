# H5: enlarged frame-group joint selection — 2026-10-23

**The best original partial remains 64 of 66 parts, missing two brackets.**
The enlarged model chooses among all 29 checked complete frame arrangements
while moving cogs, brackets and inserts together. The first encoding returns
`UNKNOWN` during presolve. A changed exact implication encoding returns
`UNKNOWN` under its separately declared 60-second allowance.
A faster, independently audited clique cover then returns
`UNKNOWN` under its own unchanged 60-second allowance.
Finally, an explicit no-presolve strategy change on the byte-identical audited
model reaches search and returns `FEASIBLE`.
No full original-job target witness or H5 completion is claimed;
H2/H5 remain open at **60%** completed milestone weight.

## Complete geometry and preserved baseline

The entire 35,488-entry accumulated source pool is preserved. All 29,631 eligible
small poses enter a fresh graph: 11,202 brackets, 13,272 inserts and 5,157 cogs.
This preserves all 5,302 old 26-group choices and all 21,468 latest wide-only
choices. All three small families move freely; exactly one complete 18-frame
group is selected. The original 64-part layout maps exactly to group 26.

Graph construction takes 104.398829 seconds and checks
39,215,548 expanded-bound pairs, yielding
**33,489,837 conflicts**. A separate sequential bounds scan covers
287,110,177 same-sheet possibilities and
39,215,411 exact distances, independently reconstructing
every saved adjacency row. The two distance counts differ because the builder
uses expanded rectangles while the auditor uses Euclidean bounding-box distance;
their complete conflict graphs agree exactly.

All 32,989 small poses and 141 used frame poses pass original stock/transform
checks. All 4,437 within-group frame pairs pass. Independent distances to each
whole group's polygon union recheck 765,513 distances and all 956,681 group
memberships. All 1,521 same-sheet pairs in the exact original seed pass.
All 4,576 original small-family count combinations preserve filled-area ordering
under the integer objective. Original job and target are unchanged.

## Bounded reduction, hints and selection

Fresh substitution retains 19,967 choices and removes
9,664 only with a retained adjacent same-family replacement,
original neighbor inclusion and a superset of compatible frame groups.
The bounded search performs 45,855,783 comparisons in 30.000180
seconds; limit reached: `True`. Every unprocessed choice remains.
Independent certificates check 14,745,860
original neighbors and 230,738
group memberships. The full 64-part score and exact family counts survive mapping.

The exact induced graph has 20,913,446 conflicts. Its 20-second
compression allowance produces 290 cliques and preserves
all 12,129,254 residual edges. Every edge is reconstructed from the
saved constraints. No conflict is discarded. Timers for reduction/compression
exclude additional certificate checking, graph projection, serialization and
independent reconstruction; these are development diagnostics, not a production
budget measurement.

The 30-second hint allowance completes 1,418/1,508 deterministic
group/order starts, preserving 90 pending cases. Every result
is independently checked against the graph, group membership, original caps and
score. The original 64-part baseline remains a feasible floor.

Every binary protobuf field is independently reconstructed: 19,996
variables (19,967 small poses and 29 frame groups),
12,149,516 constraints, a minimum score of 1,566,740,785 and full
inventory score 1,646,740,785. One eight-worker, seed-zero call has a
60-second allowance and records 57.045300 wall seconds, status
`UNKNOWN`, 0 callbacks and reported bound 0.0.
The full log and any limit overrun are retained. This encoding is not rerun or extended.

The sole layout checked for this encoding is the mapped starting hint; the
solver returns no layout. It passes independent geometry checks and one fresh
frozen-CLI call, retaining its two missing-bracket violations. The detailed results remain linked below; a feasible partial
is not an original-job acceptance result. Native margins remain unqualified.

## Exact encoding follow-up

The first call stops after presolve with zero callbacks, branches and searched
solutions. Its reported zero bound is **not** an infeasibility certificate and
does not replace the independently checked feasible baseline. The saved log
identifies the cost of processing over 12 million separate pair constraints.

The changed encoding groups residual conflicts by lower-index endpoint:
selecting pose `i` implies that every listed conflicting pose `j` is absent.
It retains all larger at-most-one cliques. This is an exact representation
change, with no candidate, edge, quantity, group or objective relaxation.
Independent reconstruction matches all 20,913,446 induced
edges exactly. The 12,129,254 pair rows become
19,931 enforced conjunctions, plus
290 retained larger cliques.

Every field of the changed model is independently reconstructed. Its constraint
count falls from 12,149,516 to 40,193 while
the complete hint and score floor remain identical. This new encoding makes
one eight-worker, seed-zero call with a 60-second allowance; the prior call is
not extended or overwritten. It returns `UNKNOWN` in
73.635199 wall seconds with
0 callbacks and reported bound
0.0. Its sole starting-hint layout passes geometry and one fresh frozen-CLI
check, retaining the missing-quantity failures.
Neither encoding proves unrestricted packing impossible. No unchanged solve
is repeated. This syntax-only change also stops before search; its observed
73.635199-second soft overrun is retained and it is not a demonstrated runtime
improvement.

## Fresh first-fit clique cover

A new cover starts from the full original reduced graph. It chooses the lowest
available common neighbor directly, avoiding the prior 16-candidate scoring at
every clique extension. Its fresh 20-second allowance yields
3,201 cliques and retains every one of
5,257,882 residual edges. All 20,913,446
original edges are independently reconstructed; the complete original hint
satisfies every resulting constraint. This is a changed compression algorithm,
not a continuation of the earlier capped cover.

The exact cover has 5,261,083 rows and
12,144,883 literals, versus 12,129,544 rows in the original
cover. Its larger cliques plus aggregated residual implications produce
43,034 final model constraints. Every protobuf field
and all original edges are checked again. One separately planned eight-worker,
seed-zero call has the same 60-second allowance and returns
`UNKNOWN` after 58.732893 wall seconds,
with 0 callbacks and reported bound
0.0. Its sole starting-hint layout is checked through exact reuse of the
earlier frozen-CLI result; the solver returns no layout. Full logs,
failed results and soft overruns remain preserved. No production performance
or native-margin claim follows from these finite diagnostic models.

## Explicit search-strategy intervention

Before enlarging the candidate set, a separately declared diagnostic intervention
changes **only** `cp_model_presolve` to false on the byte-identical first-fit
model. A protobuf parameter comparison independently verifies this single change;
the 60-second allowance, eight workers and seed zero stay unchanged. All original
constraints, complete hint and objectives remain identical. The previous three
presolve failures are retained, not replaced by this result.

This strategy reaches the checked baseline after 4.2047213 seconds and returns
`FEASIBLE` in 65.892903 wall seconds,
with one callback and final reported bound 1,646,740,785. All three original
layouts pass geometry checks and preserve the missing-quantity failures:
one fresh CLI call and two exact-layout reuses.
This reaches search but does not supply a full 66-copy target witness or prove
the finite model optimal. No further unchanged call or allowance extension is made.

The log starts search at 4.64 seconds and records actual branch, LP and local
search work; the aggregate response's zero branch counters are not used to
claim no search. The 65.892903-second wall time exceeds the solver's soft
60-second allowance and is retained as observed. The distinct final layout
selects six small poses absent from the prior wide-only model, but its original
filled area stays 4,401,740.784070 mm², with two brackets missing and a roughly
0.2001 mm minimum gap. This is no improvement in the required full-job result.

## Future coverage: individual frame choices

A separate coverage audit directly reconstructs all 35,488
source poses from original vertices and checks original stock/transform rules.
All 35,488 pass; there are no rejected poses. All 29,631 small choices and
141 frame choices from the group model remain. Removing the whole-group restriction exposes
2,358 additional individual frame
poses and 3,358 additional small poses.
All 86,944 original four-family count combinations preserve area ordering;
the best original partial maps and passes geometry. This audit generates no new
poses and runs no solver; the full four-family mutual graph remains pending.

All three preceding encodings returned UNKNOWN during presolve. A separately declared strategy intervention changes only cp_model_presolve to false on the byte-identical first-fit model; its exact parameter delta is independently verified and search now reaches the baseline after 4.2047213 seconds. Preserve all four outcomes and every soft overrun. Do not repeat any unchanged model/strategy, extend any solve or resume capped work. Use the verified first-fit cover and explicit residual implications, with the measured no-presolve strategy, as the starting representation for a genuinely enlarged candidate model. Retain full edge, model and parameter audits; this is not a production speed claim. Do not rerun or extend this bounded group-choice solve or resume capped comparisons. Preserve the complete graph, residual edges, mapped original 64-part floor and every returned result. The new all-pose coverage audit identifies a distinct relaxation: release the requirement to choose one of 29 complete frame sets. Allow individually chosen original frame poses, all cogs, brackets and inserts under their original caps, retaining the original best partial as the floor. Use output/h5-all-pose-coverage-20261023/mapping.json. Build a fresh complete four-family graph; the 29-group graph omits small poses that were incompatible with those specific frame sets and does not contain frame/frame or frame/small edges. Audit every edge and use fresh same-family substitutions only with original neighbor inclusion. Preserve every residual constraint, declare fresh finite limits and independently reconstruct the entire model. This is an enlarged pose-selection problem, not an unchanged solver retry. No new geometry or unrestricted packing proof is claimed by the coverage audit. A complete original 66-copy target witness must precede native-margin qualification, a repair within the original production budget and the full H5 matrix. H2 retains Artem's unchanged gate; keep all 22 reserved vectors unopened.

## Repository and evidence

Main 7cd00432 now passes all six hosted jobs. The previous reviewed checkpoint
955cc87e was pushed normally to main; its run 39969515541 is captured as
`in_progress` / `pending`. Only observed passes
are claimed. Production source, original library/request/target and all three
READMEs remain unchanged. The published preview remains v0.2.0-alpha.1 and stable
Latest v0.1.0. These diagnostic changes do not qualify a new application release.
No registry publication, reserved-input evaluation, native packing or full H5
quality run occurs.

Evidence: [graph audit](h5-expanded-frame-joint-20261023/audit.json), [reduction](h5-expanded-frame-joint-20261023/reduction.json),
[hints](h5-expanded-frame-joint-20261023/hints.json), [model](h5-expanded-frame-joint-20261023/model.json),
[solve](h5-expanded-frame-joint-20261023/solver.json), [original layouts](h5-expanded-frame-joint-20261023/layouts.json),
[compact encoding](h5-expanded-frame-joint-20261023/compact-encoding.json),
[compact model](h5-expanded-frame-joint-20261023/compact-model.json), [compact solve](h5-expanded-frame-joint-20261023/compact-solver.json),
[compact layouts](h5-expanded-frame-joint-20261023/compact-layouts.json),
[first-fit cover](h5-expanded-frame-joint-20261023/first-fit-cover.json),
[first-fit model](h5-expanded-frame-joint-20261023/first-fit-model.json), [first-fit solve](h5-expanded-frame-joint-20261023/first-fit-solver.json),
[first-fit layouts](h5-expanded-frame-joint-20261023/first-fit-layouts.json),
[strategy parameter audit](h5-expanded-frame-joint-20261023/direct-parameters.json),
[direct search](h5-expanded-frame-joint-20261023/direct-solver.json), [direct layouts](h5-expanded-frame-joint-20261023/direct-layouts.json),
[alternate final layout](h5-expanded-frame-joint-20261023/alternate-layout.json),
[its original validation](h5-expanded-frame-joint-20261023/alternate-public.json),
[individual-pose coverage](h5-expanded-frame-joint-20261023/all-pose-audit.json),
[source review](h5-expanded-frame-joint-20261023/source-review.json), raw evidence [part 1](h5-expanded-frame-joint-20261023/raw-001.zip), [part 2](h5-expanded-frame-joint-20261023/raw-002.zip), [part 3](h5-expanded-frame-joint-20261023/raw-003.zip), [part 4](h5-expanded-frame-joint-20261023/raw-004.zip),
and [manifest](h5-expanded-frame-joint-20261023/raw-manifest.json). All 114 canonical members,
81 aliases, archive CRCs and byte hashes verify. The complete ZIP
parts stay below 50 MiB each; identical input bytes are stored once with explicit,
verified aliases. Every original source path remains represented.
