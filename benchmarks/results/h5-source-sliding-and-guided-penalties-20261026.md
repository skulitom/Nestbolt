# H5: source sliding and guided penalties — 2026-10-26

**Three bounded searches retain all 66 originals but produce no valid layout.**
The best returned positions still violate source pair or stock clearances.
All three searches are closed. Lower overlap penalties are not material savings,
higher valid part counts, or evidence that H5 passes. H2/H5 remain open at 60%
by completed gate weights.

## Source geometry and bounded searches

The starting allocation uses the verified eight-bracket/five-insert short sheet.
The first experiment fixes 18 frames and 11 inserts on the full sheet and moves
all remaining four brackets, five inserts and fifteen cogs jointly. A source
checkerboard of fifteen cogs at alternating 0°/13.5° and 261.25 mm pitch is
initially valid: 105 cog pairs and 435 fixed-core pairs pass, with a minimum cog
gap of 0.22859487 mm. This is only a 57-part source partial; the older 64-part
partials remain stronger and are preserved.

Configuration obstacles come from original filled outlines. Four cog phases,
eight bracket modes and two insert orientations are allowed. The second search
adds both frame orientations and releases every first-sheet part: 53 mandatory
originals, 106 continuous coordinates, and only 13 short-sheet originals fixed.
All 16 stock domains are rebuilt, retaining no former fixed-owner exclusions.
The 105 identical intrinsic obstacles are hash-checked; 31 frame pairs are new.

The third search uses a different adaptive objective starting from the second
search's saved best positions. All 1,378 pair terms and 53 stock terms remain
strictly positive. Before each stage, the top quarter of violated terms ranked
by squared depth divided by weight ratio receive a 1.5× weight increase (ratio
capped at one million). There are at most 100 stages, with legal mode sweeps
every fourth stage. Best poses are compared using the unweighted geometric
penalty, since scores with changing weights are not comparable.

| Search | Moving first parts | Returned status | Optimization / shared seconds | Source pair failures | Stock failures |
| --- | ---: | --- | ---: | ---: | ---: |
| Fixed 29 first parts | 24 | LOCAL_STATIONARY | 0.268804 / 7.809760 | 40 | 5 |
| All first parts | 53 | LOCAL_STATIONARY | 0.701100 / 5.011996 | 52 | 9 |
| Adaptive positive penalties | 53 | ITERATION_LIMIT | 14.120617 / 15.284898 | 50 | 10 |

Each search starts once, without random restarts, within its declared 60-second
search / 90-second shared limit. Respectively they make 473, 526 and 14,243
objective evaluations. Best unweighted penalties are 8,434.111700, 6,083.424728
and 5,004.590670 mm²; these are overlap diagnostics, not usable layout scores.
Neither all-part search accepts a frame turn: every accepted mode change is a
cog phase change, and all 18 best frames retain the unturned mode. This suggests
a limitation of single-part greedy turns from this initialization; it does not
prove that a coordinated rearrangement or any source layout is impossible.

## Independent acceptance and preserved failures

Three preflight checks cover source mode reconstruction, sampled obstacle/stock
geometry and numerical gradients (36, 60 and 60 checks). Geometry samples are
not continuous proofs. Each independent final reader reconstructs all original
rings directly from the job and verifies identities, legal transformations,
1,456 same-sheet pairs, 264 stock edges, and all 90 cutouts/10,026 hole vertices.
Pair guard is 0.21170867250963943 mm; extra stock guard is 0.011444091796875 mm.
Every returned layout fails these source conditions. No native validator is
called, no full quality run occurs, and no unrestricted exclusion is claimed.

The first guided reader rejected a diagnostic sum differing by one floating
point unit (9.094947017729282e-13). That failed checker and its result remain
preserved. A repaired reader allows 32 units only for diagnostic sum comparison;
physical source thresholds are unchanged. It replays all 100 positive weight
updates without rerunning the search and confirms the same invalid geometry.

## Repository checks and next evidence

Main ea4f2ebf's first browser job exhausted its 30-minute limit downloading
Ubuntu dependencies; browser tests had not started. Its log, terminal result
and retry request are preserved. After the other five jobs had completed,
only that browser job was rerun on the same commit. At 2026-10-26T18:44:39.423197+00:00,
[all six main checks pass](https://github.com/skulitom/Nestbolt/actions/runs/40372823229)
on attempt 2. No live main job was cancelled and no application changes were
made to obtain the pass.

The next distinct hypothesis uses the preserved 64-part allocation with three
cogs on the short sheet and adds its two missing brackets while releasing all
57 required first originals. It must first address the old partial's clearance
below the current native guard, use its actual source rotations, and validate
the changed short sheet. It is not a continuation of any closed 53-part run.

Production, READMEs, upstream heads/releases and all 22 reserved H2 vectors are
unchanged. No new release is qualified. [Checks](h5-source-sliding-and-guided-penalties-20261026/checks.json),
[scope](h5-source-sliding-and-guided-penalties-20261026/scope.json), [mode evidence](h5-source-sliding-and-guided-penalties-20261026/mode-change-audit.json),
[next step](h5-source-sliding-and-guided-penalties-20261026/next-step.json) and [raw manifest](h5-source-sliding-and-guided-penalties-20261026/raw-manifest.json).
The archive verifies 258 canonical files and
439 aliases by bytes, SHA-256 and CRC.
