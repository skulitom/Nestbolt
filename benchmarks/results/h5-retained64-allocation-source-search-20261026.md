# H5: retained 64-part allocation with all first parts movable — 2026-10-26

**The older nine-part short sheet now passes current source clearances, but a
new search for all 57 required first-sheet parts still fails.** All 66 original
identities and cutouts remain present. There is no complete target witness;
H2/H5 remain open at 60% by completed gate weights.

## Repair the distinct short allocation first

The preserved 64-part result has four brackets, two inserts and three cogs on
the short sheet. Its first sheet has 18 frames, six brackets, 19 inserts and
12 cogs; bracket copies10/11 are missing. This allocation differs from the prior
53/13 experiments, which remain closed. Original evidence is retained unchanged.

Original source rotation is preserved exactly: cogs use
**-2.2428996024478143 radians**, and horizontal reversed inserts use pi. Both
are added to the mode table by transforming the original rings, with no tooth
symmetry assumption. There are now 18 source modes and 171 unordered pair
obstacles: 136 unchanged intrinsic obstacles are hash-verified and 35 are new.
Geometry preparation takes 4.979303 seconds.

Before repair, the short sheet fails three pair guards and one stock guard.
Its minimum pair gap is 0.2011 mm and extra stock margin is 0.0001 mm. A single
fixed-mode translation repair takes 21 evaluations / 0.007894 seconds within
its declared 10-second/2,500-evaluation limit. Independent original-ring readback
then passes all **36 pairs, 36 stock edges, 17 cutouts and 2,308 hole vertices**.
Minimum pair gap becomes **0.2243086724868379 mm** and extra stock margin
**0.012600000000188238 mm**, above the unchanged native guards. Angles, mirror
attributes and original geometry are preserved; only positions change.

## One full first-sheet search

All 55 original first poses are preserved in the seed. The two missing brackets
are inserted using a deterministic 50 mm stock grid including stock boundaries
and all eight bracket modes. The second insertion accounts for the first.
All **22,640 proposals** are retained. The selected initial anchors are
[1150,2650] mm in mode6 for original28 and [200,2550] mm in mode4 for original29.
Insertion preparation takes 1.712307 seconds. This is one seed, not a valid fit.

The new inventory keeps all **57 first originals movable**: 18 frames, eight
brackets, 19 inserts and 12 cogs. The repaired short9 stays fixed. Preflight
reconstructs all18 modes, verifies 108 stock samples, 4,275 obstacle samples
(2,896 outside-source checks), and 60 weighted gradient checks. Samples are
not a continuous geometry proof. Every 1,596 pair term and 57 stock term stays
strictly positive; 100 adaptive updates and legal mode sweeps use the same
declared algorithm as the earlier guided experiment on this different inventory.

The sole call closes **ITERATION_LIMIT** after **29.220400 optimization /
30.492711 shared seconds**, within 60/90 seconds. It performs 21,787 objective
evaluations, 100 returned stages, 4,000 mode trials and 17 accepted changes
(nine cog, seven insert and one bracket changes). All18 frames remain unturned.
No retry, extension or random restart occurs.

Best unweighted overlap penalty falls from 8,880.895434 to 1,278.391832 mm².
This is not a material saving or a valid part-count improvement. The independent
final reader checks **all66 identities, 1,632 same-sheet pairs, 264 stock edges,
90 cutouts and 10,026 hole vertices**, finding **60 pair failures and 10 stock
failures**. It replays all100 weight updates and confirms no constraint was
removed. Therefore no native call or full quality run is qualified. Neither
this local failure nor the finite modes prove unrestricted impossibility.

## Checkpoint and remaining work

At 2026-10-26T18:52:18.990433+00:00, [all six main ea4f2ebf checks pass](https://github.com/skulitom/Nestbolt/actions/runs/40372823229),
allowing a normal two-commit push with the queued7a37f3da evidence. Production,
READMEs, upstream heads/releases and all22 reserved H2 vectors remain unchanged.
No new release qualifies. The next search needs a materially different source
geometry mechanism, such as coordinated orientation/position changes; these
closed runs must not be extended or reseeded. A full66 source/native/material
witness remains required before integration and the full H5 matrix.

[Checks](h5-retained64-allocation-source-search-20261026/checks.json), [short repair](h5-retained64-allocation-source-search-20261026/short-repair-result.json),
[preflight](h5-retained64-allocation-source-search-20261026/preflight-checks.json), [full result](h5-retained64-allocation-source-search-20261026/result-checks.json),
[scope](h5-retained64-allocation-source-search-20261026/scope.json), [next step](h5-retained64-allocation-source-search-20261026/next-step.json),
[raw manifest](h5-retained64-allocation-source-search-20261026/raw-manifest.json). The archive verifies
258 canonical files and 1327
aliases by bytes, SHA-256 and CRC.
