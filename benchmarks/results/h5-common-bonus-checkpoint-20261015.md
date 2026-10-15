# H5 common-line search bonus: development checkpoint — 2026-10-15

N4 now has an optional search bonus through the shared core, CLI, browser and
MCP schema. **H5 remains open; overall v1.1 completion stays at 20%.** This is a
10-second, one-seed development pilot, not the required 60-second, three-seed
measurement or final acceptance. No held-out geometry was read and no release
or registry publication was made.

## Behavior

`common_line.search_bonus` defaults to false. The browser exposes **Search for
more shared cuts**; CLI uses `--common-line --kerf <mm> --common-line-bonus`.
Changing either kerf control preserves the bonus selection. Project and effective
request files retain it. MCP uses the same typed request and preparation path.

With the bonus enabled, the existing material search gets 90% of its budget;
the remaining 10% tries local translations that align opposite straight edges
of exact source contours. Cost is material relative to this phase's starting
layout minus saved cut length divided by total cutting length. Every accepted
move improves that cost and saved length, retains sheet/rotation/mirror/quantity
assignments, passes independent collision and source validation, and stays
within 1% of the refinement's starting material use. Lead collision envelopes
remain binding. The original COMMON detector and exporter determine accepted
savings; a cheap pairwise estimate only orders trial positions.

This internal material guard is not the external H5 comparison against normal
mode. A shorter material-search phase and common-line's prohibition on
part-in-hole can change that comparison. The default search path, validator,
COMMON geometry and published v1 benchmark configuration are unchanged.

## Pilot and retained evidence

[Full three-arm results and 78 raw archives](h5-common-pilot-20261015T134229Z/README.md)
use all 13 frozen cutting-development jobs, kerfs 0.2 and 1.5 mm, seed 0, and
10 seconds per run. Arms are normal mode at the same spacing, common-line with
the bonus off, and common-line with the bonus on. The original geometry, stock,
quantities and orientation rules are preserved. Each saved layout is revalidated
in a fresh public CLI process, including its full common-line report.

| Kerf | Median bonus-off cut saving | Median bonus-on cut saving | Median material cost vs normal | Worst material cost | Jobs over +1% |
| --- | ---: | ---: | ---: | ---: | ---: |
| 0.2 mm | 8.586% | 13.120% | +0.000% | +6.205% | 3 / 13 |
| 1.5 mm | 7.270% | 13.430% | +0.000% | +5.364% | 3 / 13 |

All **78/78** nest and fresh-validation results are valid. Maximum report
round-trip difference is 2.9103830456733704e-11, below the unchanged 1e-9 harness
tolerance. Longest public nesting/export process is 10.9841 seconds. No failures
were excluded or rescored. Eight physical CCD0 cores were used, one per run;
focused builds/tests used CCD1 concurrently. This pilot is not a timing claim.

Normal mode placed 21 copies inside holes on `m-mechanical-large-plates` and 49
on `m-mechanical-panel-hardware`; common-line mode placed none, as required.
Those two jobs exceed +1% material at both kerfs. The other outliers are
`c-bracket-mixed` laser (+4.809%) and `c-bracket-u` plasma (+4.480%). All per-job
results remain visible. No gate threshold or dataset allocation was relaxed.

Pilot product working-source SHA-256:
`55c3b12e8ffc829d871bbf8a7fa2a4b9a8213402539a411ef42c0ddf32241b46`.
Pilot executable SHA-256:
`3c8f9fea026a4980fb641cb4de36e13a910d10324da95bb763434f042da2ed23`.
Results SHA-256:
`e6c0ae343b5e10400dd55b1c0aa99c525819b955c09becd86acbe825e4ab18cf`.
The frozen cutting manifest remains
`922d36732c6e7624b1c5501c8320effb12b33f37d7361cc5d5856b28d19ca814`.

After the pilot, seed-index arithmetic was made identical on 32-bit WebAssembly
and 64-bit native platforms by taking the modulus before narrowing to `usize`.
That changes no seed-0 proposal or score. Untouched UTF-8 test strings were also
restored after detecting a local editing-encoding error; production geometry
and scoring were unaffected. The pilot's original source/binary
hashes remain authoritative; it is not relabelled as a run of the later build.
The [pilot source archive](h5-common-pilot-20261015T134229Z/pilot-source.zip)
reconstructs the exact measured source hash, including those original test bytes.
Current-source checks and artifact hashes are recorded in
[verification.json](h5-bonus-checks-20261015T134600Z/verification.json).

## Validation and remaining work

The focused suites cover opt-in defaults, deterministic valid alignment,
defects, lead collision envelopes, and the six independent COMMON geometry/
Clipper2 property tests. Public CLI and MCP round trips exercise both option
values. Chromium and Firefox exercise both values, kerf edits, saved projects
and compensated exports. Strict workspace Clippy and the production browser
build pass. The final optimized CLI suite passes all 23 tests and MCP passes
all five connection tests. Six repeatable normal/bonus-off layouts exactly match
the retained earlier executable, with no leads involved. The frozen shop inventory
check confirms all 1,181 hashes unchanged. [Initial checks](h5-bonus-checks-20261015T134015Z/checks.json) and
[current checks](h5-bonus-checks-20261015T134600Z/checks.json) retain their logs.

The required 60-second, three-seed savings/material matrix and Deepnest-next
zero-spacing `mergeLines` SVG comparison remain outstanding. The existing
[COMMON geometry/native LightBurn check](h5-commonline-checkpoint-20261014.md)
stands: this work changes placement search, not cutting/export geometry.
Material outliers must be resolved or explicitly addressed before claiming H5.

Competitor refresh on 2026-10-15: [sparrow](https://github.com/JeroenGar/sparrow)
still describes strip packing; [sparrow/studio's README](https://raw.githubusercontent.com/JeroenGar/sparrow-studio/main/README.md)
still states no nesting inside holes or automatic multi-sheet allocation.
[Deepnest-next releases](https://github.com/deepnest-next/deepnest/releases)
list v1.5.6 as latest. [LightBurn's 2.2 early-access announcement](https://lightburnsoftware.com/blogs/news/lightburn-2-2-00-early-access-true-nesting-center-line-trace-multi-page-projects)
remains the relevant nesting release. The competitor stop condition was not
triggered; no upstream implementation code was copied.
