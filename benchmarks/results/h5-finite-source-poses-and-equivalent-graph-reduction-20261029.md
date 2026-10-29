# H5 finite source poses and equivalent graph reduction — 2026-10-29

Three distinct, bounded models were independently audited and each called once.
The 1,525-pose centroid model returned `INFEASIBLE`; the expanded 4,575-pose
boundary model returned `UNKNOWN`; an exactly equivalent 1,817-pose reduction
of that expanded model returned `INFEASIBLE`. No call returned an assignment.
These are solver results for finite sampled positions. There is no independent
unsatisfiability certificate and no claim that continuous placements are impossible.

H5 remains open. The 29 remaining continuous cog-site choices, the 440 overall
allocation candidates, the original-source-valid 11-part short sheet and the
existing valid 64-part layout are preserved. No new 66-part layout, native check,
production change or release is claimed. Milestone completion remains **60%**.

## Source poses and geometry checks

The preceding [component halfspace checkpoint](h5-local-grid-construction-and-component-halfspaces-20261029.md)
left 29 choices of two empty sites among the 15 source cog sites. The new models
retain those choices and all 12 legal bracket/insert source modes. They select
seven brackets and six inserts around the fixed 29 parts and 13 selected cog
sites, to accompany the already validated 11 parts on the short sheet.

The centroid pool uses the exact arithmetic mean of each compatible unary hull's
vertices. The expanded pool retains those 1,525 poses and adds two per hull: each
endpoint of an exact farthest-vertex pair, inset 1/1,000 of the way toward the
mean. These are source transforms, not resized or substituted shapes. Each pose
requires its recorded obstructing cog sites to be empty.

Independent geometry readbacks checked every pose against stock, fixed original
sources, all cog sites not marked empty, and its exact rational unary hull. They
then reconstructed every pair distance and the complete conflict graph. A pair
closer than 0.225 mm conflicts. All 12 source modes remain represented, including
their separately retained aliases.

| Pool | Bracket / insert poses | All pairs checked | Conflicts | Clique rows | Preparation |
| --- | ---: | ---: | ---: | ---: | ---: |
| Centroid | 707 / 818 | 1,162,050 | 196,382 | 5,281 | 1.430545 s |
| Boundary | 2,121 / 2,454 | 10,463,025 | 1,695,837 | 17,551 | 12.512783 s |

The independent readbacks took 3.222969 s and 14.674313 s respectively. The
expanded pool's nearest pair-distance margin from the conflict threshold was
0.00015902866649639136 mm, above the audit's 1e-8 mm tolerance. Its minimum
fixed-source gap was 0.22558409931070858 mm, nonempty-cog gap
0.22602295261299332 mm and extra stock clearance 0.025083706124860328 mm.
See [expanded source audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/boundary-source-audit.json).

## Equivalent reductions

A pose B is removable only if an active pose A of the same family can replace it:
A conflicts with B, requires a subset of B's empty sites, and has no additional
active conflict neighbour outside A and B. Therefore a selection containing B
cannot already contain A, and exchanging them preserves counts and compatibility.
Every sequential removal was checked against the graph at that step, including
chains of later replacements.

The [dominance audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/dominance-audit.json) verified 2,758 removals:
1,910 identical closed-neighbourhood cases and 848 other dominated poses.
The induced graph retains 1,817 poses (1,169 brackets, 648 inserts) and 347,454
conflicts. Reduction took 2.792508 s; independent audit took 2.848786 s.

Projecting the original cover gives 12,425 clique rows. Removing 2,735 rows
contained in retained rows leaves 9,690 with exactly the same complete edge
coverage. Every containment and the full cover were independently checked;
preparation took 0.239646 s and audit 0.164944 s. See
[clique-cover audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/clique-cover-audit.json).

A separate spatial-index preparation regenerated the expanded source poses,
graph and clique cover byte for byte. It explicitly classified the 1,695,837
indexed possible pairs and matched the graph independently checked over all
10,463,025 pairs. This measured preparation took 11.207008 s, compared with
12.512783 s for the all-pairs preparation. This is one measured construction,
not a repeated performance benchmark. See [equivalence audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/indexed-equivalence-audit.json).
The reduced model charges this preparation plus both exact reductions.

## Three closed calls and full timing charges

Each model has Boolean pose selectors and 15 empty-site flags, exact family
counts, exactly two empty sites, all 76 forbidden empty-site pairs, pose-to-site
implications and its complete conflict cover. No objective or hint is supplied.
The independent model readers checked every variable, domain, constraint and
serialized field, including binary/text equivalence.

