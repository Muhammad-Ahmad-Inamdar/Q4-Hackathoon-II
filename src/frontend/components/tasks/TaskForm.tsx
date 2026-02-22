import { useState } from 'react'
import { TaskCreate, TaskUpdate } from '@/lib/types'

interface TaskFormProps {
  initialData?: TaskUpdate;
  onSubmit: (data: TaskCreate | TaskUpdate) => void;
  onCancel: () => void;
  submitLabel: string;
  isUpdating?: boolean;
  isSubmitting?: boolean;
}

export default function TaskForm({ initialData, onSubmit, onCancel, submitLabel, isUpdating = false, isSubmitting = false }: TaskFormProps) {
  const [title, setTitle] = useState(initialData?.title || '')
  const [description, setDescription] = useState(initialData?.description || '')
  const [completed, setCompleted] = useState(initialData?.completed || false)
  const [priority, setPriority] = useState<'low' | 'normal' | 'urgent' | 'high' | 'important' | 'urgent-important' | 'critical'>(initialData?.priority || 'normal')
  const [error, setError] = useState('')

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()

    if (!title.trim()) {
      setError('Title is required')
      return
    }

    if (isSubmitting) return; // Prevent submission while already submitting

    const taskData = isUpdating
      ? { title: title.trim(), description: description.trim(), completed, priority }
      : { title: title.trim(), description: description.trim(), priority }

    onSubmit(taskData)
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      {error && (
        <div className="rounded-md bg-red-50 dark:bg-red-900/20 p-4 border border-red-200 dark:border-red-800">
          <p className="text-sm text-red-700 dark:text-red-300 font-medium">{error}</p>
        </div>
      )}

      <div>
        <label htmlFor="title" className="block text-sm font-medium text-[rgb(var(--text-secondary))]">
          Title
        </label>
        <div className="mt-1">
          <input
            id="title"
            name="title"
            type="text"
            required
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            disabled={isSubmitting}
            className="block w-full px-3 py-2 border border-[rgb(var(--border-primary))] rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] placeholder-[rgb(var(--text-muted))] disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          />
        </div>
      </div>

      <div>
        <label htmlFor="description" className="block text-sm font-medium text-[rgb(var(--text-secondary))]">
          Description
        </label>
        <div className="mt-1">
          <textarea
            id="description"
            name="description"
            rows={3}
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={isSubmitting}
            className="shadow-sm block p-2 w-full focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border border-[rgb(var(--border-primary))] rounded-md bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] placeholder-[rgb(var(--text-muted))] disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          />
        </div>
      </div>

      <div>
        <label htmlFor="priority" className="block text-sm font-medium text-[rgb(var(--text-secondary))]">
          Priority/Tag
        </label>
        <div className="mt-1">
          <select
            id="priority"
            name="priority"
            value={priority}
            onChange={(e) => setPriority(e.target.value as 'low' | 'normal' | 'urgent' | 'high' | 'important' | 'urgent-important' | 'critical')}
            disabled={isSubmitting}
            className="block w-full px-3 py-2 border border-[rgb(var(--border-primary))] rounded-md shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          >
            <option value="normal">Normal</option>
            <option value="urgent">Urgent</option>
            <option value="important">Important</option>
            <option value="urgent-important">Urgent & Important</option>
          </select>
        </div>
      </div>

      {isUpdating && (
        <div className="flex items-center">
          <input
            id="completed"
            name="completed"
            type="checkbox"
            checked={completed}
            onChange={(e) => setCompleted(e.target.checked)}
            disabled={isSubmitting}
            className="h-4 w-4 text-indigo-600 dark:text-indigo-400 focus:ring-indigo-500 dark:focus:ring-indigo-400 border-[rgb(var(--border-primary))] rounded bg-[rgb(var(--bg-primary))] disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
          />
          <label htmlFor="completed" className="ml-2 block text-sm text-[rgb(var(--text-primary))]">
            Completed
          </label>
        </div>
      )}

      <div className="flex justify-end space-x-3">
        <button
          type="button"
          onClick={onCancel}
          disabled={isSubmitting}
          className="inline-flex items-center px-4 py-2 border border-[rgb(var(--border-primary))] text-sm font-medium rounded-md shadow-sm text-[rgb(var(--text-primary))] bg-[rgb(var(--bg-primary))] hover:bg-[rgb(var(--bg-tertiary))] focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
        >
          Cancel
        </button>
        <button
          type="submit"
          disabled={isSubmitting}
          className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 dark:bg-indigo-700 hover:bg-indigo-700 dark:hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors duration-200"
        >
          {isSubmitting && (
            <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
          )}
          {submitLabel}
        </button>
      </div>
    </form>
  )
}