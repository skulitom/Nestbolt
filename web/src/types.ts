export type Point = [number, number];
export interface Polygon { outer: Point[]; holes: Point[][] }

export interface LibraryPart {
  id: string;
  source: string;
  polygon: Polygon;
  components?: Polygon[];
  area_mm2: number;
  bounds_mm: [number, number, number, number];
  holes: unknown[];
}
export interface SheetOutline { id: string; source: string; width_mm: number; height_mm: number; origin_mm: Point; outline_mm: Polygon[]; tolerance_mm: number }
export interface SheetImport { outlines: SheetOutline[]; warnings: string[]; imports: { file: string; report: ImportReport }[] }
export interface LightBurnProject { file: string; xml: string; unit_ids: string[]; fixed_top_level: number; mirror_x: boolean; mirror_y: boolean; layers: { index: number; image: boolean; name: string; mode: string; output: boolean; hidden: boolean; cuts: boolean; kerf_mm: number }[] }
export const partGeometry = (part: LibraryPart): Polygon[] => part.components?.length ? part.components : [part.polygon];
export interface Library { lightburn?: LightBurnProject; version: number; tolerance: number; parts: LibraryPart[]; warnings: string[]; imports?: { file: string; report: ImportReport }[]; sheet_outlines?: SheetOutline[] }
export interface ImportReport {
  /** In warning order for this file. Older saved projects can omit this field. */
  entries?: ImportEntry[];
  silent_join_mm: number;
  close_gaps_mm: number | null;
  closed_gaps: { source: string; from_mm: Point; to_mm: Point; size_mm: number }[];
  open_contours: { source: string; start_mm: Point; end_mm: Point; end_gap_mm: number; suggested_close_gaps_mm: number | null }[];
  layers?: ImportChannel[];
  colors?: ImportChannel[];
  selection_mode?: string;
  cleanup?: { duplicate_segments_removed: number; zero_length_segments_removed: number; overlapping_segments_merged: number; closed_path_overlaps_preserved?: number };
  units?: { declared: boolean; mm_per_unit: number; largest_dimension_in_drawing_units: number | null; possible_inches: boolean } | null;
}
export interface ImportSource { layer: string; entity: string; id?: string | null }
export type SkipReason =
  | 'unsupported' | 'rational_spline' | 'invalid_spline' | 'hidden'
  | 'not_cut_geometry' | 'paper_space' | 'no_stroke_or_fill' | 'ignored_layer';
export type ImportEntry =
  | { kind: 'skipped'; source: ImportSource; reason: SkipReason; count: number }
  | { kind: 'not_selected'; layer: string; color: string; count: number }
  | { kind: 'unknown_block'; source: ImportSource; block: string }
  | { kind: 'unresolved_use'; source: ImportSource; href: string }
  | { kind: 'fit_point_spline'; source: ImportSource }
  | { kind: 'polyline_width'; source: ImportSource }
  | { kind: 'outline_touches'; source: ImportSource; closed_under_mm: number }
  | { kind: 'outline_crosses'; source: ImportSource }
  | { kind: 'degenerate_contour'; source: ImportSource }
  | { kind: 'overlaps_kept'; sources: ImportSource[] }
  | { kind: 'cleanup' }
  | { kind: 'gap_closed'; gap: number }
  | { kind: 'open_contour'; contour: number }
  | { kind: 'duplicate_handle'; handle: string; count: number }
  | { kind: 'undefined_layer'; layer: string; count: number }
  | { kind: 'units_missing' }
  | { kind: 'possible_inches' }
  | { kind: 'svg_slice_not_clipped' };
export interface ImportChannel { name: string; entities: number; geometry_entities: number; selected_entities: number }
export interface ImportSelection { layers?: string[]; colors?: string[]; dxfUnitMm?: number; sheetLayers?: string[] }

export type Rotations =
  | { kind: 'free' }
  | { kind: 'list'; degrees: number[] }
  | { kind: 'step'; degrees: number };

