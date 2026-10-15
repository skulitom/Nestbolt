// Unmodified independent MIT reader; input contains normalized authored coupons.
import fs from 'node:fs/promises';
import path from 'node:path';
import { parseLbrn2, lbrn2ToSvg } from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';
const [input, output] = process.argv.slice(2);
await fs.mkdir(output);
for (const name of ['line45', 'arc45', 'arc90']) {
  const project = parseLbrn2(await fs.readFile(path.join(input, `${name}.lbrn2`), 'utf8'));
  await fs.writeFile(path.join(output, `${name}.svg`), lbrn2ToSvg(project));
}
