# Instructions

- Following Playwright test failed.
- Explain why, be concise, respect Playwright best practices.
- Provide a snippet of code with the fix, if possible.

# Test info

- Name: features.spec.ts >> lead allowances expose flags, reserve offcuts and export a separate review layer
- Location: tests/features.spec.ts:70:1

# Error details

```
Error: nesting failed: Error: no complete layout within 1 s: these parts are many or detailed; allow more time
```

# Page snapshot

```yaml
- generic [ref=e3]:
  - banner [ref=e4]:
    - heading "Nestbolt" [level=1] [ref=e5]
    - textbox "Project name" [ref=e6]: Untitled project
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
        - generic [ref=e20]:
          - generic [ref=e21]:
            - checkbox "Close larger gaps" [ref=e22]
            - text: Close larger gaps
          - paragraph [ref=e23]: Gaps up to 0.005 mm join automatically. Larger repairs are listed with their positions.
          - group [ref=e24]:
            - generic "Layers and colours — leads.svg" [ref=e25] [cursor=pointer]
            - paragraph [ref=e26]: "Cleanup: 0 duplicate segments removed; 0 zero-length segments removed; 0 collinear overlaps merged."
            - paragraph [ref=e27]: Automatic selection prefers cut, outline and profile layers. Tick a choice to set a filter; layer and colour filters apply together. Counts include ignored entities.
            - group "Cut layers (automatic)" [ref=e28]:
              - generic [ref=e30]:
                - checkbox "Layer 0 in leads.svg" [checked] [ref=e31]
                - text: "0"
                - generic [ref=e32]: 1 entities · 1 selected outlines/paths
            - group "Cut colours (automatic)" [ref=e33]:
              - generic [ref=e35]:
                - 'checkbox "Colour #000000 in leads.svg" [checked] [ref=e36]'
                - text: "#000000"
                - generic [ref=e37]: 1 entities · 1 selected outlines/paths
            - group "Sheet outline layers (automatic SHEET)" [ref=e38]:
              - generic [ref=e40]:
                - checkbox "Sheet layer 0 in leads.svg" [ref=e41]
                - text: "0"
            - button "Use automatic selection for leads.svg" [ref=e42] [cursor=pointer]
          - button "Apply import options" [ref=e43] [cursor=pointer]
        - table [ref=e44]:
          - rowgroup [ref=e45]:
            - row [ref=e46]:
              - columnheader [ref=e47]
              - columnheader "Part" [ref=e48]
              - columnheader "Qty" [ref=e49]
              - columnheader "Rotation" [ref=e50]
              - columnheader "Mirror" [ref=e51]
              - columnheader [ref=e52]
          - rowgroup [ref=e53]:
            - row [ref=e54]:
              - cell [ref=e55]
              - cell "leads-1 2.0 cm²" [ref=e58]:
                - text: leads-1
                - generic [ref=e59]: 2.0 cm²
              - cell [ref=e60]:
                - spinbutton "Quantity of leads-1" [ref=e61]: "2"
              - cell "0/90/180/270°" [ref=e62]:
                - combobox "Rotations of leads-1" [ref=e63]:
                  - option "0/90/180/270°" [selected]
                  - option "0/180° (grain)"
                  - option "Fixed 0°"
                  - option "Every 15°"
                  - option "Free"
              - cell [ref=e64]:
                - checkbox "Allow mirroring leads-1" [ref=e65]
              - cell [ref=e66]:
                - button "Remove leads-1" [ref=e67] [cursor=pointer]: ×
      - region [ref=e68]:
        - heading "Sheets" [level=2] [ref=e69]
        - group "Sheet size 1" [ref=e70]:
          - generic [ref=e72]:
            - text: Width
            - spinbutton "Width mm" [ref=e73]: "60"
            - text: mm
          - generic [ref=e74]:
            - text: Height
            - spinbutton "Height mm" [ref=e75]: "35"
            - text: mm
          - generic [ref=e76]:
            - text: Count
            - spinbutton "Count" [ref=e77]
          - generic [ref=e78]:
            - text: Margin
            - spinbutton "Margin mm" [ref=e79]: "0"
            - text: mm
          - generic [ref=e80]:
            - text: Remnant outline
            - button "Remnant outline for sheet size 1" [ref=e81]
          - group [ref=e82]:
            - generic "Defects (0)" [ref=e83]
        - combobox "Add a sheet size" [ref=e84]:
          - option "Add sheet size…" [selected]
          - option "Diode laser 300×200"
          - option "CO2 bed 600×400"
          - option "Plywood 1220×2440"
          - option "Sheet metal 1250×2500"
          - option "Sheet metal 1500×3000"
          - option "Fabric roll 1500 × 10 m"
      - region [ref=e85]:
        - heading "Settings" [level=2] [ref=e86]
        - generic [ref=e87]:
          - generic [ref=e88]:
            - text: Part spacing
            - spinbutton "Part spacing mm" [ref=e89]: "1"
            - text: mm
          - generic [ref=e90]:
            - text: Edge spacing
            - spinbutton "Edge spacing mm" [ref=e91]: "1"
            - text: mm
          - generic [ref=e92]:
            - text: Goal
            - combobox "Goal" [ref=e93]:
              - option "Place every part" [selected]
              - option "Fill the sheets (most area)"
              - option "Fill by priority"
          - generic [ref=e94]:
            - text: Time
            - spinbutton "Time s" [ref=e95]: "1"
            - text: s
        - generic [ref=e96]:
          - checkbox "Common-line cutting" [ref=e97]
          - text: Common-line cutting
        - generic [ref=e98]:
          - checkbox "Lead-in allowances" [checked] [ref=e99]
          - text: Lead-in allowances
        - generic [ref=e100]:
          - generic [ref=e101]:
            - text: Lead kerf
            - spinbutton "Lead kerf mm" [ref=e102]: "0.2"
            - text: mm
          - generic [ref=e103]:
            - text: Lead length
            - spinbutton "Lead length mm" [ref=e104]: "3"
            - text: mm
          - generic [ref=e105]:
            - text: Lead style
            - combobox "Lead style" [ref=e106]:
              - option "Line"
              - option "Arc" [selected]
          - generic [ref=e107]:
            - text: Outer lead angle
            - spinbutton "Outer lead angle °" [ref=e108]: "45"
            - text: °
          - generic [ref=e109]:
            - text: Hole lead angle
            - spinbutton "Hole lead angle °" [ref=e110]: "90"
            - text: °
        - paragraph [ref=e111]: Enter the measured kerf. Length is the distance along the lead, including an arc. Space is reserved for both cutting directions. Small holes may need a shorter lead or a manual start.
        - paragraph [ref=e112]: In LightBurn, turn off Choose best starting point and LEADIN layer output. Use the reported length and style; outer angles are positive, hole angles negative. Keep lead-out and overcut off.
        - group [ref=e113]:
          - generic "Advanced" [ref=e114] [cursor=pointer]
          - generic [ref=e115]:
            - checkbox "Quick initial layout" [ref=e116]
            - text: Quick initial layout
          - paragraph [ref=e117]: Start with a simple arrangement, then improve it. May use more material.
          - generic [ref=e118]:
            - generic "Complex drawings and large quantities use fewer workers to limit memory" [ref=e119]:
              - text: Workers
              - spinbutton "Workers" [ref=e120]: "1"
            - generic [ref=e121]:
              - text: Seed
              - spinbutton "Seed" [ref=e122]: "0"
            - generic [ref=e123]:
              - checkbox "Repeatable" [ref=e124]
              - text: Repeatable
      - button "Nest" [ref=e126] [cursor=pointer]
      - alert [ref=e127]: "Error: no complete layout within 1 s: these parts are many or detailed; allow more time"
    - region [ref=e128]:
      - heading "Result" [level=2] [ref=e129]
      - paragraph [ref=e130]: Import parts, choose sheets and press Nest, or try the example boxes.
  - contentinfo [ref=e131]:
    - text: Built on
    - link "jagua-rs" [ref=e132] [cursor=pointer]:
      - /url: https://github.com/JeroenGar/jagua-rs
    - text: and
    - link "sparrow" [ref=e133] [cursor=pointer]:
      - /url: https://github.com/JeroenGar/sparrow
    - text: by Jeroen Gardeyn et al. MIT licensed;
    - link "third-party notices" [ref=e134] [cursor=pointer]:
      - /url: ./THIRD_PARTY_NOTICES.txt
    - text: .
    - link "Benchmark results" [ref=e135] [cursor=pointer]:
      - /url: ./results/
    - text: against Deepnest, SVGnest and Sparrow.
```

