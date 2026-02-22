'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthContext';
import ThemeToggle from './ThemeToggle';

const Navigation = () => {
  const pathname = usePathname();
  const { state, logout } = useAuth();

  const isActive = (path: string) => pathname === path;

  return (
    <nav className="bg-[rgb(var(--bg-primary))] shadow-sm">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link href="/" className="flex-shrink-0 flex items-center">
              <div className="h-8 w-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center">
                <span className="text-white text-sm font-bold">T</span>
              </div>
              <span className="ml-2 text-xl font-bold text-[rgb(var(--text-primary))]">TaskMaster Pro</span>
            </Link>
            <div className="hidden sm:ml-6 sm:flex sm:space-x-8">
              <Link
                href="/"
                className={`${
                  isActive('/')
                    ? 'border-indigo-500 text-[rgb(var(--text-primary))]'
                    : 'border-transparent text-[rgb(var(--text-secondary))] hover:border-[rgb(var(--border-secondary))] hover:text-[rgb(var(--text-primary))]'
                } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
              >
                Home
              </Link>
              {state.isAuthenticated && (
                <Link
                  href="/dashboard"
                  className={`${
                    isActive('/dashboard')
                      ? 'border-indigo-500 text-[rgb(var(--text-primary))]'
                      : 'border-transparent text-[rgb(var(--text-secondary))] hover:border-[rgb(var(--border-secondary))] hover:text-[rgb(var(--text-primary))]'
                  } inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium`}
                >
                  Dashboard
                </Link>
              )}
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <ThemeToggle />
            {!state.isAuthenticated ? (
              <div className="flex items-center space-x-4">
                <Link
                  href="/login"
                  className="text-sm font-medium text-[rgb(var(--text-secondary))] hover:text-[rgb(var(--text-primary))]"
                >
                  Sign in
                </Link>
                <Link
                  href="/signup"
                  className="ml-4 inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                >
                  Sign up
                </Link>
              </div>
            ) : (
              <div className="flex items-center space-x-4">
                <span className="text-sm text-[rgb(var(--text-secondary))] hidden md:inline">
                  {state.user?.email}
                </span>
                <button
                  onClick={() => {
                    logout();
                  }}
                  className="text-sm font-medium text-[rgb(var(--text-secondary))] hover:text-[rgb(var(--text-primary))]"
                >
                  Sign out
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navigation;