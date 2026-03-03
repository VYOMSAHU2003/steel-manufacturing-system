"use client"

import { Navbar } from '@/components/navbar'
import { AuthGuard } from '@/components/auth-guard'
import { useAuth } from '@/components/auth-provider'
import { cn } from '@/lib/utils'

interface DashboardLayoutProps {
  children: React.ReactNode
  className?: string
}

function DashboardContent({ children, className }: DashboardLayoutProps) {
  const { user, logout } = useAuth()
  
  return (
    <div className="h-screen flex bg-background">
      <Navbar user={user} onLogout={logout} />
      
      {/* Main content area */}
      <div className="flex-1 lg:pl-72">
        <main className={cn(
          "h-full overflow-auto",
          "px-4 py-6 lg:px-8 lg:py-8",
          className
        )}>
          {children}
        </main>
      </div>
    </div>
  )
}

export function DashboardLayout({ children, className }: DashboardLayoutProps) {
  return (
    <AuthGuard>
      <DashboardContent className={className}>
        {children}
      </DashboardContent>
    </AuthGuard>
  )
}