# Test source

```ts
  1   | import { expect, test, type Page } from '@playwright/test';
  2   | import { readFileSync } from 'node:fs';
  3   | import { fileURLToPath } from 'node:url';
  4   | import { zip } from '../src/zip.js';
  5   | import type { Project } from '../src/types.js';
  6   | 
  7   | // One end-to-end test per v1 feature through the browser app (the CLI has the
  8   | // same set in crates/cli/tests/features.rs). examples/parts.svg imports as
  9   | // parts-1 frame (80 x 60, 60 x 40 window), parts-2 washer (24 mm), parts-3
  10  | // bracket and parts-4 elliptical tab.
  11  | const example = (name: string) => fileURLToPath(new URL(`../../examples/${name}`, import.meta.url));
  12  | const fixture = (name: string) => fileURLToPath(new URL(`./fixtures/${name}`, import.meta.url));
  13  | 
  14  | type Layout = { sheets: { id: string; stock_id: string }[];
  15  |   placements: { part_id: string; transform: { rotation_radians: number; mirrored: boolean } }[] };
  16  | type ProjectFile = { request: { quick_start?: boolean; common_line?: { kerf_mm: number; search_bonus?: boolean }; spacing_mm: number; edge_spacing_mm: number; sheets: { count?: number | null }[] };
  17  |   result: { layout: Layout; validation: { valid: boolean } } };
  18  | 
  19  | /** Read one entry of the app's stored (uncompressed) ZIP. */
  20  | function zipEntry(path: string, wanted: string): string {
  21  |   const bytes = readFileSync(path);
  22  |   for (let at = 0; bytes.readUInt32LE(at) === 0x04034b50;) {
  23  |     const size = bytes.readUInt32LE(at + 18);
  24  |     const nameLength = bytes.readUInt16LE(at + 26);
  25  |     const extra = bytes.readUInt16LE(at + 28);
  26  |     const name = bytes.subarray(at + 30, at + 30 + nameLength).toString('utf8');
  27  |     const start = at + 30 + nameLength + extra;
  28  |     if (name === wanted) return bytes.subarray(start, start + size).toString('utf8');
  29  |     at = start + size;
  30  |   }
  31  |   throw new Error(`${wanted} not in ${path}`);
  32  | }
  33  | 
  34  | async function project(page: Page): Promise<ProjectFile> {
  35  |   const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  36  |   return JSON.parse(zipEntry(await archive.path(), 'project.json'));
  37  | }
  38  | 
  39  | /** Import files, keep only the given parts with quantities, one sheet size, one worker. */
  40  | async function setUp(page: Page, files: string[], keep: Record<string, number>, w: number, h: number, seconds = 5) {
  41  |   await page.goto('/');
  42  |   await page.locator('.drop input[type=file]').setInputFiles(files);
  43  |   await expect(page.locator('table.parts tbody tr').first()).toBeVisible();
  44  |   const ids = await page.getByRole('button', { name: /^Remove / }).evaluateAll((buttons) =>
  45  |     buttons.map((b) => b.getAttribute('aria-label')!.replace('Remove ', '')));
  46  |   for (const id of ids.filter((id) => !(id in keep))) {
  47  |     await page.getByRole('button', { name: `Remove ${id}`, exact: true }).click();
  48  |   }
  49  |   for (const [id, quantity] of Object.entries(keep)) await page.getByLabel(`Quantity of ${id}`).fill(String(quantity));
  50  |   const sheet = page.locator('fieldset.sheet-row').first();
  51  |   await sheet.getByLabel('Width').fill(String(w));
  52  |   await sheet.getByLabel('Height').fill(String(h));
  53  |   await page.getByLabel('Time').fill(String(seconds));
  54  |   await page.getByText('Advanced').click();
  55  |   await page.getByLabel('Workers').fill('1');
  56  |   return sheet;
  57  | }
  58  | 
  59  | async function nest(page: Page) {
  60  |   await page.getByRole('button', { name: 'Nest' }).click();
  61  |   // Lead review flags also use .error; only the app alert means nesting failed.
  62  |   await expect(page.locator('.summary, [role="alert"]').first()).toBeVisible({ timeout: 90_000 });
> 63  |   if (await page.getByRole('alert').count()) throw new Error(`nesting failed: ${await page.getByRole('alert').innerText()}`);
      |                                                    ^ Error: nesting failed: Error: no complete layout within 1 s: these parts are many or detailed; allow more time
  64  |   await expect(page.locator('.summary')).toContainText('valid');
  65  | }
  66  | 
  67  | const metric = async (page: Page, name: string) =>
  68  |   Number(await page.locator('.summary div', { hasText: name }).locator('dd').innerText());
  69  | 
  70  | test('lead allowances expose flags, reserve offcuts and export a separate review layer', async ({ page }, testInfo) => {
  71  |   const source = fileURLToPath(new URL('../../crates/core/tests/fixtures/leads.svg', import.meta.url));
  72  |   const sheet = await setUp(page, [source], { 'leads-1': 2 }, 60, 35, 1);
  73  |   await sheet.getByLabel('Margin').fill('0');
  74  |   await page.getByLabel('Lead-in allowances', { exact: true }).check();
  75  |   await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  76  |   await page.getByLabel('Lead kerf').fill('0.2');
  77  |   await page.getByLabel('Lead length').fill('0.4');
  78  |   await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  79  |   await page.getByLabel('Lead length').fill('3');
  80  |   await page.getByLabel('Outer lead angle').fill('45.001');
  81  |   await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  82  |   await page.getByLabel('Outer lead angle').fill('45');
  83  |   await page.getByLabel('Lead style').selectOption('arc');
  84  |   await nest(page);
  85  |   await expect(page.locator('.lead-report')).toContainText('4/6 contours have checked space', { timeout: 90_000 });
  86  |   await expect(page.locator('.lead-report')).toContainText('2 need manual attention');
  87  |   await expect(page.locator('.lead-preview')).toHaveCount(4);
  88  |   expect(await page.locator('svg.sheet').first().evaluate(el => el.getBoundingClientRect().height)).toBeGreaterThan(150);
  89  |   await expect(page.locator('[role=alert]')).toHaveCount(0);
  90  |   const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP' }).click()]);
  91  |   const saved = JSON.parse(zipEntry(await archive.path(), 'project.json'));
  92  |   expect(saved.request.lead_in.style).toBe('arc');
  93  |   expect(saved.result.validation.metrics.placed_area).toBeCloseTo(391.68, 5);
  94  |   expect(saved.result.lead_in.validation.valid).toBe(true);
  95  |   expect(saved.result.lead_in.validation.source_checked).toBe(true);
  96  |   expect(saved.result.lead_in.validation.coverage).toEqual({ expected_contours: 6, reserved_contours: 4, flagged_contours: 2 });
  97  |   expect(saved.result.lead_in.parts.flatMap((p: { reservations: { shortened: boolean }[] }) => p.reservations).filter((r: { shortened: boolean }) => r.shortened)).toHaveLength(2);
  98  |   await expect(page.locator('.lead-report')).toContainText('1.2 mm lead.');
  99  |   const svg = zipEntry(await archive.path(), `sheets/${saved.result.layout.sheets[0].id}.svg`);
  100 |   expect(svg).toContain('id="LEADIN"');expect(svg).toContain('stroke="#ff0000"');
  101 |   const dxf = zipEntry(await archive.path(), `sheets/${saved.result.layout.sheets[0].id}.dxf`);
  102 |   expect(dxf).toContain('LEADIN');
  103 |   await testInfo.attach('lead-project', { body: JSON.stringify(saved), contentType: 'application/json' });
  104 |   await testInfo.attach('lead-controls', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  105 |   await page.locator('.results').evaluate(el => el.scrollTo(0, el.scrollHeight));
  106 |   await testInfo.attach('lead-preview', { body: await page.screenshot({ fullPage: true }), contentType: 'image/png' });
  107 |   await page.getByLabel('Common-line cutting', { exact: true }).check();
  108 |   await page.getByLabel('Kerf mm', { exact: true }).fill('0.3');
  109 |   await expect(page.getByLabel('Lead kerf')).toHaveValue('0.3');
  110 |   await page.getByLabel('Lead-in allowances', { exact: true }).uncheck();
  111 |   await expect(page.locator('.lead-report')).toHaveCount(0);
  112 | });
  113 | 
  114 | for (const bonus of [false, true]) {
  115 | test(`common-line kerf overrides spacing and exports its own compensated layer (bonus ${bonus})`, async ({ page }, testInfo) => {
  116 |   const source = fileURLToPath(new URL('../../crates/core/tests/fixtures/common-panels.svg', import.meta.url));
  117 |   const sheet = await setUp(page, [source], { 'common-panels-1': 2 }, 86, 36, 1);
  118 |   await sheet.getByLabel('Margin').fill('0');
  119 |   await page.getByLabel('Repeatable', { exact: true }).check();
  120 |   await page.getByLabel('Part spacing').fill('5');
  121 |   await page.getByLabel('Common-line cutting', { exact: true }).check();
  122 |   await expect(page.getByRole('button', { name: 'Nest', exact: true })).toBeDisabled();
  123 |   await expect(page.getByLabel('Search for more shared cuts')).not.toBeChecked();
  124 |   if (bonus) await page.getByLabel('Search for more shared cuts').check();
  125 |   await page.getByLabel('Kerf mm', { exact: true }).fill('0.2');
  126 |   await expect(page.getByLabel('Search for more shared cuts')).toBeChecked({ checked: bonus });
  127 |   await expect(page.getByLabel('Part spacing')).toBeDisabled();
  128 |   await expect(page.getByLabel('Part spacing')).toHaveValue('0.2');
  129 |   await nest(page);
  130 |   const saved = await project(page);
  131 |   expect(!!saved.request.common_line?.search_bonus).toBe(bonus);
  132 |   await testInfo.attach('common-line-project', { body: JSON.stringify(saved), contentType: 'application/json' });
  133 |   await expect(page.locator('.common-line-report')).toContainText('30.0 mm saved');
  134 |   const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Download all sheets (ZIP)' }).click()]);
  135 |   const svg = zipEntry(await archive.path(), `sheets/${saved.result.layout.sheets[0].id}.svg`);
  136 |   expect(svg).toContain('id="COMMON"');
  137 |   expect(svg).toContain('stroke="#0000ff"');
  138 |   await page.getByLabel('Common-line cutting', { exact: true }).uncheck();
  139 |   await expect(page.getByLabel('Part spacing')).toHaveValue('5');
  140 |   await expect(page.locator('.common-line-report')).toHaveCount(0);
  141 | });
  142 | }
  143 | 
  144 | test('quick initial layout is optional and survives project export and reopening', async ({ page }) => {
  145 |   await setUp(page, [example('parts.svg')], { 'parts-3': 8 }, 300, 150, 1);
  146 |   const quick = page.getByLabel('Quick initial layout', { exact: true });
  147 |   await expect(quick).not.toBeChecked();
  148 |   await quick.check();
  149 |   await page.getByLabel('Repeatable', { exact: true }).check();
  150 |   await nest(page);
  151 |   await expect(page.locator('.summary')).toContainText('8/8');
  152 |   const saved = await project(page);
  153 |   expect(saved.request.quick_start).toBe(true);
  154 |   expect(saved.result.validation.valid).toBe(true);
  155 |   const [archive] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP', exact: true }).click()]);
  156 |   const path = await archive.path();
  157 |   expect(zipEntry(path, `sheets/${saved.result.layout.sheets[0].id}.svg`)).toContain('<svg');
  158 |   await page.getByRole('button', { name: 'New', exact: true }).click();
  159 |   await page.locator('input[type=file][accept=".zip"]').setInputFiles(path);
  160 |   await expect(quick).toBeChecked();
  161 |   await expect(page.locator('.summary')).toContainText('8/8');
  162 |   await quick.uncheck();
  163 |   expect((await project(page)).request.quick_start).toBeUndefined();
```