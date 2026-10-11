// Isolate the upstream desktop app's settings before any upstream module loads.
const { app } = require('electron')
const path = require('node:path')
if (!process.env.NESTBENCH_PROFILE || !process.env.NESTBENCH_UPSTREAM) {
  throw new Error('Explicit benchmark profile and upstream checkout are required')
}
app.setPath('userData', process.env.NESTBENCH_PROFILE)
app.setAppPath(process.env.NESTBENCH_UPSTREAM)
app.setName('deepnest-benchmark')
require(path.join(process.env.NESTBENCH_UPSTREAM, 'main.js'))
