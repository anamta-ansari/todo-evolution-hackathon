'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '@/contexts/AuthContext';

export default function SettingsPage() {
  const router = useRouter();
  const { signOut } = useAuth();
  const [isLoggingOut, setIsLoggingOut] = useState(false);

  const handleBackToDashboard = () => {
    router.push('/dashboard');
  };

  const handleLogout = async () => {
    setIsLoggingOut(true);
    try {
      await signOut();
      router.push('/signin');
    } catch (error) {
      console.error('Error signing out:', error);
      setIsLoggingOut(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-pink-50 to-purple-100 p-4">
      <div className="max-w-4xl mx-auto">
        <header className="py-6 flex justify-between items-center">
          <h1 className="text-3xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-pink-500 to-purple-600">
            Account Settings
          </h1>
        </header>

        <main className="mt-8">
          <div className="bg-white p-8 rounded-xl shadow-lg max-w-md mx-auto">
            <div className="space-y-6">
              <div>
                <h2 className="text-xl font-semibold text-gray-800 mb-4">Manage Your Account</h2>
                <p className="text-gray-600">Access your account settings and preferences here.</p>
              </div>

              <div className="pt-4 border-t border-gray-200">
                <div className="space-y-4">
                  <button
                    onClick={handleBackToDashboard}
                    className="w-full px-4 py-3 bg-pink-500 text-white rounded-lg hover:bg-pink-600 transition-colors"
                  >
                    Back to Dashboard
                  </button>

                  <button
                    onClick={handleLogout}
                    disabled={isLoggingOut}
                    className={`w-full px-4 py-3 rounded-lg ${
                      isLoggingOut
                        ? 'bg-gray-300 text-gray-500'
                        : 'bg-red-500 text-white hover:bg-red-600'
                    } transition-colors`}
                  >
                    {isLoggingOut ? 'Signing out...' : 'Logout'}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}