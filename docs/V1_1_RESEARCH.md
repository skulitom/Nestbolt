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

The [N1 native export check](../benchmarks/results/h2-lightburn-20261013T195848Z.md)
now verifies these colours in Nestbolt's own DXF/SVG exports. All ten nested
files import; native saved dimensions agree within 0.000033 mm. The two spline
files show a 0.003275 mm width difference in LightBurn's numeric field despite
preserving the analytic curve width. Native field readings and saved geometry
are therefore recorded separately. No full H2 pass is claimed.

The [render-backed label review](../benchmarks/results/n0-labels-20261013.md)
also establishes a nested text caveat: LightBurn 2.1.01 stores its Text BackupPath
cache in world coordinates, while the Text XForm remains local to its parent.
The published MIT converter double-applies the parent transform in these samples
and skips several unsupported shape/sharing cases. See LBRN2.md before using it
as an oracle; a converted SVG alone is not a completeness check.

The [controlled preserving-writer probes](../benchmarks/results/h3-native-probe-20261013T224854Z.md)
confirm moved and rotated editable Text follows its live transform despite an
unchanged BackupPath cache; native Save As refreshes the cached world transform.
A re-homed bitmap copy renders correctly. All four saved origin flag combinations
keep the same numeric placement in a bottom-left device, and both source-origin
variants tested in a top-right device retain those coordinates while the device
axes reflect the display. Native Save As rewrites the flags to the active device.
All ten geometry checks pass, but its bitmap-only save also renumbers image-layer
priority from 3 to 0. That difference is retained; this is not full H3 acceptance.

