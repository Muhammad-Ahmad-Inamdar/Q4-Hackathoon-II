'use client'

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import TaskList from './components/TaskList'
import { useAuth } from '@/context/AuthContext'

export default function DashboardPage() {
  const router = useRouter()
  const { state } = useAuth();
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Since we're using the AuthProvider context, the authentication state is managed globally
    // We just need to check if the user is authenticated and redirect if not
    if (!state.isLoading && !state.isAuthenticated) {
      router.push('/login')
    }
    setLoading(false)
  }, [state, router])

  if (loading || state.isLoading) {
    return <div className="min-h-screen bg-gray-50 flex items-center justify-center">Checking authentication...</div>
  }

  if (!state.isAuthenticated) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="py-12">
        <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="bg-white shadow overflow-hidden sm:rounded-lg">
            <div className="px-4 py-5 sm:px-6 border-b border-gray-200">
              <h3 className="text-lg leading-6 font-medium text-gray-900">Task Dashboard</h3>
              {state.user?.email && (
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  Welcome back, {state.user.email}! Manage your tasks efficiently.
                </p>
              )}
            </div>
            <div className="px-4 py-5 sm:p-6">
              <TaskList />
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}