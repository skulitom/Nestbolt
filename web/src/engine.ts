import type { ImportSelection, Layout, Library, NestRequest, NestResult, Report, SheetImport } from './types';
import { betterResult } from './scoring';

type Progress = (t: number, material: number, layout?: Layout) => void;
type Pending = { resolve: (v: string) => void; reject: (e: Error) => void; progress?: Progress };

/** A Web Worker running the WebAssembly engine, addressed by request ids. */
class EngineWorker {
  private worker = new Worker(new URL('./worker.ts', import.meta.url), { type: 'module' });
  private pending = new Map<number, Pending>();
  private next = 0;
  /** Linear memory of this worker's engine after its last finished request. */
  memory = 0;

  constructor() {
    this.worker.onmessage = (event) => {
      const { id, type } = event.data;
      const p = this.pending.get(id);
      if (!p) return;
      if (type === 'progress') {
        p.progress?.(event.data.t, event.data.material, event.data.layout ? JSON.parse(event.data.layout) : undefined);
      }
      else {
        this.pending.delete(id);
        this.memory = event.data.memory ?? this.memory;
        if (type === 'done') p.resolve(event.data.value);
        else p.reject(new Error(event.data.message));
      }
    };
    this.worker.onerror = (event) => {
      for (const p of this.pending.values()) p.reject(new Error(event.message || 'engine worker failed'));
      this.pending.clear();
    };
  }

  call(type: string, args: unknown, progress?: Progress): Promise<string> {
    const id = this.next++;
    return new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject, progress });
      this.worker.postMessage({ id, type, args });
    });
  }

  terminate() {
    this.worker.terminate();
    for (const p of this.pending.values()) p.reject(new Error('cancelled'));
    this.pending.clear();
  }
}

let utility: EngineWorker | null = null;
const tool = () => (utility ??= new EngineWorker());

export async function importFiles(files: { name: string; text: string }[], tolerance = 0, closeGapsMm?: number, selection: ImportSelection = {}): Promise<Library> {
  return JSON.parse(await tool().call('import', { files, tolerance, closeGapsMm, ...selection }));
}

export async function inspectFiles(files: { name: string; text: string }[]): Promise<NonNullable<Library['imports']>> {
  return JSON.parse(await tool().call('inspect', { files }));
}

export async function importSheet(file: { name: string; text: string }, closeGapsMm?: number, selection: ImportSelection = {}): Promise<SheetImport> {
  return JSON.parse(await tool().call('import_sheet', { file, closeGapsMm, ...selection }));
}

export async function readDrawingFile(file: File): Promise<{ name: string; text: string }> {
  const text = await tool().call('decode', { name: file.name, bytes: new Uint8Array(await file.arrayBuffer()) });
  return { name: file.name, text };
}

export async function validate(library: Library, request: NestRequest, layout: unknown): Promise<Report> {
  return JSON.parse(await tool().call('validate', {
    library: JSON.stringify(library), request: JSON.stringify(request), layout: JSON.stringify(layout) }));
}

export async function exportSheet(library: Library, request: NestRequest, layout: unknown, sheet: string,
  format: 'svg' | 'dxf' | 'lbrn2', outline = format === 'lbrn2'): Promise<string> {
  return tool().call('export', { library: JSON.stringify(library), request: JSON.stringify(request),
    layout: JSON.stringify(layout), sheet, format, outline });
}

export async function estimate(library: Library, request: NestRequest): Promise<{ sheets_lower_bound: number }> {
  return JSON.parse(await tool().call('estimate', { library: JSON.stringify(library), request: JSON.stringify(request) }));
}

/** Benchmark run of a polygon job in its own worker, the same search as `nestbolt sheets`. */
export async function nestJob(job: string, seconds: number, seed: number, repeatable = false) {
  const worker = new EngineWorker();
  try {
    const value = await worker.call('nest_job', { job, seconds, seed, repeatable });
    return { result: JSON.parse(value), memoryBytes: worker.memory };
  } finally {
    worker.terminate();
  }
}

/** Run independent searches (seeds seed, seed+1, ...) and keep the best valid one. */
export class Portfolio {
  private workers: EngineWorker[] = [];

  async run(library: Library, request: NestRequest,
    options: { seconds: number; seed: number; workers: number; repeatable: boolean; live?: number },
    onProgress: (worker: number, t: number, material: number, layout?: Layout) => void): Promise<NestResult> {
    this.workers = Array.from({ length: Math.max(1, options.workers) }, () => new EngineWorker());
    const lib = JSON.stringify(library);
    const req = JSON.stringify(request);
    const runs = this.workers.map((w, i) =>
      w.call('nest', { library: lib, request: req, seconds: options.seconds, seed: options.seed + i, repeatable: options.repeatable,
        live: options.live ?? 0 }, (t, m, layout) => onProgress(i, t, m, layout)).then((v) => JSON.parse(v) as NestResult));
    const settled = await Promise.allSettled(runs);
    this.stop();
    const ok = settled.flatMap((s) => (s.status === 'fulfilled' && s.value.validation.valid ? [s.value] : []));
    if (!ok.length) {
      const failure = settled.find((s) => s.status === 'rejected') as PromiseRejectedResult | undefined;
      throw failure?.reason ?? new Error('no valid layout');
    }
    return ok.reduce((a, b) => betterResult(b, a, request.mode) ? b : a);
  }

  stop() {
    for (const w of this.workers) w.terminate();
    this.workers = [];
  }
}

/** Same source-stem and sheet-order naming as the native preserving exporter. */
export function exportFilename(library: Library, layout: Layout, sheet: string, format: 'svg' | 'dxf' | 'lbrn2'): string {
  if (!library.lightburn) return `${sheet}.${format}`;
  const basename = library.lightburn.file.split(/[\\/]/).pop() || 'project';
  const stem = basename.replace(/\.[^.]*$/, '');
  const safe = Array.from(stem).map(c => /[a-zA-Z0-9_-]/.test(c) ? c : '-').join('');
  return `${safe}-sheet-${layout.sheets.findIndex(s => s.id === sheet) + 1}${format === 'lbrn2' ? '' : '-cuts'}.${format}`;
}