**Training-label discrepancy found during N1:** the apparent enclosed island in
the Iris PE switch plate's R43 label is a polygonization artefact of duplicated
cutout vertices differing by 6.96e-13 mm. The [reproduction report](../benchmarks/results/h2-r43-label-discrepancy-20261013.md)
preserves the source and frozen label and explains the diagnosis. Artem approved
a [documented scoring exception](../benchmarks/results/h2-r43-scoring-exception-20261013.md)
on 2026-10-13: the exact hash-scoped case scores one part with 37 holes. The
original label, split and raw failed result remain unchanged.

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
- `MirrorX`/`MirrorY` record the machine origin corner. The original sources disagreed
  ([LaserPost](https://github.com/nuCarve/laserpost/blob/main/src/lightburn.js) vs the forum).
  [Local saved projects](LBRN2.md#coordinate-systems-and-origins) establish bottom-left=False/False,
  top-left=False/True, top-right=True/True and bottom-right=True/False. The native
  writer probes above confirm numeric placement uses the active device axes;
  do not apply these flags again as a per-shape transform.

**VertList grammar:**
- Each vertex is `V<x> <y>`, optionally followed by `c0x<n>c0y<n>c1x<n>c1y<n>` (no spaces), optionally followed by `S`
  (smooth).
- `c0` is the outgoing Bézier handle and `c1` the incoming one ([staff](https://forum.lightburnsoftware.com/t/lbrn-or-lbrn2-xml-file-docuumentation/42317)).
- **Corrected by native evidence, 2026-10-13:** a lone `c0x1` or `c1x1` means none, but another lone x value or a lone y value denotes a handle whose omitted coordinate is zero. The earlier inference that both coordinates must be present was wrong. Native lb-02 through lb-05 SVG exports confirm eight affected shapes; see [the reader checkpoint](../benchmarks/results/h3-reader-checkpoint-20261013.md).
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
- **Nestbolt at plan writing:** its DXF had only CUT and SHEET layers and no colours.
  N1 now exports the verified palette and accepts existing review paths; N4/N5
  generation remains pending (`crates/core/src/export.rs`).


### N0 public-project verification (2026-10-13)

The [44-project native reference review](../benchmarks/results/n0-public-labels-20261013.md)
confirms all exported reference vectors and 151 image rectangles within 0.01 mm.
The published MIT converter requires documented reference-input normalization for
Group Y reflections, world-space text caches, compact primitives, Polygon and
shared bitmap data. Hidden layers may be absent from native SVG. Native re-save
can also change legacy Scan+Cut to Scan and generate missing text backups; it is
not evidence of lossless XML preservation. Original source XML remains authoritative.
See [local observations](LBRN2.md#public-project-reference-normalization-and-native-export-limits).


### N2 surface integration evidence (2026-10-13 UTC)

The [authored-fixture surface checkpoint](../benchmarks/results/h3-surfaces-20261013T233512Z.md)
now exercises real search through CLI, MCP and both browser engines. Per-sheet
LBRN2/ZIP output retains text caches, shared Bitmap data, rigid disconnected
groups and settings; original XML drives independent validation. The native
reader/writer observations above remain the format evidence. Surface tests do
not establish H3's five searched native projects or cut-settings dialogues.
Legacy output, uncached movable text and groups mixing fixed and active artwork
still need completion. The latter fail clearly at public import because keeping
the entire group fixed would otherwise leave active geometry outside the check.

### N2 legacy conversion evidence (2026-10-14 UTC)

The [native legacy-format check](../benchmarks/results/h3-legacy-20261013T235803Z.md)
confirms that FormatVersion 1 requires compact path lists. Original legacy V/P
elements can remain alongside them without extra cuts, preserving unknown XML.
Native saves of the original legacy project and Nestbolt's converted identity
sheet are canonically identical. Partial controls and absent-handle markers
are preserved. CLI, MCP and both browsers now exercise this conversion.

Native LightBurn silently ignores a new T1 setting/rectangle appended after
Notes; the writer now puts settings before shapes and the outline before trailing
metadata. The failed and corrected native results are retained. All original
settings remain exact; native normalization of the newly generated T1 name and
priority is recorded separately. This completes the legacy output implementation,
not the five-project H3 gate or the remaining uncached-text/mixed-group cases.


### N2 five-project native evidence (2026-10-14 UTC)

The [five actual searched projects](../benchmarks/results/h3-lightburn-20261014T001636Z.md) complete the native H3 opening,
position/size and cut-settings-dialogue requirement: 16 units, both device
origins, shared images/vectors, groups, editable cached text, kerf and leads.
All 23 original settings remain exact; 34 paired dialog pages check 648 controls.
The independent native reference covers 409 leaves/537 contours with maximum
point/bounds errors below 0.000530 mm. Native UI fields differ by at most
0.003652 mm on the curved mirrored probe. Initial observation/association
failures are retained, and the device/desktop state was restored. This does
not resolve uncached Text, mixed fixed/active groups, or full H3 acceptance.


### Text portability and native repair evidence (2026-10-14 UTC)

[LightBurn documents backup paths](https://docs.lightburnsoftware.com/legacy/UI/FontsAndText)
as the saved geometry used when the original font is unavailable. The
[training audit](../benchmarks/results/h3-text-cache-20261014T005902Z.md) finds
122 uncached Text objects in eight originals; all cached native re-saves pass
477 leaf / 1,223 contour comparisons within 0.000500 mm. A font name does not
identify exact portable geometry. Native Save As also changes settings, so the
repaired references cannot replace frozen originals in a lossless-round-trip
claim. Requiring repair before geometry acceptance is proposed, not approved.


### N3 engine experiment and separator overflow (reviewed 2026-10-15)

The [2026-10-14 jagua-rs 2.0 spike](../benchmarks/results/jagua-2-spike-20261014.md)
compares a locally ported Nestbolt/Sparrow build with pinned 1.1.0 on twelve
v1 development jobs. Eight of twelve repeatable layouts are identical, with
median 1.50x speed-up for those eight. Short wall-clock runs show a median
1.70x separator-evaluation rate, against 1.01x in the identical-build control.
Four repeatable layouts diverge, and the faster debug build exposes upstream
Sparrow's infinite-weight assertion. These are recorded experimental findings,
not browser measurements, a completed H4 gate, or a new published quality claim.

The report and its raw JSON are preserved byte-for-byte from `c691aed` on
`spike/jagua-2`. The experimental dependency/solver port remains on that branch;
production still uses jagua-rs 1.1.0 and Sparrow `4629b22`. A future port needs
compatible upstream versions, repeatable-work recalibration and the full H4
checks. Published v1 results and held-out isolation remain unchanged.

The independent [weight-ceiling fix](../benchmarks/results/separator-weight-cap-20261014.md)
from `83aa089` is integrated. Its 138 recorded development layouts all pass the
standalone validator; 64/65 layouts remain identical at 60 work-seconds. The
four 300-work-second pairs ran on CCD1, a recorded deviation from the plan's
CCD0 benchmark placement; they support the overflow diagnosis, not a speed gate.
The cap applies to Nestbolt's separator only. Delegated upstream Sparrow still
uses its pinned original implementation; its [issue draft](upstream-drafts/sparrow-gls-weight-overflow.md)
is preserved and has not been posted. The reported bound is for shop-scale
geometry, not a proof over every coordinate accepted by the public validator.


### Native arc-length definition (2026-10-15)

[Three authored calibration previews](../benchmarks/results/h6-lead-native-calibration-20261015.md)
show LightBurn Pro 2.1.01 interpreting arc length literally: 3 mm at 45° has
radius about 3.82 mm; 3 mm at 90° has radius about 1.91 mm. Both reject the
plan's original 1.5 mm radius. Artem approved matching LightBurn's definition
([decision 3](PLAN_V1_1.md#10-reviewed-decisions)). The audit uses a 0.05 mm
raster tolerance and preserves native projects/settings/screenshots. This is
calibration on an outer straight edge, not H6's three searched-export checks.
Hole, corner, direction and zero-angle behavior still need native coverage.

### Native lead setting precision and separate layers (2026-10-15)

The [mixed-settings follow-up](../benchmarks/results/h6-lead-settings-checkpoint-20261015.md)
imports an actual searched public SVG, assigns its contours to native layers,
and preserves the six original contours and starts. LightBurn Pro 2.1.01 in mm
accepts one decimal place for lead length and displays two for angle. Setting
1.162 mm through the native control produces and saves 1.2 mm. The earlier
three-decimal report assumption is therefore superseded: round each trial down
to 0.1 mm before constructing and validating its paths; reject angles needing
more than two decimal places. The original input attempt and saved project stay
in the evidence folder.

Two native previews verify outer +45°/3.0 mm settings and separate hole −90°
settings (1.7 mm line, 1.2 mm arc), with native leads off on flagged 0.4 mm holes.
All 12 saved native contour starts/outlines match the public exports within
0.00000224 mm. Raster samples of all eight leads match a reserved direction
within 0.026764 mm under the declared 0.075 mm raster tolerance. This supports
the preview observation, not the independent 0.01 mm vector clearance gate.
The earlier [three searched coupons](../benchmarks/results/h6-lead-planner-checkpoint-20261015.md)
cover outer corners, holes and reversal; zero-angle native coverage and broader
H6 acceptance remain unfinished. No held-out geometry was used.

### Independent lead source validation (2026-10-15)

The [source-validation checkpoint](../benchmarks/results/h6-lead-source-checkpoint-20261015.md)
rebuilds coverage from placed original contours and evaluates their source
segments independently of the planner. Bernstein polynomial evaluation and
bounded subdivision cover quadratic/cubic Béziers; elliptical arcs use a second
derivative chord-error bound. Physical flattening tolerance is 0.0001 mm and
attachment tolerance is 0.000008 mm. Owner material is rebuilt from those source
curves, and each supplied lead's stroke and pierce are checked against it.

A mixed-curve regression also exposed a 0.000000001010 mm² sliver lost by rounded
polygon union. The collision export now retries strict containment with the
kernel's two-grid (0.000002 mm) outward margin when necessary. Larger missing
material remains an error; the validator's zero-outside-area requirement is
unchanged. This is a containment repair, not a relaxed area tolerance or a
performance/material-cost claim. Multipart planning and broader H6 acceptance
remain pending.


## Local update — grouped lead cutting files (2026-10-15)

Artem approved [plan decision 4](PLAN_V1_1.md#10-reviewed-decisions): new contour starts and LEADIN review paths belong in separate SVG/DXF cutting files, while the editable LBRN2 retains its original starts/settings. The [authored group/native check](../benchmarks/results/h6-lead-group-checkpoint-20261015.md) confirms preserved children/settings and native import of disconnected cuts, holes, an island and open paths. All thirty native contour comparisons and sixteen closed-contour starts pass the 0.01 mm tolerance. This is local format/feature evidence, not an allowance-cost benchmark or H6 completion. Engraving and image bounds are protected artwork, never cutting-file geometry.


### Local update — 2026-10-15: H6 material costs and gate closure

The [completed H6 evidence](../benchmarks/results/h6-complete-20261015.md) now includes all 156 layouts on the frozen 13-job development set, both kerfs and three seeds. Default lead allowances add median material costs of +1.0696% (0.2 mm laser) and +6.0951% (1.5 mm plasma), measured against the same common-line workflow without leads. Plasma small-hole flags remain explicit; this is not a promise of automatic leads for every contour. One report-order comparator error was resolved on the same saved layout with unchanged numerical tolerance; original failures remain. Original native coupons and mixed settings revalidate unchanged. H6 is complete and overall v1.1 completion is 20%; no published v1 quality claim or held-out allocation changes.

### 2026-10-15: common-line placement bonus development result

The [first 13-job bonus pilot](../benchmarks/results/h5-common-bonus-checkpoint-20261015.md)
uses normalized saved cutting length in a local placement cost, off by default.
All 78 layouts validate. At ten seconds and seed 0, median cut savings are
13.12% laser and 13.43% plasma; median material cost is zero, but three jobs per
kerf exceed +1% relative to ordinary nesting. Normal mode places 21 and 49 copies
inside holes in the two mechanical jobs, which common-line mode intentionally
forbids. This distinction must remain visible in the full H5 comparison; the
pilot does not relax the material gate or complete H5. Deepnest's zero-spacing
SVG merge comparison and the required 60-second/three-seed measurements remain.


### 2026-10-15: full common-line comparison and material shortfall

The [60-second, three-seed measurement](../benchmarks/results/h5-cutting-development-20261015.md)
retains 234/234 valid Nestbolt layouts and 35/39 valid native Deepnest outcomes.
The four native failures are no-layout results (all three panel-hardware seeds
and batch-500 seed 1), retained and unscored. The comparison calls the pinned
app's public SVG export service, with network requests blocked. Independent
source-line coverage and physical-scale checks distinguish native reported
merged length from actual SVG savings; these values can differ substantially.
Deepnest uses zero spacing and is not kerf compensated.

Nestbolt's median savings are 13.0311% laser and 13.1005% plasma. Median material
cost is zero, but the two mechanical jobs remain above +1%: plates +5.219% /
+4.345%, panel-hardware +6.508% / +5.596% (laser / plasma). Normal mode places
21 / 49 copies in holes in every seed; both common-line arms place none.
The bonus-off arm already has material outliers, so the final alignment phase
alone does not explain them. This is a measured association, not a proof that
better packing under the common-line restrictions is impossible. Every other
job is within +1%. H5 remains open; its material condition is unchanged.

All 273 archives and 3,654 internal recorded files pass hash verification. The
frozen shop inventory remains 1,181 files. The JSON report includes per-job
three-seed medians, inclusive quartiles and failures. Overall completion remains
20% (H1 and H6); no new final acceptance or published v1 claim follows.

### 2026-10-15: two material-search hypotheses rejected

The [48-run mechanical diagnostic](../benchmarks/results/h5-material-probes-20261015.md) tests longer initial repacking and rigid complementary-bracket pairs. All original-job validations pass, with 228,580 filled-outer pair checks independently confirming that holes remain reserved. Both hypotheses worsen every job/kerf median, so neither changes production behavior. Pair preparation is explicitly outside the 60-second search budget; it is exploratory evidence, not H5 acceptance. The original material guard remains open, and no impossibility claim follows from these failed heuristics.

### 2026-10-15: N3 competitor refresh

The official [Sparrow Studio README](https://github.com/JeroenGar/sparrow-studio)
and [application description](https://sparrowstudio.app/) still describe strip
packing without automatic fixed-sheet allocation or nesting inside holes. The
plan's competitor stop condition is not triggered by this check. The official
[Deepnest releases](https://github.com/deepnest-next/deepnest/releases) list
1.5.6. LightBurn's [2.2 feature documentation](https://docs.lightburnsoftware.com/2.2/NewFeatures/)
still places True Nest in Pro; the release directories list
[2.1.04 stable](https://release.lightburnsoftware.com/LightBurn/Release/) and
[2.2.00-RC-6](https://release.lightburnsoftware.com/LightBurn/RC/).
These are a current availability check, not new competitor measurements. The
locally installed LightBurn 2.1.01 trial and all pinned benchmark dependencies
remain unchanged.

### 2026-10-15: early rectangle incumbent exposes browser costs

The [early-start checkpoint](../benchmarks/results/h4-quick-start-20261015.md)
tests the existing rectangle packer before ordinary construction. Six isolated
trials on the frozen curve-heavy job all validate; with existing hole grouping,
500 riders and material 2.2468772308 match the prior long native diagnostic.
The integrated option produces a checked native incumbent at 7.38 seconds.
It is off by default, exposed and saved through UI/CLI/MCP, preserving the
meaning of published v1 settings under the plan's option rule.

Both browsers now finish all 2,000 placements and export their original cutting
geometry, but peak working memory is 2.190/2.123 GB and the largest observed
heartbeat gaps are 2,861.8/1,620 ms. Chrome's repeated live-preview tasks, final
preview task and download-assembly task point to exact-geometry caching and
off-thread ZIP assembly as distinct next hypotheses. Worker memory needs a
separate measurement. Neither proxy simplification nor geometry tolerance was
changed in this experiment.

The original harness fails its final guard because optimized CLI tests rebuild
the validator executable concurrently. Its original outputs and failure remain;
product sources and browser build hashes are unchanged, and separate checks
using a pinned executable confirm both saved layouts and every metric. Future
benchmarks must wait for optimized CLI tests as well as explicit release builds.
H4 is still open on scale, browser quality and the native matrix. No held-out
geometry, gate threshold, default, release or final acceptance changes.

### 2026-10-15: exact preview reuse retained

The [preview-cache comparison](../benchmarks/results/h4-preview-cache-20261015.md)
removes repeated full-vertex extent scans and per-copy SVG path construction.
Bounds use original vertices with bounded orientation caches; weak keys release
old library/layout snapshots. Shared SVG paths retain every component/hole point
and full coordinate precision, with independent matrix/extent tests including
arbitrary rotations and reflection.

Chrome's nesting/preview Long Task falls from 1,608 to 111 ms, and its heartbeat
gap from 2,092.6 to 209.2 ms. Firefox's gap falls from 733 to 370 ms. Both saved
layouts are byte-identical and fresh metrics agree exactly. This is a one-run
development comparison, not the quality matrix. Unlike the prior batch, every
source/asset/validator guard passes. The full browser suite passes 66 enabled
tests; original test and teardown failures remain recorded.

Keep the cache. Two effective workers still peak above 2 GB, and unchanged ZIP
assembly still stalls for 2.8/1.6 seconds. Next measure one worker to distinguish
memory and CPU contention from drawing costs, then move archive assembly off the
main thread. H4 remains open without changing its 1.5 GB / 200 ms limits or any
native solver setting.


### 2026-10-15: background ZIP generation retained; scale still fails

The [worker/archive comparison](../benchmarks/results/h4-background-archive-20261015.md)
first measures one search worker with unchanged product code, then moves ZIP
exports to a short-lived worker at that same setting. The worker encodes each
independently checked cutting file into an immutable Blob piece and returns a
composite ZIP Blob. Output strings, CRC calculation and archive assembly leave
the main thread. All twelve SVG/DXF comparisons are byte-identical, and all
four saved layouts retain the same original geometry and validated metrics.

The export heartbeat gap falls from 2,613.6 to 51.6 ms in Chrome and from 1,621
to 51 ms in Firefox. Whole working sets fall to 1.419/1.368 GB, but Chrome's
private-memory peak remains 1.822 GB during nesting. Firefox's private peak is
1.389 GB, while its nesting heartbeat gap is 202 ms. Both overall scale results
remain failed under the unchanged strict limits. No rounding, excluded phase or
alternative memory definition is used to pass the gate. Timings are single-run
development observations; the unchanged nesting path's faster wall time is not
credited to the export change.

Both source/site/runner/fixture guards and the exact pinned validator executable
pass. All 74 enabled browser tests pass, including byte parity, invalid-layout
rejection and worker cleanup. The old raw results and six check logs remain
archived with hashes. Production worker defaults are unchanged. Next investigate
search-worker memory and Firefox live-preview responsiveness before considering
a default worker heuristic; browser quality and the native matrix remain open.


### 2026-10-15: redundant collision-layout lifetimes reduced

The [memory diagnosis and retained change](../benchmarks/results/h4-layout-lifetimes-20261015.md)
locate Chrome's remaining peak during nesting: its search engine reports
694,157,312 bytes, versus 2,359,296 for the import utility. The sheet-window
search unnecessarily cloned its read-only input sheets and retained a temporary
full-width collision layout. Borrowing those inputs and dropping the temporary
before search reduce Chrome engine memory to 390,266,880 bytes, without changing
geometry, operations, random choices or work coefficients.

Both browsers now pass the frozen scale workflow with one selected worker:
working sets 1.206/1.350 GB, private peaks 1.228/1.277 GB, maximum heartbeat gaps
106.7/184 ms. The unchanged default two-worker policy still fails: working sets
1.573/1.543 GB, private peaks 1.789/1.611 GB and Firefox heartbeat 290 ms. The
one-worker success is kept separate from those failed default-setting results.
All layouts remain byte-identical; 24 SVG/DXF comparisons match exactly.

Eight authored before/after repeatable pairs preserve every result field except
elapsed wall time, and all 16 outcomes validate independently. All 287 workspace
tests and 74 enabled browser tests pass; builds, types, strict lint, formatting
and source guards pass. Three browser archives, the replay archive and original
check logs retain all 181 recorded members with hashes. Next revise the worker
policy from measured complexity, then verify the old G5 workload and continue
H4 quality/native gates. No gate, held-out allocation or published v1 claim changes.


### 2026-10-15: automatic worker policy passes both scale workloads

The [complexity-based policy](../benchmarks/results/h4-worker-policy-20261015.md)
counts all component/hole vertices across requested copies. Dense jobs at
500,000 vertices use one search worker; simpler jobs retain the existing
two-worker cap above 1,000 copies. This is a conservative heuristic, not a
universal memory guarantee. The UI reports the effective count. Native/WASM
bytes, per-worker search defaults and work coefficients are unchanged.

The frozen letters/gears job has 1,418,500 vertices across copies and now passes
with automatic workers and Quick initial layout enabled in both browsers:
working sets 1.198/1.350 GB, private peaks 1.261/1.276 GB, heartbeat gaps 68/176 ms.
Original G5 has 190,500 vertices and retains two workers with quick start off;
it also passes (private peaks 0.822/0.927 GB, heartbeat gaps 47/81 ms). G5 retains
the original all-sheet download, with an additional local Save for independent
validation included in memory/responsiveness telemetry. All four 2,000-part
layouts validate, with exact native metric agreement. H4 layouts and twelve
SVG/DXF comparisons remain byte-identical to the prior one-worker results.

All 80 enabled browser tests pass, four remain opt-in skipped, and types/build
checks pass. Two raw archives preserve 62 members, plus five archived check
logs, with verified CRC/SHA-256. Source/site/runner/fixture/executable guards and
the frozen shop manifest pass. Original failures remain unchanged. Continue the
eleven-job quality subset, full G5 comparison and 195-run native matrix; H4 stays
open and overall completion is 20%. No held-out geometry or gate changes.


### 2026-10-15: reviewed LightBurn repair and grouping prerequisites

Artem approved the [documented text repair prerequisite and mixed-group rejection](PLAN_V1_1.md#10-reviewed-decisions).
Eight original projects lack 122 embedded text outlines; their original XML,
labels, split and failed geometry checks remain unchanged. Native repaired
copies must still pass the full independent geometry comparison. A native repair
save can normalize settings and is not credited as lossless original-project
preservation. The [approval record](../benchmarks/results/h3-reviewed-decisions-20261015.json)
pins each original, label and native reference to its verified hash.

Groups mixing output-enabled artwork with Tool/output-off shapes must reject
with instructions to ungroup in LightBurn and group movable artwork separately.
The lower-level unit/writer API previously retained such a group as fixed while
the public importer rejected it. The guard now lives in unit preparation so both
paths enforce the approved rule. Read-only inspection and original XML remain
available. Dedicated Tool, output-off and nested-group checks retain the rejected
case; the writer-success fixture now uses only fixed children in its fixed group.

Current-build corpus, native-repair and public-interface checks are underway.
No original failed result is relabelled, and H3's other requirements remain open
until the evidence audit is complete. Overall completion remains 20%.


The [completed prerequisite verification](../benchmarks/results/h3-approved-prerequisites-20261015.md)
passes all 56 original no-op checks, 1,550 comparable original leaves, all 477
repaired leaves / 1,223 contours, and 112 canonical output diffs. The original
122 missing text caches are not relabelled as verified. Seven repaired projects
import and produce valid diagnostic layouts; repaired L17 separately rejects a
standalone zero-width open path. Original public import is 45 accepted and 11
clear rejections (six movable-text prerequisites, one mixed group, four without
movable units). Two accepted originals have fixed uncached text with explicit
warnings; their complete geometry evidence still comes from the repaired inputs.
All 290 workspace, 25 optimized CLI and 82 browser tests pass. A verified archive
preserves 4,354 raw members, plus six separately archived check logs. H3 remains
open on the open-line case and the complete requirement audit; completion is 20%.


## N2 open-stroke verification — 2026-10-15 UTC

The [open-stroke checkpoint](../benchmarks/results/h3-open-line-fix-20261015.md) resolves the repaired L17 rejection. Bounding axes narrower than two curve tolerances receive a symmetric conservative footprint; original open paths and cut settings remain exact in the preserving export. The first grid-only attempt still failed on seventeen nearly horizontal strokes and remains archived. All eight native repairs now import, with 477 independently compared leaves and 210 unit footprints. Original training adds 225 independently compared units; 114 canonical diagnostic sheet diffs pass.

L17 nests 73 units on one sheet. Two new native saves preserve 36 open paths in total and pass 93 leaf comparisons within 0.000516 mm. The earlier five native-checked layouts revalidate with unchanged canonical contents apart from sub-picometre top-level XForm replay. All 293 workspace, 26 optimized CLI and 84 enabled browser tests pass. Three frozen native held-out projects remain unevaluated, so H3 is still open and completion remains 20%. Frozen inputs, labels, split and all failures remain intact.


### 2026-10-15: measured H4 development quality

The [complete eleven-job, three-seed comparison](../benchmarks/results/h4-quality-checkpoint-20261015.md) independently validates all 99 native/Chrome/Firefox layouts with exact metric agreement. Firefox passes the subset at +0.486636% median material and +1.211913% worst job; Chrome narrowly fails the median at +1.014665%, although its worst job is +3.301224%. The +1%/+5% thresholds are unchanged. All public-example components and curve clearances are retained, with 18 additional library/request validations. The five-second pilot failures and initial JSON-round-trip assertion remain archived. Full G5 and the 195-run native matrix remain outstanding; H4 is incomplete and milestone completion remains 20%.

### 2026-10-15: missing LightBurn settings and frozen unit labels

The [native missing-settings probe](../benchmarks/results/h3-missing-layer-native-20261015.md) confirms Line defaults at indices 0/1 and Tool at 30/31, including after an explicit Fill document. Native layer priority does carry the intervening order. Nestbolt now applies the geometric defaults consistently to membership, fixed shapes and cutting sidecars while preserving the original XML settings. L36 matches its two-unit frozen label and completes a lead-enabled CLI search with three validated cutting contours.

A fresh 64-input audit preserves every reader payload unchanged and passes 114 canonical sheet comparisons; only L36's writer membership differs from the previous build. All 45 imported originals match exact membership, independently reconstructed physical cut holes, fixed shapes and cutting layers. All eight approved repairs match membership and holes. L42's original layer comparison remains a documented mismatch because native repair changed legacy Scan+Cut to Scan; the repaired source's own settings are preserved. Original failures and labels stay unchanged. Three native held-out projects remain unevaluated; H3 and H2 remain open and completion stays 20%.


### 2026-10-15: H3 requirement review completed

The [complete H3 review](../benchmarks/results/h3-complete-20261015.md) closes N2 under the approved Text repair and mixed-group rules. After training calibration and a committed evaluation plan, all three reserved native projects pass once: 199 leaves / 247 contours, exact membership, physical holes, fixed shapes and layers, nine allowed canonical sheet comparisons and three independently valid actual searches. The maximum point difference is 0.000499846 mm against 0.01 mm; saved and standalone metrics agree exactly. The reserved inputs remain evaluation-only and may not guide product or parameter tuning.

All 59 original projects and eight auxiliary repairs are accounted for. Combined evidence verifies 1,749 comparable original leaves, 477 prepared leaves, 120 canonical diagnostic sheets and 443 units. Current inspection payloads retain the exact bytes used for earlier independent geometry checks. The five native-checked layouts revalidate and re-export with unchanged settings/children/resources; placement replay differs by at most 2.274e-13 mm. All 298 original native evidence files and 1,181 frozen inventory files retain their hashes. Original missing Text geometry and L42's native repair layer mismatch are not relabelled as successes.

H1, H3 and H6 now total **45%**. H2, H4 and H5 remain open. This changes no thresholds, split, published v1 quality claim, release or registry entry. The original failed checks and intermediate incomplete checkpoints remain linked in the completion report.


### 2026-10-15: isolated browser compiler pilot

The [fat-LTO pilot](../benchmarks/results/h4-lto-probe-20261015.md) keeps source and search settings unchanged, and measures both compiler variants on the eleven H4 development jobs at 60 seconds, seed 0, in both browsers. All 44 layouts and eight additional public example validations pass with exact metric agreement. Relative to thin LTO, Chrome median material changes by -0.045601% and charged-work rate by +0.325196%; Firefox changes by +0.094779% material and -3.552800% charged-work rate, with a worst material increase of +3.365375%. These single-seed diagnostics do not justify changing the build. The candidate stays unintegrated; the original bindings/site were preserved and verified. All outputs and both builds are archived. H4 remains open and completion remains 45%.


### 2026-10-15: bounded collision scoring passes the H4 subset

[CPU profiles](../benchmarks/results/h4-browser-profile-20261015.md) identify weighted collision scoring as 54.915851% of letters' sampled time. Gear-1 remains dominated by edge/quadtree work and has an explicit 17.707883-second sampling gap. The [bounded-score implementation and full comparison](../benchmarks/results/h4-score-pruning-20261015.md) retain exact reference arithmetic and reject only already-worse partial scores. All eight candidate equal-work comparisons match the baseline exactly across two executable variants; geometry, randomness, work coefficients and search settings are unchanged.

All 99 native/Chrome/Firefox layouts and 18 extra public example checks validate with exact metric agreement. Chrome passes the original +1% median/+5% worst subset bounds at +0.710335% / +3.316424%; Firefox passes at +0.664508% / +3.268252%. The scoring change is retained. All 297 workspace, 26 optimized CLI and 84 enabled browser tests pass. Mixed short native timings establish no speed gain; historical seed-0 browser charged-work-rate increases are trajectory-dependent diagnostics. The original failed subset and the report-only archive-inventory error remain preserved.

Full G5 development quality, the 195-run native comparison against frozen 75cbb32 and current-build scale confirmation remain outstanding. The older M4 binary and final seeds are not substitutes for that development comparison. H4 stays open and completed weight stays 45%.

### 2026-10-15: common-line final-sheet assignment inspection

[Read-only inspection of twelve retained H5 median layouts](../benchmarks/results/h5-last-sheet-inspection-20261015.md) verifies every source archive and used job/layout hash. For one 0.2 mm large-plates bonus assignment, even filled outer area divided by gross sheet area exceeds the material guard. Compressing that same final sheet cannot pass; changing its assignment may. The other weak bounds do not prove packability. This supports a future exchange strategy while preserving holes, validity and the deadline. No new searches, relaxed threshold or H5 completion claim.


### 2026-10-15: current-build browser scale confirmation

[All four scale workflows pass](../benchmarks/results/h4-current-scale-20261015.md) on the retained bounded-score build. The required 2,000-part letters/gears drawing uses one automatic search worker with Quick initial layout enabled; original G5 uses two with that option off. Chrome/Firefox curve-heavy working-set peaks are 1.257/1.352 GB, private peaks 1.223/1.275 GB and maximum heartbeat gaps 87.8/175 ms. G5 peaks and pauses also pass. Firefox's Long Tasks API is unavailable; its conservative UI heartbeat remains the responsiveness evidence.

All four layouts independently validate, with exact metrics. Curve-heavy layout bytes and all twelve SVG/DXF exports match the earlier passing worker-policy measurement. Two verified archives preserve all 68 raw members. The complete 65-job development matrix has started under its committed plan, with 699 new attempts plus 81 matching reused results. Temperature providers returned no reading; 4201 MHz is a clock observation, not thermal evidence. H4 remains open and completion remains 45% until the full comparisons and requirement audit pass.


### 2026-10-15: remaining native import messages and exchange scope

[Review of all 56 training native originals](../benchmarks/results/h2-native-warning-review-20261015.md) identifies missing explanatory messages in twelve accepted projects: bounding-rectangle use in all twelve, plus line fallback in L28 and cached-text use in L40. The archived public payloads and labels are hash-verified, and importer code is unchanged since their measurement. Fourteen fixed-shape and two fixed uncached-text expectations are covered; eleven clear original rejections stay separate. The diagnostic gaps do not change geometry or H3 preservation, and font availability must not be inferred. Implement messages after the running H4 comparison; H2 remains open.

[H5 source inspection](../benchmarks/results/h5-last-sheet-inspection-20261015.md) finds existing direct insertions, receiver-only relocation and global swaps. A directed exchange with a smaller blocker is a distinct, unmeasured possibility; ordinary swaps already exist. Preserve quantities, hole reservations, valid incumbents and the shared deadline in any later experiment. No product or benchmark change was made during this review.


### 2026-10-15: current vector export fidelity replay

[Current public import/export replay](../benchmarks/results/h2-export-replay-20261015.md) verifies all 246 accepted training vectors against saved layouts and original options, with identical imported geometry and valid current exports. Of 492 outputs, 491 are byte-identical. One Iris SVG retains its failed byte comparison; a separate independent segment comparison bounds its source difference at 0.000491918 mm, within the unchanged 0.01 mm gate. Its changed endpoints move by 0.000001 mm (one nanometre). The original failed check, unit-wording correction and both versions of every output are retained in a verified 3,942-member archive.

This is a functional regression check on CCD1, with no new nesting or held-out evaluation, and closes the current vector-export concern after the lead/sidecar changes. Historical raw-file hashes were first recorded by this replay, with case-result equality to the committed old report; no earlier sealing is claimed. Native diagnostic messages and remaining reserved acceptance keep H2 open at 45% overall completion.

### 2026-10-16: full comparison and preview repair integration

The [sealed full H4 comparison](../benchmarks/results/h4-full-development-20261016.md)
has 780 valid layouts and passes native/full-G5 bounds. Native median change is
0%, while the worst job is +2.559175%; passing the median does not imply every
job improved. Chrome/Firefox medians are +0.150364%/+0.194317%, with totals
+0.615913%/+0.755448%. Every individual seed also passes G5's original bounds.
The run took 88.799 minutes; 699 attempts are new and 81 are exact-build reuse.

The [native surface follow-up](../benchmarks/results/native-diagnostics-surfaces-20261016.md)
found duplicated messages in actual project downloads after automated checks
had passed. Import now takes the complete nesting message list once. All 56
training records and CLI/MCP/Chromium/Firefox checks pass; all 45 accepted
libraries retain exact non-warning fields and eleven original errors are exact.
The fix and flat hole index are integrated for `0.2.0-alpha.1`. Full production
checks and current-build performance remain required; completion stays 45%.

### 2026-10-16: integrated preview Chrome result

The [completed Chrome arm](../benchmarks/results/h4-preview-chrome-failure-20261016.md)
validates all 201 layouts and passes full G5 (median +0.242546%, total +0.571472%,
with all three individual-seed bounds passing). The curve-heavy subset instead
misses H4: median +1.046217% against +1%, although every job stays within +5%.
Native passes its 65-job comparison with a 0% median change. The
[complete original matrix](../benchmarks/results/h4-preview-development-20261016.md)
is now sealed with all 603 new layouts valid. Firefox passes the subset at
+0.788924% and full G5 at +0.140371% median/+0.401506% total. All results and limits
remain unchanged, and the release stays pending. This observation does not
establish a cause for the gap.

The subsequent [isolated eight-pair bound probe](../benchmarks/results/h4-score-chunks-probe-20261016.md)
passes the unchanged subset with 99 valid layouts: Chrome +0.378238% and Firefox
+0.432882% median material, worst jobs +3.103068%/+2.969688%. Four fixed-work
pairs preserve all results except elapsed wall time; their +0.204357% median
wall difference establishes no speed gain. Historical same-job/seed charged-work
rate medians are -2.993932% native, +7.644946% Chrome and +0.480342% Firefox, but
different trajectories make those diagnostic rather than isolated throughput.
The full native/G5 comparison and final integration/scale checks remain required.

The existing collision-scoring profile motivates an isolated investigation of
checking the same nonnegative partial-score bound within long pole rows. It must
retain accumulation order, accepted score bits, ties, geometry, work accounting
and deadlines. Extra checks may cost time, so no speed or quality benefit is
assumed. It is separate from the unintegrated common-line exchange candidate.

### 2026-10-16: directed-exchange pilot and path observations

The [paired H5 pilot](../benchmarks/results/h5-exchange-pilot-v2-20261016.md)
retains all 72 valid outcomes. Mechanical candidate medians remain +4.175294%
to +5.869406% above ordinary mode, failing +1%; all 24 candidate runs have zero
exchange proposals. Two [existing-timer diagnostics](../benchmarks/results/h5-exchange-path-20261016.md)
also validate and show no exchange call, although both record separator work
and panel-hardware records ordinary relocation. Exchange is called only after
three failed separation returns; a call can consume the remaining exploration
budget. This is evidence about the two observed trajectories, not a proof of
unreachability. The earlier bounded relocation opportunity is a new hypothesis.
Keep the candidate isolated and preserve all original gates and attempts.


### 2026-10-16: early exchange call point, functional evidence only

[The isolated follow-up](../benchmarks/results/h5-early-exchange-preparation-20261016.md)
reaches and accepts an exchange in an authored full-window test before gap
filling can short-circuit relocation. Seven focused and 82 optimized core tests
pass. Identical public observers on current `7eba929` baseline/candidate preserve
ordinary-mode results except wall time; common-mode fixed-work replays and
independent metrics agree. Those small API cases have zero proposals, so only
the targeted window test establishes reachability. Both setup failures remain
preserved. The new matched mechanical/control pilot is prepared but unopened;
it waits for the active release quality/scale sequence. No material improvement
or general reachability claim follows from these authored checks.


### 2026-10-16: competitor shipment check before the preview

The [published Sparrow Studio description](https://sparrowstudio.app/) still
explicitly excludes automatic allocation across multiple fixed sheets and
placing parts inside holes. Its [repository README](https://github.com/JeroenGar/sparrow-studio/blob/2102a9a4ed8d78f4f5ad58bdef25a68fc7b96fe6/README.md)
now distinguishes the deployed `web/` app from a separate, unpublished redesign.
The new app's Sheets tab does not establish a shipped fixed-sheet solver.
[Exact commit/README hashes and the review](../benchmarks/results/competitor-stop-review-20261016/review.json)
record this distinction. The plan's shipment stop rule is not triggered. This
availability check changes no dependency, frozen competitor result or README
comparison claim; it is not a new benchmark.


### 2026-10-16 — Integrated score-bound full outcome

The [current 7eba929 matrix](../benchmarks/results/h4-preview-score-release-20261016.md)
completes with 603 new and 195 reused valid layouts. Native median is +0.000681%
versus frozen v1, and both full G5 comparisons pass all aggregate/per-seed limits.
Chrome's curve subset still fails (+1.032679% median versus +1%); Firefox passes
(+0.881781%). Original raw outcomes and prior failures remain sealed. Scale is
not started and the preview stays unreleased. Current profiles on gear-1, sign-1
and example-gears are planned separately to identify remaining costs after the
score changes; they cannot substitute for a quality gate.


### 2026-10-16 — Current collision-tree diagnosis

[Current profiles](../benchmarks/results/h4-browser-profile-20261016T040030Z.md)
validate gear-1, sign-1 and example-gears. Edge/quadtree traversal accounts for
roughly 47–76% of sampled time; bounding-box generation adds 5–9%. Sample gaps
are below 0.000155 s. This supports testing one shallower separator-window tree
configuration in isolation, retaining all original geometry. Fewer tree visits
may instead increase leaf work, so no optimization is justified without measured
quality, original-job validation and full regression evidence. No dependency or
product code changes in this diagnostic; no H4 credit or new public claim.


### 2026-10-16: complete browser-performance requirement review

[H4 is complete](../benchmarks/results/h4-depth-complete-20261016.md) on the
integrated depth-three collision-tree build. All full native and browser
quality limits pass, as do both 2,000-part scale workflows in both browsers
and exact saved-curve checks for every curved-workload placement. Peak
observed RSS is 1.352409 GB; maximum heartbeat gap is 199 ms. These are
development/scale observations, not a new competitor result or universal
resource guarantee. The Windows servicing interruption is retained with all
402 completed pre-restart outcomes; only missing Firefox outcomes were
recovered. Earlier failed candidates remain preserved. H2/H5 stay open.


### 2026-10-16: atomic obstruction-set pilot outcome

[All 72 outcomes validate](../benchmarks/results/h5-obstruction-set-recovered-pilot-20261016.md),
but five of eight material pairs fail +1%. The complete-group candidate accepts
ten of 147 exchange attempts; neither panel-hardware kerf accepts an exchange.
All mechanical medians remain +4.66% to +5.96% above ordinary mode. The original
full H5 comparison remains authoritative, and this pilot is rejected for
production integration. New work needs a distinct, evidenced placement
hypothesis; these observations do not prove global infeasibility.


**Preview published, 2026-10-16:** [v0.2.0-alpha.1](https://github.com/skulitom/Nestbolt/releases/tag/v0.2.0-alpha.1)
is published at `c36baa8` under Artem's release authorization. All five release
jobs pass; [actual downloads and all four build attestations](../benchmarks/results/preview-depth-published-20261016.md)
verify, including exact tag/source binding and unchanged stable Latest/assets.
[Published Windows CLI/MCPB feature checks](../benchmarks/results/preview-depth-published-features-20261016.md)
pass with authored inputs only. The original Python-launch and shared-cache
verification errors remain preserved alongside their limited recoveries.
The README links the preview and separates hosted v0.1.0 from newer local
browser features. No new registry version, reserved evaluation or public
competitor claim. H2/H5 remain open; completed milestone weight stays 60%.


**N4 diagnosis, 2026-10-17:** [four current-candidate traces](../benchmarks/results/h5-obstruction-stage-diagnosis-20261017.md)
validate all layouts but show zero complete blocker-set proposals: 620 sampled
sets fail the smaller-area heuristic. All 29 attempted exchanges are partial;
27 fail receiving-sheet repair and two succeed. An [independently validated
authored witness](../benchmarks/results/h5-area-witness-20261017.md) demonstrates
that returning more combined part area can preserve both validity and material.
The first incorrectly oriented witness is retained with its failed material
assertion. This motivates a separately tested complete-set eligibility change;
it proves no mechanical feasibility or quality gain. Production stays unchanged,
and H2/H5 remain open at 60% completed weight.


**N4 complete-set preparation, 2026-10-17:** [the isolated eligibility change](../benchmarks/results/h5-complete-set-preparation-20261017.md)
passes 85 core tests, strict lint and authored public comparisons. Complete
two/three-blocker sets may now be considered regardless of combined part area;
both-sheet repair and final independent geometry/material limits remain.
Equal/larger-area tests pass without extra material; impossible returns retain
the incumbent. The [committed 72-outcome pilot](../benchmarks/results/h5-complete-set-pilot-20261017/plan.json)
uses the unchanged paired method and original thresholds. It has not started
at this checkpoint. Production remains unchanged; H2/H5 are open at 60%.


**N4 complete-set outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-complete-set-pilot-20261017.md),
including an independent filled-outer audit of 133,412 same-sheet pairs in all
48 common-mode layouts. All four mechanical material pairs still fail +1%, at
+5.433792% / +6.521291% for large plates and +5.700699% / +5.764347% for panel
hardware (laser/plasma). Four control pairs meet material limits. Of 74 exchange
attempts, eleven succeed; none on panel hardware. The candidate is rejected for
integration and the full gate is not opened. Counters alone do not establish
which repair stage now limits progress. Original outcomes/limits remain;
H2/H5 are open at 60%.


**N4 return-stage diagnosis, 2026-10-17:** [all four traced outputs validate](../benchmarks/results/h5-complete-stage-diagnosis-20261017.md).
All 23 actual attempts move complete blocker sets, pass receiving-sheet repair
and fail return-sheet repair within the existing budget. There are 427 eligible
equal/larger-area samples and no smaller complete sets. No partial attempt or
acceptance occurs. Source/binary/input/trace integrity is verified. Next inspect
how returned groups are placed and repaired; these observations do not prove
feasibility or impossibility, or replace the failed quality pilot. Production
and gate limits remain unchanged; H2/H5 are open at 60%.


**N4 return-frame preparation, 2026-10-17:** [the isolated initialization change](../benchmarks/results/h5-return-frame-preparation-20261017.md)
passes 90 core tests, strict lint and authored public checks. A returned group
may rotate/reflect into the vacated incoming frame when every part permits it;
otherwise it retains the previous translation. Both repairs and exact material
limits remain. The original type error, arithmetic-test error and guarded
0.0007 mm² material increase are preserved and reviewed. Separate tests require
strict rejection and a successful exchange with a fixed envelope. The
[72-outcome comparison](../benchmarks/results/h5-return-frame-pilot-20261017/plan.json)
retains original inputs, budgets and limits. No integration or quality claim.
H2/H5 remain open at 60%.


**N4 return-frame outcome, 2026-10-17:** [all 72 outcomes validate](../benchmarks/results/h5-return-frame-pilot-20261017.md),
with an independent hole-reservation audit of 133,535 same-sheet
pairs across all 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.208689%; m-mechanical-large-plates at 1.5 mm: +4.649005%; m-mechanical-panel-hardware at 0.2 mm: +5.475484%; m-mechanical-panel-hardware at 1.5 mm: +5.886483%
There are 11 accepted exchanges from 71 attempts.
Reject this candidate for integration; do not open the full 13-job gate for it. Production remains unchanged. Counters alone do not establish the
remaining repair bottleneck or impossibility. H2/H5 remain open at 60%.


**N4 return-frame diagnosis, 2026-10-17:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-frame-stage-diagnosis-20261017.md)
record 23 complete-set attempts. Every reciprocal frame is permitted and every
receiving-sheet repair succeeds, but all return-sheet repairs fail. None reaches
the final geometry/material guard. Orientation fallback is not the immediate
cause in these observations. Next inspect source capacity and placement of the
larger returned groups; area ratios alone do not prove impossibility. A balanced
multi-part exchange needs a separate authored feasibility example first.
Original results/limits remain; no production change or H5 closure. Completion 60%.


**N4 balanced-group witness, 2026-10-17:** [two independently valid layouts](../benchmarks/results/h5-balanced-exchange-witness-20261017.md)
show two incoming rectangles exchanging with three return squares at identical
material and quantities. A necessary stacking bound excludes all single-incoming
choices within that explicitly scoped selection. This supports investigating
balanced groups, but proves no mechanical improvement; inspect actual source
capacity/placement before implementing a new heuristic. No optimizer run,
production change or gate relaxation. H2/H5 remain open at 60%.


**N4 capacity diagnosis, 2026-10-18:** [four valid diagnostic outcomes](../benchmarks/results/h5-return-capacity-diagnosis-20261017.md)
record 25 complete reciprocal attempts. Independent geometry checks confirm
clear repaired receivers and overlapping repaired return sheets. Source area
occupancy is 75.281–85.554% of the actual shortened search boundary: area alone
does not prove infeasibility, and occupancy alone does not prove a packing exists.
Next seek a complete, independently valid repack of fixed saved assignments with
their original boundary and legal orientations before changing repair. Preserve
all failed outcomes; no production change, relaxed limit or H5 credit. 60% complete.


**N4 assignment feasibility, 2026-10-18:** [three independently valid source packings](../benchmarks/results/h5-assignment-repack-20261018.md)
fit the unchanged saved boundaries and quantities: both large-plate cases and
the 0.2 mm panel case. The 1.5 mm panel case remains unresolved after six retained
rounds. This proves only source-assignment feasibility, not whole-job material
improvement. Earlier traces repeat eight distinct assignments over 25 attempts
(17 repeats after first occurrence). Next test retained compatible repair progress
within the existing shared budget, preserving geometry/orientation identities,
tracker-key consistency, rollback and independent acceptance. No production change
or relaxed gate; H2/H5 remain open at 60%.


**N4 source-repair reuse outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-return-reuse-pilot-20261018.md).
The independent filled-outer audit checks 133,470 same-sheet
pairs across all 48 common-mode layouts, retaining hole reservation and kerf.
There are 6 failed material pairs out of eight under the original +1%
limit. m-mechanical-large-plates at 0.2 mm: +5.607522%; m-mechanical-large-plates at 1.5 mm: +5.124968%; m-mechanical-panel-hardware at 0.2 mm: +6.668421%; m-mechanical-panel-hardware at 1.5 mm: +5.745273%; c-bracket-mixed at 0.2 mm: +2.419752%; c-bracket-mixed at 1.5 mm: +1.016169%
The candidate records 11 accepted exchanges from 73 attempts and
37 compatible source-repair reuses. Reuse counts do not establish repair
completion or explain remaining failures. Reject this candidate for integration; do not open the full 13-job gate for it. Production, prior failures
and frozen inputs remain unchanged. H2/H5 remain open at 60%.


**N4 reuse-stage diagnosis, 2026-10-18:** [four diagnostic outputs validate](../benchmarks/results/h5-return-reuse-stage-diagnosis-20261018.md).
All 24 complete-obstruction exchanges repair the receiver, then fail source
repair. Sixteen resume a compatible saved state; seven reduce loss further,
none reaches zero, and none reaches final material/geometry acceptance.
The reader verifies original inventories and exact restored loss across each
reuse. The issue is incomplete repair, not observed cache-state corruption.
Each case spends 0.903–1.054 seconds in source repairs within the existing
early-call budget. Available windows shrink after successive attempts; three
late attempts reach source repair with an already-expired pair deadline and
return their unchanged state. These observed durations are not minimum required
repair times and do not prove that a larger allowance would solve H5.
Production and all failed results remain unchanged. H2/H5 remain open at 60%.


**N4 balanced-pair preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-balanced-group-preparation-20261018.md)
passes 97 optimized core tests, strict lint, ten authored observer outcomes,
four public CLI comparisons and five unchanged paired-harness checks. All 90
prior tests remain; seven new tests cover the two-to-three exchange, permissions,
frozen sheets, bounded pair selection, valid single fallback and rejected
attempts. The original test-assumption failures and independently valid fallback
output remain preserved. Normal output stays exact and common replay passes.

Two nearby copies can move together against their complete obstruction union,
using at most half the existing exchange window before the single-part path.
The original total budget, independent geometry/material acceptance and saved
incumbent guards stay. [The committed 72-outcome plan](../benchmarks/results/h5-balanced-group-pilot-20261018/plan.json)
retains the same cases, kerfs, seeds, matched cores, 60-second limits and +1%
condition. No measured improvement, production change or H5 credit is claimed;
the full 13-job gate remains required. H2/H5 are open at 60%.


**N4 balanced-pair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-balanced-group-pilot-20261018.md).
The independent filled-outer audit checks 133,456 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.188368%; m-mechanical-large-plates at 1.5 mm: +5.469920%; m-mechanical-panel-hardware at 0.2 mm: +6.652162%; m-mechanical-panel-hardware at 1.5 mm: +5.589744%; c-bracket-mixed at 0.2 mm: +1.501017%
The candidate accepts 19/41 total exchanges, including 13/25
two-part exchanges. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 pair-identity diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-balanced-stage-20261018.md).
There are 11 attempts and 3 accepted exchanges, including
2 pairs. 2 accepted exchanges return the
same original part types and quantities as they take; per-sheet inventory is
unchanged in those cases, although poses may change. Immediate material falls
in 0 accepted exchanges and last-sheet occupied
extent falls in 0. These traces do not reconstruct
the earlier pilot or prove a later benefit/harm from rearrangement. Retained
proposal identities, losses, material and extent are preserved. The independent
filled-outer audit checks 18,569 pairs. No gate relaxation,
production change, reserved-file access or H5 credit. H2/H5 remain open at 60%.
Source inspection also confirms that accepting an exchange short-circuits
the following gap-fill and relocation calls in that window. The next isolated
change should test whether gap filling after an accepted exchange can use its
new arrangement, while preserving the total search limit and normal-mode
behavior. This identifies a missed execution path, not a measured quality gain.


**N4 post-exchange gap-fill preparation, 2026-10-18:** [the isolated correction](../benchmarks/results/h5-post-exchange-fill-preparation-20261018.md)
passes 98 optimized core tests, strict lint/build, ten authored observer outcomes,
four public CLI comparisons and five paired-harness checks. A new known-gap
regression fails on the unchanged runtime, then passes when direct gap filling
continues after an accepted exchange. Normal output stays exact and common
fixed-work replay passes. Original exchange, repair, geometry/material rules,
search limits and all 97 earlier tests remain. Counters track the follow-up
calls and moved parts. The committed 72-outcome pilot preserves its original
paired method and +1% limit. No measured improvement, production change or
H5 credit yet. H2/H5 remain open at 60%.


**N4 post-exchange gap-fill outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-post-exchange-fill-pilot-20261018.md).
The independent filled-outer audit checks 133,374 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.484564%; m-mechanical-large-plates at 1.5 mm: +5.388338%; m-mechanical-panel-hardware at 0.2 mm: +6.386542%; m-mechanical-panel-hardware at 1.5 mm: +5.563315%
The candidate accepts 19/42 total exchanges, including 12/24
two-part exchanges. The post-exchange gap-fill step runs 19 times and moves 14 parts; these counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 productive-exchange preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-productive-exchange-preparation-20261018.md)
passes 101 optimized core tests, preserving all 98 previous tests, strict
lint/build, ten authored public outcomes, four CLI comparisons and five
paired-harness checks. It distributes bounded pairs across original part
types and rejects same-inventory swaps without material reduction. Two
new regressions fail on the unchanged runtime, while a positive witness
saving over 99.9 mm2 passes. The original rounding-only positive fixture
is preserved. Sixteen independent validations cover eight actual authored
outcomes. Normal output and common fixed-work replay pass; geometry,
budgets and the +1% material limit remain. The committed 72-outcome pilot
retains the previous paired method. No production change or H5 credit;
H2/H5 remain open at 60%.


**N4 productive-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-productive-exchange-pilot-20261018.md).
The independent filled-outer audit checks 133,603 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.483065%; m-mechanical-large-plates at 1.5 mm: +5.402498%; m-mechanical-panel-hardware at 0.2 mm: +7.022646%; m-mechanical-panel-hardware at 1.5 mm: +5.298801%
The candidate accepts 12/121 total exchanges, including 1/62
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 11 parts. The new guard rejects 45 same-inventory proposals without material improvement; these counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 productive-exchange diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-productive-stage-20261018.md).
Of 28 attempts, 18 fail source repair, seven reject unchanged
inventory, one expires after repair, one fails the material guard and one
is accepted without immediate material/extent reduction. All eight paired
attempts preserve inventory; all twenty single attempts return more recorded
item area than they remove. The large-plate source's largest item has only
one copy, excluding it from the same-item pair selector. Requested source
windows range from -0.003617 to 0.398944 seconds, with 4 already
nonpositive. Timings do not prove minimum repair time or impossibility.
The independent outer audit checks 18,669 pairs. The
next hypothesis is bounded mixed-item pairs with authored correctness checks;
budgets and every geometry/material limit remain. No integration or H5 credit;
H2/H5 remain open at 60%.


**N4 mixed-assignment witness, 2026-10-18:** [two distinct incoming rectangles](../benchmarks/results/h5-mixed-exchange-witness-20261018.md)
(30x40 and 30x50 mm) can exchange with three 30x30 mm squares. Both authored
layouts preserve all seven parts and exactly 19,700 mm2 material; frozen CLI
and independent filled-outer checks pass. Eight conservative height bounds
rule out either chosen incoming part moving alone while one filler remains
on each sheet, even if it moves. The two incoming parts have different IDs
and dimensions, so the current same-original-item selector cannot pair them.
This is a scoped geometric witness, with zero optimizer runs. It neither
proves global impossibility nor mechanical quality. The next candidate still
requires an original-runtime regression, allowed-pose/rollback tests and the
unchanged H5 quality gates. Production stays unchanged; H2/H5 remain open at 60%.


**N4 mixed-exchange preparation, 2026-10-18:** [the isolated candidate](../benchmarks/results/h5-mixed-exchange-preparation-20261018.md)
passes 107 optimized core tests, retaining all 101 previous tests, strict
lint/build, ten public outcomes, four CLI comparisons and five pilot checks.
Six new tests and twelve actual before/after validations cover mixed parts,
per-member poses, frozen sheets, bounded choices and rollback. The original
runtime failure and first candidate's missed seed-two group placement remain
preserved; mixed-group corner anchors correct that failure without weakening
tests. Up to six mixed pairs interleave existing same-item pairs within the
original phase/budget. All geometry/material rules and paired methods remain.
No measured quality claim or integration; H2/H5 stay open at 60%.

**Competitor shipment check, 2026-10-18:** [the published descriptions](../benchmarks/results/competitor-stop-review-20261018.md)
continue to exclude automatic allocation across fixed sheets and placing parts
inside holes. The repository identifies its new app as unpublished. These sources
do not trigger the shipment stop rule. This is an availability check, not a new
capability test or benchmark; the exact repository commit and response hashes
are recorded. Production, dependencies and frozen comparisons remain unchanged.


**N4 mixed-exchange outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-mixed-exchange-pilot-20261018.md).
The independent filled-outer audit checks 133,299 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +6.069459%; m-mechanical-large-plates at 1.5 mm: +6.160993%; m-mechanical-panel-hardware at 0.2 mm: +6.770269%; m-mechanical-panel-hardware at 1.5 mm: +5.607046%
The candidate accepts 12/132 total exchanges, including 1/69
two-part exchanges. The post-exchange gap-fill step runs 12 times and moves 19 parts. The new guard rejects 49 same-inventory proposals without material improvement; mixed pairs account for 0/11 accepted/attempted exchanges. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 mixed-pair diagnosis preparation, 2026-10-18:** [the separate observer](../benchmarks/results/h5-mixed-stage-preparation-20261018.md)
passes 107 optimized tests, strict lint/build, nine actual authored traces and
22 malformed-observation checks. Each paired generation call records an exact
sample-rejection partition, retained proposals and deadline truncation;
existing traces retain choices, repair loss/time and final rejection stage.
All seven exchange counters reconcile. Insertions reverse exactly, with the
other 151 files unchanged. Four serial seed-zero mechanical observations are
planned under original 60-second limits. Logging can perturb trajectories;
this diagnoses the failed pilot without replacing it. No integration or H5
credit; production and reserved inputs remain unchanged at 60% completion.


**N4 mixed-pair diagnosis, 2026-10-18:** [all four outputs validate](../benchmarks/results/h5-mixed-stage-20261018.md).
The two large-plate traces examine all 24 pair calls and 4,764 samples without
sample truncation, but retain no paired proposal. The area filter rejects
1,721 otherwise eligible samples, including 575 mixed samples. Panel traces
generate only the first same-item pair per kerf; all seven attempted paired
swaps reject unchanged inventory, and no mixed pair is generated. Their
repairs already have zero loss and each takes less than 0.0001 seconds;
remaining construction/validation time is not separately measured.
Overall, 28 attempts yield 19 failed source repairs, seven neutral rejections,
one material rejection and one accepted single swap saving 18.669 mm2
immediately. The filled-outer audit checks 18,626 pairs.
The next hypothesis targets the proposal-area filter with an authored runtime
regression; it is not a quality claim. H2/H5 remain open at 60%.

**N4 larger-return witness, 2026-10-18:** [a valid mixed pair exchange](../benchmarks/results/h5-larger-return-witness-20261018.md)
returns 2,790 mm2 of parts after removing 2,700 mm2, while keeping all seven
parts and every material metric unchanged at 19,700 mm2. Frozen CLI and
independent filled-outer checks validate both authored layouts. Eight
conservative height bounds exclude either selected incoming part moving
alone while one filler stays on each sheet. The current pair-area filter
excludes this complete return set. This proves a limitation of that filter,
with zero optimizer runs; an actual runtime regression and full candidate
checks remain necessary. It does not establish mechanical quality or H5.


**N4 larger-return candidate review, 2026-10-18:** [the first implementation is unqualified](../benchmarks/results/h5-larger-return-review-20261018.md).
The new larger-return regression first fails against unchanged runtime, then
passes after removing the paired proposal area filter. All four new tests
pass, but the complete suite reports 107 passes and four older failures.
Every original assertion, failed source and binary is preserved. Six new
actual outcomes and ten original/broader comparison observations pass 32
independent CLI validations. The broader results are equal in one case and
save 66.0529 / 266.0522 mm2 in two; the gap-filling case is 0.0388 mm2 worse
and leaves its named small part on the last sheet despite one recorded fill.
A logging-setup failure and shared-target stale executable are preserved;
recovery uses a fresh target and reuses all completed original observations.
Next inspect the intermediate fill and accepted snapshots before correcting
behavior or targeted tests. No assertion change, quality pilot, integration
or H5 credit; H2/H5 remain open at 60%.


**N4 larger-return qualification, 2026-10-18:** [the corrected isolated candidate](../benchmarks/results/h5-larger-return-preparation-20261018.md)
passes 113 optimized core tests, strict lint/build, ten public outcomes,
four CLI comparisons and five pilot checks. The original candidate's four
failures remain. An exact replay with eight validated intermediate layouts
shows gap filling moves the named part correctly; later compression moves it
again while reducing material. Four route-specific tests now target their
invariants, 103 prior tests are unchanged and six tests are added. The actual
strict material guard rejects even a one-ULP increase. A direct post-exchange
fill test and all six larger-return outcomes pass fourteen more independent
validations. Guard extraction reverses exactly; all other runtime text is
unchanged beyond the area filter and unused sum removal. The same 72-outcome
pilot is committed before measurement. No quality or integration claim;
H2/H5 remain open at 60%.


**N4 larger-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-larger-return-pilot-20261018.md).
The independent filled-outer audit checks 133,465 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.739579%; m-mechanical-large-plates at 1.5 mm: +6.431410%; m-mechanical-panel-hardware at 0.2 mm: +6.701091%; m-mechanical-panel-hardware at 1.5 mm: +4.836540%; c-bracket-mixed at 1.5 mm: +1.989411%
The candidate accepts 13/119 total exchanges, including 10/81
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 15 parts. The unchanged neutral guard rejects 33 same-inventory proposals without material improvement; mixed pairs account for 1/4 accepted/attempted exchanges. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.


**N4 larger-return diagnosis preparation, 2026-10-18:** [the isolated observer](../benchmarks/results/h5-larger-stage-preparation-20261018.md)
passes all 113 unchanged core tests, strict lint/build, fourteen authored trace
cases, the direct strict-material guard and 31 malformed-observation checks.
All 154 formatted files match an exact reconstruction, with only two observed
files. Timings distinguish construction, repairs and validation; complete
after-exchange/after-fill layouts will be checked independently. The first
logger compile failure remains preserved. Four serial seed-zero mechanical
observations retain the original 60-second budgets. Logging may perturb wall
time; this diagnoses the rejected candidate without replacing its failed
quality comparison. No integration or H5 credit; completion stays 60%.


**N4 larger-return diagnosis, 2026-10-18:** [all four final and four intermediate layouts validate](../benchmarks/results/h5-larger-stage-20261018.md).
The filled-outer audits check 23,542 same-sheet pairs. Of 23 attempts, two
accept, fourteen fail source repair and seven are neutral inventory rejections.
Panel paired repairs start with zero loss; repeated validation costs 0.367 /
0.299 seconds, and no mixed pair is generated. Large-plate exchanges save only
86.418 / 40.2735 mm2 immediately; filling changes neither total and leaves
0.965 / 0.552 seconds of the original exchange opportunity. Next verify whether
neutral trials preserve exact original-item poses before considering an early
rejection. Equal inventory/material alone cannot justify skipping validation.
These instrumented observations do not replace the five failed pilot pairs;
no integration or H5 credit, and completion remains 60%.


**N4 exact-state diagnosis preparation, 2026-10-18:** [the observer passes all 116 optimized tests](../benchmarks/results/h5-exact-state-preparation-20261018.md),
strict lint/build, fourteen authored trace cases and 37 malformed-record checks.
All 113 prior tests remain unchanged. Exact reconstruction covers all 154 files;
153 are unchanged from the preceding observer. Two panel-hardware diagnostics
will compare complete internal pose multisets and independently check both
layouts saved for neutral rejections. The comparison records observations only;
all decisions, full validators, material guards and time limits remain.
No production integration, reserved access or quality claim; H2/H5 remain open
and completed weight stays 60%.


**N4 exact-state diagnosis, 2026-10-18:** [both final and all 12 saved layouts validate](../benchmarks/results/h5-exact-state-20261018.md).
1 of 6 neutral trials exactly preserve the complete internal physical state.
Independent filled-outer checks cover 111,838 same-sheet pairs.
Public pose multisets match in 1/6 pairs; exact internal comparison also
requires shared model/container identity and full float bits. All original
validators and decisions remain. This diagnostic establishes no quality gain;
the five failed pilot comparisons remain authoritative. H2/H5 stay open at 60%.

An exact-state early rejection now has an observed target, but its impact on
search quality is unproven. A separate candidate may reject only a complete
exact-state match before repeated validation, preserving shared container and
original-item identity, full transform bits, reflection and multiplicity.
Every changed state and every accepted exchange must retain the original
full geometry/material checks. Qualify the predicate and early branch with
authored regressions, preserve expired/disabled behavior and rollback, and
repeat the existing paired development protocol only for that changed build.
Do not infer a quality gain or promote it from these diagnostic timings.


**N4 exact-state candidate preparation, 2026-10-18:** [all 117 optimized tests pass](../benchmarks/results/h5-exact-reject-preparation-20261018.md),
with all 113 prior tests unchanged. The new branch regression first fails
against the original runtime; its source, executable and log are preserved.
The candidate rejects only a complete exact internal-state match before
repeated validation. Changed states and all accepted exchanges retain the
original full validators, strict material guards and budgets. Twelve branch
outcomes pass 24 frozen-CLI checks; strict lint/build, ten public outcomes,
four CLI comparisons and five adversarial pilot checks also pass. The paired
72-outcome method is unchanged and committed before measurement. No quality
result, production integration or release claim; H2/H5 remain open at 60%.
All six hosted checks on main `924336a` have passed.


**N4 exact-state early-rejection outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-exact-reject-pilot-20261018.md).
The independent filled-outer audit checks 133,535 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.349182%; m-mechanical-large-plates at 1.5 mm: +5.485080%; m-mechanical-panel-hardware at 0.2 mm: +6.767422%; m-mechanical-panel-hardware at 1.5 mm: +5.195747%; c-bracket-mixed at 0.2 mm: +1.027791%; c-bracket-mixed at 1.5 mm: +1.177346%
The candidate accepts 13/125 total exchanges, including 11/87
two-part exchanges. The post-exchange gap-fill step runs 13 times and moves 12 parts. The early exact-state and original neutral guards reject 41 same-inventory proposals without material improvement; mixed pairs account for 2/5 accepted/attempted exchanges. The neutral total includes 3 exact-state rejections before repeated validation. These counts alone do not establish final quality. These counts do not establish improved final material or
identify remaining failure stages. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and
all earlier failed results remain unchanged. H2/H5 remain open at 60%.

The [saved-height follow-up](../benchmarks/results/h5-exact-reject-pilot-20261018/source-review.json) reconstructs all twelve prior neutral-layout material values exactly; every sheet maximum is unchanged. It suggests qualifying an exact material-profile rejection only if this pilot still fails. No new filter or quality claim.


**N4 material-profile candidate preparation, 2026-10-18:** [all 123 optimized tests pass](../benchmarks/results/h5-material-profile-preparation-20261018.md),
with all 117 prior tests unchanged. The candidate rejects same-inventory
trials whose exact original-geometry profiles prove unchanged charged
material. It uses the existing validator footprints and preserves every
accepted geometry/material check. Budgets and coefficients are unchanged;
profile work uses the existing vertex charge. Five proofs, 23 witness pairs
and 47 frozen-CLI checks cover geometry contexts, real gains and an invalid
overlap; 12 branch outcomes pass another 24 CLI checks. The original failing
branch regression is preserved. Strict lint/build, public parity/replay,
five harness tests and exact formatted-source reconstruction pass. The
unchanged 72-outcome method is committed before measurement. No quality,
integration or release claim; H2/H5 remain open at 60%.


**N4 material-profile rejection outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-material-profile-pilot-20261018.md).
The independent filled-outer audit checks 133,235 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.169797%; m-mechanical-large-plates at 1.5 mm: +6.158488%; m-mechanical-panel-hardware at 0.2 mm: +6.407212%; m-mechanical-panel-hardware at 1.5 mm: +5.654893%; c-bracket-mixed at 0.2 mm: +1.823168%
The candidate accepts 13/147 exchanges, including 11/108 paired and 1/18 mixed-item exchanges. Follow-up gap filling runs 13 times and moves 16 parts. Of 49 neutral rejections, 3 are caught by exact internal-state equality and 46 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.

The [read-only frontier inspection](../benchmarks/results/h5-material-profile-pilot-20261018/source-review.json) finds unchanged top-defining insert poses in all six older neutral panel pairs. It uses no new search or held-out geometry and makes no claim about every current failure.


**N4 height-setting part observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-frontier-observer-preparation-20261018.md).
All 123 existing optimized tests pass. The observer records original part
families for available, visited and attempted exchange choices alongside the
validated public baseline. It changes no decision, work charge or budget.
Sixteen authored cases, sixteen malformed-record rejections and
35 frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.


**N4 height-setting part diagnosis, 2026-10-18:** [both final and baseline layouts validate](../benchmarks/results/h5-frontier-observer-20261018.md).
None of 25 attempts selects the insert family defining the credited sheet
height. Both traces visit only choices 0, 1 and 12; the insert pair at index
6 and insert singles from 73 are never visited. Twelve trials are rejected
early and thirteen stop at source repair or expiry. The independent audit
checks 31,740 filled-outer pairs and reconstructs both material values
exactly. This supports qualifying a boundary-first member ranking under the
existing choice limits, budgets and full acceptance guards. It proves no
quality gain; H2/H5 remain open at 60%.

The actual search reaches only choice indices 0, 1 and 12 in both
diagnostics: a frame pair, its mixed frame/cog alternative, and the first
frame single. The insert pair is present at index 6; insert singles start at
73. Neither is visited. Both height-setting copies are inserts on the same
last sheet that receives the material offcut credit. Removing repeated
neutral validation increased attempts but did not reach that family.

The next isolated candidate should rank incoming members by proximity to the
last sheet's upper edge before forming the existing bounded pair and single
choices. In the solver's rotated strip frame this is the placed shape's
rightmost extent. Keep area as a tie-breaker and retain stable equal ties,
the six same-item and six mixed-pair limits, sampling, repair caps, all work
budgets and full geometry/material acceptance checks. Prove that a smaller
part at the boundary outranks a larger interior part, that ties are stable,
and that disabled/expired behavior and useful existing exchanges remain.
Only after those checks should the unchanged paired quality pilot run.
This is a ranking hypothesis, not evidence of feasible improvement or a
reason to relax any H5 requirement.


**N4 boundary-priority preparation, 2026-10-18:** [all 126 optimized tests pass](../benchmarks/results/h5-boundary-priority-preparation-20261018.md),
with 123 prior tests unchanged. The isolated candidate orders incoming parts
by upper extent before area, retaining stable ties and the existing bounded
pair generators. Selected pairs keep their original member anchor order. Budgets, sampling, repairs, work charges and every full
acceptance check are unchanged. Two original ordering regressions fail as
expected and are preserved; all three new tests pass afterwards. The first
revision also exposes three existing exchange regressions; preserving pair
anchors resolves them with unchanged assertions and retained failures. The order
fixture and twelve rejection-boundary outcomes pass 25 frozen-CLI checks.
Strict lint/build, public parity/replay, five pilot tests and exact source
reconstruction pass. The unchanged 72-outcome plan is committed before
measurement. No quality or integration claim; H2/H5 remain open at 60%.


**N4 boundary-priority outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-boundary-priority-pilot-20261018.md).
The independent filled-outer audit checks 133,236 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.771660%; m-mechanical-large-plates at 1.5 mm: +4.211101%; m-mechanical-panel-hardware at 0.2 mm: +5.991880%; m-mechanical-panel-hardware at 1.5 mm: +5.770657%; c-bracket-mixed at 0.2 mm: +1.591789%; c-bracket-mixed at 1.5 mm: +1.089470%
The candidate accepts 17/100 exchanges, including 12/73 paired and 0/0 mixed-item exchanges. Follow-up gap filling runs 17 times and moves 20 parts. Of 1 neutral rejections, 0 are caught by exact internal-state equality and 1 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 exact boundary-copy observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-boundary-observer-preparation-20261018.md).
All 126 existing optimized tests pass. The observer records original part
families and exact physical poses for available, visited and attempted
exchange choices alongside the validated public baseline. Each chosen pose
matches a unique baseline copy exactly, with complete single-copy coverage. It changes no decision, work charge or budget.
Sixteen authored cases, 21 malformed-record rejections and
35 frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.


**N4 exact boundary-copy diagnosis, 2026-10-18:** [both diagnostic outcomes and every saved baseline validate](../benchmarks/results/h5-boundary-observer-20261018.md).
19 of 19 attempts select at least one actual part defining the credited sheet height; 0 select every part defining that height. 1 of the first group and 0 of the second group are accepted. The independent audit checks 31,794 filled-outer
pairs and reconstructs every material value exactly. Every selected physical
pose matches its baseline exactly. This identifies copy coverage, without
establishing final quality or packing feasibility. The six failed pilot
comparisons remain authoritative. H2/H5 remain open at 60%.


**N4 boundary-pair preparation, 2026-10-18:** [all 130 optimized tests pass](../benchmarks/results/h5-boundary-pair-preparation-20261018.md),
including all 126 prior tests unchanged. The isolated candidate includes the
two highest source members first in the appropriate same-item or mixed pair
list, removes duplicate pairs and retains the six-plus-six caps and remaining
nearby alternatives. Original pair anchors, repairs, budgets, work charges and
all full acceptance checks remain. Three expected failures are preserved.
Independent original-contour checks confirm both highest physical copies in
same-item and mixed-item witnesses. Those and twelve rejection-boundary cases
pass 26 frozen-CLI checks. Strict lint/build, public parity/replay, source
reconstruction and five pilot harness checks pass. The unchanged 72-outcome
plan is committed before measurement. No quality claim; H2/H5 remain open at 60%.


**N4 boundary-pair preflight recovery, 2026-10-18:** the first launch stops
before any measurement because the old balanced-diagnostic PID now belongs to
`svchost.exe`, whose command line is protected. Its creation time is later than
the original diagnostic's recorded start, proving PID reuse. The old runner
and committed plan are preserved in [the recovery record](../benchmarks/results/h5-boundary-pair-pilot-20261018/preflight-recovery/checks.json).
The guard now checks process creation time before attempting the command
line. Six checks cover missing/reused processes, active original-runner
rejection, the existing different-command behavior and both inaccessible
identity cases. Unresolved identity still fails closed. The two old H4 PIDs
are absent. Block, scoring, case and measurement functions are AST-identical;
no candidate, budget, input or scoring change and zero searches before repair.
The amended plan is committed before its first measurement. H2/H5 remain open
at 60%.


**N4 boundary-pair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-boundary-pair-pilot-20261018.md).
The independent filled-outer audit checks 133,454 same-sheet
pairs across 48 common-mode layouts. 6 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +4.750258%; m-mechanical-large-plates at 1.5 mm: +5.823218%; m-mechanical-panel-hardware at 0.2 mm: +6.614117%; m-mechanical-panel-hardware at 1.5 mm: +5.725452%; c-bracket-mixed at 0.2 mm: +1.439312%; c-bracket-mixed at 1.5 mm: +1.316785%
The candidate accepts 14/120 exchanges, including 11/77 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 15 parts. Of 3 neutral rejections, 0 are caught by exact internal-state equality and 3 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 boundary-pair observation, 2026-10-18:** [the isolated diagnostic qualifies](../benchmarks/results/h5-boundary-pair-observer-preparation-20261018.md).
All 130 existing optimized tests pass. The observer records original part
families and exact physical poses for available, visited and attempted
exchange choices alongside the validated public baseline. Each chosen pose
matches a unique baseline copy exactly, with complete single-copy coverage. It changes no decision, work charge or budget.
Sixteen authored cases, 21 malformed-record rejections and
35 frozen-CLI baseline checks pass. Twelve parent branch witnesses
and their counters match exactly; every formatted source file reconstructs.
Two serial panel diagnostics retain both kerfs, seed zero, 60 seconds and
physical CCD0 CPU 8. Logging can affect wall trajectories, so this is not a
quality comparison. No new selector, integration or H5 credit; H2/H5 stay open
at 60%. The plan is committed before measurement.


**N4 boundary-pair diagnosis, 2026-10-18:** [both diagnostic outcomes and every saved baseline validate](../benchmarks/results/h5-boundary-pair-observer-20261018.md).
22 of 22 attempts select at least one actual part defining the credited sheet height; 11 select every part defining that height. 0 of the first group and 0 of the second group are accepted. The independent audit checks 31,766 filled-outer
pairs and reconstructs every material value exactly. Every selected physical
pose matches its baseline exactly. This identifies copy coverage, without
establishing final quality or packing feasibility. The six failed pilot
comparisons remain authoritative. H2/H5 remain open at 60%.


**N4 exchange-failure observation, 2026-10-18:** [the isolated failure-detail observer qualifies](../benchmarks/results/h5-exchange-failure-observer-preparation-20261018.md).
All 130 optimized tests and strict code checks pass. The original short-circuit
conditions, clock reads and work charges are unchanged; extra loss/pose or
validated-trial data is recorded only inside existing failed branches.
Sixteen authored cases, 35 public baseline checks, twelve exact parent branch
witnesses, 34 malformed-record rejections and four synthetic parser cases pass.
The same two serial panel searches retain both kerfs, seed zero and 60 seconds.
Logging can change wall trajectories; no quality comparison or integration.
The committed scope requires independent checks of captured trials. H2/H5
remain open at 60%.


**N4 exchange-failure diagnosis, 2026-10-18:** [the focused cause audit is complete](../benchmarks/results/h5-exchange-failure-observer-20261018.md).
Recorded causes are 4 material increased, 18 source loss positive. All 4 captured final-trial
layouts validate independently, with exact metrics and independently rebuilt
material. Original/final geometry and every selected physical pose also pass.
Failed source snapshots remain diagnostic states. No quality rerun or
integration follows from these observations; H2/H5 remain open at 60%.


**N4 contained-return preparation, 2026-10-18:** [the isolated return-seed change qualifies](../benchmarks/results/h5-contained-return-preparation-20261018.md).
All 133 optimized tests pass, retaining all 130 prior tests. A fitting returned
group may translate inside the existing source bounding box, with charged
geometry work and an exact second check. Other cases keep the old poses.
Existing choices, budgets, repairs and full acceptance checks remain.
Two expected old-behavior failures and the first implementation's rotated-edge
failure are preserved; its small interior-seed correction changes no assertion.
Strict lint/build, twelve branch outcomes, 29 public CLI checks, deterministic
replays, exact source reconstruction and five harness checks pass. No quality
pilot has started; its plan must be committed first. H2/H5 remain open at 60%.


**N4 contained-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-contained-return-pilot-20261018.md).
The independent filled-outer audit checks 133,170 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.219533%; m-mechanical-large-plates at 1.5 mm: +5.440022%; m-mechanical-panel-hardware at 0.2 mm: +5.617328%; m-mechanical-panel-hardware at 1.5 mm: +5.658268%; c-bracket-mixed at 0.2 mm: +2.014519%
The candidate accepts 14/111 exchanges, including 12/74 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 14 parts. Of 3 neutral rejections, 0 are caught by exact internal-state equality and 3 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 free-space return preparation, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-free-return-preparation-20261018.md)
tries at most 256 translations per returned part against the source and earlier
returns, keeping each orientation and reflection. It checks filled-hole collision
geometry, charges work, observes the shared deadline, and always retains every
part with the previous seed as fallback. Original choices, repairs and strict
acceptance remain. All 137 optimized tests pass: 130 prior tests are unchanged,
three former no-improvement expectations now require strict material reduction
or exact incumbent retention, and four new regressions retain their expected
old-behavior failures. The first implementation's three failures remain with six
independent CLI checks proving the new authored improvement; runtime guards remain.
Four new frozen-CLI checks and independent filled-outer checks qualify two authored
outputs; 12 original branch outcomes, 24 branch validations, 10 public outcomes,
four public comparisons and five adversarial harness tests pass. Exact source
reconstruction, lint and build pass. The same matched pilot is ready to be planned;
no quality measurement has begun and no integration or H5 credit is earned.
H2/H5 remain open at 60%.


