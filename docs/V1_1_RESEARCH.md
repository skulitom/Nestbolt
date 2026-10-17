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
