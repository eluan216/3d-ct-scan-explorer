'use client';

import { useViewerStore } from '@/store/viewer';

interface Props {
  structureNames: string[];
}

export function Controls({ structureNames }: Props) {
  const shape = useViewerStore((s) => s.shape);
  const crosshair = useViewerStore((s) => s.crosshair);
  const opacity = useViewerStore((s) => s.opacity);
  const windowLevel = useViewerStore((s) => s.windowLevel);
  const windowWidth = useViewerStore((s) => s.windowWidth);
  const setCrosshair = useViewerStore((s) => s.setCrosshair);
  const setOpacity = useViewerStore((s) => s.setOpacity);
  const setWindow = useViewerStore((s) => s.setWindow);
  const resetAll = useViewerStore((s) => s.resetAll);

  if (!shape) {
    return (
      <div className="p-3 text-xs text-accent-muted">Volume not loaded</div>
    );
  }

  const [ni, nj, nk] = shape;

  return (
    <div className="space-y-3 p-3 text-sm">
      <div className="flex items-center justify-between">
        <h2 className="text-xs font-medium text-accent-muted">Controls</h2>
        <button
          type="button"
          onClick={() => resetAll(structureNames)}
          className="text-xs text-accent hover:underline"
        >
          Reset all
        </button>
      </div>

      {/* Slice positions */}
      <div className="space-y-2">
        <label className="block text-xs text-accent-muted">
          Axial (k) — {crosshair.k}
          <input
            type="range"
            min={0}
            max={Math.max(0, nk - 1)}
            value={crosshair.k}
            onChange={(e) => setCrosshair({ k: Number(e.target.value) })}
            className="mt-1 w-full accent-accent"
          />
        </label>
        <label className="block text-xs text-accent-muted">
          Coronal (j) — {crosshair.j}
          <input
            type="range"
            min={0}
            max={Math.max(0, nj - 1)}
            value={crosshair.j}
            onChange={(e) => setCrosshair({ j: Number(e.target.value) })}
            className="mt-1 w-full accent-accent"
          />
        </label>
        <label className="block text-xs text-accent-muted">
          Sagittal (i) — {crosshair.i}
          <input
            type="range"
            min={0}
            max={Math.max(0, ni - 1)}
            value={crosshair.i}
            onChange={(e) => setCrosshair({ i: Number(e.target.value) })}
            className="mt-1 w-full accent-accent"
          />
        </label>
      </div>

      {/* Window / level – values stored for later use when raw HU is available;
          current volume.bin is already windowed by the pipeline. */}
      <div className="space-y-2 border-t border-surface-border pt-2">
        <label className="block text-xs text-accent-muted">
          Window level — {windowLevel}
          <input
            type="range"
            min={-200}
            max={400}
            value={windowLevel}
            onChange={(e) => setWindow(Number(e.target.value), windowWidth)}
            className="mt-1 w-full accent-accent"
          />
        </label>
        <label className="block text-xs text-accent-muted">
          Window width — {windowWidth}
          <input
            type="range"
            min={1}
            max={2000}
            value={windowWidth}
            onChange={(e) => setWindow(windowLevel, Number(e.target.value))}
            className="mt-1 w-full accent-accent"
          />
        </label>
        <p className="text-[10px] text-accent-muted/70">
          Display volume is pre-windowed by the pipeline. These values are kept for
          metadata consistency and future raw-HU support.
        </p>
      </div>

      {/* Mesh opacity */}
      <div className="border-t border-surface-border pt-2">
        <label className="block text-xs text-accent-muted">
          Mesh opacity — {opacity.toFixed(2)}
          <input
            type="range"
            min={0.05}
            max={1}
            step={0.05}
            value={opacity}
            onChange={(e) => setOpacity(Number(e.target.value))}
            className="mt-1 w-full accent-accent"
          />
        </label>
      </div>
    </div>
  );
}