**N4 free-space-return outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-free-return-pilot-20261018.md).
The independent filled-outer audit checks 133,284 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.281226%; m-mechanical-large-plates at 1.5 mm: +5.706866%; m-mechanical-panel-hardware at 0.2 mm: +6.604732%; m-mechanical-panel-hardware at 1.5 mm: +5.890184%; c-bracket-mixed at 1.5 mm: +1.090957%
The candidate accepts 16/93 exchanges, including 13/62 paired and 1/4 mixed-item exchanges. Follow-up gap filling runs 16 times and moves 17 parts. Of 6 neutral rejections, 0 are caught by exact internal-state equality and 5 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 actual return-seed observation preparation, 2026-10-18:** the [isolated diagnostic](../benchmarks/results/h5-free-return-observer-preparation-20261018.md)
records actual contained/placed return poses, original source members, charged
work, repair losses and validated material outcomes including acceptance. It
reconstructs the failed candidate exactly after removing observations; all 137
tests remain unchanged and pass, as do lint and build. Sixteen authored cases,
35 frozen-CLI baselines, 32 trial validations,
twelve exact parent branch witnesses and 44 malformed-record checks qualify the
reader. Four serial mechanical diagnostics are planned; no measurement has begun.
Logging can affect wall trajectories and supports no quality claim. No production
change, reserved-input access or H5 credit. H2/H5 remain open at 60%.


