/** @type {import('next').NextConfig} */
const nextConfig = {
  async rewrites() {
    return [
      {
        source: "/:path*",
        destination: "http://localhost:8000/:path*",
        // destination: "http://backend:8000/:path*",
      },
    ];
  },
};

export default nextConfig;
