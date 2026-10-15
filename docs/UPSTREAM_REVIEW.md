# Upstream review — 2026-10-11

Rechecked 2026-10-13 for v1.1 N0 and the early N2 format probes. The current
[Sparrow Studio README](https://github.com/JeroenGar/sparrow-studio) still excludes
nesting in holes and automatic allocation across sheets; the stop rule is not
triggered. [Sparrow](https://github.com/JeroenGar/sparrow) still describes strip
packing. [Deepnest releases](https://github.com/deepnest-next/deepnest/releases)
still list v1.5.6 as latest. [LightBurn's 2.2 early-access note](https://lightburnsoftware.com/blogs/news/lightburn-2-2-00-early-access-true-nesting-center-line-trace-multi-page-projects)
describes Pro-only True Nest, multi-page projects and a REST API. Our format gate
remains on the installed 2.1.01; no update is installed for this work.

Reviewed before starting M0. Repeat at the start of every milestone. If Sparrow
Studio ships fixed-sheet allocation or part-in-part, stop and tell Artem.

| Project | Observed revision / release | Finding |
| --- | --- | --- |
| [sparrow](https://github.com/JeroenGar/sparrow) | `4629b22795ae6b25b3b460ccde6fb36a71292b6d` | 0.3.0 manifest pins jagua-rs 1.1.0; strip solver, MIT |
| [sparrow/studio](https://github.com/JeroenGar/sparrow-studio) | `a738c18d9c28e371983b164129190dad1616d273` | README still says strip packing, no automatic multi-sheet allocation or nesting in holes; MIT |
| [jagua-rs](https://github.com/JeroenGar/jagua-rs) | `9e00fd867be0fc493002aea68a1c6613d5b833d6` | 1.1.0, MPL-2.0, BPP/SPP, reflection axes, container holes; item holes still rejected |
| [deepnest-next](https://github.com/deepnest-next/deepnest) | `1e7ba6e2382557f337ad481ca3251fc22032ca0f` | Active sheet nester; latest GitHub release observed: v1.5.6 (2025-05-19); inspected native adapter has valid FU/spacing-safe smoke results, full matrix pending |
| [SVGnest](https://github.com/Jack000/SVGnest) | `1248dc21efd3f90d1aa52ba5785e27e5217ed2c9` | Default-branch commit dated 2019-04-11; distinguish this from repository push timestamps |
| [LightBurn release notes](https://lightburnsoftware.com/blogs/news/lightburn-2-2-00-early-access-true-nesting-center-line-trace-multi-page-projects) | 2.2.00 early access, 2026-09-16 | True Nest remains a paid comparison outside our measured gate; no licence obtained |

**Stop condition not triggered.** README review establishes declared capability,
not measured performance. Versions above are a dated observation, not a permanent
claim about competitors. The source manifests were inspected because some README
version statements lag the current release.

Rechecked the four required competitors on the same date before M1 preparation
while M0 runs were active. Sparrow Studio still explicitly excludes automatic
multi-sheet allocation and nesting in holes; the stop condition remains untriggered.
The observed releases/revisions above are unchanged.

Rechecked before M2 implementation at 22:30 UTC on 2026-10-11. GitHub API heads
for Sparrow, Studio and deepnest-next match the revisions above. Studio still
explicitly excludes automatic multi-sheet allocation and nesting in holes;
Deepnest's latest release remains v1.5.6. LightBurn's primary release note still
describes Pro-only True Nest in 2.2 early access. The stop condition is not
triggered. M2 starts while the remaining M1 comparisons finish.

Sparrow's [published reproduction instructions](https://github.com/JeroenGar/sparrow/blob/4629b22795ae6b25b3b460ccde6fb36a71292b6d/data/experiments/README.md)
require historical revisions and nightly/SIMD settings. The new integration smoke
uses the current pinned revision and a stable compiler; it does not reproduce those
published numbers.

Distribution references reviewed: [Cutbolt #2](https://github.com/skulitom/Cutbolt/pull/2)
and [Inkbolt #1](https://github.com/skulitom/Inkbolt/pull/1). They inform the M4 plan;
no code from these PRs has been copied. MCP uses the [official Rust SDK](https://github.com/modelcontextprotocol/rust-sdk),
pinned to rmcp 3.5.1.


Rechecked on 2026-10-13 at the H1 completion / N1 boundary. The [Studio README](https://github.com/JeroenGar/sparrow-studio)
still excludes automatic multi-sheet allocation and nesting in holes; no stop
condition fired. [Sparrow](https://github.com/JeroenGar/sparrow) remains a strip
solver. [Deepnest releases](https://github.com/deepnest-next/deepnest/releases)
still mark v1.5.6 latest. The [LightBurn early-access note](https://lightburnsoftware.com/blogs/news/lightburn-2-2-00-early-access-true-nesting-center-line-trace-multi-page-projects)
still describes 2.2 True Nest as Pro-only. This is a capability/documentation
review, not a performance measurement or software update.

Rechecked on 2026-10-14 during the N4/N5 implementation checkpoint. The
[Studio README](https://github.com/JeroenGar/sparrow-studio) still explicitly
excludes nesting in holes and automatic allocation across sheets. The stop
condition is not triggered. [Sparrow](https://github.com/JeroenGar/sparrow)
still describes strip packing, [Deepnest releases](https://github.com/deepnest-next/deepnest/releases)
still mark v1.5.6 latest, and the [LightBurn early-access note](https://lightburnsoftware.com/blogs/news/lightburn-2-2-00-early-access-true-nesting-center-line-trace-multi-page-projects)
still describes 2.2 Pro True Nest. No competitor code or software was changed.

Rechecked on 2026-10-15 while returning to N3 after H3 completion. The
[Studio README](https://github.com/JeroenGar/sparrow-studio) still excludes
automatic allocation across sheets and nesting inside holes, so the stop
condition is not triggered. [Sparrow](https://github.com/JeroenGar/sparrow)
still describes a strip solver. [Deepnest's release list](https://github.com/deepnest-next/deepnest/releases)
still marks v1.5.6 as latest; the [LightBurn 2.2 early-access note](https://lightburnsoftware.com/blogs/news/lightburn-2-2-00-early-access-true-nesting-center-line-trace-multi-page-projects)
still limits True Nest to Pro. These are current documentation observations,
not new performance measurements or installed-software changes.
