# H2 requirement review — 2026-10-16

**The training evidence accounts for all 313 labelled training files. H2 remains
open on reserved evaluation and the pending denominator clarification.** This
review binds the saved results to the preview's source changes; it does not
claim another import, timing, fidelity or native desktop measurement.

[Machine review](h2-requirements-review-20261016/checks.json) at `0a9fb44`:
257 vector files and 56 native projects. There are 291 accepted libraries and
22 original clear rejections. The accepted vector count includes the approved,
exact-hash [R43 scoring exception](h2-r43-scoring-exception-20261013.md); its
original label, split and failed raw comparison remain unchanged.

| Requirement | Evidence and boundary |
| --- | --- |
| Training parts, holes and cut selection | [Complete vector review](h2-habits-checkpoint-20261014.md): 245 raw exact matches plus the one approved exception; eleven named repairs/rejections. [Native H3 review](h3-complete-20261015.md) supplies membership, physical cutting holes, layers and fixed-shape checks. The [latest native audit](native-diagnostics-surfaces-20261016.md) retains all 45 accepted training libraries' non-warning fields exactly and all eleven original errors exactly. Rejections are accounted for, not counted as imported geometry. |
| Messages and no silently missing selected parts | [Vector warning/cut-layer audit](h2-warning-audit-20261014T015958Z.md) covers all 246 imports and eleven actionable rejections. [Native explanations](native-diagnostics-surfaces-20261016.md) cover all 56 training originals, including rectangle proxies, cached text, missing controls, fixed artwork and repair instructions. No new exception is applied to the independently reviewed Gherkin retrace. |
| Robustness | [Retained run](h2-import-robustness-20261014T015959Z.json): 183 files, 36 imports and 147 rejections, no crash or timeout, maximum 1.275 seconds against ten seconds. This is the original timing record, not a new preview timing claim. |
| Habit properties | [Seeded property run](h2-habit-fuzz-20261014T015256Z.md): 10,000 importer cases plus 1,008 nesting cases, zero failures, all 17 generator habits covered in each fixed-seed batch. Original saved failures/regressions remain. The preview adds the exact CI curve regression and passes all current workspace tests; it does not relabel the historical 10,000 cases as rerun. |
| Vector fidelity | [Full sweep](h2-fidelity-20261014T012836Z.md): all 246 importable files, 5,138 matched contours, maximum SVG 0.003301680 mm and DXF 0.000499980 mm against 0.01 mm. [Public replay](h2-export-replay-20261015.md) confirms identical imported geometry, valid saved layouts and 492 exports; 491 are byte-identical. The remaining byte comparison stays failed, with a separate geometric bound of 0.000491918 mm that passes the original fidelity limit. |
| Native fidelity | [H3 evidence](h3-complete-20261015.md): all originals preserve byte-identical no-op output; independently checked diagnostic sheet transforms and the native project searches preserve original contents/settings. Approved text repairs are auxiliary inputs, not rewritten originals. L42's native layer normalization and original failure remain explicit. New native warnings preserve every accepted training library's non-warning fields; the preserving writer is unchanged. |
| LightBurn sizes and colours | [Five DXF/five SVG native imports](h2-lightburn-20261013T195848Z.md) retain saved geometry within 0.000033 mm, with CUT/COMMON/LEADIN/SHEET on C00/C01/C02/T1. Eight numeric UI sizes match after rounding; two spline width fields differ by 0.003275 mm while their saved curves retain the expected width within 0.000002 mm. That display limitation remains; this review does not claim ten exact UI-field matches or change the gate. |
| UI, CLI and MCP | [Integrated preview checks](preview-integration-20261016.md): 302 workspace tests, 27 optimized CLI tests and 86 enabled Chromium/Firefox tests pass, including actual stdio MCP imports and the new messages in saved projects. Earlier [gap](h2-gap-checkpoint-20261013.md), [selection](h2-layer-checkpoint-20261013.md), [encoding](h2-encoding-checkpoint-20261013.md), [cleanup](h2-cleanup-checkpoint-20261013.md) and [stock-outline](h2-sheet-checkpoint-20261013.md) surface checks remain linked. |
| Reserved acceptance | The three native projects passed their once-only H3 evaluation. Their saved summary is reused without reopening drawings or labels. Twenty-two reserved vectors remain unevaluated. Two frozen negative fixtures cap the literal whole-population maximum at 23/25, or 92%, against the unchanged 95% requirement. The existing clarification remains pending; no denominator, split or outcome is changed. |

## Applicability to the preview

The only product source changes since vector replay commit `465f994` are the
hole index and four native-import files. All ordinary SVG/DXF reader and exporter
files, the preserving LightBurn writer, public CLI/MCP/WASM adapters and validator
sources are unchanged. Every third-party Cargo lock record is identical; the five
local package versions changed to `0.2.0-alpha.1`.

The current complete core source equals the candidate used in the latest
56-project native audit. Its changed reader code adds explanations, and the
public importer removes a duplicate message concatenation. Exact comparison of
all non-warning library fields establishes that those diagnostic changes retain
the training geometry. The hole-index change affects search and is undergoing
its separate current-build performance confirmation.

These source and data comparisons support retaining the earlier training
evidence. They do not turn it into newly measured preview timing or extend any
result to unevaluated reserved inputs. Original failures, limits, reviewed
exceptions and published v1 numbers remain intact. H2 stays open and overall
completed milestone weight remains **45%**.
