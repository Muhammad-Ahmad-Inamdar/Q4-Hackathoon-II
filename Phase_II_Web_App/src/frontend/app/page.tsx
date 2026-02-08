import Link from 'next/link'
import AuthGuard from '@/components/common/AuthGuard'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 dark:from-gray-900 dark:to-gray-800 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
      <div className="mt-8 sm:mx-auto sm:w-full sm:max-w-lg">
        <div className="bg-white dark:bg-gray-800 py-8 px-6 shadow-xl sm:rounded-2xl sm:px-10 border border-gray-200 dark:border-gray-700">
          <div className="text-center">
            <div className="mx-auto h-12 w-12 rounded-full bg-indigo-600 flex items-center justify-center">
              <span className="text-white text-xl font-bold">T</span>
            </div>
            <h1 className="mt-4 text-3xl font-extrabold text-gray-900 dark:text-white sm:text-4xl">
              TaskMaster Pro
            </h1>
            <p className="mt-3 text-lg text-gray-500 dark:text-gray-400">
              Streamline your productivity with our elegant task management solution
            </p>
          </div>

          {/* Show login/signup links only when not authenticated */}
          <AuthGuard fallback={
            <div className="mt-8">
              <div className="bg-gray-50 dark:bg-gray-700/50 rounded-lg p-6 text-center">
                <p className="text-gray-700 dark:text-gray-300 mb-6">
                  Get started with our powerful task management platform
                </p>
                <div className="flex flex-col sm:flex-row justify-center gap-4">
                  <Link
                    href="/login"
                    className="flex-1 inline-block w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
                  >
                    Sign In
                  </Link>
                  <Link
                    href="/signup"
                    className="flex-1 inline-block w-full py-3 px-4 border border-transparent rounded-md shadow-sm text-base font-medium text-indigo-700 bg-indigo-100 hover:bg-indigo-200 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 dark:text-white dark:bg-indigo-600 dark:hover:bg-indigo-700"
                  >
                    Create Account
                  </Link>
                </div>
              </div>
            </div>
          }>
            {/* Show welcome message when authenticated */}
            <div className="mt-8 text-center">
              <p className="text-gray-700 dark:text-gray-300 mb-6">
                You are logged in and ready to boost your productivity!
              </p>
              <Link
                href="/dashboard"
                className="inline-block py-3 px-6 border border-transparent rounded-md shadow-sm text-base font-medium text-white bg-indigo-600 hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500"
              >
                Go to Dashboard
              </Link>
            </div>
          </AuthGuard>

          <div className="mt-8 text-center">
            <p className="text-xs text-gray-500 dark:text-gray-400">
              © {new Date().getFullYear()} TaskMaster Pro. All rights reserved.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}