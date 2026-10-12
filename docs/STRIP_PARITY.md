# Native strip parity

The `nestbolt strip` diagnostic connects the unmodified Sparrow 0.3.0 library to
Nestbolt jobs and the independent geometry checker. It uses the same pinned
revision as the current Sparrow comparator:
`4629b22795ae6b25b3b460ccde6fb36a71292b6d`.

The complete development comparison contains **39 valid outputs**, covering all
13 S jobs at 60 seconds with seeds 0, 1 and 2. Against the better finite
three-seed median of Sparrow's identical and upstream-default settings, the
median regression is **−0.03903427%**, and the largest is **+1.64931279%**.
This meets the development thresholds of at most 1% median and 2% per instance.
The [audited table](../benchmarks/results/strip-development-20261012T040418Z-961c9a96.md)
retains every attempt, reference table and full-precision score. Final G3 still
requires the frozen acceptance settings, final seeds and benchmark envelope.

## Input and output

```sh
cargo run --release -p nestbolt-cli -- strip --job benchmarks/datasets/S/s-fu-strip.json --output fu-strip-layout.json --seconds 60 --seed 0
```

Use an all-parts polygon job with one available rectangular stock type, one simple
outline per part, zero clearance and margins, and no defects. Unsupported
constraints are rejected. Discrete, stepped and continuous rotation and permitted
reflection are mapped to Sparrow, then checked against the original job. Stock
width remains the maximum allowed width; successful layouts must fit it.
Units, part identifiers and copy counts survive the conversion.

The command writes the layout to the requested new file, reports progress on
stderr and returns the result JSON on stdout. An existing output file is preserved.
Every accepted candidate passes Nestbolt's independent checker. Its strip length
is measured from the original transformed vertices, rather than Sparrow's
reported container width.

## Execution and evidence

The adapter uses one search worker, no polygon simplification or concavity
closing, and the comparator's 90/10 exploration/compression split. Import,
construction, search and candidate validation share the declared 1–300 second
budget. A candidate is accepted only if its independent check finishes before
the global deadline. An indivisible upstream operation can finish later; the
returned incumbent must still have been accepted within the budget.

These timed results can vary with machine scheduling. The diagnostic is native
only and is separate from deterministic fixed-sheet search, the browser engine
and the planned MCP `nest` interface. Both WebAssembly builds continue to exclude
the Sparrow dependency. The library and its additional dependencies are recorded
in the locked dependency notices.

The development harness sets `RAYON_NUM_THREADS=1`; each process was additionally
pinned to one logical CPU. At most eight solver processes ran concurrently.
Seed 0 used CPUs 0/2/4/8, seed 1 used 6/12/14, and seed 2 used 2/4/8/10 after
those earlier slices ended. This is development evidence, not a new final
hardware calibration. No solver settings changed during the 39 attempts.

`scripts/strip_pilot.py` retains original jobs' hashes, executable/source hashes,
raw output, progress and independent validation. `scripts/strip_report.py`
requires all 39 unique slots, audits the saved output, independently checks every
layout again, recomputes strip lengths and audits the original Sparrow references.
Failed attempts remain failures; a failure cannot become an automatic parity win.
The [source provenance record](../benchmarks/results/strip-source-provenance-20261012T0408.json)
also maps executed Windows source bytes to Git's LF-normalized text hashes.

Tests cover reflection conversion, original-vertex scoring, input restrictions,
global deadline limits, a real native solve, the actual CLI file contract and
the report's complete population and failure handling.
