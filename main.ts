// World Ledger: one-image front page of the world's news for Sunday 22 November 2026.
//
// The picture is drawn ahead of time by tools/render.py (Python + Pillow, run by hand) and committed as entry.png.
// At grading time this program only checks that committed file and writes the very same bytes to the output folder:
// no network, no clock, no randomness, so two runs always produce identical bytes.
//
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES: number = 1024 * 1024; // the gate's limit: 1 MiB
const SIDE: number = 1024; // the gate's limit and our exact canvas: 1024 x 1024
const PNG_SIGNATURE: number[] = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];

function fail(reason: string): never {
  throw new Error(`entry.png rejected: ${reason}`);
}

// Check that the bytes are a 1024 x 1024, 8-bit, truecolour (RGB) PNG under 1 MiB.
function checkPng(bytes: Buffer): void {
  if (bytes.length >= MAX_BYTES) fail(`${bytes.length} bytes is not under 1 MiB`);
  if (bytes.length < 57) fail('too short to be a PNG');
  for (let i = 0; i < PNG_SIGNATURE.length; i++) {
    if (bytes[i] !== PNG_SIGNATURE[i]) fail('missing PNG signature');
  }
  if (bytes.readUInt32BE(8) !== 13 || bytes.toString('latin1', 12, 16) !== 'IHDR') fail('first chunk is not IHDR');
  const width = bytes.readUInt32BE(16);
  const height = bytes.readUInt32BE(20);
  const bitDepth = bytes[24];
  const colourType = bytes[25];
  if (width !== SIDE || height !== SIDE) fail(`${width} x ${height} is not ${SIDE} x ${SIDE}`);
  if (bitDepth !== 8 || colourType !== 2) fail(`bit depth ${bitDepth}, colour type ${colourType} is not 8-bit RGB`);
}

const image: Buffer = readFileSync(new URL('./entry.png', import.meta.url));
checkPng(image);

const outputDir: string = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outputDir, { recursive: true });
writeFileSync(join(outputDir, 'entry.png'), image);
