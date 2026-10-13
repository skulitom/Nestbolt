# v1.1 research notes (2026-10-13)

*Reference for [PLAN_V1_1.md](PLAN_V1_1.md).*

**Local verification update (2026-10-13):** [LBRN2.md](LBRN2.md) records the
LightBurn 2.1.01 probes and their saved files. They establish the origin flags,
the `StartV` start-point attribute, lead setting names, independent vertex/primitive
sharing, image/vector setting families with colliding indices, and modern
Fill/Line sub-layers. Modern DXF export is AC1021 and Legacy is AC1009, both with `$INSUNITS=4`; the blanket
"exported DXFs carry no units" statement below does not hold for this export
variant. Earlier linked reports remain historical evidence, not a schema.

The subsequent [native collection report](../benchmarks/results/n0-native-20261013.md)
records the 15 real-design projects and 35 exports. Legacy DXF line conversion
produced five files rejected structurally by ezdxf; their native bytes are kept.
The T1 palette check now also covers **Allow Importing to Tool Layers**: with it
enabled, exact true-colour BYLAYER geometry maps to T1, while explicit entity
ACI 30 still maps to C05. The option was restored after testing.

How these were gathered:
- Compiled from public sources by research agents on 2026-10-13. Nothing was decompiled.
- Files were only inspected (headers streamed, repository trees listed); none were copied into the repo.
- deepnest-next was read in the local checkout `.cache/upstream/deepnest-next` (revision 1e7ba6e, v1.5.6), for its
  behaviour only.
- Items marked **verify** must be confirmed before they are relied on.

## 1. Messy real-world files

### 1.1 Which program wrote a file (DXF header fingerprints)

| Writer | Fingerprint |
|---|---|
| Fusion 360 | `$ACADVER=AC1014` and `$INSUNITS`, `$HANDSEED=FFFF`, a single layer `0`, group codes without leading spaces. Confirmed by 3 projects whose READMEs name Fusion. |
| Inkscape (R14) | `$ACADVER`, `$HANDSEED=FFFF`, `$MEASUREMENT`; padded group codes; layers named after SVG layers (`Layer_1`). |
| KiCad plot | R12, no `$ACADVER`, only `$ANGBASE/$ANGDIR/$MEASUREMENT`; everything as LINE. |
| FreeCAD | comment `999 FreeCAD v0.21`. |
| LibreCAD | comment `999 dxfrw`. |
| QCAD | comment `999 dxflib`. |
| SolidWorks | AC1015 with about 199 header variables. |
| OpenSCAD | no HEADER section at all. |

### 1.2 Usable sources: real files under permissive licences

Re-check each licence at download time and record it in the manifest.

