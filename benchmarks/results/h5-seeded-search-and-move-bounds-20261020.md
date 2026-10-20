# H5: seeded searches and exact local-move bounds — 2026-10-20

**No improved partial or complete layout is found.** The new exact result is
that none of the **331** arrangements reachable by changing zero, one or two
frame/bracket/cog poses about the saved seed can exceed **13 inserts** within
the audited retained pool. This is a local finite-pool statement, not an
unrestricted packing impossibility. H2/H5 remain open; completion stays 60%.

## Seeded searches with fixed cog arrangements

The [previous feasible hints](h5-dominated-poses-and-seeds-20261020.md) seed four
changed integer models. Each selects all 18 frames and 12 brackets together
with actual whole inserts, fixes one original 15-cog arrangement, preserves
all compatible insert choices and old frame exclusions, and maximizes inserts
up to the original cap of 21. All 58 previously audited area rows are
substituted exactly, including tautologies. Every model field and complete
hint is independently checked before solving.

Each case receives one declared 30-second call, eight workers and seed zero:

| Cog case | Variables | Measured seconds | Inserts returned | Final insert bound |
| --- | ---: | ---: | ---: | ---: |
| 0 | 4075 | 30.305709900 | 12 | 21 |
| 1 | 4096 | 30.139847700 | 12 | 21 |
| 2 | 4170 | 30.128836100 | 13 | 21 |
| 3 | 4187 | 30.115266700 | 13 | 21 |

All four calls return `FEASIBLE`, retaining only their starting counts.
The bound of 21 does not prove a 13-insert optimum. All callback and final
selections are retained; because they differ, **eight** layouts receive
original geometry checks. Six frozen CLI validations are new and two reuse
byte-verified exact prior layouts/results. Each fails only the unchanged
insert quantity. Soft cleanup overruns are recorded without extending or
repeating a search.

## Restore all cog positions

The existing fully audited **9059-pose** pool contains 1997 frame, 1875 bracket,
1240 insert and 3947 cog poses, with 2,649,582 original conflict edges.
It allows independent cog choices. The later 2260 contact additions have
conditional fixed-cog edges only; they are not silently included in this model.

One pose may replace another of the same family only if they conflict and,
excluding the compared pair, its entire original conflict neighborhood is
contained in the other's. The substitute must be a final survivor. This
preserves family quantities and completion existence within this finite pool.
Independent explicit-set checks verify **2247** replacements, leaving **6812**
poses: 1217 frames, 1593 brackets, 686 inserts and 3316 cogs. The bounded
reduction finishes in 2.255584 seconds after 9,118,943 comparisons.

Mapping the known seed changes five candidate indices. The resulting 58-part
partial passes all 1212 original same-sheet pair checks, with minimum clearance
0.201000 mm, and the frozen CLI rejects it only for eight missing inserts.
Its material charge is 4,985,103.45 mm², within the unchanged target, but it is
not a complete job or a native-margin-qualified result.

The new 6812-variable model requires exactly 18 frames, 12 brackets and 15 cogs,
allows 13–21 inserts, preserves every projected conflict and supplies the
complete feasible seed. All 18,704 constraints are reconstructed.
One declared 60-second search returns `FEASIBLE` after **60.397778600 seconds**,
with 13 inserts and final upper bound 21. Its callback and distinct final
selection pass original geometry checks and fail only insert quantity.
The callback reuses the exact newly checked seed result; the final selection
receives a fresh frozen CLI check. No packing improvement is claimed.

## Exhaustive one- and two-core-move checks

Here “core” means the seed's 18 frames, 12 brackets and 15 cogs. Inserts remain
free throughout. The census considers every retained same-family replacement
of one core pose, then every pair of replacements with matching family counts,
while leaving all other core poses fixed. It includes zero changes.

The one-move census finds **23** feasible replacements and **11** distinct
available-insert sets. The two-move extension checks all **990** removed pairs
and **89,371** candidate pairs, finding **307** exact two-move replacements.
Together there are **331** moves and **64** distinct available-insert sets.

For each set, the saved certificate partitions its candidates into original
pairwise-conflicting cliques or singleton vertices. At most one insert can be
selected from each group. Independent explicit-set enumeration reconstructs
every move and exact available-insert set, then checks all **689** cover groups.
Every cover has at most **13** groups. Thus no zero/one/two-core move can improve
the known 13-insert partial within this retained pool, even when all inserts
are reselected. The certificates do not restrict new continuous positions or
larger coordinated moves.

## A bounded larger move remains unresolved

Motivated by that proof, a changed feasibility model asks for **14–21 inserts**
while retaining 39–42 of the original 45 core poses: exactly three to six core
replacements. All original family counts and conflicts remain. The old objective
and hint are removed, because the 13-insert seed is not feasible for this target.
The entire 18,705-constraint model is reconstructed against the audited parent.

Its single declared 30-second, eight-worker, seed-zero call returns `UNKNOWN`
after **30.157355500 seconds**, with no incumbent. This is neither
a new layout nor proof that three-to-six moves cannot work. The full log and
original timeout remain. There is no retry or hidden continuation.

## Next work and repository state

Do not repeat the four fixed-cog optimizations, the free-cog search or the three-to-six-move feasibility search unchanged. The audited reduced pool cannot improve the saved 13-insert seed with at most two core moves. The larger search timed out without deciding three-to-six moves. Next diagnose the minimum frame/bracket/cog blockers of a mutually compatible 21-insert set, allowing only this temporary diagnostic to omit blocked core poses. Use the exact blocker sets to identify coordinated relocation regions and generate new original-geometry contact positions, rather than extending an expired search. Preserve every original core quantity in any subsequent completion model. Only an original 66-copy layout passing geometry, the frozen CLI, native margins and the unchanged material/cutting gates can qualify H5. H2 remains open under Artem’s original-denominator decision.

Prior local commits **6cde1bd** and **56f818a** are now confirmed on remote main.
All six hosted checks for **f6edfb7** pass, superseding its historical pending
snapshots. The **56f818a** hosted checks are still running in the saved snapshot; no later push cancels them.
Core source and the three READMEs retain their exact reviewed hashes. The
README already identifies the hosted app as a main preview and links the
qualified v0.2.0-alpha.1 release; no release-facing change is needed here.
No reserved held-out file, native quality run or new release is involved.

[Checks](h5-seeded-search-and-move-bounds-20261020/checks.json), [fixed searches](h5-seeded-search-and-move-bounds-20261020/fixed-results.json),
[free-pool audit](h5-seeded-search-and-move-bounds-20261020/free-pool-audit.json), [free search](h5-seeded-search-and-move-bounds-20261020/free-results.json),
[two-move certificate audit](h5-seeded-search-and-move-bounds-20261020/two-move-audit.json),
[larger-move result](h5-seeded-search-and-move-bounds-20261020/escape-result.json), [source/release review](h5-seeded-search-and-move-bounds-20261020/source-review.json),
[push confirmation](h5-seeded-search-and-move-bounds-20261020/push-confirmation.json),
[previous main CI](h5-seeded-search-and-move-bounds-20261020/main-ci-f6edfb7.json), [current main CI snapshot](h5-seeded-search-and-move-bounds-20261020/main-ci-56f818a.json),
[raw models, certificates, logs and layouts](h5-seeded-search-and-move-bounds-20261020/raw.zip),
and [manifest](h5-seeded-search-and-move-bounds-20261020/raw-manifest.json).
All 208 archive members, CRCs and hashes verify.
