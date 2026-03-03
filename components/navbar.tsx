"use client"

import { useState } from 'react'
import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { Button } from '@/components/ui/button'
import { Badge } from '@/components/ui/badge'
import { ThemeToggle } from '@/components/theme-provider'
import {
  Store,
  Factory,
  Package,
  ShieldCheck,
  Truck,
  Users,
  Settings,
  Menu,
  X,
  LogOut,
  Bell,
  User,
  Crown,
  Briefcase,
  Wrench
} from 'lucide-react'
import { Sheet, SheetContent, SheetTrigger } from '@/components/ui/sheet'
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar'
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu'

const navigation = [
  {
    name: 'Dashboard',
    href: '/',
    icon: Store,
    description: 'Overview & Analytics'
  },
  {
    name: 'Raw Materials',
    href: '/raw-materials',
    icon: Package,
    description: 'Material Inventory'
  },
  {
    name: 'Production',
    href: '/production',
    icon: Factory,
    description: 'Production Planning'
  },
  {
    name: 'Inventory',
    href: '/inventory',
    icon: Store,
    description: 'Stock Management'
  },
  {
    name: 'Quality',
    href: '/quality',
    icon: ShieldCheck,
    description: 'Quality Assurance'
  },
  {
    name: 'Logistics',
    href: '/logistics',
    icon: Truck,
    description: 'Shipping & Delivery'
  }
]

interface NavbarProps {
  user?: {
    id: string
    username: string
    role: string
    name: string
    email: string
  }
  onLogout?: () => void
}

