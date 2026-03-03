"use client"

import { DashboardLayout } from '@/components/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Progress } from '@/components/ui/progress'
import { Tabs, TabsContent, TabsList, TabsTrigger } from '@/components/ui/tabs'
import {
  Factory,
  Plus,
  Search,
  Calendar,
  Clock,
  PlayCircle,
  PauseCircle,
  CheckCircle,
  AlertCircle,
  TrendingUp,
  Users,
  BarChart3
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
  AreaChart,
  Area,
  PieChart,
  Pie,
  Cell
} from 'recharts'

const productionOrders = [
  {
    id: 'PO-2024-001',
    product: 'Steel Beams - Grade A',
    quantity: 500,
    unit: 'units',
    priority: 'High',
    startDate: '2024-03-01',
    endDate: '2024-03-15',
    progress: 65,
    status: 'In Progress',
    assignedLine: 'Production Line A',
    estimatedCompletion: '2024-03-12',
    customer: 'ABC Construction',
    materials: ['Iron Ore', 'Coal', 'Limestone']
  },
  {
    id: 'PO-2024-002',
    product: 'Steel Plates - Grade B',
    quantity: 1200,
    unit: 'tons',
    priority: 'Medium',
    startDate: '2024-03-05',
    endDate: '2024-03-20',
    progress: 30,
    status: 'In Progress',
    assignedLine: 'Rolling Mill B',
    estimatedCompletion: '2024-03-18',
    customer: 'XYZ Industries',
    materials: ['Scrap Steel', 'Alloy Elements']
  },
  {
    id: 'PO-2024-003',
    product: 'Wire Rods',
    quantity: 800,
    unit: 'tons',
    priority: 'Low',
    startDate: '2024-03-10',
    endDate: '2024-03-25',
    progress: 10,
    status: 'Scheduled',
    assignedLine: 'Wire Mill C',
    estimatedCompletion: '2024-03-23',
    customer: 'Wire Works Ltd',
    materials: ['Iron Ore', 'Carbon']
  },
  {
    id: 'PO-2024-004',
    product: 'Steel Tubes',
    quantity: 300,
    unit: 'units',
    priority: 'Critical',
    startDate: '2024-02-28',
    endDate: '2024-03-08',
    progress: 90,
    status: 'Near Completion',
    assignedLine: 'Tube Mill D',
    estimatedCompletion: '2024-03-06',
    customer: 'Pipeline Corp',
    materials: ['Steel Coils', 'Coating Materials']
  },
]

const productionLines = [
  {
    id: 'PL-A',
    name: 'Blast Furnace #1',
    status: 'Running',
    currentOrder: 'PO-2024-001',
    efficiency: 95,
    capacity: '500 tons/day',
    operators: 8,
    nextMaintenance: '2024-03-15'
  },
  {
    id: 'PL-B',
    name: 'Rolling Mill A',
    status: 'Running',
    currentOrder: 'PO-2024-002',
    efficiency: 88,
    capacity: '300 tons/day',
    operators: 6,
    nextMaintenance: '2024-03-20'
  },
  {
    id: 'PL-C',
    name: 'Wire Mill',
    status: 'Idle',
    currentOrder: null,
    efficiency: 0,
    capacity: '200 tons/day',
    operators: 4,
    nextMaintenance: '2024-03-10'
  },
  {
    id: 'PL-D',
    name: 'Tube Mill',
    status: 'Running',
    currentOrder: 'PO-2024-004',
    efficiency: 92,
    capacity: '150 units/day',
    operators: 5,
    nextMaintenance: '2024-03-12'
  },
]

function getStatusBadge(status: string) {
  switch (status) {
    case 'In Progress':
      return <Badge className="bg-blue-100 text-blue-800">In Progress</Badge>
    case 'Scheduled':
      return <Badge variant="secondary">Scheduled</Badge>
    case 'Near Completion':
      return <Badge className="bg-green-100 text-green-800">Near Completion</Badge>
    case 'Completed':
      return <Badge className="bg-green-600 text-white">Completed</Badge>
    case 'On Hold':
      return <Badge variant="destructive">On Hold</Badge>
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}

function getPriorityBadge(priority: string) {
  switch (priority) {
    case 'Critical':
      return <Badge variant="destructive">Critical</Badge>
    case 'High':
      return <Badge className="bg-orange-100 text-orange-800">High</Badge>
    case 'Medium':
      return <Badge className="bg-yellow-100 text-yellow-800">Medium</Badge>
    case 'Low':
      return <Badge variant="secondary">Low</Badge>
    default:
      return <Badge variant="outline">{priority}</Badge>
  }
}

function getLineStatusBadge(status: string) {
  switch (status) {
    case 'Running':
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse" />
          <span className="text-green-700">Running</span>
        </div>
      )
    case 'Idle':
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-yellow-500 rounded-full" />
          <span className="text-yellow-700">Idle</span>
        </div>
      )
    case 'Maintenance':
      return (
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-red-500 rounded-full" />
          <span className="text-red-700">Maintenance</span>
        </div>
      )
    default:
      return <span className="text-muted-foreground">{status}</span>
  }
}

