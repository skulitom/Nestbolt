import type { Layout, Library } from './types.js';

/** Same source-stem and sheet-order naming as the native preserving exporter. */
export function exportFilename(library: Library, layout: Layout, sheet: string, format: 'svg' | 'dxf' | 'lbrn2'): string {
  if (!library.lightburn) return `${sheet}.${format}`;
  const basename = library.lightburn.file.split(/[\\/]/).pop() || 'project';
  const stem = basename.replace(/\.[^.]*$/, '');
  const safe = Array.from(stem).map(c => /[a-zA-Z0-9_-]/.test(c) ? c : '-').join('');
  return `${safe}-sheet-${layout.sheets.findIndex(s => s.id === sheet) + 1}${format === 'lbrn2' ? '' : '-cuts'}.${format}`;
}