**N4 actual return-seed diagnosis, 2026-10-18:** [four original-job outputs validate](../benchmarks/results/h5-free-return-observer-20261018.md).
The seed stage incurs work but changes none of 43 observed return poses. Of 24
attempts, two valid large-plate exchanges save only 28.887/132.567 mm², seventeen
panel source repairs retain positive loss and actual filled-outer violations,
and five valid panel trials increase material and are correctly rejected.
Four baselines/finals pass 37,119 filled-outer pair checks; all seven captured
material trials pass independent validation and exact material reconstruction.
The one-success-per-window caller motivates a bounded continuation experiment
under the same absolute deadline, after authored correctness checks. This is
not yet implemented and does not solve the panel repair failures. Original
limits, failed evidence, production and reserved inputs remain; H2/H5 stay open at 60%.


**N4 exchange-continuation preparation, 2026-10-18:** the [qualified isolated candidate](../benchmarks/results/h5-exchange-chain-preparation-20261018.md)
allows up to four exchanges under the original absolute deadline, continuing only
after a strict material gain. Rejection or an accepted flat result stops it. All
single-step guards and the preceding return initializer remain. All 141 optimized
tests pass, with 137 unchanged prior tests and four new regressions. The expected
two old-behavior failures and an earlier source assembly syntax failure remain.
Seven saved chain outputs pass fourteen frozen-CLI checks and independent geometry;
twelve original branch outcomes, 24 branch checks, ten public outcomes, four public
comparisons and five harness tests pass. Source reconstruction, lint and build pass.
The four-job matched pilot is ready to be planned; no new quality run has begun.
This does not resolve panel repair failures or earn H5 credit. H2/H5 remain open
at 60%; production and release claims are unchanged.


**N4 exchange-continuation outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-exchange-chain-pilot-20261018.md).
The independent filled-outer audit checks 133,153 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.359062%; m-mechanical-large-plates at 1.5 mm: +5.690931%; m-mechanical-panel-hardware at 0.2 mm: +6.541327%; m-mechanical-panel-hardware at 1.5 mm: +5.555891%
The candidate accepts 28/169 exchanges, including 25/101 paired and 2/5 mixed-item exchanges. Follow-up gap filling runs 14 times and moves 22 parts. Of 6 neutral rejections, 0 are caught by exact internal-state equality and 5 by the material profile before full validation. Counts do not establish time saving or improved final quality. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 continuous-repair qualification failure, 2026-10-18:** the [isolated allocation](../benchmarks/results/h5-continuous-repair-failure-20261018.md)
passes 142 tests and fails three unchanged exchange regressions. It uses the
existing relocation allowance and lets each source repair use its phase remainder.
The new source-repair witness validates, but the old larger-return and mixed-item
examples lose required swaps. Six independent validations confirm valid retained
incumbents with the same material as the preceding accepted results. The authored
delay is explicitly simulated; no wall-time or quality claim follows. All failures
remain, no assertions change, and no quality pilot starts. Next preserve the
original short phase, then allow strictly improving continuous repairs with the
remaining allowance. Production is unchanged; H2/H5 remain open at 60%.


**N4 two-phase repair qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-extended-repair-preparation-20261018.md)
retains the original short exchange phase, then uses the remaining existing
relocation allowance for longer source repairs. Both phases share four accepted
exchanges; the extended phase requires strict material gains. The original guards,
overall budget and validation reserve remain. All 148 optimized tests pass:
141 old bodies unchanged and seven new regressions. The three opportunities lost
by the rejected direct-long-source allocation match their prior witnesses exactly.
Both red runs and a corrected new frozen-sheet fixture are preserved. Thirteen
saved extended outcomes pass 26 CLI checks and independent geometry; the actual
source-repair fixture, original branch checks, public replay, source reconstruction,
lint, build and five harness tests also pass. A matched four-job pilot is ready
to be planned. No quality improvement, integration or H5 closure is claimed.
H2/H5 remain open at 60%; production and release claims are unchanged.


**N4 extended-repair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-extended-repair-pilot-20261018.md).
The independent filled-outer audit checks 133,152 same-sheet
pairs across 48 common-mode layouts. 5 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.499695%; m-mechanical-large-plates at 1.5 mm: +6.491064%; m-mechanical-panel-hardware at 0.2 mm: +5.679440%; m-mechanical-panel-hardware at 1.5 mm: +5.568800%; c-bracket-mixed at 1.5 mm: +1.594065%
The candidate accepts 44/472 exchanges, including 32/239 paired and 1/47 mixed-item exchanges. Follow-up gap filling runs 16 times and moves 27 parts. Of 24 neutral rejections, 0 are caught by exact internal-state equality and 23 by the material profile before full validation. Counts do not establish time saving or improved final quality. The extended phase accepts 20/322 attempts and rejects 191 material-flat trials. Six extended acceptances are mechanical; all flat rejections are bracket cases. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 provisional assignment qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-assignment-bridge-preparation-20261018.md)
keeps the original short search, then may cross validated material-flat steps
when last-sheet filled area strictly decreases. Only a final material gain commits
the sequence; incomplete steps roll back with their accepted counters. An actual
old-policy fixture demonstrates two flat steps followed by a valid material gain.
All 156 native tests pass: 148 old bodies, that witness and seven new policy tests.
Five expected old-behavior failures remain. Eight initial and 24 new-output CLI
checks, independent filled geometry, exact old witnesses, public replay, source
reconstruction, lint, build and five harness tests pass. The original four-step
cap, total deadline, validation reserve and geometry guards remain. No quality
comparison has begun, and no production change or H5 credit is claimed.
H2/H5 stay open at 60%.


**N4 assignment-bridge outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-assignment-bridge-pilot-20261018.md).
The independent filled-outer audit checks 133,388 same-sheet
pairs across 48 common-mode layouts. 4 of eight material pairs fail
the original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.936840%; m-mechanical-large-plates at 1.5 mm: +4.638902%; m-mechanical-panel-hardware at 0.2 mm: +6.747151%; m-mechanical-panel-hardware at 1.5 mm: +6.156172%
The candidate accepts 44/505 exchanges, including 32/267 paired and 4/44 mixed-item exchanges. Follow-up gap filling runs 17 times and moves 23 parts. Of 29 neutral rejections, 0 are caught by exact internal-state equality and 28 by the material profile before full validation. Counts do not establish time saving or improved final quality. The extended phase attempts 309 repairs and records 21 steps, including 5 flat steps. 18 steps belong to committed sequences; 3 roll back across 3 rollbacks. The canonical area guard rejects 189 flat trials. Committed intermediate steps need not each improve material; their sequence ends with strict whole-job improvement. Reject this candidate for integration; do not open the full 13-job gate for it. Production, frozen inputs and earlier failures remain
unchanged. H2/H5 remain open at 60%.


**N4 joint-repair witness, 2026-10-18:** the [unchanged-runtime authored test](../benchmarks/results/h5-joint-repair-witness-20261018.md)
shows why repairing fixed sheet assignments can fail: two source rectangles cannot
fit together even in the full usable sheet. The existing separator finds a valid
joint rearrangement by moving the extra source part to the receiver. Material
drops from 29,699.9994 to 28,799.9993 mm², with the earlier sheet exactly fixed.
Five independent CLI checks retain three valid outputs and two expected invalid
proposals; eight filled-outer pairs pass. One audit error compared authored f64
and converted f32 coordinates as byte-identical; it is preserved, and the corrected
audit reuses the same saved outputs without changing tolerance or rerunning search.
All runtime code and 156 prior test bodies remain unchanged; only the new test ran.
This proves a constructed case, not policy selection or development-job quality.
Next qualify a bounded joint-repair policy before any new matched pilot. H2/H5
remain open at 60%.


