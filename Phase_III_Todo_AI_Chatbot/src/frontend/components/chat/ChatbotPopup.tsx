'use client';

import React, { useState, useEffect, useRef } from 'react';
import { useAuth } from '@/context/AuthContext';
import { useToast } from '@/context/ToastContext';
import ChatMessage from './ChatMessage';
import ChatInput from './ChatInput';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

export default function ChatbotPopup() {
  const { state } = useAuth();
  const { showToast } = useToast();
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  // Parse AI response to detect task operations and show appropriate toasts
  const parseTaskOperation = (response: string): { operation: string; success: boolean } | null => {
    const lowerResponse = response.toLowerCase();
    
    // Success patterns
    const createdPatterns = ['task created', 'task added', 'created successfully', 'added successfully', 'i\'ve added', 'i have added'];
    const deletedPatterns = ['task deleted', 'task removed', 'deleted successfully', 'removed successfully', 'i\'ve deleted', 'i have deleted', 'i\'ve removed', 'i have removed'];
    const updatedPatterns = ['task updated', 'updated successfully', 'i\'ve updated', 'i have updated', 'task modified', 'modified successfully'];
    const completedPatterns = ['task completed', 'marked as complete', 'marked complete', 'completed successfully', 'i\'ve marked', 'task marked'];
    
    // Error patterns
    const errorPatterns = ['error', 'failed', 'unable to', 'could not', 'couldn\'t', 'sorry, i'];

    // Check for errors first
    for (const pattern of errorPatterns) {
      if (lowerResponse.includes(pattern)) {
        return { operation: 'error', success: false };
      }
    }

    // Check for success operations
    for (const pattern of createdPatterns) {
      if (lowerResponse.includes(pattern)) {
        return { operation: 'created', success: true };
      }
    }

    for (const pattern of deletedPatterns) {
      if (lowerResponse.includes(pattern)) {
        return { operation: 'deleted', success: true };
      }
    }

    for (const pattern of updatedPatterns) {
      if (lowerResponse.includes(pattern)) {
        return { operation: 'updated', success: true };
      }
    }

    for (const pattern of completedPatterns) {
      if (lowerResponse.includes(pattern)) {
        return { operation: 'completed', success: true };
      }
    }

    return null;
  };

  // Dispatch custom event to notify dashboard of task changes
  const dispatchTaskChangeEvent = () => {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new Event('tasks-changed'));
    }
  };

  // Show toast notification based on task operation
  const showTaskToast = (operation: string, success: boolean) => {
    if (!success) {
      showToast('Failed to perform task operation. Please try again.', 'error');
      return;
    }

    switch (operation) {
      case 'created':
        showToast('Task created successfully', 'success');
        break;
      case 'deleted':
        showToast('Task deleted successfully', 'success');
        break;
      case 'updated':
        showToast('Task updated successfully', 'success');
        break;
      case 'completed':
        showToast('Task marked as complete', 'success');
        break;
      default:
        break;
    }
  };

  // Auto-scroll to bottom when new messages arrive
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  // Load conversation history when chatbot opens
  useEffect(() => {
    if (isOpen && state.isAuthenticated && messages.length === 0) {
      loadConversationHistory();
    }
  }, [isOpen, state.isAuthenticated]);

  const loadConversationHistory = async () => {
    try {
      const token = localStorage.getItem('access_token');
      const userId = state.user?.id;

      if (!token || !userId) return;

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat/history`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.messages && data.messages.length > 0) {
          const formattedMessages: Message[] = data.messages.map((msg: any) => ({
            id: msg.id,
            role: msg.role as 'user' | 'assistant',
            content: msg.content,
            timestamp: msg.created_at,
          }));
          setMessages(formattedMessages);
          setConversationId(data.conversation.id);
        } else if (data.conversations && data.conversations.length > 0) {
          // Load most recent conversation
          const latestConv = data.conversations[0];
          await loadSpecificConversation(latestConv.id);
        }
      }
    } catch (error) {
      console.error('Failed to load conversation history:', error);
    }
  };

  const loadSpecificConversation = async (convId: string) => {
    try {
      const token = localStorage.getItem('access_token');
      const userId = state.user?.id;

      if (!token || !userId) return;

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat/history?conversation_id=${convId}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
        },
      });

      if (response.ok) {
        const data = await response.json();
        if (data.success && data.messages) {
          const formattedMessages: Message[] = data.messages.map((msg: any) => ({
            id: msg.id,
            role: msg.role as 'user' | 'assistant',
            content: msg.content,
            timestamp: msg.created_at,
          }));
          setMessages(formattedMessages);
          setConversationId(data.conversation.id);
        }
      }
    } catch (error) {
      console.error('Failed to load conversation:', error);
    }
  };

  const sendMessage = async (content: string) => {
    if (!state.isAuthenticated || !state.user?.id) {
      console.error('User not authenticated');
      return;
    }

    const userMessage: Message = {
      id: `temp-${Date.now()}`,
      role: 'user',
      content,
      timestamp: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setIsLoading(true);

    try {
      const token = localStorage.getItem('access_token');
      const userId = state.user.id;

      if (!token) {
        throw new Error('No authentication token found');
      }

      const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/${userId}/chat`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`,
        },
        body: JSON.stringify({ message: content }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Failed to send message');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: `temp-${Date.now()}-2`,
        role: 'assistant',
        content: data.response,
        timestamp: data.timestamp,
      };

      setMessages((prev) => [...prev, assistantMessage]);

      // Parse response to detect task operations and show toast
      const taskOperation = parseTaskOperation(data.response);
      if (taskOperation) {
        showTaskToast(taskOperation.operation, taskOperation.success);
        if (taskOperation.success) {
          dispatchTaskChangeEvent();
        }
      }

      if (data.conversation_id && !conversationId) {
        setConversationId(data.conversation_id);
      }
    } catch (error) {
      console.error('Failed to send message:', error);

      const errorMessage: Message = {
        id: `temp-${Date.now()}-error`,
        role: 'assistant',
        content: 'Sorry, I encountered an error. Please try again.',
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, errorMessage]);
      
      // Show error toast for network/API failures
      showToast('Failed to send message. Please check your connection and try again.', 'error');
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChatbot = () => {
    setIsOpen(!isOpen);
  };

  if (!state.isAuthenticated) {
    return null; // Only show for authenticated users
  }

  return (
    <>
      {/* Floating Action Button */}
      {!isOpen && (
        <button
          onClick={toggleChatbot}
          className="fixed bottom-6 right-6 z-50 flex items-center justify-center w-16 h-16 rounded-full bg-gradient-to-r from-indigo-600 to-purple-600 text-white shadow-lg hover:shadow-xl transform hover:scale-110 transition-all duration-300"
          aria-label="Open chatbot"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            className="h-8 w-8"
            viewBox="0 0 20 20"
            fill="currentColor"
          >
            <path
              fillRule="evenodd"
              d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
              clipRule="evenodd"
            />
          </svg>
        </button>
      )}

      {/* Chatbot Popup */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-full max-w-md">
          <div className="bg-white dark:bg-gray-800 rounded-2xl shadow-2xl overflow-hidden border border-gray-200 dark:border-gray-700 flex flex-col" style={{ height: '600px' }}>
            {/* Header */}
            <div className="bg-gradient-to-r from-indigo-600 to-purple-600 px-6 py-4 flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-white/20 flex items-center justify-center">
                  <svg
                    xmlns="http://www.w3.org/2000/svg"
                    className="h-6 w-6 text-white"
                    viewBox="0 0 20 20"
                    fill="currentColor"
                  >
                    <path
                      fillRule="evenodd"
                      d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                      clipRule="evenodd"
                    />
                  </svg>
                </div>
                <div>
                  <h3 className="text-white font-bold text-lg">AI Assistant</h3>
                  <p className="text-indigo-100 text-xs">Manage your tasks with natural language</p>
                </div>
              </div>
              <button
                onClick={toggleChatbot}
                className="text-white/80 hover:text-white transition-colors"
                aria-label="Close chatbot"
              >
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-6 w-6"
                  fill="none"
                  viewBox="0 0 24 24"
                  stroke="currentColor"
                >
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900">
              {messages.length === 0 ? (
                <div className="flex flex-col items-center justify-center h-full text-center px-4">
                  <div className="w-16 h-16 rounded-full bg-indigo-100 dark:bg-indigo-900/30 flex items-center justify-center mb-4">
                    <svg
                      xmlns="http://www.w3.org/2000/svg"
                      className="h-8 w-8 text-indigo-600 dark:text-indigo-400"
                      viewBox="0 0 20 20"
                      fill="currentColor"
                    >
                      <path
                        fillRule="evenodd"
                        d="M18 10c0 3.866-3.582 7-8 7a8.841 8.841 0 01-4.083-.98L2 17l1.338-3.123C2.493 12.767 2 11.434 2 10c0-3.866 3.582-7 8-7s8 3.134 8 7zM7 9H5v2h2V9zm8 0h-2v2h2V9zM9 9h2v2H9V9z"
                        clipRule="evenodd"
                      />
                    </svg>
                  </div>
                  <h4 className="text-gray-900 dark:text-gray-100 font-semibold mb-2">Welcome to AI Chat!</h4>
                  <p className="text-gray-600 dark:text-gray-400 text-sm mb-4">
                    I can help you manage your tasks. Try saying:
                  </p>
                  <div className="space-y-2 text-sm">
                    <div className="bg-white dark:bg-gray-800 px-3 py-2 rounded-lg text-gray-700 dark:text-gray-300">
                      &quot;Add buy groceries to my list&quot;
                    </div>
                    <div className="bg-white dark:bg-gray-800 px-3 py-2 rounded-lg text-gray-700 dark:text-gray-300">
                      &quot;Show me all my tasks&quot;
                    </div>
                    <div className="bg-white dark:bg-gray-800 px-3 py-2 rounded-lg text-gray-700 dark:text-gray-300">
                      &quot;Mark the first task as complete&quot;
                    </div>
                  </div>
                </div>
              ) : (
                <>
                  {messages.map((msg) => (
                    <ChatMessage
                      key={msg.id}
                      role={msg.role}
                      content={msg.content}
                      timestamp={msg.timestamp}
                    />
                  ))}
                  {isLoading && (
                    <div className="flex justify-start mb-4">
                      <div className="bg-white dark:bg-gray-800 rounded-2xl px-4 py-3 shadow-md border border-gray-200 dark:border-gray-700">
                        <div className="flex gap-1">
                          <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                          <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                          <div className="w-2 h-2 bg-indigo-600 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                        </div>
                      </div>
                    </div>
                  )}
                  <div ref={messagesEndRef} />
                </>
              )}
            </div>

            {/* Input */}
            <ChatInput
              onSend={sendMessage}
              disabled={isLoading}
              placeholder="Type your message..."
            />
          </div>
        </div>
      )}
    </>
  );
}
