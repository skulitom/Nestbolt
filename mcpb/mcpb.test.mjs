// Adapted from skulitom's MIT-licensed Inkbolt distribution tests.
import test, { before, after } from 'node:test';
import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { readFile, writeFile, mkdir, mkdtemp, rm, access, link } from 'node:fs/promises';
import path from 'node:path';
import { gunzipSync } from 'node:zlib';
import { archive, DOCUMENTS, smoke } from './archive.mjs';
import { root, cargoVersion, assembleMcpb, buildMcpb, registryEntry, BUNDLE_NAME, SERVER, VERSION, json, mergeTools } from './build.mjs';
import { releasePolicy } from './release.mjs';
import { readZip, writeZip, sha256 } from './zip.mjs';
import { checkManifest, inside, verifyMcpb, ENTRIES } from './verify.mjs';

let temp, base, binary, template, metadata, build, fixtureTools;
// Packaging fixtures need no executable; the real-binary test covers discovery.
const assembleFixture = options => assembleMcpb(options, async () => fixtureTools);
const buildFixture = options => buildMcpb(options, async () => fixtureTools);
const version = '7.8.9';
const writeJSON = (file, value) => writeFile(file, json(value));
const cargo = value => `[workspace]\nmembers = ["a"]\n\n[workspace.package]\nversion = "${value}"\nedition = "2024"\n\n[workspace.dependencies]\nunused = "0.1.0"\n`;
before(async () => {
  await mkdir(path.join(root, 'target'), { recursive: true });
  temp = await mkdtemp(path.join(root, 'target/mcpb-test-'));
  base = path.join(temp, 'source');
  await mkdir(path.join(base, 'mcpb'), { recursive: true });
  template = JSON.parse(await readFile(path.join(root, 'mcpb/manifest.json')));
  fixtureTools = [...template.tools.slice(1).reverse(), { name: 'new_tool', description: 'New tool sentence. More detail.' }];
  metadata = { ...JSON.parse(await readFile(path.join(root, 'server.json'))), version: '0.0.1' };
  await writeJSON(path.join(base, 'mcpb/manifest.json'), template);
  await writeJSON(path.join(base, 'server.json'), metadata);
  await writeFile(path.join(base, 'Cargo.toml'), cargo(version));
  for (const name of DOCUMENTS) await writeFile(path.join(base, name), `Fixture ${name}\r\n`);
  binary = path.join(base, 'stand-in.exe');
  await writeFile(binary, Buffer.from([77, 90, 0, 13, 10, 255]));
  build = await buildFixture({ base, binary, out: path.join(temp, 'first') });
});
after(async () => {
  if (temp) {
    assert.ok(inside(path.join(root, 'target'), temp));
    await rm(temp, { recursive: true, force: true });
  }
});

test('metadata stays package-free with the required identity and short description', async () => {
  const server = JSON.parse(await readFile(path.join(root, 'server.json')));
  assert.equal(server.name, 'io.github.skulitom/nestbolt');
  assert.equal(server.$schema, 'https://static.modelcontextprotocol.io/schemas/2025-12-11/server.schema.json');
  assert.equal(server.repository.id, '1414822696');
  assert.equal(Object.hasOwn(server, 'packages'), false);
  assert.ok(server.description.length > 0 && server.description.length <= 100);
});

test('workspace version comes from [workspace.package]', async () => {
  assert.match(await cargoVersion(), VERSION);
  assert.equal(await cargoVersion(base), version);
});

test('manifest template has no version and has valid binary-server fields', async () => {
  assert.equal(Object.hasOwn(template, 'version'), false);
  checkManifest({ ...template, version: await cargoVersion() }, await cargoVersion());
});

