import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  reactStrictMode: true,
  // Add empty turbopack config to acknowledge Turbopack usage
  turbopack: {},
};

export default nextConfig;
