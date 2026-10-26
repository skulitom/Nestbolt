# H5: exact completion obstruction and single-cog release census — 2026-10-26

**The verified six-cog arrangement cannot accommodate either missing bracket
within the original inward placement domains.** Exact continuous-domain proofs
replace the earlier finite-pose observation. Releasing one cog position opens
bracket regions in four cases; a complete two-bracket capacity proof rules out
one more of those cases. Original cogs **57, 64 and 65** remain the useful
single-position releases to investigate. No complete layout is claimed.
H2/H5 remain open at **60%** completed milestone weight.

## Full continuous-domain check with all six cogs fixed

Keep the independently verified six original cog anchors and the other 57
original placements unchanged. Both original brackets 28/29 and insert 50
remain required. The identical brackets have **16 original mode/sheet queries
and 2,418 inward domains**; the insert has **2 queries and 338 domains**.

For each cog on the same sheet, translate every full guarded source collision
clause into a condition on the missing part's real anchor. With moving anchor
`(x,y)` and fixed cog `(cx,cy)`, the original outside inequality becomes:

`a*x + b*y <= a*cx + b*cy - outside_bound`.

Exact integer bounds first identify complete domain boxes inside a failed
clause and clauses true throughout a box. Otherwise clip the entire real inward
domain using rational arithmetic. Apply each outside-clause union by retaining
all closed halfplane pieces and carrying closed complements between splits.
This retains boundary lines and isolated points as well as areas. No grid
sample, floating polygon simplification, inset or new safety padding is added.

All **2,756 domains** finish in **3.751736s**, with no pending case
or cap: **2,304** complete box exclusions, **451** further continuous exclusions,
and **one insert domain** remaining as **89** convex fragments. The insert
residual is original query 16, domain row/index 13. All **2,418 bracket domains
are empty**, so these exact 63 placed originals cannot be completed to all 66.

Independent audit takes **5.514913s**. It checks committed source
provenance, rechecks all six witness domains and **427** original cog-pair
clauses, enumerates **5,816,904 exact integer corner values**, and replays all
**1,136 changed-clause events** with a separate candidate-vertex/convex-hull
clipper. Every initial domain, residual, line/point boundary and complete query
inventory agrees. Every retained insert fragment satisfies every source clause.

The first audit stopped at an archive lookup: two historical witness audit
summaries live in their original guarded-cell archive. A separate repaired
readback resolves exactly those hashes there; the failed source, plan and
traceback are retained. Three additional witness query/mutual files read during
the witness recheck are separately matched to committed hashes and archived.
No geometry computation or solver is repeated by this provenance repair.

This proves only a **conditional obstruction** with the exact six poses,
recorded source orientations/inward domains and fixed 57. It does not prove
unrestricted packing impossible and must not become a domain exclusion in a
model where these cogs can move.

## Six distinct single-position releases

Release each cog position in turn while keeping the other five and the 57
original source placements fixed. The released cog remains a required part;
this diagnostic only measures bracket regions before placing that cog and the
insert. It does not remove a part from the intended 66-original layout.

Each case covers all **2,418 bracket domains**. All six complete in a shared
**13.630690s**, below the declared 180-second preparation budget and each
60-second case cap. No solver is used. Independent exact replay verifies all
**14,508 domain cases**, including their original source clauses and boundaries.

| Released original cog | Source sheet | Residual domains | Convex fragments | Line/point fragments |
|---|---:|---:|---:|---:|
| 54 | 1 | 0 | 0 | 0 |
| 57 | 1 | 5 | 171 | 18 |
| 58 | 1 | 14 | 14 | 0 |
| 62 | 1 | 0 | 0 | 0 |
| 64 | 2 | 14 | 83 | 0 |
| 65 | 2 | 30 | 364 | 1 |