**N4 joint-repair qualification, 2026-10-18:** the [isolated candidate](../benchmarks/results/h5-joint-repair-preparation-20261018.md)
retains the short phase, then repairs only the selected receiver/source pair
within the remaining original allowance. It rechecks the exact cropped source,
lowers parts into freed space with existing bounded sampling, and commits a joint sequence only
after strict final whole-job material improvement. Incomplete sequences restore
their layout, tracker and accepted counters. All 165 native tests pass, including
157 unchanged prior tests and eight new policy tests. Independent validation covers
32 saved native layouts and 93 filled-outer pairs;
ten public outcomes, four CLI comparisons and six common-mode hole-reservation
checks pass. Source reconstruction, exact prior witnesses, lint and build pass.
The two insufficient-gain repairs, one newly invalid flat-fixture assumption,
initial compile error and audit error remain preserved. The rollback fixture uses the previously validated compacted output and
retains every assertion; runtime, guards and earlier tests are unchanged
by that fixture correction. A new committed pilot plan and harness checks are
still required before quality measurement. Production is unchanged; H2/H5 remain
open at 60%.

**N4 joint-repair pilot plan, 2026-10-18:** the [72-outcome plan](../benchmarks/results/h5-joint-repair-pilot-20261018/plan.json)
is prepared for the qualified isolated candidate. Four unchanged development jobs,
both kerfs, three seeds and three arms retain the original 60-second budgets and
rotating matched physical cores. Six execution/scoring functions are AST-identical
to the preceding pilot; all five existing adversarial harness tests pass. The
finisher retains archive/metric checks and adds joint-repair completion, expiry,
acceptance and rollback counter checks. Every outcome is retained; no search has
started at this checkpoint. Only a passing original material limit on every pilot
pair can open the full 13-job comparison. Production is unchanged; H2/H5 remain
open at 60%.

**N4 joint-repair outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-joint-repair-pilot-20261018.md).
The independent filled-outer audit checks 133,466 same-sheet
pairs across all 48 common-mode layouts. Five of eight material pairs fail the
original +1% limit. m-mechanical-large-plates at 0.2 mm: +5.612886%; m-mechanical-large-plates at 1.5 mm: +4.680766%; m-mechanical-panel-hardware at 0.2 mm: +6.781641%; m-mechanical-panel-hardware at 1.5 mm: +5.716098%; c-bracket-mixed at 1.5 mm: +1.481353%
There are 55/789 accepted/attempted exchanges. Joint repair attempts 589 pairs: 270 complete, 300 fail and 19 expire. It records 35 provisional steps, including 10 flat steps; 28 steps commit and 7 roll back across 4 rollbacks. Only committed counts survive rollback. Pair completion alone does not mean whole-job acceptance or final quality improvement. Reject this candidate for integration; do not open the full 13-job gate for it. The isolated candidate retains its 165 passing native tests,
prior witnesses and complete qualification evidence. Production remains unchanged.
The next diagnostic will trace actual accepted joint repairs and their material
gain before choosing another policy. H2/H5 remain open at 60%.

**N4 joint-repair observation plan, 2026-10-18:** the [diagnostic observer](../benchmarks/results/h5-joint-observer-preparation-20261018.md)
passes all 165 unchanged tests and preserves 86 exact native witnesses. Its 48
linked native trace records pass structural checks; nine malformed records are
rejected. Independent checks validate 23 saved layouts and 53 filled-outer pairs.
Four public fixed-work outcomes match the unobserved candidate exactly except
elapsed time. All 157 source files reconstruct, with 155 unrelated files unchanged;
lint/build pass. The first public reference-path error is preserved and its saved
outcome reused. The [four-case plan](../benchmarks/results/h5-joint-observer-20261018/plan.json)
retains both mechanical jobs, both kerfs, seed zero, 60 seconds and serial physical
CCD0 CPU 8. It records actual pair membership, material gains, repair/lowering
times, expiry, rejection and rollback. No development observation has started at
this checkpoint. Logging can change wall trajectories; no quality comparison,
pilot retry or integration follows. Production and the released preview remain
unchanged; H2/H5 remain open at 60%.

**N4 actual joint-repair diagnosis, 2026-10-18:** [all four serial diagnostics validate](../benchmarks/results/h5-joint-observer-20261018.md).
Fifteen attempts yield ten completed repairs, five committed steps, five
material-increase rejections and five expiries. Eight completed repairs move
extra members beyond the proposed swap, including all five accepted repairs.
Independent checking validates 40 saved layouts and 173,333 filled-outer pairs;
all 21 whole-job material values reconstruct exactly. Panel lowering never
reduces the source top in six observed stages. Four selected panel top pairs
expose a 10.901367 mm band when removed, before returns are placed. This motivates
an explicit source-boundary target, subject to an actual valid witness and full
qualification; it does not establish feasibility. Original limits, failures and
production remain unchanged. All six checks on pushed main `e0945cd` pass.
No quality/release claim or H5 credit; H2/H5 remain open at 60%.

**N4 source-frontier qualification, 2026-10-18:** [the explicit witness and automatic policy pass](../benchmarks/results/h5-frontier-preparation-20261018.md).
The original helper leaves the authored source at 87.200677 mm with its old crop
and finds 51.000558 mm under the exposed boundary. Automatic selection also finds
a valid strict gain and rolls back unfinished flat steps. All 171 native tests,
166 unchanged earlier tests, 139 exact earlier outputs, strict lint/build and six
public checks pass. Independent audits preserve quantities, fixed sheets and
reserved holes, including 856 public filled-outer pairs. The extra target scan
is charged; empty sources keep the original crop. All deadlines, the shared cap,
material limits and production remain unchanged. A new matched pilot is still
required; no H5 or release credit. H2/H5 remain open at 60%.

**Browser curve-test follow-up, 2026-10-18:** [the d414824 trace and local correction](../benchmarks/results/browser-curve-initial-layout-20261018.md)
preserve a Chromium import/export failure: no complete eight-part layout within
five seconds. This fidelity test now explicitly uses quick initial layout,
retaining the five-second allowance and all original assertions, with added checks
for all eight parts and the saved option. The full local suite passes 86 tests
with four skips, two workers and zero retries; hosted confirmation is pending.
Application source, benchmark limits and release assets are unchanged. H2/H5
remain open at 60%.

**N4 source-frontier pilot plan, 2026-10-18:** the [72-outcome matched plan](../benchmarks/results/h5-source-frontier-pilot-20261018/plan.json)
is ready for the qualified isolated policy. The same four jobs, two kerfs, three
seeds, ordinary/common baseline engines, 60-second allowance and rotating physical
cores remain. Six execution/scoring functions are AST-identical to the preceding
pilot; all five adversarial harness checks pass. The verified preflight confirms
that earlier local measurements are finished. Archive, metric, hole and rollback
checks remain; a separate counter identifies proposals with a tighter source crop.
No measurement has started at this checkpoint. Every original failure and threshold
remains. The full 13-job comparison still requires every pilot material pair to
pass. Production is unchanged; H2/H5 remain open at 60%.

**N4 source-frontier outcome, 2026-10-18:** [all 72 outcomes validate](../benchmarks/results/h5-source-frontier-pilot-20261018.md),
but five of eight material pairs fail the original +1% limit: m-mechanical-large-plates at 0.2 mm: +6.496681%; m-mechanical-large-plates at 1.5 mm: +4.989335%; m-mechanical-panel-hardware at 0.2 mm: +6.588633%; m-mechanical-panel-hardware at 1.5 mm: +5.416304%; c-bracket-mixed at 0.2 mm: +2.829306%
Independent checking covers all 48 common layouts and 132,966 filled-outer
pairs. The candidate records 63/347 accepted/attempted exchanges. Joint repair has 145 attempts: 63 complete, 61 fail and 21 expire. There are 143 proposed calls with tighter source crops, 35 committed joint steps and 5 rolled-back steps. All accepted counts exclude rolled-back steps. No candidate pair beats its matched common-baseline median.
Reject this candidate for integration. The next investigation checks saved layouts
for geometrically constructed transfers into narrow gaps missed by uniform sampling;
it must produce actual validated layouts before another policy is justified.
All limits and production remain unchanged; H2/H5 remain open at 60%.

**Hosted browser confirmation, 2026-10-18:** [main 4b13a85 passes the browser job](../benchmarks/results/browser-curve-hosted-confirmation-20261018.md):
86 tests pass with four opt-in skips, including the corrected curve import/export
test in Chromium and Firefox. The original failed job remains preserved. This
confirms the test-only correction; the separate Windows workflow checks are
still pending. Product source, release assets and gate limits remain unchanged.

**N4 saved-gap diagnosis, 2026-10-18:** [four saved mechanical layouts](../benchmarks/results/h5-saved-gap-diagnosis-20261018.md)
produce no fixed-neighbour transfers into earlier sheets in the tested convex-hull
or concave constructions. A direct-target source pass moves one insert without
material gain. Four smaller source moves per case save 0.054057–1.572117 mm of
height, recovering only 0.0348–0.7374% of the remaining material gap. All 33 public
CLI checks (21 unique layouts) and independent filled-outer checks pass. These are
post-hoc finite-angle geometry diagnostics, not quality/speed evidence or a proof
of infeasibility. Preserve them and investigate validated multi-part constructions
before proposing another runtime change. Production, budgets, four-step cap,
material limits and the published preview remain unchanged; completion stays 60%.

**N4 mixed-pattern diagnosis, 2026-10-18:** [verified component constructions](../benchmarks/results/h5-pattern-construction-20261018.md)
find compact two-bracket/one-insert groups and smaller free-angle round-part pairs.
All 446 component CLI checks and independent checks of 948 incomplete placement
attempts pass their stated scope. The component checks use subset quantities and
may enlarge stock; they do not validate a whole original job. Both large-plate
cases pass the refined finite-catalog area check, but no complete target placement
is found; the panel catalogs still exceed available area. Keep all failures and
test actual-outline placement and joint assignment before any runtime proposal.
No global infeasibility, quality or speed claim follows. Production, budgets,
repair cap, material limits and the preview remain unchanged; completion is 60%.

**N4 actual-outline construction, 2026-10-18:** [the retained beam and backfill](../benchmarks/results/h5-outline-construction-20261018.md)
test actual filled outer contours. All 159,819 beam additions replay; both panel
diagnostic timeouts remain explicit. Backfill adds 74 parts without moving existing
poses. The closest case places 63/66 parts, missing three cogs; every case remains
incomplete. Eight original public checks reject exactly the missing quantities.
The audit's null-metrics handling failure is preserved and repaired without new
packing searches. Next investigate collective repair of these saved partials,
first accounting for the native conversion guard, rather than treating physical
clearance as proof of zero native proxy loss. No runtime, gate limit or release
change; H2/H5 remain open at 60%.

**N4 saved-partial joint repair, 2026-10-18:** [four bounded native attempts](../benchmarks/results/h5-pattern-joint-diagnosis-20261018.md)
restore every missing original copy in explicit overlapping proposals; all original
partial poses remain exact. All four existing helper calls expire under seed 0
and their original 12-work-second diagnostic allowance, producing no complete
target layout. Every physically legal partial part already has positive native
collision loss. Next inspect exact native polygons and collision partners before
attributing this solely to conversion margins or designing another construction.
Rankings of all 308,326 recorded scores are checked; independent geometry checks
cover 32,527 original pairs and 5,395 selected-insertion comparisons. Input/build/audit harness failures remain
preserved; no native repair or quality run was repeated. Runtime, guard, budgets,
thresholds and release assets are unchanged; H2/H5 remain open at 60%.

**N4 native-margin diagnosis, 2026-10-18:** [exact native polygons and tracker entries](../benchmarks/results/h5-native-collision-diagnosis-20261018.md)
agree on all 51,175 checked pairs. The saved physical gaps are too tight for the
unchanged native inflation/edge margins. Translations below 0.18 mm produce four
partials with exactly zero native loss on each sheet and the joined strip; all
original sizes, rotations, assignments and stock targets remain. The extra
0.001 mm construction cushion still misses its declared limit and is preserved
as failed. Original public checks reject only the unchanged missing quantities;
13,566 additional filled-outer pairs pass. Restoring the same missing poses still
expires all four original-budget repair calls. Next observe the retained best
snapshot on expiry for the closest case, without accepting it or changing limits.
The f32 audit correction, original linearization failure and all failed repairs
remain preserved. Runtime/release assets stay unchanged; H2/H5 remain open at 60%.

**N4 terminal repair diagnosis, 2026-10-18:** [one fixed observational replay](../benchmarks/results/h5-terminal-repair-diagnosis-20261018.md)
reproduces the previous failure's exact work, statistics and expiry. The retained
best state reduces physical overlap 78.8441%, but has ten pair overlaps and one cog
47.7152 mm outside stock. All residual overlaps involve cogs; all 15 cogs move and
no frame moves. Original identities/quantities, budgets and rejection remain.
All 380 sampled fixed-neighbour cog free regions are empty. A collective local
linear step also fails actual geometry at all five tested fractions and accepts
no move. Independent original-shape checks cover 2,953 terminal-state pairs plus
7,485 collective-trial pairs; the original CLI rejects both terminal states and
the full collective proposal. Preserve these restricted failures, then investigate
joint selection of compatible actual-outline placements and alternative frame
allocations before another runtime proposal. All six prior main `cb5e23c` hosted
checks pass. Runtime, release assets and accurate READMEs remain unchanged;
H2/H5 stay open at 60%.

**N4 joint saved-placement selection, 2026-10-18:** [a finite binary construction](../benchmarks/results/h5-saved-placement-selection-20261018.md)
selects among 2,614 original-outline poses, including all 25 prior frame
configurations. The known 63-part partial certifies model feasibility; all frame
locations are selectable. The 120-second solve ends at its limit with a different
63-part arrangement, still missing three cogs. An independent reconstruction
enumerates 2,700,951 candidate pairs and verifies the exact 332,265-edge conflict
graph; all 1,303 selected-part pairs pass, and the original CLI rejects only the
missing quantity. The solver's finite-pool bound is recorded without a global
infeasibility claim. Preserve the timeout and generate new contact positions
before any further selection attempt; no unchanged-pool or native search repeat.
Production, targets, limits, release assets and accurate READMEs stay unchanged;
H2/H5 remain open at 60%.

**N4 expanded contact selection, 2026-10-18:** [8,798 verified poses](../benchmarks/results/h5-contact-selection-20261018.md)
include 3,600 new outline contacts and sheet half-turns. Independent enumeration
of 29,902,803 pairs reproduces all 2,517,051 conflicts and verifies the equivalent
17,097-clique model. Three bounded MILP mechanism attempts preserve their timeouts
and the same 63-part partial. Disabling expensive presolve reaches the first
relaxation quickly but gives no better layout. Exact-inventory CP-SAT requires all
66 parts; its initial runtime crash and failing tiny probe are retained. Standard
CPython, with the same package versions, passes the probe and solves the identical
model bytes to UNKNOWN at 120 seconds, returning no complete layout. Independent
model parsing verifies every exact quantity and nonbinding hint. Next investigate
coordinated multi-cog components from actual contacts, retaining full original-job
validation before any feasibility claim. All six prior main `5743a32` checks pass.
No native quality run, runtime, gate, release or README change; H2/H5 remain at 60%.

**N4 coherent cog groups, 2026-10-18:** [162 alternating lattices](../benchmarks/results/h5-cog-lattices-20261018.md)
produce 1,134 verified components and pass 45,360 independent pair checks.
All 504,000 fixed-column whole-job constructions finish without a full layout;
the greatest filled-area result is 52/66, missing fourteen inserts. Eight distinct
outline-gap continuations add fifteen parts total but remain partial; all 144
proposed additions and 10,915 final pairs independently check, with original CLI
quantity failures only. A separate exact-inventory rectangle model frees all
frame positions and chooses one of five full cog decompositions. Independent
parsing verifies all 471 variables and 517 constraints. The one 120-second search
ends UNKNOWN, not infeasible, without a full selection. The earlier 63/66 partial
remains better. Next investigate ragged staggered cog rows with actual contact
pitches; preserve all quantities, stock targets and full-layout validation.
No native packing, quality run, production, gate, release or README change;
H2/H5 remain open at 60%.

**N4 ragged cog pockets, 2026-10-18:** [54 staggered variants](../benchmarks/results/h5-ragged-pockets-20261018.md)
produce 324 valid groups with 20,034 independently checked pairs. Filling their
actual inter-part pockets produces 48 verified components: 1,197 proposed
additions, 6,301 final pairs and 237 accepted additions across variants. Four
complete original-inventory recipes pass their restricted rectangle-area test;
two area failures remain preserved. Three serial 120-second models test free
rectangle placement, proven full-width separator symmetry, and normal subset-sum
coordinates. Independent parsing verifies exact quantities, targets and every
model difference; independent enumeration verifies all reduced coordinate domains.
All three return UNKNOWN without a full selection. The earlier 63/66 partial is
not improved. Next inspect the documented cumulative/area propagation flags with
one controlled same-model experiment, preserving all limits and failures. All six
main 67e77b1 checks pass. No native packing, quality run, production integration,
gate credit, release or README change; H2/H5 remain open at 60%.

**N4 contact direction and outline construction, 2026-10-18:** [actual-outline investigations](../benchmarks/results/h5-outline-contact-direction-20261018.md)
retain the unchanged-model propagation timeout and all unsuccessful fixed/adaptive
constructions. Caching exact primitive exclusions lets all eighteen fixed-order
searches finish their original allowances; cached primitives and translation terms
audit exactly. Retained-layout checks cover 30,621 pairs; all best layouts remain
incomplete. The empty-sheet audit failure and corrected unknown return-code
metadata are preserved. A directed-contact probe exposes a better global rotation.
The subsequent declared 36-phase scan gives 324 verified components and 13,860
pair checks at minimum 0.225123442 mm. Its 15-cog rectangle is 5.6804% smaller than
the earlier sampled-angle component; this is not whole-job material savings.
Next use contact-aligned staggered rows and the retained bracket-pattern aspect
choices in a complete original-inventory construction. No native packing, quality
run, runtime integration, release, README change or gate credit; H2/H5 remain 60%.

**N4 aligned pockets and frame rows, 2026-10-18:** [verified contact-aligned components](../benchmarks/results/h5-aligned-pockets-and-rows-20261018.md)
include a fifteen-cog group with three inserts, preserving every original outline
and all group bounds. Checks cover 224 filled alternatives, 5,511 proposed
additions and 29,724 component pairs. The independent-bracket-aspect model remains
UNKNOWN. Column and row constructions retain 2,711,981 attempted arrangements;
the row cap leaves 60,583 unattempted. Twenty-four outline continuations preserve
27,954 checked pairs, but all remain incomplete. The best new 58-part layout lacks
eight inserts and still has less filled area than the earlier 63-part partial.
A diagnostic census supplies 261 new geometric signatures for the next exact-count
placement-selection pool; original coordinates remain untouched. All six f825cab
checks pass, and c9b0176 is pushed to main. Original failures, native-margin caveats
and all gate limits remain; no runtime/release/README change or gate credit. 60%.

**H2 gate decision, 2026-10-20:** Artem [chose to keep the original 25-file
gate and leave H2 open](../benchmarks/results/h2-gate-decision-20261020.md).
The proposed positive-only denominator is not adopted. Two deliberate negatives
cap literal exact-import success at 92%, below the unchanged 95% requirement.
This is a classification bound, not a measured held-out result. The pending
question is resolved; frozen labels/split and once-only native outcomes remain,
and no remaining reserved vector is opened. Completion remains 60%.

**N4 coordinated contact selection, 2026-10-20:** [the completed model audit](../benchmarks/results/h5-coordinated-contact-selection-20261020.md) preserves three earlier bounded selections and
adds 2,260 exact cog-contact poses. Independent checks reproduce 774,312 new
conflicts over 10,571,998 added same-sheet pairs and verify all 24,750 model
constraints. The changed 120-second construction returns the identical 58-part
partial, missing eight inserts; its original CLI rejection and measured
121.154159-second elapsed time remain. The insert bound stays 21, so no full
layout or impossibility is proved. Next inspect necessary local area capacities
before another changed-model attempt; do not repeat these models or extend
their limits. All six c9b0176 checks pass and c824e5a is pushed to main.
No runtime, native-quality, release, README or gate change. H2/H5 remain at 60%.

**N4 local-area bounds, 2026-10-20:** [58 necessary stock capacities](../benchmarks/results/h5-area-capacity-relaxations-20261020.md)
pass exact rational checks on 75,957 positive coefficients, preserving the
complete 58-part hint. All six continuous relaxations finish within their declared
limits; the four cases fixing each cog arrangement remain fractional. Exact
independent dual reconstruction keeps the insert bound at 21 in every case,
with only the original quantity cap active. No full layout or impossibility
is established and no integer search is repeated. The original preparation
syntax failure is retained. Next investigate a bounded whole-placement
construction guided by these fractions, retaining every branch and the original
acceptance rules. Remote landing pages and READMEs are reconciled exactly and
pushed as 8a81205; the hosted main preview is verified. H2/H5 remain open at 60%.

**N4 whole-group diagnosis, 2026-10-20:** [bounded branching and fixed-group completion](../benchmarks/results/h5-whole-group-diagnosis-20261020.md)
retain all 421 LP branches, 227 checked fractional solutions and 41 unvisited
frontier entries. No branch completes 18 frames. A separate census finds 26
retained complete frame sets, of which only six combinations with the four cog
sets are compatible. Six independently reconstructed fixed-group models solve
in under 0.6 seconds each, with solver-reported maxima of 12, 12, 10, 11, 13 and
13 inserts. All 21 returned partial layouts pass original geometry checks and
fail the frozen CLI only for missing inserts. No improvement, full-layout credit
or unrestricted impossibility claim. Original environment/auditor failures are
preserved and no solver run is repeated. Next investigate new complete frame
arrangements while relaxing only the smaller-part choices, explicitly excluding
the 26 reviewed exact frame sets before bounded completion checks. H2/H5 remain
open at 60%; runtime and README contents are unchanged.

