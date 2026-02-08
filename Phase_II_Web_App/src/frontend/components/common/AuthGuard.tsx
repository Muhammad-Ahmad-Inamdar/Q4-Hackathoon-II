'use client';

import React from 'react';
import { useAuth } from '../../context/AuthContext';

interface AuthGuardProps {
  children: React.ReactNode;
  fallback?: React.ReactNode;
  authenticatedFallback?: React.ReactNode;
}

const AuthGuard: React.FC<AuthGuardProps> = ({
  children,
  fallback = null,
  authenticatedFallback = null
}) => {
  const { state } = useAuth();

  // While loading, show nothing or a loading indicator
  if (state.isLoading) {
    return <div>Loading...</div>;
  }

  // If authenticated and authenticatedFallback is provided, show that instead
  if (state.isAuthenticated && authenticatedFallback) {
    return authenticatedFallback;
  }

  // If not authenticated and fallback is provided, show fallback
  if (!state.isAuthenticated && fallback) {
    return fallback;
  }

  // If authenticated and no authenticatedFallback, show children
  // If not authenticated and no fallback, show children
  return <>{children}</>;
};

export default AuthGuard;