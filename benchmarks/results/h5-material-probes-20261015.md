# H5 material diagnostics — 2026-10-15

Two proposed levers failed to improve the material shortfall. **Keep production behavior unchanged; H5 remains open.** These development diagnostics do not prove the +1% target impossible. Overall completed milestone weight remains 20% (H1 and H6).

## Results

The schedule probe runs both frozen mechanical jobs at both kerfs, seeds 0–2, with a 60-second total search budget. Only the share assigned to initial repacking changes: 10% (current default), 50%, or 85%. Holes stay reserved and the common-line bonus is disabled. All 36 searches, original-job validations and public exports pass. Both longer warm stages worsen the median material at every job/kerf.

The separate pairing probe builds rigid pairs of identical concave orthogonal parts using their geometry and rotation rules. It selects six bracket pairs for large plates and twenty for panel hardware, preserving all original rings and expanding placements back to original copies for validation and export. Its conservative multipart hulls reduce local proxy area, but restricting placement to these pairs worsens every job/kerf median. All 12 searches and original-job checks pass. **This probe adds 0.586 seconds or less of pattern preparation outside its 60-second search budget and is not an equal-total-time product comparison.**

| Job | Kerf mm | 10% warm | 50% warm | 85% warm | Rigid pairs, 10% warm |
| --- | ---: | ---: | ---: | ---: | ---: |
| m-mechanical-large-plates | 0.2 | 1.15672414 | 1.16297423 | 1.16622561 | 1.18129828 |
| m-mechanical-large-plates | 1.5 | 1.15990000 | 1.16847915 | 1.17689235 | 1.18271201 |
| m-mechanical-panel-hardware | 0.2 | 1.58471272 | 1.59086516 | 1.60831965 | 1.64962556 |
| m-mechanical-panel-hardware | 1.5 | 1.60720929 | 1.60911417 | 1.63208019 | 1.66935617 |

Values are three-seed medians of normalized material consumption; lower is better. The default diagnostic medians are still +4.3420% to +5.9170% above the normal-mode medians from the earlier full comparison. Normal mode places 21/49 inserts in frame holes; these diagnostics reserve every hole. That explains part of the difficulty but is not a mathematical impossibility proof. The earlier full common-line comparison remains the authoritative H5 measurement; these smaller solver diagnostics do not replace it.

## Verification and provenance

- Product source baseline: `2c530e7def5f093f4f780e9855018b3732f58963`. Only a development example and Python experiment runners were added; no existing product source or default changed. The public CLI binary remains SHA-256 `4cec132d9540524a0007b2a0894d6682064d42709ee971b48860d4199712137a`.
- Eight independent CCD0 lanes use logical CPUs 0, 2, 4, 6, 8, 10, 12 and 14, one per physical core. The example build and lint use CCD1. Pair preparation/report work uses CCD1. No source or runner changed during either measured batch.
- All 48 ZIP archives and 744 recorded members pass hash checks. Fresh public CLI validation matches saved material exactly; the ordinary schedule arms match all saved metrics exactly. Grouped and expanded copy counts intentionally differ, so the pairing arm compares material and independently checks every original copy.
- An additional Shapely audit transforms original **filled outer contours** and checks all 228,580 same-sheet pairs. Every pair is disjoint and has at least the requested kerf clearance; minimum measured slack is 0.0000019999998 mm. This independently excludes all part-in-hole placement.
- Pair expansion was separately checked with five copies (including an odd remainder), four quarter-turns and both reflection states. All eight cases preserve copy identities and agree with independently transformed grouped geometry within 3.22e-13 mm; fixed-orientation inputs reject the incompatible pair.
- Maximum external search process times: 59.9997 seconds for the schedule batch and 59.8387 seconds for pairs. Pair preparation is additional, as stated above. Export/revalidation are outside the solver budget.
- The frozen cutting manifest (`922d36732c6e7624b1c5501c8320effb12b33f37d7361cc5d5856b28d19ca814`) and shop manifest (`02e1f40fe7ad6459cce801620d7de4a14c10d9a1fad435e6d1b45a68ac34c3b7`) are unchanged. No held-out geometry was read.
- Rust example release build, formatting and strict Clippy pass; Python runners compile. The existing product did not change, so its full runtime suite was not repeated locally. The prior checkpoint passes [all six CI jobs](https://github.com/skulitom/Nestbolt/actions/runs/38757915004), including Linux, Windows, browser, both maker rebuilds and benchmark smoke.
- The CPU clock observation is 4201 MHz. The ACPI sensor query was denied; no CPU die-temperature claim is made.

## Reproduce and retain

Build `cargo build --release --locked -p nestbolt-core --example sheet_schedule` on CCD1, then run `python scripts/h5_schedule_probe.py --warm 0.1 0.5 0.85` for the schedule probe. For the exploratory pair probe use the pinned shop Python environment and `scripts/h5_schedule_probe.py --pair-complements --warm 0.1`. New directories are created; existing raw evidence is never overwritten. These are development runs only.

- [Schedule plan, records and archive hashes](h5-schedule-probe-20261015T152046Z/results.json); the exact runner/example versions used are archived alongside them.
- [Pair plan, records and archive hashes](h5-pair-probe-20261015T152814Z/results.json); the exact runner/example/pattern versions used are archived alongside them.
- [Integrity and transform checks](h5-material-probes-20261015-checks.json), [filled-outer clearance audit](h5-material-probes-20261015-filled-check.json).

Further work needs a different placement strategy, such as exchanges between sheets that retain the incumbent and share the existing deadline. Repeating these warm-time settings or permanently locking these bracket pairs is not supported by the measurements. No gate threshold, production default, published v1 result, release or registry state changes.
