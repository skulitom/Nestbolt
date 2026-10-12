export type Point = [number, number];
export interface Polygon { outer: Point[]; holes: Point[][] }

export interface LibraryPart {
  id: string;
  source: string;
  polygon: Polygon;
  area_mm2: number;
  bounds_mm: [number, number, number, number];
  holes: unknown[];
}
export interface Library { version: number; tolerance: number; parts: LibraryPart[]; warnings: string[] }

export type Rotations =
  | { kind: 'free' }
  | { kind: 'list'; degrees: number[] }
  | { kind: 'step'; degrees: number };

export interface RequestPart { id: string; quantity: number; rotations: Rotations; allow_mirror: boolean; priority: number }
export interface Margins { left: number; right: number; bottom: number; top: number }
export interface RequestSheet {
  id?: string;
  width_mm: number;
  height_mm: number;
  count?: number | null;
  margins_mm: Margins;
  defects_mm: Polygon[];
  /** A remnant's usable outline inside width x height; absent or empty is the full rectangle. */
  outline_mm?: Polygon[];
}
export type Mode = 'all' | 'fill_area' | 'fill_priority';
export interface NestRequest {
  name?: string;
  parts: RequestPart[];
  sheets: RequestSheet[];
  spacing_mm: number;
  edge_spacing_mm: number;
  mode: Mode;
}

export interface Transform { translation: Point; rotation_radians: number; mirrored: boolean }
export interface Placement { part_id: string; copy_index: number; sheet_id: string; transform: Transform }
export interface Layout { version: number; units: string; sheets: { id: string; stock_id: string }[]; placements: Placement[] }
export interface Metrics {
  sheets_used: number;
  placed_parts: number;
  requested_parts: number;
  normalized_material: number;
  utilization: number;
  material_area: number;
}
export interface Report { valid: boolean; violation_count: number; violations: { code: string; message: string }[]; metrics: Metrics | null }
export interface NestResult { layout: Layout; validation: Report; seed: number; seconds: number; repeatable: boolean; parts_in_holes: number }

export interface Project {
  version: 1;
  name: string;
  library: Library | null;
  request: NestRequest;
  result: NestResult | null;
  savedAt: string;
}

/** A bundled example from web/public/examples/examples.json. */
export interface Example {
  id: string;
  title: string;
  summary: string;
  file: string;
  /** Copies by drawing element id; others get `default_quantity` or 1. */
  quantities: Record<string, number>;
  default_quantity?: number;
  rotations: Rotations;
  overrides?: Record<string, Rotations>;
  sheet: [number, number];
  margin: number;
  spacing: number;
  edge: number;
  seconds: number;
}
