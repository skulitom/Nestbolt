// Headed unmodified comparator. Run inside Anode on Windows or a test display.
import { _electron as electron } from 'playwright'
import { mkdirSync, readFileSync, writeFileSync, appendFileSync } from 'node:fs'
import { resolve, dirname, join, sep } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createHash } from 'node:crypto'
import { execFileSync } from 'node:child_process'
import { verifyCpu } from './cpu-limit.mjs'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const requestPath = resolve(process.argv[2])
const request = JSON.parse(readFileSync(requestPath, 'utf8'))
const output = dirname(requestPath)
const upstream = join(root, '.cache/upstream/deepnest-next')
const profile = join(output, 'profile')
const imports = join(output, 'empty-imports')
mkdirSync(profile, { recursive: true })
mkdirSync(imports, { recursive: true })
writeFileSync(join(profile, 'settings.json'), JSON.stringify({ showNotifications: false, threads: 1, useSvgPreProcessor: false, useQuantityFromFileName: false }) + '\n')
let affinity
if (process.platform === 'win32') {
  // A separate logical CPU from the current SVGnest batch's CPU 0.
  const mask = execFileSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-File',
    join(root, 'benchmarks/browser/cpu-job.ps1'), '-ControllerId', String(process.pid), '-Mask', '4'],
    { encoding: 'utf8', windowsHide: true }).trim()
  if (mask !== '4') throw new Error('Deepnest controller CPU limit failed')
  affinity = { platform: 'win32', mask, method: 'JOB_OBJECT_LIMIT_AFFINITY' }
} else if (process.platform === 'linux') {
  const cpu = readFileSync('/proc/self/status', 'utf8').match(/^Cpus_allowed_list:\s*(.+)$/m)[1].split(/[-,]/)[0]
  execFileSync('taskset', ['-pc', cpu, String(process.pid)])
  affinity = { platform: 'linux', cpu }
} else {
  throw new Error('Deepnest benchmark CPU controls currently support Windows/Linux')
}
const executable = process.platform === 'win32' ? join(upstream, 'node_modules/electron/dist/electron.exe')
  : join(upstream, 'node_modules/electron/dist/electron')
const result = { status: 'starting', errors: [], console: [], candidates: 0, last: null,
  affinity, configured_workers: 1, seed: request.seed, budget_seconds: request.seconds,
  background_throttling: false,
  hardware_acceleration: false,
  electron_executable_sha256: createHash('sha256').update(readFileSync(executable)).digest('hex') }
