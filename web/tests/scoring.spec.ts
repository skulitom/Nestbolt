import { expect, test } from '@playwright/test';
import { betterResult } from '../src/scoring.js';
import type { NestResult } from '../src/types.js';

const result = (area: number, priority: number, material: number, sheets = 1): NestResult => ({
  layout: { version: 1, units: 'mm', sheets: [], placements: [] }, seed: 0, seconds: 1, repeatable: true, parts_in_holes: 0,
  validation: { valid: true, violation_count: 0, violations: [], metrics: { sheets_used: sheets, placed_parts: 1, requested_parts: 2,
    normalized_material: material / 100, utilization: area / material, material_area: material, placed_area: area, placed_priority: priority } },
});

test('portfolio uses the native area and priority objectives with material as the tie breaker', () => {
  const small = result(50, 10, 70), large = result(72, 1, 100);
  expect(betterResult(large, small, 'fill_area')).toBe(true);
  expect(betterResult(large, small, 'fill_priority')).toBe(false);
  expect(betterResult(small, large, 'all')).toBe(true);
  expect(betterResult(result(72, 10, 100), small, 'fill_priority')).toBe(true);
  expect(betterResult(result(50, 10, 60), small, 'fill_area')).toBe(true);
  expect(betterResult(result(50, 10, 60), small, 'fill_priority')).toBe(true);
  expect(betterResult(result(50, 10, 60, 2), small, 'all')).toBe(false);
});
