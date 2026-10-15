import init, { export_sheet } from './pkg/nestbolt_wasm.js';
import { exportFilename } from './export-names';
import type { Project } from './types';
import { ZipBuilder } from './zip';

// Generate checked cutting files, encode them and assemble the download here.
// Only the immutable finished Blob crosses back to the main thread. Each text
// export can be collected after add(), instead of retaining all exports at once.
self.onmessage = async (event: MessageEvent<{ project: Project; includeProject: boolean }>) => {
  try {
    const { project, includeProject } = event.data;
    const { library, request, result } = project;
    const archive = new ZipBuilder();
    if (includeProject) {
      archive.add('project.json', JSON.stringify(project, null, 1));
      if (result) archive.add('layout.json', JSON.stringify(result.layout, null, 1));
    }
    if (library && result) {
      await init();
      const lib = JSON.stringify(library), req = JSON.stringify(request), layout = JSON.stringify(result.layout);
      const formats: ('svg' | 'dxf' | 'lbrn2')[] = library.lightburn
        ? (request.lead_in ? ['lbrn2', 'svg', 'dxf'] : ['lbrn2']) : ['svg', 'dxf'];
      for (const sheet of result.layout.sheets) for (const format of formats) {
        archive.add(`sheets/${exportFilename(library, result.layout, sheet.id, format)}`,
          export_sheet(lib, req, layout, sheet.id, format, format === 'lbrn2' ? (project.lightburnOutline ?? true) : false));
      }
    } else if (!includeProject) {
      throw new Error('No completed layout to export.');
    }
    self.postMessage({ type: 'done', value: archive.finish() });
  } catch (error) {
    self.postMessage({ type: 'error', message: String(error) });
  }
};
