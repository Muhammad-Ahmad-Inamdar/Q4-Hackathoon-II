'use client';

import React from 'react';

// Better Auth mein 'ClientProvider' ki zaroorat nahi hoti.
// Aap sirf children return kar sakte hain ya agar koi aur context (jaise Theme) 
// add karna ho toh yahan kar sakte hain.

export function AuthProvider({ children }: { children: React.ReactNode }) {
  return (
    <>
      {children}
    </>
  );
}