// Source geometry only: no nesting or quality evaluation occurs here.
import { readFileSync } from 'node:fs'
import { Teagan } from '@freesewing/teagan'
import { Bruce } from '@freesewing/bruce'

const request = JSON.parse(readFileSync(0, 'utf8'))
const Constructor = { teagan: Teagan, bruce: Bruce }[request.design]
if (!Constructor) throw new Error('Unknown pinned design')
const pattern = new Constructor({
  measurements: request.measurements,
  sa: request.seam_allowance,
  complete: false,
})
pattern.draft()
const logs = pattern.getLogs()
const warnings = [logs.pattern, ...logs.sets].flatMap(x => [...x.warn, ...x.error])
if (warnings.length) throw new Error(JSON.stringify(warnings))

// Read full precision operations, avoiding asPathstring's 0.01 mm rounding.
const parts = Object.entries(pattern.parts[0])
  .filter(([, part]) => !part.hidden)
  .map(([id, part]) => {
    const path = request.seam_allowance ? part.paths.sa : part.paths.seam
    if (!path) throw new Error(`Missing cut boundary: ${id}`)
    const ops = path.ops.map(op => {
      if (!['move', 'line', 'curve', 'close'].includes(op.type)) {
        throw new Error(`Unsupported operation: ${op.type}`)
      }
      const result = { type: op.type }
      for (const name of ['to', 'cp1', 'cp2']) {
        if (op[name]) {
          const { x, y } = op[name]
          if (!Number.isFinite(x) || !Number.isFinite(y)) throw new Error('Nonfinite point')
          result[name] = [x, y]
        }
      }
      return result
    })
    return { id, ops }
  })
process.stdout.write(JSON.stringify({ design: request.design, version: '4.10.2', parts }) + '\n')
