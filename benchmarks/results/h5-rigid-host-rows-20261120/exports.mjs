// Revalidate and export the same 66 physical placements with both production workers.
import assert from "node:assert/strict";
import {createHash} from "node:crypto";
import {mkdir, readdir, readFile, writeFile} from "node:fs/promises";
import {createRequire} from "node:module";
import path from "node:path";

const [inputs, native, output] = process.argv.slice(2);
const dist = path.resolve("web/dist");
const {chromium, firefox} = createRequire(path.resolve("web/package.json"))("playwright");
const workers = (await readdir(path.join(dist, "assets"))).filter(name => /^worker-.*\.js$/.test(name));
assert.equal(workers.length, 1);
const library = await readFile(path.join(inputs, "library.json"), "utf8");
const request = await readFile(path.join(inputs, "request.json"), "utf8");
const layout = await readFile(path.join(native, "layout.json"), "utf8");
const report = JSON.parse(await readFile(path.join(native, "report.json"), "utf8"));
const summary = [];

for (const [name, engine, launch] of [["chrome", chromium, {channel: "chrome"}], ["firefox", firefox, {}]]) {
  const browser = await engine.launch(launch);
  try {
    const page = await browser.newPage();
    await page.route("http://nestbolt.test/**", async route => {
      const url = new URL(route.request().url());
      if (url.pathname === "/") {
        return route.fulfill({contentType: "text/html", body: "<!doctype html><title>Nestbolt</title>"});
      }
      if (!/^\/assets\/[\w.-]+$/.test(url.pathname)) return route.abort();
      const body = await readFile(path.join(dist, url.pathname.slice(1)));
      await route.fulfill({contentType: url.pathname.endsWith(".wasm") ? "application/wasm" : "text/javascript", body});
    });
    await page.goto("http://nestbolt.test/");
    const result = await page.evaluate(async ({workerName, library, request, layout}) => {
      const worker = new Worker("/assets/" + workerName, {type: "module"});
      let id = 0;
      const call = (type, args) => new Promise((resolve, reject) => {
        const current = ++id;
        const timer = setTimeout(() => reject(new Error(type + " timed out")), 30000);
        worker.onerror = e => { clearTimeout(timer); reject(new Error(e.message)); };
        worker.onmessage = ({data}) => {
          if (data.id !== current || data.type === "progress") return;
          clearTimeout(timer);
          if (data.type === "error") reject(new Error(data.message));
          else resolve(data.value);
        };
        worker.postMessage({id: current, type, args});
      });
      try {
        const args = {library, request, layout};
        const validation = JSON.parse(await call("validate", args));
        const files = {};
        for (const sheet of JSON.parse(layout).sheets) {
          for (const format of ["svg", "dxf"]) {
            files[sheet.id + "." + format] = await call("export", {...args, sheet: sheet.id, format, outline: false});
          }
        }
        return {validation, files};
      } finally { worker.terminate(); }
    }, {workerName: workers[0], library, request, layout});
    assert.equal(result.validation.valid, true);
    assert.equal(result.validation.metrics.placed_parts, report.validation.metrics.placed_parts);
    assert.equal(result.validation.metrics.normalized_material, report.validation.metrics.normalized_material);
    const hashes = {};
    for (const [file, data] of Object.entries(result.files)) {
      const bytes = Buffer.from(data);
      const ref = await readFile(path.join(native, file));
      assert(bytes.equals(ref), name + " differs in " + file);
      hashes[file] = createHash("sha256").update(bytes).digest("hex");
    }
    summary.push({browser: name, placed: result.validation.metrics.placed_parts, files: hashes});
  } finally { await browser.close(); }
}
await mkdir(output, {recursive: true});
await writeFile(path.join(output, "exports.json"), JSON.stringify(summary, null, 2) + "\n");
console.log(summary.map(check => check.browser + ": " + Object.keys(check.files).length + " matching exports").join(", "));
