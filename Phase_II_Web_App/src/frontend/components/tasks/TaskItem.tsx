'use client'

import { useState } from 'react'
import { Task } from '@/lib/types'
import { updateTask, deleteTask, toggleTaskCompletion } from '@/lib/api'
import EditTaskModal from './EditTaskModal'

export default function TaskItem({ task, onTaskUpdate }: { task: Task; onTaskUpdate: () => void }) {
  const [isEditing, setIsEditing] = useState(false)
  const [isLoading, setIsLoading] = useState(false)

  const handleToggleCompletion = async () => {
    setIsLoading(true)
    try {
      await toggleTaskCompletion(task.id)
      onTaskUpdate()
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleTaskClick = async () => {
    // Toggle completion when clicking the task title
    setIsLoading(true)
    try {
      await toggleTaskCompletion(task.id)
      onTaskUpdate()
    } catch (error) {
      console.error('Failed to toggle task completion:', error)
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
    } catch (error) {
      console.error('Failed to delete task:', error)
    } finally {
      setIsLoading(false)
    }
  }

  // Format the created date
  const formattedDate = new Date(task.created_at).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });

  // Determine priority display and styling
  const getPriorityDisplay = (priority: 'low' | 'normal' | 'urgent' | undefined) => {
    if (!priority) return null;

    const priorityStyles = {
      low: 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300',
      normal: 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300',
      urgent: 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300',
    };

    const priorityLabels = {
      low: 'Low',
      normal: 'Normal',
      urgent: 'Urgent',
    };

    return (
      <span className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium ${priorityStyles[priority]}`}>
        {priorityLabels[priority]}
      </span>
    );
  };

  return (
    <li className="border rounded-md p-4 bg-white dark:bg-gray-800 border-gray-200 dark:border-gray-700">
      <div className="flex items-center justify-between">
        <div className="flex items-center">
          <input
            type="checkbox"
            checked={task.completed}
            onChange={handleToggleCompletion}
            disabled={isLoading}
            className="h-4 w-4 text-indigo-600 dark:text-indigo-400 focus:ring-indigo-500 dark:focus:ring-indigo-400 border-gray-300 dark:border-gray-600 rounded bg-white dark:bg-gray-700"
          />
          <div className="ml-3">
            <div className="flex items-center space-x-2">
              <span
                className={`block cursor-pointer ${task.completed ? 'line-through text-gray-500 dark:text-gray-400' : 'text-gray-800 dark:text-gray-200 hover:text-indigo-600 dark:hover:text-indigo-400'}`}
                onClick={handleTaskClick}
              >
                {task.title}
              </span>
              {getPriorityDisplay('normal')} {/* Using default priority for now - would come from task data */}
            </div>
            <div className="flex items-center mt-1 space-x-2">
              <span className="text-xs text-gray-500 dark:text-gray-400">
                {formattedDate}
              </span>
            </div>
          </div>
        </div>
        <div className="flex space-x-2">
          <button
            onClick={() => setIsEditing(true)}
            disabled={isLoading}
            className="text-sm font-medium text-indigo-600 dark:text-indigo-400 hover:text-indigo-500 dark:hover:text-indigo-300"
          >
            Edit
          </button>
          <button
            onClick={handleDelete}
            disabled={isLoading}
            className="text-sm font-medium text-red-600 dark:text-red-400 hover:text-red-500 dark:hover:text-red-300"
          >
            Delete
          </button>
        </div>
      </div>
      {task.description && (
        <p className="mt-2 text-sm text-gray-600 dark:text-gray-300">{task.description}</p>
      )}

      {isEditing && (
        <EditTaskModal
          task={task}
          onClose={() => setIsEditing(false)}
          onTaskUpdated={onTaskUpdate}
        />
      )}
    </li>
  )
}