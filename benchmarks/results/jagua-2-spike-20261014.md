# jagua-rs 2.0 (main) spike — 2026-10-14

Development triage on the local branch `spike/jagua-2`; not for merge. Nestbolt
was built against unreleased jagua-rs `main` and compared with the current
1.1.0 build. No held-out jobs or final records were used. This makes no
benchmark claim, and the published v1 results, pinned to jagua-rs 1.1.0,
are unchanged.

## What was built

| | Baseline | Spike |
| --- | --- | --- |
| Nestbolt | `6c462c2`, from a clean `git archive` | `6c462c2` plus the port commits on `spike/jagua-2` |
| jagua-rs | 1.1.0 from crates.io (checksum in `Cargo.lock`) | git `main` `9f95e23fdd17` (package 2.0.0, not on crates.io) |
| Sparrow | `4629b22` (git pin) | `4629b22` copied to `spike/sparrow`, ported to the same jagua-rs revision |
| Release binary SHA-256 | `f340ec1c…dbcf` | `9d9dfdc9…f056` |

jagua-rs itself is unmodified. Upstream has no Sparrow port to 2.0 yet; the
last open step of [jagua-rs#125](https://github.com/JeroenGar/jagua-rs/pull/125)
is "update sparrow, then measure". The local Sparrow copy only changes what
the new API forces (below).

## Compile breaks

Everything else in the workspace, including tests, examples, MCP and WASM,
compiles unchanged. The private `Hazard` fields and the removed
`HazardEntity::is_dynamic` do not affect Nestbolt.

| Where | Break | Spike fix |
| --- | --- | --- |
| `crates/core/src/lib.rs:94`, `construct.rs:897` | `CDEConfig` has no `quadtree_depth` or `cd_threshold` | Fields dropped |
| `construct.rs:903`, `sheets/vstrip.rs:157` | `SPSurrogateConfig` has no `n_ff_piers` | Field dropped; every config already used 0 piers, so no behaviour change |
| `sheets/vstrip.rs:148-151` | Aspect-scaled `quadtree_depth` for long virtual strips | Removed; the flat index has no depth to tune |
| Sparrow `config.rs:88-93` | Same three fields in `DEFAULT_SPARROW_CONFIG` (depth 4, threshold 64, 0 piers) | Fields dropped |
| Sparrow `consts.rs:44` | `SvgDrawOptions::quadtree` removed | Field dropped |
| Sparrow `util/assertions.rs:15` | `layout_qt_matches_fresh_qt` renamed | `layout_cde_matches_fresh` |

Twelve errors in total (seven in Nestbolt, five in Sparrow), all mechanical.

## Tests

| Check | 1.1.0 baseline | 2.0 spike |
| --- | --- | --- |
| Debug workspace tests | 237 passed, 1 ignored (242 s of test time) | 236 passed, **1 failed**, 1 ignored (37 s) |
| Release CLI feature tests | 21 passed | 21 passed |
| Release `sparrow_` core tests | 2 passed | 2 passed |
| Strict workspace Clippy | not rerun | passes |
| `nestbolt-wasm` for `wasm32-unknown-unknown` | not rerun | builds |

The debug suite runs about 6.6 times faster on 2.0. Most of that is likely
1.1.0's quadtree debug assertions rebuilding the tree on every change; it says
nothing about release speed, which is measured below.

### The one failure is a latent Sparrow bug, not a 2.0 regression

`native_strip_search_returns_original_geometry_and_units_within_its_envelope`
panics in Sparrow's separator with `weighted loss should never increase: ∞ > NaN`
(`worker.rs:87`, a debug assertion). Sparrow's guided-local-search weights are
multiplied by 1.2-2.0 per iteration while a pair collides and by 0.95 otherwise,
with a floor of 1 and no ceiling, and they survive rollbacks. On this three-square
fixture, compression keeps one pair colliding until its weight passes f32's
maximum (about 3.4e38). Once that pair separates, ∞ × 0 gives NaN.

Instrumented logging showed one pair entry climbing through 1e30-1e36 before
the panic. It is version-independent:

| Debug build, same fixture | Time until the assertion fires |
| --- | --- |
| jagua-rs 1.1.0 + Sparrow `4629b22` | 2.29 s (also fires in a 60 s run) |
| jagua-rs 2.0 + the ported copy | 0.15 s |

The test's budget is 1 s, so 1.1.0 passes only because it is slower. Release
builds compile the assertion out, so an overflow there would carry NaN into
the search unnoticed (inferred, not observed in this spike); our independent
validator still guards validity. Nestbolt's own separator port
has the same uncapped update (`crates/core/src/separate.rs:205-220`, weights kept by
`restore_keep_weights`), but its tracker is rebuilt (weights reset to 1) on
every place, pin and container swap. A faster engine reaches the overflow sooner
in wall-clock mode; in repeatable mode the iteration count is fixed by the work
budget.

## The f32 overlap from the `484ce8b` crash is still missed on 2.0

`a_trial_the_collision_engine_lets_overlap_is_rejected_not_fatal` replays a fixed
76 passes, not a time budget. It passes on 2.0, so pass 75 is still a `rejected`
trial. The new engine lets the same 10.5% overlap through, and Nestbolt's
original-geometry check still catches it. This matches the code: the 2.0 narrow
phase still uses f32 `Edge::collides_with` plus one interior-point containment
test. Keep the typed `Rejected` handling.

## Quadtree-era guards

`CDEngine::register_hazard` in 2.0 no longer requires a hazard inside the
root (there is no `QTHazard::constrict`), and a shape outside the root simply
collides with the exterior.

To test this, the first three guards below were removed together in the spike
tree. The full debug suite gave the same result (236 passed; the only failure
was the Sparrow overflow), including `regression_ci_quadtree_child_edges`.
Five extra `search_fuzz` runs with fresh random cases all passed, as did the
release CLI feature tests (21). The guards were then restored.

| Guard | Written for | On 2.0 | Suggestion |
| --- | --- | --- | --- |
| `separate.rs:536-553`: keep an item in place when a coordinate-descent move leaves the container box, or crosses the root box without an edge inside it | The `QTHazard::constrict` panic ([ci-quadtree-fix](ci-quadtree-fix-20261013.md)) | Not needed for safety | Keep for now: removing it changes which moves are accepted, so trajectories and repeatable results change. Treat removal as a tuning experiment and update the comment. |
| `construct.rs:507-513`: drop zones wholly outside a remnant region | Quadtree roots could not hold outside hazards | Not needed; such zones cannot block a placement inside the region | Keep (fewer index entries); update the comment |
| `sheets/vstrip.rs:137-141`: skip defects beyond the shortened last sheet | A jagua-rs debug assertion | Not needed for safety; the first reason (cannot block a part) still holds | Keep; drop the quadtree half of the comment |
| `sheets/vstrip.rs:457-470`: move a dropped sheet's parts onto the new last sheet before swapping containers | "Every hazard must lie inside the smaller container's quadtree" | Not tested separately. Parts left outside the new container would still be infeasible, so the move is still needed. | Keep; update the comment |

## Speed and results (development triage)

Twelve development B/M jobs (no held-out jobs), `nestbolt sheets`. Each job ran
both binaries at the same time, each pinned to its own physical CCD0 core, with
four job pairs at once. Every layout was re-checked with the standalone
`validate` command, which has no jagua-rs dependency. **All 72 layouts are
valid.**

### Repeatable budget (20 work-seconds, seed 0)

The same job, seed and work budget give the same layout only while every
collision answer is identical.

| Job | Material 1.1.0 | Material 2.0 | Same layout | Real s 1.1.0 | Real s 2.0 | Speed-up |
| --- | ---: | ---: | :---: | ---: | ---: | ---: |
| b-albano-strip-sheet | 1.73334 | 1.71349 | no | 8.20 | 5.31 | 1.54x |
| b-jakobs1-strip-sheet | 0.74123 | 0.74123 | yes | 2.70 | 2.02 | 1.34x |
| b-swim-strip-sheet | 1.61245 | 1.61245 | yes | 8.37 | 6.56 | 1.28x |
| b-shirts-nest-mb-free | 6.99995 | 7.09925 | no | 8.06 | 5.81 | 1.39x |
| b-trousers-strip-sheet | 2.20294 | 2.20276 | no | 9.37 | 6.04 | 1.55x |
| b-marques-strip-sheet | 1.03849 | 1.03849 | yes | 7.62 | 5.13 | 1.48x |
| b-fu-nest-mb-given | 3.42868 | 3.42868 | no | 6.45 | 3.70 | 1.74x |
| m-garment-bruce-1 | 0.20497 | 0.20497 | yes | 2.56 | 1.68 | 1.53x |
| m-mechanical-batch-1000 | 1.09448 | 1.09448 | yes | 6.53 | 3.29 | 1.98x |
| m-box-mini | 0.66600 | 0.66600 | yes | 5.84 | 3.03 | 1.92x |
| m-sign-1 | 0.77149 | 0.77149 | yes | 4.30 | 2.96 | 1.45x |
| m-mechanical-defective-stock | 2.75454 | 2.75454 | yes | 9.50 | 5.32 | 1.79x |

All 24 runs finished their work before the real-time limit and are reported as
repeatable. Lower material is better.

Eight of twelve layouts are byte-identical, so for those jobs 2.0 is a pure
speed-up: the same work in a median 1.50 times less real time. Four jobs diverge.
The likely cause is collection order (2.0 documents it as unspecified), which
changes which hazards an early-stopping evaluation counts. This has not been
traced. A port would change repeatable results for some jobs.

### Wall clock (20 s, seeds 0 and 1)

"Evals/s" is Nestbolt's own separator evaluations per real second. "Sparrow"
marks runs that handed the job to the pinned Sparrow optimiser, whose
evaluations Nestbolt does not count.

| Job | Seed | Material 1.1.0 | Material 2.0 | Evals/s 1.1.0 | Evals/s 2.0 | Ratio |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| b-albano-strip-sheet | 0 | 1.71312 | 1.67695 | 345,915 | 582,855 | 1.68x |
| b-albano-strip-sheet | 1 | 1.73761 | 1.69593 | 346,790 | 546,196 | 1.58x |
| b-fu-nest-mb-given | 0 | 3.42860 | 3.42858 | 489,601 | 843,438 | 1.72x |
| b-fu-nest-mb-given | 1 | 3.42859 | 3.42858 | 466,040 | 792,616 | 1.70x |
| b-jakobs1-strip-sheet | 0 | 0.72512 | 0.70024 | Sparrow | Sparrow | — |
| b-jakobs1-strip-sheet | 1 | 0.72562 | 0.72548 | Sparrow | Sparrow | — |
| b-marques-strip-sheet | 0 | 1.03867 | 0.99395 | 242,117 | Sparrow | — |
| b-marques-strip-sheet | 1 | 1.03861 | 1.03848 | 216,640 | 367,578 | 1.70x |
| b-shirts-nest-mb-free | 0 | 6.90900 | 6.84496 | 213,702 | 378,514 | 1.77x |
| b-shirts-nest-mb-free | 1 | 6.86964 | 6.86002 | 234,488 | 391,044 | 1.67x |
| b-swim-strip-sheet | 0 | 1.58052 | 1.58047 | 255,665 | 337,581 | 1.32x |
| b-swim-strip-sheet | 1 | 1.62853 | 1.59678 | 263,435 | 345,064 | 1.31x |
| b-trousers-strip-sheet | 0 | 2.08864 | 2.20254 | 297,264 | 445,578 | 1.50x |
| b-trousers-strip-sheet | 1 | 2.12122 | 2.09244 | 259,482 | 469,377 | 1.81x |
| m-box-mini | 0 | 0.66600 | 0.66600 | 198,940 | 400,758 | 2.01x |
| m-box-mini | 1 | 0.66600 | 0.66600 | 188,746 | 380,413 | 2.02x |
| m-garment-bruce-1 | 0 | 0.19975 | 0.19945 | Sparrow | Sparrow | — |
| m-garment-bruce-1 | 1 | 0.19634 | 0.19523 | Sparrow | Sparrow | — |
| m-mechanical-batch-1000 | 0 | 1.03192 | 1.02524 | 64,771 | 167,513 | 2.59x |
| m-mechanical-batch-1000 | 1 | 1.03107 | 1.02521 | 53,641 | 126,549 | 2.36x |
| m-mechanical-defective-stock | 0 | 2.70070 | 2.66703 | 82,582 | 162,920 | 1.97x |
| m-mechanical-defective-stock | 1 | 2.67852 | 2.66535 | 68,641 | 170,938 | 2.49x |
| m-sign-1 | 0 | 0.72617 | 0.72029 | 140,890 | 213,892 | 1.52x |
| m-sign-1 | 1 | 0.72114 | 0.72135 | 131,980 | 199,027 | 1.51x |

Wall-clock runs are not repeatable, so the same jobs and seeds were also run
with two byte-identical copies of the 1.1.0 binary, using the same pairing and
cores.

| | 1.1.0 vs 2.0 | 1.1.0 vs 1.1.0 (noise control) |
| --- | --- | --- |
| Valid layouts | 48/48 | 48/48 |
| Median separator evals/s ratio (comparable pairs) | **1.70x** (1.31-2.59, n = 19) | 1.01x (0.83-1.10, n = 20) |
| Second binary lower / tied / higher material | **20 / 2 / 2** | 8 / 5 / 11 |
| Median material change | **-0.53%** | +0.00% |
| Median absolute change | 0.57% | 0.02% |
| Largest single change | +5.45% (trousers, seed 0) | +1.19% (trousers, seed 1) |

The direction and size are well outside the control's spread. With two seeds
and 20 s, this is a signal worth a proper run, not a result. One outcome
changed sheet count: marques seed 0 handed off to Sparrow on 2.0 and got a
valid one-sheet layout (0.99395), while 1.1.0 stayed on the separator with two
sheets. Its earlier development records keep a two-sheet fallback because
Sparrow's exactly touching layouts failed the single-precision check. Seed 1
kept two sheets on both. The jobs delegated to Sparrow (jakobs1, bruce-1)
also used less material in all four runs (-0.02% to -3.43%), consistent with
Sparrow doing more work in the same time.

## What a real port needs

1. Wait for jagua-rs 2.0.0 on crates.io and a Sparrow release ported to it,
   then re-pin both together. The workspace, the Sparrow delegation and the
   pinned Sparrow comparator all share one engine.
2. Cap or renormalise the guided-search weights in `separate.rs` (and report
   the Sparrow equivalent upstream). This is independent of 2.0, but 2.0 reaches
   it sooner.
3. Keep the f32 `Rejected` handling. The quadtree guards can stay or be
   simplified (table above); none is required for safety on 2.0.
4. The work coefficients (`nestbolt-work-v2`) were fitted on 1.1.0. With 2.0
   the same work takes about two-thirds of the real time, and some trajectories
   change, so a port is a work-model version bump.
5. Any new quality claim needs a new final run with a fresh held-out set, with
   the Sparrow comparator on the same engine.

Raw rows, hashes and logs: [jagua-2-spike-20261014.json](jagua-2-spike-20261014.json).
