import { useEffect, useMemo, useRef, useState } from 'preact/hooks';
import { exportSheet, importFiles, Portfolio } from './engine';
import { SheetCanvas } from './canvas';
import { PALETTE, PartThumb, SheetPreview, sheetUsage } from './preview';
import { deleteProject, listProjects, loadProject, saveProject } from './storage';
import type { Example, Layout, Library, LibraryPart, Mode, NestRequest, NestResult, Point, Project, RequestPart, RequestSheet, Rotations } from './types';
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

  async function onFiles(list: FileList | null) {
    if (!list?.length) return;
    setError(null);
    setBusy('Importing…');
    try {
      const files = await Promise.all([...list].map(async (f) => ({ name: f.name, text: await f.text() })));
      // Part ids are `<file stem>-<n>`: importing a file again replaces its parts.
      const merged = await importFiles(files);
      const parts = [...(library?.parts ?? []).filter((p) => !merged.parts.some((q) => q.id === p.id)), ...merged.parts];
      const next: Library = { version: 1, tolerance: merged.tolerance, parts, warnings: [...(library?.warnings ?? []), ...merged.warnings] };
      setLibrary(next);
      update({
        parts: [
          ...request.parts.filter((p) => !merged.parts.some((q) => q.id === p.id)),
          ...merged.parts.map((p) => ({ id: p.id, quantity: 1, rotations: ROTATIONS[0].value, allow_mirror: false, priority: 1 })),
        ],
      });
    } catch (e) {
      setError(String(e));
    } finally {
      setBusy(null);
    }
  }

  /** Use the largest closed outline of a drawing as a remnant sheet, moved to the origin. */
  async function onRemnant(i: number, list: FileList | null) {
    if (!list?.length) return;
    setError(null);
    try {
      const lib = await importFiles([{ name: list[0].name, text: await list[0].text() }]);
      const largest = lib.parts.reduce<LibraryPart | null>((a, b) => (!a || b.area_mm2 > a.area_mm2 ? b : a), null);
      if (!largest) throw new Error(`${list[0].name} has no closed outline to use as a remnant`);
      const [x0, y0, x1, y1] = largest.bounds_mm;
      const move = (ring: Point[]): Point[] => ring.map(([x, y]) => [x - x0, y - y0]);
      updateSheet(i, {
        width_mm: x1 - x0, height_mm: y1 - y0,
        outline_mm: [{ outer: move(largest.polygon.outer), holes: largest.polygon.holes.map(move) }],
      });
    } catch (e) {
      setError(String(e));
    }
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

  const project = (): Project => ({ version: 1, name, library, request, result, savedAt: new Date().toISOString() });

  function open(p: Project) {
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
      for (const format of ['svg', 'dxf'] as const) {
        files.push({ name: `sheets/${sheet.id}.${format}`, data: await exportSheet(library, request, r.layout, sheet.id, format) });
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
  const canRun = !!library && request.parts.length > 0 && request.sheets.length > 0 && !busy;

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
              <input type="file" accept=".svg,.dxf" multiple onChange={(e) => onFiles((e.target as HTMLInputElement).files)} />
              <span>Import SVG or DXF (or drop files here)</span>
            </label>
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
            {library?.warnings.length ? <ul class="warnings">{library.warnings.slice(0, 5).map((w) => <li>{w}</li>)}</ul> : null}
            <table class="parts">
              <thead><tr><th></th><th>Part</th><th>Qty</th><th>Rotation</th><th title="Allow mirroring">Mirror</th>{request.mode === 'fill_priority' ? <th>Priority</th> : null}<th></th></tr></thead>
              <tbody>
                {request.parts.map((p, i) => {
                  const lp = part(p.id);
                  return (
                    <tr key={p.id}>
                      <td>{lp ? <PartThumb polygon={lp.polygon} color={colors.get(p.id) ?? '#888'} /> : null}</td>
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
                      onClick={() => updateSheet(i, { outline_mm: [] })}>×</button></span>
                ) : (
                  <label class="remnant">Remnant outline <input type="file" accept=".svg,.dxf" aria-label={`Remnant outline for sheet size ${i + 1}`}
                    onChange={(e) => onRemnant(i, (e.target as HTMLInputElement).files)} /></label>
                )}
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
              <label>Part spacing <input type="number" min={0} step={0.1} value={request.spacing_mm} onInput={(e) => update({ spacing_mm: num(e) })} /> mm</label>
              <label>Edge spacing <input type="number" min={0} step={0.1} value={request.edge_spacing_mm} onInput={(e) => update({ edge_spacing_mm: num(e) })} /> mm</label>
              <label>Goal <select value={request.mode} onChange={(e) => update({ mode: (e.target as HTMLSelectElement).value as Mode })}>
                <option value="all">Place every part</option>
                <option value="fill_area">Fill the sheets (most area)</option>
                <option value="fill_priority">Fill by priority</option>
              </select></label>
              <label>Time <input type="number" min={1} max={300} value={seconds} onInput={(e) => setSeconds(Math.min(300, Math.max(1, num(e))))} /> s</label>
            </div>
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
                      <button onClick={guarded(async () => download(`${s.id}.svg`, await exportSheet(library, request, result.layout, s.id, 'svg'), 'image/svg+xml'))}>SVG</button>
                      <button onClick={guarded(async () => download(`${s.id}.dxf`, await exportSheet(library, request, result.layout, s.id, 'dxf'), 'application/dxf'))}>DXF</button>
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
