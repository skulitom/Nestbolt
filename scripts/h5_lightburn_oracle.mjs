// Read native H5 saves with the independent unmodified MIT reader.
import fs from 'node:fs/promises';
import path from 'node:path';
import { parseLbrn2, lbrn2ToSvg } from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';

const [folder, output] = process.argv.slice(2);
if (!folder || !output) throw new Error('Pass evidence folder and new output directory');
await fs.mkdir(output);
for (const stem of ['laser-svg-native', 'plasma-dxf-native']) {
  const project = parseLbrn2(await fs.readFile(path.join(folder, `${stem}.lbrn2`), 'utf8'));
  await fs.writeFile(path.join(output, `${stem}.svg`), lbrn2ToSvg(project));
}
