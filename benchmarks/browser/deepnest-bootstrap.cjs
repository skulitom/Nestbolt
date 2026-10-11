// Isolate the upstream desktop app's settings before any upstream module loads.
const { app, session } = require('electron')
const path = require('node:path')
if (!process.env.NESTBENCH_PROFILE || !process.env.NESTBENCH_UPSTREAM) {
  throw new Error('Explicit benchmark profile and upstream checkout are required')
}
app.setPath('userData', process.env.NESTBENCH_PROFILE)
app.setAppPath(process.env.NESTBENCH_UPSTREAM)
app.setName('deepnest-benchmark')
app.disableHardwareAcceleration()
// Keep a hidden benchmark window running like a foreground user window.
app.commandLine.appendSwitch('disable-background-timer-throttling')
app.commandLine.appendSwitch('disable-renderer-backgrounding')
app.commandLine.appendSwitch('disable-backgrounding-occluded-windows')
app.on('web-contents-created', (event, contents) => contents.setBackgroundThrottling(false))
if (process.env.NESTBENCH_PRELOAD) {
  app.on('ready', () => {
    session.defaultSession.registerPreloadScript({ type: 'frame', filePath: process.env.NESTBENCH_PRELOAD })
    session.defaultSession.webRequest.onBeforeRequest({ urls: ['http://*/*', 'https://*/*'] }, (details, callback) => callback({ cancel: true }))
  })
}
require(path.join(process.env.NESTBENCH_UPSTREAM, 'main.js'))
