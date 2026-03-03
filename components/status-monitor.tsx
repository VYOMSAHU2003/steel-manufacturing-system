"use client"

import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { 
  Wifi, 
  WifiOff, 
  Server, 
  Database, 
  Activity, 
  CheckCircle, 
  AlertTriangle,
  XCircle,
  Zap
} from 'lucide-react'
import { useRealTimeData } from '@/hooks/use-realtime-data'

export function StatusMonitor() {
  const { isConnected, lastUpdate } = useRealTimeData()
  
  const services = [
    {
      name: 'Frontend',
      status: 'online',
      icon: Server,
      description: 'Next.js Application',
      lastCheck: new Date()
    },
    {
      name: 'Backend API',
      status: isConnected ? 'online' : 'offline',
      icon: Database,
      description: 'Streamlit Server',
      lastCheck: lastUpdate
    },
    {
      name: 'Real-time Data',
      status: isConnected ? 'online' : 'degraded',
      icon: Activity,
      description: 'Live Updates',
      lastCheck: lastUpdate
    }
  ]

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'online':
        return <CheckCircle className="w-4 h-4 text-green-500" />
      case 'degraded':
        return <AlertTriangle className="w-4 h-4 text-yellow-500" />
      case 'offline':
        return <XCircle className="w-4 h-4 text-red-500" />
      default:
        return <AlertTriangle className="w-4 h-4 text-gray-500" />
    }
  }

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'online':
        return <Badge className="bg-green-100 text-green-800 border-green-200">Online</Badge>
      case 'degraded':
        return <Badge className="bg-yellow-100 text-yellow-800 border-yellow-200">Degraded</Badge>
      case 'offline':
        return <Badge variant="destructive">Offline</Badge>
      default:
        return <Badge variant="outline">Unknown</Badge>
    }
  }

  const formatTime = (date: Date | null) => {
    if (!date) return 'Never'
    return date.toLocaleTimeString()
  }

  return (
    <Card className="w-full">
      <CardHeader>
        <CardTitle className="flex items-center gap-2">
          <Activity className="w-5 h-5" />
          System Status
        </CardTitle>
        <CardDescription>
          Monitor the health of all application services
        </CardDescription>
      </CardHeader>
      <CardContent className="space-y-4">
        {services.map((service, index) => (
          <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
            <div className="flex items-center gap-3">
              <service.icon className="w-5 h-5 text-muted-foreground" />
              <div>
                <div className="flex items-center gap-2">
                  {getStatusIcon(service.status)}
                  <span className="font-medium">{service.name}</span>
                </div>
                <p className="text-xs text-muted-foreground">{service.description}</p>
              </div>
            </div>
            <div className="text-right">
              {getStatusBadge(service.status)}
              <p className="text-xs text-muted-foreground mt-1">
                {formatTime(service.lastCheck)}
              </p>
            </div>
          </div>
        ))}
        
        <div className="flex items-center justify-between pt-4 border-t">
          <div className="flex items-center gap-2">
            {isConnected ? (
              <Wifi className="w-4 h-4 text-green-500" />
            ) : (
              <WifiOff className="w-4 h-4 text-red-500" />
            )}
            <span className="text-sm">
              {isConnected ? 'Connected to backend' : 'Running in offline mode'}
            </span>
          </div>
          <div className="flex items-center gap-2">
            <Zap className="w-3 h-3 text-blue-500 animate-pulse" />
            <span className="text-xs text-muted-foreground">
              Last update: {formatTime(lastUpdate)}
            </span>
          </div>
        </div>
      </CardContent>
    </Card>
  )
}