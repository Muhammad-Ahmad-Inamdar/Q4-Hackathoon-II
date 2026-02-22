'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { useAuth } from '@/context/AuthContext';
import ChatbotPopup from '@/components/chat/ChatbotPopup';

export default function Home() {
  const { state } = useAuth();
  const [isClient, setIsClient] = useState(false);

  useEffect(() => {
    setIsClient(true);
  }, []);

  return (
    <div className="min-h-screen bg-[rgb(var(--bg-primary))]">
      {/* Hero Section */}
      <section className="py-16 bg-gradient-to-br from-indigo-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex flex-col items-center text-center">
            {/* Logo and Brand */}
            <div className="mb-6">
              <div className="mx-auto h-24 w-24 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 flex items-center justify-center shadow-lg">
                <span className="text-white text-4xl font-bold">T</span>
              </div>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-bold bg-gradient-to-r from-indigo-600 to-purple-600 bg-clip-text text-transparent mb-6">
              TaskMaster Pro
            </h1>

            <p className="text-lg sm:text-xl text-[rgb(var(--text-secondary))] max-w-2xl mx-auto mb-10 leading-relaxed">
              Streamline your productivity with our elegant and intuitive task management solution.
              Organize, prioritize, and accomplish more with simplicity.
            </p>

            {/* Conditional buttons based on auth state */}
            {isClient && state.isAuthenticated ? (
              <Link
                href="/dashboard"
                className="px-10 py-4 bg-gradient-to-r from-green-600 to-emerald-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-lg"
              >
                Go to Dashboard
              </Link>
            ) : (
              <Link
                href="/signup"
                className="px-10 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 text-lg"
              >
                Let's Get Started
              </Link>
            )}

            <div className="text-sm text-[rgb(var(--text-secondary))] mt-6">
              A completely free task management solution
            </div>

            {/* Show sign in option when not authenticated */}
            {!state.isAuthenticated && (
              <div className="mt-4">
                <Link
                  href="/login"
                  className="text-[rgb(var(--text-secondary))] hover:text-[rgb(var(--text-primary))] underline"
                >
                  Already have an account? Sign in
                </Link>
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-16 bg-[rgb(var(--bg-primary))]">
        <div className="container mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="text-3xl sm:text-4xl font-bold text-[rgb(var(--text-primary))] mb-4">
              Powerful Features
            </h2>
            <p className="text-lg text-[rgb(var(--text-secondary))] max-w-2xl mx-auto">
              Everything you need to stay organized and boost your productivity
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {[
              {
                icon: "✅",
                title: "Task Management",
                description: "Create, organize, and track your tasks with ease"
              },
              {
                icon: "🔒",
                title: "Secure Platform",
                description: "Your data is protected with modern security practices"
              },
              {
                icon: "📱",
                title: "Responsive Design",
                description: "Access your tasks from any device, anywhere"
              },
              {
                icon: "⚡",
                title: "Fast & Efficient",
                description: "Quick task creation and management process"
              },
              {
                icon: "🔍",
                title: "Smart Filtering",
                description: "Organize tasks by status, priority, and more"
              },
              {
                icon: "🎯",
                title: "Focus Enhancement",
                description: "Stay focused on what matters most"
              }
            ].map((feature, index) => (
              <div
                key={index}
                className="bg-[rgb(var(--bg-secondary))] p-6 rounded-xl border border-[rgb(var(--border-primary))] hover:shadow-lg transition-all duration-300 hover:-translate-y-1 text-center"
              >
                <div className="text-4xl mb-4">{feature.icon}</div>
                <h3 className="text-xl font-semibold text-[rgb(var(--text-primary))] mb-2">{feature.title}</h3>
                <p className="text-[rgb(var(--text-secondary))]">{feature.description}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
      
      {/* AI Chatbot for authenticated users */}
      <ChatbotPopup />
    </div>
  )
}