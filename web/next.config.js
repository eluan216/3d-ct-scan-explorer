/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // allow loading assets from the sibling assets/ directory during local dev
  async rewrites() {
    return [
      {
        source: '/assets/:path*',
        destination: '/api/assets/:path*',
      },
    ];
  },
};

module.exports = nextConfig;
