// Mock authentication system to bypass Better Auth database issues
export const auth = {
  // Mock configuration to satisfy the import in route.ts
  plugins: [],
  emailAndPassword: {
    enabled: true,
  },
  session: {
    expiresIn: 7 * 24 * 60 * 60, // 7 days
  },
};

// Export a mock API for authentication
export const mockAuthAPI = {
  signIn: async (email: string, password: string) => {
    // Mock sign in functionality
    return {
      user: { id: 'mock-user-id', email },
      session: { token: 'mock-session-token' }
    };
  },
  signUp: async (email: string, password: string) => {
    // Mock sign up functionality
    return {
      user: { id: 'mock-user-id', email },
      session: { token: 'mock-session-token' }
    };
  },
  signOut: async () => {
    // Mock sign out functionality
    return {};
  }
};