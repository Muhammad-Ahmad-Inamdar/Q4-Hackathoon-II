'use client';

import { useEffect, useState } from 'react'
import { useRouter } from 'next/navigation'
import TaskList from './components/TaskList'
import { useAuth } from '@/context/AuthContext'
import CollapsibleTaskSidebar from '@/components/common/CollapsibleTaskSidebar'
import ChatbotPopup from '@/components/chat/ChatbotPopup'

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
    return (
      <div className="min-h-screen bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
          <p className="text-lg text-[rgb(var(--text-secondary))]">Loading your dashboard...</p>
        </div>
      </div>
    );
  }

  if (!state.isAuthenticated) {
    return null; // Redirect happens in useEffect
  }

  return (
    <div className="flex flex-col md:flex-row">
      <CollapsibleTaskSidebar />
      <main className="flex-1 py-8 w-full overflow-x-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="mb-8">
            <h1 className="text-3xl font-bold text-[rgb(var(--text-primary))]">Task Dashboard</h1>
            {state.user?.email && (
              <p className="mt-2 text-lg text-[rgb(var(--text-secondary))]">
                Welcome back, <span className="font-semibold text-indigo-600 dark:text-indigo-400">{state.user.email}</span>! Manage your tasks efficiently.
              </p>
            )}
          </div>

          <div className="bg-[rgb(var(--bg-secondary))] rounded-2xl shadow-xl p-4 sm:p-6 transition-all duration-300 hover:shadow-2xl overflow-x-auto">
            <TaskList />
          </div>
        </div>
      </main>
      
      {/* AI Chatbot */}
      <ChatbotPopup />
    </div>
  )
}