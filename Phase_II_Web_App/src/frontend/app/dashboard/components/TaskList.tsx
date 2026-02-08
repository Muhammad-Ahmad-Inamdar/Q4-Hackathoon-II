'use client'

import { useEffect, useState } from 'react'
import { Task, TaskStatusFilter } from '@/lib/types'
import { getTasks } from '@/lib/api'
import TaskItem from '@/components/tasks/TaskItem'
import CreateTaskModal from '@/components/tasks/CreateTaskModal'
import TaskFilters from './TaskFilters'

export default function DashboardTaskList() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([])
  const [loading, setLoading] = useState(true)
  const [showModal, setShowModal] = useState(false)
  const [filters, setFilters] = useState({
    status: 'all' as TaskStatusFilter,
    priority: 'all' as 'all' | 'low' | 'normal' | 'urgent',
    sortBy: 'createdAt' as 'createdAt' | 'title' | 'deadline' | 'priority',
    sortOrder: 'desc' as 'asc' | 'desc'
  })

  useEffect(() => {
    fetchTasks()
  }, [])

  useEffect(() => {
    // Apply filters and sorting to tasks
    let result = [...tasks]

    // Apply status filter
    if (filters.status === 'pending') {
      result = result.filter(task => !task.completed)
    } else if (filters.status === 'completed') {
      result = result.filter(task => task.completed)
    }

    // Apply priority filter
    if (filters.priority !== 'all') {
      // For now, we're assuming tasks have a priority property
      // In a real implementation, this would depend on how priority is stored
      result = result.filter(task => {
        // For demonstration purposes, we'll assign a priority based on title length
        // In a real implementation, tasks would have a priority field
        const taskPriority = task.title.length > 20 ? 'urgent' : task.title.length > 10 ? 'normal' : 'low';
        return taskPriority === filters.priority;
      });
    }

    // Apply sorting
    result.sort((a, b) => {
      let comparison = 0;
      if (filters.sortBy === 'createdAt') {
        comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
      } else if (filters.sortBy === 'title') {
        comparison = a.title.localeCompare(b.title);
      } else if (filters.sortBy === 'priority') {
        // Sort by priority: urgent > normal > low
        const priorityOrder = { 'urgent': 3, 'normal': 2, 'low': 1 };
        const aPriority = a.title.length > 20 ? 'urgent' : a.title.length > 10 ? 'normal' : 'low';
        const bPriority = b.title.length > 20 ? 'urgent' : b.title.length > 10 ? 'normal' : 'low';
        comparison = priorityOrder[bPriority] - priorityOrder[aPriority]; // Higher priority first
      } else if (filters.sortBy === 'deadline') {
        // For now, we'll use the created_at as deadline for demonstration purposes
        // In a real implementation, tasks would have a deadline field
        comparison = new Date(a.created_at).getTime() - new Date(b.created_at).getTime();
      }

      return filters.sortOrder === 'asc' ? comparison : -comparison;
    });

    setFilteredTasks(result)
  }, [tasks, filters])

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

  const handleStatusFilterChange = (filter: TaskStatusFilter) => {
    setFilters(prev => ({ ...prev, status: filter }))
  }

  const handlePriorityFilterChange = (filter: 'all' | 'low' | 'normal' | 'urgent') => {
    setFilters(prev => ({ ...prev, priority: filter }))
  }

  const handleSortByChange = (sortBy: 'createdAt' | 'title' | 'deadline' | 'priority') => {
    setFilters(prev => ({ ...prev, sortBy }))
  }

  const handleSortOrderChange = (order: 'asc' | 'desc') => {
    setFilters(prev => ({ ...prev, sortOrder: order }))
  }

  if (loading) {
    return <div className="text-center py-8 text-gray-700 dark:text-gray-300">Loading tasks...</div>
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-xl font-bold text-gray-800 dark:text-white">Your Tasks</h2>

        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setShowModal(true)}
            className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-indigo-600 dark:bg-indigo-700 hover:bg-indigo-700 dark:hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
          >
            Add Task
          </button>
        </div>
      </div>

      <TaskFilters
        statusFilter={filters.status}
        onStatusFilterChange={handleStatusFilterChange}
        priorityFilter={filters.priority}
        onPriorityFilterChange={handlePriorityFilterChange}
        sortBy={filters.sortBy}
        onSortByChange={handleSortByChange}
        sortOrder={filters.sortOrder}
        onSortOrderChange={handleSortOrderChange}
      />

      {filteredTasks.length === 0 ? (
        <div className="text-center py-8">
          <p className="text-gray-500 dark:text-gray-400">
            {tasks.length === 0
              ? 'No tasks yet. Create your first task!'
              : filters.status === 'all'
                ? 'No tasks match your filters.'
                : `No ${filters.status} tasks.`
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