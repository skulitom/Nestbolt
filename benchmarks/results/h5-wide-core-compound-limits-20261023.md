# H5: compound limits around the improved core — 2026-10-23

**Both finite compound models retain the best 64-part score, missing two
brackets.** Neither improves the original 64-part layout. The candidate-model
optima are now known; unrestricted packing remains unresolved. H2/H5 remain
open at **60%**.

## Actual compound contacts and reflected geometry

The first model fixes only the checked 18 wide frames and 15 cogs from the new
64-part partial. It preserves the entire prior pool and its 31-part small seed,
then generates actual-outline contacts for all 36 saved compounds at four
quarter-turns plus single-part classes on both sheets. It does not substitute
a filled compound bounding rectangle for member outlines.

A separate reflection census checks 144 source-pattern/rotation cases. All 456
members match direct affine reflection under allowed transforms, including
rectangular inserts represented without a forbidden mirror flag. All 540 member
pairs pass. Maximum reconstruction error is 8.039×10⁻¹⁴ mm and maximum area
difference is 3.527×10⁻¹¹ mm². Family-preserving member matching identifies 24
cases equivalent to previous rotations and six equivalent to earlier reflections.
All equivalence certificates are rechecked, yielding **114 new compound
geometries**. The 1e-8 mm / 1e-6 mm² diagnostic deduplication tolerances are stated;
this is not an exhaustive continuous proof.

The second construction queries only those 114 reflected geometries on both
sheets. The previous single-part and unreflected queries are not repeated, and
no capped member list is resumed. Each model preserves the exact original
64-part baseline and original family caps.

| Checked result | Quarter-turn compounds | New reflected compounds |
| --- | ---: | ---: |
| Queries completed | 308/308 | 228/228 |
| Added brackets / inserts | 1,514 / 1,600 | 936 / 1,600 |
| Retained small choices | 6,594 | 9,130 |
| Complete conflict edges | 4,294,175 | 8,783,223 |
| Capped member lists preserved | 126 | 64 |
| Choices after certified substitution | 2,286 | 3,164 |
| Starting layouts checked | 80/80 | 80/80 |
| Single solve wall seconds | 6.466548700 | 10.080987600 |
| Proven finite optimum | 815,800,000 | 815,800,000 |
| Full inventory would require | 895,800,000 | 895,800,000 |

Both complete source prefixes, fixed and seed mappings, original stock bounds,
allowed transforms, member geometry, all query regions and every event are
independently checked. The first audit covers 12,746,553 same-sheet possibilities
and 4,859,252 exact distances; the second covers 23,960,484 possibilities and
9,945,558 exact distances. Every region reconstructs with zero area difference;
cache translation errors remain below 9.166×10⁻¹³ mm.

The first complete graph compresses without residuals. The second retains all
1,336,544 residual edges after its 20-second compression allowance. Both full
graphs are reconstructed independently. Fresh same-family substitutions verify
4,588,685 and 9,419,574 original neighbor relationships, preserve the entire
64-part score, and exactly preserve both induced graphs. No prior reduction is
reused; no original conflict is dropped.

Each model's every protobuf field is independently reconstructed. Each makes
exactly one eight-worker, seed-zero call with a 60-second allowance and finishes
early with `OPTIMAL`. Neither is repeated or extended. All six original layout
audits pass geometry and retain only the two missing-bracket violations: five
fresh frozen-CLI calls and one exact-layout reuse. Filled area remains
4,401,740.784070 mm² at charged material 4,988,890.203495 mm². The roughly
0.2001 mm minimum gap remains unqualified for native margins.

The saved generation timers cover query/proposal generation; complete graph
construction, serialization and independent audits are additional work. These
diagnostics are not production-budget or H5 quality results.

## Expanded frame-choice coverage

A new coverage audit preserves the full **35,488-entry** pool and the exact old
11,319-entry source prefix. It retains all 26 previous complete frame sets and
adds the exact wide, tall and mixed sets at indices 26–28. All **29 groups**
contain 18 original frames; their 141 distinct frame poses and all 32,989 small
poses receive stock/transform checks. Unused frame poses in the raw pool are
preserved, not included in this group-choice claim.

