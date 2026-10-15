// H5 only: call the pinned app's public SVG export service after the budget.
// No engine or export implementation is copied or patched. No DXF conversion.
import { writeFileSync } from 'node:fs'
import { join } from 'node:path'
import { createHash } from 'node:crypto'

export async function saveCutExports(page, native, output) {
  const exports = await page.evaluate(async native => {
    DeepNest.stop()
    const { ExportService } = await import('../build/ui/services/export.service.js')
    const actual = DeepNest.config()
    if (actual.spacing !== 0 || actual.mergeLines !== true) throw new Error('H5 requires native spacing zero and mergeLines enabled')
    const settings = { ...actual, units: 'mm', exportWithSheetBoundboarders: false,
      exportWithSheetsSpace: false, exportWithSheetsSpaceValue: 0 }
    const generate = mergeLines => {
      const service = new ExportService({ deepNest: DeepNest, svgParser: SvgParser,
        config: { getSync: key => key === 'mergeLines' ? mergeLines : settings[key] } })
      return service.generateSvgExport(native)
    }
    return { merged: generate(true), unmerged: generate(false),
      native_merged_length: native.mergedLength ?? 0, settings,
      sheet_bounds: native.placements.map(p => DeepNest.parts[p.sheet].bounds),
      selected_candidate: native }
  }, native)
  const hashes = {}
  for (const kind of ['merged', 'unmerged']) {
    const name = `cuts-${kind}.svg`
    const bytes = Buffer.from(exports[kind] + '\n')
    writeFileSync(join(output, name), bytes)
    hashes[name] = createHash('sha256').update(bytes).digest('hex')
  }
  return { native_merged_length: exports.native_merged_length, settings: exports.settings,
    sheet_bounds: exports.sheet_bounds, selected_candidate: exports.selected_candidate,
    files: hashes, format: 'svg', network_conversion: false,
    service: 'build/ui/services/export.service.js: ExportService.generateSvgExport' }
}
