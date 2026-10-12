import type { Layout, Library, NestRequest, NestResult, Report } from './types';

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

export async function importFiles(files: { name: string; text: string }[], tolerance = 0): Promise<Library> {
  return JSON.parse(await tool().call('import', { files, tolerance }));
}

export async function validate(library: Library, request: NestRequest, layout: unknown): Promise<Report> {
  return JSON.parse(await tool().call('validate', {
    library: JSON.stringify(library), request: JSON.stringify(request), layout: JSON.stringify(layout) }));
}

export async function exportSheet(library: Library, request: NestRequest, layout: unknown, sheet: string,
  format: 'svg' | 'dxf', outline = false): Promise<string> {
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

const key = (r: NestResult): [number, number] => {
  const m = r.validation.metrics;
  return m ? [m.sheets_used, m.material_area] : [Infinity, Infinity];
};

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
    return ok.reduce((a, b) => {
      const [ka, kb] = [key(a), key(b)];
      return kb[0] < ka[0] || (kb[0] === ka[0] && kb[1] < ka[1]) ? b : a;
    });
  }

  stop() {
    for (const w of this.workers) w.terminate();
    this.workers = [];
  }
}
