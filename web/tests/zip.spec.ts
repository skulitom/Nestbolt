import { expect, test } from '@playwright/test';
import { unzip, zip, ZipBuilder } from '../src/zip.js';

test('incremental Blob ZIP preserves stored-format bytes, Unicode and byte views', async () => {
  const backing = new Uint8Array([91, 0, 1, 255, 92]);
  const files = [{ name: 'sheets/café.svg', data: '<svg>Ω</svg>' },
    { name: 'bytes.bin', data: backing.subarray(1, 4) }, { name: 'empty.txt', data: '' }];
  const archive = new ZipBuilder();
  for (const file of files) archive.add(file.name, file.data);
  const blob = archive.finish();
  expect(blob.type).toBe('application/zip');
  const bytes = new Uint8Array(await blob.arrayBuffer());
  expect(bytes).toEqual(zip(files));
  // Blob ownership is immutable, including when a caller reuses a byte buffer.
  backing[2] = 77;
  const entries = unzip(bytes);
  expect(new TextDecoder().decode(entries.get('sheets/café.svg'))).toBe('<svg>Ω</svg>');
  expect(entries.get('bytes.bin')).toEqual(new Uint8Array([0, 1, 255]));
  expect(entries.get('empty.txt')?.length).toBe(0);
  expect(new Uint8Array(await blob.arrayBuffer())).toEqual(bytes);
});

test('empty Blob ZIP remains readable by the project ZIP reader', async () => {
  const bytes = new Uint8Array(await new ZipBuilder().finish().arrayBuffer());
  expect(bytes).toEqual(zip([]));
  expect(unzip(bytes).size).toBe(0);
});
