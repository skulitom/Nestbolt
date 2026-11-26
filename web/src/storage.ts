// Projects stay in this browser (IndexedDB); nothing is uploaded.
import type { Pricing, Project, SheetPreset } from './types';

const DB = 'nestbolt';
const STORE = 'projects';

function open(): Promise<IDBDatabase> {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open(DB, 1);
    request.onupgradeneeded = () => request.result.createObjectStore(STORE, { keyPath: 'name' });
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

async function run<T>(mode: IDBTransactionMode, body: (store: IDBObjectStore) => IDBRequest<T>): Promise<T> {
  const db = await open();
  return new Promise((resolve, reject) => {
    const tx = db.transaction(STORE, mode);
    const request = body(tx.objectStore(STORE));
    request.onsuccess = () => resolve(request.result);
    request.onerror = () => reject(request.error);
  });
}

export const saveProject = (project: Project) => run('readwrite', (s) => s.put(project));
export const loadProject = (name: string) => run<Project | undefined>('readonly', (s) => s.get(name));
export const deleteProject = (name: string) => run('readwrite', (s) => s.delete(name));
export const listProjects = () =>
  run<Project[]>('readonly', (s) => s.getAll()).then((all) =>
    all.map((p) => ({ name: p.name, savedAt: p.savedAt })).sort((a, b) => b.savedAt.localeCompare(a.savedAt)));

const PRESETS_KEY = 'nestbolt.customSheetPresets.v1';
const PRICING_KEY = 'nestbolt.shopPricing.v1';

export function loadSheetPresets(): SheetPreset[] {
  try {
    const raw = localStorage.getItem(PRESETS_KEY);
    if (!raw) return [];
    const parsed = JSON.parse(raw);
    return Array.isArray(parsed) ? parsed.filter((p) => p && typeof p.label === 'string' && p.w > 0 && p.h > 0) : [];
  } catch { return []; }
}

export function saveSheetPresets(presets: SheetPreset[]) {
  try { localStorage.setItem(PRESETS_KEY, JSON.stringify(presets)); } catch { /* ignore storage restrictions */ }
}

export function loadShopPricing(): Pricing {
  try {
    const raw = localStorage.getItem(PRICING_KEY);
    if (!raw) return {};
    const parsed = JSON.parse(raw);
    return parsed && typeof parsed === 'object' ? parsed : {};
  } catch { return {}; }
}

export function saveShopPricing(pricing: Pricing) {
  try { localStorage.setItem(PRICING_KEY, JSON.stringify(pricing)); } catch { /* ignore storage restrictions */ }
}
