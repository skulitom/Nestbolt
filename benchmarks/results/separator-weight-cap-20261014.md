# Separator weight ceiling — 2026-10-14

The separator's guided-local-search update (`crates/core/src/separate.rs`, from
Sparrow 0.3.0) multiplied colliding entries' weights by 1.2–2.0 per iteration
and decayed the others by 0.95, with a floor of 1 and no ceiling. Weights
survive rollbacks within one `separate()` call. A pair that collides on enough
consecutive iterations overflows f32 to `∞`, and `∞ × 0.95` stays `∞`. Every
overlap with that partner then evaluates to the same `∞` until the tracker is
rebuilt. Found during the [jagua-rs 2.0 spike](jagua-2-spike-20261014.md),
where upstream Sparrow's own debug assertion fires on the same rule.

## Change

`MAX_WEIGHT = 1e20` caps the update (`clamp(1.0, MAX_WEIGHT)`). With at most 64
poles per surrogate, a loss is below `80·d²` for parts of diameter `d` (under
1e10 at 10 m in millimetres), so weighted losses and their sums stay far below
`f32::MAX`. The new unit test
`separate::tests::weights_stay_finite_when_a_collision_never_clears` traps two
sheet-sized squares in one sheet. Without the cap it fails in 0.16 s with
`weight overflowed: inf`; with the cap the weight sits exactly at `MAX_WEIGHT`.

## How large weights get

All 65 development B/M jobs (no held-out jobs), `nestbolt sheets --repeatable`,
60 work-seconds, seed 0, run with a temporary stderr probe of the largest weight
(the search itself unchanged). One process per physical CCD0 core.

| Largest weight reached | Jobs |
| --- | ---: |
| below 1e2 | 55 |
| 1e2 to 1e5 | 6 |
| 1e5 to 1e20 | 3 (fu-nest-mb-free 1.4e12, blaz1-nest-mb-free 1.3e15, fu-nest-mb-given 1.1e16) |
| above 1e20 | 1 (blaz1-nest-mb-given 1.1e34) |

At 300 work-seconds (CCD1, 97–151 s real), all four multi-bin blaz1/fu jobs
reach `∞`, and both blaz1 jobs also overflow a weighted loss. The final
acceptance build `75cbb32` used the same update, and its 300 s wall-clock runs
did more work than this. Its records for these four jobs therefore very likely
include stretches of search with infinite weights. Validity was never affected,
and no final record was rerun or used here.

## Effect on repeatable results

| Run | Identical layouts | Changed |
| --- | ---: | --- |
| 65 development jobs, 60 work-seconds | 64 | blaz1-nest-mb-given: 9.6670624 → 9.6668741 material, 10 sheets both |
| four multi-bin jobs, 300 work-seconds | 0 | blaz1-free +0.0006%, blaz1-given −0.0001%, fu-free +0.0001%, fu-given +0.0002% material; same sheet counts |

All 138 layouts pass the standalone validator, and every run finished its work
before the real-time limit. Only runs whose weights pass 1e20 change, and on one
seed the material effect is negligible. This is a robustness fix, not a quality
gain. `WORK_VERSION` stays `nestbolt-work-v2`: no coefficient changed, and the
[search contract](../../docs/SEARCH_CONTRACT.md) scopes repeatability to the same
build.

Upstream report drafted, not posted:
[docs/upstream-drafts/sparrow-gls-weight-overflow.md](../../docs/upstream-drafts/sparrow-gls-weight-overflow.md).
Its reproduction uses Sparrow `4629b22`'s own debug CLI: three 2×2 squares at
strip height 5, `-t 60 -s 0`, panic after 20–30 s.

[Rows, binary hashes and probe lines](separator-weight-cap-20261014.json).
