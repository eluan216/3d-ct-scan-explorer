'use client';

import { useEffect, useState } from 'react';

function supportsWebGL(): boolean {
  try {
    const canvas = document.createElement('canvas');
    return !!(
      window.WebGLRenderingContext &&
      (canvas.getContext('webgl') || canvas.getContext('experimental-webgl'))
    );
  } catch {
    return false;
  }
}

export function WebGLFallback({ children }: { children: React.ReactNode }) {
  const [ok, setOk] = useState<boolean | null>(null);

  useEffect(() => {
    setOk(supportsWebGL());
  }, []);

  if (ok === null) {
    return (
      <div className="flex h-full items-center justify-center text-accent-muted">
        Checking graphics support…
      </div>
    );
  }

  if (!ok) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
        <p className="text-accent">WebGL is not available</p>
        <p className="max-w-sm text-sm text-accent-muted">
          This viewer needs WebGL to render 3D meshes. Slice views may still work
          if the volume loads successfully. Try a different browser or enable
          hardware acceleration.
        </p>
      </div>
    );
  }

  return <>{children}</>;
}
