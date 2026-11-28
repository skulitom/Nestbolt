# Status — 2026-11-27

This page is the current state in one screen. Every dated checkpoint, failed
trial and superseded result up to 2026-11-20 is kept unchanged in the
[status history](STATUS_HISTORY.md); every benchmark run is in
[BENCHMARKS.md](../BENCHMARKS.md).

## At a glance

| | State |
| --- | --- |
| v1 (fixed-sheet nesting) | **Accepted** on 2026-10-13. Final run: 8.5% less material at the median at 60 s; the 60-second win-rate bar was missed |
| v1.1 (real shop files) | **75% of milestone weight.** Five of six gates complete; import acceptance (H2) stays open |
| Stable release | [v0.1.0](https://github.com/skulitom/Nestbolt/releases/tag/v0.1.0), 2026-10-14, also on the MCP Registry |
| Preview release | [v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1), 2026-10-16 |
| `main` | Ahead of the preview; see [what is on main](#on-main-since-the-preview). The [hosted browser app](https://skulitom.github.io/Nestbolt/) is built from `main` |

Progress counts completed milestone weights only. The published benchmark
figures belong to the frozen build `75cbb32`; nothing on `main` makes a new
comparison against other tools. A new claim needs a new final run with a fresh
held-out set and fresh seeds.

## v1.1 — real shop files

[Plan](PLAN_V1_1.md) · [milestone weights](PLAN_V1_1.md#7-milestones-progress-weights)

| Gate | Weight | State | Evidence |
| --- | ---: | --- | --- |
| H1 — messy-file corpus | 15% | Complete | [Frozen corpus and split](../benchmarks/results/h1-freeze-20261013.md): 534 inputs, 338 labels, 25 files held out |
| H2 — import robustness | 25% | **Open** | [Training results and reader checks](../benchmarks/results/h2-training-exports-20261120/README.md), [gate decision](../benchmarks/results/h2-gate-decision-20261020.md) |
| H3 — LightBurn round-trip | 25% | Complete | [Full requirement review](../benchmarks/results/h3-complete-20261015.md) |
| H4 — curve-heavy parts in the browser | 15% | Complete | [Completion evidence](../benchmarks/results/h4-depth-complete-20261016.md) |
| H5 — common-line cutting | 15% | Complete | [13-job confirmation](../benchmarks/results/h5-rigid-host-rows-20261120.md) |
| H6 — lead-in allowances | 5% | Complete | [Gate evidence and material costs](../benchmarks/results/h6-complete-20261015.md) |

**H2 is open by decision.** The gate needs exact imports on at least 95% of the
25 held-out files, which is 24 files. Two of the 25 are deliberate negatives,
so the frozen labels cap the count at 23 (92%). On 2026-10-20 Artem chose to
keep the gate as written ([reviewed decision 8](PLAN_V1_1.md#10-reviewed-decisions)),
so H2 earns no completion credit. Three held-out LightBurn projects have been
evaluated once; the other 22 files remain reserved.

What the importer does on the files it may be tuned on, as of `bf9eaa62`
(2026-11-20):

- all 313 training files reproduce their reviewed outcomes: 291 imports and 22
  rejections that name the repair;
- every exported contour re-imports within 0.01 mm (largest distance
  0.003302 mm), checked with independent SVG and DXF readers;
- all 183 robustness files import or fail clearly within 0.837 s.

**H5 passed with two options enabled:** *Nest parts inside holes* and *Search
for more shared cuts*. The 13-job development comparison saved a median 13.031%
of cutting distance at 0.2 mm kerf and 13.101% at 1.5 mm. All 234 layouts
validated, and every job stayed within +1% material of ordinary nesting.
Common-line mode still reserves holes by default.

## On main since the preview

None of this is in a tagged release yet.

- **Engine:** moved to jagua-rs 2.0.0 and Sparrow `73c02f65`
  ([#52](https://github.com/skulitom/Nestbolt/pull/52)). At 60 seconds over
  three development seeds, the ported build used less material than the
  previous `main` on 43 of 65 jobs and more on 16; the median change was
  -0.20%. All 390 layouts validated. jagua-rs 2.0.0 removes short edges from
  its own collision outlines, which left no margin at corners when spacing
  was near zero; the separation now covers it, and rejected constructor
  trials fell from up to eight per run to none in 8,640. The repeatable work
  clock is `nestbolt-work-v5`. Browser performance and the common-line
  comparison have not been rerun on this engine.
  [Runs, margins and calibration](../benchmarks/results/jagua-2-port-20261127.md)
- **Common-line cutting** completed its gate
  ([#27](https://github.com/skulitom/Nestbolt/pull/27)).
- **DXF import:** binary DXF and every `$INSUNITS` unit
  ([#41](https://github.com/skulitom/Nestbolt/pull/41)), −Z extrusion, MINSERT
  and paper-space handling ([#22](https://github.com/skulitom/Nestbolt/pull/22)),
  listed layers that are off or frozen
  ([#39](https://github.com/skulitom/Nestbolt/pull/39),
  [#48](https://github.com/skulitom/Nestbolt/pull/48)), truncated binary files
  reported as such ([#47](https://github.com/skulitom/Nestbolt/pull/47)).
- **SVG import:** cutouts drawn with explicit units or compact point lists
  ([#29](https://github.com/skulitom/Nestbolt/pull/29),
  [#30](https://github.com/skulitom/Nestbolt/pull/30)).
- **Import diagnostics as data:** structured warnings
  ([#26](https://github.com/skulitom/Nestbolt/pull/26)) and the report returned
  with an import that finds no part
  ([#44](https://github.com/skulitom/Nestbolt/pull/44)).
- **Larger jobs:** up to 10,000 parts
  ([#42](https://github.com/skulitom/Nestbolt/pull/42)), an indexed clearance
  validator and repeatable budgets recalibrated as `nestbolt-work-v4`
  ([#50](https://github.com/skulitom/Nestbolt/pull/50)).
- **Free rotation:** parts that fit only between quarter turns are placed, and
  parts that fit no sheet are named
  ([#40](https://github.com/skulitom/Nestbolt/pull/40)); an interrupted search
  keeps its typed error ([#46](https://github.com/skulitom/Nestbolt/pull/46)).
- **Shop workflow:** offcut and remnant export that re-imports as stock, job
  quotes from exact curve lengths, and a client for LightBurn's local REST API
  ([#50](https://github.com/skulitom/Nestbolt/pull/50)).
- **Library use:** drawing import and export build without the nesting engines
  ([#25](https://github.com/skulitom/Nestbolt/pull/25)); a small pinned checkout
  is [documented](../CONTRIBUTING.md#use-the-rust-crates-from-a-small-checkout)
  ([#28](https://github.com/skulitom/Nestbolt/pull/28)).

## Open work

- **H2** stays open as described above.
- **Crate distribution**
  ([#13](https://github.com/skulitom/Nestbolt/issues/13)): the crates are not on
  crates.io. `nestbolt-core` depends on Sparrow from Git, which crates.io does
  not accept; `nestbolt-validator` has no such dependency.
- **Next stable release:** the preview is the newest tagged build. Releases and
  registry publication happen only on Artem's instruction.

## v1 — accepted

Closed on Artem's acceptance on 2026-10-13
([plan decision 5](PLAN.md#9-decisions-artem-2026-10-11-and-later)). The
[final acceptance run](https://skulitom.github.io/Nestbolt/results/) used build
`75cbb32`, seeds 1000–1004 and ten held-out maker jobs.

| Gate | Result |
| --- | --- |
| G1 — every layout valid | Met: 375/375 at 60 s, 60/60 at 300 s, 60/60 at 30 s, 65/65 strips |
| G2 — less material than the best competitor, 60 s | **Not met as written.** Median 8.52%, but 48 of 56 wins or ties (85.7% against the 90% required) and two jobs more than 1% worse. Every loss is against Sparrow, seven of the eight on one-sheet jobs |
| G2 — 300 s | Met: median 9.61%, 11 of 11, worst +0.84% |
| G3 — strip parity with Sparrow | Met: median −0.002%, worst +0.72% |
| G4 — speed | Met: 10 of 11 |
| G5 — browser quality and scale | Met |
| G6 — export fidelity and opening | Met |
| G7 — real MCP client | Met |
| G8 — one-command reproduction | Met |

The milestone table, per-gate evidence and the first final build that crashed
on one job are in the [status history](STATUS_HISTORY.md#v1--accepted).
