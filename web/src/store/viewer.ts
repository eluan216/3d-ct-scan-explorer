/**
 * Shared viewer state.
 * Crosshair is stored in voxel indices (i, j, k) of the cropped volume.
 */

import { create } from 'zustand';

export interface Crosshair {
  i: number;
  j: number;
  k: number;
}

interface ViewerState {
  // 3D mesh controls
  selected: string | null;
  visible: Record<string, boolean>;
  opacity: number;
  setSelected: (name: string | null) => void;
  setVisible: (name: string, value: boolean) => void;
  setOpacity: (value: number) => void;
  resetVisibility: (names: string[]) => void;

  // volume + crosshair
  shape: [number, number, number] | null; // [I, J, K]
  spacing: [number, number, number] | null;
  crosshair: Crosshair;
  setVolumeMeta: (shape: [number, number, number], spacing: [number, number, number]) => void;
  setCrosshair: (c: Partial<Crosshair>) => void;
  setCrosshairFromPlane: (plane: 'axial' | 'coronal' | 'sagittal', a: number, b: number) => void;
}

function clamp(v: number, lo: number, hi: number) {
  return Math.max(lo, Math.min(hi, v));
}

export const useViewerStore = create<ViewerState>((set, get) => ({
  selected: null,
  visible: {},
  opacity: 0.85,
  setSelected: (name) => set({ selected: name }),
  setVisible: (name, value) =>
    set((s) => ({ visible: { ...s.visible, [name]: value } })),
  setOpacity: (value) => set({ opacity: value }),
  resetVisibility: (names) =>
    set({
      visible: Object.fromEntries(names.map((n) => [n, true])),
      selected: null,
      opacity: 0.85,
    }),

  shape: null,
  spacing: null,
  crosshair: { i: 0, j: 0, k: 0 },

  setVolumeMeta: (shape, spacing) => {
    const mid: Crosshair = {
      i: Math.floor(shape[0] / 2),
      j: Math.floor(shape[1] / 2),
      k: Math.floor(shape[2] / 2),
    };
    set({ shape, spacing, crosshair: mid });
  },

  setCrosshair: (partial) => {
    const { shape, crosshair } = get();
    if (!shape) return;
    const next = {
      i: partial.i !== undefined ? clamp(Math.round(partial.i), 0, shape[0] - 1) : crosshair.i,
      j: partial.j !== undefined ? clamp(Math.round(partial.j), 0, shape[1] - 1) : crosshair.j,
      k: partial.k !== undefined ? clamp(Math.round(partial.k), 0, shape[2] - 1) : crosshair.k,
    };
    set({ crosshair: next });
  },

  /**
   * Update crosshair from a 2-D click inside a given plane.
   * a, b are pixel indices in the displayed image (already orientation-corrected).
   */
  setCrosshairFromPlane: (plane, a, b) => {
    const { shape, crosshair } = get();
    if (!shape) return;
    const [ni, nj, nk] = shape;

    if (plane === 'axial') {
      // display: column = ni-1-i  (R left), row = nj-1-j  (A top)
      const i = clamp(ni - 1 - Math.round(a), 0, ni - 1);
      const j = clamp(nj - 1 - Math.round(b), 0, nj - 1);
      set({ crosshair: { i, j, k: crosshair.k } });
    } else if (plane === 'coronal') {
      // display: column = ni-1-i, row = nk-1-k  (S top)
      const i = clamp(ni - 1 - Math.round(a), 0, ni - 1);
      const k = clamp(nk - 1 - Math.round(b), 0, nk - 1);
      set({ crosshair: { i, j: crosshair.j, k } });
    } else {
      // sagittal: column = nj-1-j, row = nk-1-k
      const j = clamp(nj - 1 - Math.round(a), 0, nj - 1);
      const k = clamp(nk - 1 - Math.round(b), 0, nk - 1);
      set({ crosshair: { i: crosshair.i, j, k } });
    }
  },
}));
