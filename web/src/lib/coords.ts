/**
 * Map a pointer position on a CSS-sized canvas (object-contain)
 * back to canvas pixel coordinates.
 */

export function pointerToCanvasPixel(
  clientX: number,
  clientY: number,
  rect: DOMRect,
  canvasWidth: number,
  canvasHeight: number,
): { a: number; b: number } | null {
  const cssW = rect.width;
  const cssH = rect.height;
  if (cssW <= 0 || cssH <= 0) return null;

  // object-contain letterboxing
  const scale = Math.min(cssW / canvasWidth, cssH / canvasHeight);
  const dispW = canvasWidth * scale;
  const dispH = canvasHeight * scale;
  const offsetX = (cssW - dispW) / 2;
  const offsetY = (cssH - dispH) / 2;

  const x = clientX - rect.left - offsetX;
  const y = clientY - rect.top - offsetY;

  if (x < 0 || y < 0 || x > dispW || y > dispH) return null;

  return {
    a: (x / scale),
    b: (y / scale),
  };
}
