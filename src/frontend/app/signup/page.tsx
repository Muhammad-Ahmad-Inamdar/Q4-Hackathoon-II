'use client'

import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import SignupForm from '@/components/auth/SignupForm'
import { useAuth } from '@/context/AuthContext'

export default function SignupPage() {
  const router = useRouter()
  const { state } = useAuth()

  useEffect(() => {
    // If user is already authenticated, redirect to dashboard
    if (state.isAuthenticated) {
      router.push('/dashboard')
    }
  }, [state, router])

  // If user is already logged in, don't show the signup form
  if (state.isAuthenticated) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex items-center justify-center">
        <p className="text-lg text-gray-700 dark:text-gray-300">You are already logged in. Redirecting to dashboard...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="sm:mx-auto sm:w-full sm:max-w-md w-full max-w-sm">
        <div className="text-center mb-8">
          <div className="mx-auto h-12 w-12 rounded-full bg-indigo-600 flex items-center justify-center">
            <span className="text-white font-bold">T</span>
          </div>
          <h2 className="mt-6 text-3xl font-extrabold text-[rgb(var(--text-primary))]">
            Create your account
          </h2>
          <p className="mt-2 text-[rgb(var(--text-secondary))]">
            Join thousands of productive individuals today
          </p>
        </div>

        <div className="bg-[rgb(var(--bg-secondary))] py-8 px-6 shadow-xl rounded-2xl border border-[rgb(var(--border-primary))]">
          <SignupForm />
        </div>

        <p className="mt-6 text-center text-sm text-[rgb(var(--text-secondary))]">
          Already have an account?{' '}
          <a
            href="/login"
            className="font-medium text-indigo-600 hover:text-indigo-500 dark:text-indigo-400 dark:hover:text-indigo-300"
          >
            Sign in
          </a>
        </p>
      </div>
    </div>
  )
}