// contexts/AuthContext.tsx
'use client';

import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import { useRouter } from 'next/navigation';

type User = {
  id: number;
  email: string;
  name?: string;
};

type AuthContextType = {
  user: User | null;
  signIn: (email: string, password: string) => Promise<boolean>;
  signUp: (email: string, password: string) => Promise<boolean>;
  signOut: () => void;
  isLoading: boolean;
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

// API base URL from environment
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [token, setToken] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();

  // Check if user is logged in on initial load
  useEffect(() => {
    const storedUser = localStorage.getItem('user');
    const storedToken = localStorage.getItem('auth_token');

    if (storedUser && storedToken) {
      setUser(JSON.parse(storedUser));
      setToken(storedToken);
    }
    setIsLoading(false);
  }, []);

  const signIn = async (email: string, password: string): Promise<boolean> => {
    try {
      // Call the correct backend API endpoint
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/signin`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();

        // Store user and token in localStorage
        localStorage.setItem('user', JSON.stringify(data));
        localStorage.setItem('auth_token', data.access_token);

        setUser({
          id: data.user_id,
          email: data.email
        });
        setToken(data.access_token);

        return true;
      } else {
        console.error('Sign in failed:', await response.text());
        return false;
      }
    } catch (error) {
      console.error('Sign in error:', error);
      return false;
    }
  };

  const signUp = async (email: string, password: string): Promise<boolean> => {
    try {
      // Call the correct backend API endpoint
      const response = await fetch(`${API_BASE_URL}/api/v1/auth/signup`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email, password }),
      });

      if (response.ok) {
        const data = await response.json();

        // Store user and token in localStorage
        localStorage.setItem('user', JSON.stringify(data.user));
        localStorage.setItem('auth_token', data.access_token);

        setUser({
          id: data.user.id,
          email: data.user.email
        });
        setToken(data.access_token);

        return true;
      } else {
        console.error('Sign up failed:', await response.text());
        return false;
      }
    } catch (error) {
      console.error('Sign up error:', error);
      return false;
    }
  };

  const signOut = () => {
    // Remove user and token from localStorage
    localStorage.removeItem('user');
    localStorage.removeItem('auth_token');
    setUser(null);
    setToken(null);
    router.push('/signin');
    router.refresh();
  };

  return (
    <AuthContext.Provider value={{ user, signIn, signUp, signOut, isLoading }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}