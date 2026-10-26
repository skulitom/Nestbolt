# H5: source guards repaired for the retained 49 originals — 2026-10-26

**The retained 49 non-cog originals now pass every current source-clearance and
stock guard.** All two bracket movers and 15 cogs remain mandatory. This prepares
the next coordinated construction; it is not a complete 66-part fit. H2/H5 stay
open at **60%**.

## The failed small repair is preserved

The previous retained source readback had six pair-clearance and three stock
failures. The first construction enclosed the fixed-orientation filled outlines
in outward integer component rectangles, required 225 µm component gaps and
allowed translations of at most 50 µm per axis. An exact integer difference
constraint pass found the construction inconsistent. Its independent reader
preserves an eight-edge negative cycle with sum **−29 µm**, involving inserts
0 through 6. This excludes that sufficient construction model, not source
repair in general.

The cycle identifies the needed correction: insert 0 requires at least 13 µm
upward movement for stock clearance; the seven-insert stack then requires
insert 6 to move at least **79 µm**. A separate deterministic construction
therefore permits those seven inserts up to 79 µm in positive Y. Every other
coordinate bound, orientation, sheet and source identity stays as before.
The 225 µm construction gap and actual source/native requirements are unchanged.
All component-pair bounds are recalculated for the changed ranges, including
1,458 far pairs; an old 50 µm far-pair claim is never reused unsafely.

The new 98-variable, 284-constraint system has an explicit integer assignment.
It takes one exact pass sequence, without random seeds, an external solver or
time-budget extension. All 49 originals receive translations; the maximum
absolute axis change is **0.079 mm**. The previous failure remains frozen.

## Full original-ring readback of the retained subset

The independent reader verifies all 98 shifts, every constraint, 88 near and
1,458 far component pairs, source identity, sheet and orientation preservation,
and the complete partition into 49 retained originals plus 17 mandatory movers.
It then transforms the original source rings directly, reserving filled outers
with part-in-hole off. All **918 same-sheet source pairs** and **196 stock
edges** pass. All **69 cutouts and 6,294 hole vertices** are preserved.

Minimum source gap is **0.2256789543045 mm**, above the unchanged
**0.2117086725096 mm** requirement. Minimum extra stock margin is
**0.0131000000000 mm**, above **0.0114440917969 mm**. There are zero retained
source pair or stock failures. No native call is made for this partial layout.

The next geometry must be rebuilt from these corrected source transforms.
The older fixed-51-pose capacity exclusion remains valid for its original input;
it cannot be transferred to this changed arrangement. The remaining mandatory
originals are bracket copies 2 and 5 in canonical labeling (the original missing
copies 10 and 11) and all 15 cogs. All must fit and pass full source, native and
material checks before any H5 or release claim.

## Main CI and evidence

The Windows check completed successfully after the preserved browser timeout,
leaving five successful jobs. Only the browser job was retried, after the first
attempt had fully stopped. [Main 36f162d0 attempt 2](https://github.com/skulitom/Nestbolt/actions/runs/40400314122)
at 2026-10-26T21:44:38.604514+00:00: 5 of six checks pass; the browser-only retry remains in progress and must not be interrupted. Production, READMEs and upstream heads/releases
are unchanged. No held-out vectors or new release are involved.

[Checks](h5-retained49-source-guard-repair-20261026/checks.json), [source audit](h5-retained49-source-guard-repair-20261026/source-checks.json),
[corrected 49 placements](h5-retained49-source-guard-repair-20261026/corrected49-source.json),
[mandatory 17 movers](h5-retained49-source-guard-repair-20261026/mandatory17-movers.json),
[failed repair](h5-retained49-source-guard-repair-20261026/failed50um-result.json), [negative cycle](h5-retained49-source-guard-repair-20261026/negative-cycle.json),
[next step](h5-retained49-source-guard-repair-20261026/next-step.json) and [raw manifest](h5-retained49-source-guard-repair-20261026/raw-manifest.json).
The archive verifies 36 canonical files and
14 identical-content aliases by bytes, SHA-256 and CRC.
