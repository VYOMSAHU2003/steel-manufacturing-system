"use client"

import { useState } from 'react'
import { useAuth } from '@/components/auth-provider'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Label } from '@/components/ui/label'
import { Alert, AlertDescription } from '@/components/ui/alert'
import { Spinner } from '@/components/ui/spinner'
import { Factory, Loader2, AlertCircle, Shield, Users, Settings, Eye } from 'lucide-react'

const demoAccounts = [
  { username: 'admin', password: 'admin123', role: 'Administrator', icon: Shield },
  { username: 'manager', password: 'manager123', role: 'Production Manager', icon: Users },
  { username: 'operator', password: 'operator123', role: 'System Operator', icon: Settings },
  { username: 'quality', password: 'quality123', role: 'Quality Inspector', icon: Eye },
]

export function LoginPage() {
  const { login, isLoading } = useAuth()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    
    if (!username.trim() || !password.trim()) {
      setError('Please enter both username and password')
      return
    }

    const success = await login(username.trim(), password)
    if (!success) {
      setError('Invalid username or password')
    }
  }

  const handleDemoLogin = (demoUsername: string, demoPassword: string) => {
    setUsername(demoUsername)
    setPassword(demoPassword)
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-gray-900 p-4">
      <div className="w-full max-w-6xl grid lg:grid-cols-2 gap-8 items-center">
        
        {/* Left Side - Branding */}
        <div className="hidden lg:flex flex-col items-center justify-center space-y-8 p-8">
          <div className="text-center space-y-4">
            <div className="flex items-center justify-center space-x-4 mb-8">
              <div className="relative">
                <Factory className="h-16 w-16 text-primary animate-pulse" />
                <div className="absolute -top-2 -right-2 h-6 w-6 bg-blue-500 rounded-full animate-bounce" />
              </div>
              <div>
                <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  BSP Steel
                </h1>
                <p className="text-xl text-muted-foreground font-medium">Manufacturing System</p>
              </div>
            </div>
            
            <div className="max-w-md space-y-4 text-center">
              <h2 className="text-2xl font-semibold text-foreground">
                Welcome to the Future of Steel Manufacturing
              </h2>
              <p className="text-muted-foreground leading-relaxed">
                Manage production, inventory, quality assurance, and logistics with our 
                comprehensive manufacturing management system.
              </p>
            </div>

            {/* Feature Highlights */}
            <div className="grid grid-cols-2 gap-4 mt-8 max-w-md">
              {[
                { icon: Factory, label: 'Production Control' },
                { icon: Shield, label: 'Quality Assurance' },
                { icon: Users, label: 'Team Management' },
                { icon: Settings, label: 'System Integration' },
              ].map((feature, index) => (
                <div key={index} className="flex flex-col items-center space-y-2 p-3 bg-white/50 dark:bg-gray-800/50 rounded-lg">
                  <feature.icon className="h-6 w-6 text-primary" />
                  <span className="text-sm font-medium text-center">{feature.label}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        {/* Right Side - Login Form */}
        <div className="w-full max-w-md mx-auto">
          <Card className="border-2 shadow-2xl bg-white/95 dark:bg-gray-900/95 backdrop-blur">
            <CardHeader className="text-center pb-2">
              <div className="flex justify-center lg:hidden mb-4">
                <Factory className="h-12 w-12 text-primary" />
              </div>
              <CardTitle className="text-2xl font-bold">Sign In</CardTitle>
              <CardDescription>
                Enter your credentials to access the system
              </CardDescription>
            </CardHeader>
            
            <CardContent className="space-y-6">
              {error && (
                <Alert variant="destructive">
                  <AlertCircle className="h-4 w-4" />
                  <AlertDescription>{error}</AlertDescription>
                </Alert>
              )}
              
              <form onSubmit={handleSubmit} className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="username">Username</Label>
                  <Input
                    id="username"
                    type="text"
                    placeholder="Enter username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    className="bg-background"
                    disabled={isLoading}
                  />
                </div>
                
                <div className="space-y-2">
                  <Label htmlFor="password">Password</Label>
                  <div className="relative">
                    <Input
                      id="password"
                      type={showPassword ? "text" : "password"}
                      placeholder="Enter password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                      className="bg-background pr-10"
                      disabled={isLoading}
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="sm"
                      className="absolute right-0 top-0 h-full px-3 py-2 hover:bg-transparent"
                      onClick={() => setShowPassword(!showPassword)}
                    >
                      <Eye className={`h-4 w-4 ${showPassword ? 'text-primary' : 'text-muted-foreground'}`} />
                    </Button>
                  </div>
                </div>
                
                <Button 
                  type="submit" 
                  className="w-full bg-gradient-to-r from-blue-600 to-purple-600 hover:from-blue-700 hover:to-purple-700" 
                  disabled={isLoading}
                >
                  {isLoading ? (
                    <>
                      <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                      Signing In...
                    </>
                  ) : (
                    'Sign In'
                  )}
                </Button>
              </form>

              <div className="relative">
                <div className="absolute inset-0 flex items-center">
                  <span className="w-full border-t" />
                </div>
                <div className="relative flex justify-center text-xs uppercase">
                  <span className="bg-background px-2 text-muted-foreground">Demo Accounts</span>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-2">
                {demoAccounts.map((account, index) => (
                  <Button
                    key={index}
                    variant="outline" 
                    size="sm"
                    className="flex flex-col h-auto p-3 text-xs"
                    onClick={() => handleDemoLogin(account.username, account.password)}
                    disabled={isLoading}
                  >
                    <account.icon className="h-4 w-4 mb-1" />
                    <span className="font-medium">{account.username}</span>
                    <span className="text-muted-foreground">{account.role}</span>
                  </Button>
                ))}
              </div>

              <div className="text-xs text-center text-muted-foreground">
                Click any demo account above to auto-fill credentials
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}