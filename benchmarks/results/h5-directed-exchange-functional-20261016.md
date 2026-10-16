# Directed common-line exchange: isolated functional evidence

The isolated candidate passes six focused tests, 80 core unit tests (one existing
ignored test), six common-line geometry tests, strict lint for the library and
common-line integration target, and eight authored public-CLI checks.
**This is not a packing comparison or an H5 pass.** The release candidate and
all active H4 source, executable, site and input guards remain unchanged.

The candidate is based on `0a9fb440560bf96f5a81bd05e3f50d7df01238b3`. It changes only `sheets.rs`,
`sheets/vstrip.rs` and the new `sheets/vstrip/exchange.rs` in an isolated workspace.
It is not integrated into production. Builds and functional checks used CCD1
(logical CPUs 16–31), outside the active measurement's CCD0 lanes.

## Operation and constraints

From a feasible stalled window, try inserting a last-sheet part into one of
three earlier receivers. Proposals identify actual collision hazards and reject
static hazards. A smaller blocking part returns to the last sheet. At most six
proposals are retained per receiver; receiver and source repairs share bounded
slices of the existing relocation allowance. The source keeps its current
shortened boundary. Failed repairs leave the original separator untouched.

Before accepting an exchange, the complete job, including frozen sheets, passes
the independent validator with no increase in material area or sheet count.
The operation reserves check time, charges deterministic work, respects rotation
and reflection rules, and keeps the existing independently valid incumbent.
It is enabled only when the caller reserves part holes; ordinary part-in-hole
search keeps its existing path. No gate, tolerance, default or frozen input changes.

The six focused tests cover eleven authored scenarios: seven successful
exchanges and four refusals/no-ops. They check a smaller actual obstruction,
seeds 0–4, a frozen sheet and allowed reflection, stock defects, expired/disabled
calls, larger return parts and an impossible source repair. Frozen-sheet
placements and failed-call state compare exactly in the same internal frame.
The complete original geometry, counts and material are independently checked.

The public checks use a newly authored frame/insert/bracket job and fixed work
budgets, seeds 0 and 1. Ordinary baseline and candidate layout, job, SVG and DXF
bytes match exactly; both retain twelve hole riders. Candidate common-line
replays also match those files exactly and report zero hole riders. All eight
layouts pass the unchanged production validator. These are functional and
repeatability checks, not wall-clock quality or speed measurements.

## Retained failures and scope

- Initial compile errors involved flag scope, method visibility and a Rust
  borrow; the same first failure was captured before repair.
- The first test build lacked the existing compile-time validation example;
  its unchanged tracked bytes were added to the isolated workspace.
- Two initial assertions compared authored f64 coordinates with the pre-existing
  f32 frame conversion. They now compare the exact state before and after this
  operation in the same frame, with no widened numeric tolerance.
- The first defect fixture requested an unsupported relation between edge and
  part clearance. The fixture now uses the supported equal-clearance case.
- Two broad lint attempts lacked unrelated compile-time examples/development
  fixtures. Their failures remain. The final strict lint scope is explicitly the
  library and common-line target; this report does not claim a full workspace lint.

All original logs, source snapshots, public inputs/results, helpers, final source
tree and both executables are in the verified archive. The existing production
workspace checks remain separate evidence.

The next decision requires a committed, equal-budget development comparison
against the unchanged preview binary after H4 quality and scale release the
measurement cores. Include both failed mechanical jobs, both kerfs, all three
development seeds and controls; keep every outcome. Do not infer that this
authored success fixes the retained +1% material failures. H5 remains open and
completed milestone weight remains 45%.

Baseline CLI SHA-256: `41a0e9c75b320572cf0e229061cbedde23e0f10259b98081f8c2da761404df3c`. Candidate CLI:
`668181ff4b3ec6d589c7222fd2bdcd0a7e99b0d8ef7c7e6374ec3982ce286356`. Raw archive: 292 members,
5,436,999 bytes, SHA-256 `724145500bb28d419034d95f9027d692f210d2198cd87e03ddcaafd85a62c77a`; CRC and every member
hash were checked. [Checks](h5-directed-exchange-functional-20261016/checks.json)
and [archive inventory](h5-directed-exchange-functional-20261016/integrity.json).
