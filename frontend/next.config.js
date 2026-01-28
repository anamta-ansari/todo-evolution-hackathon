const path = require('path');

/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,

  // // Explicitly disable turbopack
  // experimental: {
  //   turbo: {
  //     // Disable turbopack experimental features that might cause issues
  //   }
  // },

  // Configure webpack to exclude backend code
  webpack: (config, { isServer }) => {
    // Add alias to ensure proper module resolution
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, './'),
    };

    // Exclude backend-related files from processing
    if (!isServer) {
      config.resolve.fallback = {
        ...config.resolve.fallback,
        // Prevent processing of backend-specific modules
        fs: false,
        net: false,
        tls: false,
      };
    }

    // Don't bundle backend code
    config.externals = config.externals || [];
    if (isServer) {
      // On the server side, mark backend modules as external
      config.externals.push(
        'backend',
        '../backend',
        '../../backend',
        'better-auth/node',
        '@better-auth/node'
      );
    }

    return config;
  },

  // Don't transpile backend packages
  transpilePackages: [],
};

module.exports = nextConfig;