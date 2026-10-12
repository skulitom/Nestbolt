import test from 'node:test'
import assert from 'node:assert/strict'
import { EventEmitter } from 'node:events'
import { closeOwnedProcess } from './deepnest-lifecycle.mjs'

function child() {
  const child = new EventEmitter()
  Object.assign(child, { exitCode: null, signalCode: null, pid: 123,
    finish() { this.exitCode = 0; this.emit('exit', 0) } })
  return child
}

test('graceful exit never invokes forced process termination', async () => {
  const process = child()
  await closeOwnedProcess(process, () => process.finish(), () => assert.fail('forced'), 10, 10)
  assert.equal(process.listenerCount('exit'), 0)
})

test('a taskkill failure is ignored only after the exact child exits', async () => {
  const process = child()
  await closeOwnedProcess(process, () => {}, () => {
    setImmediate(() => process.finish())
    throw new Error('process already gone')
  }, 1, 100)
  assert.equal(process.listenerCount('exit'), 0)
  const stillAlive = child()
  await assert.rejects(closeOwnedProcess(stillAlive, () => {}, () => {
    throw new Error('permission denied')
  }, 1, 1), /permission denied/)
  assert.equal(stillAlive.listenerCount('exit'), 0)
})

test('successful force command is insufficient without an observed exit', async () => {
  await assert.rejects(closeOwnedProcess(child(), () => {}, () => {}, 1, 1), /did not exit/)
})
