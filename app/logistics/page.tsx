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
  Truck,
  Plus,
  Search,
  MapPin,
  Package,
  Clock,
  CheckCircle,
  AlertTriangle,
  Route,
  Calendar,
  BarChart3,
  TrendingUp,
  Users
} from 'lucide-react'

const shipments = [
  {
    id: 'SH-2024-001',
    orderId: 'ORD-2024-045',
    customer: 'ABC Construction Ltd.',
    destination: 'New York, NY',
    product: 'Steel Beams - Grade A',
    quantity: '500 units',
    carrier: 'Fast Transport Co.',
    trackingNumber: 'FTC-789456123',
    shipDate: '2024-02-25',
    estimatedDelivery: '2024-03-02',
    actualDelivery: null,
    status: 'In Transit',
    priority: 'High',
    value: '$625,000',
    progress: 65
  },
  {
    id: 'SH-2024-002',
    orderId: 'ORD-2024-046',
    customer: 'XYZ Industries',
    destination: 'Chicago, IL',
    product: 'Steel Plates - Grade B',
    quantity: '200 tons',
    carrier: 'Reliable Logistics',
    trackingNumber: 'RL-456789012',
    shipDate: '2024-02-28',
    estimatedDelivery: '2024-03-05',
    actualDelivery: null,
    status: 'Preparing',
    priority: 'Medium',
    value: '$170,000',
    progress: 15
  },
  {
    id: 'SH-2024-003',
    orderId: 'ORD-2024-047',
    customer: 'Steel Works Corp.',
    destination: 'Houston, TX',
    product: 'Wire Rods',
    quantity: '150 tons',
    carrier: 'Express Freight',
    trackingNumber: 'EF-123456789',
    shipDate: '2024-02-20',
    estimatedDelivery: '2024-02-27',
    actualDelivery: '2024-02-26',
    status: 'Delivered',
    priority: 'Low',
    value: '$108,000',
    progress: 100
  },
  {
    id: 'SH-2024-004',
    orderId: 'ORD-2024-048',
    customer: 'Pipeline Solutions',
    destination: 'Denver, CO',
    product: 'Steel Tubes',
    quantity: '300 units',
    carrier: 'Mountain Transport',
    trackingNumber: 'MT-987654321',
    shipDate: '2024-02-26',
    estimatedDelivery: '2024-03-04',
    actualDelivery: null,
    status: 'In Transit',
    priority: 'Critical',
    value: '$135,000',
    progress: 45
  },
]

const carriers = [
  {
    id: 'CAR-001',
    name: 'Fast Transport Co.',
    rating: 4.8,
    onTimeDelivery: 96.5,
    activeShipments: 12,
    capacity: 'Heavy Cargo',
    contact: 'transport@fastco.com',
    status: 'Active'
  },
  {
    id: 'CAR-002',
    name: 'Reliable Logistics',
    rating: 4.6,
    onTimeDelivery: 94.2,
    activeShipments: 8,
    capacity: 'Medium & Heavy',
    contact: 'ops@reliable.com',
    status: 'Active'
  },
  {
    id: 'CAR-003',
    name: 'Express Freight',
    rating: 4.9,
    onTimeDelivery: 98.1,
    activeShipments: 15,
    capacity: 'All Types',
    contact: 'service@express.com',
    status: 'Active'
  },
  {
    id: 'CAR-004',
    name: 'Mountain Transport',
    rating: 4.3,
    onTimeDelivery: 91.7,
    activeShipments: 6,
    capacity: 'Specialized',
    contact: 'info@mountain.com',
    status: 'Limited'
  },
]

const deliveryRoutes = [
  {
    id: 'RT-001',
    name: 'Northeast Route',
    destinations: ['New York', 'Boston', 'Philadelphia'],
    frequency: 'Daily',
    averageDuration: '2-3 days',
    cost: '$2.50/mile',
    status: 'Active'
  },
  {
    id: 'RT-002',
    name: 'Midwest Route',
    destinations: ['Chicago', 'Detroit', 'Milwaukee'],
    frequency: 'Daily',
    averageDuration: '1-2 days',
    cost: '$2.20/mile',
    status: 'Active'
  },
  {
    id: 'RT-003',
    name: 'Southern Route',
    destinations: ['Houston', 'Dallas', 'Atlanta'],
    frequency: '3x/week',
    averageDuration: '2-4 days',
    cost: '$2.80/mile',
    status: 'Active'
  },
  {
    id: 'RT-004',
    name: 'Western Route',
    destinations: ['Los Angeles', 'San Francisco', 'Seattle'],
    frequency: '2x/week',
    averageDuration: '4-6 days',
    cost: '$3.20/mile',
    status: 'Seasonal'
  },
]

function getStatusBadge(status: string) {
  switch (status) {
    case 'Delivered':
      return <Badge className="bg-green-100 text-green-800">Delivered</Badge>
    case 'In Transit':
      return <Badge className="bg-blue-100 text-blue-800">In Transit</Badge>
    case 'Preparing':
      return <Badge className="bg-yellow-100 text-yellow-800">Preparing</Badge>
    case 'Delayed':
      return <Badge variant="destructive">Delayed</Badge>
    case 'Cancelled':
      return <Badge variant="secondary">Cancelled</Badge>
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
      return <Badge className="bg-blue-100 text-blue-800">Medium</Badge>
    case 'Low':
      return <Badge variant="secondary">Low</Badge>
    default:
      return <Badge variant="outline">{priority}</Badge>
  }
}

