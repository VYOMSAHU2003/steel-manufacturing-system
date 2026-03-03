"use client"

import { useAuth } from '@/components/auth-provider'
import { LoginPage } from '@/components/login-page'
import { Spinner } from '@/components/ui/spinner'

export function AuthGuard({ children }: { children: React.ReactNode }) {
  const { user, isLoading, isAuthenticated } = useAuth()

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center space-y-4">
          <Spinner className="mx-auto h-8 w-8" />
          <p className="text-muted-foreground">Loading BSP Steel System...</p>
        </div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return <LoginPage />
  }

  return <>{children}</>
}