**N4 frame/bracket capacity, 2026-10-20:** [four new frame constructions and exact bracket bounds](../benchmarks/results/h5-frame-bracket-diagnosis-20261020.md)
follow four preserved 30-second mixed-model timeouts. A changed frame-only
heuristic finds four new final frame sets; all 19 returned frame/cog proposals
pass original geometry checks. Four independently reconstructed completion
models reject these sets without a layout. Removing inserts and reconstructing
exact rational dual bounds proves that their surviving finite poses allow at
most 7, 7, 10 and 10 brackets, below the required 12. This does not prove the
unrestricted job impossible. Individual pose availability is insufficient;
next select all 18 frames and 12 brackets together before exact insert
completion. No expired model is extended, no quality run occurs and no gate
changes. H2/H5 remain open at 60%; runtime and README contents are unchanged.

**N4 certified reduction and starting layouts, 2026-10-20:** [joint construction and safe pose substitution](../benchmarks/results/h5-dominated-poses-and-seeds-20261020.md)
preserve eight bounded searches without incumbents. Independent set checks
verify 4,105 same-family substitutions across four cases, preserving future
insert compatibility and frame exclusions while removing 26–30% of joint
variables. Direct substitution of known partials produces six valid partials
using three distinct new exact frame sets. Their bounded insert completions retain 12, 12, 10, 11, 13 and 13
inserts; all twelve original CLI checks fail only the required insert quantity.
Exact checks across 57,374 constraints establish complete feasible starting
hints for all four reduced joint models. Next optimize actual whole-insert
count with these hints, retaining all conflicts and original acceptance rules.
No full layout or improvement is claimed; H2/H5 remain open at 60%.

**N4 seeded search and local-move bounds, 2026-10-20:** [the complete audit](../benchmarks/results/h5-seeded-search-and-move-bounds-20261020.md)
preserves four seeded fixed-cog searches and one search with all cog positions
movable; none improves its 12/13-insert starting count. Independent checks verify
2247 safe pose substitutions and all returned geometry. Exhaustive enumeration
and clique certificates prove that all 331 zero/one/two-core moves about the
mapped seed allow at most 13 inserts within the retained finite pool. A changed
three-to-six-move search for at least 14 inserts times out without a candidate;
larger moves and new continuous positions remain unresolved. Next diagnose
compatible insert sets and their exact core blockers before generating changed
contact positions. No unchanged search is repeated and no full-job credit is
awarded. Prior local 6cde1bd and 56f818a are pushed to main; all six f6edfb7
checks pass. The README accurately describes the existing preview. H2/H5
remain open at 60%; runtime and release assets are unchanged.

**N4 complete-insert blockers and new frame contacts, 2026-10-20:** [the full audit](../benchmarks/results/h5-insert-blockers-and-frame-contacts-20261020.md)
verifies a 21-insert diagnostic after temporarily removing two frames. Exact
clique certificates over all 1036 zero/one/two-core deletions prove that at
least two saved core poses must be removed within this insert pool; they do
not independently prove the secondary area tie. The 64-part diagnostic packs
less filled area than the known 58-part partial and receives no improvement
credit. Two bounded completion searches, the second adding 240 new exact frame
contacts and restoring original core choices, both retain only 16 frames.
Independent geometry verifies all ten returned layouts, 179,683 new conflicts
and complete clique coverage. Both original missing frames remain required.
Next check frame-only capacity before selecting a different insert arrangement
or diagnosing bracket/cog obstructions. All six 56f818a hosted checks pass and
f321537 is pushed to main. H2/H5 remain open at 60%; runtime, README and release
assets are unchanged.

**N4 frame capacity and joint small parts, 2026-10-20:** [the complete audit](../benchmarks/results/h5-frame-capacity-and-joint-small-parts-20261020.md)
finds two geometry-verified 18-frame arrangements around all 21 inserts. Their
fixed-group small-part optima are 16 and 13; independent clique certificates
allow at most 8 and 6 cogs, below the required 15. A changed joint model keeps
all 18 frames and increases its own seed from 16 to 21 small parts, ending with
all 12 brackets and 9 cogs after one 30-second limit. All 18 returned layouts
pass original geometry and retain their quantity-only CLI failures. Six cogs
are still missing, and filled area remains below the known 58-part partial.
Next construct new cog contacts around the final 51 non-cog poses; do not
repeat expired searches. Remote abeb2739's comparison page and README link
merge cleanly as 09f59894, preserving 11 incoming and 25 local files. Its push
cancelled f321537's remaining Windows/Linux checks. No complete CI success
or release is inferred. H2/H5 remain open at 60%; core source is unchanged.

**N4 cog free regions and continuous capacity, 2026-10-20:** [the independently audited certificate](../benchmarks/results/h5-cog-free-regions-and-continuous-capacity-20261020.md)
proves at most **13 cogs** fit around the current 51 fixed non-cog poses,
even allowing arbitrary angles and continuous positions. The original job
requires 15, so at least one frame, bracket or insert must move. Earlier
finite sampling adds 437 cog poses but still selects nine; both returned
layouts pass original geometry and retain their six-missing-cog CLI failures.
The weaker finite cover of 14, continuous box bound of 18 and band bound of 16
are preserved. Exact reachable-area checks allow 10 cogs on the first sheet;
an independently verified diameter cover allows 3 on the last. This is a
conditional upper bound, not an attainable 13-cog layout or a claim after other parts move.
Next audit which single non-cog releases can remove this obstruction;
do not repeat the ruled-out cog-only search. Core source and all three README
hashes remain unchanged. No native quality run or new release is qualified.
H2/H5 remain open at 60% under the original requirements.

**N4 single non-cog release census, 2026-10-20:** [all 51 independently audited cases](../benchmarks/results/h5-single-non-cog-release-census-20261020.md)
rule out completing the current arrangement by moving only one bracket or
insert: all 12 bracket and 21 insert choices have cog capacity below the
required 15, even when the removed part is omitted entirely. All 121 center
components and 242 diameter covers verify. A separate component certificate
tightens the last insert case from 15 to 14; its original loose result remains.
The 18 frame releases remain inconclusive at bounds of 15–17, with no new
layout or feasibility claim. Next analyze changed frame positions while
preserving the other 50 non-cog poses; multiple-part changes remain possible.
All six hosted checks on remote abeb2739 now pass. Core source, README and
release assets are unchanged; no native quality or held-out run occurs.
H2/H5 remain open at 60%.

**N4 continuous single-frame regions, 2026-10-20:** [the complete audited record](../benchmarks/results/h5-single-frame-continuous-regions-20261020.md)
covers all 72 frame/size-class/sheet queries and retains all 18 original frame
poses. Guaranteed occupied rectangles exclude 16 of 52 whole center regions.
A changed midpoint subdivision stops at its declared 120-second boundary
after 165 new cases, preserving 49 pending nodes. Independent exact geometry,
area and tree-coverage checks rule out ten of the eighteen single-frame moves.
Together with the previous small-part certificates, 43 single non-cog changes
are excluded and eight frame choices remain unresolved. No unfinished tree
is treated as a proof. Next construct and audit changed frame/cog candidates
within the remaining regions; do not extend the expired tree unchanged.
Core source, README and releases remain unchanged. H2/H5 remain open at 60%.

**N4 joint frame/cog constructions, 2026-10-20:** [all eight changed models and audits](../benchmarks/results/h5-joint-frame-cog-construction-20261020.md)
combine one movable frame with free cog choices around the other 50 fixed
non-cog poses. The 80 queries add 853 frame and 641 cog poses across the conditional
sets; every proposal, filter and relevant pair conflict is independently checked.
All eight finite-pool models report an optimum of nine cogs, without hitting
their 20-second limits. All 16 returned layouts pass original geometry and
retain the six-missing-cog CLI failure; 12 CLI calls are fresh and four exact
results are reused. No partial improves and no unrestricted impossibility is
claimed. Next investigate coordinated whole groups with all small-part families
free, after reviewing prior frame-group results; do not repeat these models.
Core source, README and releases remain unchanged. H2/H5 stay open at 60%.


**N4 joint frame-group selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-group-choice-20261023.md)
chooses among 26 complete frame groups while all bracket, cog and insert poses
remain free. A recomputed 5,302-pose graph and complete model pass independent
checks. One 60-second search returns a 62-part partial: all 18 frames and 12
brackets, 13 cogs and 19 inserts. Filled area reaches 4,342,015.346194 mm² within
the original material allowance, but two cogs and two inserts remain missing.
All four returned layouts pass original geometry and retain quantity-only CLI
failures. The final bound is unresolved; no optimum or full-job pass is claimed.
Next diagnose free regions and construct changed contacts, preserving the new
seed; do not repeat the expired model. Incoming e9046d53’s comparison index and
both pending evidence commits are merged and pushed as 44ff9cc4. Its checks are
recorded separately. Core source and all three READMEs remain unchanged; the
published preview is still accurate and no new release is qualified. H2/H5
remain open at 60%, with original gates and held-out isolation preserved.


**N4 continuous capacity and cog/insert contacts, 2026-10-23:** [the complete audit](../benchmarks/results/h5-cog-insert-regions-20261023.md)
checks three continuous cog-capacity bounds (18, 22 and 35), all inconclusive.
Around the saved 30 frame/bracket poses, 12 queries add 196 cog and 72 insert
poses. All 259,549 conflicts, full clique coverage and the model pass independent
checks. One bounded solve reports a finite-pool optimum with the same 62 parts;
both returned layouts pass geometry and retain their two-cog/two-insert CLI
shortfalls. No filled-area improvement or unrestricted impossibility is claimed.
A distinct three-column/six-row group of all 18 wider frames and 11 optional
side-strip inserts passes 406 geometry pairs. Next complete its small families
with newly audited candidates and conflicts; do not retry the fixed-core model.
Core source, README and releases remain unchanged. H2/H5 stay open at 60%.


**N4 wider-frame small-part selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-wide-small-selection-20261023.md)
checks 10,066 poses and all 5,286,767 conflicts. Certified same-family substitutions
retain 7,776 choices; every dropped alternative preserves counts and filled area.
The insert cap, 834 pending lists, compression cap and reduction cap are preserved.
One bounded 60-second solve places 62/66 parts, missing four cogs; its filled area
is below the prior best. All nine hint/returned layouts pass geometry and retain
their original CLI quantity failures. No optimum or full witness is claimed.
A finite audit of saved denser cog groups finds 488 absent poses and verifies
135 placed subassemblies. Next combine those coordinates with new small-part
contacts under fresh declared limits; do not repeat the expired model. All six
44ff9cc4 hosted checks pass and the prior checkpoint is pushed as 37edb1d2.
Core source, accurate READMEs and releases remain unchanged. H2/H5 stay open at 60%.


**N4 denser-cog progress, 2026-10-23:** [the complete audit](../benchmarks/results/h5-dense-wide-progress-20261023.md)
improves the retained partial to 64/66 original parts, missing two cogs. Filled
area is 4,381,615.346194 mm², 39,600 mm² above the previous best, under the same
material target. All 750 new contact queries, 7,910,375 conflicts, fresh safe
substitutions and 3,000 group-based starting layouts are checked. One bounded
solve reaches 63 parts; a new gap query appends an insert without moving any
of them. All original geometry checks pass and the frozen CLI retains the two-cog
quantity failure. Native margins remain unqualified. The new fixed-non-cog
continuous capacity bound is 19 (18 first sheet, one last), inconclusive for 15.
Next construct and audit a changed cog-only pool against those exact 51 non-cogs;
do not retry the expired all-small model or capped lists. Original requirements,
source, accurate READMEs and release assets remain; H2/H5 stay open at 60%.


**N4 fixed-part cog limit, 2026-10-23:** [the complete audit](../benchmarks/results/h5-dense-cog-limit-20261023.md)
preserves the best 64/66 partial. Sixteen new queries and all compatible prior
poses give 2,846 cog choices. All 1,169,914 conflicts and model fields are checked;
one bounded solve proves a finite-pool optimum of 13 cogs with all 51 non-cogs
fixed. The two-cog CLI shortfall remains. No unrestricted impossibility is claimed.
An independent 165-case complete-cog census finds that these particular groups
require at least eight small-part moves. The selected checked 58-part subassembly
contains all frames/cogs and needs three brackets plus five inserts; it does not
improve the retained partial. Next test a newly bounded completion of those eight
parts, preserving original geometry, production repair limits and full H5 scope.
Prior checkpoints are pushed as 2333dd2c. Source, accurate READMEs and releases
remain unchanged; H2/H5 stay open at 60%.


**N4 complete-cog small-part relocation, 2026-10-23:** [the complete audit](../benchmarks/results/h5-complete-cog-small-relocation-20261023.md)
preserves the best 64/66 partial. Around the checked 58-part subassembly, all 20
new queries finish; 99 insert choices yield a finite optimum of three additional
inserts. A distinct model fixes only the 18 frames and all 15 cogs, freeing every
bracket and insert. Its 2,045 choices, 342,611 conflicts and full model pass
independent checks. One bounded solve retains 61 parts, missing three brackets
and two inserts. Its bound excludes the complete inventory in this finite pool;
no continuous impossibility or optimum is claimed. All returned original layouts
are audited and their quantity-only CLI failures retained. No pending list is
resumed and no solve repeated. Next compare other saved complete-cog arrangements
with small parts free, using fresh declared limits. Source, accurate READMEs and
releases remain unchanged; H2/H5 stay open at 60%.


**N4 complete-cog group choice, 2026-10-23:** [the complete audit](../benchmarks/results/h5-complete-cog-group-choice-20261023.md)
preserves the best 64/66 partial. All 1,670 newly declared group/contact queries
and 3,300 starting layouts complete. The 9,089 choices, 165 group decisions,
3,051,661 conflicts and full model pass independent checks. One bounded solve
reaches 63 parts, missing three brackets; its filled area remains below the
retained result and its bound is unresolved. All four original layouts pass
geometry and retain quantity-only CLI failures. The 980 capped lists remain
pending. A new 210-combination coverage audit identifies 200 additional complete
cog groups, including 12+3 and 10+5 distributions across sheets. Next test those
changed group choices under fresh limits; do not repeat the expired model.
All six prior-main checks pass and both saved checkpoints are pushed as 37b671d3.
Source, accurate READMEs and releases remain unchanged; H2/H5 stay open at 60%.


**N4 two-sheet cog progress, 2026-10-23:** [the complete audit](../benchmarks/results/h5-two-sheet-cog-progress-20261023.md)
improves retained filled area by 325.437876 mm² with a checked 63-part layout,
missing two brackets and one insert. The previous 64-part result remains the
highest-count partial. All 365 groups, 500 new contact queries, 6,603,323 conflicts,
fresh group-preserving substitutions and 7,300 starting layouts are checked.
One bounded solve and all four original layouts retain quantity-only failures;
the full-inventory bound remains unresolved. All 541,132 residual edges and 322
capped lists are preserved. Twenty new fixed-layout gap queries are empty under
positive padding. A separate 18-frame/15-cog subassembly in four tall columns
with 8+4+3 cogs passes original geometry and the expected CLI quantity failure.
Next complete its brackets/inserts under fresh limits; it is not a new best
partial or production repair. Source, accurate READMEs and releases remain
unchanged. H2/H5 stay open at 60%.


**N4 alternate-frame compound limits, 2026-10-23:** [the full audit](../benchmarks/results/h5-frame-compound-limits-20261023.md)
checks actual-outline bracket/insert compounds around the tall 8+4+3 and mixed
9+1+5 cog cores. Both fresh finite models reach optimal area below full inventory;
neither improves the saved 63-part area or 64-part count partials. All 616 queries,
3,337,889 conflicts, fresh reductions, model fields and 14 original layouts are
checked; only expected missing quantities fail. The original preflight reader
failure and 97 capped lists remain preserved. A new coverage audit retains every
earlier all-family choice plus 8,914 compatible additions around the 18 wide
frames. Next build its complete graph and select cogs/brackets/inserts together
under fresh limits, preserving both checked seeds. All six checks passed on
37b671d3, then queued checkpoints were pushed to main 4592d97c; its checks are
recorded separately. Source, accurate READMEs and releases remain unchanged.
H2/H5 stay open at 60%; no reserved files or production quality runs are used.


**N4 improved joint partial, 2026-10-23:** [the complete audit](../benchmarks/results/h5-latest-wide-joint-progress-20261023.md)
places all frames, cogs and inserts: 64/66 parts, lacking two brackets. Filled
area improves by 19,800 mm² over the previous best; all older partials remain.
The complete 21,468-choice graph, 20,223,984 conflicts, fresh substitutions,
1,877,444 retained residual edges and every model field are checked. One bounded
solve returns feasible; all five original layouts pass geometry with expected
quantity-only failures. Sixteen new fixed-layout bracket regions are empty under
positive padding. The next checked 33-part core has four changed cog poses and
preserves the new 64-part seed for fresh actual-compound bracket/insert contacts.
No previous solve, capped list or unchanged gap check is resumed. Main's current
checks remain separately recorded; queued commits await their successful finish.
Source, accurate READMEs and releases remain unchanged. H2/H5 stay open at 60%.


**N4 improved-core compound limits, 2026-10-23:** [the full audit](../benchmarks/results/h5-wide-core-compound-limits-20261023.md)
preserves the 64-part baseline through two newly bounded compound models. Both
reach a finite optimum with two brackets missing; no unrestricted impossibility
is claimed. All 536 queries, complete graphs, fresh reductions, model fields and
six original layouts are checked. The reflection census verifies 114 geometries
absent from previous queries; all 190 capped lists and 1,336,544 residual edges
remain preserved. A new 29-frame-group coverage audit checks every membership
and retains 29,631 compatible small poses plus the exact 64-part seed. Next build
its complete mutual graph and choose frames/cogs/brackets/inserts together under
fresh limits. Main's 7cd00432 checks remain separately recorded. Source, accurate
READMEs and releases remain unchanged; H2/H5 stay open at 60%.


**N4 expanded frame-group selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-expanded-frame-joint-20261023.md)
checks a fresh 29,631-pose graph with 33,489,837 conflicts across all 29
whole frame groups. Group-preserving substitutions retain the 64-part baseline;
all residual edges and pending work remain. The first bounded solve returns
`UNKNOWN` during presolve. A changed exact implication encoding preserves
every edge, reduces constraints from 12,149,516 to
40,193, and returns `UNKNOWN`
during presolve. A fresh, cheaper clique cover retains all edges, reduces
residuals to 5,257,882, and its separately bounded changed
model returns `UNKNOWN`. Every original layout is audited;
an independently verified no-presolve strategy then reaches search on the
byte-identical model and returns `FEASIBLE`.
No full 66-copy witness is found. A separate coverage audit exposes 2,358
additional individual frame poses and 3,358
additional small poses by removing the whole-frame-group restriction. The next
model needs a fresh complete four-family graph. Previous checkpoint 955cc87e is
pushed after all six 7cd00432 checks pass. Product source, accurate READMEs and
releases remain unchanged; H2/H5 stay open at 60%.


**N4 individual-frame joint selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-individual-frame-joint-20261023.md)
frees every original frame pose and all three small families across the full
35,488-pose pool. All 38,969,399 new four-family conflicts, original
transforms/stock bounds and both 64-part seeds are independently checked.
Fresh substitutions and first-fit constraints preserve every induced edge;
all model and parameter fields are verified. One unchanged-allowance solve
returns `FEASIBLE`. Best checked inventory: 64/66;
missing {"bracket": 2}. Native and complete H5
qualification remain open. All 16 conservative bracket insertion regions for
the distinct final layout are empty. Thirty fresh repair cores, each freeing
one cog plus all brackets and inserts, preserve both 64-part layouts and all
989,670 independently checked memberships; their conditional selection is
pending. The earlier 752b1c60 checkpoint is pushed after
all six 955cc87e checks pass. Source, accurate READMEs and releases remain
unchanged; H2/H5 stay open at 60%.


**N4 one-cog repair selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-one-cog-release-joint-20261023.md)
selects one of 30 checked 18-frame/14-cog cores and jointly relocates a cog,
all brackets and all inserts. Every original conflict, core membership,
substitution, model field and parameter is verified. Fresh reduction completes
at 6,641 variable poses; complete first-fit compression preserves all 4,686,314
reduced conflicts with no residual edges. One 60-second solve reaches search
and returns `FEASIBLE`; all three original layouts remain 64/66, missing two
brackets. The full bound is unresolved. No native or production qualification
is inferred. Main 752b1c60 awaits its last Windows check, with d49d0ff6 committed
locally. Source, READMEs and releases remain unchanged; H2/H5 stay open at 60%.


**N4 continuous cog contacts, 2026-10-23:** [the complete audit](../benchmarks/results/h5-one-cog-continuous-regions-20261023.md)
preserves a failed mitre-buffer equivalence check and a failed round-buffer
alternative, then verifies an explicit circumscribed 128-gon clearance helper.
All 120 new one-cog region queries complete; 4,000 new poses pass original
geometry and all 120,000 memberships across 30 fixed cores. There are 3,971
new centers beyond 0.05 mm and 2,075 poses opening old bracket choices, which
are candidate diagnostics rather than additional placed parts. All 60 capped
proposal lists remain recorded. The 20,058-choice joint graph and selection
are pending; best checked inventory remains 64/66. Both queued checkpoints
are pushed to main facf0f38 after all six 752b1c60 checks pass. Source, READMEs,
releases and gate requirements are unchanged; H2/H5 stay open at 60%.


**N4 continuous-cog joint selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-continuous-cog-joint-20261023.md)
checks all 20,058 choices, 6,917,176 new geometric conflicts and a separately
justified count-derived cog clique. Fresh substitutions retain 6,808 choices,
including 197 new cogs, with all 30 baselines preserved. Complete compression
and every model/parameter field verify. One bounded solve reaches active
search and returns `FEASIBLE`; all three original layouts remain 64/66,
missing two brackets, with the full bound unresolved. Five new 33-part cores
are checked for a fresh bracket/insert contact investigation; their old
candidate-count rankings are not inventory gains. Main facf0f38 checks are
pending and 5e88ac91 is committed locally. Source, READMEs, releases and gate
requirements remain unchanged; H2/H5 stay open at 60%.


**N4 changed-core small-part selection, 2026-10-23:** [the complete audit](../benchmarks/results/h5-shifted-core-small-joint-20261023.md)
checks 4,000 fresh small-part poses across seven fixed cores, all 211,995
memberships and a new complete 19,719,151-conflict graph. Certified reduction
retains 4,739 choices, including 1,246 new poses; every constraint and model
field verifies. One bounded solve finds a different 63/66 layout: 11 brackets,
19 inserts, all 18 frames and 15 cogs. It fills 400 mm² more but misses one
bracket and two inserts. Both original 64-part baselines remain preserved.
All four original layout audits pass geometry and fail only original missing
quantities. Forty fresh padded insertion regions are empty, without an
impossibility claim; coordinated small-part moves are the next investigation.
All 1,950 capped member lists and the unresolved full bound remain preserved.
Main facf0f38 passes all six checks, and checkpoints 5e88ac91/0526421e are pushed.
Source, READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 pair-contact selection and repository refresh, 2026-10-25:** [the complete audit](../benchmarks/results/h5-small-pair-joint-20261025.md)
checks 60 paired-release neighborhoods, 600 regions and 3,435 new small-part
positions. All memberships and the complete 28,976,111-conflict graph verify.
Certified reduction preserves both 64-part and both 63-part baselines. One
bounded search returns the same 63-part area result, missing one bracket and
two inserts; all three original layout checks fail only on quantities. The
full bound remains unresolved and all 27 deferred insert lists remain saved.
The next investigation is a continuous occupied-area relaxation for the seven
fixed cores, with conservative coverage checks before any negative conclusion.
Merge 55835d7c preserves the nine incoming Inkbolt example/website files and
all 37 local checkpoint files byte for byte, and is pushed to main. Main
4045822e passed all six checks and Pages; the refreshed upstream stop rule
does not fire. Engine source, READMEs and releases remain unchanged; H2/H5 stay open
at 60% completed milestone weight.


