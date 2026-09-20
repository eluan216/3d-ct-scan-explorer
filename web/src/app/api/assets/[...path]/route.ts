/**
 * Dev helper: serve files from the sibling ../assets directory.
 * In production you would place assets under public/ or a CDN.
 */

import { NextRequest, NextResponse } from 'next/server';
import { readFile } from 'fs/promises';
import path from 'path';

export async function GET(
  _req: NextRequest,
  { params }: { params: { path: string[] } },
) {
  const rel = params.path.join('/');
  // resolve against the monorepo assets folder
  const filePath = path.join(process.cwd(), '..', 'assets', rel);

  try {
    const data = await readFile(filePath);
    const ext = path.extname(filePath).toLowerCase();
    const type =
      ext === '.json'
        ? 'application/json'
        : ext === '.glb'
          ? 'model/gltf-binary'
          : 'application/octet-stream';

    return new NextResponse(data, {
      headers: {
        'Content-Type': type,
        'Cache-Control': 'public, max-age=3600',
      },
    });
  } catch {
    return NextResponse.json({ error: 'Not found' }, { status: 404 });
  }
}
