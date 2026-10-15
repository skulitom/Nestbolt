# N5 lead planning and searched native coupons — 2026-10-15

The core planner now chooses contour starts, constructs the calibrated line/arc
leads, shortens them when needed, and supplies enlarged collision geometry to the
existing search. This checkpoint starts from `43684ad`. H6 remains open and the
completed milestone total remains **15%**.

## Core contract

`lead_in::prepare` retains the original job and source curves. It returns a
separate collision job and one reservation or explicit flag per contour. Local
lead coordinates are millimetres even for inch jobs. Line length is 0.5–50 mm;
arc length and sweep follow Artem's approved plan decision 3. Near-zero arcs use
a stable chord only when its sagitta fits inside the independent envelope's
existing approximation allowance.

Outer candidates are convex corners in descending turn order, then midpoints
of straight edges. Collinear subdivisions, including the source seam, form one
edge. A smooth outer contour uses the arc-length midpoint of its longest curve
segment. Holes prefer the longest straight edge; smooth holes use a boundary
point nearest their area centroid, with radial straight leads capped at the
centre. The smooth-boundary search is bounded and heuristic.

Each attachment reserves both traversal directions. At a corner, reversing uses
the incoming edge's reversed tangent. This matters because LightBurn can reverse
cut direction while retaining the start point. Shared-edge attachment intervals
can exclude candidate starts, including intervals crossing the source seam.
Length trials reduce by 10% down to an explicit 0.5 mm attempt. A flag means these
candidate trials failed; it does not prove no other feasible attachment exists.

The validator's new `Owner` check rejects a lead that pierces material or cuts
deeper than the contour's ordinary half-kerf band. The owner contour is flattened
at 0.0001 mm. Offset/grid/flattening allowances total 0.000808 mm at this boundary
check; the lead centreline is checked separately against a much shallower inset.
The pierce disc must clear the original owner. A fully eroded owner fails closed.
Previously reserved contours' lead envelopes may not overlap one another.

The collision job unions original polygon material, the tightly flattened exact
curves and the two physical lead envelopes. The original job is used for final
material metrics and independent original-part validation in the integration
test and diagnostic generator. Public search/report callers are not yet wired
to this separation. Multi-component rigid units currently reject explicitly.

## Verification

The final core sources pass **250 workspace tests**, with one existing ignored
test, **12 optimized lead tests**, strict workspace Clippy, formatting, and both
validator and browser WASM builds. The authored diagnostic example was added
after the workspace test run started; it separately passes strict Clippy and a
release build. All 1,181 frozen inventory hashes and the manifest are unchanged.
[Check logs and source hashes](h6-lead-planner-checks-20261015/checks.json).

The new tests cover line/arc calibration, arbitrary headings and waste sides,
near-zero angle precision, original-job preservation, reversed corner tangents,
small-hole shortening and explicit flags, complete contour accounting, exact
restarted curve attachment, collinear subdivisions, shared-edge exclusions,
invalid inputs, and physically equivalent millimetre/inch jobs. The two property
families each run 64 cases. A real four-part search validates the collision job,
original parts and every allowance, confirms 800 mm² of original placed material,
and writes both SVG and DXF with starts equal to the lead attachments.

## Searched native coupons

[Saved evidence](h6-lead-coupons-20261015T091012Z/preparation.json) contains three
authored MIT jobs, each with four copies and eight contours. Every job was
actually searched for one repeatable work-second, with a 30 s cooperative limit,
seed 0, pinned to CPU 0. Source/binary/runner hashes agree before and after.
All 12 placements and 24 supplied allowances pass independent geometry checks;
no contour is flagged or shortened. No corpus geometry or held-out labels were
opened. These small jobs make no speed or material-efficiency claim.

LightBurn Pro 2.1.01 imported `line45.svg`, `arc45.dxf` and `arc90.svg`. Each native
layer uses 3 mm leads of the named style/angle. The same angle applies to outer
and hole contours in each coupon; these are custom settings, not proof of the
45° outer/90° hole default combination on one native layer. Best-start selection
is off, best-direction selection remains on. LEADIN/C02 and the sheet outline
are output-disabled; no device was connected or fired. In these imports the
orange sheet outline maps to C05, so the native check explicitly disables it.

The three previews show native cutting leads clearing neighbouring parts, with
hole leads inside the holes. Red traversal moves are distinct from black cutting
paths and are not treated as lead collisions. The screenshots record this visual
observation at their displayed scale; they do not numerically reconstruct native
kerf/pierce envelopes. Native saves retain settings and source shapes, not the
computed preview lead paths.

- [Line 45° preview](h6-lead-coupons-20261015T091012Z/line45-preview.png)
- [Arc 45° preview](h6-lead-coupons-20261015T091012Z/arc45-preview.png)
- [Arc 90° preview](h6-lead-coupons-20261015T091012Z/arc90-preview.png)

The independent saved-project audit uses the existing MIT `lbrn2-to-svg` reader,
resolving only shared geometry, transforms and documented omitted zero handles.
It compares contour geometry and start points after removing LightBurn's common
import translation. SVG/DXF are checked separately with svgpathtools/ezdxf.
The first audit stopped because a DXF primitive union is a multipart geometry
without one directed coordinate sequence. That diagnostic is retained; winding
is now reported only for ordered SVG/native contours, while all DXF geometry and
start checks remain required.

The [final geometry audit](h6-lead-coupons-20261015T091012Z/geometry-audit-20261015T092107567923Z.json)
passes all 24 contours in SVG, DXF and native saves. Native starts differ by at
most **0.000002569 mm**. The maximum native contour difference is **0.00245745 mm**
on the round DXF coupon, below the unchanged 0.01 mm threshold. Rectangle
geometry differences stay below 0.000002569 mm.

The hidden display was restored, all ten optimization checkboxes match their
original states, the owned LightBurn process closed, and the desktop lease was
released. Native screenshots and project bytes remain unedited.

## Remaining H6 work

The CLI, MCP and browser controls, reports and end-to-end tests remain pending.
The public pipeline must use original material for all ranking/reporting while
searching the enlarged geometry, handle multi-component units explicitly, and
combine per-copy common-line exclusions with start selection after search.
Full contour coverage and owner/source-curve attachment also need an independent
final report, rather than relying only on planner records. The existing final
allowance checker checks supplied allowances against other parts, other leads
and stock constraints; it exempts the owner and does not prove missing-contour
coverage. Material cost on the common-line development set remains unmeasured.

Native shortened-lead handling and the different default outer/hole angles need
clear user instructions and verification. These three custom-setting coupons
advance the native requirement but do not complete H6 or authorize release.
