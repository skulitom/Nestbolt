// One Nestbolt engine per worker: the main thread never runs geometry.
import init, { estimate_sheets, export_sheet, import_files_with_options, memory_bytes, nest, nest_job, validate } from './pkg/nestbolt_wasm.js';

const ready = init();

self.onmessage = async (event: MessageEvent) => {
  const { id, type, args } = event.data;
  try {
    await ready;
    let value: string;
    switch (type) {
      case 'import':
        value = import_files_with_options(JSON.stringify(args.files), JSON.stringify({
          ...(args.tolerance > 0 ? { tolerance: args.tolerance } : {}),
          ...(args.closeGapsMm !== undefined ? { close_gaps_mm: args.closeGapsMm } : {}),
        }));
        break;
      case 'nest':
        value = nest(args.library, args.request, args.seconds, args.seed, args.repeatable, args.live ?? 0,
          (t: number, material: number, layout?: string) => self.postMessage({ id, type: 'progress', t, material, layout }));
        break;
      case 'nest_job':
        value = nest_job(args.job, args.seconds, args.seed, args.repeatable,
          (t: number, material: number) => self.postMessage({ id, type: 'progress', t, material }));
        break;
      case 'validate':
        value = validate(args.library, args.request, args.layout);
        break;
      case 'export':
        value = export_sheet(args.library, args.request, args.layout, args.sheet, args.format, args.outline);
        break;
      case 'estimate':
        value = estimate_sheets(args.library, args.request);
        break;
      default:
        throw new Error(`unknown request ${type}`);
    }
    self.postMessage({ id, type: 'done', value, memory: memory_bytes() });
  } catch (error) {
    self.postMessage({ id, type: 'error', message: String(error) });
  }
};
