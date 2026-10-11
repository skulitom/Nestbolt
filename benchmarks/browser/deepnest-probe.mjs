// Run this headed probe inside Anode. It does not start a nesting benchmark.
import { _electron as electron } from 'playwright'
import { mkdirSync, writeFileSync } from 'node:fs'
import { resolve, dirname, join, sep } from 'node:path'
import { fileURLToPath } from 'node:url'

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..')
const output = resolve(process.argv[2])
const upstream = join(root, '.cache/upstream/deepnest-next')
const profile = join(output, 'profile')
const imports = join(output, 'empty-imports')
mkdirSync(profile, { recursive: true })
mkdirSync(imports, { recursive: true })
writeFileSync(join(profile, 'settings.json'), JSON.stringify({ showNotifications: false, threads: 1 }) + '\n')
let app
try {
  app = await electron.launch({
    executablePath: join(upstream, 'node_modules/electron/dist/electron.exe'),
    args: [join(root, 'benchmarks/browser/deepnest-bootstrap.cjs')], cwd: upstream,
    env: { ...process.env, NESTBENCH_PROFILE: profile, NESTBENCH_UPSTREAM: upstream,
      SAVE_PLACEMENTS_PATH: imports + sep, deepnest_debug: '0' },
  })
  const actual = await app.evaluate(({ app }) => ({ profile: app.getPath('userData'), version: app.getVersion() }))
  if (resolve(actual.profile) !== profile) throw new Error('Profile isolation failed')
  const page = await app.firstWindow()
  await page.waitForFunction(() => window.DeepNest && window.config)
  const state = await page.evaluate(() => ({ title: document.title, url: location.href,
    config: window.DeepNest.config(), parts: window.DeepNest.parts.length,
    methods: Object.getOwnPropertyNames(Object.getPrototypeOf(window.DeepNest)) }))
  await page.screenshot({ path: join(output, 'desktop.png') })
  writeFileSync(join(output, 'probe.json'), JSON.stringify({ ...actual, ...state }, null, 2) + '\n')
  process.stdout.write(JSON.stringify({ profile: actual.profile, version: actual.version, title: state.title, parts: state.parts }) + '\n')
} finally {
  if (app) await app.close()
}
