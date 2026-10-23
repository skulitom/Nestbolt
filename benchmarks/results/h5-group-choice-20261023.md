# H5: joint frame-group and small-part selection — 2026-10-23

**A new 62-part partial places more filled area within the original material allowance,
but still lacks two cogs and two inserts.** All 18 frames and 12 brackets are present.
H2/H5 remain open and completed milestone weight stays 60%. No product code changes
or new release are qualified by this experiment.

## Repository and release refresh

Incoming main `e9046d53` adds the comparison index and metadata. Merge `44ff9cc4`
preserves all six incoming files and all 30 local evidence/doc files from the two
previous unpushed checkpoints, byte for byte. Both raw archives (466 and 362
members) pass SHA and CRC checks again. The merge is pushed to main. The previous
7c47f498 checks, incoming e9046d53 checks and its Pages deployment all pass.
Checks on merge 44ff9cc4 are still running in the saved snapshot; a complete pass is not inferred.

Core source and all three READMEs retain their reviewed hashes. The existing
README accurately identifies the v0.2.0-alpha.1 preview, stable v0.1.0, hosted
preview from main, 60% milestone completion and incomplete import/material gates.
No README revision or another application release is justified by these offline
diagnostics. Artem’s release authorization remains recorded; no registry is published.

The [current Studio README](https://github.com/JeroenGar/sparrow-studio/blob/c0bb9e8671defc5c25a02feb91789601a08f2e75/README.md)
identifies its new app as unpublished. The [published app description](https://sparrowstudio.app/)
still states strip packing without multiple fixed sheets or part-in-hole.
The October 21 upstream commit changes its API specification; these sources do
not trigger the plan’s shipped-feature stop rule. Read-only source snapshots are
preserved. H2 retains Artem’s original-denominator decision; no reserved input is evaluated.

## Changed construction

The earlier [whole-group tests](h5-whole-group-diagnosis-20261020.md) fixed both
frames and cogs. This model jointly chooses one of all 26 audited complete
18-frame groups and all three small-part families. It starts from the whole
11,319-pose source pool, including 900 later bracket and 900 later insert contacts,
with every original cog choice restored. It creates no new coordinates.

Filtering only for compatibility with at least one frame group retains 5,302
small poses: 1,579 bracket, 1,393 insert and 2,330 cog. The graph is recomputed from
original filled outlines, without reusing conflicts conditional on fixed cogs.
Generation completes in 28.395672900 seconds; all 1,173,136 edges fit into
8,779 checked cliques before the 30-second compression limit, with no residual edges.

An independent full-pair audit checks 743,589 frame/small pairs, 3,978 within-group
frame pairs and 8,715,150 small-pair possibilities. Bounding-box lower bounds
avoid unnecessary exact distances; all 1,375,283 remaining distances and complete
clique edge coverage agree. Every retained transform, stock bound and quantity
in the complete 58-part starting hint passes. All 4,576 possible small-family count
combinations have the same ordering under original filled areas and the model’s
integer area weights. The complete protobuf model, including group implications,
family caps, objective, area floor and full hint, is independently reconstructed.

## One bounded search and all returned layouts

One 60-second call, eight offline workers and seed 0 ends `FEASIBLE` after
60.121854000 seconds. Three callbacks and a different final placement
all use frame group 2. The reported upper bound still permits the full inventory;
this is neither an optimum nor a finite-pool infeasibility certificate. The
expired search is not extended or restarted.

Every layout below has 18 original frames. Areas are mm².

| Return | Brackets | Cogs | Inserts | Filled area | Charged material |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 12 | 15 | 13 | 4,323,340.784070 | 4,985,103.450000 |
| 1 | 12 | 14 | 16 | 4,332,678.065132 | 4,988,890.203495 |
| 2 | 12 | 13 | 19 | 4,342,015.346194 | 4,988,890.353495 |
| final | 12 | 13 | 19 | 4,342,015.346194 | 4,988,890.353495 |

The best partial has 4,342,015.346194 mm² of filled area, 18,674.562124 more than
its 58-part seed and 10,462.718938 more than the earlier 63-part partial recorded in
[the prior comparison](h5-coordinated-contact-selection-20261020.md). It places
62 rather than 63 copies and uses 3,786.903495 mm² more charged material than its
58-part seed, reaching the original 4,988,890.353495 mm² allowance exactly. This is
progress in filled area within the allowance, not complete-job material evidence.

All four returns pass independent original geometry, clearance, rotations and
stock checks. All four fresh calls to the hash-pinned original CLI fail **only**
their missing-copy quantities; the final two lack two cogs and two inserts each.
Minimum clearance for those two is 0.201 mm, and their target material has no
remaining headroom. Native construction margins are not qualified. No search
engine integration, native packing, quality rerun or held-out evaluation occurs.

## Preserved packaging correction

The first evidence sealer wrote a valid ZIP but looked up one archive member
using Windows backslashes; ZIP normalized its name to forward slashes. That
verification stopped with a missing-member KeyError. The failed helper, its raw
archive and partial output files are preserved together. The repaired sealer
uses normalized archive paths and verifies every member hash and CRC. No model,
search, geometry audit or CLI call is repeated for this packaging correction.

## Next investigation

Do not retry the expired group-choice model unchanged. Inspect the saved 62-part geometry and its free regions to identify the obstruction for the two missing cogs and two missing inserts, then construct changed contacts with coordinated small-part moves. Before fixing additional parts, check that the resulting conditional free space has enough capacity. Declare finite generation and solver limits, retain the 62-part seed and every result, and independently recompute all changed conflicts. Native construction margins and an original 66-copy witness are still required before a quality pilot; retain all original H5 savings/material and full-scope requirements. H2 stays open under Artem’s decision.

Evidence: [reconciliation](h5-group-choice-20261023/reconciliation.json), [graph audit](h5-group-choice-20261023/graph-audit.json),
[model audit](h5-group-choice-20261023/model-audit.json), [solver result](h5-group-choice-20261023/solver-result.json),
[all-layout audit](h5-group-choice-20261023/layout-audit.json), [source review](h5-group-choice-20261023/source-review.json),
[raw inputs, graphs, models, outputs and upstream snapshots](h5-group-choice-20261023/raw.zip),
and [verified manifest](h5-group-choice-20261023/raw-manifest.json). All 83 archive members,
CRCs and byte hashes verify.
