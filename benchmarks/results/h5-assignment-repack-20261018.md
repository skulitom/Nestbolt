# Fixed return-assignment feasibility repacking — 2026-10-18

**Three of four fixed source assignments now have independently valid packings.**
Both 21-part large-plate cases and the 103-part panel case at 0.2 mm kerf fit
the exact original shortened boundaries. The 103-part panel case at 1.5 mm
kerf remains unresolved after all six recorded rounds.

| Saved assignment | Kerf mm | Parts | Rounds | Independent result | Successful repair seconds |
| --- | ---: | ---: | ---: | --- | ---: |
| m-mechanical-large-plates | 0.2 | 21 | 1 | Valid source packing | 1.048544 |
| m-mechanical-large-plates | 1.5 | 21 | 1 | Valid source packing | 2.291579 |
| m-mechanical-panel-hardware | 0.2 | 103 | 1 | Valid source packing | 6.155242 |
| m-mechanical-panel-hardware | 1.5 | 103 | 6 | Unresolved; all six rounds fail | — |

The complete four-case session took 72.078 seconds. Each
case followed the committed seed-zero, serial CPU8 plan: saved positions
first, then up to five full random restarts, each round bounded by a ten-second
deadline within sixty seconds total. All three successes came from the first
warm round; the unresolved case retained its warm failure and all five random
failures. Observed round durations include a small deadline-check overrun.
These are diagnostic durations, not a quality comparison or proof of minimum
necessary repair time. Different search trajectories can behave differently.

All four inputs first restored through the unchanged original full-job model
with exact saved f32 collision polygons and container vertices. Independent
Shapely checks then verified membership, unchanged shortened boundary, no
collision-polygon overlap/outside area, original allowed orientations and
reflection, filled-outer separation and kerf. The three public subset layouts
also pass the original CLI validator, including all quantities. Successful
minimum original kerf slack is 0.012918, 0.013573 and 0.009903 mm respectively.
Every unsuccessful round is retained with its failed independent and CLI checks.

[The independent audit](h5-assignment-repack-20261018/independent-audit.json)
links all nine rounds; [verification](h5-assignment-repack-20261018/verification.json)
binds the four immutable original archives and input/source/binary guards.
This proves feasibility of those three source assignments only. It neither
proves whole-job material improvement nor makes the fourth assignment impossible.

A read-only [inventory/container analysis](h5-assignment-repack-20261018/repeated-assignments.json)
finds 8 distinct assignments across the earlier 25 attempts, with **17 repeats
after the first occurrence within the same exchange invocation**. Identical
original item indices and counts identify interchangeable copies; unstable
snapshot placement keys are excluded. This motivates testing retained repair
progress for compatible repeated assignments while keeping the original
shared budget, acceptance checks and rollback. It is not measured reuse or
evidence of a speed/quality gain. Stale collision-tracker keys must never be
carried into a reconstructed layout.

Production remains unchanged. Any repair-state reuse needs authored safety
checks and the original matched quality gate before integration. **H2/H5
remain open; completion stays 60%.**
