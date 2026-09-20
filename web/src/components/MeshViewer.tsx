'use client';

import { Suspense, useEffect, Component, ReactNode } from 'react';
import { Canvas } from '@react-three/fiber';
import { OrbitControls, useGLTF, Center } from '@react-three/drei';
import { useViewerStore } from '@/store/viewer';
import { OrientationIndicator } from './OrientationIndicator';

interface MeshProps {
  url: string;
  name: string;
}

function OrganMesh({ url, name }: MeshProps) {
  const { scene } = useGLTF(url);
  const { selected, visible, opacity } = useViewerStore();
  const isVisible = visible[name] !== false;
  const isSelected = selected === name;

  const clone = scene.clone(true);

  clone.traverse((child) => {
    if ((child as any).isMesh) {
      const mesh = child as any;
      mesh.material = mesh.material.clone();
      mesh.material.transparent = true;
      mesh.material.opacity = isSelected ? 1 : opacity * (isVisible ? 1 : 0);
      mesh.material.depthWrite = isSelected || opacity > 0.9;
      mesh.visible = isVisible;
    }
  });

  return <primitive object={clone} />;
}

class MeshErrorBoundary extends Component<
  { children: ReactNode; fallback?: ReactNode },
  { hasError: boolean }
> {
  constructor(props: { children: ReactNode; fallback?: ReactNode }) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  render() {
    if (this.state.hasError) {
      return (
        this.props.fallback ?? (
          <div className="flex h-full items-center justify-center text-sm text-accent-muted">
            Failed to render 3D meshes
          </div>
        )
      );
    }
    return this.props.children;
  }
}

interface Props {
  meshes: { name: string; url: string }[];
}

export function MeshViewer({ meshes }: Props) {
  const resetVisibility = useViewerStore((s) => s.resetVisibility);

  useEffect(() => {
    resetVisibility(meshes.map((m) => m.name));
  }, [meshes, resetVisibility]);

  return (
    <div className="relative h-full w-full">
      <MeshErrorBoundary>
        <Canvas
          camera={{ position: [0, 0, 250], fov: 45, near: 0.1, far: 2000 }}
          gl={{ antialias: true, powerPreference: 'default' }}
          dpr={[1, 1.5]}
        >
          <color attach="background" args={['#1a0d14']} />
          <ambientLight intensity={0.6} />
          <directionalLight position={[100, 150, 80]} intensity={0.9} />
          <directionalLight position={[-80, -50, -100]} intensity={0.3} />

          <Suspense fallback={null}>
            <Center>
              {meshes.map(({ name, url }) => (
                <OrganMesh key={name} name={name} url={url} />
              ))}
            </Center>
          </Suspense>

          <OrbitControls
            makeDefault
            enableDamping
            dampingFactor={0.08}
            minDistance={20}
            maxDistance={600}
          />
        </Canvas>
      </MeshErrorBoundary>

      <OrientationIndicator />
    </div>
  );
}
