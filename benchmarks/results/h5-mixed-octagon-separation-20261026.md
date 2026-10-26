# H5: all-angle mixed cog/bracket separation — 2026-10-26

**Exact source-contained geometry detects all eight demonstrated cog/bracket
collisions, but the strengthened model closes UNKNOWN without a layout.**
H2/H5 remain open at **60%**. This is neither a source witness nor an
unrestricted impossibility proof.

## Source geometry

The earlier all-angle cog disk has quantization-safe radius 109,113 µm. An
eight-vertex integer octagon lies inside that disk: cardinal reach 109,113 µm,
diagonal coordinates 77,154 µm. It therefore lies inside the original cog at
every real rotation. This is source-contained geometry, not the larger virtual
disk used only for cog/cog capacity.

Each of the eight bracket variants has three source-contained component
rectangles. Their Minkowski sums with the reflected octagon produce 24 convex
forbidden polygons, each with 12 integer facets. For relative anchor
`cog - bracket`, strict interior is forbidden; at least one inward facet must
satisfy `nx*dx + ny*dy <= rhs`. Boundary contact is retained as a necessary
relaxation, so passing does not establish the required cutting clearance.

An independent integer support certificate verifies all eight octagon vertices,
24 sums, 288 facets and 9,216 point-sum support checks. It confirms that the
octagon detects all eight physical collision pairs from the complete proxy
assignment. It also covers all 26 previously derived fixed-position bracket
anchor cells, with 1,248 exact corner/facet checks. That fixed-position result
does not exclude layouts where existing parts move.

## All originals remain movable

The new serialized model preserves every original variable/domain and all
5,016 base constraints byte for byte. For each of the eight demonstrated pairs,
it adds separation for all eight bracket variants, both sheets and all three
components. The resulting **384 conditional clauses and 4,608 facet
inequalities** yield **5,217 variables and 10,008 constraints**.

A clause activates only when the bracket selects that variant and both
originals select the same sheet. Each chosen facet enforces its outside
inequality. Inactive cases can set all their facet selectors false. All 66
originals are mandatory; no original coordinate, sheet or mode is fixed.
The prior 609-value necessary assignment is an advisory hint, and the audit
explicitly verifies that the new clauses reject it for all eight pairs. These
eight pairs do not exhaust the source collision checks required for a layout.

The independent reader verifies the entire unchanged prefix, every new Boolean,
halfplane and conditional clause, and each hint. Model SHA-256:
`85aa9db170034348857d51bae18f7db241ff652e149c4048699fc7c4369e6c35`.

## Closed bounded search

One call requests 60 solver seconds within 90 shared seconds, with `fj`
excluded. It returns **UNKNOWN**, with **127,806 branches and 54,245 conflicts**.
Solver time is **60.056504 seconds**, returned solve **60.063253**, shared
process **61.378682**. The small soft overruns are preserved. The independent
response audit checks the saved model, parameters, raw response, log and
process boundary. There is no assignment, native call or quality run.

The call is closed without extension, retry or reseeding. A distinct next
investigation can derive cog-center free regions against all non-cog source
components in the saved arrangement, then apply the proved all-angle cog/cog
separation to locate which existing non-cog poses need coordinated movement.
Any fixed-position obstruction must stay scoped to that arrangement. The
original full-source and material requirements remain unchanged.

## Repository and evidence

At 2026-10-26T21:10:34.243710+00:00, [main 36f162d0 checks](https://github.com/skulitom/Nestbolt/actions/runs/40400314122):
3 of six preceding main checks pass; preserve the remaining live checks before pushing. Production, READMEs and upstream heads/releases are unchanged.
All 22 reserved H2 vectors remain unopened. No new release qualifies.

[Checks](h5-mixed-octagon-separation-20261026/checks.json), [geometry audit](h5-mixed-octagon-separation-20261026/geometry-checks.json),
[model audit](h5-mixed-octagon-separation-20261026/model-checks.json), [response audit](h5-mixed-octagon-separation-20261026/response-checks.json),
[scope](h5-mixed-octagon-separation-20261026/scope.json), [next step](h5-mixed-octagon-separation-20261026/next-step.json) and
[raw manifest](h5-mixed-octagon-separation-20261026/raw-manifest.json). The archive verifies
717 canonical files and 120
identical-content aliases by bytes, SHA-256 and CRC.
