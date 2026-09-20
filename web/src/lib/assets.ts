/**
 * Asset loading helpers.
 * The frontend only ever reads the manifest and the files it references.
 */

import { Manifest, VolumeMetadata, isManifest } from '@/types/manifest';

const ASSET_BASE = '/assets';

export class AssetError extends Error {
  constructor(message: string) {
    super(message);
    this.name = 'AssetError';
  }
}

export async function loadManifest(url = `${ASSET_BASE}/manifest.json`): Promise<Manifest> {
  const res = await fetch(url);
  if (!res.ok) {
    throw new AssetError(`Failed to load manifest (${res.status})`);
  }
  const data = await res.json();
  if (!isManifest(data)) {
    throw new AssetError('Manifest failed schema validation');
  }
  return data;
}

export async function loadVolumeMetadata(
  manifest: Manifest,
): Promise<VolumeMetadata> {
  const res = await fetch(`${ASSET_BASE}/${manifest.volume.metadata}`);
  if (!res.ok) {
    throw new AssetError(`Failed to load volume metadata (${res.status})`);
  }
  return res.json();
}

export function meshUrl(manifest: Manifest, name: string): string | null {
  const rel = manifest.meshes[name];
  if (!rel) return null;
  return `${ASSET_BASE}/${rel}`;
}

export function listStructures(manifest: Manifest): string[] {
  return Object.keys(manifest.meshes).sort();
}
