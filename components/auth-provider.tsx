"use client"

import React, { createContext, useContext, useEffect, useState } from 'react'

interface User {
  id: string
  username: string
  email: string
  fullName: string
  role: 'admin' | 'manager' | 'operator' | 'quality' | 'logistics'
  isActive: boolean
}

interface AuthContextType {
  user: User | null
  login: (username: string, password: string) => Promise<boolean>
  logout: () => void
  isLoading: boolean
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

const defaultUsers = [
  {
    id: '1',
    username: 'admin',
    password: 'admin123',
    email: 'admin@bspsteel.com',
    fullName: 'Admin User',
    role: 'admin' as const,
    isActive: true
  },
  {
    id: '2', 
    username: 'manager',
    password: 'manager123',
    email: 'manager@bspsteel.com',
    fullName: 'Production Manager',
    role: 'manager' as const,
    isActive: true
  },
  {
    id: '3',
    username: 'operator',
    password: 'operator123',
    email: 'operator@bspsteel.com',
    fullName: 'System Operator',
    role: 'operator' as const,
    isActive: true
  },
  {
    id: '4',
    username: 'quality',
    password: 'quality123',
    email: 'quality@bspsteel.com',
    fullName: 'Quality Inspector',
    role: 'quality' as const,
    isActive: true
  }
]

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    // Check for stored user on mount
    const storedUser = localStorage.getItem('bsp_user')
    if (storedUser) {
      try {
        setUser(JSON.parse(storedUser))
      } catch (error) {
        console.error('Failed to parse stored user:', error)
        localStorage.removeItem('bsp_user')
      }
    }
    setIsLoading(false)
  }, [])

  const login = async (username: string, password: string): Promise<boolean> => {
    setIsLoading(true)
    
    // Simulate API call delay
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const foundUser = defaultUsers.find(
      u => u.username === username && u.password === password
    )

    if (foundUser) {
      const { password: _, ...userWithoutPassword } = foundUser
      setUser(userWithoutPassword)
      localStorage.setItem('bsp_user', JSON.stringify(userWithoutPassword))
      setIsLoading(false)
      return true
    }
    
    setIsLoading(false)
    return false
  }

  const logout = () => {
    setUser(null)
    localStorage.removeItem('bsp_user')
  }

  const value: AuthContextType = {
    user,
    login,
    logout,
    isLoading,
    isAuthenticated: !!user
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}