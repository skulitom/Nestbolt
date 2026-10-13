# N1 layer and colour selection checkpoint — 2026-10-13

**H2 remains incomplete; total milestone completion is 15%.**

The UI now inventories layers/colours before import and supports per-file filters,
including drawings whose outlines are all open. CLI `--layers` / `--colors` and
MCP `layers` / `colors` use the same core selection. Reports count selected,
unselected and ignored entity instances. Automatic selection prefers
cut/outline/profile layer names. Explicit filters intersect; ignored annotations,
bend/extent/construction layers and hidden geometry remain excluded with warnings.

DXF block children resolve layer 0, BYBLOCK and BYLAYER. Block base points and
negative-Z INSERT placement now compose in the correct order. Broken POLYLINE
sequences name the required re-export fix. SVG presentation attributes, simple
CSS tag/class/ID rules, inline styles and group/use inheritance determine colours.
Ordinary DOCTYPE declarations work with no external resolver; unsupported CSS
selectors name a plain-SVG/presentation-attribute export fix.

## Training diagnostics

[Complete report](h2-import-training-20261013T184036Z.json), 257 frozen training
DXF/SVG inputs. No held-out geometry or label was read.

| Set | Imported | Rejected | Matching part/hole counts |
| --- | ---: | ---: | ---: |
| Generated | 167 | 3 | 160/170 |
| Real | 55 | 4 | 49/59 |
| LightBurn native DXF/SVG | 24 | 4 | 12/28 |
| Total | 246 | 11 | **221/257** |

The pre-change baseline matched 165/257. This comparison diagnoses import
behavior, not H2 acceptance or nesting quality. Exact layer/warning acceptance and
curve re-export fidelity are still pending. Native projects are outside this
vector-only diagnostic and will require N2. Remaining mismatches include
overlapping segments, repeated/near-coincident native DXF contours, legacy DXF
encoding, complex topology and labelled negative fixtures imported partially.
The four rejected native line-converted files now name their missing SEQEND and
request a corrected export, consistent with their pre-frozen negative labels.

[Robustness report](h2-import-robustness-20261013T184058Z.json): 183 attempts,
83 imported, 100 rejected, no panic or timeout; slowest 0.764 s. Both runs used
one process on each of four CCD0 physical cores with a 10 s limit. Product and
runner source hashes stayed unchanged; builds ran on CCD1. Original reports,
including all earlier failures, remain retained.

## Verification

- Six focused core layer/style/block tests passed. Two first-attempt bounds
  assertions incorrectly demanded analytic bounds from a flattened circle proxy;
  the corrected tests verify the exact source arc centre/radii and require proxy
  bounds within 0.005 mm. No product behavior changed for that correction.
- CLI selection test and MCP stdio import/nest/export test passed.
- Chromium and Firefox: 6/6 gap, layer/colour and open-only inventory checks passed.
- Production WASM/web build and schema generation passed.
- Full workspace tests passed, with one existing ignored Sparrow debug test.
  Strict Clippy first flagged the MCP options initializer; the equivalent struct
  initializer fixes that lint and Clippy passes. A final simple-CSS precedence
  correction gives `*` lower priority than a tag selector; all six focused tests
  pass with that regression case. The recorded corpus/browser runs precede these
  final two small changes; their source hashes identify their exact code state.
- Frozen inventory: all 1,181 files and the manifest hash unchanged. The first
  integrity command used the system Python without ezdxf; the pinned corpus
  environment then completed the check successfully.

Cleanup, units/encoding, full fidelity and property testing, export palette and
native LightBurn evidence remain pending. The held-out scoring clarification is
also pending; neither the corpus nor the allocation was changed.
