'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { useAuth } from '@/context/AuthContext'
import { login as apiLogin } from '@/lib/auth'

export default function LoginForm() {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const router = useRouter()
  const { login: updateAuthState } = useAuth()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')

    try {
      const result = await apiLogin(email, password)

      // Extract user info from the result or decode from token
      const token = result.access_token
      if (token) {
        // Decode token to get user info
        const tokenParts = token.split('.')
        let userId = 'unknown'
        let userEmail = email

        if (tokenParts.length === 3) {
          try {
            const payload = JSON.parse(atob(tokenParts[1]))
            userId = payload.user_id || payload.sub || 'unknown'
            userEmail = payload.email || email
          } catch (decodeErr) {
            console.error('Error decoding token:', decodeErr)
          }
        }

        // Update auth context
        updateAuthState({ id: userId, email: userEmail })
      }

      router.push('/dashboard')
      router.refresh()
    } catch (err: any) {
      // Handle error properly to avoid [object Object] display
      if (err instanceof Error) {
        setError(err.message || 'An error occurred during login')
      } else if (typeof err === 'string') {
        setError(err)
      } else {
        setError('An error occurred during login')
      }
    }
  }

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {error && (
        <div className="rounded-md bg-red-50 p-4">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      <div>
        <label htmlFor="email" className="block text-sm font-medium text-[rgb(var(--text-primary))]">
          Email address
        </label>
        <div className="mt-1">
          <input
            id="email"
            name="email"
            type="email"
            autoComplete="email"
            required
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="appearance-none block w-full px-3 py-3 border border-[rgb(var(--border-primary))] rounded-lg shadow-sm placeholder-[rgb(var(--text-muted))] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] sm:text-sm transition-all duration-200"
          />
        </div>
      </div>

      <div>
        <label htmlFor="password" className="block text-sm font-medium text-[rgb(var(--text-primary))]">
          Password
        </label>
        <div className="mt-1">
          <input
            id="password"
            name="password"
            type="password"
            autoComplete="current-password"
            required
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="appearance-none block w-full px-3 py-3 border border-[rgb(var(--border-primary))] rounded-lg shadow-sm placeholder-[rgb(var(--text-muted))] focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 bg-[rgb(var(--bg-primary))] text-[rgb(var(--text-primary))] sm:text-sm transition-all duration-200"
          />
        </div>
      </div>

      <div>
        <button
          type="submit"
          className="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 transition-all duration-200 transform hover:scale-[1.02]"
        >
          Sign in
        </button>
      </div>

      <div className="text-sm text-[rgb(var(--text-secondary))]">
        Don't have an account?{' '}
        <Link href="/signup" className="font-medium text-indigo-600 hover:text-indigo-500">
          Sign up
        </Link>
      </div>
    </form>
  )
}