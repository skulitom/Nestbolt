# H5: fixed cog rows and a new short-sheet exchange preflight

The conditional full 66 model passes every audit but closes **UNKNOWN** without
a candidate. Fixing only the cog rows makes presolve smaller and faster; it
does not prove feasibility or infeasibility. A subsequent allocation review
prepares six source-valid fixed 11-part variants for a different short-sheet
construction. H5 remains open and the best valid result remains 64 originals.

## Conditional construction, all 66 required

Only the fourteen first-sheet cogs are fixed, in three rigid rows. All forty
orthogonal blocks remain movable:18 frames, 5 brackets and 17 inserts. The
unchanged short sheet holds 7 brackets, 4 inserts and 1 cog.

| Row block | Cogs | X anchor, µm | Y anchor, µm |
|---|---:|---:|---:|
| 40 | 5 | 97,925 | 2,107,875 |
| 41 | 5 | 177,925 | 2,354,875 |
| 42 | 4 | 97,925 | 2,601,875 |

The model retains all 7,932 variable domains and all 35,015 previous constraints
byte for byte. It adds exactly six anchor equalities, producing 35,021
constraints. Its 622 soft hints come from the source-valid 61-part control;
no other original pose becomes a hard restriction. All 43 blocks remain
mandatory and all 903 pair relationships remain checked.

The [independent field audit](h5-fixed-cog-rows-and-short-exchange-20261028/model-audit.json) rechecks every field
of all four ancestor models, every unchanged field, the six equalities and
all hints. The 61-part control fails exactly five missing-bracket
requirements; all eight 62-part witnesses fail only four missing brackets.
Audit copies changing only those mandatory requirements pass 111,931 and
112,002 cover-pair visits respectively. All source capacities still hold.

The [fresh original-source readback](h5-fixed-cog-rows-and-short-exchange-20261028/source-bridge-audit.json) validates
the 61-part control and all eight 62-part witnesses, including their fixed cog
poses. The full negative keeps the cog rows legal and places all forty
orthogonal blocks at the same otherwise legal anchor. It has 780 original
collisions and no stock failures, preserving 90 holes and 10,026 hole vertices.
The model rejects it through 14 collision constraints and 2,750 cover-collision
visits. All six fixed-anchor equalities hold even in that negative control.
The [identity audit](h5-fixed-cog-rows-and-short-exchange-20261028/row-identity-audit.json) again rejects all three
wrong-size row substitutions and accounts for every original exactly once.

## Sole bounded call, closed

The search uses one 60-second algorithm budget within 90 shared seconds,
four workers, seed 0 and `fj` disabled. Search begins at 6.25 s with 2,485
remaining variables and 14,551 constraints after presolve, compared with
16.88 s and 7,865 variables for the previous fully movable capacity model.
These are presolved solver statistics, not changes to the audited source
model. The result is **UNKNOWN**, with no incumbent, assignment or candidate.

| Recorded quantity | Seconds |
|---|---:|
| Allocated solve time | 59.128695 |
| Returned solve time | 59.175779 |
| Solver wall time | 59.172620 |
| Algorithm time | 60.054484 |
| Shared time | 60.147361 |
| Returned solve soft overrun | 0.047085 |
| Algorithm soft overrun | 0.054484 |

The returned worker reports 55,521 branches and 29,868 conflicts, not aggregate
counters across workers. The [response audit](h5-fixed-cog-rows-and-short-exchange-20261028/response-audit.json)
rechecks all four ancestor stages, the complete conditional model, input
hashes, parameters, logs, response and timing. The call remains closed.
No source-valid 66 or native check follows, and no infeasibility is claimed.

## New short-sheet allocation preflight

The [allocation review](h5-fixed-cog-rows-and-short-exchange-20261028/allocation-review.json) rejects the proposed
6-bracket/4-insert/2-cog alternative before geometry work: the existing
ordered-projection certificate already excludes it. The different
**5-bracket/6-insert/2-cog** allocation survives the necessary frontier.
Survival is not evidence that the original shapes fit.

The preflight returns to a previously validated 12-part short sheet containing 6 brackets,
5 inserts and 1 cog. Fresh original-ring readback passes all 66 pair checks.
Six declared cases each remove a different bracket copy—3, 4, 7, 8, 10 or 11—and
retain the other eleven original poses. Each proposes adding cog copy 0 and
insert copy 0. All six fixed 11-part sets pass original geometry and stock checks.

Every target short sheet therefore contains 13 originals. Its complete
first-sheet complement is explicitly recorded as **18 frames, 7 brackets,
15 inserts and 13 cogs**, or 53 originals. The sets are disjoint, contain every
original identity once and do not inherit a fixed-first-sheet feasibility
claim. The [preflight](h5-fixed-cog-rows-and-short-exchange-20261028/exchange-preflight.json) and
[six-case summary](h5-fixed-cog-rows-and-short-exchange-20261028/exchange-cases.json) preserve these checks.

No new 13-part short layout, translation regions or construction call exists
yet. The [frozen next study](h5-fixed-cog-rows-and-short-exchange-20261028/exchange-plan.json) requires fresh
fixed-world source regions for all six cases, 36 declared finite cog phases
and both insert orientations. Audit complete source-obstacle containment,
transforms, stock limits and representative controls before a single finite
enumeration. Its preparation limit is 120 s; its later algorithm/shared limits
are 60/90 s with at most 10,000 cog poses. A valid 13-part short sheet would still need all 53
first-sheet originals placed and a complete original 66 check before native
validation. Finite-angle failure would not prove the allocation impossible.

## Publication and unchanged gates

The prior two checkpoints reached main `83f3f51f` through a normal atomic
fast-forward after all six prior CI jobs passed. The
[push receipt](h5-fixed-cog-rows-and-short-exchange-20261028/prior-push-receipt.json) records that transition.
At this snapshot, CI 40783629977 has four passing jobs and both platform
checks running. This checkpoint waits for all six before another main push;
no live run is cancelled.

Production and all three READMEs remain unchanged. Fresh GitHub reads confirm
unchanged Sparrow/Studio heads and releases, Stable v0.1.0 and Preview v0.2.0-alpha.1.
All 444 necessary allocation survivors, the best valid 64, H2's original gate
and its 22 unopened vectors remain preserved. H2/H5 stay open at **60% completed
milestone weight**. No new release qualifies.

The [raw manifest](h5-fixed-cog-rows-and-short-exchange-20261028/raw-manifest.json) binds 892 canonical files,
545 identical aliases and 5500581 compressed bytes, including full models,
controls, source geometry, the closed response, the exchange inventory,
scripts and recursive source dependencies. Independent archive verification
checks every byte, alias, hash binding, JSON and local report link.