function getCarrierStatusBadge(status: string) {
  switch (status) {
    case 'Active':
      return <Badge className="bg-green-100 text-green-800">Active</Badge>
    case 'Limited':
      return <Badge className="bg-yellow-100 text-yellow-800">Limited</Badge>
    case 'Inactive':
      return <Badge variant="secondary">Inactive</Badge>
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}

export default function LogisticsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
              <Truck className="w-8 h-8 text-primary" />
              Logistics & Shipping
            </h1>
            <p className="text-muted-foreground">
              Manage shipments, track deliveries, and coordinate logistics operations
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Route className="w-4 h-4 mr-2" />
              Track All
            </Button>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              New Shipment
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Shipments</CardTitle>
              <Truck className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">47</div>
              <div className="flex items-center space-x-1">
                <TrendingUp className="h-3 w-3 text-green-500" />
                <p className="text-xs text-green-600">+8 this week</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">On-Time Delivery</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">94.8%</div>
              <p className="text-xs text-muted-foreground">Last 30 days</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-orange-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Value</CardTitle>
              <BarChart3 className="h-4 w-4 text-orange-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">$2.8M</div>
              <p className="text-xs text-muted-foreground">Shipments in transit</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-purple-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Active Carriers</CardTitle>
              <Users className="h-4 w-4 text-purple-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <p className="text-xs text-muted-foreground">Verified partners</p>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="shipments" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="shipments">Shipments</TabsTrigger>
            <TabsTrigger value="carriers">Carriers</TabsTrigger>
            <TabsTrigger value="routes">Routes</TabsTrigger>
          </TabsList>

          <TabsContent value="shipments" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Shipment Tracking</CardTitle>
                <CardDescription>
                  Monitor all shipments and delivery status in real-time
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input placeholder="Search shipments..." className="pl-9" />
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Filter by Status
                  </Button>
                  <Button variant="outline" size="sm">
                    Filter by Priority
                  </Button>
                </div>

                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Shipment ID</TableHead>
                        <TableHead>Customer & Product</TableHead>
                        <TableHead>Destination</TableHead>
                        <TableHead>Carrier</TableHead>
                        <TableHead>Progress</TableHead>
                        <TableHead>Priority</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {shipments.map((shipment) => (
                        <TableRow key={shipment.id} className="hover:bg-muted/50">
                          <TableCell className="font-medium">{shipment.id}</TableCell>
                          <TableCell>
                            <div>
                              <p className="font-medium">{shipment.customer}</p>
                              <p className="text-sm text-muted-foreground">
                                {shipment.product} • {shipment.quantity}
                              </p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <MapPin className="w-3 h-3 text-muted-foreground" />
                              <span className="text-sm">{shipment.destination}</span>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div>
                              <p className="text-sm font-medium">{shipment.carrier}</p>
                              <p className="text-xs text-muted-foreground font-mono">
                                {shipment.trackingNumber}
                              </p>
                            </div>
                          </TableCell>
                          <TableCell>
                            <div className="space-y-2">
                              <div className="flex items-center justify-between text-sm">
                                <span>{shipment.progress}%</span>
                                <span className="text-muted-foreground">
                                  Est: {shipment.estimatedDelivery}
                                </span>
                              </div>
                              <Progress value={shipment.progress} className="h-2" />
                            </div>
                          </TableCell>
                          <TableCell>{getPriorityBadge(shipment.priority)}</TableCell>
                          <TableCell>{getStatusBadge(shipment.status)}</TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Button variant="ghost" size="sm">
                                <Route className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Package className="w-4 h-4" />
                              </Button>
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

          <TabsContent value="carriers" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Shipping Carriers</CardTitle>
                <CardDescription>
                  Manage carrier partnerships and performance metrics
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {carriers.map((carrier) => (
                    <Card key={carrier.id} className="border hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <span>{carrier.name}</span>
                          {getCarrierStatusBadge(carrier.status)}
                        </CardTitle>
                        <CardDescription>
                          {carrier.capacity} • {carrier.contact}
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-muted-foreground">Rating</p>
                            <p className="font-medium">{carrier.rating}/5.0 ⭐</p>
                          </div>
                          <div>
                            <p className="text-muted-foreground">Active Shipments</p>
                            <p className="font-medium">{carrier.activeShipments}</p>
                          </div>
                        </div>
                        
                        <div>
                          <div className="flex items-center justify-between text-sm mb-2">
                            <span>On-Time Delivery</span>
                            <span>{carrier.onTimeDelivery}%</span>
                          </div>
                          <Progress value={carrier.onTimeDelivery} className="h-2" />
                        </div>

                        <div className="flex gap-2">
                          <Button variant="outline" size="sm" className="flex-1">
                            View Details
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            disabled={carrier.status !== 'Active'}
                          >
                            Book Shipment
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="routes" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Delivery Routes</CardTitle>
                <CardDescription>
                  Optimize delivery routes and manage shipping lanes
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {deliveryRoutes.map((route) => (
                    <Card key={route.id} className="border hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <span>{route.name}</span>
                          <Badge variant={route.status === 'Active' ? 'default' : 'secondary'}>
                            {route.status}
                          </Badge>
                        </CardTitle>
                        <CardDescription>
                          {route.destinations.join(' • ')}
                        </CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-muted-foreground">Frequency</p>
                            <p className="font-medium">{route.frequency}</p>
                          </div>
                          <div>
                            <p className="text-muted-foreground">Duration</p>
                            <p className="font-medium">{route.averageDuration}</p>
                          </div>
                        </div>
                        
                        <div>
                          <p className="text-sm text-muted-foreground">Cost</p>
                          <p className="font-medium text-lg">{route.cost}</p>
                        </div>

                        <div className="flex gap-2">
                          <Button variant="outline" size="sm" className="flex-1">
                            <MapPin className="w-4 h-4 mr-2" />
                            View Map
                          </Button>
                          <Button variant="outline" size="sm">
                            <Calendar className="w-4 h-4" />
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}