export function Navbar({ user, onLogout }: NavbarProps) {
  const pathname = usePathname()
  const [isOpen, setIsOpen] = useState(false)

  if (!user) return null

  const getRoleIcon = (role: string) => {
    switch (role) {
      case 'admin': return Crown
      case 'manager': return Briefcase
      case 'operator': return Wrench
      case 'quality': return ShieldCheck
      case 'logistics': return Truck
      default: return User
    }
  }

  const RoleIcon = getRoleIcon(user.role)

  return (
    <>
      {/* Desktop Navbar */}
      <nav className="hidden lg:flex lg:flex-col lg:w-72 lg:fixed lg:inset-y-0 lg:bg-card lg:border-r lg:border-border">
        <div className="flex flex-col flex-1">
          {/* Logo Section */}
          <div className="flex items-center px-6 py-4 border-b border-border">
            <div className="flex items-center space-x-3">
              <div className="relative">
                <Factory className="h-8 w-8 text-primary" />
                <div className="absolute -top-1 -right-1 h-3 w-3 bg-blue-500 rounded-full animate-pulse" />
              </div>
              <div>
                <h1 className="text-lg font-bold text-foreground">BSP Steel</h1>
                <p className="text-xs text-muted-foreground">Manufacturing System v2.0</p>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <div className="flex-1 px-3 py-4 space-y-1">
            {navigation.map((item) => {
              const isActive = pathname === item.href
              const Icon = item.icon
              
              return (
                <Link
                  key={item.name}
                  href={item.href}
                  className={cn(
                    'group flex items-center px-3 py-3 rounded-lg text-sm font-medium transition-all',
                    'hover:bg-accent hover:scale-[1.02] hover:shadow-sm',
                    isActive
                      ? 'bg-primary text-primary-foreground shadow-lg'
                      : 'text-foreground hover:text-accent-foreground'
                  )}
                >
                  <Icon
                    className={cn(
                      'mr-3 h-5 w-5 transition-transform group-hover:scale-110',
                      isActive ? 'text-primary-foreground' : 'text-muted-foreground group-hover:text-accent-foreground'
                    )}
                  />
                  <div className="flex flex-col">
                    <span>{item.name}</span>
                    <span className="text-xs opacity-75">{item.description}</span>
                  </div>
                  {isActive && (
                    <div className="ml-auto h-2 w-2 bg-primary-foreground rounded-full animate-pulse" />
                  )}
                </Link>
              )
            })}
          </div>

          {/* User Profile Section */}
          <div className="px-3 py-4 border-t border-border">
            <DropdownMenu>
              <DropdownMenuTrigger asChild>
                <Button variant="ghost" className="w-full h-auto px-3 py-3 justify-start">
                  <Avatar className="h-8 w-8">
                    <AvatarFallback className="bg-primary text-primary-foreground">
                      {user.name.split(' ').map((n: string) => n[0]).join('')}
                    </AvatarFallback>
                  </Avatar>
                  <div className="ml-3 flex flex-col items-start">
                    <span className="text-sm font-medium">{user.name}</span>
                    <div className="flex items-center space-x-1">
                      <RoleIcon className="h-3 w-3" />
                      <span className="text-xs text-muted-foreground capitalize">{user.role}</span>
                    </div>
                  </div>
                </Button>
              </DropdownMenuTrigger>
              <DropdownMenuContent className="w-56" align="end" forceMount>
                <DropdownMenuLabel className="font-normal">
                  <div className="flex flex-col space-y-1">
                    <p className="text-sm font-medium leading-none">{user.name}</p>
                    <p className="text-xs leading-none text-muted-foreground">{user.email}</p>
                  </div>
                </DropdownMenuLabel>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="cursor-pointer">
                  <User className="mr-2 h-4 w-4" />
                  <span>Profile</span>
                </DropdownMenuItem>
                <DropdownMenuItem className="cursor-pointer">
                  <Settings className="mr-2 h-4 w-4" />
                  <span>Settings</span>
                </DropdownMenuItem>
                <DropdownMenuSeparator />
                <DropdownMenuItem className="cursor-pointer text-red-600" onClick={onLogout}>
                  <LogOut className="mr-2 h-4 w-4" />
                  <span>Log out</span>
                </DropdownMenuItem>
              </DropdownMenuContent>
            </DropdownMenu>
          </div>
        </div>
      </nav>

      {/* Mobile Header */}
      <div className="lg:hidden flex items-center justify-between px-4 py-3 border-b border-border bg-card">
        <div className="flex items-center space-x-3">
          <Factory className="h-6 w-6 text-primary" />
          <div>
            <h1 className="text-sm font-bold text-foreground">BSP Steel</h1>
            <p className="text-xs text-muted-foreground">Manufacturing</p>
          </div>
        </div>

        <div className="flex items-center space-x-2">
          <ThemeToggle />
          <Button variant="ghost" size="sm" className="relative">
            <Bell className="h-5 w-5" />
            <Badge className="absolute -top-1 -right-1 h-4 w-4 p-0 text-xs">3</Badge>
          </Button>
          
          <Sheet open={isOpen} onOpenChange={setIsOpen}>
            <SheetTrigger asChild>
              <Button variant="ghost" size="sm">
                <Menu className="h-5 w-5" />
              </Button>
            </SheetTrigger>
            <SheetContent side="left" className="w-72 p-0">
              <div className="flex flex-col h-full">
                {/* Mobile Logo */}
                <div className="flex items-center px-6 py-4 border-b border-border">
                  <div className="flex items-center space-x-3">
                    <Factory className="h-8 w-8 text-primary" />
                    <div>
                      <h1 className="text-lg font-bold text-foreground">BSP Steel</h1>
                      <p className="text-xs text-muted-foreground">Manufacturing System</p>
                    </div>
                  </div>
                </div>

                {/* Mobile Navigation */}
                <div className="flex-1 px-3 py-4 space-y-1">
                  {navigation.map((item) => {
                    const isActive = pathname === item.href
                    const Icon = item.icon
                    
                    return (
                      <Link
                        key={item.name}
                        href={item.href}
                        onClick={() => setIsOpen(false)}
                        className={cn(
                          'group flex items-center px-3 py-3 rounded-lg text-sm font-medium transition-all',
                          'hover:bg-accent',
                          isActive
                            ? 'bg-primary text-primary-foreground'
                            : 'text-foreground hover:text-accent-foreground'
                        )}
                      >
                        <Icon className="mr-3 h-5 w-5" />
                        <div className="flex flex-col">
                          <span>{item.name}</span>
                          <span className="text-xs opacity-75">{item.description}</span>
                        </div>
                      </Link>
                    )
                  })}
                </div>

                {/* Mobile User Section */}
                <div className="px-3 py-4 border-t border-border">
                  <div className="flex items-center space-x-3">
                    <Avatar className="h-8 w-8">
                      <AvatarFallback className="bg-primary text-primary-foreground">
                        {user.name.split(' ').map((n: string) => n[0]).join('')}
                      </AvatarFallback>
                    </Avatar>
                    <div className="flex-1">
                      <p className="text-sm font-medium">{user.name}</p>
                      <div className="flex items-center space-x-1">
                        <RoleIcon className="h-3 w-3" />
                        <p className="text-xs text-muted-foreground capitalize">{user.role}</p>
                      </div>
                    </div>
                    <Button variant="ghost" size="sm" onClick={onLogout}>
                      <LogOut className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            </SheetContent>
          </Sheet>
        </div>
      </div>
    </>
  )
}