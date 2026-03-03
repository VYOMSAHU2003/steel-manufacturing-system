"use client"

import { DashboardLayout } from '@/components/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Progress } from '@/components/ui/progress'
import { useData } from '@/components/data-provider'
import { useRealTimeData, useProductionMetrics, useAlertSystem } from '@/hooks/use-realtime-data'
import {
  Factory,
  Package,
  TrendingUp,
  AlertTriangle,
  CheckCircle,
  Clock,
  Users,
  DollarSign,
  BarChart3,
  Activity,
  Wifi,
  WifiOff,
  Zap
} from 'lucide-react'
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  AreaChart,
  Area
} from 'recharts'
import Link from 'next/link'

export default function DashboardPage() {
  const { dashboardMetrics, isLoading, refreshAll } = useData()
  const { isConnected, lastUpdate } = useRealTimeData()
  const productionMetrics = useProductionMetrics()
  const { alerts } = useAlertSystem()

  const formatTime = (date: Date | null) => {
    if (!date) return 'Never'
    return date.toLocaleTimeString()
  }

  // Sample data for charts
  const productionData = [
    { time: '00:00', output: 2200, target: 2400 },
    { time: '04:00', output: 2450, target: 2400 },
    { time: '08:00', output: 2800, target: 2400 },
    { time: '12:00', output: 3100, target: 2400 },
    { time: '16:00', output: 2900, target: 2400 },
    { time: '20:00', output: Math.round(productionMetrics.output), target: 2400 }
  ]

  const qualityData = [
    { time: 'Week 1', quality: 94.2, defects: 8 },
    { time: 'Week 2', quality: 95.8, defects: 6 },
    { time: 'Week 3', quality: 93.1, defects: 11 },
    { time: 'Week 4', quality: Math.round(productionMetrics.quality), defects: 4 }
  ]

  const inventoryData = [
    { material: 'Iron Ore', level: 78, status: 'Good' },
    { material: 'Coal', level: 45, status: 'Low' },
    { material: 'Limestone', level: 92, status: 'Good' },
    { material: 'Scrap Metal', level: 34, status: 'Critical' }
  ]

  const efficiencyData = [
    { name: 'Furnace #1', value: Math.round(productionMetrics.efficiency) },
    { name: 'Rolling Mill', value: Math.round(productionMetrics.efficiency - 7) },
    { name: 'Casting', value: Math.round(productionMetrics.efficiency + 3) },
    { name: 'Finishing', value: Math.round(productionMetrics.efficiency - 13) }
  ]

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']
  
  const getColorForLevel = (level: number) => {
    if (level > 70) return '#00C49F'
    if (level > 40) return '#FFBB28' 
    return '#FF8042'
  }
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight">Steel Manufacturing Dashboard</h1>
            <p className="text-muted-foreground">
              Real-time overview of production, inventory, and quality metrics
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Badge variant="outline" className={`${isConnected ? 'bg-green-50 text-green-700 border-green-200' : 'bg-red-50 text-red-700 border-red-200'}`}>
              {isConnected ? (
                <>
                  <Wifi className="w-3 h-3 mr-1" />
                  Backend Connected
                </>
              ) : (
                <>
                  <WifiOff className="w-3 h-3 mr-1" />
                  Offline Mode
                </>
              )}
            </Badge>
            <Badge variant="outline" className="bg-blue-50 text-blue-700 border-blue-200">
              <Zap className="w-2 h-2 mr-1 animate-pulse" />
              Last Update: {formatTime(lastUpdate)}
            </Badge>
            <Button variant="outline" size="sm" onClick={refreshAll} disabled={isLoading}>
              <Activity className="w-4 h-4 mr-2" />
              {isLoading ? 'Refreshing...' : 'Refresh Data'}
            </Button>
          </div>
        </div>

        {/* Key Metrics Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-l-4 border-l-blue-500 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Production Output</CardTitle>
              <Factory className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{Math.round(productionMetrics.output)} tons</div>
              <div className="flex items-center space-x-2">
                <TrendingUp className="h-4 w-4 text-green-500" />
                <p className="text-xs text-green-600">+{((productionMetrics.output - 2800) / 28).toFixed(1)}% from target</p>
              </div>
              <Progress value={(productionMetrics.output / 3800) * 100} className="mt-3" />
              <p className="text-xs text-muted-foreground mt-1">Target: 3,800 tons</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Inventory Status</CardTitle>
              <Package className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,245 items</div>
              <div className="flex items-center space-x-2">
                <CheckCircle className="h-4 w-4 text-green-500" />
                <p className="text-xs text-green-600">Optimal levels</p>
              </div>
              <Progress value={85} className="mt-3" />
              <p className="text-xs text-muted-foreground mt-1">Raw materials: 85%</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Quality Score</CardTitle>
              <CheckCircle className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{Math.round(productionMetrics.quality)}%</div>
              <div className="flex items-center space-x-2">
                {productionMetrics.quality >= 95 ? (
                  <>
                    <CheckCircle className="h-4 w-4 text-green-500" />
                    <p className="text-xs text-green-600">Excellent quality</p>
                  </>
                ) : (
                  <>
                    <AlertTriangle className="h-4 w-4 text-yellow-500" />
                    <p className="text-xs text-yellow-600">Needs attention</p>
                  </>
                )}
              </div>
              <Progress value={productionMetrics.quality} className="mt-3" />
              <p className="text-xs text-muted-foreground mt-1">Target: 96%</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500 hover:shadow-lg transition-shadow">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Orders</CardTitle>
              <Clock className="h-4 w-4 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">47</div>
              <div className="flex items-center space-x-2">
                <TrendingUp className="h-4 w-4 text-green-500" />
                <p className="text-xs text-green-600">8 completed today</p>
              </div>
              <Progress value={62} className="mt-3" />
              <p className="text-xs text-muted-foreground mt-1">On-time delivery: 92%</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Production Overview */}
          <Card className="lg:col-span-2">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Factory className="w-5 h-5" />
                Production Line Status
              </CardTitle>
              <CardDescription>
                Real-time status of all production lines
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {[
                { name: 'Blast Furnace #1', status: 'Running', efficiency: Math.round(productionMetrics.efficiency), color: 'green' },
                { name: 'Rolling Mill A', status: 'Running', efficiency: Math.round(productionMetrics.efficiency - 7), color: 'green' },
                { name: 'Steel Furnace #2', status: isConnected ? 'Running' : 'Maintenance', efficiency: isConnected ? Math.round(productionMetrics.efficiency - 15) : 0, color: isConnected ? 'blue' : 'yellow' },
                { name: 'Continuous Caster', status: 'Running', efficiency: Math.round(productionMetrics.efficiency + 3), color: 'green' },
                { name: 'Cold Rolling', status: 'Running', efficiency: Math.round(productionMetrics.efficiency - 13), color: 'blue' },
              ].map((line, index) => (
                <div key={index} className="flex items-center justify-between p-4 border rounded-lg hover:bg-accent/50 transition-colors">
                  <div className="flex items-center space-x-3">
                    <div className={`w-3 h-3 rounded-full bg-${line.color}-500 animate-pulse`} />
                    <div>
                      <p className="font-medium">{line.name}</p>
                      <p className="text-sm text-muted-foreground">{line.status}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium">{line.efficiency}%</p>
                    <Progress value={line.efficiency} className="w-20" />
                  </div>
                </div>
              ))}
            </CardContent>
          </Card>

          {/* Recent Activity */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="w-5 h-5" />
                Recent Activity
              </CardTitle>
              <CardDescription>
                Latest system updates and alerts
              </CardDescription>
            </CardHeader>
            <CardContent className="space-y-4">
              {alerts.slice(0, 5).map((activity, index) => {
                const getIcon = (type: string) => {
                  switch (type) {
                    case 'success': return CheckCircle
                    case 'warning': return AlertTriangle
                    case 'info': return Factory
                    default: return Clock
                  }
                }
                
                const Icon = getIcon(activity.type)
                const getTimeAgo = (time: Date) => {
                  const diff = Math.floor((Date.now() - time.getTime()) / 1000 / 60)
                  return diff < 1 ? 'Just now' : `${diff} min ago`
                }
                
                return (
                  <div key={activity.id} className="flex items-start space-x-3 p-3 border rounded-lg hover:bg-accent/50 transition-colors">
                    <Icon className={`w-4 h-4 mt-0.5 ${
                      activity.type === 'success' ? 'text-green-500' :
                      activity.type === 'warning' ? 'text-yellow-500' :
                      'text-blue-500'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <p className="text-sm font-medium">{activity.message}</p>
                      <p className="text-xs text-muted-foreground">{getTimeAgo(activity.time)}</p>
                    </div>
                  </div>
                )
              })}
            </CardContent>
          </Card>
        </div>

        {/* Charts Row */}
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Production Trends
              </CardTitle>
              <CardDescription>24-hour production output vs target</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={productionData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis domain={[2000, 3500]} />
                    <Tooltip 
                      formatter={(value, name) => [value + ' tons', name === 'output' ? 'Actual Output' : 'Target']}
                    />
                    <Line type="monotone" dataKey="output" stroke="#3b82f6" strokeWidth={3} dot={{ r: 4 }} />
                    <Line type="monotone" dataKey="target" stroke="#ef4444" strokeDasharray="5 5" strokeWidth={2} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Quality Metrics
              </CardTitle>
              <CardDescription>Weekly quality performance and defect rates</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={qualityData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="time" />
                    <YAxis yAxisId="quality" orientation="left" domain={[90, 100]} />
                    <YAxis yAxisId="defects" orientation="right" domain={[0, 15]} />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + (name === 'quality' ? '%' : ' defects'),
                        name === 'quality' ? 'Quality Score' : 'Defect Count'
                      ]}
                    />
                    <Area yAxisId="quality" type="monotone" dataKey="quality" stroke="#10b981" fill="#10b981" fillOpacity={0.3} strokeWidth={2} />
                    <Bar yAxisId="defects" dataKey="defects" fill="#f59e0b" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Equipment Efficiency and Inventory Levels */}
        <div className="grid gap-4 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Activity className="h-5 w-5" />
                Equipment Efficiency
              </CardTitle>
              <CardDescription>Real-time equipment performance distribution</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={efficiencyData}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {efficiencyData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [value + '%', 'Efficiency']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Raw Material Inventory
              </CardTitle>
              <CardDescription>Current inventory levels by material type</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={inventoryData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="material" />
                    <YAxis domain={[0, 100]} />
                    <Tooltip 
                      formatter={(value, name) => [value + '%', 'Stock Level']}
                      labelFormatter={(label) => `Material: ${label}`}
                    />
                    <Bar dataKey="level" radius={[4, 4, 0, 0]}>
                      {inventoryData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={getColorForLevel(entry.level)} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Quick Actions */}
        <Card>
          <CardHeader>
            <CardTitle>Quick Actions</CardTitle>
            <CardDescription>
              Frequently used operations and shortcuts
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-4">
              {[
                { name: 'New Production Order', icon: Factory, href: '/production' },
                { name: 'Inventory Check', icon: Package, href: '/inventory' },
                { name: 'Quality Test', icon: CheckCircle, href: '/quality' },
                { name: 'Schedule Shipment', icon: Clock, href: '/logistics' },
                { name: 'Raw Materials', icon: BarChart3, href: '/raw-materials' },
                { name: 'Analytics', icon: DollarSign, href: '/' },
              ].map((action, index) => (
                <Link key={index} href={action.href}>
                  <Button
                    variant="outline"
                    className="w-full h-20 flex-col space-y-2 hover:bg-accent hover:scale-105 transition-all cursor-pointer"
                  >
                    <action.icon className="w-6 h-6" />
                    <span className="text-xs text-center">{action.name}</span>
                  </Button>
                </Link>
              ))}
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}