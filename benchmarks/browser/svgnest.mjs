// Drive unmodified SVGnest in a real local Chromium instance. No uploaded geometry.
import { chromium } from 'playwright'
import { createServer } from 'node:http'
import { readFileSync, writeFileSync, appendFileSync } from 'node:fs'
import { resolve, dirname, join } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { limitCpu, verifyCpu } from './cpu-limit.mjs'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const requestPath = resolve(process.argv[2])
const request = JSON.parse(readFileSync(requestPath, 'utf8'))
const output = dirname(requestPath)
const upstream = join(root, '.cache/upstream/svgnest')
const scripts = ['util/pathsegpolyfill.js', 'util/matrix.js', 'util/geometryutil.js',
  'util/parallel.js', 'util/placementworker.js', 'util/clipper.js', 'svgparser.js', 'svgnest.js']
const allowedFiles = new Set([...scripts, 'util/eval.js', 'util/json.js'])
const affinity = limitCpu()

const server = createServer((req, res) => {
  const path = new URL(req.url, 'http://localhost').pathname.slice(1)
  if (!path) {
    res.setHeader('Content-Type', 'text/html; charset=utf-8')
    res.end('<!doctype html><title>SVGnest local benchmark</title>' +
      '<style>body{background:#eee}svg{display:block;max-width:900px;max-height:650px;margin:20px;background:white}.hole{fill:white}</style>' +
      scripts.map(p => `<script src="/${p}"></script>`).join(''))
  } else if (allowedFiles.has(path)) {
    res.setHeader('Content-Type', 'text/javascript; charset=utf-8')
    res.end(readFileSync(join(upstream, path)))
  } else {
    res.writeHead(404).end()
  }
})
await new Promise(resolve => server.listen(0, '127.0.0.1', resolve))
let browser
const result = { candidates: 0, last: null, console: [], errors: [], affinity,
  random_seed: request.seed, configured_workers: 1, budget_seconds: request.seconds }
let solveStart = null
try {
  browser = await chromium.launch({ headless: true })
  result.browser_version = browser.version()
  const context = await browser.newContext()
  const base = `http://127.0.0.1:${server.address().port}`
  await context.route('**/*', route => route.request().url().startsWith(base + '/') ? route.continue() : route.abort())
  await context.addInitScript(({ seed }) => {
    Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 1 })
    let state = seed >>> 0
    Math.random = () => {
      let t = state = (state + 0x6D2B79F5) >>> 0
      t = Math.imul(t ^ (t >>> 15), t | 1)
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296
    }
  }, { seed: request.seed })
  const page = await context.newPage()
  page.on('console', message => { if (result.console.length < 1000) result.console.push({ type: message.type(), text: message.text() }) })
  page.on('pageerror', error => result.errors.push(String(error)))
  await page.exposeFunction('saveCandidate', candidate => {
    // Renderer and controller each enforce the cutoff. Completed results that
    // arrive after it are retained neither as the final result nor for scoring.
    if (solveStart === null || performance.now() - solveStart > request.seconds * 1000) return
    if (candidate.elapsed_ms > request.seconds * 1000) return
    result.candidates++
    result.last = candidate
    appendFileSync(join(output, 'candidates.jsonl'), JSON.stringify(candidate) + '\n')
  })
  await page.goto(base, { waitUntil: 'load' })
  result.input_fidelity = await page.evaluate(prepared => {
    if (new Parallel([]).options.maxWorkers !== 1) throw new Error('Upstream worker limit was not applied')
    SvgNest.config(prepared.config)
    const svg = SvgNest.parsesvg(prepared.svg)
    let coordinates = 0
    for (const [id, ring] of Object.entries(prepared.source_rings)) {
      const node = Array.from(svg.children).find(p => p.id === id)
      if (!node) throw new Error(`Source contour lost during import: ${id}`)
      const actual = SvgParser.polygonify(node).map(p => [p.x,p.y])
      const expected = ring.slice()
      for (const points of [actual,expected]) {
        if (points.length>1 && points[0][0]===points.at(-1)[0] && points[0][1]===points.at(-1)[1]) points.pop()
      }
      if (actual.length!==expected.length) throw new Error(`Source vertex count changed: ${id}`)
      for(let i=0;i<actual.length;i++)for(let axis=0;axis<2;axis++) {
        if(actual[i][axis]!==expected[i][axis]) throw new Error(`Source coordinate rounded during import: ${id}/${i}/${axis}`)
        coordinates++
      }
    }
    const bin = svg.querySelector('#sheet')
    if (!bin) throw new Error('Source sheet was lost during import')
    SvgNest.setbin(bin)
    const nodes = Array.from(svg.children).filter(p => p.id !== 'sheet')
    const parts = SvgNest.getParts(nodes)
    if (parts.length !== prepared.copies) throw new Error(`Source import changed quantity: ${parts.length}/${prepared.copies}`)
    window.benchmark = { started: null, iterations: 0, config: SvgNest.config() }
    return { encoding: prepared.input_encoding, contours: Object.keys(prepared.source_rings).length,
      coordinates, maximum_absolute_error: 0 }
  }, request.prepared)
  result.configuration = await page.evaluate(() => window.benchmark.config)
  result.affinity_verification = verifyCpu(affinity)
  const executables = [...new Set(result.affinity_verification.filter(p => /chrome|chromium/i.test(p.name)).map(p => p.executable))]
  if (!executables.length || executables.some(p => !p)) throw new Error('Browser executable provenance is missing')
  result.browser_executables = executables.map(path => ({ path, sha256: createHash('sha256').update(readFileSync(path)).digest('hex') }))
  solveStart = performance.now()
  const solving = page.evaluate(seconds => {
    const state = window.benchmark
    state.started = performance.now()
    SvgNest.start(() => {}, (svgs, utilisation, placed, total) => {
      state.iterations++
      const elapsed = performance.now() - state.started
      if (!svgs || elapsed > seconds * 1000) return
      const sheets = svgs.map(svg => Array.from(svg.children).filter(c => c.tagName.toLowerCase() === 'g').map(group => {
        const matrix = group.transform.baseVal.consolidate().matrix
        const children = Array.from(group.children)
        return { outer_id: children[0].id, hole_ids: children.slice(1).map(c => c.id),
          matrix: [matrix.a, matrix.b, matrix.c, matrix.d, matrix.e, matrix.f] }
      }))
      window.saveCandidate({ elapsed_ms: elapsed, native_utilisation: utilisation,
        native_placed: placed, native_total: total, sheets, svgs: svgs.map(s => s.outerHTML) })
    })
  }, request.seconds)
  // The external timer can close a renderer stuck in synchronous preprocessing.
  let startupError
  solving.catch(error => { startupError = String(error) })
  await new Promise(resolve => setTimeout(resolve, request.seconds * 1000))
  result.controller_solve_ms = performance.now() - solveStart
  if (startupError) result.errors.push(startupError)
  // Never await renderer completion past the time budget to gain more search.
  await browser.close()
  browser = null
  result.status = result.last ? 'completed' : 'no_layout'
} catch (error) {
  result.status = 'failed'
  result.errors.push(String(error))
} finally {
  if (browser) await browser.close()
  server.closeAllConnections()
  await new Promise(resolve => server.close(resolve))
  writeFileSync(join(output, 'browser-result.json'), JSON.stringify(result, null, 2) + '\n')
}
process.stdout.write(JSON.stringify({ status: result.status, candidates: result.candidates, errors: result.errors }) + '\n')
