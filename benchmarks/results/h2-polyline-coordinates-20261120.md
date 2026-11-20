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
Uploading the file through the production web build in Chrome showed two
separate parts, each with quantity one.

The [257 training vectors](h2-import-training-20261120T123836Z.json) produced
246 imports and 11 rejections. Every per-file result, including reported cut
layers, warnings and part/hole counts, matches the October training run after
excluding elapsed time. The existing R43 decision accounts for the one raw
count mismatch. The [183 robustness files](h2-import-robustness-20261120T123849Z.json)
produced 36 imports and 147 rejections. All statuses matched October. Three
previously rejected extrusion examples returned updated diagnostic details.
The slowest file took 0.782 seconds. Both runs selected only development inputs.

All 246 imported training files nested and passed independent layout validation.
All 5,138 contours matched one-to-one on SVG and DXF re-import. The maximum
distance was 0.003302 mm for SVG and 0.000500 mm for DXF against a 0.01 mm
limit. The separate warning audit verified the expected diagnostics and cut
layers in all 246 imports and the repair instructions for all 11 rejections.
See the [fidelity measurements](h2-fidelity-20261120T124440Z.md) and
[training warning audit](h2-warning-audit-20261120T130512Z.md).

An independent ezdxf 1.4.4 audit of the 246 exported sheets read 91,537
entities. Every drawing used R2007, millimetres and the expected four layer
colours. The reader reported zero errors, repairs or zero-length lines.
The [per-sheet audit](h2-dxf-structure-20261120.json) records each file hash,
entity counts and actual layer colours. To replay it, run
`scripts/h2_dxf_audit.py` with the fidelity JSON and `--out` from the shop
Python environment. Supply `--work-dir` if the generated sheets have moved.

The [frozen H2 decision](h2-gate-decision-20261020.md) still applies. Its
maximum exact-import score is 23 of 25 against a 95% requirement.

## Paper-space block instances

A separate R2007 drawing written with ezdxf contains the same nested block
once in model space and once in Layout1. Each instance references a 10 × 8 mm
rectangle on the CUT layer. The previous CLI returned two parts. The updated
CLI, MCP and WebAssembly each return the model-space rectangle with bounds
(22, 34) to (32, 42) mm and report the skipped title-block instance. The Rust
regression reproduces the original two-part failure.

All 246 successful [training imports](h2-import-training-20261120T131255Z.json)
and 36 successful [robustness imports](h2-import-robustness-20261120T131324Z.json)
produced byte-identical libraries before and after this fix. Every file kept
its import or rejection status. Two previously rejected real DXFs now report
fewer open contours after their drawing-layout instances are excluded. The
counts dropped from 54 to 45 for `api-cw750-details.dxf` and from six to three
for `byblock-bylayer.dxf`.
