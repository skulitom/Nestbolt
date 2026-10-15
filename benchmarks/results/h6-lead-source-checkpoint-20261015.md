# Independent lead source validation — 2026-10-15

Final lead validation now independently derives contour coverage, evaluates
attachments on original curves, and checks each lead against its own material.
The shared finalization path applies this to CLI, MCP and browser validation and
SVG/DXF export. This advances N5; H6 remains open and completed milestone weight
remains **15%**.

## What the checker establishes

The validator accepts original job/layout data, original curve definitions,
analytic lead paths with source segment/parameter attachments, and explicit
flags. It does not accept the planner's expected contour count or flattened
owner geometry. Contours are enumerated from each original component and its
holes, once per placed copy. A contour needs exactly one reservation or a
nonempty flag. Missing decisions invalidate the report; unknown, duplicate or
ambiguous decisions are errors. Flags describe unresolved contours, not safe
leads.

The separate source implementation evaluates line, quadratic, cubic and rotated
elliptical-arc segments. Bézier attachment evaluation uses Bernstein polynomials;
subdivision bounds chord error using the control hull. Ellipse subdivision uses
a second-derivative bound. Flattening tolerance is 0.0001 mm; attachment tolerance
is 0.000008 mm. Invalid/disconnected/open curves and excessive subdivision fail
explicitly. Each contour is bounded to fewer than 10,000 segments and at most
10,000 flattened points including its seam.

Rebuilt original material is used for both owner and neighbour checks. Owner
checks permit the ordinary half-kerf boundary cut, but reject an inward
centreline, a deeper stroke or a pierce in material. Existing independent
footprint construction checks other leads, stock edges, margins, remnants and
defects. Complete reports expose `source_checked: true` and independent coverage
counts; the partial footprint-only API explicitly reports `false` and `null`.
Reported useful area still comes from the original job, while actual reserved
space controls offcut/material accounting.

## Retained failure and containment repair

The mixed line/cubic/quadratic/arc integration fixture initially failed before
the new final check: polygon-union intersection rounding omitted
**0.000000001010 mm²** of original material. Canonical collision polygons are
now reconstructed and checked before use. If containment fails, one existing
two-grid outward margin (0.000002 mm) is tried, followed by the same strict
zero-outside-area check. There is no accepted missing-area tolerance. A separate
regression rejects an envelope missing a 0.001 mm strip.

An initial inch-property assertion also used squared job units where the
established metric contract uses mm². Correcting that test did not change
production metrics. Its failing seed remains checked in. Both observations and
the initial fixture compilation corrections are retained in
[development failures](h6-lead-source-20261015T112252Z/development-failures.json).

## Verification

The full workspace passes **272 tests**, with one existing ignored test. All
**22 optimized CLI tests** and **four focused Chromium/Firefox cases** pass.
Production WASM/browser builds, browser type checks, strict lint, formatting and
generated schemas also pass. The new checks include omitted/duplicate/unknown decisions, detached
or altered attachments, inward leads, curved neighbours extending beyond their
search polygons, multi-component/hole coverage, subdivision bounds, collinear
backtracking, and randomized Bézier/ellipse/units/rotation/reflection cases.
The core mixed-curve fixture uses reflection and rotation in both mm and inches.

[Command results, source hashes and logs](h6-lead-source-20261015T112252Z/checks.json)
record these checks. Builds and tests use CPU 16–31; standalone retained-layout
validation/export uses CPU 0. The first frozen-integrity command used the system
Python, which lacked `ezdxf` and stopped during import. The retained rerun uses
the existing shop environment and verifies all **1,181 files** and the unchanged
frozen manifest hash. Held-out access was hashes only.

Both line and arc settings pass [fresh standalone validation/export](h6-lead-source-20261015T112252Z/recheck/checks.json)
on the retained actual searched layout used by the
[mixed-settings native check](h6-lead-settings-checkpoint-20261015.md). Each covers
six contours: four reservations and two explicit flags. Every per-copy plan,
length, start, path and bound equals the earlier native-tested report, and all
CUT SVG attributes are unchanged. Original input hashes are rechecked. This
reuses native evidence without claiming another native session, solver benchmark,
material-cost comparison or final acceptance run.

## Scope

This validates supplied analytic paths against original source geometry; it
does not independently infer lead style/settings or replace native evidence.
Export start/end checks remain covered by the existing ordered-export and
public surface tests. The validator can enumerate multiple components, while
the public planner still explicitly rejects multi-component rigid units.
Multipart planning and the required common-line-set allowance-cost comparison
remain unfinished. No published v1 result, frozen label, split or gate threshold
has changed.