**N4 continuous occupied-area audit, 2026-10-25:** [the independent audit](../benchmarks/results/h5-occupied-area-relaxation-20261025.md)
checks all 168 queries, twelve permitted orientation/reflection classes and
seven fixed arrangements. All 99,983 known compatible polygon/translation
memberships and four prior baselines are covered. Every combined and family
area upper bound exceeds the required inventory; no core is excluded and no
packing feasibility is established. A failed round-offset assertion and its
repaired subset check are preserved without regenerating geometry. A separate
source-derived distance census finds only core 0 meets both conservative pair
and stock screens; actual native qualification remains required. Next build
an exact-count direct-coordinate model for its 12 brackets and 21 inserts,
with independently checked inward rounding, original outlines and new declared
limits. No solver retry, native packing, quality run or held-out evaluation
occurs. Engine source, accurate READMEs and releases remain unchanged; H2/H5
remain open at 60% completed milestone weight.


**N4 direct-coordinate domain preparation, 2026-10-25:** [the original-geometry and rational audit](../benchmarks/results/h5-direct-coordinate-domains-20261025.md)
checks all 20 orientation/sheet regions around fixed core 0, representing all
twelve permitted orientation/reflection cases. New placements retain 0.22 mm
separation and 0.02 mm extra stock margin. Every inward-rounded halfspace and
all 3,884 source faces verify. Certified consolidation retains 3,703 nonempty
grid domains, including all source-face lineages, with 55,992 per-copy choices
for the full 12 brackets and 21 inserts. No solver has run and no complete
layout is claimed. Next encode and independently check the exact-count model,
using only certified containment removal if needed before its one declared
60-second solve. Both prior checkpoints are pushed as 8f941426; its CI is
pending and the older main run is cancelled. Engine source, accurate READMEs
and releases are unchanged. H2/H5 stay open at 60% completed milestone weight.


**N4 exact-count coordinate result, 2026-10-25:** [the complete model audit](../benchmarks/results/h5-direct-coordinate-selection-20261025.md)
certifies 26 domain-containment removals and preserves all 3,677 retained
domains. Every field of the 60,537-variable/306,319-constraint model verifies,
including exact original quantities and all 978 cross-part arm pairs. One
declared 60-second search reports INFEASIBLE for the restricted grid/domain
model with fixed core 0, finishing at 59.73 seconds with 60.354444 seconds
actual elapsed time. No layout is returned and no solve is repeated. This
does not prove the unrestricted continuous problem impossible or that the
fixed core must move. Next verify an outer coordinate relaxation covering
all original continuous placements before drawing any conditional negative
conclusion. Engine source, accurate READMEs and releases remain unchanged;
H2/H5 stay open at 60%, with all original counts and acceptance limits retained.


**N4 continuous-coverage outer result, 2026-10-25:** [the complete audit](../benchmarks/results/h5-outer-coordinate-relaxation-20261025.md)
checks 24 source regions, all twelve permitted orientation/reflection cases,
953 outward domains and all 14,734 known compatible core-0 poses. Exact rational
containment and rounding cover the full source regions, not just saved samples.
Every field of the 22,290-variable/128,377-constraint exact-count model verifies.
One bounded outer search reports INFEASIBLE in 13.950743 seconds. Within the
recorded geometry/coverage model this excludes the full inventory with core 0
unchanged; it does not exclude different frame/cog arrangements. A single
projected cog in saved core 5 yields a new arrangement passing all 438 original
pair and 132 stock-boundary screens, with the other 32 placements unchanged.
Next check its complete outer regions and exact-count feasibility before any
accepted-layout claim. Actual native qualification and all H5 requirements
remain. Source, accurate READMEs and releases are unchanged; H2/H5 stay open
at 60% completed milestone weight.


**N4 guarded alternative and unrestricted relaxation, 2026-10-25:**
[The evidence](../benchmarks/results/h5-guarded-core-and-global-relaxation-20261025.md) rebuilds and audits all 24
continuous regions around the guarded core-5 alternative: 864 outward domains,
18,724 coverage vertices and all 12,860 compatible saved small-part poses.
Its independently checked exact-count model reports INFEASIBLE in 9.923168
seconds, conditionally excluding that fixed arrangement. A new necessary
relaxation lets all 66 parts move and represents each freely rotating cog by
a polygon strictly inside its certified 109.1157 mm inscribed disk. Original
non-cog components, orientations, counts and target sheet domains remain.
Independent geometry and complete 31,467-variable/37,061-constraint encoding
audits pass. One 60-second call returns UNKNOWN in 60.152007 seconds with no
incumbent or proof; the preserved 64-part sanity check still lacks two brackets.
Both completed calls and the initial failed geometry preparation are retained.
Next investigate audited original-area bounds and global packing propagation;
do not retry unchanged calls or weaken acceptance. No full target witness,
native qualification, production-budget run or H5 matrix result is obtained.
Source, accurate READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 global packing propagation and compound proxies, 2026-10-25:**
[The evidence](../benchmarks/results/h5-global-propagation-and-compound-proxy-20261025.md) independently verifies original
filled-area bounds, outward sheet capacities and floor-safe inner rectangles
for every part. Adding two global NoOverlap2D and four cumulative constraints
to the all-movable polygon model yields 31,935 variables/37,849 constraints,
fully audited. One bounded call remains UNKNOWN in 60.188312 seconds. A distinct
smaller model replaces pairwise polygon disjunctions with five disjoint inner
rectangles per cog, preserving full original-area charges and all66 counts.
Its 1,806 variables/2,824 constraints also audit completely; one call remains
UNKNOWN in 60.176534 seconds. Neither search returns an incumbent or proof.
Both original64-part sanity checks pass the new conditions but still miss two
brackets. Next audit exact orientation aliases and source-derived, nonbinding
hints before considering a different bounded construction test. All original
limits, native checks and H5 matrix requirements remain. Source, accurate
READMEs and releases are unchanged; H2/H5 stay open at 60%.


**N4 exact orientation aliases and audited source hints, 2026-10-25:**
[The evidence](../benchmarks/results/h5-orientation-aliases-and-source-hints-20261025.md) checks exact representative and
inverse maps for all 28 original modes, retaining 22 representatives and all
16 original orientation/reflection classes. All bracket cases stay distinct.
The original 66-part layout passes 1,456 polygon-pair checks but exceeds the
target at the same seven recorded parts. Only 59 compatible poses supply
nonbinding hints; all 66 parts remain required and every position stays free.
Every field of the 1,686-variable/2,584-constraint model and all 1,482 hint values
verify independently. One bounded call returns UNKNOWN in 60.101281 seconds
without an incumbent or proof. A source census prepares a different finite
orientation-inventory construction, with two additional brackets mandatory;
no search of that inventory occurs yet. After all six previous main checks
passed, five checkpoints were pushed normally through 247e823a. Its new CI
40233299884 remains distinct from the completed previous run. Source, accurate
READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 source orientation inventory and exact proxy-slot coverage, 2026-10-25:**
[The evidence](../benchmarks/results/h5-source-inventory-and-proxy-slot-coverage-20261025.md) checks a finite source-derived
orientation inventory with all 66 parts mandatory and every position free.
Its 1,486-variable/2,178-constraint model and 1,406 nonbinding hint values audit
completely; one bounded call remains UNKNOWN in 60.111765 seconds. Separately,
all 16 missing-bracket mode domains around the fixed 64-part proxy layout are
covered exactly: 1,950 forbidden rectangles cover 266,545,630,376 integer
mode/anchor pairs, independently checked across 145,251 critical cells.
No extra bracket fits while those existing poses stay fixed, including at
touching boundaries. A complete single-part release census records all 64
parts and 33 frame/cog cases; released parts must be restored in any next
63-plus-3 construction. This is conditional evidence, not unrestricted
infeasibility or a full target witness. All original acceptance requirements
remain; source, accurate READMEs and releases are unchanged. H2/H5 stay open
at 60% completed milestone weight.


**N4 complete single-core relocation exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/h5-single-core-relocation-exclusion-20261025.md) covers all 33 recorded frame/cog
releases, with 63 source poses fixed and the released part plus two brackets
mandatory. All 576 queries and 3,462 integer free cells audit completely; 1,152
exact allocation inequalities exclude 28 cases. The other five cog cases have
an independently reconstructed 1,111-variable/2,118-constraint model, including
all 416 cell options and 120 component pairs. One bounded call returns
INFEASIBLE in 0.150878 seconds with no incumbent; no LRAT certificate is claimed.
All 66 original counts are retained. These 33 conditional neighborhoods are
closed; broader coordinated moves remain unresolved. No unrestricted
impossibility, target witness or H5 qualification is claimed. Source, accurate
READMEs and releases are unchanged; H2/H5 remain open at 60%.


**N4 complete pair relocation census and outline diagnosis, 2026-10-25:**
[The evidence](../benchmarks/results/h5-pair-core-relocation-and-outline-diagnosis-20261025.md) completes all 528 core-pair
releases and 9,984 mode queries. Independent coverage and 53,424 allocation
inequalities exclude 299 cases; all 229 survivors and 424 allocations enter
one fully audited 73,266-variable/141,477-constraint model. One bounded call
finds a complete 66-part proxy arrangement in 7.952451 seconds. Independent
reconstruction verifies all copies, 138 inner rectangles and 6,456 component
pairs. The original-outline lift fails seven pair and two stock checks. Two
certified-disk conflicts remain after every cog angle and full floor-center
uncertainty, rejecting those selected coordinates. Broader cells and
neighborhoods remain unresolved. Next strengthen necessary collision geometry
against actual fixed original outlines; no unchanged retry or acceptance
reduction. Source, accurate READMEs and releases stay unchanged. No original
target witness or H5 qualification; H2/H5 remain open at 60%.


**N4 original-outline collision regions, 2026-10-25:**
[The evidence](../benchmarks/results/h5-original-outline-collision-regions-20261025.md) verifies a stronger floor-safe
16-gon for all cog angles against the actual fixed original outlines. Exact
subset checks and an independent triangle oracle verify all 100 obstacle caches;
all 43 source poses and 2,000 compatible pairs remain valid. A mixed-dimensional
GEOS guard failure is preserved; 1,262 completed queries are reused unchanged
and only 1,388 unfinished queries resume within the original work budget.
All 2,650 queries finish. Independent outward covers account for every whole
prior cell: 42,226 cells including 3,081 points/lines. They reject three prior
false anchors and exclude another 22 cases, leaving 207 cases/286 allocations.
Next construct fully covered convex domains and a joint model using the stronger
cog polygon itself. No solver call, accepted target layout or H5 qualification
is claimed. Source, accurate READMEs and releases stay unchanged; H2/H5 remain
open at 60% completed milestone weight.


**N4 stronger two-core relocation exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/h5-strong-pair-relocation-exclusion-20261025.md) covers all 207 remaining cases
and 286 allocations with 32,626 convex domains, 165,640 outward halfplanes and
960,962 exact vertex tests. The empty-set guard failure is preserved; 40 completed
queries are reused unchanged within the original work budget. An exact support
atlas audits 324 convex Minkowski hulls and every relevant edge normal. The full
56,046-variable/356,662-constraint model uses the stronger cog 16-gon directly.
One bounded call returns INFEASIBLE in 20.878256 seconds with no incumbent or
LRAT certificate. Together with prior 299 area and 22 empty-role exclusions,
all 528 recorded two-core neighborhoods are closed, conditionally on the source
poses/inventory. A distinct conflict-owner census prepares 57 fixed plus nine
mandatory movable originals, preserving all 66 parts. All six existing main
checks now pass; accumulated commits are ready for the next normal push.
No unrestricted impossibility, accepted target or H5 qualification is claimed.
Source, accurate READMEs and releases stay unchanged; H2/H5 remain open at 60%.


**N4 complete conflict-owner neighborhood, 2026-10-25:**
[The evidence](../benchmarks/results/h5-conflict-owner-neighborhood-20261025.md) restores seven originals and both missing brackets with
57 source transforms fixed, retaining all 66 required parts. All 20 original-stock
queries complete with 199 convex domains; independent checks cover 3,638 outward
halfplanes, 82,650 rational vertex tests and 361 component Minkowski hulls.
The fully audited 1,871-variable/10,774-constraint model finds a necessary-model
arrangement in 1.133719 seconds. Its original-outline trial fails 17 clearance
checks and three stock bounds; all failures are preserved. Exact 109.1 mm whole
circles reject five selected cog conflicts, and a separately certified 139.2707 mm
all-angle stock support rejects three anchors while retaining all 15 valid source
cog centers. The hull support is not used as filled collision geometry. These
conditions prepare the next stronger model; no completed call is retried.
The previous six checkpoints are on main 51fe56c0; its new CI remains separate
from the prior successful run. No accepted target, native qualification or H5
completion is claimed. Source, accurate READMEs and releases stay unchanged;
H2/H5 remain open at 60% completed milestone weight.


**N4 stronger circles and full-original construction, 2026-10-25:**
[The evidence](../benchmarks/results/h5-circle-stock-neighborhood-20261025.md) strengthens the same 57-fixed/nine-moving neighborhood
with a certified 128-vertex cog proxy, exact circle separation for all 15 cog
pairs and the all-angle stock bounds. All 20 queries complete; 18 are reused
unchanged. Independent checks cover 274 domains, 4,204 outward halfplanes,
85,992 rational vertex tests and 361 exact component Minkowski hulls.
The fully audited 9,549-variable/22,313-constraint model returns UNKNOWN in
60.174056 seconds, with no incumbent; the completed call stays closed.
A distinct full-original preparation retains every cog tooth at its known source
angle, all bracket choices and 20 inward stock-grid queries. Its 57 starting
originals meet the 0.2 mm requested clearance, but nine pairs and four stock
margins fall below the current native conservative guards. These shortfalls
must be addressed and independently checked before that source is frozen for
an original-outline construction. No guard, material cap or count is reduced.
No accepted target or H5 qualification is claimed. Source, accurate READMEs and
releases stay unchanged; H2/H5 remain open at 60% completed milestone weight.


**N4 corrected source guards and original-outline regions, 2026-10-25:**
[The evidence](../benchmarks/results/h5-guarded-source-adjustment-20261025.md) corrects all nine pair and four stock-margin shortfalls
without changing original shapes, counts, orientations, sheets or the material
target. One audited 228-variable/695-constraint bounded adjustment finishes in
0.027011 seconds. Fifteen originals move by at most 0.023 mm per axis. Independent
checks cover all 1,246 original pairs and 228 stock edges; the minimum gap is
0.2125 mm and extra stock margin 0.0125 mm, both above unchanged native guards.
The baseline still contains only 57 originals; all nine others remain mandatory.
All 100 full-original collision obstacles and 20 free-region queries are rebuilt
and independently checked using 11,872 raw triangle hulls and 2,491 expanded
triangle hulls. Every cog tooth is preserved, with no outward region padding.
Next is a joint full-original nine-part model using this adjusted source.
No complete target, native full-job validation or H5 qualification is claimed.
Source, accurate READMEs and releases stay unchanged; H2/H5 remain open at 60%.


**N4 complete original-shape joint searches, 2026-10-25:**
[The evidence](../benchmarks/results/h5-full-original-joint-20261025.md) audits all 20 actual-original placement regions, 82 mutual
collision cases, 3,525 raw allowed faces and 512 forbidden pieces. All nine
moving originals remain mandatory alongside the adjusted 57-part source.
The full-original joint model returns UNKNOWN in 60.875060 seconds; a smaller
conservative moving-cog-hull model is conditionally INFEASIBLE in 8.862555 seconds.
A distinct original-shape constraint-generation experiment shares 60 seconds
across construction, audits and eight calls, ending UNKNOWN in 60.102165 seconds.
All seven relaxed 66-original proposals are independently reconstructed: 11,191
pair checks and 1,848 stock-edge checks preserve every failure. Fixed clearances
and stock margins pass; none passes moving-part collisions. The best recorded
overlap diagnosis still has seven overlapping pairs, so no native call is made.
All bounded searches stay closed. Next investigate certified whole-domain pair
exclusions or a structurally larger neighborhood, without relaxing counts,
material limits, clearance guards or H5. Source, accurate READMEs and releases
are unchanged; H2/H5 remain open at 60%.


**N4 whole-domain conflicts and three-cog exclusion, 2026-10-25:**
[The evidence](../benchmarks/results/h5-original-domain-conflicts-20261025.md) independently checks all 8,449,813 domain pairs and
5,453,534 original-shape collision exclusions. Lossless row grouping preserves
23,481,818 physical exclusions in 4,580 group constraints. A necessary-region
model finds a candidate in 8.094902 seconds; its complete original-coordinate
model is INFEASIBLE in 0.030771 seconds for that selected combination only.
The ordinary interval replay reaches a fixed point without proving a conflict.
A separate core diagnostic identifies three cog domains, then an independent
228-segment exact-rational no-fit disk certificate proves a broader three-region
exclusion. Groups containing 12/2/29 complete domains exclude 696 triples across
all six moving cogs, without changing any original count or material limit.
Next add that verified global occupancy clause before another declared search.
Four checkpoints are pushed normally to main 4f359ff7 after all six previous CI
jobs pass; new CI 40240715636 is tracked separately. No native acceptance,
quality run or new release is claimed. H2/H5 remain open at 60%.


**N4 complete convex conflicts and second-sheet capacity, 2026-10-25:**
[The evidence](../benchmarks/results/h5-convex-domain-conflicts-20261025.md) scans all 2,996,279 pairs left open by the box table and
independently verifies 108,041 additional whole-convex original-shape exclusions.
The complete table now has 5,561,575 exclusions, represented losslessly as
24,091,856 physical exclusions. A first three-region assignment is rejected by
a whole-convex bracket/cog collision. The refined master finds a necessary
assignment, but its full original-coordinate model is INFEASIBLE. Exact replay
then proves a second-sheet pair conflict independently of the solver core.
All 51 unresolved second-sheet pairs receive bounded exact interval checks:
32 conflicts are proved, 19 fixed points stay non-proofs, and all 1,920 events
are independently replayed. A separate original no-fit-disk argument proves
that at most two moving cogs fit the complete second-sheet region inventory.
The next master includes all 480 physical new pair clauses and this capacity;
its coordinate check still fails, having placed five cogs in one first-sheet
domain. Next derive independently certified regional occupancy limits across
all six copies. All original counts, material limits and native guards remain
unchanged; no complete target, native call, quality run or release is claimed.
Main CI40240715636 has 4/6 successful jobs and remains in_progress in the
saved snapshot. Accurate READMEs remain unchanged. H2/H5 remain open at 60%.


**N4 regional cog capacity and simultaneous anchors, 2026-10-25:**
[The evidence](../benchmarks/results/h5-cog-region-capacities-20261025.md) certifies 1,215 whole integer boxes and independently
checks every membership, cell diagonal and dominance witness. Thirty-five
retained bounds (30 capacity-one, five capacity-two) count all six cogs and
eliminate the prior five-in-one-region assignment. A first master/coordinate
pipeline finishes within 11.416324 seconds of a shared60-second allowance; its
selected original-coordinate model is INFEASIBLE. A second pipeline adds all
six simultaneous cog anchors and a certified strict inner32-gon of the original
collision disk, finishing in43.440899 seconds. Its necessary assignment still
has four actual original cog collisions, and the full selected-coordinate model
is INFEASIBLE. Next strengthen simultaneous geometry with the complete original
cog obstacle (61 pieces/2,720 edges), retaining all counts, guards and material
limits. Both bounded pipelines stay closed; no full target or native acceptance
is claimed. Main's new15-file scrap/offcut documentation change is merged as
da4ced0f, preserving all15 remote and73 local evidence files byte-exact. The older
CI was cancelled after five passes; new main CI40242602102 is independently
tracked. Production and accurate READMEs are unchanged. H2/H5 remain open at60%.


**N4 complete guarded cog model and original-outline core, 2026-10-25:**
[The evidence](../benchmarks/results/h5-full-cog-coordinates-20261025.md) independently reconstructs a52,790-variable/66,018-constraint
model with all original cog collision pieces and existing domain/occupancy limits.
Its single call returns UNKNOWN without an incumbent. Shared elapsed60.870843s
exceeds the declared60s by0.870843s; the solver soft-limit overshoot is also
preserved, with no budget-pass claim, retry or follow-up coordinate call.
All200,309 remaining cog-domain pairs receive complete guarded-region checks:
146 raw-table exclusions are independently verified;16 overlap earlier proofs,
so130 ordered pairs (1,950 physical clauses) are newly available to the master.
A separately prepared complete original-outline collision core has71 convex
pieces and352 necessarily rounded edges, reducing the direction upper bound
from39,540 to5,280 while retaining tooth geometry. Its full union, strict raw
containment and exact necessary rounding are independently audited. Next use
this smaller preliminary model with the new pair exclusions; every positive
still needs full guarded-original, native and H5 validation. Main CI40242602102
is independently tracked; source, accurate READMEs, releases and all acceptance
limits are unchanged. H2/H5 remain open at60%; no reserved vectors are evaluated.


**N4 original-core search and complete second-sheet cog pairs, 2026-10-25:**
[The evidence](../benchmarks/results/h5-original-core-search-20261025.md) preserves a full 18,530-variable / 34,068-constraint original-core
master UNKNOWN with no incumbent. Its single 45-second call takes 45.305899s;
the soft-limit overshoot is explicit, while shared 47.844358s stays within 60s.
No full-coordinate or native follow-up is opened. A separate bounded diagnostic
resolves all 15 remaining second-sheet pairs. Five have original-shape witnesses;
ten receive independent exact proofs covering 74 nodes / 540 events / 32 splits.
Together with prior certificates, all 1,024 pairs are classified:1,019 excluded,
five feasible. All 75 original pair and 40 stock-edge checks pass for those five
two-cog witnesses, but seven other moving originals are absent and still required.
The first geometry audit's metadata lookup failure is preserved alongside its
corrected read-back. The ten proofs provide 150 new physical pair clauses for
the next full 66-original search; verified coordinates may guide optional hints.
Production source, READMEs, material/native limits and releases are unchanged.
H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched. Main's own
CI40242602102 remains tracked before the next normal push.


