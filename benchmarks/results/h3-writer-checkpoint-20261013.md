# LightBurn units and preserving writer checkpoint — 2026-10-13

**H3 remains incomplete; completed milestone progress remains 15%.**

The shared core now assembles rigid nesting units and writes a selected sheet of
a version-1 LightBurn project. Top-level groups stay together. A closed cutting
shape takes wholly contained engraving, image and text bounds; containment checks
the whole rectangle against holes and concavities. If several cutting outlines
contain a shape, the smallest wins with a warning. Fixed content survives in every
output, and incomplete movable geometry stops nesting with repair instructions.

Closed multi-contour shapes use containment parity; rigid group components are
unioned. Text, images and open shapes use bounds. Axis-aligned open strokes can
be attached to an enclosing cut or protected within a group using a one-tolerance
envelope; standalone zero-area bounds still require grouping. These footprints
do not rewrite the original curves or layers.

The writer edits byte ranges. It composes placements with top-level XForms,
removes other sheets' units, independently re-homes vertex/primitive/image
definitions whose owners were omitted, and optionally adds the T1 sheet rectangle
and missing Tool setting. Children, text caches, unknown XML, all cut settings,
root origin flags and document metadata remain intact. It refuses to overwrite
a non-Tool setting at index 30. It supports repeated unit copies and an exact
identity write with the outline disabled.

[Training writer audit](h3-writer-20261013T222334Z.json):

- 50/56 projects write and have byte-identical identity output. Six reject
  incomplete movable text; the two legacy projects are among those six.
- 100 diagnostic sheet files pass an independent canonical XML diff whitelist.
  They contain 227 units across 76 nonempty sheets; 376 fixed top-level shape
  occurrences stay in place. Re-homing moves 180 vertex and 50 primitive lists.
  Bitmap re-homing is exercised by the authored test, not this corpus partition.
- 46 projects have nonempty diagnostic layouts accepted by the independent core
  validator. Four contain no movable units and are not credited as validated
  layouts. Maximum complete diagnostic process time is 0.588 s, including the
  reader, assembly, two writes, rereads and validation.

[Independent footprint and placement audit](h3-unit-geometry-20261013T222532Z.json):
all 227 unit footprints agree with the hashed per-shape SVG references from the
published MIT converter, using the previously native-verified normalization.
Maximum boundary Hausdorff distance is 0.000579 mm, below 0.01 mm. GEOS checks of
the same diagnostic placements using those reference footprints find zero
overlap and zero area outside the sheets. This is a deterministic writer test,
not a search quality or material-efficiency result.

Twelve core tests pass, as do strict workspace Clippy, the WebAssembly check and
the native diagnostic build. All 1,181 frozen hashes verify. The first new test
run retained a strict-float equality failure (3.06e-16 mm); its geometric assertion
now uses 1e-10 mm. The first Clippy run caught a map-iteration style issue; fixed.
Logs and their hashes are listed in the machine-readable checkpoint. No held-out
source or label was inspected. Benchmark children ran on four separate CCD0
physical cores; Python/XML and reference geometry used another CCD0 core.

Remaining: UI/CLI/MCP integration, actual search layouts, native opening/settings
and mirrored-origin checks, legacy output conversion, and complete uncached-text
support. The current core writer explicitly requests a native version-1 save for
legacy input; this is not completion of the plan's legacy output requirement.

Separately, the [pushed checkpoint's Linux CI job](https://github.com/skulitom/Nestbolt/actions/runs/38476307333/job/115567734686)
found an existing whole-search fuzz panic in jagua-rs `QTHazard::constrict`.
The [exact shrunk case and seed](ci-search-panic-20261013.json) are preserved.
That failure remains open and takes priority before the next push. It does not
change the XML/geometry results above; a passing full-workspace CI is not claimed.
