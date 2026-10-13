# LightBurn reader checkpoint — 2026-10-13

**H3 is incomplete; completed milestone progress remains 15%.**

The core now reads original `.lbrn`/`.lbrn2` documents into a separate geometry
scene while retaining every original XML byte. Supported inspection includes
both path encodings, independent shared vertices/primitives, forward references,
StartV, Rect/rounded Rect, Ellipse, Polygon, Group, cached Text and shared Bitmaps.
Layer identity includes image/vector family; kerf and fixed content are reported.
The diagnostic `lightburn_inspect` example uses this same core API.

[Final reader run](h3-reader-20261013T220428Z.json): 56/56 frozen training projects
parse; 56 no-op outputs are byte-identical. Maximum time is 0.252 s. Eight projects
contain 122 uncached Text shapes: XML remains intact, geometry is explicitly
incomplete, and warnings ask for a native re-save to cache the font outlines.

[Independent geometry run](h3-geometry-20261013T220610Z.json): all 1,550 comparable
leaf shapes pass, covering 2,046 contours. It compares 64 points per contour in
each direction against curves flattened at 0.0005 mm, plus bounding boxes and
image corners. Maximum contour distance is 0.000906 mm, box difference 0.000712 mm,
and image-corner difference 0.000029 mm, below 0.01 mm. Complete geometry is proved
for 48 projects; uncached text is counted as missing, not a passing comparison.

The published `lbrn2-to-svg@0.5.3` package is unchanged. Its test-only adapter
normalizes the native-verified N0 limitations (groups, text caches, sharing,
compact line runs and regular polygons). The new run exposed a further issue:
zero-valued handle coordinates can be omitted. The
[initial comparison](h3-geometry-20261013T215946Z.json) had 1,542 passing and eight
failing shapes, despite matching bounds; largest contour distance was 0.812520 mm.
Both the first product reader and the oracle missed these handles.

LightBurn's frozen SVG exports independently establish the omitted-zero rule.
After correcting the reader and reference adapter, all eight affected native
shapes also pass direct native-SVG comparisons, with maximum distance 0.000283 mm
and box difference 0.000006 mm. The earlier
[reader run](h3-reader-20261013T215600Z.json) and failures remain preserved.

Seven authored core tests pass. They cover exact no-op preservation, independent
sharing, StartV, transforms and text caches, legacy/compact cubic equivalence,
primitive shapes/open paths, unsupported geometry, invalid references/numbers,
and omitted zero handles. Strict workspace Clippy and the WebAssembly check pass;
the native diagnostic builds. All 1,181 frozen hashes verify.

Reader processes used four CCD0 physical cores, one child per core. Geometry
comparison used one further CCD0 physical core after the reader run ended;
builds/tests used CCD1. Source/binary/runner hashes stayed fixed during each run.
No held-out project, geometry or label was read; no source file was modified.

This checkpoint adds inspection and no-op preservation. Nesting units, per-sheet
writing, canonical nesting diffs, original uncached-text support, UI/CLI/MCP
integration and native opening checks still need work. H2 also remains incomplete.
The [machine-readable checkpoint](h3-reader-checkpoint-20261013.json) records
the retained failed trials and exact verification scope.
