// Native release archives with fixed metadata. Node 20+, no external archiver.
// Adapted from skulitom's MIT-licensed Inkbolt distribution scripts.
import { readFile } from 'node:fs/promises';
import { spawnSync } from 'node:child_process';
import { gzipSync } from 'node:zlib';
import { fileURLToPath } from 'node:url';
import path from 'node:path';
import { cargoVersion, root, textFile, writeUnchangedOrNew } from './build.mjs';
import { PROTOCOL } from './mcp-client.mjs';
import { writeZip } from './zip.mjs';

export const TARGETS = {
  'x86_64-pc-windows-msvc': { platform: 'win32', arch: 'x64', suffix: '.exe', extension: 'zip' },
  'x86_64-unknown-linux-gnu': { platform: 'linux', arch: 'x64', suffix: '', extension: 'tar.gz' },
  'aarch64-apple-darwin': { platform: 'darwin', arch: 'arm64', suffix: '', extension: 'tar.gz' }
};
export const DOCUMENTS = ['LICENSE', 'README.md', 'THIRD_PARTY_NOTICES', 'llms.txt'];

// Short root-level names fit the ustar name field; preserve the executable bits.
export function writeTarGz(files, executables) {
  const blocks = [], octal = (value, length) => value.toString(8).padStart(length - 1, '0') + '\0';
  for (const [name, data] of [...files].sort(([a], [b]) => a < b ? -1 : a > b ? 1 : 0)) {
    if (!/^[A-Za-z0-9_.-]{1,100}$/.test(name)) throw new Error(`Unsupported tar entry name: ${name}`);
    const header = Buffer.alloc(512);
    header.write(name); header.write(octal(executables.has(name) ? 0o755 : 0o644, 8), 100);
    header.write(octal(0, 8), 108); header.write(octal(0, 8), 116);
    header.write(octal(data.length, 12), 124); header.write(octal(315532800, 12), 136);
    header.fill(32, 148, 156); header.write('0', 156); header.write('ustar\0' + '00', 257);
    header.write(octal(header.reduce((sum, byte) => sum + byte, 0), 7) + ' ', 148);
    blocks.push(header, data, Buffer.alloc((512 - data.length % 512) % 512));
  }
  blocks.push(Buffer.alloc(1024));
  const bytes = gzipSync(Buffer.concat(blocks), { level: 9 });
  bytes[9] = 3; // Fixed gzip OS marker (Unix).
  return bytes;
}

function run(binary, args, input, base) {
  const result = spawnSync(path.resolve(binary), args, { cwd: base, input, encoding: 'utf8', timeout: 15000, maxBuffer: 8 * 1024 * 1024, windowsHide: true });
  if (result.error) throw result.error;
  return result;
}

/** Both executables start and report the release version. */
export function smoke({ cli, server, version, base = root }) {
  const printed = run(cli, ['--version'], '', base);
  if (printed.status !== 0 || printed.stdout.trim() !== `nestbolt ${version}`) throw new Error(`CLI version check failed: ${printed.stdout}${printed.stderr}`);
  const initialize = JSON.stringify({ jsonrpc: '2.0', id: 1, method: 'initialize', params: { protocolVersion: PROTOCOL, capabilities: {}, clientInfo: { name: 'nestbolt-archive', version: '1.0.0' } } });
  const reply = JSON.parse(run(server, [], initialize + '\n', base).stdout.split('\n')[0]);
  if (reply.result?.serverInfo?.version !== version) throw new Error(`MCP server version check failed: ${JSON.stringify(reply)}`);
}

export async function archive({ target, cli, server, base = root, out = path.join(root, 'target/dist/release'), check = true }) {
  const spec = TARGETS[target];
  if (!spec) throw new Error(`Unsupported release target: ${target}`);
  if (!cli || !server) throw new Error('--cli and --server are required.');
  const version = await cargoVersion(base);
  if (check) {
    if (process.platform !== spec.platform || process.arch !== spec.arch) throw new Error(`Build ${target} on its native runner.`);
    smoke({ cli, server, version, base });
  }
  const names = [`nestbolt${spec.suffix}`, `nestbolt-mcp${spec.suffix}`];
  const files = new Map([[names[0], await readFile(cli)], [names[1], await readFile(server)]]);
  for (const name of DOCUMENTS) files.set(name, await textFile(path.join(base, name)));
  const bytes = spec.extension === 'zip' ? writeZip(files) : writeTarGz(files, new Set(names));
  const file = path.resolve(out, `nestbolt-v${version}-${target}.${spec.extension}`);
  await writeUnchangedOrNew(file, bytes);
  return { file, bytes };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  Promise.resolve().then(async () => {
    const options = {}, args = process.argv.slice(2);
    for (let i = 0; i < args.length; i += 2) {
      if (!['--target', '--cli', '--server', '--out'].includes(args[i]) || !args[i + 1] || args[i + 1].startsWith('--') || Object.hasOwn(options, args[i].slice(2))) throw new Error(`Unknown or incomplete option: ${args[i]}`);
      options[args[i].slice(2)] = args[i + 1];
    }
    const result = await archive(options); console.log(`${result.file}: ${result.bytes.length} bytes; CLI and MCP server version checks passed.`);
  }).catch(error => { console.error(error.message); process.exitCode = 1; });
}
