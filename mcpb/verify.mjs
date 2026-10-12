// Verify the Windows bundle in fresh folders under target/, never the user's drawings.
// Adapted from skulitom's MIT-licensed Inkbolt distribution scripts.
import assert from 'node:assert/strict';
import { readdirSync, lstatSync } from 'node:fs';
import { readFile, writeFile, mkdir, mkdtemp, readdir, rm } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { root, cargoVersion, VERSION, SERVER } from './build.mjs';
import { readZip, sha256 } from './zip.mjs';

import { inside, mcpFolders, startMcp } from './mcp-client.mjs';
export { inside } from './mcp-client.mjs';

export const ENTRIES = ['LICENSE', 'THIRD_PARTY_NOTICES', 'manifest.json', SERVER];
const SMOKE_SVG = '<svg xmlns="http://www.w3.org/2000/svg" width="100mm" height="50mm" viewBox="0 0 100 50">'
  + '<rect x="5" y="5" width="40" height="20"/><circle cx="70" cy="25" r="10"/></svg>\n';

export function checkManifest(manifest, version) {
  for (const key of ['name', 'version', 'description', 'display_name', 'long_description']) assert.ok(typeof manifest[key] === 'string' && manifest[key], `manifest.${key} is required`);
  assert.equal(manifest.manifest_version, '0.3');
  assert.equal(manifest.name, 'nestbolt');
  assert.equal(manifest.display_name, 'Nestbolt');
  assert.equal(manifest.version, version, 'manifest version must equal Cargo.toml version');
  assert.match(manifest.version, VERSION);
  assert.ok(manifest.author?.name && manifest.author?.url, 'manifest author is required');
  for (const url of [manifest.author.url, manifest.repository?.url, manifest.homepage, manifest.documentation, manifest.support]) assert.equal(new URL(url).protocol, 'https:');
  assert.equal(manifest.license, 'MIT');
  assert.equal(manifest.server?.type, 'binary');
  assert.equal(manifest.server.entry_point, SERVER);
  assert.deepEqual(manifest.server.mcp_config, {
    command: '${__dirname}/' + SERVER,
    args: [],
    env: { NESTBOLT_WORKSPACE: '${user_config.workspace}' }
  });
  assert.deepEqual(manifest.compatibility?.platforms, ['win32']);
  assert.equal(manifest.user_config?.workspace?.type, 'directory');
  assert.equal(manifest.user_config.workspace.required, true);
  assert.equal(manifest.user_config.workspace.default, '${HOME}');
  assert.ok(manifest.user_config.workspace.title && manifest.user_config.workspace.description);
  assert.ok(Array.isArray(manifest.tools) && manifest.tools.length > 0, 'manifest tools are required');
  assert.equal(new Set(manifest.tools.map(tool => tool.name)).size, manifest.tools.length, 'manifest tool names must be unique');
  assert.ok(manifest.tools.every(tool => typeof tool.name === 'string' && tool.name && typeof tool.description === 'string' && tool.description && !/[\r\n]/.test(tool.description)), 'tools need names and one-line descriptions');
}

// Observe repository files outside the owned temporary directory. This is a write
// regression check, not an OS sandbox or a system-wide filesystem monitor. Build,
// benchmark and package folders are skipped: other local jobs may write there.
const VOLATILE = new Set(['.git', '.cache', 'node_modules', 'output', 'target']);
function inventory(base, excluded) {
  const result = {};
  function walk(directory) {
    for (const entry of readdirSync(directory, { withFileTypes: true }).sort((a, b) => a.name.localeCompare(b.name))) {
      const file = path.join(directory, entry.name);
      if (file === excluded || (entry.isDirectory() && VOLATILE.has(entry.name) && directory === root)) continue;
      const info = lstatSync(file);
      if (entry.isDirectory()) { result[path.relative(base, file)] = 'directory'; walk(file); }
      else result[path.relative(base, file)] = [info.size, info.mtimeMs, info.ctimeMs];
    }
  }
  walk(base);
  return result;
}

async function call(client, name, args) {
  const reply = await client.request('tools/call', { name, arguments: args });
  assert.equal(reply.isError ?? false, false, `${name} failed: ${JSON.stringify(reply)}`);
  return reply.structuredContent ?? JSON.parse(reply.content.find(part => part.type === 'text').text);
}

