# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: lightburn.spec.ts >> LightBurn leads download separate cutting files and preserve the editable group
- Location: tests\lightburn.spec.ts:8:1

# Error details

```
Error: expect(locator).toHaveCount(expected) failed

Locator:  locator('.error')
Expected: 0
Received: 2
Timeout:  5000ms

Call log:
  - Expect "toHaveCount" locator('.error') with timeout 5000ms
  - waiting for locator('.error')
    14 × locator resolved to 2 elements
       - unexpected value "2"

```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - heading "Nestbolt" [level=1] [ref=e5]
    - textbox "Project name" [ref=e6]: lead-group
    - button "Save" [ref=e7] [cursor=pointer]
    - combobox "Open saved project" [ref=e8]:
      - option "Open saved…" [selected]
    - button "Delete" [disabled] [ref=e9]
    - button "Project ZIP" [ref=e10] [cursor=pointer]
    - button "Open ZIP" [ref=e11] [cursor=pointer]
    - button "New" [ref=e12] [cursor=pointer]
  - paragraph [ref=e13]: Free, open-source nesting for laser, CNC and other sheet cutting. Everything runs in this browser; files are never uploaded.
  - main [ref=e14]:
    - complementary [ref=e15]:
      - region [ref=e16]:
        - heading "Parts" [level=2] [ref=e17]
        - generic [ref=e18] [cursor=pointer]:
          - button "Import SVG, DXF or LightBurn (or drop files here)" [ref=e19]
          - text: Import SVG, DXF or LightBurn (or drop files here)
        - group [ref=e20]:
          - generic "LightBurn layers — preserved" [ref=e21] [cursor=pointer]
          - paragraph [ref=e22]: Groups stay together. Preview shows the space each unit occupies; exported projects retain editable artwork and settings.
          - table [ref=e23]:
            - rowgroup [ref=e24]:
              - row [ref=e25]:
                - columnheader "Layer" [ref=e26]
                - columnheader "Mode" [ref=e27]
                - columnheader "Output" [ref=e28]
                - columnheader "Kerf (mm)" [ref=e29]
            - rowgroup [ref=e30]:
              - row [ref=e31]:
                - 'cell "Layer 0: CUT" [ref=e32]'
                - cell "Cut" [ref=e33]
                - cell "On" [ref=e34]
                - cell "0.2" [ref=e35]
              - row [ref=e36]:
                - 'cell "Layer 1: ENGRAVE" [ref=e37]'
                - cell "Scan" [ref=e38]
                - cell "On" [ref=e39]
                - cell "0" [ref=e40]
              - row [ref=e41]:
                - cell "Layer 30" [ref=e42]
                - cell "Tool" [ref=e43]
                - cell "On" [ref=e44]
                - cell "0" [ref=e45]
          - generic [ref=e46]:
            - checkbox "Include sheet outline on T1" [checked] [ref=e47]
            - text: Include sheet outline on T1
        - list [ref=e48]:
          - listitem [ref=e49]: 1 top-level Tool/output-off shapes stay at their original positions in every exported sheet
          - listitem [ref=e50]: LightBurn layer kerf values are preserved and reported; spacing is not changed automatically
        - table [ref=e51]:
          - rowgroup [ref=e52]:
            - row [ref=e53]:
              - columnheader [ref=e54]
              - columnheader "Part" [ref=e55]
              - columnheader "Qty" [ref=e56]
              - columnheader "Rotation" [ref=e57]
              - columnheader "Mirror" [ref=e58]
              - columnheader [ref=e59]
          - rowgroup [ref=e60]:
            - row [ref=e61]:
              - cell [ref=e62]
              - cell "unit-1 (lead-group-unit-1) 13.1 cm²" [ref=e65]:
                - text: unit-1 (lead-group-unit-1)
                - generic [ref=e66]: 13.1 cm²
              - cell [ref=e67]:
                - spinbutton "Quantity of lead-group-unit-1" [ref=e68]: "2"
              - cell "0/90/180/270°" [ref=e69]:
                - combobox "Rotations of lead-group-unit-1" [ref=e70]:
                  - option "0/90/180/270°" [selected]
                  - option "0/180° (grain)"
                  - option "Fixed 0°"
                  - option "Every 15°"
                  - option "Free"
              - cell [ref=e71]:
                - checkbox "Allow mirroring lead-group-unit-1" [ref=e72]
              - cell [ref=e73]:
                - button "Remove lead-group-unit-1" [ref=e74] [cursor=pointer]: ×
      - region [ref=e75]:
        - heading "Sheets" [level=2] [ref=e76]
        - group "Sheet size 1" [ref=e77]:
          - generic [ref=e79]:
            - text: Width
            - spinbutton "Width mm" [ref=e80]: "150"
            - text: mm
          - generic [ref=e81]:
            - text: Height
            - spinbutton "Height mm" [ref=e82]: "100"
            - text: mm
          - generic [ref=e83]:
            - text: Count
            - spinbutton "Count" [ref=e84]
          - generic [ref=e85]:
            - text: Margin
            - spinbutton "Margin mm" [ref=e86]: "0"
            - text: mm
          - generic [ref=e87]:
            - text: Remnant outline
            - button "Remnant outline for sheet size 1" [ref=e88]
          - group [ref=e89]:
            - generic "Defects (0)" [ref=e90]
        - combobox "Add a sheet size" [ref=e91]:
          - option "Add sheet size…" [selected]
          - option "Diode laser 300×200"
          - option "CO2 bed 600×400"
          - option "Plywood 1220×2440"
          - option "Sheet metal 1250×2500"
          - option "Sheet metal 1500×3000"
          - option "Fabric roll 1500 × 10 m"
      - region [ref=e92]:
        - heading "Settings" [level=2] [ref=e93]
        - generic [ref=e94]:
          - generic [ref=e95]:
            - text: Part spacing
            - spinbutton "Part spacing mm" [ref=e96]: "0.2"
            - text: mm
          - generic [ref=e97]:
            - text: Edge spacing
            - spinbutton "Edge spacing mm" [ref=e98]: "1"
            - text: mm
          - generic [ref=e99]:
            - text: Goal
            - combobox "Goal" [ref=e100]:
              - option "Place every part" [selected]
              - option "Fill the sheets (most area)"
              - option "Fill by priority"
          - generic [ref=e101]:
            - text: Time
            - spinbutton "Time s" [ref=e102]: "1"
            - text: s
        - generic [ref=e103]:
          - checkbox "Common-line cutting" [disabled] [ref=e104]
          - text: Common-line cutting
        - paragraph [ref=e105]: For common-line cutting, export the cut outlines from LightBurn as SVG or DXF and import them here.
        - generic [ref=e106]:
          - checkbox "Lead-in allowances" [checked] [ref=e107]
          - text: Lead-in allowances
        - generic [ref=e108]:
          - generic [ref=e109]:
            - text: Lead kerf
            - spinbutton "Lead kerf mm" [ref=e110]: "0.2"
            - text: mm
          - generic [ref=e111]:
            - text: Lead length
            - spinbutton "Lead length mm" [ref=e112]: "3"
            - text: mm
          - generic [ref=e113]:
            - text: Lead style
            - combobox "Lead style" [ref=e114]:
              - option "Line" [selected]
              - option "Arc"
          - generic [ref=e115]:
            - text: Outer lead angle
            - spinbutton "Outer lead angle °" [ref=e116]: "45"
            - text: °
          - generic [ref=e117]:
            - text: Hole lead angle
            - spinbutton "Hole lead angle °" [ref=e118]: "90"
            - text: °
        - paragraph [ref=e119]: Enter the measured kerf. Length is the distance along the lead, including an arc. Space is reserved for both cutting directions. Small holes may need a shorter lead or a manual start.
        - paragraph [ref=e120]: In LightBurn, turn off Choose best starting point and LEADIN layer output. Use the reported length and style; outer angles are positive, hole angles negative. Keep lead-out and overcut off.
        - paragraph [ref=e121]: Download the cutting SVG or DXF for the new starts and lead review paths. The LightBurn file preserves the editable project with its original starts and settings. Cutting files contain cut paths only; keep the project for engraving and images. Open cuts need a manual start.
        - group [ref=e122]:
          - generic "Advanced" [ref=e123] [cursor=pointer]
          - generic [ref=e124]:
            - generic "Jobs of more than 1000 parts use at most two workers, to limit memory" [ref=e125]:
              - text: Workers
              - spinbutton "Workers" [ref=e126]: "1"
            - generic [ref=e127]:
              - text: Seed
              - spinbutton "Seed" [ref=e128]: "0"
            - generic [ref=e129]:
              - checkbox "Repeatable" [ref=e130]
              - text: Repeatable
      - button "Nest" [ref=e132] [cursor=pointer]
    - region [ref=e133]:
      - heading "Result" [level=2] [ref=e134]
      - generic [ref=e135]:
        - generic [ref=e136]:
          - term [ref=e137]: Sheets
          - definition [ref=e138]: "1"
        - generic [ref=e139]:
          - term [ref=e140]: Material
          - definition [ref=e141]: "0.343"
        - generic [ref=e142]:
          - term [ref=e143]: Utilisation
          - definition [ref=e144]: 50.9%
        - generic [ref=e145]:
          - term [ref=e146]: Placed
          - definition [ref=e147]: 2/2
        - generic [ref=e148]:
          - term [ref=e149]: Check
          - definition [ref=e150]: valid
      - region "Lead allowance details" [ref=e151]:
        - heading "Lead allowances" [level=3] [ref=e152]
        - paragraph [ref=e153]: 8/10 contours have checked space. 2 need manual attention.
        - paragraph [ref=e154]: "lead-group-unit-1 #1, contour 5: Open cutting contour has no enclosed waste side; its original path is exported without a lead or start change Disable the native lead for this contour or change its start manually."
        - paragraph [ref=e155]: "lead-group-unit-1 #2, contour 5: Open cutting contour has no enclosed waste side; its original path is exported without a lead or start change Disable the native lead for this contour or change its start manually."
        - paragraph [ref=e156]: LEADIN is a red review layer. Assign separate cut settings to contours with different angles or shortened lengths before enabling LightBurn’s own leads.
      - button "Download all sheets (ZIP)" [ref=e157] [cursor=pointer]
      - figure "sheet-0 offcut 150 × 67 mm LightBurn Cutting SVG Cutting DXF" [ref=e159]:
        - img "Layout of sheet-0" [ref=e160]:
          - generic "Offcut 150 × 67 mm" [ref=e162]
          - 'generic "lead-group-unit-1 #1" [ref=e163]'
          - 'generic "lead-group-unit-1 #2" [ref=e164]'
          - 'generic "lead-group-unit-1 #1, contour 1: 3.0 mm lead" [ref=e165]'
          - 'generic "lead-group-unit-1 #1, contour 2: 3.0 mm lead"'
          - 'generic "lead-group-unit-1 #1, contour 3: 3.0 mm lead" [ref=e166]'
          - 'generic "lead-group-unit-1 #1, contour 4: 3.0 mm lead" [ref=e167]'
          - 'generic "lead-group-unit-1 #2, contour 1: 3.0 mm lead" [ref=e168]'
          - 'generic "lead-group-unit-1 #2, contour 2: 3.0 mm lead"'
          - 'generic "lead-group-unit-1 #2, contour 3: 3.0 mm lead" [ref=e169]'
          - 'generic "lead-group-unit-1 #2, contour 4: 3.0 mm lead" [ref=e170]'
          - generic "Bounding box of the placed parts" [ref=e171]
        - generic [ref=e172]:
          - text: sheet-0
          - generic "Clear material above the placed parts" [ref=e173]: offcut 150 × 67 mm
          - button "LightBurn" [ref=e174] [cursor=pointer]
          - button "Cutting SVG" [ref=e175] [cursor=pointer]
          - button "Cutting DXF" [ref=e176] [cursor=pointer]
  - contentinfo [ref=e177]:
    - text: Built on
    - link "jagua-rs" [ref=e178] [cursor=pointer]:
      - /url: https://github.com/JeroenGar/jagua-rs
    - text: and
    - link "sparrow" [ref=e179] [cursor=pointer]:
      - /url: https://github.com/JeroenGar/sparrow
    - text: by Jeroen Gardeyn et al. MIT licensed;
    - link "third-party notices" [ref=e180] [cursor=pointer]:
      - /url: ./THIRD_PARTY_NOTICES.txt
    - text: .
    - link "Benchmark results" [ref=e181] [cursor=pointer]:
      - /url: ./results/
    - text: against Deepnest, SVGnest and Sparrow.
