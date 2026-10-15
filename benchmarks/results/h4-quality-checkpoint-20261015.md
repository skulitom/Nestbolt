# H4 development quality: all layouts valid, Chrome narrowly misses

The eleven declared curve-heavy development jobs ran for 60 seconds with seeds 0–2 in native, installed Google Chrome 155.0.8059.41 and Firefox 157.0. **All 99 layouts independently validate**, with exact agreement of every saved/standalone metric. Firefox passes this subset; Chrome does not. H4 remains open and completed milestone weight stays 20%.

| Engine | Valid | Median material difference from native | Worst job difference | Total difference | Subset gate |
| --- | ---: | ---: | ---: | ---: | --- |
| Native | 33/33 | reference | reference | reference | reference |
| chrome | 33/33 | +1.014665% | +3.301224% | +1.375503% | fail |
| firefox | 33/33 | +0.486636% | +1.211913% | +0.431490% | pass |

Chrome's unrounded median is +1.0146645905193097%, exceeding the +1% limit. It is not rounded into a pass. Every job in both browsers is within the separate +5% limit. These are equal-weight per-job differences between three-seed material medians. All required attempts participate; failed or missing attempts could not pass. The total difference is informational for this subset.

| Job | Native median | Chrome difference | Firefox difference |
| --- | ---: | ---: | ---: |
| m-mechanical-cog-washers | 1.871767062 | +0.7282% | +0.1247% |
| m-public-gear-1 | 0.940400875 | +3.1819% | +0.5302% |
| m-public-gear-2 | 0.823038290 | +0.3795% | +0.2202% |
| m-public-gear-3 | 0.509866027 | +1.6165% | +1.2119% |
| m-public-gear-4 | 0.552170088 | +0.2509% | +0.1545% |
| m-sign-1 | 0.716512220 | +0.8073% | +0.8826% |
| m-sign-2 | 0.579480767 | -0.2627% | +0.4697% |
| m-sign-3 | 0.138445442 | +1.1951% | +1.1121% |
| m-sign-4 | 0.320065857 | +2.9469% | +0.9357% |
| example-letters | 0.276669505 | +1.0147% | +0.4866% |
| example-gears | 0.939389425 | +3.3012% | +0.2123% |

## Method and fixed inputs

The G5 runner serves the unchanged built site locally and calls its real WebAssembly worker once per job. At most eight jobs run together on physical CCD0 CPUs 0, 2, 4, 6, 8, 10, 12 and 14. Native processes are individually pinned; browser process trees inherit and retain the same eight-core mask. All six browser sessions report no affinity deviations. Native validation runs after each browser batch exits. No optional quick start, common-line mode, lead allowances or simplification environment override was enabled. This is a local development measurement, with no geometry uploads or held-out inputs.

The nine existing maker jobs are unchanged. The [frozen example fixtures](../datasets/browser-quality/README.md) use the shipped examples and actual app request settings. Letters has 45 imported parts / 156 cutting pieces from 147 glyph quantities; disconnected contours are retained. Gears has two parts / 40 copies. The diagnostic `project_job` example calls the existing public conversion, retaining every component and the curve-clearance allowance. All 18 saved example layouts also pass validation against their original public library/request pairs.

The product binaries are those measured after `9364ec4`; the uncommitted diagnostic job-conversion example is included in the recorded source digest and archived verbatim. The later `104770a` change affects only the unrelated preservation test and its documentation. No measured code, executable, input or built-site asset changed during this run.

- CLI SHA-256: `3e2d43d495bdc9ad1f8e672dbdd7cb122af17dea3e48dad32eba5cffb24e77f5`.
- WASM SHA-256: `1eeaeef28cd8c297a825516dbe5e2460acc9e7add3fd220641d1d71798476c3a`.
- Complete source digest: `c1f0f3daacbc0ec3730322f1c5999d5cdcf8e1f7001df5fd24aaaab5992a3783`.
- Reported search elapsed ranges: native 59.626–60.525 s; Chrome 59.659–60.675 s; Firefox 59.688–60.743 s. The shared solver uses cooperative deadline checks.

## Retained preparation and pilot outcomes

The first fixture preparation rejected exact JSON numeric equality: re-serialization changed a coordinate by 5.684341886080802e-14 mm. The final preparation uses the existing 1e-9 absolute JSON comparison tolerance, keeping exact structure and discrete values. No geometric tolerance or input outline changed. The original script and failed preparation remain archived.

A separate five-second, seed-0 pilot runs both examples in all three engines. Gears validates in all three; letters clearly reports no complete layout within five seconds in all three. Those outcomes remain unscored pilot evidence and are not replaced by the subsequent 60-second runs. Failure-ranked scoring checks verify that one failed seed prevents a gate pass even when the median remains finite, and two failures produce a null median.

## Remaining requirements and evidence

Chrome needs a measured improvement before the subset can pass. The complete G5 development comparison and the 195-run native matrix are still outstanding; no H4 completion claim follows from Firefox alone or the earlier scale passes. The published `75cbb32` binary is present and matches its sealed SHA-256 `1dd58ac0ef3347af878271f888b7c326045961ba9d959cc4743acbce04b526de`. The older M4 development records use a different binary (`33d6d8ee…`), so they must not be silently substituted for that reference. No published v1 results or final acceptance run changed.

[Full 99-run record](h4-quality-20261015T200939Z/results.json), [predeclared plan and guards](h4-quality-20261015T200939Z/plan.json), [six-run pilot](h4-quality-20261015T200454Z/results.json), [verification checks](h4-quality-checkpoint-20261015/checks.json). All 1,181 frozen shop files still match their original hashes. The [raw archive](h4-quality-checkpoint-20261015/raw.zip) retains 655 members, including every layout, search result, standalone validation, browser plan/log, initial failure and runner snapshot; [CRC/SHA-256 integrity](h4-quality-checkpoint-20261015/integrity.json) was verified before removal of exact loose copies.
