'use client';

import { usePathname, useRouter, useSearchParams } from 'next/navigation';
import { TaskStatusFilter } from '@/lib/types';
import { Suspense } from 'react';

function TaskSidebarContent() {
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
    <aside className="w-64 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen">
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
    </aside>
  );
}

export default function TaskSidebar() {
  return (
    <Suspense fallback={<div className="w-64 bg-[rgb(var(--bg-primary))] border-r border-[rgb(var(--border-primary))] min-h-screen p-6"><p className="text-[rgb(var(--text-primary))]">Loading filters...</p></div>}>
      <TaskSidebarContent />
    </Suspense>
  );
}