export default function ProductionPage() {
  // Sample data for production charts
  const productionTrends = [
    { hour: '08:00', output: 45, efficiency: 85, target: 50 },
    { hour: '10:00', output: 52, efficiency: 92, target: 50 },
    { hour: '12:00', output: 48, efficiency: 88, target: 50 },
    { hour: '14:00', output: 55, efficiency: 95, target: 50 },
    { hour: '16:00', output: 51, efficiency: 89, target: 50 },
    { hour: '18:00', output: 49, efficiency: 87, target: 50 },
  ]

  const lineEfficiency = [
    { line: 'Line A', efficiency: 94, capacity: 100, utilization: 85 },
    { line: 'Line B', efficiency: 88, capacity: 120, utilization: 92 },
    { line: 'Line C', efficiency: 91, capacity: 80, utilization: 78 },
    { line: 'Line D', efficiency: 86, capacity: 90, utilization: 88 },
  ]

  const productMix = [
    { name: 'Steel Beams', value: 35, color: '#0088FE' },
    { name: 'Steel Plates', value: 28, color: '#00C49F' },
    { name: 'Rebar', value: 20, color: '#FFBB28' },
    { name: 'Wire Rod', value: 17, color: '#FF8042' },
  ]

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042']
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
              <Factory className="w-8 h-8 text-primary" />
              Production Planning
            </h1>
            <p className="text-muted-foreground">
              Manage production orders, schedules, and resource allocation
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Calendar className="w-4 h-4 mr-2" />
              Schedule
            </Button>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              New Order
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Orders</CardTitle>
              <Factory className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">24</div>
              <div className="flex items-center space-x-1">
                <TrendingUp className="h-3 w-3 text-green-500" />
                <p className="text-xs text-green-600">+3 this week</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Avg Efficiency</CardTitle>
              <BarChart3 className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">89%</div>
              <p className="text-xs text-muted-foreground">Across all lines</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">On-Time Delivery</CardTitle>
              <CheckCircle className="h-4 w-4 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">92%</div>
              <p className="text-xs text-muted-foreground">Last 30 days</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Operators</CardTitle>
              <Users className="h-4 w-4 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">127</div>
              <p className="text-xs text-muted-foreground">Currently active</p>
            </CardContent>
          </Card>
        </div>

        {/* Production Analytics */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Production Output Trends
              </CardTitle>
              <CardDescription>Hourly production output and efficiency metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={productionTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis yAxisId="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + (name === 'efficiency' ? '%' : ' units'),
                        name === 'output' ? 'Output' : name === 'efficiency' ? 'Efficiency' : 'Target'
                      ]}
                    />
                    <Bar yAxisId="left" dataKey="output" fill="#3b82f6" name="output" />
                    <Line yAxisId="right" type="monotone" dataKey="efficiency" stroke="#10b981" strokeWidth={3} name="efficiency" />
                    <Line yAxisId="left" type="monotone" dataKey="target" stroke="#ef4444" strokeDasharray="5 5" name="target" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Production Line Performance
              </CardTitle>
              <CardDescription>Efficiency and utilization by production line</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={lineEfficiency}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="line" />
                    <YAxis domain={[0, 120]} />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + (name === 'efficiency' ? '%' : name === 'utilization' ? '%' : ' units'),
                        name === 'efficiency' ? 'Efficiency' : name === 'utilization' ? 'Utilization' : 'Capacity'
                      ]}
                    />
                    <Bar dataKey="efficiency" fill="#0088FE" name="efficiency" />
                    <Bar dataKey="utilization" fill="#00C49F" name="utilization" />
                    <Bar dataKey="capacity" fill="#FFBB28" opacity={0.5} name="capacity" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Factory className="h-5 w-5" />
                Production Mix
              </CardTitle>
              <CardDescription>Current product distribution by type</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={productMix}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {productMix.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [value + '%', 'Production Share']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Clock className="h-5 w-5" />
                Daily Production Capacity
              </CardTitle>
              <CardDescription>Utilization vs available capacity</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <AreaChart data={productionTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="hour" />
                    <YAxis domain={[0, 60]} />
                    <Tooltip 
                      formatter={(value, name) => [value + ' units', name === 'output' ? 'Current Output' : 'Target Capacity']}
                    />
                    <Area type="monotone" dataKey="target" stackId="1" stroke="#ef4444" fill="#fecaca" />
                    <Area type="monotone" dataKey="output" stackId="2" stroke="#3b82f6" fill="#93c5fd" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="orders" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="orders">Production Orders</TabsTrigger>
            <TabsTrigger value="lines">Production Lines</TabsTrigger>
            <TabsTrigger value="schedule">Schedule Overview</TabsTrigger>
          </TabsList>

          <TabsContent value="orders" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Production Orders</CardTitle>
                <CardDescription>
                  Manage and track all production orders and their progress
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input placeholder="Search orders..." className="pl-9" />
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Filter by Status
                  </Button>
                </div>

                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Order ID</TableHead>
                        <TableHead>Product</TableHead>
                        <TableHead>Quantity</TableHead>
                        <TableHead>Priority</TableHead>
                        <TableHead>Progress</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Deadline</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {productionOrders.map((order) => (
                        <TableRow key={order.id} className="hover:bg-muted/50">
                          <TableCell className="font-medium">{order.id}</TableCell>
                          <TableCell>
                            <div>
                              <p className="font-medium">{order.product}</p>
                              <p className="text-sm text-muted-foreground">
                                Line: {order.assignedLine}
                              </p>
                            </div>
                          </TableCell>
                          <TableCell>{order.quantity} {order.unit}</TableCell>
                          <TableCell>{getPriorityBadge(order.priority)}</TableCell>
                          <TableCell>
                            <div className="space-y-2">
                              <div className="flex items-center justify-between text-sm">
                                <span>{order.progress}%</span>
                                <span className="text-muted-foreground">
                                  Est: {order.estimatedCompletion}
                                </span>
                              </div>
                              <Progress value={order.progress} className="h-2" />
                            </div>
                          </TableCell>
                          <TableCell>{getStatusBadge(order.status)}</TableCell>
                          <TableCell>
                            <div>
                              <p className="text-sm">{order.endDate}</p>
                              <p className="text-xs text-muted-foreground">
                                Customer: {order.customer}
                              </p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Button variant="ghost" size="sm">
                                <PlayCircle className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <PauseCircle className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">Edit</Button>
                            </div>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="lines" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Production Line Status</CardTitle>
                <CardDescription>
                  Monitor real-time status and performance of all production lines
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {productionLines.map((line) => (
                    <Card key={line.id} className="border hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <span>{line.name}</span>
                          {getLineStatusBadge(line.status)}
                        </CardTitle>
                        <CardDescription>
                          {line.currentOrder ? 
                            `Currently processing: ${line.currentOrder}` : 
                            'Available for new orders'
                          }
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-muted-foreground">Capacity</p>
                            <p className="font-medium">{line.capacity}</p>
                          </div>
                          <div>
                            <p className="text-muted-foreground">Operators</p>
                            <p className="font-medium">{line.operators} active</p>
                          </div>
                        </div>
                        
                        <div>
                          <div className="flex items-center justify-between text-sm mb-2">
                            <span>Efficiency</span>
                            <span>{line.efficiency}%</span>
                          </div>
                          <Progress value={line.efficiency} className="h-2" />
                        </div>

                        <div className="flex items-center justify-between text-xs text-muted-foreground">
                          <span>Next Maintenance: {line.nextMaintenance}</span>
                        </div>

                        <div className="flex gap-2">
                          <Button variant="outline" size="sm" className="flex-1">
                            View Details
                          </Button>
                          <Button variant="outline" size="sm">
                            <AlertCircle className="w-4 h-4" />
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="schedule">
            <Card>
              <CardHeader>
                <CardTitle>Production Schedule</CardTitle>
                <CardDescription>
                  Weekly production schedule and resource allocation
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="text-center py-12 text-muted-foreground">
                  <Calendar className="w-12 h-12 mx-auto mb-4" />
                  <p>Production schedule calendar coming soon...</p>
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}