# Exchange path diagnostic — 2026-10-16

**Neither diagnostic reached the exchange call.** Both outputs validate.
These are two separately planned, debug-enabled observations of the unchanged
candidate, not repeat quality attempts or a speed comparison. The original
[72-attempt pilot](h5-exchange-pilot-v2-20261016.md) remains unchanged.

Existing timers record separator work in both mechanical jobs; panel-hardware
also records ordinary relocation. Neither contains an `exchange` timer.
That timer surrounds the call even when it returns without a proposal, so
its absence identifies a call-path issue on these observed trajectories.
Source inspection places exchange only after three consecutive failed
separation returns, while ordinary relocation also has an earlier opportunity.
A separation call may consume the remaining exploration budget. This does
not prove exchange unreachable on every job or seed.

Keep this candidate unintegrated. A future isolated experiment can test the
existing bounded initial relocation opportunity while preserving the whole
search deadline, independent acceptance and failed incumbent. H5 still needs
its original material and cutting conditions; neither limit changes.

The committed plan uses kerf 0.2 mm, seed 0, 60 seconds, physical CCD0 CPUs
8/10 and `NESTBOLT_DEBUG=1` in the two child processes only. All source/input/
binary guards pass; the parent and original pilot have no environment override.
Both saved layouts independently validate with identical metrics.

[Results and exact timers](h5-exchange-path-20261016/results.json),
[verification](h5-exchange-path-20261016/verification.json),
[fixed plan](h5-exchange-path-20261016/plan.json).

The verified raw archive retains 28 members, 86,153 bytes,
SHA-256 `1efce6bca92e82d124afd95157f965554487566cace211b58c490428b5ed81a4`. CRC, every member size and hash were checked.
All original logs and outputs remain preserved. No milestone is completed.
