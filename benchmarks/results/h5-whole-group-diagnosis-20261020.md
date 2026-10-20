# H5: bounded branching and whole-group diagnosis — 2026-10-20

**No complete layout or improved partial was found.** Fixing complete frame and
cog arrangements reduces six previously difficult conditional problems to
sub-second solves, but each leaves 8–11 inserts missing. H2/H5 remain open at 60%.
The README already describes the published preview and the remaining work;
no product change or new release is justified by these diagnostics.

## Bounded LP-guided branching

The [previous area relaxations](h5-area-capacity-relaxations-20261020.md) leave all
four cog cases feasible only fractionally. This construction fixes actual
placement decisions, propagates conflict cliques and family quotas, and requires
all 21 inserts. It reuses the saved roots and restores each parent simplex basis.
A tiny saved probe checks the installed HiGHS API against an elementary LP before
the construction; no solver package or product dependency is changed.

The plan declares **120 seconds total**, at most **512 visited nodes**, at most
**10 seconds per LP**, eight offline threads and seed zero. Round-robin cases use
depth-first branching, selecting the highest-valued available pose in the first
unfinished family: frame, bracket, insert. The selected branch precedes exclusion.
The search stops after **120.005029800 seconds and 421 LP calls**. All inputs,
branch states, decisions, results and 41 unvisited frontier entries are retained.
No suffix is retried.

- 227 optimal fractional vectors; all independently checked against the original
  rows, area capacities, exact quantities and fixed-variable bounds.
- 193 restricted LP infeasibility reports and one final time limit, preserved as
  solver reports without an independent global infeasibility certificate.
- 417 calls restore a parent basis; the four initial branches start cold.
- Maximum fixed frames in cases 0–3: **9, 10, 12, 13**. No case completes the
  required 18 frames or reaches bracket/insert branching.

Independent set-based propagation reproduces every state, branch choice, visit
order and frontier entry. Maximum row, equality and bound residuals are
8.48654×10⁻⁷, 1.19096×10⁻¹⁰ and 3.66934×10⁻¹¹ respectively.
The existing 58-part partial is preserved exactly, with eight inserts missing.
These failures do not prove the unrestricted job impossible.

## Complete frame groups

The already audited source events contain **48 complete source frame groups**,
deduplicating to **26 exact sets of 18 original poses**. All 3,978 within-frame
pairs pass filled-outer checks; minimum distance is 0.225 mm.
Crossing these sets with the four complete 15-cog arrangements yields 104
combinations. All 20,592 same-sheet frame/cog pairs are checked, and the result
agrees with the existing candidate compatibility map. **Only six combinations
are compatible.** All six retain enough individual bracket and insert candidates
to pass a simple quantity count; that count alone does not show they can coexist.

For each compatible pair, a new finite model fixes all 18 frames and 15 cogs,
requires 12 brackets, and maximizes whole inserts from zero to the original cap
21. It projects the original conflict cliques onto every surviving candidate.
Models contain 542–964 Boolean variables and 1,804–3,069 distinct cliques.
All six protobuf models, including objective, domains, quantities and hint, are
independently reconstructed before solving. Geometry checks also cover all
101,663 same-sheet pairs within fixed groups and between each surviving pose and
the fixed parts. The matching case receives the complete known 58-part hint.

Each case declares one **20-second maximum**, eight workers and seed zero.
All six return `OPTIMAL` in less than 0.6 seconds:

| Case | Frame group | Cog group | Seconds | Inserts placed | Inserts missing |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0 | 0 | 0 | 0.191282200 | 12 | 9 |
| 1 | 0 | 1 | 0.099330800 | 12 | 9 |
| 2 | 1 | 0 | 0.132531800 | 10 | 11 |
| 3 | 1 | 1 | 0.132775400 | 11 | 10 |
| 4 | 2 | 2 | 0.451055900 | 13 | 8 |
| 5 | 2 | 3 | 0.566813300 | 13 | 8 |

These are solver-reported optima for the **fixed-group finite-pose subproblems**.
They are not independent infeasibility certificates or upper bounds on arbitrary
continuous layouts. They show that recombining the retained smaller-part poses
with these six fixed groups cannot supply all 21 inserts.

All **20 callback incumbents plus one different final layout** pass independent
original filled-outer, rotation, margin, clearance and target-material checks.
The frozen original CLI rejects all 21 layouts **only for the original insert
quantity shortfall**. None is promoted to a valid full job, and native-margin
qualification has not been attempted.

## Preserved audit corrections

The first combined auditor could not start: the existing geometry environment
lacks protobuf, and the existing solver environment lacks Shapely. Both failures
and the original auditor are saved. The corrected audit uses the two existing
environments for their respective checks and binds them to identical input
hashes. No package is installed and no solve is repeated.

The first result auditor incorrectly requires the final selected indices to
equal the last callback. Case 4 returns a different layout with the same optimum.
The failure, original auditor and completed checks remain. The corrected auditor
checks this additional final layout separately and reuses the already saved CLI
checks after verifying their exact layouts and commands. No search or completed
validator measurement is repeated.

## Next investigation and repository state

The six complete frame/cog combinations from the retained layouts are exhausted within this finite pose pool; do not rerun them unchanged. Next investigate a changed model requiring whole frame placements while temporarily relaxing bracket/insert variables, with an explicit constraint excluding the 26 already reviewed exact frame sets. Fix one original cog arrangement at a time. Declare finite time/case limits before running. Only newly found complete 18-frame sets should proceed to a separately bounded exact bracket/insert completion check. Fractional completion or restricted infeasibility has no original-job acceptance credit. If no new complete set appears, preserve that failure rather than retrying a suffix. Any full original 66-copy layout still needs the frozen validator, independent filled-outer geometry, native-margin qualification and unchanged H5 material/cutting gates. H2 stays open under Artem’s explicit decision to retain the original denominator.

Product digest and all three current README hashes remain unchanged. The hosted
browser continues to be a preview from main. All six checks for pushed merge
8a81205 now pass ([hosted evidence](h5-whole-group-diagnosis-20261020/main-ci-8a81205.json)).
These new offline diagnostics and the preceding area checkpoint are local until
a subsequent recorded push.
No held-out evaluation, native packing, quality run, registry publication,
release asset or milestone credit changes.

[Checks](h5-whole-group-diagnosis-20261020/checks.json), [branch audit](h5-whole-group-diagnosis-20261020/diving-audit.json),
[census](h5-whole-group-diagnosis-20261020/frame-census.json), [model audit](h5-whole-group-diagnosis-20261020/model-audit.json),
[result audit](h5-whole-group-diagnosis-20261020/result-audit.json), [source review](h5-whole-group-diagnosis-20261020/source-review.json),
[raw inputs, models, branches, failures and layouts](h5-whole-group-diagnosis-20261020/raw.zip), and
[verified manifest](h5-whole-group-diagnosis-20261020/raw-manifest.json). All 1300 archive
members, CRCs and byte hashes verify.
