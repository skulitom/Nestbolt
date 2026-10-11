// Measure the pinned parser's numeric input fidelity without running a search.
import { chromium } from 'playwright'
import { createServer } from 'node:http'
import { readFileSync, writeFileSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const source = resolve(process.argv[2]), destination = resolve(process.argv[3])
const request = JSON.parse(readFileSync(source, 'utf8'))
const scripts = ['util/pathsegpolyfill.js','util/matrix.js','util/geometryutil.js','util/parallel.js',
  'util/placementworker.js','util/clipper.js','svgparser.js','svgnest.js']
const server = createServer((req,res) => {
  const path = new URL(req.url,'http://localhost').pathname.slice(1)
  if (!path) {
    res.setHeader('Content-Type','text/html')
    res.end('<!doctype html>'+scripts.map(p=>`<script src="/${p}"></script>`).join(''))
  } else if (scripts.includes(path)) {
    res.setHeader('Content-Type','text/javascript')
    res.end(readFileSync(join(root,'.cache/upstream/svgnest',path)))
  } else res.writeHead(404).end()
})
await new Promise(resolve=>server.listen(0,'127.0.0.1',resolve))
let browser
try {
  browser = await chromium.launch({headless:true})
  const context = await browser.newContext()
  const base = `http://127.0.0.1:${server.address().port}`
  await context.route('**/*',route=>route.request().url().startsWith(base+'/')?route.continue():route.abort())
  const page = await context.newPage()
  await page.goto(base)
  const result = await page.evaluate(prepared => {
    const source = new DOMParser().parseFromString(prepared.svg,'image/svg+xml')
    const expected = Array.from(source.documentElement.children).map(node=>({id:node.id,
      points:node.getAttribute('points').trim().split(/\s+/).map(pair=>pair.split(',').map(Number))}))
    const runs = []
    for (const encoding of ['polygon','path']) {
      const doc = source.cloneNode(true)
      if (encoding==='path') for (const node of Array.from(doc.documentElement.children)) {
        const path = doc.createElementNS('http://www.w3.org/2000/svg','path')
        path.id=node.id
        const points=expected.find(p=>p.id===node.id).points
        path.setAttribute('d',points.map(([x,y],i)=>`${i?'L':'M'}${x} ${y}`).join(' ')+' Z')
        node.replaceWith(path)
      }
      SvgNest.config(prepared.config)
      const parsed=SvgNest.parsesvg(new XMLSerializer().serializeToString(doc))
      let maximum=0,coordinates=0,worst=null
      for (const part of expected) {
        const node=Array.from(parsed.children).find(n=>n.id===part.id)
        if(!node) throw new Error('Import lost '+part.id)
        const actual=SvgParser.polygonify(node)
        const wanted=part.points.slice()
        if(wanted.length>1 && wanted[0][0]===wanted.at(-1)[0] && wanted[0][1]===wanted.at(-1)[1])wanted.pop()
        if(actual.length>1 && actual[0].x===actual.at(-1).x && actual[0].y===actual.at(-1).y)actual.pop()
        if(actual.length!==wanted.length)throw new Error('Import changed vertex count '+part.id)
        for(let i=0;i<wanted.length;i++)for(let axis=0;axis<2;axis++){
          const value=actual[i][axis?'y':'x'],error=Math.abs(value-wanted[i][axis]);coordinates++
          if(error>maximum){maximum=error;worst={id:part.id,index:i,axis,expected:wanted[i][axis],actual:value}}
        }
      }
      runs.push({encoding,coordinates,maximum_absolute_error:maximum,worst})
    }
    return runs
  },request.prepared)
  const proof={scope:'Parser fidelity diagnostic; no optimisation or quality claim',browser_version:browser.version(),
    request:source,request_sha256:createHash('sha256').update(readFileSync(source)).digest('hex'),
    probe_sha256:createHash('sha256').update(readFileSync(fileURLToPath(import.meta.url))).digest('hex'),
    scripts:Object.fromEntries(scripts.map(p=>[p,createHash('sha256').update(readFileSync(join(root,'.cache/upstream/svgnest',p))).digest('hex')])),result}
  writeFileSync(destination,JSON.stringify(proof,null,2)+'\n',{flag:'wx'})
  process.stdout.write(JSON.stringify(result)+'\n')
} finally {
  if(browser)await browser.close()
  server.closeAllConnections()
  await new Promise(resolve=>server.close(resolve))
}