let app, solveStart
const started = performance.now()
const checkpoint = name => {
  (result.stages_ms ||= {})[name] = performance.now()-started
  writeFileSync(join(output, 'stage-progress.json'), JSON.stringify({ stages_ms: result.stages_ms })+'\n')
}
async function closeOwnedApp() {
  if (!app) return
  const child = app.process()
  const running = () => child.exitCode === null && child.signalCode === null
  if (running()) {
    // Bypass renderer beforeunload handlers, which can stall behind native NFP
    // work. Only this isolated Electron process tree belongs to the controller.
    const exited = new Promise(resolve => child.once('exit', resolve))
    app.evaluate(({ app }) => app.exit(0)).catch(() => {})
    await Promise.race([exited, new Promise(resolve => setTimeout(resolve, 2000))])
    if (running()) {
      if (process.platform === 'win32') {
        execFileSync('taskkill', ['/PID', String(child.pid), '/T', '/F'], { windowsHide: true, stdio: 'ignore' })
      } else {
        try { execFileSync('pkill', ['-KILL', '-P', String(child.pid)]) } catch {}
        child.kill('SIGKILL')
      }
      await exited
    }
  }
  await app.close().catch(() => {})
  app = null
}
try {
  app = await electron.launch({ executablePath: executable, timeout: 120000,
    args: [join(root, 'benchmarks/browser/deepnest-bootstrap.cjs')], cwd: upstream,
    env: { ...process.env, NESTBENCH_PROFILE: profile, NESTBENCH_UPSTREAM: upstream,
      NESTBENCH_PRELOAD: join(root, 'benchmarks/browser/deepnest-preload.cjs'), NESTBENCH_SEED: String(request.seed),
      SAVE_PLACEMENTS_PATH: imports + sep, deepnest_debug: '0', DEEPNEST_LONGLIST: '' } })
  checkpoint('app_launched')
  app.on('window', page => {
    page.on('pageerror', error => result.errors.push(String(error)))
    page.on('console', message => { if (result.console.length < 1000) result.console.push({ type: message.type(), text: message.text() }) })
  })
  const actual = await app.evaluate(({ app }) => ({ profile: app.getPath('userData'), versions: process.versions }))
  if (resolve(actual.profile) !== profile) throw new Error('Profile isolation failed')
  result.versions = actual.versions
  result.direct_inspection = await Promise.race([
    app.evaluate(async ({ BrowserWindow }) => {
      const windows = BrowserWindow.getAllWindows()
      return await Promise.all(windows.map(async w => ({ url: w.webContents.getURL(),
        state: await w.webContents.executeJavaScript('({ready:document.readyState,main:!!window.DeepNest,seed:window.nestbenchSeed,config:!!window.config})') })))
    }),
    new Promise(resolve => setTimeout(() => resolve({ error:'direct inspection timeout' }), 3000)),
  ])
  writeFileSync(join(output, 'direct-inspection.json'), JSON.stringify(result.direct_inspection)+'\n')
  await app.firstWindow()
  const page = app.windows().find(p => p.url().endsWith('/main/index.html'))
  if (!page) throw new Error(`Main window was not found: ${app.windows().map(p => p.url()).join(', ')}`)
  page.on('pageerror', error => result.errors.push(String(error)))
  await page.waitForFunction(() => window.DeepNest && window.config && window.nestbenchSeed !== undefined, undefined, { polling: 100, timeout: 120000 })
  checkpoint('main_ready')
  let background = app.context().pages().find(p => p.url().endsWith('/background.html'))
  if (!background) background = await app.context().waitForEvent('page', { predicate: p => p !== page, timeout: 120000 })
  await background.waitForFunction(() => window.db && window.Parallel && window.nestbenchSeed !== undefined, undefined, { polling: 100, timeout: 120000 })
  background.on('pageerror', error => result.errors.push(String(error)))
  background.on('console', message => { if (result.console.length < 1000) result.console.push({ type: message.type(), text: message.text() }) })
  checkpoint('both_windows_ready')
  result.worker_check = await background.evaluate(() => ({ workers: new Parallel([]).options.maxWorkers, seed: window.nestbenchSeed }))
  if (result.worker_check.workers !== 1 || result.worker_check.seed !== request.seed) throw new Error('Background worker/seed control failed')
  await page.exposeFunction('saveNativeCandidate', candidate => {
    if (solveStart === undefined || performance.now()-solveStart > request.seconds*1000 || candidate.elapsed_ms > request.seconds*1000) return
    result.candidates++
    result.last = candidate
    appendFileSync(join(output, 'candidates.jsonl'), JSON.stringify(candidate)+'\n')
  })
  result.imported = await page.evaluate(prepared => {
    if (window.DeepNest.parts.length !== 0) throw new Error('Nonempty isolated profile at import')
    DeepNest.config(prepared.config)
    const evidence = []
    for (const source of prepared.imports) {
      const parts = DeepNest.importsvg(`source-${source.source}.svg`, null, source.svg, undefined, false)
      if (parts.length !== 1 || DeepNest.parts.length-1 !== source.source) throw new Error('SVG import changed source identity/count')
      const part = parts[0]
      const children = part.polygontree.children || []
      if (children.length !== source.hole_count || children.some(c => c.children?.length)) throw new Error('SVG import changed hole topology')
      part.quantity = source.quantity
      part.sheet = source.kind === 'stock'
      evidence.push({ source: source.source, quantity: part.quantity, sheet: part.sheet,
        bounds: part.bounds, polygon: part.polygontree.map(p => [p.x,p.y]), holes: children.map(c => c.map(p => [p.x,p.y])) })
    }
    return { inputs: evidence, config: DeepNest.config(), seed: window.nestbenchSeed }
  }, request.prepared)
  if (result.imported.seed !== request.seed || result.imported.config.threads !== 1) throw new Error('Main-window seed/configuration control failed')
  const binaries = [...new Set([
    ...await page.evaluate(() => Object.keys(require.cache).filter(path => path.endsWith('.node'))),
    ...await background.evaluate(() => Object.keys(require.cache).filter(path => path.endsWith('.node'))),
  ])]
  result.native_binaries = binaries.map(path => ({ path, sha256: createHash('sha256').update(readFileSync(path)).digest('hex') }))
  checkpoint('source_imported')
  result.affinity_verification = verifyCpu(affinity)
  solveStart = performance.now()
  let startupError
  page.evaluate(seconds => {
    const started = performance.now()
    DeepNest.start(() => {}, () => {
      const elapsed = performance.now()-started
      if (elapsed > seconds*1000 || !DeepNest.nests.length) return
      window.saveNativeCandidate({ elapsed_ms: elapsed, native: JSON.parse(JSON.stringify(DeepNest.nests[0])) })
    })
  }, request.seconds).catch(error => { startupError = String(error) })
  await new Promise(resolve => setTimeout(resolve, request.seconds*1000))
  result.controller_solve_ms = performance.now()-solveStart
  checkpoint('budget_finished')
  if (startupError) result.errors.push(startupError)
  result.status = result.last ? 'completed' : 'no_layout'
  writeFileSync(join(output, 'browser-result.json'), JSON.stringify(result, null, 2)+'\n')
  await closeOwnedApp()
  checkpoint('app_closed')
} catch (error) {
  result.status = 'failed'
  result.errors.push(String(error))
  if (app) {
    result.windows = app.windows().map(page => ({ url: page.url(), closed: page.isClosed() }))
    result.window_states = await Promise.all(app.windows().map(async page => {
      try {
        return await Promise.race([
          page.evaluate(() => ({ url: location.href, ready: document.readyState, seed: window.nestbenchSeed,
            main: !!window.DeepNest, config: !!window.config, background: !!window.db, parallel: !!window.Parallel })),
          new Promise(resolve => setTimeout(() => resolve({ inspection: 'timed out' }), 1000)),
        ])
      } catch (error) { return { inspection: String(error) } }
    }))
  }
} finally {
  await closeOwnedApp()
  writeFileSync(join(output, 'browser-result.json'), JSON.stringify(result, null, 2)+'\n')
}
process.stdout.write(JSON.stringify({ status: result.status, candidates: result.candidates, errors: result.errors })+'\n')
