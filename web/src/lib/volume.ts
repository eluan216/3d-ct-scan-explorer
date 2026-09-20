/**
 * Load and sample the raw volume.bin produced by the pipeline.
 */

import { VolumeMetadata } from '@/types/manifest';

export class VolumeData {
  readonly data: Uint8Array;
  readonly shape: [number, number, number]; // I, J, K
  readonly spacing: [number, number, number];

  constructor(data: Uint8Array, meta: VolumeMetadata) {
    this.data = data;
    this.shape = meta.shape as [number, number, number];
    this.spacing = meta.spacing_mm as [number, number, number];

    const expected = this.shape[0] * this.shape[1] * this.shape[2];
    if (data.byteLength < expected) {
      throw new Error(
        `volume.bin too small: got ${data.byteLength} bytes, expected >= ${expected}`,
      );
    }
  }

  /** C-order index: i * nj * nk + j * nk + k */
  private idx(i: number, j: number, k: number): number {
    const [, nj, nk] = this.shape;
    return i * nj * nk + j * nk + k;
  }

  value(i: number, j: number, k: number): number {
    return this.data[this.idx(i, j, k)];
  }

  /**
   * Extract a 2-D slice already oriented for display.
   * Returns a flat Uint8Array of size width*height (row-major).
   */
  extractDisplaySlice(
    plane: 'axial' | 'coronal' | 'sagittal',
    index: number,
  ): { pixels: Uint8Array; width: number; height: number } {
    const [ni, nj, nk] = this.shape;

    if (plane === 'axial') {
      // fixed k; column = ni-1-i, row = nj-1-j
      const width = ni;
      const height = nj;
      const pixels = new Uint8Array(width * height);
      const k = Math.max(0, Math.min(nk - 1, index));
      for (let row = 0; row < height; row++) {
        const j = nj - 1 - row;
        for (let col = 0; col < width; col++) {
          const i = ni - 1 - col;
          pixels[row * width + col] = this.value(i, j, k);
        }
      }
      return { pixels, width, height };
    }

    if (plane === 'coronal') {
      // fixed j; column = ni-1-i, row = nk-1-k
      const width = ni;
      const height = nk;
      const pixels = new Uint8Array(width * height);
      const j = Math.max(0, Math.min(nj - 1, index));
      for (let row = 0; row < height; row++) {
        const k = nk - 1 - row;
        for (let col = 0; col < width; col++) {
          const i = ni - 1 - col;
          pixels[row * width + col] = this.value(i, j, k);
        }
      }
      return { pixels, width, height };
    }

    // sagittal: fixed i; column = nj-1-j, row = nk-1-k
    const width = nj;
    const height = nk;
    const pixels = new Uint8Array(width * height);
    const i = Math.max(0, Math.min(ni - 1, index));
    for (let row = 0; row < height; row++) {
      const k = nk - 1 - row;
      for (let col = 0; col < width; col++) {
        const j = nj - 1 - col;
        pixels[row * width + col] = this.value(i, j, k);
      }
    }
    return { pixels, width, height };
  }
}

export async function loadVolume(
  binUrl: string,
  meta: VolumeMetadata,
): Promise<VolumeData> {
  const res = await fetch(binUrl);
  if (!res.ok) throw new Error(`Failed to load volume.bin (${res.status})`);
  const buf = await res.arrayBuffer();
  return new VolumeData(new Uint8Array(buf), meta);
}
