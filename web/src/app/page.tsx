import { ViewerShell } from '@/components/ViewerShell';

export default function HomePage() {
  return (
    <div className="flex h-screen flex-col">
      <header className="flex items-center justify-between border-b border-surface-border px-4 py-2">
        <div>
          <h1 className="text-base font-semibold tracking-tight">
            3D CT Scan Explorer
          </h1>
          <p className="text-xs text-accent-muted">
            Learning use only · not a medical device
          </p>
        </div>
      </header>

      <div className="min-h-0 flex-1">
        <ViewerShell />
      </div>

      <footer className="border-t border-surface-border px-4 py-1.5 text-center text-xs text-accent-muted">
        For learning only. Not for diagnosis.
      </footer>
    </div>
  );
}
