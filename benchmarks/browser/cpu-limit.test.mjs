import test from 'node:test'
import assert from 'node:assert/strict'
import { selectedCpu } from './cpu-limit.mjs'

test('CPU indices select exactly one bit, including values beyond 32-bit masks', () => {
  for(const index of [0,2,4,6,31,40,62]) {
    const selected=selectedCpu(0,String(index),64)
    assert.equal(selected.index,index)
    assert.equal(BigInt(selected.mask),1n<<BigInt(index))
  }
})
test('invalid, multiple, fractional, negative and unavailable CPU selections fail', () => {
  for(const value of ['', '-1', '1.5', '1,2', '04', '32', '999999999999999999']) {
    assert.throws(() => selectedCpu(0,value,32))
  }
  assert.throws(() => selectedCpu(0,'63',64))
})
