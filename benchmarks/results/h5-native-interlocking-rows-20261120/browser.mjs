// Exercise the deployed worker and its WASM engine on the same local inputs as the CLI.
import {createServer} from "node:http";
import {createRequire} from "node:module";
import {readFile, readdir, mkdir, writeFile} from "node:fs/promises";
import path from "node:path";

const [source, output, mode="work", secondsArg="30", selected="both"] = process.argv.slice(2);
if (!["work","wall"].includes(mode)) throw new Error("Expected work or wall timing");
if (!["both","chrome","firefox"].includes(selected)) throw new Error("Unknown browser");
const seconds=Number(secondsArg);
const require = createRequire(path.resolve("web/package.json"));
const {chromium, firefox} = require("playwright");
const dist = path.resolve("web/dist");
const workers = (await readdir(path.join(dist,"assets"))).filter(n => /^worker-.*\.js$/.test(n));
if (workers.length !== 1) throw new Error("Expected one production nesting worker");
const library = await readFile(path.join(source,"library.json"),"utf8");
const request = await readFile(path.join(source,"request.json"),"utf8");
const server = createServer(async (req,res) => {
  const file = req.url === "/" ? "index.html" : req.url?.slice(1);
  if (!file || !/^(index\.html|assets\/[\w.-]+)$/.test(file)) { res.writeHead(404).end(); return; }
  try {
    const data = await readFile(path.join(dist,file));
    res.writeHead(200,{"Content-Type":file.endsWith(".wasm")?"application/wasm":file.endsWith(".js")?"text/javascript":
      file.endsWith(".css")?"text/css":"text/html"}).end(data);
  } catch { res.writeHead(404).end(); }
});
await new Promise(resolve => server.listen(0,"127.0.0.1",resolve));
try {
  for (const [name,engine,launch] of [["chrome",chromium,{channel:"chrome"}],["firefox",firefox,{}]]) {
    if (selected!=="both" && name!==selected) continue;
    const browser = await engine.launch(launch);
    try {
      const page = await browser.newPage();
      await page.goto("http://127.0.0.1:"+server.address().port+"/");
      const result = await page.evaluate(async ({library,request,workerName,mode,seconds}) => {
        const worker = new Worker("/assets/"+workerName,{type:"module"});
        const call = (id,type,args) => new Promise((resolve,reject) => {
          const timeout=setTimeout(()=>reject(new Error("Worker "+type+" timed out")),100000);
          worker.onerror=e=>{clearTimeout(timeout); reject(new Error(e.message));};
          worker.onmessage=({data})=>{
            if (data.id!==id || data.type==="progress") return;
            clearTimeout(timeout);
            if(data.type==="error") reject(new Error(data.message)); else resolve(data.value);
          };
          worker.postMessage({id,type,args});
        });
        try {
          const nested=JSON.parse(await call(1,"nest",{library,request,seconds,seed:0,repeatable:mode==="work"}));
          const layout=JSON.stringify(nested.layout);
          const validated=JSON.parse(await call(2,"validate",{library,request,layout}));
          return {nested,validated};
        } finally { worker.terminate(); }
      },{library,request,workerName:workers[0],mode,seconds});
      const copies = JSON.parse(request).parts.reduce((sum, part) => sum + part.quantity, 0);
      if (!result.nested.validation.valid || !result.validated.valid || result.nested.layout.placements.length!==copies)
        throw new Error(name+" failed layout validation");
      await mkdir(output,{recursive:true});
      await writeFile(path.join(output,name+".json"),JSON.stringify(result));
      console.log(name,result.nested.repeatable,result.validated.metrics.normalized_material);
    } finally { await browser.close(); }
  }
} finally { await new Promise(resolve => server.close(resolve)); }
