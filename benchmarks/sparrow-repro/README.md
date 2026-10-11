# Published Sparrow reproduction (M0)

This isolated executable runs the **unmodified historical Sparrow 0.1.0 library**
at `7f069e9d146f5599d7ba69a47ab4e8097c56e54f`, using its jagua-rs 0.6.2 revision
`6e47329e4fd8dfe014428bd9045db132d26d35c9`. These versions used **MPL-2.0**.
The adapter's benchmark orchestration is adapted from historical `src/bench.rs`
under MPL-2.0, with attribution and the full licence in `UPSTREAM_LICENSE`.
They are not dependencies of the Nestbolt product. Current Sparrow is MIT;
that fact must not be substituted for the historical version's licence.

## Frozen method

Before any full-budget reproduction run, `../m0-reference.json` freezes all 26
published archives, their 1,300 lengths, input hashes, master seeds, the method,
and the [paper's Table 2](https://arxiv.org/html/2509.13329v1#S11.T2).

- Run every one of the 13 instances, for 1,200 seconds, with 3 search workers.
- For each instance use indices **0, 1, 2 from its archive without `(1)`**. The
  adapter reproduces the archive master seed to per-run `SmallRng` derivation.
- Compare the mean of these three lengths with the mean of **all 100 published
  lengths** for that instance. The absolute relative difference must be <=1%
  **for every instance**. Missing, failed or incomplete runs cannot pass.
- Report individual lengths, mean, median and quartiles. Preserve every attempt.
  Do not select the best seeds, switch baselines or discard a failure.
- This is a **39-run native quality reproduction**, not a statistical replication
  of all 1,300 experiments or a claim of identical layouts. Three seeds match the
  plan's development sampling; wider statistical evidence belongs to later gates.
- `blaz1` is SHAPES2 in the paper. Six supplied inputs already contain the paper's
  0.01% strip-height inflation. We preserve it. Raw archived densities use that
  inflated height; multiplying those six densities by 1.0001 reproduces the
  paper's nominal-height figures to their printed precision. The length metric
  needs no adjustment. Every archived mean was checked against the paper.
- M0 verifies quantities, finite metrics, instance identity and file hashes.
  The independent Clipper2 checker now also validates every completed layout
  against the original polygons. These checks do not establish the full M1
  baseline, G1 or Nestbolt solver quality.

## Environment and limits

The paper ran Ubuntu 20.04 under WSL2 on a Ryzen 9 7950X. This reproduction is
**native Windows on Artem's Ryzen 9 7950X3D**, with `nightly-2025-06-14`, SIMD,
`only_final_svg`, and `-C target-cpu=native`. Time-based search depends on hardware
and scheduling; even the same seeds do not promise identical layouts.

All archived runs identify the same solver commit, but were run June 14–18, 2025.
One toolchain is frozen here (the date of the earliest archived run). The original
Cargo.lock was not archived. Our replacement freezes registry releases available
before `2025-06-14T17:00:00Z`; it is a **reconstructed lock**, not the original.
`spin 0.9.8` is now yanked and is an explicit historical-only exception required
by the old dependency graph. It is confined to this local benchmark environment.
All dependency notices are retained in the separate `THIRD_PARTY_NOTICES`.

Search settings and the timing/seed sequence match historical `bench.rs`. The
wrapper adds JSON export and bounded external execution; it changes no solver
source or parameters. Each run has its own process and output directory.
At most 3 instances run concurrently (9 search workers total). Sessions stop
after at most 18 runs and stay under three hours even at lower concurrency.
The paper's three-worker setting is specific to M0; later equal-budget tool
comparisons retain the plan's one-worker rule.

On 2026-10-11 Artem confirmed temperature monitoring need not be a prerequisite.
The modest concurrency and bounded sessions remain in place.

## Commands from the repository root

The ignored upstream caches are the pinned clones described in
`docs/UPSTREAM_REVIEW.md`. `scripts/m0_reference.py --check` reads the historical
input blobs and the archives from those Git revisions, avoiding checkout line
ending differences. Historical input blobs remain cached locally. M1 preparation
has separately frozen the matching OR-Datasets collection under its retained MIT
licence; see [source provenance](../sources/README.md).

```powershell
rustup toolchain install nightly-2025-06-14 --profile minimal
python scripts/m0_reference.py --check
python scripts/m0.py build
python scripts/test_m0.py
python scripts/m0.py run --experiment published-20261011 --max-runs 18 --parallel 3
```

Repeat the last command for the next bounded session until all 39 runs finish.
Use `python scripts/m0.py report --experiment published-20261011` for a snapshot.
It verifies output hashes and never treats a partial matrix as a pass.
After all 39 runs finish, validate their original geometry and retain the final
table. The summary command refuses missing or failed runs and geometry checks:

```powershell
python scripts/validate_m0.py --experiment published-20261011
python scripts/m0_summary.py --experiment published-20261011
```

Use a different experiment name with `--smoke --max-runs 2` for five-second checks.
Smoke results never count towards the reproduction.

The runner preserves raw JSON/SVG, stdout/stderr, derived seeds, compiler, flags,
source/binary/input hashes, CPU, OS, Nestbolt commit and dirty state. It appends
each completed/failed attempt to `BENCHMARKS.md`. An interrupted directory is
preserved and requires explicit investigation; it is never overwritten.

To audit the historical lock reconstruction (not needed for ordinary replay):

```powershell
python scripts/lock_at_date.py benchmarks/sparrow-repro/Cargo.toml --before 2025-06-14T17:00:00 --toolchain nightly-2025-06-14 --allow-yanked spin
python scripts/notices.py --historical --check
```

Sources: [published archives and reproduction guide](https://github.com/JeroenGar/sparrow/tree/4629b22795ae6b25b3b460ccde6fb36a71292b6d/data/experiments),
[historical benchmark](https://github.com/JeroenGar/sparrow/blob/7f069e9d146f5599d7ba69a47ab4e8097c56e54f/src/bench.rs),
[paper](https://arxiv.org/html/2509.13329v1).