Cog 57 opens query 2 and 10 regions on the first sheet; cog 58 opens only query
8 on that sheet. Cog 64 opens query 3 and 15 regions on the second sheet.
Cog 65 opens queries 3, 7, 9, 11 and 15 there. These are complete real regions,
not distinct integer placements or a proof that two brackets fit together.

The initial aggregate reader stopped after successfully auditing the first
case because a counter omitted its zero-valued residual key. The verified
per-case summary explicitly records zero. A separate aggregate recovery reads
that value, reuses the completed first audit without repeating it, and audits
only the five unfinished cases. All original process logs and the recovery
record are preserved; no geometric proof or search is restarted.

## Releasing cog 58 cannot fit both brackets

The cog-58 release leaves **14 query-8 convex regions**, all with the same
original bracket orientation. Enumerate every **196 ordered pair**, including
two brackets choosing the same region. For each pair form the exact rational
convex difference hull `B-A` from all vertex differences, then apply every
original full guarded bracket/bracket separation clause to that whole hull.

All **196** allowable difference regions are empty. Preparation takes
**1.342161s**. Independent gift-wrapped hull
reconstruction and the separate clipping oracle verify all **392** changed
clause events in **1.676416s**, preserving closed boundaries.
Thus **at most one original bracket** fits with the other five cog poses fixed,
even before replacing cog 58 or the insert. Moving only cog 58 cannot complete
the required two brackets and all 66 originals. This remains conditional on
the recorded source domains and fixed poses.

## Next focused construction and repository state

Investigate original cogs **57, 64 or 65** (moving-part indices 4, 7, 8).
Prepare complete source-domain regions for the insert and released cog against
the five retained cog poses, alongside the audited bracket regions. Preserve
every boundary and handle the signed source displacement correctly when the
released cog occurs before or after a fixed cog in the original pair order.

Each resulting focused model must contain **four mandatory movers**: brackets
28/29, insert 50 and the released original cog, with **62 fixed originals**.
Keep all 66 counts, original shapes, areas, source-domain and mutual pair rules,
native guards and material target. The old six-cog copy-index symmetry order
must not constrain individually fixed poses. A region alone is not a complete
layout. Audit all model changes before a newly declared bounded search.

Offline geometric preparation remains diagnostic; it is not a production-budget
pass. A complete original-geometry/native-valid target, production integration
and the full 13-job/two-kerf H5 matrix are still required. No solver, native
validation or quality run occurs in this checkpoint. H2 keeps its original gate
and all 22 reserved vectors untouched.

All six jobs in prior main CI 40246226212 passed. The three previous local
checkpoints were **normally pushed to main**, advancing 728b2db2 to
**822a5f67**, and the exact remote ref was verified. The saved receipt includes
the fetch, ancestry, clean tracked state, unchanged production/README checks,
normal push and remote readback. Main's new
[CI 40248595273](https://github.com/skulitom/Nestbolt/actions/runs/40248595273) is **in_progress**, with **2/6** successful
jobs at this snapshot. This new checkpoint waits for that run before the next
normal push. No existing CI was cancelled.

Production source, all three accurate READMEs, preview v0.2.0-alpha.1 and stable
Latest v0.1.0 remain unchanged. No new release is qualified.

Evidence: [continuous proof audit](h5-fixed-six-completion-20261026/fixed-six-audit.json),
[release census](h5-fixed-six-completion-20261026/release-census-audit.json),
[complete comparison](h5-fixed-six-completion-20261026/release-comparison.json),
[two-bracket capacity certificate](h5-fixed-six-completion-20261026/bracket-capacity-certificate.json),
[verified main push](h5-fixed-six-completion-20261026/main-push-receipt.json),
[raw archive](h5-fixed-six-completion-20261026/raw-001.zip) and [manifest](h5-fixed-six-completion-20261026/raw-manifest.json).
**7620 canonical files / 27621
exact-content aliases** retain every original source, proof domain, rational
fragment, changed-clause event, failure, recovery and audit with size, SHA-256
and CRC verification.
