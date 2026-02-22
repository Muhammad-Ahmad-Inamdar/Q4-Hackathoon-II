'use client'

import { useState } from 'react'
import { Task } from '@/lib/types'
import { deleteTask, toggleTaskCompletion } from '@/lib/api'
import { useToast } from '@/context/ToastContext'
// Yeh import zaroori hai edit window open karne ke liye
import EditTaskModal from './EditTaskModal' 

export default function TaskItem({ task, onTaskUpdate }: { task: Task; onTaskUpdate: () => void }) {
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)
  const { showToast } = useToast()

  const handleToggleCompletion = async () => {
    setIsLoading(true)
    try {
      await toggleTaskCompletion(task.id)
      onTaskUpdate()
      showToast(`Task marked as ${task.completed ? 'incomplete' : 'completed'}!`, 'success')
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
      showToast('Failed to update task status. Please try again.', 'error')
    } finally {
      setIsLoading(false)
    }
  }

  const handleTaskClick = async () => {
    setIsLoading(true)
    try {
      await toggleTaskCompletion(task.id)
      onTaskUpdate()
      showToast(`Task marked as ${task.completed ? 'incomplete' : 'completed'}!`, 'success')
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
      showToast('Failed to update task status. Please try again.', 'error')
    } finally {
      setIsLoading(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('Are you sure you want to delete this task?')) {
      return
    }

    setIsLoading(true)
    try {
      await deleteTask(task.id)
      onTaskUpdate()
      showToast('Task deleted successfully!', 'success')
    } catch (error) {
      console.error('Failed to delete task:', error)
      showToast('Failed to delete task. Please try again.', 'error')
    } finally {
      setIsLoading(false)
    }
  }

  const formattedDate = new Date(task.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  const getPriorityDisplay = (priority: 'low' | 'normal' | 'urgent' | 'high' | 'critical' | 'important' | 'urgent-important' | undefined) => {
    if (!priority) return null;

    const priorityStyles: Record<string, string> = {
      // Light theme: Solid vibrant backgrounds with white text for maximum contrast
      // Dark theme: Darker backgrounds with light text
      low: 'bg-green-500 text-white dark:bg-green-700 dark:text-green-100 border border-green-600 dark:border-green-600',
      normal: 'bg-yellow-500 text-white dark:bg-yellow-600 dark:text-yellow-100 border border-yellow-600 dark:border-yellow-500',
      high: 'bg-orange-500 text-white dark:bg-orange-700 dark:text-orange-100 border border-orange-600 dark:border-orange-600',
      urgent: 'bg-red-500 text-white dark:bg-red-700 dark:text-red-100 border border-red-600 dark:border-red-600',
      important: 'bg-blue-500 text-white dark:bg-blue-700 dark:text-blue-100 border border-blue-600 dark:border-blue-600',
      'urgent-important': 'bg-purple-600 text-white dark:bg-purple-700 dark:text-purple-100 border border-purple-700 dark:border-purple-600',
      critical: 'bg-fuchsia-600 text-white dark:bg-fuchsia-700 dark:text-fuchsia-100 border border-fuchsia-700 dark:border-fuchsia-600',
    };

    const priorityLabels: Record<string, string> = {
      low: 'Low',
      normal: 'Normal',
      high: 'High',
      urgent: 'Urgent',
      important: 'Important',
      'urgent-important': 'Urgent & Important',
      critical: 'Critical',
    };

    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-xs font-semibold ${priorityStyles[priority]} shadow-sm`}>
        {priorityLabels[priority]}
      </span>
    );
  };

  const getStatusBadge = () => {
    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold ${
        task.completed
          ? 'bg-green-500 text-white dark:bg-green-700 dark:text-green-100 border border-green-600 dark:border-green-600'
          : 'bg-blue-500 text-white dark:bg-blue-700 dark:text-blue-100 border border-blue-600 dark:border-blue-600'
      }`}>
        {task.completed ? '✓ Completed' : '○ Pending'}
      </span>
    );
  };

  return (
    <li className="relative overflow-hidden rounded-xl bg-[rgb(var(--bg-secondary))] shadow-sm hover:shadow-md transition-all duration-200 border border-[rgb(var(--border-primary))] group">
      <div className="absolute top-0 left-0 h-1 bg-gradient-to-r from-indigo-500 to-purple-500 w-full opacity-0 group-hover:opacity-100 transition-opacity duration-200"></div>

      <div className="p-4 sm:p-5">
        <div className="flex flex-col sm:flex-row sm:items-start justify-between gap-3 sm:gap-0">
          <div className="flex items-start space-x-3">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={handleToggleCompletion}
              disabled={isLoading}
              className="mt-1 h-4 w-4 text-indigo-600 dark:text-indigo-400 focus:ring-indigo-500 dark:focus:ring-indigo-400 border-[rgb(var(--border-primary))] rounded bg-[rgb(var(--bg-primary))] shadow-sm"
            />
            <div className="flex-1 min-w-0">
              <div className="flex flex-wrap items-center gap-2">
                <span
                  className={`text-base font-semibold cursor-pointer ${task.completed ? 'line-through text-[rgb(var(--text-secondary))] text-sm sm:text-base' : 'text-[rgb(var(--text-primary))] hover:text-indigo-600 dark:hover:text-indigo-400 text-sm sm:text-base'}`}
                  onClick={handleTaskClick}
                >
                  {task.title}
                </span>
                {getStatusBadge()}
                {getPriorityDisplay(task.priority || 'normal')}
              </div>

              {task.description && (
                <p className="mt-2 text-sm text-[rgb(var(--text-secondary))] break-words">
                  {task.description}
                </p>
              )}

              <div className="mt-3 flex flex-wrap items-center gap-2 text-xs sm:text-sm">
                <span className="inline-flex items-center text-[rgb(var(--text-secondary))]">
                  <svg className="mr-1.5 h-4 w-4 text-[rgb(var(--text-muted))]" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  {formattedDate}
                </span>
              </div>
            </div>
          </div>

          <div className="flex space-x-1 self-start">
            <button
              onClick={() => setIsEditing(true)}
              disabled={isLoading}
              className="inline-flex items-center p-2 text-sm font-medium text-[rgb(var(--text-secondary))] hover:text-indigo-600 dark:hover:text-indigo-400 hover:bg-[rgb(var(--bg-tertiary))] rounded-lg transition-colors duration-200"
              title="Edit task"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
              </svg>
            </button>
            <button
              onClick={handleDelete}
              disabled={isLoading}
              className="inline-flex items-center p-2 text-sm font-medium text-[rgb(var(--text-secondary))] hover:text-red-600 dark:hover:text-red-400 hover:bg-[rgb(var(--bg-tertiary))] rounded-lg transition-colors duration-200"
              title="Delete task"
            >
              <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>

      {isEditing && (
        <EditTaskModal
          task={task}
          onClose={() => setIsEditing(false)}
          onTaskUpdated={onTaskUpdate}
        />
      )}
    </li>
  );
}