Each sole call used four workers, seed zero and the recorded parameters, with
a four-second source-validation reserve. The charged preparation includes the
saved short-sheet shared time of 22.247810100321658 s and every required
construction stage. The two earlier solver calls are closed and were not resumed
or added to a later call's construction time.

| Model | Variables / constraints | Charged preparation | Allocated solve | Returned solve | Algorithm total | Shared total | Status |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | --- |
| Centroid | 1,540 / 7,640 | 34.268056 s | 21.099456 s | 2.183379 s | 37.089446 s | 37.144401 s | INFEASIBLE |
| Boundary | 4,590 / 24,470 | 45.614540 s | 9.653905 s | 9.713971 s | 56.072415 s | 56.173969 s | UNKNOWN |
| Equivalent reduction | 1,832 / 12,564 | 47.123316 s | 8.218115 s | 4.891285 s | 52.683950 s | 52.746141 s | INFEASIBLE |

The boundary call exceeded its internal solve slice by
**0.06006570067256689 s**; that result is preserved. All three algorithm totals
are below 60 seconds and all shared totals below 90 seconds. None was restarted,
extended or reseeded. All recorded assignments, incumbents, source-checker calls
and native calls are zero.

The response readers checked raw response protobufs, complete logs, parameters,
model hashes, timing charges and process closure. The reduced response reports
168,776 branches and 34,252 conflicts. Its raw LP diagnostics report zero overflow
for both workers; the other recorded LP statistics are retained without treating
them as geometry validation. See the [centroid response audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/centroid-response-audit.json),
[boundary response audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/boundary-response-audit.json) and
[reduced response audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/dominance-response-audit.json).
Auditing a solver's `INFEASIBLE` response is not an independent proof of
unsatisfiability, and finite sampling does not exclude the continuous construction.

## Diagonal capacity diagnostic

Before constructing the pools, a 2.946988-second diagnostic examined 19,102
halfspaces over six primitive diagonal directions and both sides, using the 29
remaining choices. It found no stronger component certificate or new exclusion.
The reader verified unchanged inherited capacities, scan shape and 1,522 exact
polygon-clipping oracle cases for the analytic rectangle-area function. It did
**not** independently recompute all 19,102 material bounds. This diagnostic is
not evidence that stronger diagonal bounds do not exist. See
[diagnostic audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/diagonal-diagnostic-audit.json).

## Preservation and next investigation

The next preparation investigates joint bracket/insert capacities over conservative
components of continuous possible occupied material. It will attribute all unary
hulls and source modes, retain unproved choices and independently verify any new
necessary exclusion. This is recorded in [next-step.json](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/next-step.json);
no new search is opened by that note. A full 66-part original-source success must
precede native/material validation, integration and the complete H5 matrix.

The prior checkpoint was normally fast-forwarded to main and the work branch as
`286223aee0bead996d02a5c1ef4d8b4b403b904b` after all six previous checks passed.
Its [push receipt](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/prior-main-push-receipt.json) is preserved. At this
checkpoint's publication snapshot, its browser, benchmark smoke and both maker
jobs passed; the Windows and Ubuntu checks were still running. A further push
requires all six to pass and fresh remote-head/live-run checks.

Production source and all three READMEs are unchanged. Sparrow and Studio heads
and releases are unchanged. Stable Latest remains v0.1.0 and preview remains
v0.2.0-alpha.1. H2 retains the original gate and stays open; no reserved H2 vectors
were evaluated. No new release qualifies from these research-only results.

The [manifest](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/raw-manifest.json) preserves 4875 canonical files and
992 byte-identical aliases in 62175991 bytes of multipart ZIP evidence,
including original geometry, all models and calls, recursive source bindings,
independent readers and publication snapshots. The [archive audit](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/archive-checks.json)
checks every stored byte, alias, binding and local report link.
The initial archive reader stopped because this report links to its not-yet-written
output. The second reader stopped at an incorrect repository-root depth after
being copied into the evidence folder. The separate
[v3 reader](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/archive-verifier-v3.py)
uses the correct root and defers only that own-output link until writing, then
checks every link. The
[correction record](h5-finite-source-poses-and-equivalent-graph-reduction-20261029/archive-verification-correction.json)
preserves both failures; no geometry or solver result was changed or repeated.
