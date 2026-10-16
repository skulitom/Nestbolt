"""Prepare a separate workspace for actual native and browser import-surface checks."""
from pathlib import Path
import shutil
import subprocess

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'output/release-surface-probe'
CORE=ROOT/'output/ci-curve-probe/candidate-core'
OUT.mkdir()
paths=subprocess.check_output(['git','ls-files','-z','--','Cargo.toml','Cargo.lock','rust-toolchain.toml',
    'LICENSE','THIRD_PARTY_NOTICES','README.md','.cargo','crates','web','examples','schemas','scripts/build_web.py'],cwd=ROOT).decode().split('\0')
for relative in filter(None,paths):
    source=ROOT/relative
    if source.is_file():
        target=OUT/relative
        target.parent.mkdir(parents=True,exist_ok=True)
        shutil.copyfile(source,target)
for relative in ['src/holes.rs','src/lightburn.rs','src/lightburn/path.rs','src/lightburn/units.rs',
    'tests/lightburn.rs','tests/project_lightburn.rs','tests/lightburn_diagnostics.rs','tests/hole_index_regression.rs',
    'tests/fixtures/ci-hole-curve.svg']:
    shutil.copyfile(CORE/relative,OUT/'crates/core'/relative)

def write(relative,text):
    (OUT/relative).write_text(text,encoding='utf-8',newline='\n')

def append(relative,text):
    with (OUT/relative).open('a',encoding='utf-8',newline='\n') as f:
        f.write(text)

