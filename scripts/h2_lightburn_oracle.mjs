// Independent, unmodified MIT lbrn2-to-svg package; only native H2 result files.
import fs from 'node:fs/promises';
import path from 'node:path';
import { parseLbrn2, lbrn2ToSvg } from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';

const [results, output] = process.argv.slice(2);
if (!results || !output) throw new Error('Pass results directory and a new output directory');
await fs.mkdir(output); // Never replace an earlier diagnostic.
const preparation = JSON.parse(await fs.readFile(path.join(results, 'preparation.json'), 'utf8'));
for (const row of preparation.cases) {
  if (!/^[a-z]+$/.test(row.name)) throw new Error('Unexpected case name');
  for (const format of ['dxf', 'svg']) {
    const stem = `${row.name}-${format}-native`;
    const project = parseLbrn2(await fs.readFile(path.join(results, `${stem}.lbrn2`), 'utf8'));
    await fs.writeFile(path.join(output, `${stem}.svg`), lbrn2ToSvg(project));
  }
}
