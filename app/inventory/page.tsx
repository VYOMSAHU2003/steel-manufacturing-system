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
  Store,
  Plus,
  Search,
  Download,
  Upload,
  Package,
  TrendingUp,
  TrendingDown,
  AlertTriangle,
  CheckCircle,
  Eye,
  Edit,
  BarChart3,
  FileText,
  ArrowUpCircle,
  ArrowDownCircle
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

const inventoryItems = [
  {
    id: 'INV-001',
    name: 'Steel Beams - A Grade',
    category: 'Finished Products',
    sku: 'SB-A-001',
    currentStock: 150,
    reservedStock: 30,
    availableStock: 120,
    reorderLevel: 50,
    location: 'Warehouse 1 - A12',
    unit: 'pieces',
    unitPrice: '$1,250',
    totalValue: '$187,500',
    supplier: 'Internal Production',
    lastMovement: '2024-02-27',
    status: 'Good Stock'
  },
  {
    id: 'INV-002',
    name: 'Steel Plates - B Grade',
    category: 'Finished Products',
    sku: 'SP-B-002',
    currentStock: 240,
    reservedStock: 80,
    availableStock: 160,
    reorderLevel: 100,
    location: 'Warehouse 2 - B15',
    unit: 'tons',
    unitPrice: '$850',
    totalValue: '$204,000',
    supplier: 'Internal Production',
    lastMovement: '2024-02-28',
    status: 'Good Stock'
  },
  {
    id: 'INV-003',
    name: 'Wire Rods',
    category: 'Semi-Finished',
    sku: 'WR-003',
    currentStock: 45,
    reservedStock: 20,
    availableStock: 25,
    reorderLevel: 60,
    location: 'Warehouse 1 - C08',
    unit: 'tons',
    unitPrice: '$720',
    totalValue: '$32,400',
    supplier: 'Internal Production',
    lastMovement: '2024-02-26',
    status: 'Low Stock'
  },
  {
    id: 'INV-004',
    name: 'Steel Tubes',
    category: 'Finished Products',
    sku: 'ST-004',
    currentStock: 300,
    reservedStock: 100,
    availableStock: 200,
    reorderLevel: 150,
    location: 'Warehouse 3 - D20',
    unit: 'pieces',
    unitPrice: '$450',
    totalValue: '$135,000',
    supplier: 'Internal Production',
    lastMovement: '2024-02-28',
    status: 'Good Stock'
  },
  {
    id: 'INV-005',
    name: 'Galvanized Sheets',
    category: 'Processed',
    sku: 'GS-005',
    currentStock: 15,
    reservedStock: 10,
    availableStock: 5,
    reorderLevel: 25,
    location: 'Warehouse 2 - E05',
    unit: 'tons',
    unitPrice: '$1,100',
    totalValue: '$16,500',
    supplier: 'External - Coating Co.',
    lastMovement: '2024-02-25',
    status: 'Critical'
  },
]

const recentMovements = [
  {
    id: 'MOV-001',
    type: 'IN',
    item: 'Steel Beams - A Grade',
    quantity: 50,
    unit: 'pieces',
    timestamp: '2024-02-28 14:30',
    reference: 'PO-2024-001',
    operator: 'John Smith'
  },
  {
    id: 'MOV-002',
    type: 'OUT',
    item: 'Steel Plates - B Grade',
    quantity: 25,
    unit: 'tons',
    timestamp: '2024-02-28 13:15',
    reference: 'SO-2024-045',
    operator: 'Sarah Johnson'
  },
  {
    id: 'MOV-003',
    type: 'TRANSFER',
    item: 'Wire Rods',
    quantity: 10,
    unit: 'tons',
    timestamp: '2024-02-28 11:00',
    reference: 'TRF-001',
    operator: 'Mike Davis'
  },
  {
    id: 'MOV-004',
    type: 'ADJUSTMENT',
    item: 'Steel Tubes',
    quantity: -5,
    unit: 'pieces',
    timestamp: '2024-02-28 09:45',
    reference: 'ADJ-028',
    operator: 'Lisa Chen'
  },
]