```

# Test source

```ts
  1   | import { expect, test } from '@playwright/test';
  2   | import { readFileSync } from 'node:fs';
  3   | import { fileURLToPath } from 'node:url';
  4   | 
  5   | const fixture = fileURLToPath(new URL('../../crates/core/tests/fixtures/roundtrip.lbrn2', import.meta.url));
  6   | const source = readFileSync(fixture, 'utf8');
  7   | 
  8   | test('LightBurn leads download separate cutting files and preserve the editable group', async ({ page }, info) => {
  9   |   const fixture = fileURLToPath(new URL('../../crates/core/tests/fixtures/lead-group.lbrn2', import.meta.url));
  10  |   const original = readFileSync(fixture,'utf8');
  11  |   await page.goto('/');
  12  |   await page.locator('.drop input[type=file]').setInputFiles(fixture);
  13  |   await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  14  |   await page.getByLabel('Quantity of lead-group-unit-1').fill('2');
  15  |   const sheet = page.locator('fieldset.sheet-row').first();
  16  |   await sheet.getByLabel('Width').fill('150');
  17  |   await sheet.getByLabel('Height').fill('100');
  18  |   await sheet.getByLabel('Margin').fill('0');
  19  |   await page.getByLabel('Edge spacing').fill('1');
  20  |   await page.getByLabel('Part spacing').fill('0.2');
  21  |   await page.getByLabel('Time').fill('1');
  22  |   await page.getByText('Advanced').click();
  23  |   await page.getByLabel('Workers').fill('1');
  24  |   await page.getByLabel('Lead-in allowances', { exact:true }).check();
  25  |   await expect(page.getByRole('button', { name:'Nest', exact:true })).toBeDisabled();
  26  |   await page.getByLabel('Lead kerf').fill('0.2');
  27  |   await expect(page.getByText('Download the cutting SVG or DXF', { exact:false })).toBeVisible();
  28  |   await page.getByRole('button', { name:'Nest', exact:true }).click();
  29  |   await expect(page.locator('.summary, .error').first()).toBeVisible({ timeout:90_000 });
> 30  |   await expect(page.locator('.error')).toHaveCount(0);
      |                                        ^ Error: expect(locator).toHaveCount(expected) failed
  31  |   await expect(page.locator('.lead-report')).toContainText('8/10 contours have checked space');
  32  |   await expect(page.locator('.lead-report')).toContainText('2 need manual attention');
  33  |   await expect(page.locator('.lead-report')).toContainText('Open cutting contour');
  34  |   const [svg] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Cutting SVG',exact:true}).click()]);
  35  |   expect(svg.suggestedFilename()).toBe('lead-group-sheet-1-cuts.svg');
  36  |   const svgText = readFileSync(await svg.path(),'utf8');
  37  |   const [dxf] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Cutting DXF',exact:true}).click()]);
  38  |   expect(dxf.suggestedFilename()).toBe('lead-group-sheet-1-cuts.dxf');
  39  |   const [project] = await Promise.all([page.waitForEvent('download'),page.getByRole('button',{name:'Project ZIP',exact:true}).click()]);
  40  |   await project.saveAs(info.outputPath('lead-group.zip'));
  41  |   const files=entries(await project.path());
  42  |   const saved=JSON.parse(files.get('project.json')!);
  43  |   expect(saved.library.lightburn.xml).toBe(original);
  44  |   expect(saved.result.lead_in.validation.source_checked).toBe(true);
  45  |   expect(saved.result.lead_in.validation.coverage).toEqual({expected_contours:10,reserved_contours:8,flagged_contours:2});
  46  |   expect(files.get('sheets/lead-group-sheet-1-cuts.svg')).toBe(svgText);
  47  |   expect(files.get('sheets/lead-group-sheet-1-cuts.dxf')).toBe(readFileSync(await dxf.path(),'utf8'));
  48  |   await page.evaluate(({ original, output, cuts }) => {
  49  |     const parser=new DOMParser();
  50  |     const before=parser.parseFromString(original,'text/xml');
  51  |     const after=parser.parseFromString(output,'text/xml');
  52  |     const sourceChildren=before.querySelector('Children')!.outerHTML;
  53  |     const groups=after.querySelectorAll('LightBurnProject > Shape[Type="Group"] > Children');
  54  |     if(groups.length !== 2 || Array.from(groups).some(g=>g.outerHTML!==sourceChildren)) throw new Error('Editable group children changed');
  55  |     for(const setting of Array.from(before.querySelectorAll('CutSetting'))) {
  56  |       if(!Array.from(after.querySelectorAll('CutSetting')).some(s=>s.outerHTML===setting.outerHTML)) throw new Error('Cut settings changed');
  57  |     }
  58  |     const svg=parser.parseFromString(cuts,'image/svg+xml');
  59  |     const paths=svg.querySelectorAll('#CUT path');
  60  |     if(paths.length!==2) throw new Error('Rigid copy coverage changed');
  61  |     for(const path of Array.from(paths)) {
  62  |       const d=path.getAttribute('d')!;
  63  |       if((d.match(/M/g)||[]).length!==5 || (d.match(/Z/g)||[]).length!==4) throw new Error('Original cut coverage or open path changed');
  64  |     }
  65  |     if(svg.querySelector('#SHEET')) throw new Error('Unexpected sheet outline in cutting file');
  66  |     if(!svg.querySelector('#LEADIN')) throw new Error('Missing lead review paths');
  67  |   },{original,output:files.get('sheets/lead-group-sheet-1.lbrn2')!,cuts:svgText});
  68  |   await page.locator('.results').evaluate(el=>el.scrollTo(0,el.scrollHeight));
  69  |   await page.screenshot({path:info.outputPath('lead-group.png'),fullPage:true});
  70  | });
  71  | 
  72  | test('legacy LightBurn paths become editable modern sheet files', async ({ page }, info) => {
  73  |   const legacy = fileURLToPath(new URL('../../crates/core/tests/fixtures/legacy.lbrn', import.meta.url));
  74  |   await page.goto('/');
  75  |   await page.locator('.drop input[type=file]').setInputFiles(legacy);
  76  |   await expect(page.locator('table.parts tbody tr')).toHaveCount(1);
  77  |   await page.getByLabel('Quantity of legacy-unit-1').fill('2');
  78  |   const sheet = page.locator('fieldset.sheet-row').first();
  79  |   await sheet.getByLabel('Width').fill('34');
  80  |   await sheet.getByLabel('Height').fill('14');
  81  |   await sheet.getByLabel('Margin').fill('0');
  82  |   await page.getByLabel('Edge spacing').fill('0.5');
  83  |   await page.getByLabel('Time').fill('1');
  84  |   await page.getByText('Advanced').click();
  85  |   await page.getByLabel('Workers').fill('1');
  86  |   await page.getByRole('button', { name: 'Nest', exact: true }).click();
  87  |   await expect(page.locator('.summary, .error').first()).toBeVisible({ timeout: 90_000 });
  88  |   await expect(page.locator('.error')).toHaveCount(0);
  89  |   await expect(page.locator('.summary')).toContainText('valid');
  90  |   await expect(page.locator('.summary')).toContainText('2/2');
  91  |   await expect(page.getByRole('button', { name: 'LightBurn', exact: true })).toHaveCount(2);
  92  |   const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Download all sheets (ZIP)' }).click()]);
  93  |   await download.saveAs(info.outputPath('legacy-sheets.zip'));
  94  |   const files = entries(await download.path());
  95  |   expect(files.size).toBe(2);
  96  |   const checked = await page.evaluate(outputs => outputs.map(xml => {
  97  |     const doc = new DOMParser().parseFromString(xml, 'text/xml');
  98  |     return {
  99  |       valid: !doc.querySelector('parsererror'), version: doc.documentElement.getAttribute('FormatVersion'),
  100 |       vertices: doc.querySelectorAll('VertList').length, primitives: doc.querySelectorAll('PrimList').length,
  101 |       retained: doc.querySelector('V[Future]')?.getAttribute('Future'), start: doc.querySelector('Shape[StartV]')?.getAttribute('StartV'),
  102 |       opaque: doc.querySelector('Unknown V')?.getAttribute('vx'),
  103 |     };
  104 |   }), [...files.values()]);
  105 |   for (const value of checked) expect(value).toEqual({ valid: true, version: '1', vertices: 2, primitives: 2, retained: 'a & b', start: '1', opaque: 'opaque' });
  106 |   await page.screenshot({ path: info.outputPath('legacy-layout.png'), fullPage: true });
  107 | });
  108 | 
  109 | function entries(path: string): Map<string, string> {
  110 |   const data = readFileSync(path), files = new Map<string, string>();
  111 |   for (let at = 0; data.readUInt32LE(at) === 0x04034b50;) {
  112 |     expect(data.readUInt16LE(at + 8)).toBe(0);
  113 |     const size = data.readUInt32LE(at + 18), length = data.readUInt16LE(at + 26);
  114 |     const start = at + 30 + length + data.readUInt16LE(at + 28);
  115 |     files.set(data.subarray(at + 30, at + 30 + length).toString('utf8'), data.subarray(start, start + size).toString('utf8'));
  116 |     at = start + size;
  117 |   }
  118 |   return files;
  119 | }
  120 | 
  121 | test('LightBurn rigid units nest and download as editable per-sheet projects', async ({ page }, info) => {
  122 |   await page.goto('/');
  123 |   await page.locator('.drop input[type=file]').setInputFiles(fixture);
  124 |   await expect(page.locator('table.parts tbody tr')).toHaveCount(3);
  125 |   const group = page.locator('table.parts tbody tr').filter({ hasText: 'roundtrip-unit-1' });
  126 |   await expect(group).toContainText('2.0 cm²');
  127 |   expect((await group.locator('.thumb path').getAttribute('d'))!.match(/M/g)).toHaveLength(2);
  128 |   await expect(page.getByText('LightBurn layers — preserved')).toBeVisible();
  129 |   await expect(page.locator('.import-channels tbody tr').first()).toContainText('0.2');
  130 |   await expect(page.getByLabel('Include sheet outline on T1')).toBeChecked();
```