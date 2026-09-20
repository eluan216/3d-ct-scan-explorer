import type { Metadata } from 'next';
import './globals.css';

export const metadata: Metadata = {
  title: '3D CT Scan Explorer',
  description: 'Interactive CT anatomy viewer – learning use only',
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body className="min-h-screen antialiased">{children}</body>
    </html>
  );
}
