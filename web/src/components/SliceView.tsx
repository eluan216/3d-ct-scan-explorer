'use client';

import { useRef, useEffect, useCallback } from 'react';
import { useViewerStore } from '@/store/viewer';
import { VolumeData } from '@/lib/volume';
import { pointerToCanvasPixel } from '@/lib/coords';

interface Props {
  plane: 'axial' | 'coronal' | 'sagittal';
  volume: VolumeData;
  label: string;
}

const CROSSHAIR_COLOR = 'rgba(232, 68, 122, 0.9)';

export function SliceView({ plane, volume, label }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const crosshair = useViewerStore((s) => s.crosshair);
  const setCrosshairFromPlane = useViewerStore((s) => s.setCrosshairFromPlane);

  const sliceIndex =
    plane === 'axial' ? crosshair.k : plane === 'coronal' ? crosshair.j : crosshair.i;

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    if (!ctx) return;

    const { pixels, width, height } = volume.extractDisplaySlice(plane, sliceIndex);

    if (canvas.width !== width || canvas.height !== height) {
      canvas.width = width;
      canvas.height = height;
    }

    const img = ctx.createImageData(width, height);
    for (let p = 0; p < pixels.length; p++) {
      const v = pixels[p];
      const off = p * 4;
      img.data[off] = v;
      img.data[off + 1] = v;
      img.data[off + 2] = v;
      img.data[off + 3] = 255;
    }
    ctx.putImageData(img, 0, 0);

    const [ni, nj, nk] = volume.shape;
    let cx: number;
    let cy: number;
    if (plane === 'axial') {
      cx = ni - 1 - crosshair.i;
      cy = nj - 1 - crosshair.j;
    } else if (plane === 'coronal') {
      cx = ni - 1 - crosshair.i;
      cy = nk - 1 - crosshair.k;
    } else {
      cx = nj - 1 - crosshair.j;
      cy = nk - 1 - crosshair.k;
    }

    ctx.strokeStyle = CROSSHAIR_COLOR;
    ctx.lineWidth = 1;
    ctx.beginPath();
    ctx.moveTo(cx + 0.5, 0);
    ctx.lineTo(cx + 0.5, height);
    ctx.moveTo(0, cy + 0.5);
    ctx.lineTo(width, cy + 0.5);
    ctx.stroke();

    ctx.beginPath();
    ctx.arc(cx + 0.5, cy + 0.5, 3, 0, Math.PI * 2);
    ctx.stroke();
  }, [plane, volume, sliceIndex, crosshair]);

  const onPointer = useCallback(
    (e: React.PointerEvent<HTMLCanvasElement>) => {
      const canvas = canvasRef.current;
      if (!canvas) return;
      const rect = canvas.getBoundingClientRect();
      const mapped = pointerToCanvasPixel(
        e.clientX,
        e.clientY,
        rect,
        canvas.width,
        canvas.height,
      );
      if (!mapped) return;
      setCrosshairFromPlane(plane, mapped.a, mapped.b);
    },
    [plane, setCrosshairFromPlane],
  );

  return (
    <div className="flex h-full min-h-0 flex-col border border-surface-border bg-surface-panel">
      <div className="flex items-center justify-between border-b border-surface-border px-2 py-1 text-xs text-accent-muted">
        <span>{label}</span>
        <span className="font-mono">{sliceIndex}</span>
      </div>
      <div className="relative min-h-0 flex-1">
        <canvas
          ref={canvasRef}
          className="absolute inset-0 h-full w-full cursor-crosshair object-contain"
          onPointerDown={onPointer}
          onPointerMove={(e) => {
            if (e.buttons === 1) onPointer(e);
          }}
        />
      </div>
    </div>
  );
}
