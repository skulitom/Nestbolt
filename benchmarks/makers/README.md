# Maker benchmark freeze

Forty maker jobs are frozen in `../datasets/M`, with ten reserved before any
optimiser tuning. The exact split, source parameters, curve files, job hashes,
generator hashes and licence evidence are in `../datasets/makers.json`.
No quality results were consulted in constructing or selecting these jobs.

| Category | Jobs | Held out | Source |
| --- | ---: | ---: | --- |
| Finger-jointed open boxes | 8 | 2 | Pinned Boxes.py UniversalBox, five panels per box |
| Garment cutting | 8 | 2 | FreeSewing 4.10.2 Teagan and Bruce, four synthetic measurement sets each |
| Cut-out lettering | 6 | 2 | Noto Sans default variable-font instance, six phrases |
| Mechanical parts | 12 | 2 | Original dimensioned brackets, trapezoid-tooth cogs, frames and inserts |
| Public artwork | 6 | 2 | Steren's CC0 Gear, two part sizes per job and six production runs |

These are declared generated/derived jobs, not forty unrelated donated designs.
The public-art category uses one credited source drawing. The mechanical cogs
have trapezoid teeth, not an involute transmission design.

Coverage includes 300×200 and 600×400 laser beds, 1220×2440 plywood,
1250×2500 and 1500×3000 sheets, and finite 1500-wide fabric-roll sections.
Jobs include holes, parts small enough to fit in holes, mixed quantities, 500,
1,000 and 2,000 copies, mixed stock with caps, defects, and an L-shaped remnant.
All forty use the all-parts material objective. Fill-mode behavior is tested
separately, so its area/priority objective cannot be mixed into the G2 metric.

The two held-out jobs in each category are named explicitly in the manifest.
They may be checked for source validity and final acceptance, but their nesting
results must never inform solver tuning or settings selection. Development
baselines use B and the thirty training M jobs. Final acceptance adds the ten.

## Source construction and precision

Boxes.py runs locally with zero burn compensation, no labels/reference bar,
square inner corners and a fixed metadata date. Each source group is one panel;
contained closed paths remain holes. Thick-plywood variants constrain grain to
0/180 degrees. The unmodified upstream checkout is read directly.

FreeSewing emits full-precision path operations. All required measurements,
including sleeve-library measurements, are supplied and generation refuses
warnings or errors. Original 10 mm seam-allowance paths are used. On-fold panels
are unfolded at X=0, removing only the shared fold segments; curves are preserved.
Cut-two parts have explicit reflected left/right source pieces. Placement grain
stays parallel to Y with rotations 0/180 and no optional mirroring. Measurements
are synthetic; none belongs to a person.

Font outlines retain quadratic curves and counters. Repeated letters become
quantities. Public Gear preserves the original compound contour and hole; only
the explicitly out-of-view decorative text is omitted. Its SVG units are scaled
to declared maximum dimensions. Original downloaded SVG bytes remain available.

Every job retains `curves.json` plus a physical-unit SVG contact sheet with one
of each part type and quantity attributes. The contact sheet is a source preview,
not a layout. Boxes and garments also retain their generator output.

Benchmark polygons use a **0.005 mm** subdivision bound, with coordinates rounded
to nine decimal places. Bezier control hulls bound the curve-to-chord distance;
elliptical arcs use a conservative sagitta bound. Crossed, touching and open
contours fail authoring instead of being silently repaired. Even/odd containment
preserves holes, islands and disconnected components. This authoring converter
is separate from the Rust product importer and does not establish G6 fidelity.

All forty source contracts pass the independent Rust checker. A deliberately
wasteful one-copy-per-sheet witness also passes for every complete job, including
the 2,000-copy cases. `../datasets/maker-feasibility.json` retains those reports
and witness hashes. These prove feasibility only; their material metrics are
not benchmark results, lower bounds, solver output or tuning observations.

## Reproduce and verify

The local freeze used Python 3.11.5 on Windows and Node 24.19.0. Fifteen Python
dependencies are pinned with archive hashes; npm uses its integrity-checked
lockfile. Generators are isolated from the product. Fresh generator installation
may require ordinary Python build tooling for source distributions; this is not
a claim of a hermetic compiler/toolchain build. Output bytes are checked exactly.

```powershell
python scripts/maker_freeze.py --check  # offline, no third-party Python packages
python scripts/maker_setup.py          # Python 3.11 + pinned Node; fetch checked sources
python scripts/maker_freeze.py --rebuild
.cache/maker-venv/Scripts/python.exe scripts/test_maker_geometry.py
python scripts/validate_makers.py       # regenerate full authoring witnesses
```

On Linux the venv executable is `.cache/maker-venv/bin/python`. The rebuild command
selects it automatically. CI is prepared for both Windows and Linux; hosted runs
remain pending until a remote repository exists. Do not replace the manifest or
edit a frozen generator after tuning. A necessary dataset correction requires a
new version, retained old evidence and an explicit result disclosure.

## Sources and licences

`sources.json` records immutable revisions, download hashes and attribution.
Full available notices and the publisher's licence evidence are retained in
`licenses/`; dependencies keep their own terms.

- [Boxes.py](https://github.com/florianfesti/boxes/tree/b82a6c9f84ab4b9ee91f5621b95d80b1b4fadf8d)
  is GPL-3.0-or-later software. Its [pinned FAQ](https://github.com/florianfesti/boxes/blob/b82a6c9f84ab4b9ee91f5621b95d80b1b4fadf8d/documentation/src/faq.rst)
  states that resulting drawings do not fall under the GPL. Nestbolt does not
  vendor or link Boxes.py into the product.
- [FreeSewing](https://codeberg.org/freesewing/freesewing/src/commit/3d290d25d0b6a65852dd31aec125c97bc8ca6e2c)
  is MIT, copyright Joost De Cock and contributors. The npm packages omit the
  separate licence file, so the pinned repository licence is retained here.
- [Noto Sans](https://github.com/google/fonts/tree/bd8f81ddb5c74d5c8897b36ad88b440266245103/ofl/notosans)
  is OFL-1.1, copyright 2022 The Noto Project Authors. Its original font is fetched
  by checksum into the cache; generated sign outlines retain source credit.
- [Gear by Steren](https://openclipart.org/detail/22109/gear), uploaded 2009-03-10,
  carries public-domain metadata. The [publisher FAQ](https://openclipart.org/share)
  states that its clipart uses CC0; the retrieved evidence is retained as HTML
  source, not executed or included in the app.
- Original job parameters, procedural parts and Nestbolt authoring code are MIT.

Python tool dependencies: affine 3.0.1, attrs 26.1.0, colorama 0.4.6,
fonttools 4.66.1, Markdown 3.11, numpy 2.4.6, pillow 12.3.0, PyYAML 6.0.3,
qrcode 8.2, rectpack 0.2.2, scipy 1.17.1, shapely 2.2.0, svgpathtools 1.8.0,
svgwrite 1.4.3 and typing_extensions 4.16.0. Installed-distribution notices include
their bundled third-party notices. Rectpack's omitted notice is retained from
its pinned 0.2.2 source tag, revision `123d57e0ef22adb5ae5f09b435c69f0589f521d1`.

The npm lock records all 21 packages, including FreeSewing's shared plugins,
bezier-js and Lodash helpers. FreeSewing configuration and transform packages are
explicit dependencies because they are imported at runtime but omitted by the
upstream package dependency declarations. Bezier-js declares MIT in its source
and metadata but ships no separate full licence file; that limitation and its
author/source revision are recorded in `licenses/bezier-js-NOTICE.txt`.