const warehouses = [
  {
    id: 'WH-001',
    name: 'Warehouse 1',
    location: 'North Plant',
    capacity: '5,000 tons',
    currentUtilization: 85,
    sections: 15,
    items: 234,
    manager: 'Robert Wilson'
  },
  {
    id: 'WH-002',
    name: 'Warehouse 2',
    location: 'South Plant',
    capacity: '7,500 tons',
    currentUtilization: 72,
    sections: 20,
    items: 189,
    manager: 'Emily Parker'
  },
  {
    id: 'WH-003',
    name: 'Warehouse 3',
    location: 'East Plant',
    capacity: '3,000 tons',
    currentUtilization: 93,
    sections: 12,
    items: 156,
    manager: 'David Thompson'
  },
]

function getStatusBadge(status: string) {
  switch (status) {
    case 'Good Stock':
      return <Badge className="bg-green-100 text-green-800">Good Stock</Badge>
    case 'Low Stock':
      return <Badge className="bg-yellow-100 text-yellow-800">Low Stock</Badge>
    case 'Critical':
      return <Badge variant="destructive">Critical</Badge>
    case 'Out of Stock':
      return <Badge variant="destructive">Out of Stock</Badge>
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}

function getMovementBadge(type: string) {
  switch (type) {
    case 'IN':
      return <Badge className="bg-green-100 text-green-800">IN</Badge>
    case 'OUT':
      return <Badge className="bg-red-100 text-red-800">OUT</Badge>
    case 'TRANSFER':
      return <Badge className="bg-blue-100 text-blue-800">TRANSFER</Badge>
    case 'ADJUSTMENT':
      return <Badge className="bg-orange-100 text-orange-800">ADJUST</Badge>
    default:
      return <Badge variant="outline">{type}</Badge>
  }
}

export default function InventoryPage() {
  // Sample data for inventory charts
  const stockLevels = [
    { material: 'Iron Ore', current: 2850, minimum: 2000, maximum: 5000, trend: 'stable' },
    { material: 'Coal', current: 1200, minimum: 1500, maximum: 4000, trend: 'decreasing' },
    { material: 'Limestone', current: 3200, minimum: 1000, maximum: 4000, trend: 'increasing' },
    { material: 'Scrap Metal', current: 850, minimum: 1000, maximum: 3000, trend: 'critical' },
    { material: 'Alloys', current: 450, minimum: 300, maximum: 1000, trend: 'stable' }
  ]

  const consumptionTrends = [
    { date: '2024-02-20', ironOre: 280, coal: 150, limestone: 120, scrap: 90 },
    { date: '2024-02-21', ironOre: 295, coal: 165, limestone: 135, scrap: 85 },
    { date: '2024-02-22', ironOre: 310, coal: 140, limestone: 140, scrap: 95 },
    { date: '2024-02-23', ironOre: 285, coal: 175, limestone: 125, scrap: 80 },
    { date: '2024-02-24', ironOre: 320, coal: 160, limestone: 150, scrap: 100 },
    { date: '2024-02-25', ironOre: 305, coal: 155, limestone: 145, scrap: 90 },
    { date: '2024-02-26', ironOre: 275, coal: 170, limestone: 130, scrap: 85 }
  ]

  const inventoryTurnover = [
    { category: 'Raw Materials', turnover: 8.5, value: 2.4 },
    { category: 'Work in Progress', turnover: 12.3, value: 1.8 },
    { category: 'Finished Goods', turnover: 15.7, value: 3.2 },
    { category: 'Maintenance Parts', turnover: 4.2, value: 0.8 }
  ]

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']

  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
              <Store className="w-8 h-8 text-primary" />
              Inventory Management
            </h1>
            <p className="text-muted-foreground">
              Monitor stock levels, track movements, and manage warehouse operations
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
            <Button variant="outline" size="sm">
              <Upload className="w-4 h-4 mr-2" />
              Import
            </Button>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              Add Item
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Items</CardTitle>
              <Package className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">1,247</div>
              <div className="flex items-center space-x-1">
                <TrendingUp className="h-3 w-3 text-green-500" />
                <p className="text-xs text-green-600">+5% this month</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Value</CardTitle>
              <BarChart3 className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">$2.8M</div>
              <p className="text-xs text-muted-foreground">Current inventory value</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Low Stock Items</CardTitle>
              <AlertTriangle className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">23</div>
              <div className="flex items-center space-x-1">
                <TrendingDown className="h-3 w-3 text-red-500" />
                <p className="text-xs text-red-600">Requires attention</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-red-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Warehouses</CardTitle>
              <Store className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-muted-foreground">Active locations</p>
            </CardContent>
          </Card>
        </div>

        {/* Inventory Analytics */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Current Stock Levels
              </CardTitle>
              <CardDescription>Material inventory vs minimum/maximum thresholds</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={stockLevels}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="material" angle={-45} textAnchor="end" height={80} />
                    <YAxis />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + ' tons',
                        name === 'current' ? 'Current Stock' : 
                        name === 'minimum' ? 'Minimum Level' : 'Maximum Capacity'
                      ]}
                    />
                    <Bar dataKey="maximum" fill="#e5e7eb" name="maximum" />
                    <Bar dataKey="minimum" fill="#fbbf24" name="minimum" />
                    <Bar dataKey="current" fill="#3b82f6" name="current" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingDown className="h-5 w-5" />
                Daily Consumption Trends
              </CardTitle>
              <CardDescription>Material consumption patterns over the last week</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={consumptionTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis />
                    <Tooltip 
                      formatter={(value, name) => [value + ' tons', name]}
                      labelFormatter={(label) => `Date: ${label}`}
                    />
                    <Line type="monotone" dataKey="ironOre" stroke="#0088FE" strokeWidth={2} name="Iron Ore" />
                    <Line type="monotone" dataKey="coal" stroke="#00C49F" strokeWidth={2} name="Coal" />
                    <Line type="monotone" dataKey="limestone" stroke="#FFBB28" strokeWidth={2} name="Limestone" />
                    <Line type="monotone" dataKey="scrap" stroke="#FF8042" strokeWidth={2} name="Scrap Metal" />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Package className="h-5 w-5" />
                Inventory Turnover Analysis
              </CardTitle>
              <CardDescription>Turnover rates and inventory value by category</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={inventoryTurnover}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="category" angle={-45} textAnchor="end" height={80} />
                    <YAxis yAxisId="left" orientation="left" />
                    <YAxis yAxisId="right" orientation="right" />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + (name === 'turnover' ? ' times/year' : ' M$'),
                        name === 'turnover' ? 'Turnover Rate' : 'Inventory Value'
                      ]}
                    />
                    <Bar yAxisId="left" dataKey="turnover" fill="#8884d8" name="turnover" />
                    <Bar yAxisId="right" dataKey="value" fill="#82ca9d" name="value" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Stock Status Distribution
              </CardTitle>
              <CardDescription>Material stock levels categorized by status</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Normal', value: 65, color: '#00C49F' },
                        { name: 'Low Stock', value: 20, color: '#FFBB28' },
                        { name: 'Critical', value: 10, color: '#FF8042' },
                        { name: 'Overstock', value: 5, color: '#0088FE' }
                      ]}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="value"
                      label={({ name, value }) => `${name}: ${value}%`}
                    >
                      {[{ color: '#00C49F' }, { color: '#FFBB28' }, { color: '#FF8042' }, { color: '#0088FE' }].map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.color} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [value + '%', 'Materials']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="inventory" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="inventory">Inventory Items</TabsTrigger>
            <TabsTrigger value="movements">Stock Movements</TabsTrigger>
            <TabsTrigger value="warehouses">Warehouses</TabsTrigger>
          </TabsList>

          <TabsContent value="inventory" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Inventory Items</CardTitle>
                <CardDescription>
                  Complete list of inventory items with current stock levels and status
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input placeholder="Search inventory..." className="pl-9" />
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Filter by Category
                  </Button>
                </div>

                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Item Details</TableHead>
                        <TableHead>SKU</TableHead>
                        <TableHead>Stock Status</TableHead>
                        <TableHead>Location</TableHead>
                        <TableHead>Value</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {inventoryItems.map((item) => (
                        <TableRow key={item.id} className="hover:bg-muted/50">
                          <TableCell>
                            <div>
                              <p className="font-medium">{item.name}</p>
                              <p className="text-sm text-muted-foreground">{item.category}</p>
                            </div>
                          </TableCell>
                          <TableCell className="font-mono text-sm">{item.sku}</TableCell>
                          <TableCell>
                            <div className="space-y-1">
                              <div className="flex items-center justify-between text-sm">
                                <span>Available: {item.availableStock}</span>
                                <span className="text-muted-foreground">
                                  Total: {item.currentStock}
                                </span>
                              </div>
                              <div className="flex items-center justify-between text-xs">
                                <span>Reserved: {item.reservedStock}</span>
                                <span className="text-muted-foreground">
                                  Reorder: {item.reorderLevel}
                                </span>
                              </div>
                              <Progress 
                                value={(item.currentStock / (item.reorderLevel * 2)) * 100} 
                                className="h-1"
                              />
                            </div>
                          </TableCell>
                          <TableCell>{item.location}</TableCell>
                          <TableCell>
                            <div>
                              <p className="font-medium">{item.totalValue}</p>
                              <p className="text-sm text-muted-foreground">{item.unitPrice}/{item.unit}</p>
                            </div>
                          </TableCell>
                          <TableCell>{getStatusBadge(item.status)}</TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Button variant="ghost" size="sm">
                                <Eye className="w-4 h-4" />
                              </Button>
                              <Button variant="ghost" size="sm">
                                <Edit className="w-4 h-4" />
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

          <TabsContent value="movements" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Recent Stock Movements</CardTitle>
                <CardDescription>
                  Track all inventory movements including receipts, shipments, and transfers
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Movement ID</TableHead>
                        <TableHead>Type</TableHead>
                        <TableHead>Item</TableHead>
                        <TableHead>Quantity</TableHead>
                        <TableHead>Timestamp</TableHead>
                        <TableHead>Reference</TableHead>
                        <TableHead>Operator</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {recentMovements.map((movement) => (
                        <TableRow key={movement.id} className="hover:bg-muted/50">
                          <TableCell className="font-medium">{movement.id}</TableCell>
                          <TableCell>{getMovementBadge(movement.type)}</TableCell>
                          <TableCell>{movement.item}</TableCell>
                          <TableCell>
                            <span className={movement.quantity > 0 ? 'text-green-600' : 'text-red-600'}>
                              {movement.quantity > 0 ? '+' : ''}{movement.quantity} {movement.unit}
                            </span>
                          </TableCell>
                          <TableCell>{movement.timestamp}</TableCell>
                          <TableCell className="font-mono text-sm">{movement.reference}</TableCell>
                          <TableCell>{movement.operator}</TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="warehouses" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
              {warehouses.map((warehouse) => (
                <Card key={warehouse.id} className="border hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="flex items-center justify-between">
                      <span>{warehouse.name}</span>
                      <Store className="w-5 h-5 text-muted-foreground" />
                    </CardTitle>
                    <CardDescription>{warehouse.location}</CardDescription>
                  </CardHeader>
                  <CardContent className="space-y-4">
                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Capacity</p>
                        <p className="font-medium">{warehouse.capacity}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Sections</p>
                        <p className="font-medium">{warehouse.sections}</p>
                      </div>
                    </div>
                    
                    <div>
                      <div className="flex items-center justify-between text-sm mb-2">
                        <span>Utilization</span>
                        <span>{warehouse.currentUtilization}%</span>
                      </div>
                      <Progress value={warehouse.currentUtilization} className="h-2" />
                    </div>

                    <div className="grid grid-cols-2 gap-4 text-sm">
                      <div>
                        <p className="text-muted-foreground">Items</p>
                        <p className="font-medium">{warehouse.items}</p>
                      </div>
                      <div>
                        <p className="text-muted-foreground">Manager</p>
                        <p className="font-medium">{warehouse.manager}</p>
                      </div>
                    </div>

                    <Button variant="outline" className="w-full">
                      View Details
                    </Button>
                  </CardContent>
                </Card>
              ))}
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}