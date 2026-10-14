// Unmodified independent MIT reader, given only normalized authored probes.
import fs from 'node:fs/promises';
import path from 'node:path';
import { parseLbrn2, lbrn2ToSvg } from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';
const [input, output] = process.argv.slice(2);
await fs.mkdir(output);
for (const name of await fs.readdir(input)) {
  if (!/^(svg|dxf)-native\.lbrn2$/.test(name)) continue;
  const project = parseLbrn2(await fs.readFile(path.join(input, name), 'utf8'));
  await fs.writeFile(path.join(output, name.replace('.lbrn2', '.svg')), lbrn2ToSvg(project));
}
