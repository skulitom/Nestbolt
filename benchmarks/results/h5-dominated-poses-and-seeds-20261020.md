# H5: certified pose reduction and feasible starting layouts — 2026-10-20

**No improved partial or complete layout is found.** The useful result is a
certified reduction of 26–30% of frame/bracket choices, plus concrete feasible
starting layouts for all four reduced models. These now allow a changed search
to optimize actual insert count from a known layout. H2/H5 remain open at 60%.

## Joint frames and brackets

The [bracket-capacity diagnosis](h5-frame-bracket-diagnosis-20261020.md) requires
selecting frames and brackets together. Four models therefore fix one complete
cog arrangement, require all 18 frames and 12 brackets simultaneously, retain
every projected original conflict, and exclude the 26 reviewed exact frame
sets. A blocked-insert-pose score ranks these choices but has no physical fit
guarantee. All models and costs are independently reconstructed.

Each case declares one **30-second limit**, eight workers and seed zero.
All four return `UNKNOWN` with no incumbent. The saved logs retain thousands of
search branches and many interchangeable positions; no failure is erased.

## Certified substitutions

For each fixed cog case, a same-family pose A may replace B only when:

1. A and B conflict, so a feasible selection of B cannot already contain A.
2. Apart from the compared pair, every eligible neighbor of A is already a
   neighbor of B, including **all eligible insert positions**.
3. A belongs to no additional excluded-frame-set constraint.
4. A is a final survivor, so no replacement chain is required.

Replacing B preserves family quantity and introduces no new conflict or
forbidden frame set. Its blocked-insert cost cannot increase. This preserves
completion existence within the original finite pose pool; it does not alter
geometry or assert anything about unrestricted continuous arrangements.

The reduction declares a 60-second total bound and ten million comparisons per
case, retaining unprocessed positions if either limit is reached. All four cases
finish without reaching either limit. Independent explicit-set checks verify
**4105 substitutions** against the original cliques and exclusions.
Original source candidates remain intact.

The follow-up rule is declared before reduction: only cases removing at least
25% of joint variables receive one reduced-model solve. All four qualify. Each
reduced model is reconstructed against its parent with removed variables fixed
to zero, retaining exact quantities and objective and dropping only false
literals and tautological constraints.

| Cog case | Original joint variables | Retained | Removed | Original solve seconds | Reduced solve seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 3584 | 2656 | 25.89% | 30.081012 | 30.106336 |
| 1 | 3625 | 2664 | 26.51% | 30.136473 | 30.070240 |
| 2 | 3703 | 2616 | 29.35% | 30.311369 | 30.072286 |
| 3 | 3753 | 2624 | 30.08% | 30.172644 | 30.060866 |

All four reduced calls also return `UNKNOWN` without an incumbent at their
declared 30-second limits. The smaller models do **not** demonstrate a measured
search-speed improvement. All eight failures and soft cleanup overruns remain.
No expired process or suffix is restarted.

## Direct substitution succeeds where unseeded search did not

Applying the audited substitutions once to the six previously validated
whole-group partial layouts yields six partials using three distinct new exact
frame sets outside the old exclusions, while retaining all existing inserts and cogs. The changes include
equivalent rectangular orientations, tiny translations and, in two cases,
frame movements of about **86.3248 mm**. Original filled-outline Hausdorff
distances are saved so coordinate changes are not confused with shape movement.

All six substituted partials pass original geometry, rotation, margins, clearance
and target-material checks. The frozen CLI rejects them only for their original
insert shortfall. They are construction starting points, not full jobs.

Six separately declared insert-only models fix the 18 frames, 12 brackets and
15 cogs, retain every surviving original insert pose and conflict, and maximize
the insert count up to 21. Every model is reconstructed before its single
20-second-maximum solve. All finish `OPTIMAL` quickly:

| Source case | Cog case | Seconds | Inserts | Missing |
| --- | ---: | ---: | ---: | ---: |
| 0 | 0 | 0.010051900 | 12 | 9 |
| 1 | 1 | 0.007225600 | 12 | 9 |
| 2 | 0 | 0.007254400 | 10 | 11 |
| 3 | 1 | 0.007841100 | 11 | 10 |
| 4 | 2 | 0.008681700 | 13 | 8 |
| 5 | 3 | 0.008503200 | 13 | 8 |

The six returned layouts also pass original geometry and the frozen validator's
geometry checks, failing only the unchanged insert quantity. Counts match the
prior fixed-group optima; none improves the known 58-part partial, and no native
margin qualification or quality run is attempted.

From these outputs, each reduced joint model receives a complete zero/one hint.
Exact arithmetic checks every variable domain, conflict, family equality,
excluded frame set and objective: **57,374 constraints across four hints**.
Their insert counts are **12, 12, 13 and 13**. These witnesses establish that
the four reduced frame/bracket models are feasible despite their earlier
unseeded timeouts. They do not establish feasibility of the full 21-insert job.

## Next work and repository state

All eight unseeded joint searches expire without a candidate, although direct certified substitution now supplies an exact feasible whole-frame/bracket hint for every reduced case. Do not repeat those cold starts or the six fixed-group insert completions unchanged. Next build a changed reduced model selecting whole frames, brackets and inserts together: retain the certified frame/bracket survivors, all compatible original insert poses, original conflicts, quantities and frame exclusions; maximize the actual insert count up to 21, rather than the blocked-pose heuristic. Supply a complete feasible zero/one hint from the audited 12, 12, 13 and 13-insert partials. Declare finite limits before solving and preserve every incumbent, including an unchanged seed. Partial quantities receive no full-job credit. Any complete original 66-copy layout still needs original filled-outer geometry, frozen CLI, native-margin qualification and unchanged H5 material/cutting gates. H2 remains open under Artem’s original-denominator decision.

The hosted checks on pushed **f6edfb7** are still in progress in the [saved snapshot](h5-dominated-poses-and-seeds-20261020/main-ci-f6edfb7.json).
The previous local checkpoint and this evidence remain local until a subsequent
recorded push. Core source and the three current README hashes are unchanged.
There is no held-out evaluation, native packing, quality run, new release or
milestone credit.

[Checks](h5-dominated-poses-and-seeds-20261020/checks.json), [substitution audit](h5-dominated-poses-and-seeds-20261020/substitution-audit.json),
[reduced models](h5-dominated-poses-and-seeds-20261020/reduced-model-audit.json), [completed partials](h5-dominated-poses-and-seeds-20261020/completion-audit.json),
[feasible hints](h5-dominated-poses-and-seeds-20261020/seed-audit.json), [source review](h5-dominated-poses-and-seeds-20261020/source-review.json),
[all raw models, failures, layouts and certificates](h5-dominated-poses-and-seeds-20261020/raw.zip), and
[verified manifest](h5-dominated-poses-and-seeds-20261020/raw-manifest.json).
All 312 archive members, CRCs and byte hashes verify.
