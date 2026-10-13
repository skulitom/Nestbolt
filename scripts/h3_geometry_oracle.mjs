// Test-only adapter around the published, unmodified MIT oracle.
import fs from 'node:fs/promises';
import path from 'node:path';
import { parseLbrn2, lbrn2ToSvg } from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';

const [manifest] = process.argv.slice(2);
const request = JSON.parse(await fs.readFile(manifest, 'utf8'));
const reports = [];
for (const row of request.projects) {
  const warnings = [], originalWarn = console.warn;
  console.warn = (...args) => warnings.push(args.map(String).join(' '));
  try {
    const parsed = parseLbrn2(await fs.readFile(row.normalized_xml, 'utf8'));
    const value = parsed.LightBurnProject.Shape;
    const shapes = Array.isArray(value) ? value : value ? [value] : [];
    if (shapes.length !== row.shape_indices.length) throw new Error(`Oracle shape count ${shapes.length} != ${row.shape_indices.length}`);
    await fs.mkdir(row.svg_directory, { recursive: true });
    for (let i=0; i<shapes.length; i++) {
      const svg = lbrn2ToSvg({ LightBurnProject: { ...parsed.LightBurnProject, Shape: [shapes[i]] } });
      await fs.writeFile(path.join(row.svg_directory, `${row.shape_indices[i]}.svg`), svg);
    }
    reports.push({ path: row.path, converted: shapes.length, warnings });
  } catch (error) {
    reports.push({ path: row.path, error: String(error), warnings });
  } finally { console.warn = originalWarn; }
}
await fs.writeFile(request.oracle_report, JSON.stringify({ oracle: 'lbrn2-to-svg@0.5.3', reports }, null, 2)+'\n');
