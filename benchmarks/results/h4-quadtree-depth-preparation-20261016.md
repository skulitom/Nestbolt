# Isolated collision-tree depth preparation — 2026-10-16

**All eight preparation stages pass. No quality or speed gain is claimed.**

The current preview's [CPU profiles](h4-browser-profile-20261016T040030Z.md)
put edge collection and quadrant traversal at 46.5–75.7% of sampled time.
This isolated candidate lowers only the separator-window base quadtree depth
from four to three. Aspect scaling, leaf threshold, original outlines,
independent validation, score arithmetic, work coefficients, budgets, public
options and dependencies are unchanged. Fewer tree visits may cost more leaf
work. Hazard traversal order may change; fixed-work byte identity is not assumed.

The copy uses its own Cargo target. All 196 baseline files retain their hashes;
only `crates/core/src/sheets/vstrip.rs` differs in the candidate. Production is
unchanged. Format, 75 optimized core tests, strict core lint, native build, WASM
build, bindings, TypeScript and browser bundle pass on CCD1. This preparation
has not run measured searches or read held-out geometry.

[Preparation](h4-quadtree-depth-preparation-20261016/preparation.json),
[build results](h4-quadtree-depth-preparation-20261016/build.json),
[exact source/build archive](h4-quadtree-depth-preparation-20261016/raw.zip),
[member verification](h4-quadtree-depth-preparation-20261016/integrity.json).
The archive retains both source copies, exact executable/WASM/site, all logs
and preparation helpers. CRC, every size and every SHA-256 are verified.

The next single-use pilot fixes all 11 declared development jobs, seeds 0–2,
60 seconds, native/Chrome/Firefox and at most eight physical CCD0 cores.
All 99 attempts must validate independently. Original +1% median and +5% job
limits remain unchanged. It starts only after both previous measured sessions
are terminal and sealed. A pilot cannot complete H4 or establish release readiness;
full quality/native comparisons, scale and current packaging checks remain.
The failed preview and rejected common-line candidate remain preserved.
Completed milestone weight stays 45%.
