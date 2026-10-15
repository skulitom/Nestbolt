# Isolated LightBurn diagnostic candidate — 2026-10-16

The candidate supplies all missing expected messages across the **56 frozen
training native projects**, while retaining **45 successful imports with exact
geometry/project equality and eleven identical clear rejections**. All 23
focused authored tests pass. This is an isolated prototype; production code is
unchanged while the guarded H4 comparison runs. H2 remains open and completed
milestone weight remains 45%.

## Messages and unchanged behaviour

Three reader changes explain existing behaviour:

- An artwork's shape index and type identify each bounding rectangle actually
  used for nesting. Attached engravings and fixed shapes do not get this message
  merely because their bounds exist.
- Missing Bezier controls report the native endpoint fallback, the number of
  affected segments and the number that become straight lines because both
  controls are absent. An omitted zero coordinate is not mistaken for an absent
  control. A curve with one remaining control is not called a straight line.
- Text with embedded outlines reports use of that cache and preservation of
  editable text. It explicitly says local fonts are not consulted; it does not
  claim that a font is missing on this computer.

No path construction, coordinates, nesting membership, settings, source XML or
export transformations change. The isolated copy also retains the separately
tested [hole-index repair](ci-curve-flat-index-probe-20261016.md). That search
change is not exercised by this import-only comparison.

## Verification

The [passing second audit](h2-native-warning-probe-20261016-v2/checks.json)
uses the public `decode_drawing` and `Library::import` APIs, the original filename
and the archived 0.005 mm import tolerance. Every source and label hash matches
the frozen training manifest. The original libraries are read from the
hash-verified H3 archive and match both their individual recorded hashes and
the archive inventory.

For all 45 accepted projects, the **whole library object is identical after
removing only its top-level warnings array**. This comparison includes exact
curves, polygons, components, areas, bounds, part identifiers, layer settings,
unit mapping and the full editable XML. Every previous warning is retained in
order. All eleven rejected projects produce the original error text exactly and
create no partial library. No nesting searches or reserved geometry are opened.

| Expected diagnostic on accepted originals | Covered |
| --- | ---: |
| Bounding rectangle | 12/12 |
| Fixed Tool/output-disabled shapes | 14/14 |
| Cached text outlines | 1/1 |
| Missing Bezier control fallback | 1/1 |
| Uncached text needing repair | 2/2 |

New messages also truthfully describe existing behaviour in other accepted
files: 29 libraries gain messages in total. The largest resulting warning array
has 26 entries, within the MCP's existing 50-entry reply limit. The browser's
Show all import messages control and the CLI expose the complete array. Actual
surface regression checks remain required after integration.

The [23 focused tests](h2-native-warning-probe-20261016-v2/authored-tests-stdout.log)
cover the existing native reader/writer and public project APIs plus the new
diagnostics. They verify compact and legacy partial controls, implicit zero
coordinates, attached/fixed/grouped artwork, exact original XML and an exact
identity sheet export. Core, validator and dependencies use `opt-level=3` with
debug assertions enabled, matching the production workspace's engine settings.
The isolated workspace omits unused CLI/MCP packages; every dependency it does
use matches the production lock's version, source and checksum. This does not
replace full workspace, CLI/MCP/browser or performance checks.

## Preserved failures and evidence

The [first audit](h2-native-warning-probe-20261016/checks.json) remains failed:
55/56 coverage checks passed, with all 45 geometry comparisons and eleven
rejections already exact. L28's message said “straight segments” but the reviewed
coverage rule requires an explicit line-fallback explanation. The candidate now
says “straight line segments”; the same coverage predicates and source geometry
are retained. The full 56-project check and 23 tests were rerun after that change.

An earlier preflight stopped before opening inputs because it required equality
of the complete dependency package sets. Cargo had pruned 43 unused CLI/MCP
packages from the isolated workspace. No candidate dependency differed. The
corrected preflight compares every used dependency's full record to production
and records the unused entries. Its failed source and explanation are retained.

The raw archives contain both attempts' libraries, messages, errors, candidate
patches, source inventories and harness snapshots. CRC, every member size and
every SHA-256 were verified before consolidating loose per-project files:

| Attempt | Members | Bytes | SHA-256 |
| --- | ---: | ---: | --- |
| [First, failed](h2-native-warning-probe-20261016/raw.zip) | 232 | 3,177,556 | `76d63f043232526045b531f7fac6c6845b837559db3f2455b0c1b68d570c1cb2` |
| [Second, passing](h2-native-warning-probe-20261016-v2/raw.zip) | 234 | 3,179,726 | `aaf3b4404537d62f13751080e609d37e47766ad74f72114c255606eeb02c39ec` |

The [second archive inventory](h2-native-warning-probe-20261016-v2/archive-integrity.json)
and source patch preserve the exact candidate. Harness files are snapshots of
scripts executed from `output/`, not standalone entry points at their archived
locations. The first test record retains the final tool-output chunk; the
second has complete captured test output. Source checkpoint: `73eb689`.
All production source/binary/site/runner guards still match the running H4 plan.
Integration, complete H2 fidelity review and the remaining reserved evaluation
are outstanding. No gate, label, split or original failure is changed.