test('manifest lists exactly the server tools', async () => {
  const source = await readFile(path.join(root, 'crates/mcp/src/main.rs'), 'utf8');
  const names = [...source.matchAll(/#\[tool\([\s\S]*?\)\]\s*async fn (\w+)/g)].map(match => match[1]);
  assert.deepEqual(new Set(template.tools.map(tool => tool.name)), new Set(names));
});

test('tool merge keeps curated descriptions, drops absent tools and follows live order without mutation', () => {
  const overrides = [
    { name: 'first', description: 'Curated first.' },
    { name: 'dropped', description: 'Retired.' },
    { name: 'last', description: 'Curated last.' }
  ];
  const live = [
    { name: 'last', description: 'Server last.', inputSchema: {} },
    { name: 'first', description: 'Server first.' }
  ];
  const before = structuredClone({ overrides, live });
  assert.deepEqual(mergeTools(overrides, live), {
    tools: [overrides[2], overrides[0]], added: [], dropped: ['dropped']
  });
  assert.deepEqual({ overrides, live }, before);
});

test('new tool descriptions use the first sentence and normalize whitespace', () => {
  for (const [description, expected] of [
    ['  Nest a\nsmall job. Keep the source.  ', 'Nest a small job.'],
    ['Inspect it! Then edit.', 'Inspect it!'],
    ['Ready? More details.', 'Ready?'],
    ['Spacing of 1.5 mm. More details.', 'Spacing of 1.5 mm.'],
    ['  No final punctuation  ', 'No final punctuation']
  ]) {
    assert.deepEqual(mergeTools([], [{ name: 'new_tool', description }]), {
      tools: [{ name: 'new_tool', description: expected }], added: ['new_tool'], dropped: []
    });
  }
});

test('new tool descriptions stop at a whole word within 160 characters', () => {
  const merge = description => mergeTools([], [{ name: 'new_tool', description }]).tools[0].description;
  const exact = 'word '.repeat(31) + 'final';
  assert.equal(exact.length, 160);
  assert.equal(merge(exact), exact);
  assert.equal(merge(exact + ' more words.'), exact);
  assert.equal(merge('word '.repeat(31) + 'longerword.'), 'word '.repeat(31).trim());
  assert.throws(() => merge('x'.repeat(161)), /word boundary/);
});

test('tool merge rejects empty catalogs, invalid names and duplicates', () => {
  for (const live of [[], undefined, {}]) assert.throws(() => mergeTools([], live), /no tools/);
  for (const name of ['', '_nest', 'nest_', 'Nest', 'bad-name', 'bad.name', 'é', 'bad\n', ' bad', 'bad__name', 7, null, undefined]) {
    assert.throws(() => mergeTools([], [{ name, description: 'Description.' }]), /Invalid tool name/);
  }
  assert.throws(() => mergeTools([], [null]), /Invalid tool name/);
  const tool = { name: 'valid_tool_123', description: 'Description.' };
  assert.deepEqual(mergeTools([], [tool]).tools, [tool]);
  assert.throws(() => mergeTools([], [tool, tool]), /Duplicate tool name/);
});

test('new tools require usable descriptions while curated descriptions remain exact', () => {
  for (const description of [undefined, null, '', ' \n ']) {
    assert.throws(() => mergeTools([], [{ name: 'new_tool', description }]), /server description/);
  }
  const override = { name: 'known', description: 'Curated text. A second sentence is retained.' };
  assert.deepEqual(mergeTools([override], [{ name: override.name }]).tools, [override]);
});

test('two builds are identical, with exactly the required entries and checksum', async () => {
  const second = await buildFixture({ base, binary, out: path.join(temp, 'second') });
  assert.deepEqual(second.bytes, build.bytes);
  const entries = readZip(build.bytes);
  assert.deepEqual([...entries.keys()], [...ENTRIES].sort());
  assert.deepEqual(entries.get(SERVER).read(), await readFile(binary));
  assert.equal(entries.get('LICENSE').read().toString(), 'Fixture LICENSE\n');
  const generated = JSON.parse(entries.get('manifest.json').read());
  assert.equal(generated.version, version);
  assert.deepEqual(generated.tools, mergeTools(template.tools, fixtureTools).tools);
  assert.deepEqual(build.added, ['new_tool']);
  assert.deepEqual(build.dropped, [template.tools[0].name]);
  assert.equal(await readFile(`${build.bundle}.sha256`, 'utf8'), `${sha256(build.bytes)}  ${BUNDLE_NAME}\n`);
  await writeFile(path.join(base, 'LICENSE'), 'Fixture LICENSE\n');
  assert.deepEqual((await assembleFixture({ base, binary })).bytes, build.bytes);
  await buildFixture({ base, binary, out: path.join(temp, 'first') });
});

test('builder refuses a template version, invalid package versions and missing binaries', async () => {
  try {
    await writeJSON(path.join(base, 'mcpb/manifest.json'), { ...template, version });
    await assert.rejects(assembleFixture({ base, binary }), /must not contain version/);
  } finally { await writeJSON(path.join(base, 'mcpb/manifest.json'), template); }
  try {
    for (const value of ['1.0', 'v1.0.0', '01.0.0', '1.0.0-beta.01', '1.0.0-', '1.0.0-alpha..1', '1.0.0+build', '1.0.0-alpha/1', '1.0.0-alpha_1']) {
      await writeFile(path.join(base, 'Cargo.toml'), cargo(value));
      await assert.rejects(assembleFixture({ base, binary }), /version must have the form X.Y.Z/);
    }
    await writeFile(path.join(base, 'Cargo.toml'), '[package]\nversion = "1.2.3"\n');
    await assert.rejects(cargoVersion(base), /version must have the form X.Y.Z/);
  } finally { await writeFile(path.join(base, 'Cargo.toml'), cargo(version)); }
  await assert.rejects(assembleFixture({ base }), /--binary is required/);
  await assert.rejects(assembleFixture({ base, binary: path.join(temp, 'missing.exe') }), /Missing binary/);
});

test('existing different artifacts are preserved', async () => {
  const out = path.join(temp, 'occupied'); await mkdir(out);
  const file = path.join(out, BUNDLE_NAME); await writeFile(file, 'keep');
  await assert.rejects(buildFixture({ base, binary, out }), /already exists with different contents/);
  assert.equal(await readFile(file, 'utf8'), 'keep');
});

test('native archives are deterministic and carry both binaries, docs and licenses', async () => {
  const server = path.join(base, 'server-stand-in.exe');
  await writeFile(server, Buffer.from([77, 90, 1, 2, 3]));
  for (const target of ['x86_64-pc-windows-msvc', 'x86_64-unknown-linux-gnu', 'aarch64-apple-darwin']) {
    const options = { base, cli: binary, server, target, check: false, out: path.join(temp, 'archives') };
    const first = await archive(options), second = await archive(options);
    assert.deepEqual(first.bytes, second.bytes);
    const isWindows = target.includes('windows'), entries = new Map(), suffix = isWindows ? '.exe' : '';
    if (isWindows) {
      for (const [name, entry] of readZip(first.bytes)) entries.set(name, entry.read());
    } else {
      const tar = gunzipSync(first.bytes);
      const string = (start, size) => tar.subarray(start, start + size).toString().replace(/\0.*$/s, '');
      for (let at = 0; tar[at];) {
        const name = string(at, 100), size = parseInt(string(at + 124, 12), 8);
        assert.equal(string(at + 257, 5), 'ustar');
        assert.equal(parseInt(string(at + 100, 8), 8), name.startsWith('nestbolt') ? 0o755 : 0o644);
        const header = Buffer.from(tar.subarray(at, at + 512)), sum = parseInt(string(at + 148, 8), 8);
        header.fill(32, 148, 156);
        assert.equal(header.reduce((a, b) => a + b, 0), sum);
        entries.set(name, tar.subarray(at + 512, at + 512 + size));
        at += 512 + Math.ceil(size / 512) * 512;
      }
    }
    assert.deepEqual([...entries.keys()].sort(), [...DOCUMENTS, `nestbolt${suffix}`, `nestbolt-mcp${suffix}`].sort());
    assert.deepEqual(entries.get(`nestbolt${suffix}`), await readFile(binary));
    assert.deepEqual(entries.get(`nestbolt-mcp${suffix}`), await readFile(server));
    assert.equal(entries.get('README.md').toString(), 'Fixture README.md\n');
  }
});

test('registry entry stamps Cargo version despite stale metadata and preserves inputs', async () => {
  const out = path.join(temp, 'server.registry.json'), before = await readFile(path.join(base, 'server.json'));
  const entry = await registryEntry({ base, tag: `v${version}`, bundle: build.bundle, out });
  assert.equal(entry.version, version);
  assert.deepEqual(entry.packages, [{ registryType: 'mcpb', identifier: `https://github.com/skulitom/Nestbolt/releases/download/v${version}/${BUNDLE_NAME}`, version, fileSha256: sha256(build.bytes), transport: { type: 'stdio' } }]);
  assert.deepEqual(JSON.parse(await readFile(out)), entry);
  assert.deepEqual(await readFile(path.join(base, 'server.json')), before);
  await registryEntry({ base, tag: `v${version}`, bundle: build.bundle, out });
});

test('a Cargo-only version bump needs no manifest or metadata edits', async () => {
  try {
    await writeFile(path.join(base, 'Cargo.toml'), cargo('7.9.0'));
    const next = await buildFixture({ base, binary, out: path.join(temp, 'bumped') });
    const entry = await registryEntry({ base, tag: 'v7.9.0', bundle: next.bundle, out: path.join(temp, 'bumped-entry.json') });
    assert.equal(next.manifest.version, '7.9.0');
    assert.equal(entry.version, '7.9.0');
    assert.equal(entry.packages[0].version, '7.9.0');
    assert.deepEqual(JSON.parse(await readFile(path.join(base, 'server.json'))), metadata);
    assert.deepEqual(JSON.parse(await readFile(path.join(base, 'mcpb/manifest.json'))), template);
  } finally { await writeFile(path.join(base, 'Cargo.toml'), cargo(version)); }
});

test('preview versions survive bundle, all native archives and generated metadata', async () => {
  const preview = '0.2.0-alpha.1';
  try {
    await writeFile(path.join(base, 'Cargo.toml'), cargo(preview));
    const next = await buildFixture({ base, binary, out: path.join(temp, 'preview') });
    checkManifest(next.manifest, preview);
    assert.equal(JSON.parse(readZip(next.bytes).get('manifest.json').read()).version, preview);
    const entry = await registryEntry({ base, tag: `v${preview}`, bundle: next.bundle, out: path.join(temp, 'preview-entry.json') });
    assert.equal(entry.version, preview);
    assert.equal(entry.packages[0].version, preview);
    assert.equal(entry.packages[0].identifier, `https://github.com/skulitom/Nestbolt/releases/download/v${preview}/${BUNDLE_NAME}`);
    for (const [target, extension] of [['x86_64-pc-windows-msvc', 'zip'], ['x86_64-unknown-linux-gnu', 'tar.gz'], ['aarch64-apple-darwin', 'tar.gz']]) {
      const packed = await archive({ target, cli: binary, server: binary, base, out: path.join(temp, 'preview-archives'), check: false });
      assert.equal(path.basename(packed.file), `nestbolt-v${preview}-${target}.${extension}`);
      assert.deepEqual(await readFile(packed.file), packed.bytes);
    }
    assert.deepEqual(JSON.parse(await readFile(path.join(base, 'server.json'))), metadata);
    assert.deepEqual(JSON.parse(await readFile(path.join(base, 'mcpb/manifest.json'))), template);
  } finally { await writeFile(path.join(base, 'Cargo.toml'), cargo(version)); }
});

test('preview releases never replace Latest and stable tags sort numerically', () => {
  const tags = ['v0.2.0', 'v0.10.0', 'v0.1.0', 'v1.0.0-alpha.1', 'not-a-version', 'v01.0.0'];
  assert.deepEqual(releasePolicy('v1.0.0-alpha.1', tags), { prerelease: true, latest: false });
  assert.deepEqual(releasePolicy('v0.10.0', tags), { prerelease: false, latest: true });
  assert.deepEqual(releasePolicy('v0.2.0', tags), { prerelease: false, latest: false });
  assert.deepEqual(releasePolicy('v0.2.0-rc.1', ['v0.2.0-rc.1']), { prerelease: true, latest: false });
  assert.throws(() => releasePolicy('v0.2.1', tags), /existing valid version tag/);
  for (const tag of ['v01.0.0', 'v1.0.0-alpha.01', 'v1.0.0-alpha\n', 'v1.0.0+build']) {
    assert.throws(() => releasePolicy(tag, [...tags, tag]), /existing valid version tag/);
  }
});

test('registry entry rejects bad tags, version mismatch and packages in metadata', async () => {
  const options = { base, tag: `v${version}`, bundle: build.bundle, out: path.join(temp, 'refused.json') };
  for (const tag of ['7.8.9', 'v1.2', 'v01.2.3', 'v1.2.3-beta.01', '../v1.2.3', 'v1.2.3\n']) await assert.rejects(registryEntry({ ...options, tag }), /Tag must have the form/);
  await assert.rejects(registryEntry({ ...options, tag: 'v7.8.10' }), /Tag and Cargo.toml versions must match/);
  try {
    await writeJSON(path.join(base, 'server.json'), { ...metadata, packages: [] });
    await assert.rejects(registryEntry(options), /metadata-only/);
  } finally { await writeJSON(path.join(base, 'server.json'), metadata); }
  const files = new Map([...readZip(build.bytes)].map(([name, entry]) => [name, entry.read()]));
  files.set('manifest.json', json({ ...build.manifest, version: '7.8.8' }));
  const oldBundle = path.join(temp, 'old.mcpb'); await writeFile(oldBundle, writeZip(files));
  await assert.rejects(registryEntry({ ...options, bundle: oldBundle }), /Bundle manifest version must match/);
  files.delete('manifest.json'); await writeFile(oldBundle, writeZip(files));
  await assert.rejects(registryEntry({ ...options, bundle: oldBundle }), /Bundle has no manifest/);
});

test('registry output cannot overwrite metadata or bundle, including hard-link aliases', async () => {
  const alias = path.join(temp, 'alias.json'); await link(path.join(base, 'server.json'), alias);
  const outputs = [path.join(base, 'server.json'), build.bundle, alias, path.join(base, 'mcpb/../server.json')];
  if (process.platform === 'win32') outputs.push(path.join(base, 'SERVER.JSON'));
  for (const out of outputs) {
    const before = await readFile(out);
    await assert.rejects(registryEntry({ base, tag: `v${version}`, bundle: build.bundle, out }), /must not overwrite/);
    assert.deepEqual(await readFile(out), before);
  }
});

test('ZIP reader rejects malformed archives and detects CRC corruption', () => {
  assert.throws(() => readZip(Buffer.from('no')), /Not a ZIP/);
  const bytes = writeZip(new Map([['small', Buffer.from('abc')]]));
  bytes[30 + Buffer.byteLength('small')] ^= 1;
  assert.throws(() => readZip(bytes).get('small').read(), /damaged/);
});

test('verifier rejects incompatible manifest versions and launch commands', () => {
  assert.throws(() => checkManifest({ ...template, version: '1.0.0' }, '1.0.1'), /version must equal/);
  assert.throws(() => checkManifest({ ...build.manifest, compatibility: { platforms: ['linux'] } }, version));
  assert.throws(() => checkManifest({ ...build.manifest, server: { ...template.server, mcp_config: { command: 'unexpected' } } }, version));
  assert.throws(() => checkManifest({ ...build.manifest, server: { ...template.server, mcp_config: { ...template.server.mcp_config, env: {} } } }, version));
});

test('non-Windows verification requires explicit allow-skip', { skip: process.platform === 'win32' }, async () => {
  await assert.rejects(verifyMcpb(build.bundle), /Windows only/);
  assert.deepEqual(await verifyMcpb(build.bundle, { allowSkip: true }), { skipped: true });
});

test('real release binaries pass the archive version smoke test', async context => {
  const suffix = process.platform === 'win32' ? '.exe' : '';
  const cli = path.join(root, `target/release/nestbolt${suffix}`), server = path.join(root, `target/release/nestbolt-mcp${suffix}`);
  try { await access(cli); await access(server); } catch (error) { if (error.code !== 'ENOENT') throw error; context.skip('No release binaries'); return; }
  smoke({ cli, server, version: await cargoVersion() });
});

test('real release server passes the standalone bundle smoke test', async context => {
  const realBinary = path.join(root, 'target/release/nestbolt-mcp.exe');
  if (process.platform !== 'win32') { context.skip('Windows only'); return; }
  try { await access(realBinary); } catch (error) { if (error.code !== 'ENOENT') throw error; context.skip('No release binary'); return; }
  let real;
  try { real = await buildMcpb({ binary: realBinary, out: path.join(temp, 'real') }); } catch (error) {
    if (!error.message.includes('binary version must equal manifest version')) throw error;
    context.skip('Release binary version is stale'); return;
  }
  const output = execFileSync(process.execPath, [path.join(root, 'mcpb/verify.mjs'), real.bundle], { encoding: 'utf8', timeout: 90000, windowsHide: true });
  assert.ok(output.includes(`MCPB verified: Nestbolt ${real.manifest.version}, ${real.manifest.tools.length} tools, 4 files; import, nest and validation passed.`));
  const changed = new Map([...readZip(real.bytes)].map(([name, entry]) => [name, entry.read()]));
  changed.set('manifest.json', json({ ...real.manifest, tools: [...real.manifest.tools, { name: 'not_in_binary', description: 'Synthetic mismatch.' }] }));
  const mismatched = path.join(temp, 'mismatched.mcpb');
  await writeFile(mismatched, writeZip(changed));
  await assert.rejects(verifyMcpb(mismatched), /manifest tools must match live tools/);
});
