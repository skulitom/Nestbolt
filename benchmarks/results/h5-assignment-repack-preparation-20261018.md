# Fixed return-assignment repack preparation — 2026-10-18

The first attempted exchange in each of the four saved capacity cases is fixed
before new searching: two large-plate assignments of 21 parts and two panel
assignments of 103 parts. Both kerfs are retained. All four restore through the
original full-job model with **exact saved f32 container and collision polygons**
and allowed orientations. No rescaling, new clearance or reduced part count.

An isolated diagnostic entry passes 90 optimized core tests, strict lint and
build. Existing source differs only in exposing the module and adding the new
entry module; 146 other original files and production are unchanged. Four
malformed reconstruction inputs are rejected. The independent audit accepts an
analytic two-part layout, also validated by the public CLI, and rejects five
invalid membership, geometry, boundary or orientation cases.

After committing the plan, run four serial searches on physical CCD0 CPU 8,
seed zero, with at most six ten-second rounds each: saved positions first, then
up to five full random restarts. Stop at the first separator-clear snapshot.
Every round and failure is retained; this diagnostic does not change the short
repair budget in production or claim a quality improvement. Packaging/checks
run on CCD1. Each final snapshot is independently checked against the unchanged
shortened collision boundary and original filled outer rings, kerf, quantities,
orientations and full-stock public validation.

A verified layout proves that particular fixed assignment can fit. Failure of
this finite search proves neither infeasibility nor a need to relax H5. Any
future repair change still requires its own qualification and unchanged matched
quality gates. H2/H5 remain open at 60%; no reserved input is opened.
