import { useState } from 'react';
import { updateTask } from '@/lib/api'
import TaskForm from './TaskForm'
import { Task, TaskUpdate } from '@/lib/types'
import { useToast } from '@/context/ToastContext'

interface EditTaskModalProps {
  task: Task;
  onClose: () => void;
  onTaskUpdated: () => void;
}

export default function EditTaskModal({ task, onClose, onTaskUpdated }: EditTaskModalProps) {
  const { showToast } = useToast();
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (data: TaskUpdate) => {
    if (isSubmitting) return; // Prevent duplicate submissions

    try {
      setIsSubmitting(true);
      await updateTask(task.id, data);
      onTaskUpdated();
      onClose();
      showToast('Task updated successfully!', 'success');
    } catch (error) {
      console.error('Failed to update task:', error);
      showToast('Failed to update task. Please try again.', 'error');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 dark:bg-opacity-70 overflow-y-auto h-full w-full flex items-center justify-center z-50">
      <div className="relative bg-white dark:bg-gray-800 rounded-lg shadow-xl p-6 max-w-md w-full mx-4 border border-gray-200 dark:border-gray-700">
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-lg font-medium text-gray-900 dark:text-white">Edit Task</h3>
          <button
            onClick={onClose}
            className="text-gray-400 dark:text-gray-300 hover:text-gray-500 dark:hover:text-gray-200"
            disabled={isSubmitting}
          >
            <span className="sr-only">Close</span>
            <svg className="h-6 w-6" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        <TaskForm
          initialData={{ title: task.title, description: task.description, completed: task.completed }}
          onSubmit={handleSubmit}
          onCancel={onClose}
          submitLabel={isSubmitting ? 'Updating...' : 'Update Task'}
          isUpdating={true}
          isSubmitting={isSubmitting}
        />
      </div>
    </div>
  )
}