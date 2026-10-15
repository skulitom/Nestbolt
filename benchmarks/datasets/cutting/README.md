# H5/H6 development jobs

Frozen before the first material-cost run. The manifest references exactly the
eight maker jobs named in PLAN_V1_1.md and adds five authored jobs of rectangles
and brackets. It excludes every held-out maker job. Original maker files and
their frozen manifest remain unchanged.

The five new jobs are copyright 2026 Nestbolt contributors, MIT, under the root
LICENSE. Existing maker attribution is in `benchmarks/makers/sources.json` and
its referenced notices. Boxes-generated drawings have the upstream FAQ's output
permission; no GPL source code is reused.

`scripts/cutting_development_set.py` creates the set once and refuses to replace
it. The public library adapter represents every frozen polygon ring as exact
line segments with zero flattening tolerance, preserving holes, quantities,
rotations, mirrors, stock, margins and defects. Each run verifies the generated
job equals its original apart from the requested 0.2 or 1.5 mm clearance.

For H6, paired arms both use common-line mode with its search bonus off. The
only difference is default line lead allowances: 3 mm, 45° outer, 90° holes.
This measures the allowance's material cost in a common-line job. It does not
measure H5's optional search bonus or change the v1 quality baseline.

The full protocol is 60 wall-clock seconds, development seeds 0–2, both kerfs,
all 13 jobs and both arms. A short pilot verifies the harness first. Invalid
and timed-out outcomes are retained without a score; all flagged contours are
reported. Use the ratio of per-arm seed medians for each job/kerf pair. A final
report must state incomplete pairs and may not imply flags are solved.
