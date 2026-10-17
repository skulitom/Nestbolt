# Authored larger-return-set witness — 2026-10-17

The independent Clipper2 validator accepts both hand-built layouts with five
parts, unchanged stock/spacing/rotations and **13,300 mm² material**. A 2,550 mm²
incoming rectangle exchanges with three 900 mm² squares: 2,700 mm² combined.
The returned set retains its relative arrangement and fits within the same
charged last-sheet height. No optimizer or quality measurement runs here.

This shows that a smaller combined return area is a heuristic, not a required
consequence of the unchanged geometry/material guard. It does not prove that
any rejected development proposal is feasible or that accepting more proposals
improves search. The [four diagnostic traces](h5-obstruction-stage-diagnosis-20261017.md)
separately show that all 620 observed multi-blocker samples are filtered out by
that heuristic, leaving only partial exchanges.

The first authored orientation preserved width but increased charged height;
its equality assertion failed correctly (18,800 → 19,700 mm²). Both valid
layouts, reports and the failed assumption remain preserved. The second case
transposes the authored geometry and placement coordinates to test the actual
height metric. This is an explicit separate example, not a rescored benchmark.

[Review](h5-area-witness-20261017/review.json),
[passing checks](h5-area-witness-20261017/height-preserving/checks.json),
[all file hashes](h5-area-witness-20261017/integrity.json).
No product change, reserved geometry, integration or H5 closure; completion 60%.
