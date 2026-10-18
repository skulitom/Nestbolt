# Exact boundary-copy selection diagnosis — 2026-10-18

**19 of 19 attempts select at least one actual part defining the credited sheet height; 0 select every part defining that height. 1 of the first group and 0 of the second group are accepted.**

Two serial panel-hardware diagnostics retain both kerfs, seed zero,
60 seconds and physical CCD0 CPU 8. The separately qualified observer
changes no decision, budget or work charge. Logging may alter wall
trajectories; these observations are not a quality or speed comparison.

Both final layouts and 2 saved baselines independently validate.
All original quantities, archive/member hashes and source guards pass. The
filled-outer audit checks 31,794 same-sheet pairs at the unchanged
1e-7 mm tolerance. A separate rectangular-stock calculation reproduces
every saved baseline material value exactly. Every observed choice matches
unique physical members of that validated baseline exactly; no approximate
pose matching or part-family inference identifies the boundary copies.
The session takes 2.035 minutes.

| Kerf mm | Invocation | All attempts | Any actual top copy | Every top copy | Accepted with any / every |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.2 | 0 | 7 | 7 | 0 | 1 / 0 |
| 1.5 | 0 | 12 | 12 | 0 | 0 / 0 |

| Outcome | All attempts | Any actual top copy | Every top copy |
| --- | ---: | ---: | ---: |
| accepted | 1 | 1 | 0 |
| source_repair_or_expiry | 18 | 18 | 0 |

The combined source-repair-or-expiry outcome preserves the original
short-circuit condition; it does not distinguish repair failure from the
remaining deadline. Accepted exchanges still pass full validation and the
original material guard. Acceptance counts do not prove final quality.

The boundary ordering reaches a real height-setting copy on every attempt, but the generated pair lists never include both height-setting inserts together. The current pair generators use nearest-neighbour partners before applying their caps. The next isolated hypothesis is to include the two highest-ranked source members as the first pair in the appropriate same-item or mixed-item list, remove an equivalent duplicate, and retain the six-plus-six caps and existing nearby alternatives within those caps. Preserve original pair anchor order, allowed orientations, all repair/deadline/work limits and every full acceptance check. Authored cases must fail under the current selection when closer lower neighbours displace the upper pair, then pass for same-item and mixed-item boundary pairs, without duplicates or cap overruns. All existing 126 tests and public/rejection checks must remain. Only then prepare a matched quality pilot. This is a proposal-coverage hypothesis: it does not prove that jointly moving those copies is feasible, necessary for every improvement or sufficient to meet H5. Eighteen repair-or-expiry stops also remain unexplained by this selection result. The six failed pilot material comparisons remain authoritative.

[Committed plan](h5-boundary-observer-20261018/plan.json),
[archive verification](h5-boundary-observer-20261018/verification.json),
[independent geometry and exact copy coverage](h5-boundary-observer-20261018/layout-checks.json),
[all observed attempts](h5-boundary-observer-20261018/observed-exchanges.json).

Production, reserved inputs, release assets and README claims remain
unchanged. **H2/H5 remain open; completed milestone weight is 60%.**
