'use client';

import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { AuthState } from '../lib/types';
import { getUserInfo, logout as authLogout } from '../lib/auth';

interface AuthContextType {
  state: AuthState;
  login: (userData: any) => void;
  logout: () => void;
  checkAuthStatus: () => void;
}

const initialState: AuthState = {
  isAuthenticated: false,
  user: undefined,
  isLoading: true,
  error: undefined,
};

type AuthAction =
  | { type: 'LOGIN_START' }
  | { type: 'LOGIN_SUCCESS'; payload: { id: string; email: string } }
  | { type: 'LOGIN_FAILURE'; payload: string }
  | { type: 'LOGOUT' }
  | { type: 'CHECK_AUTH_START' }
  | { type: 'CHECK_AUTH_SUCCESS'; payload: { id: string; email: string } }
  | { type: 'CHECK_AUTH_FAILURE' }
  | { type: 'SET_LOADING'; payload: boolean };

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'LOGIN_START':
      return { ...state, isLoading: true, error: undefined };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: { id: action.payload.id, email: action.payload.email },
        isLoading: false,
        error: undefined,
      };
    case 'LOGIN_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        user: undefined,
        isLoading: false,
        error: action.payload,
      };
    case 'LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: undefined,
        isLoading: false,
      };
    case 'CHECK_AUTH_START':
      return { ...state, isLoading: true };
    case 'CHECK_AUTH_SUCCESS':
      return {
        ...state,
        isAuthenticated: true,
        user: { id: action.payload.id, email: action.payload.email },
        isLoading: false,
      };
    case 'CHECK_AUTH_FAILURE':
      return {
        ...state,
        isAuthenticated: false,
        user: undefined,
        isLoading: false,
      };
    case 'SET_LOADING':
      return { ...state, isLoading: action.payload };
    default:
      return state;
  }
};

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  const checkAuthStatus = async () => {
    dispatch({ type: 'CHECK_AUTH_START' });
    try {
      const userInfo = await getUserInfo();
      if (userInfo) {
        dispatch({
          type: 'CHECK_AUTH_SUCCESS',
          payload: { id: userInfo.id, email: userInfo.email },
        });
      } else {
        dispatch({ type: 'CHECK_AUTH_FAILURE' });
      }
    } catch (error) {
      dispatch({ type: 'CHECK_AUTH_FAILURE' });
    }
  };

  const login = (userData: any) => {
    dispatch({
      type: 'LOGIN_SUCCESS',
      payload: { id: userData.id, email: userData.email },
    });
  };

  const logout = async () => {
    try {
      await authLogout();
      dispatch({ type: 'LOGOUT' });
    } catch (error) {
      dispatch({ type: 'LOGOUT' });
    }
  };

  useEffect(() => {
    checkAuthStatus();

    // Listen for unauthorized events from API requests
    const handleUnauthorized = () => {
      dispatch({ type: 'LOGOUT' });
    };

    window.addEventListener('unauthorized', handleUnauthorized);

    return () => {
      window.removeEventListener('unauthorized', handleUnauthorized);
    };
  }, []);

  return (
    <AuthContext.Provider value={{ state, login, logout, checkAuthStatus }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};