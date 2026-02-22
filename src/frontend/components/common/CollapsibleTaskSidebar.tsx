'use client';

import { useState, useEffect } from 'react';
import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { TaskStatusFilter } from '@/lib/types';
import { Suspense } from 'react';

function CollapsibleTaskSidebarContent({ isCollapsed }: { isCollapsed: boolean }) {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const statusFilter = (searchParams.get('status') as TaskStatusFilter) || 'all';
  const priorityFilter = searchParams.get('priority') || 'all';

  const updateFilter = (filterName: string, value: string) => {
    const params = new URLSearchParams(searchParams.toString());

    if (value === 'all') {
      params.delete(filterName);
    } else {
      params.set(filterName, value);
    }

    router.push(`${pathname}?${params.toString()}`);
  };

  const clearFilters = () => {
    router.push(pathname);
  };

  return (
    <>
      {/* Collapsed version - only icons */}
      {isCollapsed ? (
        <div className="w-20 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen flex flex-col">
          <div className="p-4 flex justify-center">
            <div className="h-8 w-8 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center">
              <span className="text-white text-xs font-bold">T</span>
            </div>
          </div>

          <div className="flex-1 flex flex-col items-center py-4 space-y-4">
            <button
              onClick={() => updateFilter('status', 'all')}
              className={`p-2 rounded-lg ${statusFilter === 'all' ? 'bg-indigo-100 dark:bg-indigo-900/50' : 'hover:bg-[rgb(var(--bg-tertiary))]'}`}
              title="All Tasks"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-[rgb(var(--text-primary))]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>

            <button
              onClick={() => updateFilter('status', 'pending')}
              className={`p-2 rounded-lg ${statusFilter === 'pending' ? 'bg-indigo-100 dark:bg-indigo-900/50' : 'hover:bg-[rgb(var(--bg-tertiary))]'}`}
              title="Pending"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-[rgb(var(--text-primary))]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>

            <button
              onClick={() => updateFilter('status', 'completed')}
              className={`p-2 rounded-lg ${statusFilter === 'completed' ? 'bg-indigo-100 dark:bg-indigo-900/50' : 'hover:bg-[rgb(var(--bg-tertiary))]'}`}
              title="Completed"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-[rgb(var(--text-primary))]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </button>

            <button
              onClick={() => updateFilter('priority', 'urgent')}
              className={`p-2 rounded-lg ${priorityFilter === 'urgent' ? 'bg-indigo-100 dark:bg-indigo-900/50' : 'hover:bg-[rgb(var(--bg-tertiary))]'}`}
              title="Urgent"
            >
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-[rgb(var(--text-primary))]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
            </button>
          </div>
        </div>
      ) : (
        /* Expanded version */
        <div className="w-64 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen">
          <div className="p-6">
            <h2 className="text-lg font-semibold text-[rgb(var(--text-primary))] mb-6">Filters</h2>

            <div className="space-y-6">
              {/* Status Filter */}
              <div>
                <h3 className="text-sm font-medium text-[rgb(var(--text-primary))] mb-3">Status</h3>
                <div className="space-y-2">
                  {(['all', 'pending', 'completed'] as TaskStatusFilter[]).map((status) => (
                    <button
                      key={status}
                      onClick={() => updateFilter('status', status)}
                      className={`block w-full text-left px-3 py-2 rounded-md text-sm ${
                        statusFilter === status
                          ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-800 dark:text-indigo-200'
                          : 'hover:bg-[rgb(var(--bg-tertiary))] text-[rgb(var(--text-secondary))]'
                      }`}
                    >
                      {status.charAt(0).toUpperCase() + status.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Priority/Tag Filter */}
              <div>
                <h3 className="text-sm font-medium text-[rgb(var(--text-primary))] mb-3">Priority/Tag</h3>
                <div className="space-y-2">
                  {(['all', 'normal', 'urgent', 'important', 'urgent-important'] as const).map((tag) => (
                    <button
                      key={tag}
                      onClick={() => updateFilter('priority', tag)}
                      className={`block w-full text-left px-3 py-2 rounded-md text-sm ${
                        priorityFilter === tag
                          ? 'bg-indigo-100 dark:bg-indigo-900/50 text-indigo-800 dark:text-indigo-200'
                          : 'hover:bg-[rgb(var(--bg-tertiary))] text-[rgb(var(--text-secondary))]'
                      }`}
                    >
                      {tag === 'urgent-important' ? 'Urgent & Important' : tag.charAt(0).toUpperCase() + tag.slice(1)}
                    </button>
                  ))}
                </div>
              </div>

              {/* Clear Filters */}
              {(statusFilter !== 'all' || priorityFilter !== 'all') && (
                <button
                  onClick={clearFilters}
                  className="w-full mt-4 px-3 py-2 text-sm text-[rgb(var(--text-secondary))] hover:bg-[rgb(var(--bg-tertiary))] rounded-md"
                >
                  Clear all filters
                </button>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}

export default function CollapsibleTaskSidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [mounted, setMounted] = useState(false);

  // Check if we're on mobile and handle responsive behavior
  useEffect(() => {
    if (typeof window !== 'undefined') {
      setMounted(true);

      const checkIsMobile = () => {
        const mobile = window.innerWidth < 768;
        setIsMobile(mobile);

        if (mobile) {
          // On mobile, hide sidebar initially
          setIsCollapsed(true);
        } else {
          // On desktop, close mobile menu
          setIsMobileMenuOpen(false);
        }
      };

      checkIsMobile(); // Run on mount
      window.addEventListener('resize', checkIsMobile);

      return () => {
        window.removeEventListener('resize', checkIsMobile);
      };
    }
  }, []);

  const toggleSidebar = () => {
    if (isMobile) {
      // On mobile, toggle the mobile menu
      setIsMobileMenuOpen(!isMobileMenuOpen);
    } else {
      // On desktop, toggle the sidebar collapse state
      setIsCollapsed(!isCollapsed);
    }
  };

  // Don't render until mounted to avoid SSR issues
  if (!mounted) {
    return (
      <div className="w-64 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen p-6">
        <p className="text-[rgb(var(--text-primary))]">Loading...</p>
      </div>
    );
  }

  return (
    <div className="relative">
      {/* Mobile menu button - only visible on mobile */}
      <button
        onClick={toggleSidebar}
        className="md:hidden fixed top-4 left-4 z-50 p-2 rounded-lg bg-[rgb(var(--bg-secondary))] text-[rgb(var(--text-primary))] shadow-md hover:bg-[rgb(var(--bg-tertiary))] transition-colors"
        aria-label={isMobileMenuOpen ? "Close menu" : "Open menu"}
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          {isMobileMenuOpen ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
          ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
          )}
        </svg>
      </button>

      {/* Mobile overlay - covers main content when menu is open */}
      {isMobileMenuOpen && (
        <div
          className="md:hidden fixed inset-0 z-40 bg-black bg-opacity-50"
          onClick={() => setIsMobileMenuOpen(false)}
        ></div>
      )}

      {/* Sidebar - conditionally rendered based on mobile/desktop and open/closed state */}
      {isMobileMenuOpen ? (
        // Mobile menu open - full overlay
        <div className="md:hidden fixed top-0 left-0 h-full z-40 w-64">
          <Suspense fallback={
            <div className="w-64 bg-[rgb(var(--bg-primary))] min-h-screen p-6">
              <p className="text-[rgb(var(--text-primary))]">Loading filters...</p>
            </div>
          }>
            <CollapsibleTaskSidebarContent isCollapsed={false} />
          </Suspense>
        </div>
      ) : (
        // Desktop or mobile menu closed
        <div className={`${isMobile ? 'hidden md:block' : ''} ${isCollapsed ? 'w-20' : 'w-64'} transition-all duration-300 ease-in-out`}>
          <Suspense fallback={isCollapsed ? (
            <div className="w-20 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen"></div>
          ) : (
            <div className="w-64 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen p-6">
              <p className="text-[rgb(var(--text-primary))]">Loading filters...</p>
            </div>
          )}>
            <CollapsibleTaskSidebarContent isCollapsed={isCollapsed} />
          </Suspense>

          {/* Desktop collapse/expand toggle */}
          {!isMobile && (
            <button
              onClick={toggleSidebar}
              className="absolute top-4 -right-3 z-10 p-1.5 rounded-full bg-[rgb(var(--bg-secondary))] text-[rgb(var(--text-primary))] shadow-md hover:bg-[rgb(var(--bg-tertiary))] transition-colors"
              aria-label={isCollapsed ? "Expand sidebar" : "Collapse sidebar"}
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-4 w-4"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                style={{ transform: isCollapsed ? 'rotate(-180deg)' : 'rotate(0deg)', transition: 'transform 0.3s ease' }}
              >
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 19l-7-7 7-7" />
              </svg>
            </button>
          )}
        </div>
      )}
    </div>
  );
}