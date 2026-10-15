# LightBurn groups and separate cutting files — 2026-10-15

Artem chose separate SVG/DXF cutting files alongside the preserved editable
LightBurn project ([plan decision 4](../../docs/PLAN_V1_1.md#10-reviewed-decisions)).
That workflow now works through the browser, CLI and MCP. It advances N5;
**H6 remains open and completed milestone weight remains 15%.**

## Source paths and preservation

Original cutting curves are reconstructed from the retained XML. Each rigid
unit can contain disconnected outer contours, holes and nested islands. Full
containment determines nesting parity; winding is preserved. Every closed
contour receives a checked allowance or an explicit flag. Open cuts retain their
original path and receive a manual-attention flag without a new start or lead.
Engraving, cached engraving text and image bounds remain protected artwork and
never become CUT paths. Search footprints continue to protect the complete
original unit, including its conservative collision geometry.

The independent validator now distinguishes material boundaries from original
cutting paths. Cutting-path coverage comes from those paths, which can differ
from the collision proxy. It checks open-path continuity and requires a flag;
an attached allowance on an open cut is rejected. Protected artwork participates
in owner clearance. Ordinary material components must still be disjoint.

Default exports with leads enabled contain `<name>-sheet-<k>.lbrn2`,
`<name>-sheet-<k>-cuts.svg` and `.dxf`. The LBRN2 output is byte-identical to the
existing preserving export for the same placements without leads. Child content,
starts and cut settings are unchanged. Cutting files contain checked starts and
LEADIN review paths. Their default sheet outline is off; LBRN2 retains its default
T1 outline. Browser downloads and ZIPs follow the same filenames and content.
An explicit CLI/MCP format still selects that format.

## Native evidence

The authored MIT fixture contains one rigid group: a rectangular outer, its
rectangular hole, a nested island, a disconnected ellipse, an open cut and a
small engraving. A Tool rectangle stays fixed. A public CLI search places two
copies on one 150 × 100 mm sheet with 0.2 mm kerf, one repeatable work-second,
seed 0 and a 30 s real-time limit. It uses CPU 0. Its ten original cutting
contours produce **eight reservations and two open-cut flags**. Fresh validation
and repeat export match, and the LBRN2 file equals a no-lead preserving export.
[Preparation and hashes](h6-lead-group-20261015T115904Z/search/preparation.json).

LightBurn Pro 2.1.01 opened and saved the original fixture, the actual nested
LBRN2 and both cutting files. The unmodified MIT `lbrn2-to-svg@0.5.3` reader,
with the documented test-only group/compact-path normalization, supplies native
geometry independently of Nestbolt's reader. Thirty contour comparisons pass;
each output preserves eight closed paths and two open paths. The native cut
settings in the preserved project exactly equal its native original baseline.

| Native output | Maximum contour difference | Maximum checked start difference |
| --- | ---: | ---: |
| Preserved LBRN2 | 0.000000000000029 mm | Starts retained by the preserving byte comparison |
| Cutting SVG | 0.001819 mm | 0.000002000 mm |
| Cutting DXF | 0.000008422 mm | 0.000002237 mm |

All are below 0.01 mm. Sixteen closed-contour starts are checked across SVG/DXF;
open-cut geometry and endpoints are checked without claiming a lead attachment.
LightBurn translates imported cutting files to the workspace center; a single
translation is recorded for each import, with no per-contour alignment.
The preserved native project needs no translation correction.
[CPU 0 audit](h6-lead-group-20261015T115904Z/native-audit-20261015T121808910588Z.json).

These checks verify native import, saved geometry and starts. Red paths in the
screenshots are the exported review paths; **this session did not generate new
native leads or inspect a new cutting preview**. The earlier mixed-angle native
lead evidence remains separate. No device was connected or used. Owned windows
were closed, the hidden display restored and the desktop lease released.

## Verification and retained failures

The full workspace passes **278 tests**, with one existing ignored test, and
all **23 optimized CLI tests** pass. Ten focused Chromium/Firefox cases pass
across the first eight successes and the corrected two-case rerun. Production
WASM/browser build, browser type checks, strict lint, formatting and generated
schemas pass. Tests cover rigid transforms, reflection, island/hole topology,
unchanged editable children, exclusion of text/images/engraving, independent
source counts, open-cut rejection, repeated public exports and ZIP contents.

The initial new browser test used a non-iterable NodeList in this project's
TypeScript configuration; `Array.from` fixes it. Its next assertion mistook the
two deliberately flagged open cuts (styled with `.error`) for a failed search.
The corrected test checks actual alert roles and explicitly requires both flags.
The original logs and page snapshots remain. Early fixture construction errors
and an accidental native selection flip, immediately undone and independently
verified, are recorded in [development failures](h6-lead-group-20261015T115904Z/development-failures.json).
The first native audit passed without pinned affinity; the recorded CPU 0 rerun
confirms the same numbers. Neither is a performance measurement.

[Logs, source hashes and artifact inventory](h6-lead-group-20261015T115904Z/checks.json)
pin the checkpoint. Builds and tests use CPU 16–31. The frozen integrity check
verifies all **1,181 files** and the unchanged manifest; held-out access is hashes
only. The earlier line/arc native-tested layouts also pass fresh validation and
export with identical plans, bounds and CUT attributes.

## Remaining scope

This completes the implemented multipart lead workflow and its authored public
and native export checks. It does not complete H6's allowance-cost comparison on
the common-line development set or the remaining overall acceptance evidence.
Native common-line cutting remains unsupported; ordinary common-line analysis
explicitly requires a single outer component instead of interpreting additional
outer components as holes. Uncached text and mixed fixed/active groups keep their
existing import limitations and unresolved plan decisions. No frozen labels,
split, published v1 results or gate thresholds changed.
