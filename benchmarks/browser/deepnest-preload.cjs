// Environment controls only: seed the public JS RNG and restrict native workers.
const seed = Number(process.env.NESTBENCH_SEED)
if (!Number.isInteger(seed) || seed < 0 || seed >= 2 ** 32) throw new Error('Explicit uint32 seed required')
Object.defineProperty(navigator, 'hardwareConcurrency', { get: () => 1 })
let state = seed >>> 0
Math.random = () => {
  let t = state = (state + 0x6D2B79F5) >>> 0
  t = Math.imul(t ^ (t >>> 15), t | 1)
  t ^= t + Math.imul(t ^ (t >>> 7), t | 61)
  return ((t ^ (t >>> 14)) >>> 0) / 4294967296
}
window.nestbenchSeed = seed
