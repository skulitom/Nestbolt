// Published, unmodified MIT oracle used only for N0/N2 reference evidence.
import fs from 'node:fs/promises';
import path from 'node:path';
import {parseLbrn2, lbrn2ToSvg} from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';
const corpus=path.resolve('benchmarks/datasets/shop');
const output=path.resolve('output/shop-labels/lightburn-oracle');
await fs.mkdir(output,{recursive:true});
const manifest=JSON.parse(await fs.readFile(path.join(corpus,'manifest.draft.json'),'utf8'));
const rows=[];
for (const entry of manifest.files.filter(e=>/\.lbrn2?$/.test(e.path))) {
  const id=`L${String(rows.length).padStart(2,'0')}`;
  const row={id,path:entry.path,sha256:entry.sha256,oracle:'lbrn2-to-svg@0.5.3'};
  const warnings=[];
  const originalWarn=console.warn;
  console.warn=(...args)=>warnings.push(args);
  try {
    const project=parseLbrn2(await fs.readFile(path.join(corpus,entry.path),'utf8'));
    await fs.writeFile(path.join(output,id+'.json'),JSON.stringify(project,null,2)+'\n');
    await fs.writeFile(path.join(output,id+'.svg'),lbrn2ToSvg(project));
    row.shapes=Array.isArray(project.LightBurnProject.Shape)?project.LightBurnProject.Shape.length:project.LightBurnProject.Shape?1:0;
    row.converted=true;
  } catch(error) {row.error=String(error);}
  finally {console.warn=originalWarn;}
  row.warnings=warnings;
  rows.push(row); console.log(id, row.converted?'converted':'ERROR',entry.path);
}
await fs.writeFile(path.join(output,'manifest.json'),JSON.stringify({oracle:'lbrn2-to-svg@0.5.3',rows},null,2)+'\n');
