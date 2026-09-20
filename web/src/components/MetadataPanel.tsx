'use client';

import { Manifest, VolumeMetadata } from '@/types/manifest';

interface Props {
  manifest: Manifest;
  volumeMeta: VolumeMetadata | null;
}

function Row({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex justify-between gap-2 text-xs">
      <span className="text-accent-muted">{label}</span>
      <span className="truncate font-mono text-right">{value}</span>
    </div>
  );
}

export function MetadataPanel({ manifest, volumeMeta }: Props) {
  const structures = Object.keys(manifest.meshes ?? {}).sort();
  const labels = Object.keys(manifest.labels ?? {}).sort();

  return (
    <div className="space-y-3 p-3 text-sm">
      <h2 className="text-xs font-medium text-accent-muted">Study metadata</h2>

      <div className="space-y-1.5">
        <Row label="Subject" value={manifest.subject_id || '—'} />
        <Row label="Pipeline" value={manifest.pipeline_version || '—'} />
        <Row label="Modality" value={volumeMeta ? 'CT' : '—'} />
        <Row
          label="Orientation"
          value={volumeMeta?.orientation ?? '—'}
        />
      </div>

      <div className="space-y-1.5 border-t border-surface-border pt-2">
        <Row
          label="Dimensions"
          value={
            volumeMeta
              ? `${volumeMeta.shape[0]} × ${volumeMeta.shape[1]} × ${volumeMeta.shape[2]} vx`
              : '—'
          }
        />
        <Row
          label="Spacing"
          value={
            volumeMeta
              ? `${volumeMeta.spacing_mm.map((s) => s.toFixed(2)).join(' × ')} mm`
              : '—'
          }
        />
        <Row
          label="Intensity"
          value={
            volumeMeta?.intensity_range
              ? `${volumeMeta.intensity_range[0]} – ${volumeMeta.intensity_range[1]}`
              : '—'
          }
        />
        <Row
          label="Window"
          value={
            volumeMeta?.window_level != null && volumeMeta?.window_width != null
              ? `L ${volumeMeta.window_level} / W ${volumeMeta.window_width}`
              : '—'
          }
        />
      </div>

      <div className="border-t border-surface-border pt-2">
        <p className="mb-1 text-xs text-accent-muted">
          Structures ({structures.length})
        </p>
        {structures.length === 0 ? (
          <p className="text-xs text-accent-muted/70">None listed</p>
        ) : (
          <ul className="max-h-24 space-y-0.5 overflow-y-auto text-xs">
            {structures.map((name) => (
              <li key={name} className="truncate capitalize">
                {name.replace(/_/g, ' ')}
                {manifest.labels?.[name]?.id != null && (
                  <span className="ml-1 text-accent-muted">
                    (id {manifest.labels[name].id})
                  </span>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>

      {labels.length > 0 && labels.some((l) => !structures.includes(l)) && (
        <div className="border-t border-surface-border pt-2">
          <p className="mb-1 text-xs text-accent-muted">Label map</p>
          <ul className="text-xs text-accent-muted/80">
            {labels.map((name) => (
              <li key={name}>
                {name}: {manifest.labels[name]?.id ?? '—'}
              </li>
            ))}
          </ul>
        </div>
      )}

      <p className="border-t border-surface-border pt-2 text-[10px] text-accent-muted/60">
        No patient-identifying information is shown. Data is for learning use only.
      </p>
    </div>
  );
}