| Source | Licence (where stated) | Files | Writer (evidence) | Notable mess |
|---|---|---|---|---|
| [Rev1s10n/Tri-Hard-slab-v2](https://github.com/Rev1s10n/Tri-Hard-slab-v2) | CC BY 4.0 (README) | 6 DXF | Fusion (README + fingerprint) | 5-layer acrylic stack |
| [OpenStickCommunity/Hardware](https://github.com/OpenStickCommunity/Hardware) | CC BY 4.0 in each design's README; **verify** each design (4 checked: OSM, ARC, Open_Core0, Flatbox Rev 5 RGB) | about 20 DXF | Fusion fingerprint; AutoCAD AC1021 | `$DWGCODEPAGE ANSI_936`, an AutoCAD 2005 plotter path |
| [tahnok/LACC](https://github.com/tahnok/LACC) | CC BY-SA 4.0 (README) | 5 DXF + 5 SVG | Fusion (README); SVGs from Inkscape | 89 LINE + 20 LWPOLYLINE in one part |
| [josefadamcik/SofleKeyboard](https://github.com/josefadamcik/SofleKeyboard) | MIT | 10 DXF + plate SVGs | 6 Fusion, 3 Inkscape, 1 KiCad | 1,544 exploded LINEs; SVG viewBox of 70,610 units across 17.9 cm |
| [keebio/iris-case](https://github.com/keebio/iris-case), [keebio/dsp40-case](https://github.com/keebio/dsp40-case) | MIT | 18 DXF + 3 SVG | AC1024 with no program string, likely Illustrator (a sibling SVG says Illustrator 22); R12; one Fusion | splines inside blocks; ENTITIES holding only INSERTs; about 9,000 POLYLINE vertices; inch and mm mixed |
| [caileighf/mechanical_keyboard](https://github.com/caileighf/mechanical_keyboard) | MIT | 3 DXF + 3 SVG | probably Illustrator (inferred) | SPLINE + POLYLINE, nested INSERTs, inches |
| [MeArm/MeArm](https://github.com/MeArm/MeArm) | CC BY-SA 3.0 (README) | 4 DXF | v1 contains "ODA"; v2 Fusion; v3 R12 | v1 `$INSUNITS=5` (cm) with 1,176 SPLINEs; v2 113 ELLIPSEs; v3 TEXT in 78 blocks |
| [nortd/lasersaur](https://github.com/nortd/lasersaur) `docs/jobfiles` | CC BY-SA 4.0 ([wiki](https://github.com/nortd/lasersaur/wiki/license)) | 7 DXF | R12, writer unknown | real laser jobs, all exploded LINE/ARC |
| [nasa-jpl/open-source-rover](https://github.com/nasa-jpl/open-source-rover) | Apache-2.0 | 7 DXF | FreeCAD 0.21 | exploded; 3 layers |
| [FreeCAD/FreeCAD-library](https://github.com/FreeCAD/FreeCAD-library) | CC BY 3.0 (`LICENSE-Assets` names .dxf; per-part authors in git history) | 12 DXF | 7 Fusion (MIT E-Vent, inches), 4 Inkscape, 1 R12 | splines; an R12 file with all geometry in one block plus one INSERT |
| [mikedh/trimesh](https://github.com/mikedh/trimesh) `models/2D` | MIT for the repo; provenance of the models unstated, so **verify** before use | 24 real + 32 version variants | SolidWorks (two say "SolidWorks Educational Edition"), LibreCAD, AutoCAD 2007-2013 | inches; DIMENSION; 299 blocks in one file; `broken_loop`/`broken_pair` open contours |

### 1.3 Permissive DXF test suites

| Suite | Licence | Files | Covers |
|---|---|---|---|
| [ezdxf](https://github.com/mozman/ezdxf) `examples_dxf`, `integration_tests/data` | MIT | 81 | AC1003-R2018; binary R12-R2000; duplicate and empty handles; data after EOF; missing block records; recover01/02; MTEXT columns; hatches; wipeout; third-party files (Leica Disto, dxflib) |
| [GDAL](https://github.com/OSGeo/gdal) `autotest/ogr/data/dxf` | MIT-style | 54 | entities-only files with no HEADER; OCS/extrusion −1; bulge and smooth polylines; a recursive INSERT pair; hatch; dimension; leader; QCAD files; fuzzer cases; utf-8 |
| [ACadSharp](https://github.com/DomCR/ACadSharp) samples | MIT | 26 | one drawing in ASCII and binary for each version AC1009-AC1032; 10 dynamic-block files |
| [dxf-parser](https://github.com/gdsestimating/dxf-parser) | MIT | 13 | one real AutoCAD Architecture sheet (293 DIMENSION, 65 HATCH, MULTILEADER); small spline, ellipse and block fixtures |
| [CadQuery](https://github.com/CadQuery/cadquery) `tests/testdata` | Apache-2.0 | 8 | splines, including a rational spline; layers |

### 1.4 Not used

- **Flagged (GPL, LGPL, MPL):** these may be used only for local testing and are never committed.
  - Voron-2 and Voron-Trident: GPL-3.0, 21 DXF (Fusion panels; AutoCAD Mechanical drawings with DIMENSION, HATCH and
    LEADER).
  - LibreDWG test data: GPL-3.0, 67 files.
  - LibreCAD symbol library: GPL-2.0, about 1,340 files.
  - QCAD: GPL-3.0, about 1,185 files.
  - Inkscape extensions `tests/data/io`: GPL-2+, 27 files.
  - OpenSCAD `tests/data/dxf`: GPL-2, 31 files.
  - dxf-viewer fixtures: MPL-2.0, 84 files.
- **Excluded:**
  - NC licence: Rat-Rig/V-Core-3 (CC BY-NC-SA, 176 DXF); OpenROV (CC BY-NC-SA, 80 DXF); sendz/keyboard-case;
    splitkb/Zenestra.
  - No licence: notchGenerator (Fusion flat-pattern samples); maker-z/LaserAdjustment (probably a LightBurn DXF export);
    jonnor/projects (35 FreeCAD R12 files); OpenSourceEcology/CEB-Press (LibreCAD nests with 328 dimensions).
- **Gaps:**
  - No openly licensed LightBurn-exported DXF/SVG; the agent makes these locally (PLAN_V1_1.md section 4.1).
  - No Onshape or Rhino files; Onshape needs an account, so it is skipped.
  - SolidWorks files come only from trimesh, with an uncertain model licence.
  - Printables, Thingiverse and OpenBuilds were not checked; their download-without-login rules are unknown, so skip
    them.

### 1.5 Documented export quirks

**Fusion**
- Saving a sketch as DXF also exports construction lines ([hackaday.io](https://hackaday.io/project/161798)).
- Splines stay SPLINE ([Autodesk forum](https://forums.autodesk.com/t5/fusion-support-forum/export-dxf-with-spline-for-inkscape/td-p/7658645)).
  Flat-pattern export has "Turn Splines to Polylines", default 0.004 in ([SendCutSend](https://sendcutsend.com/blog/4-ways-to-export-a-dxf-from-fusion-360/)).
- Flat patterns:
  - bend and extent lines go on their own layers;
  - extrusion (0,0,−1) mirrors ARC/CIRCLE/LWPOLYLINE but not LINE/SPLINE;
  - bend lines stop short of the edge ([notchGenerator README](https://github.com/SanchakGarg/notchGenerator)).
- Sketch text is construction geometry by default and is dropped unless exploded ([LightBurn forum](https://forum.lightburnsoftware.com/t/using-files-from-fusion-360/32203)).
- Gaps appear in Deepnest; raising its tolerance from 0.005 to 0.5 fixed them ([Langmuir forum](https://forum.langmuirsystems.com/t/fusion360-dxf-to-deepnest-io-file-corruption/14133)).
- One entity per sketch curve (seen in MeArm v2: 389 LINE, 235 ARC).

**LightBurn**
- DXF layers are ignored; operations are assigned by colour only ([forum](https://forum.lightburnsoftware.com/t/dxf-import-and-layers-5-in-acad-results-in-1-in-lb/42020), [palette](https://docs.lightburnsoftware.com/LayerColors.html)).
  Custom colours snap to the DXF colour index ([forum](https://forum.lightburnsoftware.com/t/dxf-import-map-layers-to-colors/135913)).
- Auto-Join closes gaps up to 0.05 mm; Delete Duplicates, Close Path with tolerance and Optimize Shapes also exist.
  Text becomes shapes on export, and bitmaps are exported to SVG only ([Menus doc](https://docs.lightburnsoftware.com/UI/Menus.html)).
- Imported splines and circles become short segments ([forum](https://forum.lightburnsoftware.com/t/dxf-import-circle-is-broken-into-small-segments/50968)).
- Exported DXFs carry no units; there is a "Convert Arcs to Lines" export option ([forum](https://forum.lightburnsoftware.com/t/dxf-files-exported-from-lightburn-will-no-longer-import-into-fusion-360/103776)).
- LightBurn exports taken into Deepnest: the SVG loses its holes and the DXF comes in smaller ([forum](https://forum.lightburnsoftware.com/t/svg-or-dxf-export-and-nesting-problem-holes-in-svg-size-in-dxf-deepnest-1-0-5-lightburn-1-2-0/74249)).
- Dimensions and hatches are not imported ([forum](https://forum.lightburnsoftware.com/t/dxf-import-text-dimensions-hatch/58263)).
  Hatches import only from R12/R13 ASCII ([forum](https://forum.lightburnsoftware.com/t/dxf-hatches-not-importing/141840)),
  and solids are ignored ([forum](https://forum.lightburnsoftware.com/t/dxf-not-importing-layers/189177)).

**General**
- Deepnest DXF issues #204, #160 and #149 (scale), #169 (SolidWorks), #155 and #157 ([issues](https://github.com/Jack000/Deepnest/issues?q=dxf)).
- Onshape flat patterns put holes on the outline's layer, split bends over two layers and cut layer names at 26
  characters. Onshape also exports hidden edges ([forum](https://forum.onshape.com/discussion/19996)).
- Inkscape moved from 90 to 96 DPI in 0.92 ([release notes](https://wiki.inkscape.org/wiki/Release_notes/0.92)).
- ezdxf recover repairs damaged files only partly ([docs](https://ezdxf.mozman.at/docs/drawing/recover.html)).
- Seen in files:
  - geometry wrapped in one block plus one INSERT;
  - files with no HEADER;
  - a near-zero coordinate 0.00999928 (OpenSCAD);
  - the ANSI_936 codepage and cm units;
  - dimensions and hatches left inside production nests.

## 2. LightBurn `.lbrn2`

### 2.1 Structure

There is no official schema. LightBurn staff call the format [undocumented](https://forum.lightburnsoftware.com/t/is-lightburn-file-format-lbrn2-documented-or-open-sourced/56221).

**Root:** `<LightBurnProject AppVersion FormatVersion MaterialHeight MirrorX MirrorY [DeviceName]>`. Its children:
- `Thumbnail Source=<base64 PNG>`;
- `VariableText`;
- `UIPrefs`: `Optimize_*` entries, each with a `Value` attribute;
- `CutSetting`, `CutSetting_Img`, `Shape`;
- `Notes`.

Example: [printable_area_jig.lbrn2](https://github.com/JTCozart/LightBurnTemplates/blob/main/printable_area_jig.lbrn2).

**CutSetting (layers):**
- The `type` attribute is Cut, Scan, Scan+Cut, Offset or Tool; image layers use `CutSetting_Img type="Image"`.
- Fields are child elements of the form `<field Value=""/>`: `index`, `name`, `priority`, `speed`, `maxPower`, `kerf`,
  `numPasses`, `tabsEnabled`, `doOutput` and more.
- Tool layer T1 is index 30.
- boxes.py writes a capital `Type="Cut"`, so match the attribute case-insensitively.
- A shape's `CutIndex` matches a layer's `index`.

**Shape types:**

| Type | Attributes | Geometry |
|---|---|---|
| Rect | W H Cr Locked | centred on the local origin |
| Ellipse | Rx Ry | centred on the local origin |
| Path | VertID PrimID | `VertList`, `PrimList` |
| Group | optional CutIndex | `<Children>` |
| Text | Font Str H LS LnS Ah Av Weld HasBackupPath | `<BackupPath Type="Path">` with its own XForm |
| Bitmap | W H Gamma … SourceHash Data | base64 PNG |
| Polygon | Rx Ry N | seen only in MeerK40t's reader |

**XForm:**
- Six numbers `a b c d e f`, with x' = a·x + c·y + e and y' = b·x + d·y + f (Qt m11 m12 m21 m22 m31 m32).
- A shape's own XForm applies first, then each enclosing group's ([forum](https://forum.lightburnsoftware.com/t/lbrn2-file-documentation/52174)).
- Units are mm (inferred).
- Y points up (strongly inferred from [lbrn2-to-svg](https://github.com/jlucaso1/lbrn2-to-svg) and boxes.py).
- `MirrorX`/`MirrorY` record the machine origin corner. Sources disagree on the mapping
  ([LaserPost](https://github.com/nuCarve/laserpost/blob/main/src/lightburn.js) vs the forum), so **verify** locally.

**VertList grammar:**
- Each vertex is `V<x> <y>`, optionally followed by `c0x<n>c0y<n>c1x<n>c1y<n>` (no spaces), optionally followed by `S`
  (smooth).
- `c0` is the outgoing Bézier handle and `c1` the incoming one ([staff](https://forum.lightburnsoftware.com/t/lbrn-or-lbrn2-xml-file-docuumentation/42317)).
- A handle exists only if both its x and y are present; `c0x1` or `c1x1` alone means none.
- Numbers may use exponent form.

**PrimList grammar:**
- `L<i> <j>` is a line and `B<i> <j>` a Bézier, both by vertex index.
- One Path can hold several contours, each closing back to its own start.
- Or a single shorthand: `LineClosed` or `LineOpen`.

**Geometry sharing (critical):**
- The first Path with a given `VertID`/`PrimID` carries the lists.
- Later copies omit `VertList` and/or `PrimList`, independently, and differ only in XForm.
- In public samples, 156 paths reused geometry and 100 defined it.
- Bitmap copies omit `Data` and share by `SourceHash`.
- Sharing arrived in [0.9.21](https://lightburnsoftware.com/blogs/news/lightburn-0-9-21-image-adjustment-window-image-compositing-measure-tool-new-file-format-memory-savings-and-much-more);
  since [0.9.22](https://lightburnsoftware.com/blogs/news/lightburn-0-9-22-released-a-critical-bugfix-and-a-few-small-tweaks),
  `.lbrn` files skip it.

**Legacy `.lbrn`:**
- `FormatVersion="0"`, or no attribute at all in 0.9.07.
- Path geometry is `<V vx vy c0x c0y c1x c1y/>` and `<P T="L|B" p0 p1/>` elements inside the Shape.
- `.lbrn` is meant to be readable, `.lbrn2` compact ([staff](https://forum.lightburnsoftware.com/t/is-lightburn-file-format-lbrn2-documented-or-open-sourced/56221)).

**Versions:**
- `.lbrn2` arrived in 0.9.21 (March 2021) and is the default.
- Every sample from 0.9.24 to 2.0.05 has `FormatVersion="1"`.
- 2.0.05 adds UIPrefs `CutOrigin`, `AlignH/V` and `Optimize_CutSelected`; 1.7+ adds `DeviceName`.
- 2.2's multi-page projects have an undocumented encoding.

### 2.2 Open-source readers and writers

| Project | Licence | Language | Notes |
|---|---|---|---|
| [lbrn2-to-svg](https://github.com/jlucaso1/lbrn2-to-svg) | MIT | TypeScript | The most correct reader: resolves VertID/PrimID, LineClosed, groups, bitmaps and BackupPath text; flips Y. Use as an independent check. |
| [MeerK40t lbrn.py](https://github.com/meerk40t/meerk40t/blob/main/meerk40t/extra/lbrn.py) | MIT | Python | Reads both formats; does not follow VertID/PrimID reuse. |
| [rayforge importer](https://github.com/barebaric/rayforge/blob/main/rayforge/image/lightburn/importer.py) | MIT | Python | Does not follow shared VertIDs; mishandles BackupPath. |
| [lbrnts](https://github.com/tscircuit/lbrnts) | MIT | TypeScript | Read/write, but not lossless (its PrimList writer renumbers primitives); its format notes are AI-generated and unreliable. |
| [LaserPost](https://github.com/nuCarve/laserpost) | MIT | JavaScript | Fusion post-processor writing FormatVersion-0 `.lbrn`. |
| [boxes.py](https://github.com/florianfesti/boxes/blob/master/boxes/drawing.py) | GPL-3.0 | Python | Writes lbrn2 (`--format=lbrn2`): a group per part, `LineClosed`, Text, Notes. Its outputs are a source of test files; never copy its code. |
| [laser-layout](https://github.com/bdfinst/laser-layout) | no licence | — | Prior art: imports lbrn2 and writes a new file with one Cut layer, so the original layers are lost. Never reuse its code. |
| `Dcs102/lightburn` | — | — | A decompile of the LightBurn binary. **Never open it.** |

### 2.3 Permissively licensed sample projects

| Source | Licence | What it has |
|---|---|---|
| [JTCozart/LightBurnTemplates](https://github.com/JTCozart/LightBurnTemplates) | Unlicense | dice_tray (shared geometry, groups), ZippoLighter, printable_area_jig (1.4.03); 17 files |
| [qbalsdon/etcher](https://github.com/qbalsdon/etcher) | MIT | 11 files |
| [lbrn2-to-svg fixtures](https://github.com/jlucaso1/lbrn2-to-svg/tree/main/tests/artifacts) | MIT | 14 small 1.7.08 files with expected SVGs (minimized by script) |
| [rayforge assets](https://github.com/barebaric/rayforge/tree/main/tests/image/lightburn/assets) | MIT | includes a legacy `.lbrn` |
| [Mothbox_Hardware](https://github.com/Digital-Naturalism-Laboratories/Mothbox_Hardware) | MIT | real multi-part layouts |
| [benkrasnow/MOPA_Laser_Stainless_Colors](https://github.com/benkrasnow/MOPA_Laser_Stainless_Colors) | MIT | 10 Scan layers |
| [eMaxDH/OpenSCAD-Cutter-Lib](https://github.com/eMaxDH/OpenSCAD-Cutter-Lib) | MIT | several sheets, MirrorY=True |
| [opatiny/micromouse](https://github.com/opatiny/micromouse) | CERN-OHL-P-2.0 | repeated parts with shared geometry |
| [acwright/6502-COB](https://github.com/acwright/6502-COB) | CERN-OHL-P-2.0 | about 20 plates, LightBurn 2.0.05, MirrorX/Y=True |
| [ValveTester](https://github.com/olivergardiner/ValveTester), [CL650-DCPCCP](https://github.com/rispeed/CL650-DCPCCP) | CC0 | |
| [MarcinZukowski/lightburn-tester](https://github.com/MarcinZukowski/lightburn-tester) | Apache-2.0 | legacy `.lbrn` from 0.9.16 |

lbrnts's test assets were copied from other repositories, so its MIT licence may not cover them; don't use them.

### 2.4 LightBurn features that matter to Nestbolt

- **Quick Nest** (2.1, [docs](https://docs.lightburnsoftware.com/2.1/Reference/QuickNest/)): packs bounding boxes into
  an axis-aligned rectangle.
- **True Nest** (2.2 early access, 2026-09-16; Pro only;
  [docs](https://docs.lightburnsoftware.com/2.2/Reference/Nesting/TrueNest/)): nests by real outline. The docs don't say
  whether it places parts inside holes.
- **Nest Selected** ([docs](https://docs.lightburnsoftware.com/2.1/Reference/NestSelected/)): round-trips through
  SVGnest.com.
- **Per layer** ([Line Mode](https://docs.lightburnsoftware.com/2.1/Reference/CutSettingsEditor/LineMode/)):
  - lead-in/out: length, angle (positive outside, negative inside), line or arc; not available on galvo lasers;
  - Kerf Offset: closed shapes only, stored as `kerf`;
  - Overcut and Tabs.
- **Start point:** a Set Start Point tool. Unless "Choose best starting point" is on, the start is the shape's first
  point ([docs](https://docs.lightburnsoftware.com/latest/Reference/SetStartPoint/)).
- **Unknown:** the file field names for lead-in settings and start points; make samples locally to find out.
- **Optimization settings** are stored in the project's `UIPrefs`
  ([docs](https://docs.lightburnsoftware.com/2.0/Reference/OptimizationSettings/)), including "Remove overlapping lines".
- **DXF import:**
  - Layers come from colours matched to the 32-entry palette (00-29, T1, T2)
    ([docs](https://docs.lightburnsoftware.com/LayerColors.html)); layer names are ignored and white becomes black.
  - Import settings: auto-detect units, auto-close tolerance, Ignore Text Objects
    ([docs](https://docs.lightburnsoftware.com/2.1/Reference/SettingsPreferences/)).

## 3. Common-line cutting and lead-ins

### 3.1 deepnest-next `mergeLines` (local checkout 1e7ba6e)

- **Licence:** the top-level LICENSE is MIT, but `main/deepnest.js` is GPLv3 (header and LICENSES.md). Describe its
  behaviour only; never copy its code.
- **Defaults:**
  - worker (`main/deepnest.js:11-25`): spacing 0, curveTolerance 0.3, mergeLines true, timeRatio 0.5, 72 units per
    inch;
  - UI (`build/ui/services/config.service.js:11-35`): curveTolerance 0.72, placement "box".
- **Spacing must be 0:**
  - The UI says so (`main/index.html:760-762`).
  - An edge counts only if both its endpoints are flagged exact (`background.js:370-372, 405-407`).
  - With spacing above 0, the parts are Clipper offsets with no such flag, so the merged length is always 0
    (`deepnest.js:1020-1055, 1402-1413`).
  - Sheet edges are never counted; holes are (`background.js:1677-1679, 481-485`).
- **Tolerance and minimum length:**
  - Collinear when both ends lie within 0.1 × curveTolerance, about 0.025 mm at the UI default
    (`background.js:424, 1687`).
  - Minimum 0.5 in (12.7 mm), applied to each edge and to the overlap (`:377, 411, 467, 1684`).
- **Fitness:**
  - `area -= mergedLength × timeRatio` per candidate position (`:1689`).
  - "area" is width × 5 + height in gravity mode, width × height in box mode, and hull area in hull mode
    (`:1558, 1561, 1628`), so a length is subtracted from an area.
  - In gravity mode it only breaks ties between equal widths (`:1695-1698`).
- **Export** (`export.service.js:398-418`, `svgparser.js:244-603`):
  - Flattens the SVG, so per-part groups are lost.
  - Splits every straight segment, removes duplicates and fuses overlaps.
  - Re-chains the result into open paths, all black, with no separate layer.
- **No kerf compensation:** each shared edge loses half a kerf
  ([Langmuir forum](https://forum.langmuirsystems.com/t/sheetcam-question-on-nesting/11188?page=2)).
- **Its DXF export uploads the SVG** to `converter.deepnest.app` (`build/ui/types/index.js:8`). Never use it: that would
  break the no-upload rule. Compare with deepnest-next's SVG export only.

### 3.2 Industry practice

- ProNest has Pair, Quad, Array, snap-together and plate-edge common-line cutting
  ([Hypertherm](https://www.hypertherm.com/en-US/resources/spark-the-blog/common-line-cutting)).
- Kerf is compensated in software, and parts are spaced exactly one kerf apart:
  - Kinetic Primecut cuts the shared line with machine kerf set to none
    ([Primecut](https://kineticusa.com/PrimecutHelp/common-line-and-common-crop-cu.html)).
  - FastNEST: part spacing = kerf, software compensation
    ([FastCAM](https://response.fastcam.com/knowledge-base/article/kerf-compensation-from-fastcam-or-fastnest_1)).
  - CypCut joins edges within 0.1 mm.
- **Risks:**
  - plasma has a good and a scrap side;
  - piercing on a part edge can damage it;
  - cut direction affects bevel ([US10195682B2](https://patents.google.com/patent/US10195682B2/en));
  - small parts can tip ([OSH Cut](https://www.oshcut.com/design-guide/understanding-micro-joints)).
- **What CAM expects:**
  - SheetCam offsets closed contours only; open paths are offset to the right of the start (manual v3.1.17, pp. 61-62).
  - LightBurn's Kerf Offset works on closed shapes only; "Remove overlapping lines" dedupes within a distance.
- **Who offers it:**
  - yes: ProNest, SigmaNEST (after NC), Lantek, FastNEST, Primecut, CypCut, deepnest-next;
  - no: SVGnest, SheetCam (chain cuts only), LightBurn (dedupe only).

### 3.3 Lead-ins

- **Who draws them today:**
  - LightBurn per layer (line or arc; angle, length; overcut), since at least 0.9.07
    ([forum](https://forum.lightburnsoftware.com/t/lead-in-lead-out-advices/6897));
  - SheetCam (arc, perpendicular and ramp; moves start points until the leads fit);
  - Fusion CAM (drops passes whose leads don't fit);
  - CypCut ("Check Lead" shortens leads that cross);
  - FireControl: none.
  - Nesting tools: ProNest moves leads away from cut profiles; Primecut has nest-friendly hook leads; SigmaNEST adds
    leads after nesting; Deepnest and SVGnest: none.
- **Typical values:**
  - Thermal cutting: lead length at least the material thickness
    ([US20220055141A1](https://patents.google.com/patent/US20220055141A1/en)).
  - Laser: 2-4 mm under 3 mm thick, 4-6 mm for 3-6 mm; angle 15-45°; overcut 2-3 mm
    ([Thunder Laser](https://www.thunderlaser.com/laser-wiki/laser-parameters-guide/laser-cutting-lead-in-lead-out-overcut.html)).
  - Plasma holes: a straight 90° lead on a rigid machine, an arc with backlash; no lead-out on holes
    ([Hypertherm, Jim Colt](https://forum.linuxcnc.org/media/kunena/attachments/20660/hyperthermholes.pdf)).
  - Waterjet: radius 0.05-0.1 in, sweep 45-60° ([Purdue](https://www.purdue.edu/bidc/?p=2912)).
- **Placement:** corners first, shortening to fit, with a pierce allowance clear of other cuts
  ([Primecut](https://kineticusa.com/PrimecutHelp/automatic-lead-placement.html)).
- **Format:** there is no DXF entity for a lead; a drawn lead is open LINE/ARC geometry. LightBurn assigns layers by
  colour.
- **Nestbolt today:** its DXF has only CUT and SHEET layers and no colours (`crates/core/src/export.rs:224-364`).