All 4,437 within-group frame pairs pass. Of 3,721,977 small/frame possibilities,
136,488 exact distances determine blockers. An independent comparison to each
whole group's polygon union checks 765,513 distances and all 956,681 membership
decisions. The resulting **29,631 compatible small choices** comprise 11,202
brackets, 13,272 inserts and 5,157 cogs. All 5,302 earlier group-model choices and
all 21,468 latest wide-model choices remain. The original 64-part seed maps to
group 26 and passes geometry and compatibility again. No new contact or solver
is run in this coverage audit; the complete mutual graph remains pending.

Do not rerun or extend either completed fixed-core solve or resume their 126 and 64 capped member lists. Both finite models have a proven optimum at the preserved 64-part score, leaving two brackets missing; they do not prove unrestricted impossibility. Preserve output/h5-latest-wide-joint-20261023/layout-audit/layout-final.json as the best original partial and retain every alternate original layout. The next concrete model is output/h5-expanded-frame-group-coverage-20261023/mapping.json over the complete 35,488-pose source pool. It lets all three non-frame families move together while choosing exactly one of 29 whole 18-frame arrangements: all 26 earlier groups plus the exact wide, tall and mixed constructions at indices 26, 27 and 28. All 29,631 eligible choices, every group compatibility and the 64-part seed at group 26 are checked. Compared with the earlier 26-group model it has 24,329 additional choices; compared with the latest wide-only joint model it has 8,163 additions, while preserving all earlier choices. Declare fresh graph, reduction, compression, hint and single-solve limits. Rebuild the complete mutual graph from original geometry; do not reuse wide-only filtered adjacency or reductions. Any same-family substitution must preserve neighbor inclusion and every compatible frame group, and the mapped 64-part score floor. Preserve every residual edge and pending comparison, independently reconstruct all model fields, and validate every returned original layout. A complete 66-copy target witness must precede native-margin qualification and any production repair within the original limits/budget. Full H5 jobs and both kerfs remain required. H2 retains Artem's unchanged gate; the 22 reserved vectors stay unopened.

## Repository and evidence

Main is at pushed 7cd00432 with no incoming changes at this turn's fetch. Its
run 39964600029 is saved as `in_progress` / `pending`;
no unobserved pass is inferred. This checkpoint will follow the normal policy
of allowing the current checks to finish successfully before another push.
Original job, library, request and target hashes match the preceding archive.
Production source and all three READMEs remain unchanged. Current preview
wording stays accurate; neither a new application release nor gate completion
is claimed. No native packing, full quality matrix, registry publication or
reserved-input evaluation occurs.

Evidence: [rotation graph](h5-wide-core-compound-limits-20261023/rotated-graph-audit.json),
[rotation solve](h5-wide-core-compound-limits-20261023/rotated-solver-result.json), [rotation layouts](h5-wide-core-compound-limits-20261023/rotated-layout-audit.json),
[reflection census](h5-wide-core-compound-limits-20261023/reflection-audit.json), [reflected graph](h5-wide-core-compound-limits-20261023/reflected-graph-audit.json),
[reflected solve](h5-wide-core-compound-limits-20261023/reflected-solver-result.json), [reflected layouts](h5-wide-core-compound-limits-20261023/reflected-layout-audit.json),
[expanded coverage](h5-wide-core-compound-limits-20261023/coverage-audit.json), [frame sets](h5-wide-core-compound-limits-20261023/frame-groups.json),
[source review](h5-wide-core-compound-limits-20261023/source-review.json), [raw evidence](h5-wide-core-compound-limits-20261023/raw.zip),
and [manifest](h5-wide-core-compound-limits-20261023/raw-manifest.json). All 773 archive members, CRCs,
byte hashes and 29 input aliases verify. Identical physical input
files are stored once with explicit aliases; all raw evidence remains available.
