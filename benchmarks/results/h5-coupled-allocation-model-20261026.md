# H5: fully coupled two-sheet necessary model — 2026-10-26

**The new model allows each of the 66 originals to choose its sheet and geometry
variant, but its one bounded search returns UNKNOWN without an assignment.**
There is no source layout or impossibility proof. H2/H5 remain open at 60%.

## Every original, linked to both sheets

The model has **609 variables and 5,016 constraints**. Each original chooses
exactly one of its legal sheet/variant options; there are **342 options** in
total. A shared X/Y anchor is bounded by four guards for the selected option.
The sheet bit is linked to that same choice. A sheet/Y key orders identical
copies without fixing positions or the short-sheet allocation.

The three short-sheet counts are sums of the original sheet bits and are linked
to all **454 surviving count vectors**. The model also checks filled original
source area on both sheets, using downward-rounded integer square-micrometre
coefficients and the original target stock areas. Proxy areas are not used for
these two constraints. They rule out four further short vectors `[bracket,
insert,cog]`: `[0,0,0]`, `[0,1,0]`, `[0,2,0]` and `[1,0,0]`.

These count exclusions do not exclude the full job. The mathematical stock
relaxations used by geometry never enlarge the source/material acceptance
target. All frames stay on the first sheet, and all 15 cogs remain represented
by the previously proved all-angle necessities.

## Optional source geometry and separate cog capacity

The selected source-contained coarse rectangles participate in one NoOverlap2D
per sheet. There are 381 optional coarse rectangles for the first sheet and 345
for the short sheet. Only rectangles belonging to selected options are active.
Four source-capacity constraints use the non-cog rectangles and the 16 source
inner-disk strips per cog: 606/570 optional rectangles by sheet.

Four different capacity constraints use the virtual separation disks **only
among cogs**, with 240 optional rectangles per sheet. Those virtual disks never
enter mixed-family collision or source-capacity constraints. All 1,686 optional
rectangles use the same selected sheet/variant literal as their parent original.
Actual cog angles are not chosen by this necessary model.

An independent protobuf reader checks every variable and all 5,016 constraints,
including 1,368 stock guards, 3,372 optional intervals, all 62 copy orders, the
linked table, both source-area bounds and every capacity membership. It verifies
that every original is mandatory, every option activates only its own geometry,
no short allocation is fixed, and there are no hints or objective. The model
SHA-256 is `1027dd1d8bf01231e52b0fe4d5ff9ac42832a07e77ce1eae0b8e8317dd0585b2`.

## One closed search

The sole call requests 60 solver seconds within 90 shared seconds, with the
previously overlong `fj` worker excluded. It starts real search and returns
**UNKNOWN**, recording **87,096 branches and 62,265 conflicts**. Solver time is
**60.054159 seconds**, returned solve **60.056339**, shared process **61.456279**.
The 0.054159/0.056339 second soft overruns are preserved. No assignment, source
candidate, native call or full quality run is produced.

The response audit verifies the model hash, parameters, raw solver response,
log and closed process boundary. The call is CLOSED without extension,
reseeding or retry. These checks do not establish infeasibility of this necessary
model or the complete source job.

The next distinct investigation can map the earlier preserved 64-original
source layout into these necessary geometries and construct explicit proxy
anchor regions for its two missing bracket copies. Both missing originals must
remain mandatory. Any resulting proxy assignment still needs actual original
collision analysis; it must not be presented as a source layout or used merely
to rerun this unchanged coupled solver.

## Repository and evidence

At 2026-10-26T20:40:17.777102+00:00, [main ff5036af checks](https://github.com/skulitom/Nestbolt/actions/runs/40393931732):
5 of six checks pass; preserve the remaining live checks before the next push. Checkpoints 09091745 and 1cc9300c remain queued locally. Production,
READMEs and upstream heads/releases are unchanged. All 22 reserved H2 vectors
remain unopened, and no new release is qualified.

[Checks](h5-coupled-allocation-model-20261026/checks.json), [full model audit](h5-coupled-allocation-model-20261026/model-checks.json),
[response](h5-coupled-allocation-model-20261026/response-checks.json), [source-area exclusions](h5-coupled-allocation-model-20261026/source-area-excluded-count-vectors.json),
[scope](h5-coupled-allocation-model-20261026/scope.json), [next step](h5-coupled-allocation-model-20261026/next-step.json) and
[raw manifest](h5-coupled-allocation-model-20261026/raw-manifest.json). The archive verifies
34 canonical files and 6
identical-content aliases by bytes, SHA-256 and CRC.