write('crates/core/tests/fixtures/native-diagnostics.lbrn2','''<?xml version="1.0" encoding="UTF-8"?>
<!-- Original Nestbolt diagnostic fixture, MIT. -->
<LightBurnProject FormatVersion="1">
  <CutSetting type="Cut"><index Value="0"/></CutSetting>
  <CutSetting type="Tool"><index Value="30"/></CutSetting>
  <CutSetting_Img type="Image"><index Value="0"/></CutSetting_Img>
  <Shape Type="Rect" CutIndex="0" W="40" H="30"/>
  <Shape Type="Text" CutIndex="0" Str="attached"><BackupPath Type="Path"><VertList>V0 0V2 0V0 2</VertList><PrimList>LineClosed</PrimList></BackupPath></Shape>
  <Shape Type="Path" CutIndex="0"><XForm>1 0 0 1 100 0</XForm><VertList>V0 0V2 3</VertList><PrimList>B0 1</PrimList></Shape>
  <Shape Type="Path" CutIndex="30"><VertList>V0 0V2 3</VertList><PrimList>LineOpen</PrimList></Shape>
  <Shape Type="Group"><XForm>1 0 0 1 200 0</XForm><Children>
    <Shape Type="Text" CutIndex="0" Str="grouped"><BackupPath Type="Path"><VertList>V0 0V2 0V0 2</VertList><PrimList>LineClosed</PrimList></BackupPath></Shape>
    <Shape Type="Rect" CutIndex="0" W="40" H="30"/>
  </Children></Shape>
  <Shape Type="Bitmap" CutIndex="0" W="2" H="2" Data="aW1hZ2U="><XForm>1 0 0 1 300 0</XForm></Shape>
</LightBurnProject>
''')
append('crates/cli/tests/features.rs','''

#[test]
fn lightburn_import_diagnostics_reach_cli_and_saved_library() {
    let dir = temp("native-diagnostics");
    let source = include_str!("../../core/tests/fixtures/native-diagnostics.lbrn2");
    let input = dir.join("native-diagnostics.lbrn2");
    let output = dir.join("library.json");
    fs::write(&input, source).unwrap();
    let result = nestbolt(&["import".as_ref(), input.as_os_str(), "--output".as_ref(), output.as_os_str()]);
    assert!(result.status.success(), "{}", String::from_utf8_lossy(&result.stderr));
    let reply: Value = serde_json::from_slice(&result.stdout).unwrap();
    let saved: Value = serde_json::from_slice(&fs::read(output).unwrap()).unwrap();
    assert_eq!(saved["lightburn"]["xml"], source);
    assert_eq!(saved["parts"].as_array().unwrap().len(), 4);
    assert_eq!(reply["warnings"], saved["warnings"]);
    let messages = reply["warnings"].as_array().unwrap().iter().map(|w|w.as_str().unwrap()).collect::<Vec<_>>().join("\\n");
    for required in ["LightBurn shape 2 (Path): nesting uses a bounding rectangle", "LightBurn shape 5 (Text): nesting uses a bounding rectangle", "LightBurn shape 7 (Bitmap): nesting uses a bounding rectangle", "native endpoint fallback for missing Bezier control points", "straight line segments with both controls absent: 1", "using embedded cached font outlines", "local fonts are not consulted"] {
        assert!(messages.contains(required), "{messages}");
    }
    for excluded in ["LightBurn shape 1 (Text): nesting uses a bounding rectangle", "LightBurn shape 3 (Path): nesting uses a bounding rectangle"] {
        assert!(!messages.contains(excluded), "{messages}");
    }
}
''')
append('crates/mcp/tests/connection.rs','''

#[tokio::test(flavor = "current_thread")]
async fn lightburn_import_diagnostics_reach_mcp_and_saved_library() {
    let stamp = std::time::SystemTime::now().duration_since(std::time::UNIX_EPOCH).unwrap().as_nanos();
    let workspace = std::env::temp_dir().join(format!("nestbolt-mcp-diagnostics-{}-{stamp}",std::process::id()));
    std::fs::create_dir_all(&workspace).unwrap();
    let source = include_str!("../../core/tests/fixtures/native-diagnostics.lbrn2");
    std::fs::write(workspace.join("native-diagnostics.lbrn2"),source).unwrap();
    timeout(Duration::from_secs(30), async {
        let mut command=Command::new(env!("CARGO_BIN_EXE_nestbolt-mcp"));
        command.env("NESTBOLT_WORKSPACE", &workspace);
        let client=().serve(TokioChildProcess::new(command).unwrap()).await.unwrap();
        let imported=client.call_tool(CallToolRequestParams::new("import_parts").with_arguments(args(json!({"paths":["native-diagnostics.lbrn2"]})))).await.unwrap().structured_content.unwrap();
        assert_eq!(imported["part_count"],4);
        let saved:Value=serde_json::from_slice(&std::fs::read(workspace.join(imported["library_path"].as_str().unwrap())).unwrap()).unwrap();
        assert_eq!(saved["lightburn"]["xml"],source);
        assert_eq!(imported["warnings"],saved["warnings"]);
        let messages=imported["warnings"].as_array().unwrap().iter().map(|w|w.as_str().unwrap()).collect::<Vec<_>>().join("\\n");
        for required in ["LightBurn shape 2 (Path): nesting uses a bounding rectangle", "LightBurn shape 5 (Text): nesting uses a bounding rectangle", "LightBurn shape 7 (Bitmap): nesting uses a bounding rectangle", "native endpoint fallback for missing Bezier control points", "straight line segments with both controls absent: 1", "using embedded cached font outlines", "local fonts are not consulted"] {
            assert!(messages.contains(required), "{messages}");
        }
        for excluded in ["LightBurn shape 1 (Text): nesting uses a bounding rectangle", "LightBurn shape 3 (Path): nesting uses a bounding rectangle"] {
            assert!(!messages.contains(excluded), "{messages}");
        }
        client.cancel().await.unwrap();
    }).await.expect("diagnostic import timed out");
}
''')
append('web/tests/lightburn.spec.ts','''

test('LightBurn import diagnostics describe fallback geometry and survive a project download', async ({ page }, info) => {
  const fixture = fileURLToPath(new URL('../../crates/core/tests/fixtures/native-diagnostics.lbrn2', import.meta.url));
  const original = readFileSync(fixture, 'utf8');
  await page.goto('/');
  await page.locator('.drop input[type=file]').setInputFiles(fixture);
  await expect(page.locator('table.parts tbody tr')).toHaveCount(4);
  await page.getByText(/Show all import messages/).click();
  const all = page.locator('details').filter({ has: page.locator('summary', { hasText: 'Show all import messages' }) });
  for (const message of ['LightBurn shape 2 (Path): nesting uses a bounding rectangle', 'LightBurn shape 5 (Text): nesting uses a bounding rectangle', 'LightBurn shape 7 (Bitmap): nesting uses a bounding rectangle', 'native endpoint fallback for missing Bezier control points', 'straight line segments with both controls absent: 1', 'using embedded cached font outlines', 'local fonts are not consulted']) {
    await expect(all).toContainText(message);
  }
  await expect(all).not.toContainText('LightBurn shape 1 (Text): nesting uses a bounding rectangle');
  await expect(all).not.toContainText('LightBurn shape 3 (Path): nesting uses a bounding rectangle');
  const messages = await all.locator('li').allTextContents();
  const [download] = await Promise.all([page.waitForEvent('download'), page.getByRole('button', { name: 'Project ZIP', exact: true }).click()]);
  const path = info.outputPath('native-diagnostics.zip');
  await download.saveAs(path);
  const saved = JSON.parse(entries(path).get('project.json')!);
  expect(saved.library.lightburn.xml).toBe(original);
  expect(saved.library.warnings).toEqual(messages);
  await page.screenshot({ path: info.outputPath('native-diagnostics.png'), fullPage: true });
});
''')
# A dedicated server avoids accidentally testing a different checkout's app.
config=(OUT/'web/playwright.config.ts').read_text(encoding='utf-8')
write('web/playwright.config.ts',config.replace('4173','4185').replace('reuseExistingServer: !process.env.CI','reuseExistingServer: false'))
package=(OUT/'web/package.json').read_text(encoding='utf-8')
write('web/package.json',package.replace('--port 4173','--port 4185'))
print('Prepared isolated surface workspace:',OUT)
