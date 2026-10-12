// Observe exit on the exact owned ChildProcess, including taskkill/exit races.
const running = child => child.exitCode === null && child.signalCode === null

function waitForExit(child, milliseconds) {
  if (!running(child)) return Promise.resolve()
  return new Promise(resolve => {
    const finish = () => { clearTimeout(timer); child.removeListener('exit', finish); resolve() }
    const timer = setTimeout(finish, milliseconds)
    child.once('exit', finish)
  })
}

export async function closeOwnedProcess(child, requestExit, forceExit, graceMs = 2000, forceMs = 3000) {
  if (!running(child)) return
  Promise.resolve().then(requestExit).catch(() => {})
  await waitForExit(child, graceMs)
  if (!running(child)) return
  let forceError
  try { forceExit() } catch (error) { forceError = error }
  // taskkill can report "not found" just before Node dispatches its exit event.
  // Only observing this ChildProcess exit makes that failure safe to ignore.
  await waitForExit(child, forceMs)
  if (running(child)) throw forceError || new Error(`Owned process ${child.pid} did not exit`)
}
