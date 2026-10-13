# N1 explicit gap repair checkpoint — 2026-10-13

**H2 is not complete. Overall milestone completion remains 15%.**

The importer now separates the fixed 0.005 mm silent join threshold from curve
precision. Explicit gap repair accepts 0–1 mm and records the source, endpoints
and measured size of each larger bridge. Original curve endpoints are retained.
Remaining open paths report their endpoints and a repair suggestion. Library
reports persist the structured result; UI, CLI, MCP and WebAssembly use the same
options. Reapplying UI options replaces the previous file's parts and messages.

Validation:

- `cargo test --workspace`: passed; one pre-existing ignored Sparrow debug test.
- Four focused core gap tests and the CLI gap import test passed.
- MCP stdio import/repair/nest/export test passed. The first test harness expected
  a tool-result error flag; the server correctly returned an MCP error instead.
  The assertion was corrected to inspect that error; no product fix was needed.
- WebAssembly and production web build passed; schema generation passed.
- Chromium and Firefox UI gap/reimport tests: 2/2 passed.
- Frozen corpus integrity: all 1,181 inventoried files unchanged.
- [Generated gap diagnostic](h2-import-training-gap-checkpoint-20261013T182707Z.json):
  30/30 imported and matched part/hole counts at the labelled repair settings.
  Layer/colour flags were explicitly omitted and recorded as unavailable for
  this checkpoint; this is not layer or fidelity acceptance.

The [first diagnostic attempt](h2-import-training-20261013T182647Z.json) retained
30 CLI argument rejections because the labels also request `--layers`, which is
not implemented yet. The corrected diagnostic above exercises only gap repair.
Both attempts used the same executable and sources; no held-out geometry or
labels were read. Runs used four distinct CCD0 physical cores, one process each,
with ten-second limits; builds used CCD1.

Remaining H2 work includes layer/colour selection and inventories, duplicate and
overlap cleanup, units and block handling, existing-sheet selection, palette
exports, full labelled fidelity and actionable-failure checks, 10,000 generated
property cases, robustness recheck and native LightBurn checks. The frozen
held-out scoring clarification remains pending; neither its split nor labels
have changed. N2–N5 and H3–H6 remain incomplete.
