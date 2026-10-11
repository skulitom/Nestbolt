# Architecture notes

The decisions in [PLAN.md](PLAN.md) control product scope. This file records the
implementation boundaries and issues found while setting up the repository.

## Shared engine, separate boundaries

`core` owns import/geometry and will own the problem model and search. `cli` handles
files and batch operation. `wasm` calls the same core from a dedicated Worker.
`mcp` handles native stdio and will call the same core for its five tools. No GUI,
filesystem or MCP dependency belongs in the browser-compatible core.

Current inspection deliberately uses serial item/container imports. jagua-rs's BPP
instance helper uses Rayon internally; invoking it blindly in an unthreaded Worker
would complicate the no-SharedArrayBuffer baseline. A compile check is not yet a
browser runtime or responsiveness test. Browser Worker portfolio scheduling is M4.

Pin jagua-rs to crates.io 1.1.0, with `bpp` and `spp`; do not modify dependency files.
Original curves and f64 source geometry will need a separate representation from
the engine's f32 collision polygons to meet the 0.01 mm export fidelity gate.
Upstream BPP JSON is an inspection/interchange format, not our final project format.
It permits unrelated metadata and does not encode all planned Nestbolt constraints.

## Resolve before acceptance benchmarking

**Mixed sheet sizes:** `(sheets - 1) + last_length / sheet_length` compares equal-size
stock sensibly but cannot fairly compare different stock areas. Preserve the stated
metric for equal-stock jobs; define an area-normalised mixed-stock metric and last
sheet choice explicitly before freezing G2. Do not silently change the plan's gate.

**Determinism:** identical seeds with wall-clock termination can execute different
numbers of search steps. Define deterministic work budgets/checkpoints plus a hard
wall-clock cap and report whether the cap truncated the run. Do not claim identical
layouts from a seeded time-limited search until this is specified and tested.

**Independent validation:** jagua-rs 1.1.0 itself now depends on `geo`. Choosing `geo`
again does not automatically create an independent validator. Keep separate source
geometry, transforms and intersection/offset code paths. The new `validator` crate
uses Clipper2 1.2.0 independently, with a working historical strip adapter. See
[VALIDATION.md](VALIDATION.md) for verified scope, precision and remaining M1 work.
Never score from solver density alone.

**Area lower bounds:** `estimate_sheets` must label lower bounds as necessary, not
sufficient, conditions. Grain, spacing, holes, defects, stock mix and oversized parts
can make a job infeasible despite enough total area. Avoid representing an estimate
as a successful layout.

## MCP and distribution

The current rmcp server negotiates a real stdio connection and identifies itself
as an unfinished scaffold. It does not advertise unimplemented tools. Future tools
use file references for geometry, replies below roughly 50 KB, actionable errors,
progress/cancellation and a maximum 300-second search budget. Define the workspace
file boundary and export collision policy before adding filesystem tools.

M4 packages the native CLI/MCP binaries for Windows x64, Linux x64 and macOS arm64,
links the Windows C runtime statically, produces SHA-256 sums and validates MCPB
and MCP Registry metadata. Follow the cited Cutbolt/Inkbolt distribution work and
retain notices for anything reused. The first release and registry publish require
Artem's instruction. Pages deployment follows a tested browser build, not this scaffold.
