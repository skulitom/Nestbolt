import { partGeometry } from './types';
import { useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { exportFilename, exportSheet, importFiles, importSheet, inspectFiles, readDrawingFile, Portfolio } from './engine';
import { SheetCanvas } from './canvas';
import { PALETTE, PartThumb, SheetPreview, sheetUsage } from './preview';
import { deleteProject, listProjects, loadProject, saveProject } from './storage';
import type { Example, ImportSelection, Layout, Library, LibraryPart, Mode, NestRequest, NestResult, Project, RequestPart, RequestSheet, Rotations, SheetOutline } from './types';
import { unzip, zip } from './zip';

const ROTATIONS: { label: string; value: Rotations }[] = [
  { label: '0/90/180/270°', value: { kind: 'list', degrees: [0, 90, 180, 270] } },
  { label: '0/180° (grain)', value: { kind: 'list', degrees: [0, 180] } },
  { label: 'Fixed 0°', value: { kind: 'list', degrees: [0] } },
  { label: 'Every 15°', value: { kind: 'step', degrees: 15 } },
  { label: 'Free', value: { kind: 'free' } },
];
const rotationLabel = (r: Rotations) =>
  ROTATIONS.find((o) => JSON.stringify(o.value) === JSON.stringify(r))?.label ?? 'Custom';

const PRESETS: { label: string; w: number; h: number }[] = [
  { label: 'Diode laser 300×200', w: 300, h: 200 },
  { label: 'CO2 bed 600×400', w: 600, h: 400 },
  { label: 'Plywood 1220×2440', w: 1220, h: 2440 },
  { label: 'Sheet metal 1250×2500', w: 1250, h: 2500 },
  { label: 'Sheet metal 1500×3000', w: 1500, h: 3000 },
  { label: 'Fabric roll 1500 × 10 m', w: 1500, h: 10000 },
];

const blankSheet = (w = 600, h = 400): RequestSheet => ({
  width_mm: w, height_mm: h, count: null, margins_mm: { left: 5, right: 5, bottom: 5, top: 5 }, defects_mm: [] });

const emptyRequest = (): NestRequest => ({ parts: [], sheets: [blankSheet()], spacing_mm: 1, edge_spacing_mm: 1, mode: 'all' });

function download(name: string, data: string | Uint8Array, type: string) {
  const url = URL.createObjectURL(new Blob([data as BlobPart], { type }));
  const a = document.createElement('a');
  a.href = url;
  a.download = name;
  document.body.append(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
}

const num = (e: Event) => Number((e.target as HTMLInputElement).value);
const cores = Math.max(1, Math.min(8, (navigator.hardwareConcurrency || 2) - 1));
/** Each worker holds its own engine: large jobs use fewer, so the tab stays well under 1.5 GB. */
const LARGE_JOB = 1000;
const workersFor = (request: NestRequest, chosen: number) =>
  request.parts.reduce((n, p) => n + p.quantity, 0) > LARGE_JOB ? Math.min(chosen, 2) : chosen;

/** Until the first layout arrives: the sheet's own shape, shimmering, and what is happening. */
function Pending(props: { sheet: RequestSheet; label: string }) {
  const { width_mm: w, height_mm: h } = props.sheet;
  return (
    <div class="pending" role="status">
      <p class="hint">{props.label}</p>
      <div class="frame">
        <div class="skeleton sheet-skeleton" aria-hidden="true"
          style={{ aspectRatio: `${w} / ${h}`, width: `min(100%, calc(var(--fit-h) * ${w / h}))` }} />
      </div>
    </div>
  );
}

export function App() {
  const [name, setName] = useState('Untitled project');
  const [library, setLibrary] = useState<Library | null>(null);
  const [request, setRequest] = useState<NestRequest>(emptyRequest);
  const [result, setResult] = useState<NestResult | null>(null);
  const [seconds, setSeconds] = useState(30);
  const [runSeconds, setRunSeconds] = useState(30);
  const [workers, setWorkers] = useState(Math.min(4, cores));
  const [seed, setSeed] = useState(0);
  const [repeatable, setRepeatable] = useState(false);
  const [busy, setBusy] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [lightburnOutline, setLightburnOutline] = useState(true);
  const [closeGaps, setCloseGaps] = useState(false);
  const [gapLimit, setGapLimit] = useState(0.05);
  const [lastFiles, setLastFiles] = useState<{ name: string; text: string }[]>([]);
  const [importChoices, setImportChoices] = useState<Record<string, ImportSelection>>({});
  const [importInventory, setImportInventory] = useState<NonNullable<Library['imports']>>([]);
  const [sheetMessages, setSheetMessages] = useState<string[]>([]);
  const [progress, setProgress] = useState<{ elapsed: number; best: number | null }>({ elapsed: 0, best: null });
  const [projects, setProjects] = useState<{ name: string; savedAt: string }[]>([]);
  const [examples, setExamples] = useState<Example[]>([]);
  const [live, setLive] = useState<{ layout: Layout; material: number } | null>(null);
  const portfolio = useRef<Portfolio | null>(null);
  const zipInput = useRef<HTMLInputElement>(null);

  useEffect(() => { listProjects().then(setProjects).catch(() => setProjects([])); }, []);
  useEffect(() => {
    fetch('./examples/examples.json').then((r) => r.json()).then(setExamples).catch(() => setExamples([]));
  }, []);

  const colors = useMemo(() => new Map((library?.parts ?? []).map((p, i) => [p.id, PALETTE[i % PALETTE.length]])), [library]);
  const part = (id: string) => library?.parts.find((p) => p.id === id);
  /** The drawing's own element name ("front", "bracket") when it has one. */
  const label = (id: string) => {
    const name = part(id)?.source.split('#')[1]?.split(':')[0];
    return name && !/^(path|rect|circle|ellipse|polygon|g|use)-?\d*$/.test(name) ? `${name} (${id})` : id;
  };
  const update = (change: Partial<NestRequest>) => { setRequest((r) => ({ ...r, ...change })); setResult(null); };
  const updatePart = (i: number, change: Partial<RequestPart>) =>
    update({ parts: request.parts.map((p, j) => (j === i ? { ...p, ...change } : p)) });
  const updateSheet = (i: number, change: Partial<RequestSheet>) =>
    update({ sheets: request.sheets.map((s, j) => (j === i ? { ...s, ...change } : s)) });

  function discardFailedImport(files: { name: string }[]) {
    if (library?.lightburn) {
      if (files.some(f => f.name === library.lightburn!.file)) {
        setLibrary(null); update({ parts: [] });
      }
      return;
    }
    // Keep unrelated files, but never nest stale parts after a failed re-import.
    const retained = (library?.parts ?? []).filter((p) => !files.some((f) => p.source.startsWith(`${f.name}#`)));
    const ids = new Set(retained.map((p) => p.id));
    if (library) setLibrary({ ...library, parts: retained,
      sheet_outlines: (library.sheet_outlines ?? []).filter((s) => !files.some((f) => s.source.startsWith(`${f.name}#`))),
      warnings: library.warnings.filter((w) => !files.some((f) => w.startsWith(`${f.name}:`))),
      imports: (library.imports ?? []).filter((r) => !files.some((f) => f.name === r.file)) });
    update({ parts: request.parts.filter((p) => ids.has(p.id)) });
  }

  async function onFiles(list: FileList | null) {
    if (!list?.length) return;
    setError(null); setBusy('Importing…');
    setResult(null); setLastFiles([]); setImportChoices({}); setImportInventory([]);
    try {
      const files = await Promise.all([...list].map(readDrawingFile));
      setLastFiles(files);
      if (!files.some(f => /\.lbrn2?$/i.test(f.name))) setImportInventory(await inspectFiles(files));
      await importDrawings(files, {});
    } catch (e) {
      discardFailedImport([...list]);
      setError(`${String(e)}. No parts from this import were kept.`); setBusy(null);
    }
  }

  async function importDrawings(files: { name: string; text: string }[], choices = importChoices) {
    setError(null);
    setResult(null);
    setBusy('Importing…');
    try {
      const projectFiles = files.filter(f => /\.lbrn2?$/i.test(f.name));
      if (projectFiles.length) {
        if (files.length !== 1) throw new Error('Open one LightBurn project at a time.');
        const next = await importFiles(files);
        setLibrary(next); setImportInventory([]); setCloseGaps(false); setLightburnOutline(true);
        setName(files[0].name.replace(/\.lbrn2?$/i, ''));
        update({ parts: next.parts.map(p => ({ id: p.id, quantity: 1, rotations: ROTATIONS[0].value, allow_mirror: false, priority: 1 })) });
        return;
      }
      if (library?.lightburn) throw new Error('Choose New before importing SVG/DXF parts into a separate project.');
      // Part ids are `<file stem>-<n>`: importing a file again replaces its parts.
      const imported: Library[] = [];
      for (const file of files) imported.push(await importFiles([file], 0, closeGaps ? gapLimit : undefined, choices[file.name]));
      const merged: Library = { version: 1, tolerance: imported[0].tolerance,
        sheet_outlines: imported.flatMap((r) => r.sheet_outlines ?? []),
        parts: imported.flatMap((r) => r.parts), warnings: imported.flatMap((r) => r.warnings), imports: imported.flatMap((r) => r.imports ?? []) };
      setImportInventory(merged.imports ?? []);
      const retained = (library?.parts ?? []).filter((p) => !files.some((f) => p.source.startsWith(`${f.name}#`)));
      const parts = [...retained, ...merged.parts];
      const retainedIds = new Set(retained.map((p) => p.id));
      const next: Library = { version: 1, tolerance: merged.tolerance, parts,
        sheet_outlines: [...(library?.sheet_outlines ?? []).filter((s) => !files.some((f) => s.source.startsWith(`${f.name}#`))), ...(merged.sheet_outlines ?? [])],
        warnings: [...(library?.warnings ?? []).filter((w) => !files.some((f) => w.startsWith(`${f.name}:`))), ...merged.warnings],
        imports: [...(library?.imports ?? []).filter((r) => !files.some((f) => f.name === r.file)), ...(merged.imports ?? [])] };
      setLibrary(next);
      update({
        parts: [
          ...request.parts.filter((p) => retainedIds.has(p.id)),
          ...merged.parts.map((p) => ({ id: p.id, quantity: 1, rotations: ROTATIONS[0].value, allow_mirror: false, priority: 1 })),
        ],
      });
    } catch (e) {
      discardFailedImport(files);
      setError(`${String(e)}. No parts from this import were kept. Correct the drawing or options and apply again.`);
    } finally {
      setBusy(null);
    }
  }

  function useSheetOutline(i: number, outline: SheetOutline) {
    updateSheet(i, { width_mm: outline.width_mm, height_mm: outline.height_mm,
      outline_mm: outline.outline_mm, outline_tolerance_mm: outline.tolerance_mm, from_import: undefined });
    setSheetMessages([`Sheet size ${i + 1}: ${outline.source}, ${outline.width_mm} × ${outline.height_mm} mm. Moved to the sheet origin.`]);
  }

  /** Prefer a drawing's SHEET boundary over the cuts placed inside it. */
  async function onRemnant(i: number, list: FileList | null) {
    if (!list?.length) return;
    setError(null); setResult(null); setBusy('Importing sheet outline…');
    try {
      const result = await importSheet(await readDrawingFile(list[0]), closeGaps ? gapLimit : undefined,
        { dxfUnitMm: importChoices[list[0].name]?.dxfUnitMm });
      if (result.outlines.length !== 1) throw new Error(`${list[0].name} contains ${result.outlines.length} separate sheet outlines. Import it as a drawing and choose its sheet outline by name, or save the desired outline in a separate file.`);
      useSheetOutline(i, result.outlines[0]);
      setSheetMessages([`Sheet size ${i + 1}: ${result.outlines[0].source}, moved to the sheet origin.`, ...result.warnings]);
    } catch (e) {
      setError(`${String(e)}. Sheet size ${i + 1} was not changed.`);
    } finally { setBusy(null); }
  }

  async function run(lib: Library | null = library, req: NestRequest = request, budget = seconds) {
    if (!lib) return;
    setError(null);
    setResult(null);
    setBusy('Nesting…');
    const started = performance.now();
    let best: number | null = null;
    // The best layout any worker has shown so far, drawn at most four times a second.
    let shown: { layout: Layout; material: number } | null = null;
    const tick = setInterval(() => {
      setProgress({ elapsed: (performance.now() - started) / 1000, best });
      setLive(shown);
    }, 250);
    setRunSeconds(budget);
    setLive(null);
    portfolio.current = new Portfolio();
    try {
      const r = await portfolio.current.run(lib, req, { seconds: budget, seed, workers: workersFor(req, workers), repeatable, live: 0.5 },
        (_w, _t, material, layout) => {
          if (best === null || material < best) best = material;
          if (layout && (!shown || material <= shown.material)) shown = { layout, material };
        });
      setResult(r);
    } catch (e) {
      if (String(e).includes('cancelled')) setError('Cancelled.');
      else setError(String(e));
    } finally {
      clearInterval(tick);
      portfolio.current = null;
      setBusy(null);
      setLive(null);
      setProgress({ elapsed: 0, best: null });
    }
  }

  function cancel() { portfolio.current?.stop(); }

  /** A bundled example drawing (web/public/examples, see its LICENSES.txt), nested at once. */
  async function tryExample(example: Example) {
    setError(null);
    const [w, h] = example.sheet;
    const sheet = blankSheet(w, h);
    sheet.margins_mm = { left: example.margin, right: example.margin, bottom: example.margin, top: example.margin };
    // The example's sheet first, so the loading skeleton already has its shape.
    setRequest({ ...emptyRequest(), sheets: [sheet] });
    setBusy('Importing…');
    try {
      const text = await (await fetch(`./examples/${example.file}`)).text();
      const lib = await importFiles([{ name: example.file, text }]);
      const element = (p: LibraryPart) => p.source.split('#')[1]?.split(':')[0] ?? '';
      const req: NestRequest = {
        ...emptyRequest(),
        parts: lib.parts.map((p) => ({ id: p.id, quantity: example.quantities[element(p)] ?? example.default_quantity ?? 1,
          rotations: example.overrides?.[element(p)] ?? example.rotations, allow_mirror: false, priority: 1 })),
        sheets: [sheet], spacing_mm: example.spacing, edge_spacing_mm: example.edge,
      };
      setName(`Example: ${example.title}`);
      setLibrary(lib);
      setRequest(req);
      setResult(null);
      setBusy(null);
      setSeconds(example.seconds);
      await run(lib, req, example.seconds);
    } catch (e) {
      setError(String(e));
      setBusy(null);
    }
  }

  const project = (): Project => ({ lightburnOutline, version: 1, name, library, request, result, savedAt: new Date().toISOString() });

  function open(p: Project) {
    setLightburnOutline(p.lightburnOutline ?? true);
    setLastFiles([]);
    setImportChoices({}); setImportInventory([]);
    setSheetMessages([]);
    setCloseGaps(false);
    setGapLimit(0.05);
    setName(p.name);
    setLibrary(p.library);
    setRequest(p.request);
    setResult(p.result);
    setError(null);
  }

  async function exportsFor(r: NestResult) {
    if (!library) return [];
    const files: { name: string; data: string }[] = [];
    for (const sheet of r.layout.sheets) {
      for (const format of (library.lightburn ? ['lbrn2'] : ['svg', 'dxf']) as ('svg' | 'dxf' | 'lbrn2')[]) {
        files.push({ name: `sheets/${exportFilename(library, r.layout, sheet.id, format)}`, data: await exportSheet(library, request, r.layout, sheet.id, format, library.lightburn ? lightburnOutline : false) });
      }
    }
    return files;
  }

  async function saveZip() {
    const files: { name: string; data: string }[] = [{ name: 'project.json', data: JSON.stringify(project(), null, 1) }];
    if (result) {
      files.push({ name: 'layout.json', data: JSON.stringify(result.layout, null, 1) });
      files.push(...(await exportsFor(result)));
    }
    download(`${name.replace(/[^\w.-]+/g, '_') || 'nestbolt'}.zip`, zip(files), 'application/zip');
  }

  async function openZip(list: FileList | null) {
    if (!list?.length) return;
    try {
      const entries = unzip(new Uint8Array(await list[0].arrayBuffer()));
      const json = entries.get('project.json');
      if (!json) throw new Error('this ZIP has no project.json');
      open(JSON.parse(new TextDecoder().decode(json)));
    } catch (e) {
      setError(String(e));
    }
  }

  const guarded = (work: () => Promise<void>) => () => { work().catch((e) => setError(String(e))); };

  const metrics = result?.validation.metrics;
  const commonValid = !request.common_line || (!library?.lightburn && Number.isFinite(request.common_line.kerf_mm) && request.common_line.kerf_mm >= 0.05);
  const canRun = !!library && request.parts.length > 0 && request.sheets.length > 0 && !busy && commonValid;

  return (
    <div class="app">
      <header>
        <h1>Nestbolt</h1>
        <input class="name" aria-label="Project name" value={name} onInput={(e) => setName((e.target as HTMLInputElement).value)} />
        <button onClick={async () => { await saveProject(project()); setProjects(await listProjects()); }}>Save</button>
        <select aria-label="Open saved project" value="" onChange={async (e) => {
          const n = (e.target as HTMLSelectElement).value;
          const p = n && (await loadProject(n));
          if (p) open(p);
        }}>
          <option value="">Open saved…</option>
          {projects.map((p) => <option key={p.name} value={p.name}>{p.name}</option>)}
        </select>
        <button onClick={async () => { await deleteProject(name); setProjects(await listProjects()); }} disabled={!projects.some((p) => p.name === name)}>Delete</button>
        <button onClick={guarded(saveZip)}>Project ZIP</button>
        <button onClick={() => zipInput.current?.click()}>Open ZIP</button>
        <input ref={zipInput} type="file" accept=".zip" hidden onChange={(e) => openZip((e.target as HTMLInputElement).files)} />
        <button onClick={() => open({ version: 1, name: 'Untitled project', library: null, request: emptyRequest(), result: null, savedAt: '' })}>New</button>
      </header>
      <p class="privacy">Free, open-source nesting for laser, CNC and other sheet cutting. Everything runs in this browser; files are never uploaded.</p>
      <main>
        <aside>
          <section aria-labelledby="parts-title">
            <h2 id="parts-title">Parts</h2>
            <label class="drop"
              onDragOver={(e) => e.preventDefault()}
              onDrop={(e) => { e.preventDefault(); onFiles(e.dataTransfer?.files ?? null); }}>
              <input type="file" accept=".svg,.dxf,.lbrn,.lbrn2" multiple onChange={(e) => onFiles((e.target as HTMLInputElement).files)} />
              <span>Import SVG, DXF or LightBurn (or drop files here)</span>
            </label>
            {!library?.lightburn ? <div class="import-options">
              <label><input type="checkbox" checked={closeGaps} disabled={!!busy}
                onChange={(e) => setCloseGaps((e.target as HTMLInputElement).checked)} /> Close larger gaps</label>
              {closeGaps ? <label>Close gaps up to (mm)<input type="number" min={0} max={1} step={0.005}
                value={gapLimit} disabled={!!busy} onInput={(e) => setGapLimit(num(e))} /></label> : null}
              <p class="hint">Gaps up to 0.005 mm join automatically. Larger repairs are listed with their positions.</p>
              {importInventory.map(({ file, report }) => <details open key={file} class="import-channels">
                <summary>Layers and colours — {file}</summary>
                {report.units && !report.units.declared ? <label>DXF units when missing — {file}
                  <select value={importChoices[file]?.dxfUnitMm ?? 1} disabled={!!busy}
                    onChange={(e) => setImportChoices((current) => ({ ...current, [file]: { ...current[file], dxfUnitMm: num(e) } }))}>
                    <option value={1}>Millimetres</option><option value={25.4}>Inches</option><option value={10}>Centimetres</option>
                  </select></label> : report.units ? <p class="hint">File units: {report.units.mm_per_unit} mm per drawing unit.</p> : null}
                {report.cleanup ? <p class="hint">Cleanup: {report.cleanup.duplicate_segments_removed} duplicate segments removed; {report.cleanup.zero_length_segments_removed} zero-length segments removed; {report.cleanup.overlapping_segments_merged} collinear overlaps merged.</p> : null}
                <p class="hint">Automatic selection prefers cut, outline and profile layers. Tick a choice to set a filter; layer and colour filters apply together. Counts include ignored entities.</p>
                {(['layers', 'colors'] as const).map((kind) => <fieldset>
                  <legend>{kind === 'layers' ? 'Cut layers' : 'Cut colours'}{importChoices[file]?.[kind] === undefined ? ' (automatic)' : ''}</legend>
                  {(report[kind] ?? []).map((entry) => <label key={entry.name}>
                    <input type="checkbox" disabled={!!busy} aria-label={`${kind === 'layers' ? 'Layer' : 'Colour'} ${entry.name} in ${file}`}
                      checked={importChoices[file]?.[kind]?.includes(entry.name) ?? entry.selected_entities > 0}
                      onChange={(e) => {
                        const checked = (e.target as HTMLInputElement).checked;
                        const before = importChoices[file]?.[kind] ?? (report[kind] ?? []).filter((c) => c.selected_entities > 0).map((c) => c.name);
                        const values = checked ? [...new Set([...before, entry.name])] : before.filter((v) => v !== entry.name);
                        setImportChoices((current) => ({ ...current, [file]: { ...current[file], [kind]: values } }));
                      }} /> {entry.name} <small>{entry.entities} entities · {entry.selected_entities} selected outlines/paths</small>
                  </label>)}
                </fieldset>)}
                <fieldset>
                  <legend>Sheet outline layers{importChoices[file]?.sheetLayers === undefined ? ' (automatic SHEET)' : ''}</legend>
                  {(report.layers ?? []).filter((entry) => entry.geometry_entities > 0).map((entry) => <label key={entry.name}>
                    <input type="checkbox" disabled={!!busy} aria-label={`Sheet layer ${entry.name} in ${file}`}
                      checked={importChoices[file]?.sheetLayers?.includes(entry.name) ?? entry.name.toUpperCase() === 'SHEET'}
                      onChange={(e) => {
                        const before = importChoices[file]?.sheetLayers ?? (report.layers ?? []).filter((l) => l.name.toUpperCase() === 'SHEET').map((l) => l.name);
                        const values = (e.target as HTMLInputElement).checked ? [...new Set([...before, entry.name])] : before.filter((v) => v !== entry.name);
                        setImportChoices((current) => ({ ...current, [file]: { ...current[file], sheetLayers: values } }));
                      }} /> {entry.name}
                  </label>)}
                </fieldset>
                <button disabled={!!busy} onClick={() => setImportChoices((current) => ({ ...current, [file]: { dxfUnitMm: current[file]?.dxfUnitMm } }))}>Use automatic selection for {file}</button>
              </details>)}
              {lastFiles.length ? <button disabled={!!busy} onClick={() => importDrawings(lastFiles)}>Apply import options</button> : null}
            </div> : null}
            {!library && examples.length ? (
              <div class="examples">
                <p>Or try an example:</p>
                {examples.map((e) => (
                  <button key={e.id} class="example" onClick={() => tryExample(e)} disabled={!!busy} title={e.summary}
                    aria-label={`Try an example: ${e.title}`}>
                    <strong>{e.title[0].toUpperCase() + e.title.slice(1)}</strong><small>{e.summary}</small>
                  </button>
                ))}
              </div>
            ) : null}
            {library?.lightburn ? <details open class="import-channels">
              <summary>LightBurn layers — preserved</summary>
              <p class="hint">Groups stay together. Preview shows the space each unit occupies; exported projects retain editable artwork and settings.</p>
              <table class="lightburn-layers"><thead><tr><th>Layer</th><th>Mode</th><th>Output</th><th>Kerf (mm)</th></tr></thead>
                <tbody>{library.lightburn.layers.map(l => <tr key={`${l.image}-${l.index}`}>
                  <td>{l.image ? 'Image' : 'Layer'} {l.index}{l.name ? `: ${l.name}` : ''}</td><td>{l.mode || (l.image ? 'Image' : '—')}</td><td>{l.output ? 'On' : 'Off'}</td><td>{l.kerf_mm}</td>
                </tr>)}</tbody></table>
              <label><input type="checkbox" checked={lightburnOutline} onChange={e => setLightburnOutline((e.target as HTMLInputElement).checked)} />Include sheet outline on T1</label>
            </details> : null}
            {library?.warnings.length ? <ul class="warnings">{library.warnings.slice(0, 5).map((w) => <li>{w}</li>)}</ul> : null}
            {(library?.warnings.length ?? 0) > 5 ? <details><summary>Show all import messages ({library!.warnings.length})</summary>
              <ul class="warnings">{library!.warnings.map((w) => <li>{w}</li>)}</ul></details> : null}
            <table class="parts">
              <thead><tr><th></th><th>Part</th><th>Qty</th><th>Rotation</th><th title="Allow mirroring">Mirror</th>{request.mode === 'fill_priority' ? <th>Priority</th> : null}<th></th></tr></thead>
              <tbody>
                {request.parts.map((p, i) => {
                  const lp = part(p.id);
                  return (
                    <tr key={p.id}>
                      <td>{lp ? <PartThumb polygons={partGeometry(lp)} color={colors.get(p.id) ?? '#888'} /> : null}</td>
                      <td title={lp?.source}>{label(p.id)}<small>{lp ? `${(lp.area_mm2 / 100).toFixed(1)} cm²` : ''}</small></td>
                      <td><input type="number" min={1} max={2000} value={p.quantity} aria-label={`Quantity of ${p.id}`}
                        onInput={(e) => updatePart(i, { quantity: Math.max(1, Math.round(num(e))) })} /></td>
                      <td><select aria-label={`Rotations of ${p.id}`} value={rotationLabel(p.rotations)}
                        onChange={(e) => updatePart(i, { rotations: ROTATIONS.find((o) => o.label === (e.target as HTMLSelectElement).value)!.value })}>
                        {ROTATIONS.map((o) => <option key={o.label}>{o.label}</option>)}
                      </select></td>
                      <td><input type="checkbox" checked={p.allow_mirror} aria-label={`Allow mirroring ${p.id}`}
                        onChange={(e) => updatePart(i, { allow_mirror: (e.target as HTMLInputElement).checked })} /></td>
                      {request.mode === 'fill_priority' ? <td><input type="number" min={0} value={p.priority}
                        onInput={(e) => updatePart(i, { priority: num(e) })} /></td> : null}
                      <td><button class="icon" aria-label={`Remove ${p.id}`} onClick={() => update({ parts: request.parts.filter((_, j) => j !== i) })}>×</button></td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
            {busy === 'Importing…' && !request.parts.length
              ? <div class="parts-loading" aria-hidden="true">{[0, 1, 2].map((k) => <div key={k} class="skeleton line" />)}</div>
              : null}
          </section>
          <section aria-labelledby="sheets-title">
            <h2 id="sheets-title">Sheets</h2>
            {sheetMessages.length ? <ul class="sheet-messages">{sheetMessages.map((message) => <li>{message}</li>)}</ul> : null}
            {request.sheets.map((s, i) => (
              <fieldset key={i} class="sheet-row">
                <legend>Sheet size {i + 1}</legend>
                <label>Width <input type="number" min={1} value={s.width_mm} onInput={(e) => updateSheet(i, { width_mm: num(e) })} /> mm</label>
                <label>Height <input type="number" min={1} value={s.height_mm} onInput={(e) => updateSheet(i, { height_mm: num(e) })} /> mm</label>
                <label>Count <input type="number" min={1} placeholder="∞" value={s.count ?? ''}
                  onInput={(e) => updateSheet(i, { count: (e.target as HTMLInputElement).value ? Math.max(1, num(e)) : null })} /></label>
                <label>Margin <input type="number" min={0} value={s.margins_mm.left}
                  onInput={(e) => { const m = num(e); updateSheet(i, { margins_mm: { left: m, right: m, top: m, bottom: m } }); }} /> mm</label>
                {s.outline_mm?.length ? (
                  <span class="remnant">Remnant outline
                    <button class="icon" aria-label={`Use the full rectangle for sheet size ${i + 1}`}
                      onClick={() => updateSheet(i, { outline_mm: [], outline_tolerance_mm: 0, from_import: undefined })}>×</button></span>
                ) : (
                  <label class="remnant">Remnant outline <input type="file" accept=".svg,.dxf" aria-label={`Remnant outline for sheet size ${i + 1}`}
                    disabled={!!busy} onChange={(e) => onRemnant(i, (e.target as HTMLInputElement).files)} /></label>
                )}
                {library?.sheet_outlines?.length ? <label>Imported sheet outline
                  <select aria-label={`Imported sheet outline for sheet size ${i + 1}`} value="" disabled={!!busy}
                    onChange={(e) => {
                      const outline = library.sheet_outlines?.find((s) => s.id === (e.target as HTMLSelectElement).value);
                      if (outline) useSheetOutline(i, outline);
                    }}>
                    <option value="">Choose an outline…</option>
                    {library.sheet_outlines.map((o) => <option value={o.id}>{o.id} — {o.width_mm} × {o.height_mm} mm</option>)}
                  </select></label> : null}
                <details>
                  <summary>Defects ({s.defects_mm.length})</summary>
                  {s.defects_mm.map((d, k) => {
                    const xs = d.outer.map((p) => p[0]); const ys = d.outer.map((p) => p[1]);
                    return <div key={k} class="defect-row">{`${Math.min(...xs)}, ${Math.min(...ys)} → ${Math.max(...xs)}, ${Math.max(...ys)} mm`}
                      <button class="icon" aria-label="Remove defect" onClick={() => updateSheet(i, { defects_mm: s.defects_mm.filter((_, j) => j !== k) })}>×</button></div>;
                  })}
                  <form class="defect-form" onSubmit={(e) => {
                    e.preventDefault();
                    const f = new FormData(e.target as HTMLFormElement);
                    const [x, y, w, h] = ['x', 'y', 'w', 'h'].map((k) => Number(f.get(k)));
                    if (w > 0 && h > 0) updateSheet(i, { defects_mm: [...s.defects_mm, { outer: [[x, y], [x + w, y], [x + w, y + h], [x, y + h]], holes: [] }] });
                  }}>
                    {['x', 'y', 'w', 'h'].map((k) => <input key={k} name={k} type="number" placeholder={k} aria-label={`Defect ${k}`} />)}
                    <button type="submit">Add defect</button>
                  </form>
                </details>
                {request.sheets.length > 1 ? <button class="icon" aria-label={`Remove sheet size ${i + 1}`} onClick={() => update({ sheets: request.sheets.filter((_, j) => j !== i) })}>×</button> : null}
              </fieldset>
            ))}
            <select aria-label="Add a sheet size" value="" onChange={(e) => {
              const preset = PRESETS.find((p) => p.label === (e.target as HTMLSelectElement).value);
              if (preset) update({ sheets: [...request.sheets, blankSheet(preset.w, preset.h)] });
            }}>
              <option value="">Add sheet size…</option>
              {PRESETS.map((p) => <option key={p.label}>{p.label}</option>)}
            </select>
          </section>
          <section aria-labelledby="settings-title">
            <h2 id="settings-title">Settings</h2>
            <div class="grid">
              <label>Part spacing <input type="number" min={0} step={0.1} disabled={!!request.common_line} value={request.common_line?.kerf_mm ?? request.spacing_mm} onInput={(e) => update({ spacing_mm: num(e) })} /> mm</label>
              <label>Edge spacing <input type="number" min={0} step={0.1} value={request.edge_spacing_mm} onInput={(e) => update({ edge_spacing_mm: num(e) })} /> mm</label>
              <label>Goal <select value={request.mode} onChange={(e) => update({ mode: (e.target as HTMLSelectElement).value as Mode })}>
                <option value="all">Place every part</option>
                <option value="fill_area">Fill the sheets (most area)</option>
                <option value="fill_priority">Fill by priority</option>
              </select></label>
              <label>Time <input type="number" min={1} max={300} value={seconds} onInput={(e) => setSeconds(Math.min(300, Math.max(1, num(e))))} /> s</label>
            </div>
            <label class="check"><input type="checkbox" disabled={!!library?.lightburn && !request.common_line} checked={!!request.common_line} onChange={(e) => update({ common_line: (e.target as HTMLInputElement).checked ? { kerf_mm: 0 } : undefined })} /> Common-line cutting</label>
            {request.common_line ? <>
              <label>Kerf <input type="number" min={0.05} step={0.05} required value={request.common_line.kerf_mm} onInput={(e) => update({ common_line: { kerf_mm: num(e) } })} /> mm</label>
              <p class="hint">Enter the cut width (at least 0.05 mm). Part spacing uses this kerf; parts stay outside holes. Shared straight cuts go on COMMON with compensation included.</p>
              <p class="hint">CUT keeps the closed outlines. In CAM, replace their shared sections with COMMON and turn off kerf compensation for COMMON.</p>
            </> : null}
            {library?.lightburn ? <p class="hint">For common-line cutting, export the cut outlines from LightBurn as SVG or DXF and import them here.</p> : null}
            <details class="advanced">
              <summary>Advanced</summary>
              <div class="grid">
                <label title={`Jobs of more than ${LARGE_JOB} parts use at most two workers, to limit memory`}>Workers <input type="number" min={1} max={cores} value={workers} onInput={(e) => setWorkers(Math.min(cores, Math.max(1, num(e))))} /></label>
                <label>Seed <input type="number" min={0} value={seed} onInput={(e) => setSeed(Math.max(0, Math.round(num(e))))} /></label>
                <label class="check"><input type="checkbox" checked={repeatable} onChange={(e) => setRepeatable((e.target as HTMLInputElement).checked)} /> Repeatable</label>
              </div>
            </details>
          </section>
          <div class="run">
            {busy === 'Nesting…' ? (
              <>
                <progress max={runSeconds} value={progress.elapsed} aria-label="Search progress" />
                <span>{progress.best !== null ? `best ${progress.best.toFixed(3)} sheets` : 'searching…'}</span>
                <button onClick={cancel}>Cancel</button>
              </>
            ) : <button class="primary" disabled={!canRun} onClick={() => run()}>Nest</button>}
          </div>
          {error ? <p class="error" role="alert">{error}</p> : null}
        </aside>
        <section class="results" aria-labelledby="results-title">
          <h2 id="results-title">Result</h2>
          {busy && !(busy === 'Nesting…' && live) ? (
            <Pending sheet={request.sheets[0]} label={busy !== 'Nesting…'
              ? (busy === 'Importing…' ? 'Reading the drawing…' : busy)
              : progress.elapsed < 1 ? 'Starting the search…' : `Finding a first layout… ${progress.elapsed.toFixed(0)} s`} />
          ) : null}
          {busy === 'Nesting…' && live && library ? (
            <div class="live" aria-live="off">
              <p class="hint">Best layout so far ({live.material.toFixed(3)} sheets), updated while the search runs.</p>
              <div class="sheets">
                {live.layout.sheets.map((s) => (
                  <figure key={s.id}><SheetCanvas library={library} request={request} layout={live.layout} sheet={s.id} /></figure>
                ))}
              </div>
            </div>
          ) : null}
          {!result && !busy ? <p class="hint">Import parts, choose sheets and press Nest, or try the example boxes.</p> : null}
          {result && library && metrics ? (
            <>
              <dl class="summary">
                <div><dt>Sheets</dt><dd>{metrics.sheets_used}</dd></div>
                <div><dt>Material</dt><dd>{metrics.normalized_material.toFixed(3)}</dd></div>
                <div><dt>Utilisation</dt><dd>{(metrics.utilization * 100).toFixed(1)}%</dd></div>
                <div><dt>Placed</dt><dd>{metrics.placed_parts}/{metrics.requested_parts}</dd></div>
                <div><dt>Check</dt><dd>{result.validation.valid ? 'valid' : 'invalid'}</dd></div>
                {result.parts_in_holes ? <div><dt>In holes</dt><dd>{result.parts_in_holes}</dd></div> : null}
              </dl>
              {result.common_line?.length ? <div class="common-line-report">
                <h3>Common-line cuts</h3>
                {result.common_line.map((r) => <p key={r.sheet_id}>{r.sheet_id}: {r.cut_length_without_common_mm.toFixed(1)} → {r.cut_length_with_common_mm.toFixed(1)} mm of cutting; {r.saved_length_mm.toFixed(1)} mm saved ({(100 * r.saved_fraction).toFixed(1)}%). {r.contours_without_common} closed contours become {r.paths_with_common} cutting paths after replacing the shared sections.</p>)}
              </div> : null}
              <button onClick={guarded(async () => download('sheets.zip', zip(await exportsFor(result)), 'application/zip'))}>Download all sheets (ZIP)</button>
              <div class="sheets">
                {result.layout.sheets.map((s) => (
                  <figure key={s.id}>
                    <SheetPreview library={library} request={request} layout={result.layout} sheet={s.id} />
                    <figcaption>
                      {s.id}
                      {(() => {
                        const u = sheetUsage(library, request, result.layout, s.id);
                        return u && u.offcut > 0.01 * u.height
                          ? <span class="usage" title="Clear material above the placed parts">offcut {u.width.toFixed(0)} × {u.offcut.toFixed(0)} mm</span>
                          : null;
                      })()}
                      {library.lightburn ? <button onClick={guarded(async () => download(exportFilename(library, result.layout, s.id, 'lbrn2'), await exportSheet(library, request, result.layout, s.id, 'lbrn2', lightburnOutline), 'application/xml'))}>LightBurn</button> : <>
                        <button onClick={guarded(async () => download(`${s.id}.svg`, await exportSheet(library, request, result.layout, s.id, 'svg'), 'image/svg+xml'))}>SVG</button>
                        <button onClick={guarded(async () => download(`${s.id}.dxf`, await exportSheet(library, request, result.layout, s.id, 'dxf'), 'application/dxf'))}>DXF</button>
                      </>}
                    </figcaption>
                  </figure>
                ))}
              </div>
            </>
          ) : null}
        </section>
      </main>
      <footer>
        Built on <a href="https://github.com/JeroenGar/jagua-rs">jagua-rs</a> and <a href="https://github.com/JeroenGar/sparrow">sparrow</a> by Jeroen Gardeyn et al. MIT licensed;{' '}
        <a href="./THIRD_PARTY_NOTICES.txt">third-party notices</a>. <a href="./results/">Benchmark results</a> against Deepnest, SVGnest and Sparrow.
      </footer>
    </div>
  );
}
