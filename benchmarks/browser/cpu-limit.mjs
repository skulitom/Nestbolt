// Constrain the controller before it launches any solver/browser descendants.
import { execFileSync } from 'node:child_process'
import { readFileSync, readlinkSync } from 'node:fs'
import { fileURLToPath } from 'node:url'

function powershell(code) {
  return execFileSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-Command', code],
    { encoding: 'utf8', windowsHide: true }).trim()
}

export function limitCpu() {
  if (process.platform === 'win32') {
    const mask = execFileSync('powershell.exe', ['-NoProfile', '-NonInteractive', '-File',
      fileURLToPath(new URL('./cpu-job.ps1', import.meta.url)), '-ControllerId', String(process.pid)],
      { encoding: 'utf8', windowsHide: true }).trim()
    if (mask !== '1') throw new Error('Could not restrict controller to one CPU')
    return { platform: 'win32', mask, method: 'JOB_OBJECT_LIMIT_AFFINITY' }
  }
  if (process.platform === 'linux') {
    const allowed = readFileSync('/proc/self/status', 'utf8').match(/^Cpus_allowed_list:\s*(.+)$/m)[1]
    const cpu = allowed.split(/[-,]/)[0]
    execFileSync('taskset', ['-pc', cpu, String(process.pid)])
    return { platform: 'linux', cpu }
  }
  throw new Error('Single-core process affinity is implemented for Windows and Linux only')
}

export function verifyCpu(limit) {
  let entries
  if (limit.platform === 'win32') {
    entries = JSON.parse(powershell(`
      $nestRows = @(Get-CimInstance Win32_Process | Select-Object ProcessId,ParentProcessId)
      $nestIds = [System.Collections.Generic.HashSet[int]]::new()
      [void]$nestIds.Add(${process.pid})
      do {
        $nestAdded = $false
        foreach ($nestRow in $nestRows) {
          if ($nestIds.Contains([int]$nestRow.ParentProcessId)) {
            if ($nestIds.Add([int]$nestRow.ProcessId)) { $nestAdded = $true }
          }
        }
      } while ($nestAdded)
      $nestEvidence = @(foreach ($nestId in $nestIds) {
        $nestProcess = Get-Process -Id $nestId -ErrorAction SilentlyContinue
        if ($nestProcess) { @{pid=$nestId;name=$nestProcess.ProcessName;executable=$nestProcess.Path;affinity=$nestProcess.ProcessorAffinity.ToInt64().ToString()} }
      })
      ConvertTo-Json -InputObject $nestEvidence -Compress
    `))
    if (entries.some(p => p.affinity !== limit.mask)) throw new Error(`A browser descendant escaped single-core affinity: ${JSON.stringify(entries)}`)
  } else {
    const rows = execFileSync('ps', ['-e', '-o', 'pid=,ppid='], { encoding: 'utf8' })
      .trim().split('\n').map(row => row.trim().split(/\s+/).map(Number))
    const ids = new Set([process.pid])
    let changed
    do {
      changed = false
      for (const [id, parent] of rows) if (ids.has(parent) && !ids.has(id)) { ids.add(id); changed = true }
    } while (changed)
    entries = Array.from(ids).flatMap(pid => {
      try {
        const status = readFileSync(`/proc/${pid}/status`, 'utf8')
        return [{ pid, name: status.match(/^Name:\s*(.+)$/m)[1], executable: readlinkSync(`/proc/${pid}/exe`), affinity: status.match(/^Cpus_allowed_list:\s*(.+)$/m)[1] }]
      } catch (error) { if (error.code === 'ENOENT') return []; throw error }
    })
    if (entries.some(p => p.affinity !== limit.cpu)) throw new Error('A browser descendant escaped single-core affinity')
  }
  if (entries.length < 2) throw new Error('No browser descendants observed for CPU verification')
  return entries
}
