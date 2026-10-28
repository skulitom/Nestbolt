# Whole upper-group source search and baseline target review — 2026-10-28

Freeing the whole upper group still produces **no valid 66-part layout**.
The one bounded source search ends at a local minimum, and the independent
original-shape reader finds 34 pair failures and eight stock failures. This
does not prove the enlarged construction domain impossible. The call is closed.

## Enlarged source construction

The fixed core contains 42 independently valid originals: 18 frames and inserts
5–15 on the first sheet, plus eight brackets and five inserts on the short sheet.
All 15 cogs, four first-sheet brackets and five upper inserts may move. Compared
with the previous 17-mover model, two existing corner brackets and five inserts
are now free. Every bracket retains all eight modes, every insert both outer
classes, and the cogs use the declared 7° phase. No part or stock requirement
changes, and the valid short-sheet allocation remains eight brackets/five inserts.

The rebuilt geometry has 11 fixed-neighbor free regions and 66 pair obstacles:
45 identical intrinsic obstacles are verified and reused, and 21 involving
inserts are new. Preflight reconstructs all 11 modes from original coordinates,
checks 1,089 source-pair samples and 11 free-region representatives, and verifies
all 48 gradient components. The 22 previously placed movers exactly match the
audited source64 layout. All 66 originals are accounted for once.

The sole call returns LOCAL_STATIONARY after two positional stages, 212 objective
evaluations, 66 mode trials and one accepted change. Search time is **0.074719 s**;
shared process time **2.892560 s**. There is one initial configuration and no
random restart. The independent readback checks 1,456 pairs, 264 stock edges and
all 90 holes with 10,026 hole vertices. It retains all 34 pair failures and eight
stock failures, including the worst extra stock clearance of −5.525542 mm.
Neither source validity, native validation nor H5 completion is claimed.

## Baseline provenance

A separate read-only review verifies the nine retained laser large-plates
archives: three seeds for normal, common baseline and common candidate modes.
CRC, archive hashes, layout hashes, both source-job hashes and saved validations
are checked. All 594 original placements are reconstructed, with 13,974 filled
outer pair checks and 36,884 hole-containment checks.

Each normal layout places **all 21 inserts inside holes**, totaling 415,800 mm²
of filled insert area. Each common-line layout has zero hole riders and zero
filled-outer overlaps. The normal baseline therefore cannot be reused directly
when holes must remain reserved. This is a provenance check, not a new benchmark
or a global infeasibility argument.

The normal three-seed material median is **4,939,495.3995 mm²**. Multiplying by
the unchanged 1.01 limit reproduces **4,988,890.353495 mm²**, and the target short
outline top remains **319.42690233 mm**. No comparator, seed, metric, allowance
or threshold is replaced.

The first review attempt compared a serialized-job hash with the record's
dataset-job hash. Its failed reader and diagnostic are preserved. The corrected
reader independently verifies each hash against its corresponding original file;
no source file or recorded hash changed and no solver was rerun.

## Next step and publication

The proven short-sheet 7/5/1 and 7/6/1 exclusions remain closed. All 452 remaining
count allocations are retained. Next screen distinct remaining maximal count
vectors with the audited source X-capacity model, using a declared bounded pass
and retaining every unknown or unprocessed case. Verified exclusions may prune
counts; positive relaxed assignments still require actual source construction.

Main `541d5bc9` now passes all six jobs in
[CI 40685021297](https://github.com/skulitom/Nestbolt/actions/runs/40685021297).
The count-exclusion checkpoint and this evidence can be pushed together after
fresh remote and live-run checks. Production, READMEs and upstream heads/releases
are unchanged. H2/H5 remain open at **60% completed milestone weight**; all 22
reserved H2 vectors remain unopened, and no new release qualifies.

[Source preflight](h5-oblique24-baseline-review-20261028/source-preflight.json),
[closed source result](h5-oblique24-baseline-review-20261028/source-result-checks.json),
[baseline checks](h5-oblique24-baseline-review-20261028/baseline-target-checks.json),
[original baseline records](h5-oblique24-baseline-review-20261028/baseline-source-records.json),
[next step](h5-oblique24-baseline-review-20261028/next-step.json),
[byte-verified archive](h5-oblique24-baseline-review-20261028/raw-manifest.json).
The archive preserves 147 canonical files and
148 identical-byte aliases in 3,183,963
compressed bytes, including all source inputs, original comparator archives,
new free regions, every reused obstacle, auditors, raw failures and provenance
repair records.
