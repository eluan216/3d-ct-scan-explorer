'use client';

import { useViewerStore } from '@/store/viewer';

interface Props {
  names: string[];
}

export function StructureList({ names }: Props) {
  const { selected, visible, setSelected, setVisible, resetVisibility } =
    useViewerStore();

  return (
    <div className="flex h-full flex-col gap-2 p-3">
      <div className="flex items-center justify-between">
        <h2 className="text-sm font-medium text-accent-muted">Structures</h2>
        <button
          type="button"
          onClick={() => resetVisibility(names)}
          className="text-xs text-accent hover:underline"
        >
          Reset
        </button>
      </div>

      <ul className="flex-1 space-y-1 overflow-y-auto text-sm">
        {names.map((name) => {
          const isVisible = visible[name] !== false;
          const isSelected = selected === name;
          return (
            <li key={name}>
              <div
                className={`flex items-center gap-2 rounded px-2 py-1.5 ${
                  isSelected ? 'bg-accent/20' : 'hover:bg-surface-panel'
                }`}
              >
                <input
                  type="checkbox"
                  checked={isVisible}
                  onChange={(e) => setVisible(name, e.target.checked)}
                  className="accent-accent"
                />
                <button
                  type="button"
                  className="flex-1 text-left capitalize"
                  onClick={() => setSelected(isSelected ? null : name)}
                >
                  {name.replace(/_/g, ' ')}
                </button>
              </div>
            </li>
          );
        })}
      </ul>
    </div>
  );
}
