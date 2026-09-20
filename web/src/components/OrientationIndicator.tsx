'use client';

/**
 * Simple anatomical orientation indicator (L/R, A/P, S/I).
 */

export function OrientationIndicator() {
  return (
    <div className="pointer-events-none absolute bottom-3 right-3 select-none text-xs text-accent-muted">
      <div className="rounded border border-surface-border bg-surface-panel/80 px-2 py-1 font-mono">
        <div>R ← → L</div>
        <div>A ↑ ↓ P</div>
        <div>S · · I</div>
      </div>
    </div>
  );
}
