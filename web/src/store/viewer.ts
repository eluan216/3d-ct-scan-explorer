/**
 * Shared viewer state (crosshair, visibility, selection).
 */

import { create } from 'zustand';

interface ViewerState {
  selected: string | null;
  visible: Record<string, boolean>;
  opacity: number;
  setSelected: (name: string | null) => void;
  setVisible: (name: string, value: boolean) => void;
  setOpacity: (value: number) => void;
  resetVisibility: (names: string[]) => void;
}

export const useViewerStore = create<ViewerState>((set) => ({
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
}));
