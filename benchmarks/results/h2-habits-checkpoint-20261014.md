# H2 shop habits, diagnostic coverage and complete vector fidelity

## Results

- [Complete vector fidelity](h2-fidelity-20261014T012836Z.md): 246 pass,
  11 clear rejections, no errors/timeouts; 5,138 matched contours, maximum
  SVG 0.003301680 mm and DXF 0.000499980 mm, below the 0.01 mm limit.
  Four dense Iris cases retain independently valid incumbents at the cooperative
  deadline and correctly report non-repeatable. Earlier failures remain.
- [Seeded habit properties](h2-habit-fuzz-20261014T015256Z.md): 10,000 importer
  cases and 1,008 successful nesting cases (1,000 new plus eight saved replays),
  zero failures. All 17 N0 habits occur in each of four fixed-seed batches.
- [Diagnostic and cut-layer audit](h2-warning-audit-20261014T015958Z.md): all
  246 imports cover their expected warnings and selected layers; all 11 rejections
  name repairs. Every current library has exactly the same source contours,
  parts, polygons, tolerance and stock outlines as the full fidelity sweep.
- [Fresh count audit](h2-import-training-20261014T015939Z.json): 245 raw exact
  part/hole matches; R43 remains the only count discrepancy and uses only the
  previously approved, hash-scoped exception (246 reviewed matches).
- [Robustness rerun](h2-import-robustness-20261014T015959Z.json): 36 imports,
  147 clear rejections, no crashes or timeouts; slowest file 1.275 s, under 10 s.

## Implementation and independent checks

DXF imports now warn about undefined layers and duplicate handles in original
entity records. Handle comparison ignores case and leading zeros. Repeated
INSERT instances and HEADER HANDSEED do not create false duplicate warnings.
The authored regressions check those distinctions and retained parts. Geometry
and selection behavior are unchanged, as the full library comparison confirms.

The new analytic property fixtures vary dimensions, translations and entity
order across all 17 generator habits. They cover explicit and silent gaps,
overlap cleanup, duplicate/zero segments, cubic SPLINEs and negative extrusion,
bulges/widths, nested mirrored blocks with nonzero bases, missing/inch/cm units,
annotations, construction layers, operation colours and pre-arranged stock.
Independent formulas check bounds and area; an off-centre circular hole exposes
wrong reflections or forgotten block bases. Search properties vary quantity and
mirroring and require every feasible job to succeed and pass the independent
original-polygon validator. Failed input seeds persist for regression replay.

The Gherkin warning was reviewed independently rather than altering its label:
ezdxf/GEOS finds 104 closed paths and zero open source paths. SPLINE 42B retraces
7.888067184 mm; polygonization treats the resulting spur as open linework.
The imported affected contour matches within 0.000371576 mm and all 104 contours
remain. The existing self-touch warning describes this retained geometry.
No new scoring exception is applied.

## Verification and scope

205 workspace tests pass (one existing ignored); 20 optimized CLI feature tests
and 48 Chromium/Firefox tests pass (four opt-in benchmark/scale tests skipped).
Strict Clippy, formatting and optimized WASM/TypeScript/browser builds pass.
All 1,181 frozen inventory hashes and the frozen manifest hash are unchanged.

Builds/tests run on CCD1. Recorded property and import batches use one process
per CCD0 physical core 0/2/4/6; the independent diagnostic review uses CPU 8.
Product, binary and runner guards pass. No held-out geometry or label was
interpreted. The published v1 results and quality claims remain unchanged.

H2/H3 remain incomplete: native-project completeness and the outstanding
specification/held-out decisions still need resolution. Completed milestone
weight stays 15%; no release, registry publication or final acceptance run.
