# H2 training imports and exported cut geometry

The CLI at `bf9eaa62` accepted 291 of the 313 frozen training drawings. The other 22 returned their recorded repair instructions. This replay covers the merged DXF block and SVG unit and point-list fixes. The [summary](summary.json) records the counts and archive checksums. The [measurements](measurements.zip) contain the eight per-file reports.

| Inputs | Result |
| --- | --- |
| 257 training vectors | 245 imports matched the frozen part and hole counts directly. One matched the approved R43 expectation of a plate with 37 holes. All 246 accepted drawings matched the cut-layer and warning checks. The other 11 gave actionable errors. |
| 56 native training projects | All 45 accepted libraries matched the archived JSON, including original LightBurn XML and warnings. The other 11 reproduced the archived error text and wrote no partial library. |
| 183 robustness vectors | 36 imported and 147 returned errors. Every process finished within 0.837 seconds against a 10-second limit. |

The R43 check verified the source, label and manifest hashes before applying the reviewed count. The training native comparison used the [reviewed native archive](../h2-native-warning-probe-20261016-v3/archive-integrity.json). [R43 scoring decision](../h2-r43-scoring-exception-20261013.md)

## Cutting files

All 246 accepted vector drawings nested and passed layout validation. The G6 round trip compared 5,138 contours across 246 SVG and 246 DXF sheets. Each outer contour and hole had a distinct match. Maximum distances were 0.003302 mm for SVG and 0.000500 mm for DXF, within the 0.01 mm limit.

A second SVG reader parsed the saved paths with svgpathtools. It reconstructed the imported source curves from the saved library, applied each recorded placement and the sheet's Y reflection, and compared the contours with Shapely after subdividing curves at 0.0005 mm. It checked physical page dimensions, verified the black CUT stroke on each path and matched contours one-to-one within each part. Across 411 placements and 2,569 contours the largest measured distance was 0.003302 mm. The same reader also passed the [previously saved training exports](../h2-fidelity-20261120T124440Z.md). Controls rejected a missing hole, a duplicated hole, a deformation inside an unchanged bounding box, wrong page dimensions and a path that overrode its black group's stroke with red. [SVG reader](../../../scripts/h2_svg_audit.py), [regression controls](../../../scripts/test_h2_svg_audit.py)

ezdxf independently read 91,537 entities across the 246 DXF sheets. All declared millimetres and the expected layer colours. The reader found zero audit errors, repairs or zero-length lines. [DXF reader](../../../scripts/h2_dxf_audit.py)

## Reproduction

Build the release CLI and the core `fidelity` example using the locked dependencies. The Windows training and robustness runners use four physical cores. Use the shop Python environment for the independent file readers.

1. Run `scripts/h2_import_audit.py` for training, then with `--robustness`. Run `scripts/h2_fidelity.py` for training cut files and retain its output directory.
2. Run `scripts/h2_warning_audit.py TRAINING.json --fidelity FIDELITY.json` on the two new reports.
3. Run `scripts/h2_svg_audit.py FIDELITY.json --out svg-reader.json` and `scripts/h2_dxf_audit.py FIDELITY.json --out dxf-reader.json`. Both accept `--work-dir` if the exported sheets have moved.
4. From the repository root, run the [native training replay](replay_native.py) with `--cli target/release/nestbolt.exe --out native-training.json`.

**H2 remains open.** These measurements cover training and robustness inputs. The three completed native held-out evaluations and the 22 reserved vectors retain their prior status under the [held-out gate decision](../h2-gate-decision-20261020.md).
