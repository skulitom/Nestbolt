# Closed-contour cleanup checkpoint — 2026-10-13

**H2 remains incomplete; overall milestone completion stays 15%.**

A closed path can double back briefly along a line inserted by gap repair.
Unioning that line with its neighbour moves an endpoint away from its adjoining
arc, breaking the hole. Cleanup now retains those exact retraces with a warning.
For exploded DXF entities, a fallback recovers the original connections only when
the whole original and recleaned drawing closes within the existing 0.005 mm silent
tolerance. It never accepts a partial drawing, enables larger gap repair or
flattens the exported curves. Removed/merged counts include only actual removals.

The authored SVG regression and rotated/mirrored exploded DXF regression preserve
the hole and check curve distance. CLI and MCP retain the hole and expose the
report; Chromium and Firefox show the warning. All 163 workspace tests pass
(one existing ignored test), as do ten browser import tests, strict all-target
Clippy, schemas and the production WASM/web build.

[Real ARC fidelity rerun](h2-fidelity-20261013T210158Z.md): 24 contour comparisons,
zero unmatched; maximum SVG distance **0.000607954 mm**, DXF **0.000000660 mm**.
The [intermediate SVG-only fix](h2-fidelity-20261013T205552Z.md) still failed DXF and
is retained beside the [original full sweep](h2-fidelity-20261013T202338Z.md) and
[authored failing reproduction](h2-closed-backtrack-diagnostic-20261013.json).

[Training import rerun](h2-import-training-20261013T210235Z.json): 246 imports and
11 rejections, with no changed import/count result or layer/colour inventory and
selection mode. Raw count matches remain 245; the [approved R43 exception](h2-r43-scoring-exception-20261013.md)
gives 246 reviewed matches. Maximum time is 0.629 s. The original labels and reports
remain unchanged.

[Robustness rerun](h2-import-robustness-20261013T210319Z.json): 36 imports, 147 clear
rejections, no crash or timeout; maximum 0.820 s. GDAL's robustness-only 3d.dxf now
retains its two closed 2D polylines and still warns about unsupported 3DSOLIDs.
This observation is not a fidelity or complete-3D-import claim.

All runs used CCD0 physical cores with suspended launch/affinity before execution;
builds and tests used CCD1. Product sources remained unchanged. Frozen integrity
verified all 1,181 inventory hashes. No held-out geometry or labels were examined.
The [machine-readable checkpoint](h2-closed-retrace-checkpoint-20261013.json)
records source hashes, report links and validation scope.

Four full-sweep dense Iris timeouts and two thin Gherkin nesting errors remain.
Native projects, warning/selection completeness, 10,000-case fuzzing and sheet
outline support still need work. No full replacement fidelity sweep is claimed.
