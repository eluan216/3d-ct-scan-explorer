'use client';

import { useEffect, useState } from 'react';
import {
  loadManifest,
  loadVolumeMetadata,
  meshUrl,
  listStructures,
  AssetError,
} from '@/lib/assets';
import { Manifest, VolumeMetadata } from '@/types/manifest';
import { MeshViewer } from './MeshViewer';
import { StructureList } from './StructureList';
import { SlicePanel } from './SlicePanel';
import { Controls } from './Controls';
import { MetadataPanel } from './MetadataPanel';
import { WebGLFallback } from './WebGLFallback';

export function ViewerShell() {
  const [manifest, setManifest] = useState<Manifest | null>(null);
  const [volumeMeta, setVolumeMeta] = useState<VolumeMetadata | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    let cancelled = false;
    (async () => {
      try {
        const m = await loadManifest();
        if (cancelled) return;
        setManifest(m);

        try {
          const meta = await loadVolumeMetadata(m);
          if (!cancelled) setVolumeMeta(meta);
        } catch {
          // volume metadata is optional for the 3D-only path
        }

        if (!cancelled) setLoading(false);
      } catch (e) {
        if (!cancelled) {
          setError(e instanceof AssetError ? e.message : 'Failed to load assets');
          setLoading(false);
        }
      }
    })();
    return () => {
      cancelled = true;
    };
  }, []);

  if (loading) {
    return (
      <div className="flex h-full items-center justify-center text-accent-muted">
        Loading assets…
      </div>
    );
  }

  if (error || !manifest) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-2 p-6 text-center">
        <p className="text-accent">Could not load study</p>
        <p className="max-w-md text-sm text-accent-muted">
          {error ?? 'Unknown error'}
        </p>
        <p className="mt-4 text-xs text-accent-muted">
          Ensure a valid <code className="text-accent">assets/</code> folder with
          <code className="text-accent"> manifest.json</code> is available, then refresh.
        </p>
      </div>
    );
  }

  const names = listStructures(manifest);
  const meshes = names
    .map((name) => {
      const url = meshUrl(manifest, name);
      return url ? { name, url } : null;
    })
    .filter(Boolean) as { name: string; url: string }[];

  return (
    <div className="flex h-full min-h-0 flex-col md:flex-row">
      {/* sidebar – stacks on mobile */}
      <aside className="flex max-h-[40vh] w-full shrink-0 flex-col overflow-y-auto border-b border-surface-border md:max-h-none md:w-56 md:border-b-0 md:border-r">
        <div className="border-b border-surface-border px-3 py-2">
          <p className="text-xs text-accent-muted">Subject</p>
          <p className="truncate text-sm font-medium">{manifest.subject_id}</p>
          <p className="mt-1 text-xs text-accent-muted">
            pipeline {manifest.pipeline_version}
          </p>
        </div>

        <StructureList names={names} />

        <div className="border-t border-surface-border">
          <Controls structureNames={names} />
        </div>

        <div className="border-t border-surface-border">
          <MetadataPanel manifest={manifest} volumeMeta={volumeMeta} />
        </div>
      </aside>

      {/* main: 3D + slices */}
      <div className="flex min-h-0 min-w-0 flex-1 flex-col lg:flex-row">
        <main className="relative min-h-[36vh] flex-1 lg:min-h-0">
          <WebGLFallback>
            {meshes.length === 0 ? (
              <div className="flex h-full items-center justify-center p-4 text-center text-sm text-accent-muted">
                No meshes listed in the manifest
              </div>
            ) : (
              <MeshViewer meshes={meshes} />
            )}
          </WebGLFallback>
        </main>

        <section className="h-[42vh] shrink-0 border-t border-surface-border lg:h-auto lg:w-72 lg:border-l lg:border-t-0">
          <SlicePanel manifest={manifest} />
        </section>
      </div>
    </div>
  );
}
