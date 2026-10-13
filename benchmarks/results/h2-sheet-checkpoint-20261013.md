# Imported sheet-outline checkpoint — 2026-10-13

**H2 remains incomplete; completed milestone progress is 15%.**

The part library now offers stock outlines separately from cut parts. It detects
`SHEET` by default; UI stock-layer checkboxes, CLI `--sheet-layers` and MCP
`sheet_layers` support other layers or disabled discovery. Stock geometry and IDs
remain in the library, with size summaries in the CLI and bounded MCP replies. A request sheet can use
`from_import` without copying polygons or specifying dimensions. The shared core
resolves that ID for nesting, validation, export and estimation.

The browser can use an offered outline for any sheet size. Its remnant-file picker
now prefers SHEET over CUT and refuses to guess between multiple separate stock
outlines. The stock and its own holes move together to the lower-left origin.
Curved stock reserves its approximation error at edges in addition to the part
error. Self-touch repairs that could expand usable stock are refused.

[Ten frozen training pre-arranged nests](h2-sheets-20261013T212538Z.md) pass: stock
sizes and boundaries match their independently authored labels, expected cut-part
and hole counts remain intact, and the availability warning is present. Maximum
stock boundary distance is 0 mm. No held-out geometry or labels
were examined. The initial ten-case check also passed and is retained.

[Training import rerun](h2-import-training-20261013T212539Z.json): 246 imports,
11 rejections; all previous import/count results are unchanged. Raw count matches
remain 245; the approved R43 exception gives 246 reviewed matches. Maximum time is
0.614 s. [Robustness](h2-import-robustness-20261013T212547Z.json):
36 imports, 147 rejections, no crash or timeout; maximum 0.845 s.
Runs used CCD0 physical cores, affinity before execution and unchanged source,
binary and runner hashes. Builds/tests used CCD1. All 1,181 frozen inventory
hashes verify.

Validation: the workspace suite passed 168 tests with one existing ignored test.
The final five-test stock suite adds a self-touch rejection check; the final CLI
check covers explicit stock layers, disabled discovery, nesting and independent
validation. Both pass. The MCP session nests and validates against an imported
custom-layer stock with a hole. Sixteen Chromium/Firefox checks pass, including
custom stock selection, original remnant import and pre-arranged nest import.
Strict Clippy, schemas and native/WASM/web builds pass. The
[machine-readable checkpoint](h2-sheet-checkpoint-20261013.json) records exact
scope and the corrected test/launch mistakes.

The four dense fidelity timeouts and two thin-shape nesting errors remain;
warning completeness, 10,000-case fuzzing, native projects and the held-out
scoring question still need work. This checkpoint does not claim H2 acceptance.
