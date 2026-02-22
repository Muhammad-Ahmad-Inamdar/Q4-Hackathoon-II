'use client'

import { useEffect, useState } from 'react'
import { Task, TaskStatusFilter } from '@/lib/types'
import { getTasks } from '@/lib/api'
import TaskItem from './TaskItem'
import CreateTaskModal from './CreateTaskModal'

export default function TaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [statusFilter, setStatusFilter] = useState<TaskStatusFilter>('all')

  useEffect(() => {
    fetchTasks()
  }, [])

  useEffect(() => {
    // Apply filters to tasks
    let result = [...tasks]

    if (statusFilter === 'pending') {
      result = result.filter(task => !task.completed)
    } else if (statusFilter === 'completed') {
      result = result.filter(task => task.completed)
    }

    setFilteredTasks(result)
  }, [tasks, statusFilter])

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

  if (loading) {
    return <div className="text-center py-8 text-gray-700 dark:text-gray-300">Loading tasks...</div>
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-xl font-bold text-gray-800 dark:text-white">Your Tasks</h2>

        <div className="flex flex-wrap gap-2">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value as TaskStatusFilter)}
            className="inline-flex items-center px-3 py-2 border border-gray-300 dark:border-gray-600 text-sm font-medium rounded-md text-gray-700 dark:text-gray-200 bg-white dark:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500"
          >
            <option value="all">All Tasks</option>
            <option value="pending">Pending</option>
            <option value="completed">Completed</option>
          </select>

          <button
            onClick={() => setShowModal(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 dark:bg-indigo-700 hover:bg-indigo-700 dark:hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Add Task
          </button>
        </div>
      </div>

      {filteredTasks.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">
            {tasks.length === 0
              ? 'No tasks yet. Create your first task!'
              : statusFilter === 'all'
                ? 'No tasks yet. Create your first task!'
                : `No ${statusFilter} tasks.`
            }
          </p>
        </div>
      ) : (
        <ul className="space-y-2">
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