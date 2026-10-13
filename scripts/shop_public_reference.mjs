// Reference-only per-shape conversion through the published MIT package.
import fs from 'node:fs/promises';
import path from 'node:path';
import {parseLbrn2,lbrn2ToSvg} from '../.cache/shop-oracle/node_modules/lbrn2-to-svg/dist/index.js';
const base=path.resolve('output/shop-public-native');
const output=path.join(base,'per-shape');
await fs.mkdir(output,{recursive:true});
const collection=JSON.parse(await fs.readFile(path.join(base,'collection.json'),'utf8'));
const reports=[];
// The package applies its SVG y reflection to every Group and every leaf.
// Python has composed world transforms already. Drop only these reference
// wrappers, keeping original top-level membership for the per-shape evidence.
const leaves=shape=>shape.Type==='Group'?(shape.Children||[]).flatMap(leaves):[shape];
for(const row of collection.rows){
 const warnings=[];const oldWarn=console.warn;
 console.warn=(...args)=>warnings.push(args);
 try{
  const project=parseLbrn2(await fs.readFile(path.join(base,'compatibility-inputs',row.id+'.lbrn2'),'utf8'));
  const value=project.LightBurnProject.Shape;
  const shapes=Array.isArray(value)?value:value?[value]:[];
  const convert=members=>lbrn2ToSvg({LightBurnProject:{...project.LightBurnProject,Shape:members.flatMap(leaves)}});
  await fs.writeFile(path.join(output,row.id+'-all.svg'),convert(shapes));
  // LightBurn omits layers with hide=1 from its SVG export altogether, unlike
  // doOutput=0, whose geometry remains as display:none. Retain hidden geometry
  // in the per-shape references and compare only native-exported leaves here.
  const settings=project.LightBurnProject.CutSetting||[];
  const settingList=Array.isArray(settings)?settings:[settings];
  const hidden=new Set(settingList.filter(s=>Number(s.hide)===1).map(s=>s.index));
  const cuts=new Set(settingList.filter(s=>['Cut','Scan+Cut','ScanCut'].includes(s.type)&&Number(s.doOutput??1)!==0).map(s=>s.index));
  const exported=shapes.flatMap(leaves).filter(s=>!hidden.has(s.CutIndex));
  await fs.writeFile(path.join(output,row.id+'-native-visible.svg'),convert(exported));
  for(let i=0;i<shapes.length;i++){
   await fs.writeFile(path.join(output,`${row.id}-${String(i).padStart(3,'0')}.svg`),convert([shapes[i]]));
   await fs.writeFile(path.join(output,`${row.id}-${String(i).padStart(3,'0')}-cut.svg`),convert(leaves(shapes[i]).filter(s=>cuts.has(s.CutIndex))));
  }
  reports.push({id:row.id,shapes:shapes.length,hidden_layers_omitted_by_native_export:[...hidden],warnings});
 }finally{console.warn=oldWarn;}
}
await fs.writeFile(path.join(output,'manifest.json'),JSON.stringify({oracle:'lbrn2-to-svg@0.5.3',reports},null,2)+'\n');
console.log(JSON.stringify({projects:reports.length,top_shapes:reports.reduce((n,r)=>n+r.shapes,0),warnings:reports.filter(r=>r.warnings.length).map(r=>r.id)}));