export interface RequestPart { id: string; quantity: number; rotations: Rotations; allow_mirror: boolean; priority: number }
export interface Margins { left: number; right: number; bottom: number; top: number }
export interface RequestSheet {
  id?: string;
  from_import?: string;
  width_mm: number;
  height_mm: number;
  count?: number | null;
  margins_mm: Margins;
  defects_mm: Polygon[];
  /** A remnant's usable outline inside width x height; absent or empty is the full rectangle. */
  outline_mm?: Polygon[];
  outline_tolerance_mm?: number;
}
export type Mode = 'all' | 'fill_area' | 'fill_priority';
export interface NestRequest {
  name?: string;
  quick_start?: boolean;
  parts: RequestPart[];
  sheets: RequestSheet[];
  spacing_mm: number;
  common_line?: { kerf_mm: number; search_bonus?: boolean; allow_part_in_hole?: boolean };
  lead_in?: LeadOptions;
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
  placed_area: number;
  placed_priority: number;
}
export interface Report { valid: boolean; violation_count: number; violations: { code: string; message: string }[]; metrics: Metrics | null }
export interface CommonLineReport { sheet_id: string; kerf_mm: number; shared_length_mm: number; saved_length_mm: number; saved_fraction: number; cut_length_without_common_mm: number; cut_length_with_common_mm: number; contours_without_common: number; paths_with_common: number }
export interface LeadOptions { kerf_mm: number; length_mm: number; style: 'line' | 'arc'; outer_angle_degrees: number; hole_angle_degrees: number }
export type LeadPath = { kind: 'line'; from_mm: Point; to_mm: Point } | { kind: 'arc'; center_mm: Point; radius_mm: number; start_radians: number; sweep_radians: number };
export interface LeadReport {
  options: LeadOptions; expected_contours: number; reserved_contours: number; flagged_contours: number;
  validation: { valid: boolean; checked_contours: number; source_checked: boolean;
    coverage: { expected_contours: number; reserved_contours: number; flagged_contours: number } | null };
  parts: { part_id: string; copy_index: number; sheet_id: string; bounds_mm: [number, number, number, number];
    reservations: { contour_index: number; length_mm: number; shortened: boolean; paths: LeadPath[] }[];
    flags: { contour_index: number; reason: string }[] }[];
}
export interface NestResult { layout: Layout; validation: Report; seed: number; seconds: number; repeatable: boolean; parts_in_holes: number; common_line?: CommonLineReport[] | null; lead_in?: LeadReport | null }

export interface Project { lightburnOutline?: boolean;
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

export type OffcutMode = 'rectangular' | 'exact';
export interface OffcutOptions { mode?: OffcutMode; min_area_mm2?: number; min_dimension_mm?: number }
export interface Remnant {
  id: string;
  sheet_id: string;
  stock_id: string;
  mode: OffcutMode;
  width_mm: number;
  height_mm: number;
  area_mm2: number;
  origin_mm: Point;
  outline_mm: Polygon[];
}
export interface OffcutReport {
  mode: OffcutMode;
  min_area_mm2: number;
  min_dimension_mm: number;
  total_area_mm2: number;
  remnants: Remnant[];
}

export interface Pricing {
  sheet_cost?: number;
  material_cost_per_m2?: number;
  credit_offcut?: boolean;
  cut_speed_mm_per_min?: number;
  pierce_seconds?: number;
  machine_rate_per_hour?: number;
  setup_cost?: number;
  currency?: string;
}
export interface SheetQuote {
  sheet_id: string;
  stock_id: string;
  width_mm: number;
  height_mm: number;
  placed_parts: number;
  outer_contours: number;
  hole_contours: number;
  open_contours: number;
  pierce_count: number;
  gross_cut_length_mm: number;
  common_line_saved_mm: number;
  net_cut_length_mm: number;
  placed_area_mm2: number;
  sheet_area_mm2: number;
  utilization: number;
  trailing_offcut_area_mm2: number;
  trailing_offcut_height_mm: number;
  estimated_cut_seconds?: number;
  gross_material_cost?: number;
  offcut_credit?: number;
  net_material_cost?: number;
}
export interface CostBreakdown {
  currency: string;
  gross_material_cost: number;
  offcut_credit: number;
  net_material_cost: number;
  machine_cost: number;
  setup_cost: number;
  total_cost: number;
  cost_per_part?: number;
}
export interface JobQuote {
  version: number;
  job_name: string;
  sheets_used: number;
  placed_parts: number;
  requested_parts: number;
  outer_contours: number;
  hole_contours: number;
  open_contours: number;
  total_pierces: number;
  gross_cut_length_mm: number;
  common_line_saved_mm: number;
  net_cut_length_mm: number;
  placed_area_mm2: number;
  full_stock_area_mm2: number;
  material_area_mm2: number;
  trailing_offcut_area_mm2: number;
  utilization: number;
  estimated_cut_seconds?: number;
  costs?: CostBreakdown;
  sheets: SheetQuote[];
}
export interface QuoteResult { quote: JobQuote; csv: string; markdown: string }
export interface SheetPreset { label: string; w: number; h: number; margin: number }
