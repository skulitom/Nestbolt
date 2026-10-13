# N0 generated shop habits — 2026-10-13

**H1 remains pending; v1.1 completion remains 0%.** This report checks corpus
authoring. It does not run or make a claim about the Nestbolt importer.

`scripts/shop_habits.py` produces **170 DXFs and 170 labels** from ten clean base
drawings: six selected designs from the original v1 SVG examples and four
original procedural maker parts. Only the development job
`m-mechanical-cog-washers` is read; the generator checks it against the frozen
maker manifest and refuses held-out input. All derived drawings are MIT, with
source hashes, selected elements and transformations recorded in the
[generated manifest](../datasets/shop/generated/manifest.json) and per-file
[attribution](../datasets/shop/LICENSES.md).

The ten clean base shapes and hole counts were visually reviewed in
[this millimetre plot](n0-generated-20261013/clean-bases.png). The shapes include
rounded corners, a Bézier/elliptical-arc outline, a washer, two frames, a rotated
frame, an ellipse, an L-bracket with three holes, a cog and a drilled insert.

Each base receives all 17 variants:

- Exploded, shuffled and randomly reversed segments.
- Gaps of 0.001, 0.05 and 0.5 mm. Labels give both endpoints, measured gap and
  explicit healing tolerance where needed; without it, a clear failure is required.
- Collinear overlaps requested at 0.001 and 0.5 mm. On short curve chords the
  overlap is capped at half the chord length; every label gives the actual size.
- Two duplicate edges (including a reversed edge) and one zero-length segment.
- SPLINE control points/knots and circular arcs with extrusion `(0,0,-1)`.
  Bases without circular arcs still exercise SPLINEs; the manifest makes no
  claim that every base contains an arc.
- Closed LWPOLYLINEs with bulges where the base has circular arcs, and variable
  segment widths. Cut labels describe the centreline, not the visible stroke.
- Nested mirrored blocks with nonuniform scale and rotation, and a separate
  case containing only one INSERT for the entire drawing.
- Headerless R12 inch geometry, missing `$INSUNITS` inch geometry, and explicit
  centimetres. Inch labels require an explicit unit override; default import
  must warn and leave the coordinates unscaled.
- TEXT, MTEXT, DIMENSION, HATCH, LEADER and SOLID annotations, with bend/extent
  construction layers.
- Generic operation layer names with ACI colours for cut, score and engrave.
- A complete three-part existing nest and a separate SHEET outline.

## Verification

Run with the pinned Python 3.11 [authoring dependencies](../datasets/shop/requirements.txt):

```
python scripts/shop_habits.py --check
python scripts/shop_generated_audit.py
```

The generator uses seed **110013**, per-case derived seeds, fixed DXF metadata
and sorted DXF classes. A separate process reproduces all generated DXFs,
labels, bases and the manifest byte-for-byte. Generation refuses to overwrite
a frozen corpus; after H1 only the check mode is allowed.

All **170 DXFs parse independently with ezdxf 1.4.4**. An independent file read
of the cut centrelines matches the labelled outer bounds within
**0.000495 mm** (limit 0.002 mm), after applying the declared units and each
nested INSERT matrix. This includes the mirrored and nonuniform block case.
The audit also measures the actual loose endpoints for gap cases, checks
duplicate/zero-length counts, and checks the missing headers/units, centimetre
header, single INSERT, annotation types and operation colours. See the
[machine-readable audit](n0-generated-20261013.json).

The labels are derived from the source curves and declared generator edits,
not from Nestbolt's output. They give cut parts, holes, outer bounds, cut
layers/colours, import options, warnings and the expected default failure where
applicable. These are expected results for later H2 tests, not passing H2 results.

## Authoring corrections retained in the record

The first reproducibility check found unordered DXF class registration; required
classes are now sorted before writing. Removing only the header of a modern
DXF left incompatible layout records, so the headerless case now starts from a
legal R12 drawing. An initial bounding-box check included polyline stroke widths
and approximated nested nonuniform INSERTs with a decomposed INSERT. That check
was replaced by cut-centreline paths and exact per-level matrix application;
the original analytical labels agreed with the actual DXF matrices. No product
code was changed to make these checks pass.

Remaining H1 work is the independent render-backed labels for real/native/public
projects, complete manifest validation, and the stratified held-out freeze.
