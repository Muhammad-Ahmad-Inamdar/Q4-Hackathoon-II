'use client';

import React, { createContext, useContext, useState, useEffect } from 'react';
import { ThemeState, ThemeMode } from '../lib/types';

interface ThemeContextType {
  state: ThemeState;
  toggleTheme: () => void;
  setTheme: (mode: ThemeMode) => void;
}

const getSystemTheme = (): ThemeMode => {
  if (typeof window !== 'undefined') {
    return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  return 'light';
};

const getStoredTheme = (): ThemeMode | null => {
  if (typeof window !== 'undefined') {
    const stored = localStorage.getItem('theme');
    if (stored === 'light' || stored === 'dark') {
      return stored;
    }
  }
  return null;
};

const initialThemeState: ThemeState = {
  current: getStoredTheme() || getSystemTheme(),
  systemPreference: getSystemTheme(),
  persistedPreference: getStoredTheme(),
};

const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

export const ThemeProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [state, setState] = useState<ThemeState>(initialThemeState);

  useEffect(() => {
    // Initialize theme
    const storedTheme = getStoredTheme();
    const systemTheme = getSystemTheme();

    const initialTheme = storedTheme || systemTheme;

    setState(prev => ({
      ...prev,
      current: initialTheme,
      systemPreference: systemTheme,
      persistedPreference: storedTheme,
    }));

    // Apply theme to document
    document.documentElement.setAttribute('data-theme', initialTheme);
  }, []);

  const setTheme = (mode: ThemeMode) => {
    setState(prev => ({
      ...prev,
      current: mode,
      persistedPreference: mode,
    }));

    // Update localStorage
    localStorage.setItem('theme', mode);

    // Update document attribute for CSS
    document.documentElement.setAttribute('data-theme', mode);
  };

  const toggleTheme = () => {
    const newTheme = state.current === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
  };

  // Listen for system theme changes
  useEffect(() => {
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');

    const handleChange = () => {
      const newSystemTheme = getSystemTheme();
      setState(prev => ({
        ...prev,
        systemPreference: newSystemTheme,
      }));

      // If no persisted preference, follow system
      if (!prev.persistedPreference) {
        setTheme(newSystemTheme);
      }
    };

    mediaQuery.addEventListener('change', handleChange);

    return () => {
      mediaQuery.removeEventListener('change', handleChange);
    };
  }, []);

  return (
    <ThemeContext.Provider value={{ state, toggleTheme, setTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (context === undefined) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};