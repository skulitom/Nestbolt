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

**Mixed sheet sizes:** [SCORING.md](SCORING.md) defines the area-normalised extension
and last-sheet choice, preserving the exact stated metric for equal rectangular
stock. The independent job validator implements it. Search still prioritises the
fewest sheets; G2 still measures material rather than sheet count alone.

**Determinism:** [SEARCH_CONTRACT.md](SEARCH_CONTRACT.md) separates repeatable work
quotas from explicit wall-clock benchmark mode. Hard timeouts cannot masquerade
as completed repeatable results. Calibration, implementation and repeated-run
acceptance tests remain M2/M4 work. The first constructor uses a fixed sample
quota and an explicit integer random stream; repeated native trials match exactly.
Repacking uses fixed passes and seeds; the versioned time-to-work mapping is pending.

## First M2 constructor

`core::construct` now uses unmodified jagua collision trees to place parts on
fixed and mixed sheets with stock limits. Single-component holes are reserved;
multipart pieces use one f64 convex hull before conversion to a collision proxy.
Every output refers back to the original part and one rigid transform. Exact
allowed f64 angles are retained on export instead of round-tripping f32 trig.

Remnant islands share a physical sheet identity and stock count, each with its own
collision region. Defects and margins are blocking zones. The first pass uses the
larger of edge and part gaps plus a scale-dependent rounding guard, so it can be
more restrictive than requested. It does not claim infeasibility after failing to
place a part. Search must later recover those lost options and reduce sheet usage.

Constructor v2 anchors candidates to actual inset sheet/margin bounds, not the
square quadtree root. It compensates jagua's 0.1-radian inscribed offset joins by
dividing the requested guarded separation by cos(0.05), and nudges contact
candidates by the scale-dependent rounding guard. A narrow-sheet regression with
zero random samples and an exact-angle clearance regression cover these cases.

Constructor v3 first tests an interior-circle surrogate before full polygons;
all 30 retained maker layouts are exactly equal to v2, with cheaper rejection.
`core::optimize` reuses prepared geometry, changes part order deterministically,
and periodically attempts one fewer sheet. Independent validation accepts an
improvement only if it beats the incumbent under the declared all/fill objective.
Incomplete capped trials have no score. Progress reports every pass. Fixed passes
are an experimental work quota; calibrated deadlines and cancellation are pending.

The optional refinement stage makes bounded translations from a feasible
placement, using progressively smaller steps and several downward slopes. It
keeps the exact rotation/reflection and reconstructs each source translation from
the actual f32 displacement, avoiding accumulated proxy/source drift. Repacking
first compares this refined construction against the original incumbent with the
same order and seed, then compares a contact-candidate construction. Contact
candidates align bounding corners and sampled convex/concave vertices of the
inflated outlines; every candidate still passes the collision tree. A separate
random stream preserves the ordinary placement quota, and cached anchors bound
the cost for large contours. Later passes alternate translation/contact search
with other orders and attempts at one fewer sheet. Orders alternate between
whole part types and individual copies; a complete unique `(part, copy)`
permutation prevents duplicates or missing quantities. Both choices use fixed
integer shuffles and are recorded in per-pass progress.
Failed/incomplete trials are recorded without a score. This is still constructive
repacking; overlap repair and neighbourhood moves across existing sheets remain.

For this bootstrap, core consumes the polygon contract from the validator crate.
The checker is called for source preflight and final acceptance, never to choose
placements. Search intersections stay in jagua; final intersections stay in
Clipper2. Extract shared data types when introducing the public curve/project
model. No upstream dependency was modified and no Deepnest code was copied.

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
