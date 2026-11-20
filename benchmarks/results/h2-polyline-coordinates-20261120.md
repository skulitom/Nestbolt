# Legacy DXF polylines inside a block

The shared importer now keeps a 3D `POLYLINE` in world coordinates before
applying its enclosing block's transform. A 2D `POLYLINE` still follows its
object coordinate system. This extends Pedro Rangel's negative-extrusion fixes
to flat drawings stored with the legacy 3D polyline flag. See the
[upstream DXF fixes](https://github.com/skulitom/Nestbolt/pull/22) and
[Autodesk's vertex coordinate convention](https://help.autodesk.com/cloudhelp/2024/ENU/AutoCAD-DXF/files/GUID-0741E831-599E-4CBF-91E1-8ADBCFD6556D.htm).

A regression fixture stores the same triangle twice in a block translated by
(100, 50) mm. Both polylines specify downward extrusion. Before the fix, one
triangle landed on the other and duplicate removal returned only one part.
The corrected importer returns two triangles of 15 mm² each.

| Source entity | Minimum XY (mm) | Maximum XY (mm) |
| --- | --- | --- |
| 2D polyline | (85, 52) | (90, 58) |
| 3D polyline | (110, 52) | (115, 58) |

An independent ezdxf R2007 file gave the same results. Its reader transformed
each polyline's world vertices by the stored INSERT matrix. The release CLI,
stdio MCP `import_parts` and compiled WebAssembly `import_files_with_options`
returned identical part geometry. The locked Rust workspace test suite passed.

The [257 training vectors](h2-import-training-20261120T123836Z.json) produced
246 imports and 11 rejections. Every per-file result, including reported cut
layers, warnings and part/hole counts, matches the October training run after
excluding elapsed time. The existing R43 decision accounts for the one raw
count mismatch. The [183 robustness files](h2-import-robustness-20261120T123849Z.json)
produced 36 imports and 147 rejections. All statuses matched October. Three
previously rejected extrusion examples returned updated diagnostic details.
The slowest file took 0.782 seconds. Both runs selected only development inputs.

The [frozen H2 decision](h2-gate-decision-20261020.md) still applies. Its
maximum exact-import score is 23 of 25 against a 95% requirement.