export async function verifyMcpb(bundle, { allowSkip = false } = {}) {
  if (process.platform !== 'win32') {
    if (allowSkip) return { skipped: true };
    throw new Error('Windows only: this bundle contains a Windows x64 executable. Use --allow-skip to skip explicitly.');
  }
  const entries = readZip(await readFile(bundle));
  assert.deepEqual([...entries.keys()].sort(), [...ENTRIES].sort(), 'Unexpected or missing bundle entries');
  const manifest = JSON.parse(entries.get('manifest.json').read());
  checkManifest(manifest, await cargoVersion());
  const tempRoot = path.join(root, 'target');
  await mkdir(tempRoot, { recursive: true });
  const temp = await mkdtemp(path.join(tempRoot, 'mcpb-verify-'));
  let client;
  try {
    const extension = path.join(temp, 'extension');
    await mkdir(extension);
    const folders = await mcpFolders(temp);
    const { workspace, cwd, home, scratch } = folders;
    for (const [name, entry] of entries) {
      assert.ok(!/[\\:]/.test(name) && !name.split('/').some(part => ['', '.', '..'].includes(part)), `Unsafe bundle path: ${name}`);
      const file = path.resolve(extension, name);
      assert.ok(inside(extension, file), `Bundle path escapes extraction folder: ${name}`);
      await mkdir(path.dirname(file), { recursive: true });
      await writeFile(file, entry.read(), { flag: 'wx' });
    }
    await writeFile(path.join(workspace, 'smoke.svg'), SMOKE_SVG, { flag: 'wx' });
    const before = inventory(root, temp);
    client = startMcp({ manifest, extension, ...folders });
    await client.initialize();
    const tools = await client.listTools();
    assert.deepEqual(new Set(tools.map(tool => tool.name)), new Set(manifest.tools.map(tool => tool.name)), 'manifest tools must match live tools');
    const imported = await call(client, 'import_parts', { paths: ['smoke.svg'], library_path: 'library.json' });
    assert.equal(imported.part_count, 2);
    const request = { sheets: [{ width_mm: 200, height_mm: 100 }], spacing_mm: 1, edge_spacing_mm: 1 };
    const nested = await call(client, 'nest', { library_path: 'library.json', request, time_budget_s: 2, seed: 0, out_dir: 'run' });
    assert.equal(nested.validation.valid, true, 'nest must return a valid layout');
    assert.deepEqual(nested.files, ['run/sheet-0.svg', 'run/sheet-0.dxf']);
    const checked = await call(client, 'validate_layout', { library_path: 'library.json', request, layout_path: 'run/layout.json' });
    assert.equal(checked.valid, true);
    await client.stop(); client = null;
    assert.deepEqual(inventory(root, temp), before, 'The server changed repository files outside its temporary folders');
    assert.deepEqual((await readdir(workspace)).sort(), ['library.json', 'run', 'smoke.svg']);
    assert.deepEqual((await readdir(path.join(workspace, 'run'))).sort(), ['job.json', 'layout.json', 'report.json', 'sheet-0.dxf', 'sheet-0.svg']);
    for (const directory of [cwd, home, scratch]) assert.deepEqual(await readdir(directory), [], `Unexpected writes in ${directory}`);
    assert.deepEqual((await readdir(temp)).sort(), ['cwd', 'extension', 'home', 'tmp', 'workspace']);
    for (const [name, entry] of entries) assert.equal(sha256(await readFile(path.join(extension, name))), sha256(entry.read()), `The server changed ${name}`);
    assert.deepEqual(Object.keys(inventory(extension)).sort(), [...entries.keys(), 'server'].map(name => name.replaceAll('/', path.sep)).sort(), 'The server added files to the bundle');
    return { version: manifest.version, tools: tools.length, files: entries.size };
  } finally {
    try { await client?.stop(); } finally {
      assert.ok(inside(tempRoot, temp), 'Refusing to remove a folder outside target/');
      await rm(temp, { recursive: true, force: true });
    }
  }
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2), allowSkip = args.includes('--allow-skip'), files = args.filter(arg => arg !== '--allow-skip');
  Promise.resolve().then(() => {
    if (files.length !== 1 || files[0].startsWith('--') || args.length > 2) throw new Error('Usage: node mcpb/verify.mjs <bundle> [--allow-skip]');
    return verifyMcpb(files[0], { allowSkip });
  }).then(result => console.log(result.skipped ? 'Windows only: explicitly skipped.' : `MCPB verified: Nestbolt ${result.version}, ${result.tools} tools, ${result.files} files; import, nest and validation passed.`))
    .catch(error => { console.error(`MCPB verification failed: ${error.message}`); process.exitCode = 1; });
}
