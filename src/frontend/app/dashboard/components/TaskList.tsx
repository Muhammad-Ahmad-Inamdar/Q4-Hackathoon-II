'use client'

import { useEffect, useState, useMemo } from 'react'
import { Task, TaskStatusFilter } from '@/lib/types'
import { getTasks } from '@/lib/api'
import TaskItem from '@/components/tasks/TaskItem'
import CreateTaskModal from '@/components/tasks/CreateTaskModal'
import { useSearchParams } from 'next/navigation'

export default function DashboardTaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const searchParams = useSearchParams()

  useEffect(() => {
    fetchTasks()
    
    // Listen for tasks-changed event from chatbot
    const handleTasksChanged = () => {
      console.log('Tasks changed event received, refreshing...')
      fetchTasks()
    }
    
    window.addEventListener('tasks-changed', handleTasksChanged)
    
    return () => {
      window.removeEventListener('tasks-changed', handleTasksChanged)
    }
  }, [])

  const fetchTasks = async () => {
    try {
      const data = await getTasks()
      setTasks(data)
    } catch (error) {
      console.error('Failed to fetch tasks:', error)
      // Show a user-friendly error message
      if (error instanceof Error && error.message.includes('Network error')) {
        alert('Could not connect to the server. Please make sure the backend is running.');
      } else if (error instanceof Error && error.message.includes('401')) {
        // If unauthorized, redirect to login
        window.location.href = '/login';
      }
    } finally {
      setLoading(false)
    }
  }

  const refreshTasks = () => {
    fetchTasks()
  }

  // Get filters from URL parameters
  const statusFilter = (searchParams.get('status') as TaskStatusFilter) || 'all'
  const priorityFilter = searchParams.get('priority') || 'all'

  // Filter and sort tasks based on URL parameters
  const filteredTasks = useMemo(() => {
    let result = [...tasks]

    // Apply status filter
    if (statusFilter === 'pending') {
      result = result.filter(task => !task.completed)
    } else if (statusFilter === 'completed') {
      result = result.filter(task => task.completed)
    }

    // Apply priority/tag filter
    if (priorityFilter !== 'all') {
      // Filter by the actual priority field in the task
      result = result.filter(task => {
        // Use the task's priority field if it exists, otherwise default to 'normal'
        const taskPriority = task.priority || 'normal';

        return taskPriority === priorityFilter;
      });
    }

    // Sort by creation date (newest first)
    result.sort((a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime());

    return result
  }, [tasks, statusFilter, priorityFilter])

  if (loading) {
    return (
      <div className="space-y-4 w-full overflow-x-auto">
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
          <div className="h-8 w-48 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
          <div className="flex flex-wrap gap-2">
            <div className="h-10 w-24 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
          </div>
        </div>

        <div className="space-y-2 w-full overflow-x-auto">
          {[...Array(3)].map((_, index) => (
            <div key={index} className="rounded-xl bg-[rgb(var(--bg-secondary))] shadow-sm border border-[rgb(var(--border-primary))] p-4 sm:p-5">
              <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 sm:gap-0">
                <div className="flex items-start space-x-3">
                  <div className="mt-1 h-5 w-5 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
                  <div className="flex-1 min-w-0">
                    <div className="flex flex-wrap items-center gap-2">
                      <div className="h-5 w-32 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
                      <div className="h-5 w-16 bg-[rgb(var(--bg-tertiary))] rounded-full animate-pulse"></div>
                      <div className="h-5 w-20 bg-[rgb(var(--bg-tertiary))] rounded-full animate-pulse"></div>
                    </div>
                    <div className="mt-2 h-4 w-full bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
                    <div className="mt-2 h-4 w-3/4 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
                    <div className="mt-3 flex flex-wrap items-center gap-2">
                      <div className="h-4 w-24 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
                      <div className="flex items-center">
                        <div className="w-16 h-2 bg-[rgb(var(--bg-tertiary))] rounded-full animate-pulse mr-2"></div>
                        <div className="h-3 w-8 bg-[rgb(var(--bg-tertiary))] rounded animate-pulse"></div>
                      </div>
                    </div>
                  </div>
                </div>
                <div className="flex space-x-1 self-start">
                  <div className="h-8 w-8 bg-[rgb(var(--bg-tertiary))] rounded-lg animate-pulse"></div>
                  <div className="h-8 w-8 bg-[rgb(var(--bg-tertiary))] rounded-lg animate-pulse"></div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-4 w-full overflow-x-auto">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-xl font-bold text-[rgb(var(--text-primary))]">Your Tasks</h2>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setShowModal(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 dark:bg-indigo-700 hover:bg-indigo-700 dark:hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 whitespace-nowrap"
          >
            + Add Task
          </button>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-[rgb(var(--text-secondary))]">
            {tasks.length === 0
              ? 'No tasks yet. Create your first task!'
              : statusFilter !== 'all' || priorityFilter !== 'all'
                ? 'No tasks match your filters.'
                : 'No tasks found.'
            }
          </p>
        </div>
      ) : (
        <ul className="space-y-2 w-full overflow-x-auto">
          {filteredTasks.map((task) => (
            <TaskItem key={task.id} task={task} onTaskUpdate={refreshTasks} />
          ))}
        </ul>
      )}

      {showModal && (
        <CreateTaskModal
          onClose={() => setShowModal(false)}
          onTaskCreated={refreshTasks}
        />
      )}
    </div>
  )
}