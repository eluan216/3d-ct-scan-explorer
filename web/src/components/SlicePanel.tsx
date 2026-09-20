'use client';

import { useEffect, useState } from 'react';
import { Manifest, VolumeMetadata } from '@/types/manifest';
import { loadVolumeMetadata } from '@/lib/assets';
import { loadVolume, VolumeData } from '@/lib/volume';
import { useViewerStore } from '@/store/viewer';
import { SliceView } from './SliceView';

interface Props {
  manifest: Manifest;
}

export function SlicePanel({ manifest }: Props) {
  const [volume, setVolume] = useState<VolumeData | null>(null);
  const [error, setError] = useState<string | null>(null);
  const setVolumeMeta = useViewerStore((s) => s.setVolumeMeta);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const meta: VolumeMetadata = await loadVolumeMetadata(manifest);
        const binUrl = `/assets/${manifest.volume.bin}`;
        const vol = await loadVolume(binUrl, meta);
        if (cancelled) return;
        setVolume(vol);
        setVolumeMeta(
          vol.shape,
          vol.spacing,
          meta.window_level ?? 50,
          meta.window_width ?? 400,
        );
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : 'Failed to load volume');
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, [manifest, setVolumeMeta]);

  if (error) {
    return (
      <div className="flex h-full items-center justify-center p-4 text-center text-sm text-accent-muted">
        {error}
      </div>
    );
  }

  if (!volume) {
    return (
      <div className="flex h-full items-center justify-center text-sm text-accent-muted">
        Loading volume…
      </div>
    );
  }

  return (
    <div className="grid h-full min-h-0 grid-rows-3 gap-1 p-1">
      <SliceView plane="axial" volume={volume} label="Axial" />
      <SliceView plane="coronal" volume={volume} label="Coronal" />
      <SliceView plane="sagittal" volume={volume} label="Sagittal" />
    </div>
  );
}
