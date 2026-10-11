# Current Sparrow comparator

This is separate from the historical M0 reproduction. It calls the unmodified
Sparrow 0.3.0 public API at revision
[`4629b227`](https://github.com/JeroenGar/sparrow/tree/4629b22795ae6b25b3b460ccde6fb36a71292b6d).
The source is an exact Git dependency; its transitive dependencies retain the
current CLI smoke lock's versions. Sparrow's MIT licence and dependency notices,
including jagua-rs's MPL-2.0 terms, are retained here. No solver source is changed.

```powershell
python scripts/sparrow_benchmark.py build
python scripts/sparrow_benchmark.py run --job benchmarks/datasets/S/s-fu-strip.json --seconds 60 --seed 0 --axis x
python scripts/sparrow_benchmark.py run --job benchmarks/fixtures/sparrow-edge-gap.json --seconds 5 --axis y
```

The upstream command's time limit covers its exploration and compression phases
after constructing an initial layout. For equal-budget comparisons this wrapper
starts its deadline before polygon import and construction. The public termination
hook caps both phases at that deadline. The solution listener retains only feasible,
improving candidates received before the deadline; late final callbacks cannot
replace them. An outer watchdog handles uninterruptible construction. Parsing the
input JSON precedes the solve clock, like the browser comparators' source import.
One separator worker and `RAYON_NUM_THREADS=1` are explicit. A wall-clock budget
and seed do not promise identical layouts across runs.

Two provisional settings are available: `identical` disables upstream conservative
polygon simplification and narrow-concavity closure; `upstream-default` retains
both defaults. Both preserve original spacing, quantities and orientation rules.
Neither is yet declared the best setting. The wrapper shares the CLI's optimiser,
default search parameters and 90/10 exploration/compression split, subject to the
common deadline. Source/build/compiler hashes, all accepted native candidates,
the original job and independent validation report are retained for each attempt.

The adapter accepts a single rectangular stock type and all-parts jobs. Axis X
preserves the strip convention; axis Y rotates the entire problem rigidly so the
strip length follows the sheet offcut metric. Margins and independent edge spacing
are expressed by the virtual strip and inverse origin. Reflections are converted
through that rotation. Holed/disconnected parts, defects, remnants and mixed stock
are explicitly unsupported; they are never replaced by easier shapes. A native
strip that exceeds the fixed sheet is invalid for that sheet and has no material
score. These failed fits remain visible in the records.

Every candidate returned to the common contract is checked against original
polygons by the independent Clipper2 validator. Set S's score is then the maximum
transformed original X coordinate, not the solver's reported strip width. Sheet
scores come from the common material metric. `sparrow_report.audit_record` verifies
bytes, selected candidate history, timing, configuration and independent score.
Held-out maker jobs cannot be used in development.

The initial five-second FU strip and unequal-edge-gap sheet smokes pass. The FU
fixed-sheet attempt exceeds one sheet and receives no score. Four conversion
tests, three evidence tests and a native deadline test cover the adapter. Full
60/300-second, three-development-seed matrices remain pending.