**N4 guided full original-core search, 2026-10-25:** [the evidence](../benchmarks/results/h5-second-sheet-guided-search-20261025.md)
adds all 150 clauses from the ten proved second-sheet exclusions and 14 optional
values from a verified two-cog placement. The independent model audit covers
18,530 variables / 34,218 constraints, all hints and all 66 required originals;
no placement is fixed by a hint. The sole call finishes UNKNOWN without an
incumbent in 45.537740s; the 0.537740s soft-cap overshoot is preserved. Shared
47.986694s remains within 60s. No full-coordinate or native follow-up is opened.
Next investigate a different collision-free displacement-cell representation,
proving every retained cell safe against all original guarded inequalities
before use. That representation is not built yet. H2/H5 remain open at 60%;
production source, READMEs, releases, original counts, material target and guards
are unchanged. All 22 reserved H2 vectors remain untouched. Main CI40242602102
is still tracked before the next normal push.


**N4 exact guarded displacement cells, 2026-10-25:** [the evidence](../benchmarks/results/h5-cog-displacement-cells-20261025.md)
prepares 229 first-sheet and four second-sheet allowed relative-position cells.
It reconstructs all 122 bounded source-clause failure regions exactly, then
independently proves all 233 whole cells safe with 13,531 rational separating-axis
certificates and 831 inward halfplanes. All five known second-sheet witnesses
remain represented. The selected first-sheet simplification uses 0.005 mm
tolerance and 0.010 mm outward failure padding, an explicit stricter construction
restriction; negative results cannot exclude unrestricted packing. All nine
measured candidates, initial faces and discards remain preserved. At most 3,495
cell flags replace the earlier guarded model's 39,540 direction variables, but
no new solver model or runtime improvement is claimed yet. Next integrate these
proved cells with all 66 originals and unchanged material/native/H5 requirements.
Production source, READMEs and releases are unchanged. H2/H5 stay open at 60%;
all 22 reserved H2 vectors remain untouched. Main CI40242602102 is still tracked
before the next normal push.


**N4 guarded cell search and six-cog witness, 2026-10-25:** [the evidence](../benchmarks/results/h5-guarded-cell-search-20261025.md)
preserves a full 16,775-variable / 46,383-constraint guarded master UNKNOWN,
without an incumbent. Shared 48.579203s is within 60s; the 45-second soft-cap
overshoot is retained. A distinct four-cog first-sheet diagnostic succeeds in
7.753828s (shared 8.201210s), with every domain, bound, cell and full original
guarded clause independently verified. Combined with the known second-sheet
pair, all 63 currently placed originals pass 1,467 pair and 252 stock-edge checks.
Two brackets 28/29 and insert 50 are explicitly missing, so no full target/native
pass is claimed. A complete declared finite sample regenerates 162,863 points;
103,028 exact rejection certificates leave zero bracket and eight insert poses.
This does not prove continuous impossibility. Next keep all six cogs movable,
use their verified positions only as hints, and add 9,204 exact selected-domain
box bounds to the full model. All 66 parts, material/native limits and H5 gates
remain required. Production source, READMEs and releases are unchanged; H2/H5
remain open at 60%, with 22 reserved H2 vectors untouched. Main CI40242602102
is tracked before normal push.


**N4 guided search and exact selected-domain rejection, 2026-10-25:** [the evidence](../benchmarks/results/h5-six-cog-guided-search-20261025.md)
records a candidate from the 16,775-variable / 55,587-constraint master in
11.009201s after adding 9,204 exact domain bounds and 79 advisory hints. All 66
originals remain mandatory (nine movable, 57 fixed). The full selected-coordinate
follow-up is INFEASIBLE in 0.225323s; total pipeline time is 15.872994s within 60s.
Nineteen interval traces reach fixed points, not feasibility. A separate exact
clause tree then certifies this selected combination's rejection: 1,316 nodes,
415 complete branches, 901 contradictory leaves and 4,851 independently replayed
events, with no open leaves. Its 56.946915s proof budget is separate from the
closed solver pipeline. Other domain combinations and unrestricted packing
remain open. The early read-back failure and separate completed audit are
preserved. Next integrate the bracket/insert coordinates with the guarded cog
search using independently proved compact representations for the remaining
original profile pairs. No target/native or production pass is claimed. All
six jobs of main CI 40242602102 now pass; checkpoints can be pushed normally
after preserving any newer remote work. Production, READMEs and releases are
unchanged. H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched.


**N4 complete guarded coordinates and table projection, 2026-10-25:** [the evidence](../benchmarks/results/h5-all-original-cell-search-20261025.md)
adds all 162 remaining query-pair representations for 364 physical pair/mode
uses. Their 6,174 cells and 19,329 inward planes pass 38,211 exact separation
certificates; all 29 stricter simplifications and 11 inset/grid discards remain
explicit. The full 35,469-variable / 181,700-constraint model now includes all
nine moving originals and every one of their 36 direct guarded pair relations,
with all 66 original counts required. Its single 45-second-cap call returns
UNKNOWN in 52.627968s: the 7.627968s soft overrun is retained, while total
57.609353s stays inside the shared 60s budget. No layout/native pass is claimed.
A separately audited projection removes only the obsolete 1,572,932-literal
table and 3,395 private variables, preserving every direct geometry/count/area
constraint. All 32,074 remaining variables and 173,814 constraints inverse-map
exactly to the parent; actual solver import/export passes. That projection has
not been solved. Next use a distinct bounded call with a 10s shutdown reserve;
offline preparation is not production qualification. The prior ten checkpoints
are pushed to main 728b2db2; its own CI 40246226212 remains tracked before the
next normal push. Production, READMEs and releases are unchanged. H2/H5 remain
open at 60%, with all 22 reserved H2 vectors untouched.


**N4 direct-model negative and complete integer outer cover, 2026-10-26:** [the evidence](../benchmarks/results/h5-direct-original-search-20261025.md)
records the distinct 32,074-variable / 173,814-constraint full-coordinate model
INFEASIBLE in 42.634289s, shared 44.271944s, within its 45s cap and 60s budget
with a 10s shutdown reserve. This rejects only the fixed-57/source-angle/inward-
domain construction with stricter pair cells, not unrestricted packing. A new
necessary outer cover retains every integer displacement satisfying the original
guarded pair rules: all 164 cases / 394 physical uses, 16,210 complete slabs,
22,063 proved-invalid rectangles and 9,129 retained boxes. Independent rational
partition checks and 6,485,956 exact corner inequalities pass. Retained boxes
are not safe placements. No outer-cover model or solver has run; next replace
all stricter pair-cell constraints and audit the complete transformation before
a distinct bounded diagnostic. All originals, material/native limits and H5
production requirements remain unchanged. The provenance-lookup failure and
separate corrected audit are preserved. Main 728b2db2's own CI 40246226212 is
still tracked before pushing local checkpoints. Production, READMEs and releases
are unchanged; H2/H5 remain open at 60%, with all 22 reserved H2 vectors untouched.


**N4 complete source-clause search and rejected relaxation, 2026-10-26:** [the evidence](../benchmarks/results/h5-bounded-source-search-20261026.md)
verifies complete replacement of all strict safe cells, including 54 empty-cell
sums, by the necessary integer outer cover. Its sole call finds a candidate in
16.162402s, shared 18.195138s; independent full-source and 66-original geometry
readback rejects six moving-pair failures, including four overlaps. All 90
cutouts, original copies/areas, 1,540 same-sheet pairs and 264 stock edges are
checked. The initial false no-cutouts assertion and separate repair are retained.
A distinct complete source-clause model replaces all outer boxes, retains every
original domain/count/area/capacity rule and applies only exact rectangle-bound
simplifications. Its 167,044 variables/376,363 constraints and all 394 pair modes
pass independent reconstruction, 218,048 exact corner evaluations and actual
solver import/export. One 45s-cap call ends UNKNOWN in 45.471545s, shared 48.583887s;
the 0.471545s soft-cap overrun is preserved, the shared 60s budget holds, and no
feasibility/impossibility or native qualification is claimed. Both calls remain
closed. Next test whole-domain completion against the verified six-cog positions
with replayable exact certificates; the previous finite pose census is not a
continuous proof. Any exclusion must remain conditional on fixed witness poses.
H2/H5 stay open at 60%; production, READMEs, releases and 22 reserved H2 vectors
remain unchanged. Main 728b2db2's existing CI is allowed to finish before pushing.


**N4 exact completion obstruction and single-cog release census, 2026-10-26:** [the evidence](../benchmarks/results/h5-fixed-six-completion-20261026.md)
proves that the verified six fixed cog poses leave none of the 2,418 original
bracket domains continuously feasible; the insert retains one domain with 89
fragments. All 2,756 domains and 1,136 exact clipping events pass independent
replay, including boundaries and 5,816,904 integer corner checks. Six distinct
single-cog releases cover all 14,508 bracket domains in 13.630690s, with no
pending cases. Releasing cogs 54 or 62 leaves no bracket space. Releasing cog
58 opens individual regions, but all 196 exact ordered region-pair differences
are empty: at most one bracket fits, while two are required. Cogs 57, 64 and 65
remain the useful single-position releases to investigate in focused four-mover,
62-fixed-original models. All 66 parts and original/native/material requirements
remain mandatory. These are conditional source-pose/domain proofs, not general
packing impossibility or H5 qualification. No solver/native/quality call occurs.
The provenance lookup failure and zero-counter aggregation failure are preserved;
completed proof work is reused without reruns. Three prior checkpoints were
normally pushed to verified main 822a5f67 after all six prior CI jobs passed;
new CI 40248595273 is tracked. H2/H5 remain open at 60%; production, READMEs,
releases and all 22 reserved H2 vectors remain unchanged.


**N4 single-cog obstruction completed, 2026-10-26:** [the exact proof](../benchmarks/results/h5-single-cog-obstruction-20261026.md)
examines all 3,315 insert/released-cog domain cases for original cogs 57, 64
and 65 and independently excludes all 2,362 bracket/cog fragment pairs.
All boundaries and original source pair directions are retained. Combined
with the prior proofs for 54, 58 and 62, no single-cog-position change can
complete this layout within the recorded source angles/domains and fixed
57 poses. The empty focused models are not sent to a solver. Next widen to
at least two cog positions (five mandatory movers, 61 fixed originals), or
another fixed pose/orientation/domain inventory; never apply these conditional
exclusions when their fixed poses move. This is not unrestricted impossibility
or H5 qualification. No solver/native/quality call occurs. Full original/native
material evidence, production integration and the full matrix remain required.
H2/H5 remain open at 60%; original gate limits, production, READMEs, releases
and all 22 reserved H2 vectors remain unchanged. Main CI 40248595273 is tracked
before the next normal push.


**N4 two-cog focused source search, 2026-10-26:** [the retained result](../benchmarks/results/h5-two-cog-source-focus-20261026.md)
releases original cogs 64/65, preserving both brackets, insert and every original
part (five movers, 61 fixed). All 3,523 original domain cases finish exact clipping
and independent replay; 173 domains/261 fragments remain. Both brackets and
released cogs must use the second sheet in these source conditions. The full
parent model is preserved exactly, with eight fixed-coordinate equalities and
6,364 independently verified empty-domain exclusions appended. One bounded
call returns INFEASIBLE in 5.966434s, 9.166805s total; actual model/parameters and
terminal state pass readback. This conditional solver negative is not an
independent unrestricted geometry proof, and the call is closed. Next examine
first-sheet cogs 57/58 with new regions and correct pair ordering. No previous
conditional obstruction may be transferred. The pre-search prose-substitution
failure and recovery are preserved; no solver repeated. Production integration,
full original/native target and complete H5 matrix remain required. H2/H5 stay
open at 60%; original limits, production, READMEs, releases and 22 reserved H2
vectors are unchanged. Main CI 40248595273 is tracked before the next normal push.


**N4 first-sheet neighborhoods and area capacities, 2026-10-26:** [the evidence](../benchmarks/results/h5-first-sheet-cog-neighborhoods-20261026.md)
retains three distinct original-part searches: cogs 57/58 and 57/58/62 return
INFEASIBLE; all four first-sheet cogs return UNKNOWN. Every region and focused
model is independently audited, with all 66 originals retained. The UNKNOWN
call's 0.682462s soft-limit overrun is preserved; total time is 48.884638s within
the shared 60 seconds. All calls are closed. Separate exact area proofs yield
14 necessary source-region inequalities, independent of cog witness poses,
excluding 28 of 42 all-nine sheet allocations. Two brackets plus two cogs
cannot share sheet 2 in these source domains (180,124 versus 174,476 mm²);
the seven-part first-sheet case remains unresolved. Next add the verified
inequalities to the full nine-mover source model, with no focused witness locks
or exclusions. Original/native target, production integration and the complete
H5 matrix remain required. All six prior main checks pass; the queued batch is
ready for a normal push. H2/H5 remain open at 60%; original limits, production,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.


**N4 source area propagation and shared directions, 2026-10-26:** [the evidence](../benchmarks/results/h5-source-area-and-direction-sharing-20261026.md)
retains two closed full nine-mover searches, both UNKNOWN. Fourteen verified
area rules exclude nine allocations beyond the original global-area bounds.
An independently verified equivalent representation shares exact direction
predicates across modes, removing 55,334 variables and 110,668 constraints;
all 66 originals, 394 source pair modes and original guards remain required.
The calls finish in 49.698399s and 51.313156s within their shared 60 seconds;
their 1.532948s/3.508436s soft solver overruns are preserved. Neither result
proves impossibility or supplies a native-valid target. Next independently
verify whether complement clauses can be removed under an exact existential
assignment proof before any distinct bounded call. All earlier calls remain
closed. Prior checkpoints are on main 68c82ae1; five CI jobs pass and Windows
checks are still running at the retained snapshot. Production, READMEs,
releases and the 22 reserved H2 vectors remain unchanged. H2/H5 stay open at 60%.


**N4 one-sided directions and restored conflicts, 2026-10-26:** [the evidence](../benchmarks/results/h5-one-sided-conflict-propagation-20261026.md)
retains two closed UNKNOWN calls. Exact monotone completion permits removal
of 101,455 complement clauses. A second model restores all 5,561,575 proven
domain conflicts across all families, adding only 3,395 auxiliaries and 7,886
constraints. Complete model and bit-matrix audits pass. Both total budgets
pass at 47.741708s/48.140666s; soft overruns of 0.486188s/0.358075s remain recorded.
No target layout or impossibility proof is obtained. A visually inspected
63-original partial identifies adjacent fixed cogs 53/56/61 for a broader
12-mover/54-fixed geometry investigation. Its domains, area bounds and capacities
must be recomputed; prior fixed57 restrictions cannot be carried over. All
earlier calls remain closed. All six checks on main 68c82ae1 now pass, allowing
the queued checkpoints to be pushed normally. H2/H5 remain open at 60%; source,
READMEs, releases and the 22 reserved H2 vectors remain unchanged.


**N4 expanded cog neighborhood, 2026-10-26:** [the evidence](../benchmarks/results/h5-expanded-cog-neighborhood-20261026.md)
releases original cogs 53/56/61 for a fresh 12-mover/54-fixed construction,
retaining all 66 required originals and native guards. All 20 recomputed free
regions and 3,716 inward domains pass independent checks; no old fixed57
conditional restrictions are imported. Cog 53's original constructive-anchor
exclusion is preserved. A complete 729-triple local grid census yields 54 valid
partial repairs; the selected shifts pass all 1,467 original pair and 252 stock
checks. All nine partial cog anchors are represented in the new domains, while
brackets 28/29 and insert 50 remain missing and mandatory. The fresh geometry
covers 66 physical pairs/538 query-pair modes. Next build and audit the complete
12-part coordinate model; no solver or native call occurred here. Prior
checkpoints are on main d1645404, whose CI is running with four jobs passed at
the retained snapshot. H2/H5 stay open at 60%; production, READMEs, releases and
the 22 reserved H2 vectors remain unchanged.


**N4 expanded full-source search, 2026-10-26:** [the evidence](../benchmarks/results/h5-expanded-source-search-20261026.md)
independently verifies the complete 12-mover/54-fixed model: all 66 originals,
214,901 variables, 281,731 constraints, 538 full source pair modes, two exact
area rules and a fresh second-sheet cog capacity of two. Its one call reaches
the hard shared deadline without a saved solver response or candidate, returning
after 60.029781 seconds. The 0.029781-second outer overrun and the ordinary
readback auditor's missing-result failure are preserved; a separate timeout
audit verifies closure without assigning UNKNOWN/INFEASIBLE or claiming native
acceptance. No retry is permitted. A census identifies 16,082 exact pair/normal
projection groups that could remove 495,561 repeated matrix terms; this needs
a separate whole-model audit before another distinct bounded call. The expanded
geometry checkpoint d85f2b2a is on main after all six prior checks passed; its
own CI has four jobs passed at 02:31 UTC. H2/H5 remain open at 60%; production,
READMEs, releases and all 22 reserved H2 vectors remain unchanged.


**N4 projected models and fresh conflicts, 2026-10-26:** [the evidence](../benchmarks/results/h5-projected-source-and-fresh-conflicts-20261026.md)
verifies exact signed projections for all 201,575 source direction definitions,
removing 534,782 repeated terms, and a separate exact unary truth-channel encoding.
Both full 12-mover/54-fixed models preserve all 66 required originals and pass
independent equivalence/import audits. Their separate calls return UNKNOWN in
48.289739 and 48.865027 shared seconds; no candidate is saved and both calls are
closed. Solver soft-limit overshoots remain recorded. A fresh complete census
checks 9,437,545 domain pairs and independently proves 3,948,295 raw-original
collision exclusions. Exact row grouping preserves 25,189,075 physical uses,
ready for independently audited integration into a complete source model.
No old fixed57 table is transferred and no unmarked pair is called feasible.
At 02:49 UTC main d85f2b2a has five CI jobs passed with Windows checks running;
queued evidence awaits terminal CI before a normal push. H2/H5 remain open at
60%; product source, READMEs, releases and the 22 reserved H2 vectors are unchanged.


**N4 domain selection and three-part certificate, 2026-10-26:** [the evidence](../benchmarks/results/h5-domain-selection-and-triple-certificate-20261026.md)
retains a closed full-source UNKNOWN and refines 27,798 additional raw collision
exclusions. A verified necessary master selects domains, but its exact-coordinate
subproblem is INFEASIBLE for that tuple only. All 46 pair subproblems have checked
source witnesses; the complete bounded 120-triple census gives 87 checked
witnesses, 32 UNKNOWN and one conditional negative. Independently of solver
status, exact-rational original geometry proves that insert 50 in query16/row0
permits at most one of the nine cogs in query18/row3, covering all 36 copy pairs.
Next add and audit this single conditional-capacity rule in the necessary master;
all 169 calls here remain closed. The initial readback helper failure and repaired
audit are preserved, as are all soft-limit overruns; all outer budgets pass.
No full target/native/production qualification is claimed. All six checks on main
6a27fec0 pass, permitting a normal push. H2/H5 remain open at 60%; production,
READMEs, releases and the 22 reserved H2 vectors are unchanged.


**N4 conditional selection and original 64-part partial, 2026-10-26:** [the evidence](../benchmarks/results/h5-conditional-selection-and-partial64-20261026.md)
adds and independently audits the raw three-part capacity in the necessary master.
Its new selection moves only the insert; exact coordinates remain INFEASIBLE for
that tuple. Only the 45 changed pair/triple subsets are called: 43 witnesses and
two UNKNOWN. Four larger groups isolate the bracket region and provide an
insert/seven-cog witness. Independent reconstruction verifies a 64-original partial
with 84 cutouts / 9,294 vertices, 1,521 pair and 256 stock-edge checks; brackets 28/29 remain
missing. A new full 66-required model frees both brackets across 16 queries / 2,548 domains
each while keeping ten non-bracket domains and 60 nonbinding partial hints. Its
single call is INFEASIBLE in 27.443101 shared seconds, scoped only to that condition.
Next reopen the two bottom-strip cog domains and audit the broader source model.
All 52 calls stay closed; all shared budgets pass and soft overruns remain recorded.
Main b8535505 CI has four jobs passed at 03:46 UTC; preserve it before a normal push.
H2/H5 stay open at 60%; production, READMEs, releases and 22 reserved vectors are unchanged.


**N4 focused original-geometry obstruction, 2026-10-26:** [the evidence](../benchmarks/results/h5-focused-partial-obstruction-20261026.md)
retains the broader 54-fixed call as UNKNOWN in 47.721778 shared seconds,
including its 0.423204-second solver soft overrun. A fresh 62-fixed construction
is excluded by exact original-geometry checks: both mandatory cogs must occupy
two separate pockets, and every available bracket position collides with the
left cog. A separate rebuild frees middle cog61, giving five mandatory movers
and 61 fixed originals. All geometry, 2,118 inward domains and the complete
22,545-variable/39,619-constraint model pass independent checks; its one call is
INFEASIBLE in 18.006190 shared seconds. These are conditional results, not an
unrestricted impossibility claim. Both calls are closed and failures retained.
Next also release upper-right bracket27/cog58 and rebuild the 59-fixed geometry.
Main679e97e0 is pushed after all six prior checks passed; its own CI40267513191
is live. H2/H5 remain open at 60%; source, READMEs, releases and the 22 reserved
vectors are unchanged. No complete target layout or new release is qualified.


**N4 seven-part obstruction and broader source, 2026-10-26:** [the evidence](../benchmarks/results/h5-seven-part-obstruction-and-broader-source-20261026.md)
retains the full 59-fixed/seven-mover call as UNKNOWN (47.245034 shared seconds,
0.719084-second solver soft overrun). A new independently reconstructed census
checks all 3,644,823 domain pairs and certifies 2,369,711 raw-original conflicts.
Lossless grouping and verified family ordering yield a necessary master, which
is INFEASIBLE in 2.518526 shared seconds. The complete implication audit excludes
that finite source arrangement; it does not claim unrestricted impossibility.
Both calls stay closed. A distinct broader construction now fixes 53 originals
and moves 13, including all nine previously moving cogs and the insert. Its
geometry, 3,599 inward domains, 78-pair/954-mode inventory, physical-region
broadening and freshly derived second-sheet capacity pass independent checks.
No broader-source solver call is opened yet. Next rebuild its conflict tables
and necessary master; no old conditional exclusions transfer. Main679e97e0 has
four checks passed and two live; fec3cd72 is queued. H2/H5 remain open at 60%,
with production, READMEs, releases and all 22 reserved vectors unchanged.
