/**
 * Typed representation of the pipeline asset manifest.
 * Must stay aligned with pipeline/docs/CONTRACT.md.
 */

export interface VolumeRef {
  bin: string;
  metadata: string;
}

export interface LabelInfo {
  id: number;
}

export interface Manifest {
  pipeline_version: string;
  subject_id: string;
  volume: VolumeRef;
  meshes: Record<string, string>;
  labels: Record<string, LabelInfo>;
  slices?: Record<string, string>;
}

export interface VolumeMetadata {
  shape: [number, number, number];
  spacing_mm: [number, number, number];
  origin_mm: [number, number, number];
  orientation: string;
  intensity_range: [number, number];
  dtype?: string;
  window_level?: number;
  window_width?: number;
}

export function isManifest(value: unknown): value is Manifest {
  if (!value || typeof value !== 'object') return false;
  const m = value as Record<string, unknown>;
  return (
    typeof m.pipeline_version === 'string' &&
    typeof m.subject_id === 'string' &&
    typeof m.volume === 'object' &&
    m.volume !== null &&
    typeof m.meshes === 'object' &&
    m.meshes !== null
  );
}
