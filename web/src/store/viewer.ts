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
  selected: string | null;
  visible: Record<string, boolean>;
  opacity: number;
  windowLevel: number;
  windowWidth: number;

  setSelected: (name: string | null) => void;
  setVisible: (name: string, value: boolean) => void;
  setOpacity: (value: number) => void;
  setWindow: (level: number, width: number) => void;
  resetVisibility: (names: string[]) => void;
  resetAll: (names: string[]) => void;

  shape: [number, number, number] | null;
  spacing: [number, number, number] | null;
  crosshair: Crosshair;
  setVolumeMeta: (
    shape: [number, number, number],
    spacing: [number, number, number],
    defaultLevel?: number,
    defaultWidth?: number,
  ) => void;
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
  windowLevel: 50,
  windowWidth: 400,

  setSelected: (name) => set({ selected: name }),
  setVisible: (name, value) =>
    set((s) => ({ visible: { ...s.visible, [name]: value } })),
  setOpacity: (value) => set({ opacity: clamp(value, 0.05, 1) }),
  setWindow: (level, width) =>
    set({ windowLevel: level, windowWidth: Math.max(1, width) }),

  resetVisibility: (names) =>
    set({
      visible: Object.fromEntries(names.map((n) => [n, true])),
      selected: null,
      opacity: 0.85,
    }),

  resetAll: (names) => {
    const { shape } = get();
    const mid = shape
      ? {
          i: Math.floor(shape[0] / 2),
          j: Math.floor(shape[1] / 2),
          k: Math.floor(shape[2] / 2),
        }
      : { i: 0, j: 0, k: 0 };
    set({
      visible: Object.fromEntries(names.map((n) => [n, true])),
      selected: null,
      opacity: 0.85,
      windowLevel: 50,
      windowWidth: 400,
      crosshair: mid,
    });
  },

  shape: null,
  spacing: null,
  crosshair: { i: 0, j: 0, k: 0 },

  setVolumeMeta: (shape, spacing, defaultLevel = 50, defaultWidth = 400) => {
    const mid: Crosshair = {
      i: Math.floor(shape[0] / 2),
      j: Math.floor(shape[1] / 2),
      k: Math.floor(shape[2] / 2),
    };
    set({
      shape,
      spacing,
      crosshair: mid,
      windowLevel: defaultLevel,
      windowWidth: defaultWidth,
    });
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

  setCrosshairFromPlane: (plane, a, b) => {
    const { shape, crosshair } = get();
    if (!shape) return;
    const [ni, nj, nk] = shape;

    if (plane === 'axial') {
      const i = clamp(ni - 1 - Math.round(a), 0, ni - 1);
      const j = clamp(nj - 1 - Math.round(b), 0, nj - 1);
      set({ crosshair: { i, j, k: crosshair.k } });
    } else if (plane === 'coronal') {
      const i = clamp(ni - 1 - Math.round(a), 0, ni - 1);
      const k = clamp(nk - 1 - Math.round(b), 0, nk - 1);
      set({ crosshair: { i, j: crosshair.j, k } });
    } else {
      const j = clamp(nj - 1 - Math.round(a), 0, nj - 1);
      const k = clamp(nk - 1 - Math.round(b), 0, nk - 1);
      set({ crosshair: { i: crosshair.i, j, k } });
    }
  },
}));
