// Projects stay in this browser (IndexedDB); nothing is uploaded.
import type { Project } from './types';

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
