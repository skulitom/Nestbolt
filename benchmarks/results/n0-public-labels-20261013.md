# N0 public-project labels and independent native references

All 44 original public LightBurn projects now have reviewed labels. Together
with 74 real files, 50 native derivatives and 170 generated habits, this gives
338 labels and 148 unique reviewed renders. The 183 robustness inputs have no
part labels by design. This is authoring evidence, not H2/H3 product acceptance.

The 44 projects were opened and saved/exported in the installed LightBurn Pro
2.1.01 hidden desktop. All 763 top-level shape memberships survived native save.
Original source bytes are unchanged. Re-saves and exports are auxiliary evidence
under the original permissive licences, not extra corpus inputs. No drawings
were uploaded. The owned application was closed and desktop lease released.

The unmodified published MIT `lbrn2-to-svg@0.5.3` has observable omissions and
transform errors. Authoring-only compatibility inputs materialize shared bitmap
data, expand compact linear primitives and regular polygons, substitute native
Text BackupPaths in their observed world coordinate system, and compose group
transforms into leaves. Group wrappers are omitted only during reference SVG
conversion: the package otherwise reflects SVG Y at every nested group level.
The original 59-project package run is still separate; these adaptations do not
claim that the raw converter handles every original shape.

The normalized reference vectors were checked against independent native SVGs
using analytic bounds and 65 samples per continuous subpath, in both directions,
against curves flattened to 0.0005 mm. **44/44 agree within 0.01 mm**; the largest
sampled distance is **0.001922815 mm**. All **151 image rectangles** agree in count
and corner positions, largest difference **0.000006404 mm**. Image-only cases do
not earn vector coverage in place of the separate image check.
The [audit](../datasets/shop/references/public/reference-audit.json) retains all
per-project results. The [earlier failed comparison](../datasets/shop/references/public/reference-audit-before-group-normalization.json)
is retained; bounding boxes alone missed a group-placement error in L16.

L00's two hidden layers are omitted entirely by the native SVG exporter. Their
per-shape reference geometry remains present and the label marks them fixed;
the exported-vector comparison excludes only those hidden leaves. Output-off
layers without `hide=1` remain in native SVG as `display:none` geometry.

The four contact pages were visually reviewed together with original XML.
[Review decisions](../datasets/shop/labels/public-review-decisions.json) guard
unit counts, fixed counts and hole histograms. Important fixtures include:

- L11: a rigid Group includes an output-off outline. The entire Group stays fixed
  with an explicit warning, preserving both rigidity and the fixed shape.
- L17: 32 axis-aligned open paths have exact zero-area bounds. Labels retain them
  and require a grouping/nonzero-proxy fix before nesting; none silently vanish.
- L28: missing Bezier controls produce the same straight-line fallback in the
  published reader and native export; the warning remains explicit.
- L33: no shapes, zero-byte native SVG; its PNG is the converter's empty-project
  diagnostic, explicitly distinguished from a geometry rendering.
- L40: native reports missing Sans Serif. Original BackupPath and native SVG
  bounds still agree; the warning screenshot is retained.
- L42/L43 and other older text: native save creates previously missing caches.
  These are reference geometry only. In L42, native 2.1.01 also changes legacy
  Scan+Cut settings to Scan; labels and eventual round-trip preservation use the
  original layer state. Native re-save is not a lossless no-op oracle.

The full label/hash audit passes; H1 still requires the frozen manifest and
writer-stratified held-out split before N1 begins. Milestone completion remains
0% at this checkpoint. The 11 earlier malformed/empty/incomplete negative
fixtures remain explicit and never earn a successful H2 import result.
