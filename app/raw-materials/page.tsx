"use client"

import { DashboardLayout } from '@/components/dashboard-layout'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Badge } from '@/components/ui/badge'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table'
import { Progress } from '@/components/ui/progress'
import {
  Package,
  Plus,
  Search,
  Filter,
  Download,
  AlertTriangle,
  CheckCircle,
  TrendingDown,
  TrendingUp,
  BarChart3
} from 'lucide-react'

const rawMaterials = [
  {
    id: 'RM001',
    name: 'Iron Ore',
    category: 'Primary Material',
    currentStock: 1500,
    minimumStock: 500,
    unit: 'tons',
    location: 'Warehouse A',
    supplier: 'Mining Corp Ltd',
    lastUpdated: '2024-02-28',
    status: 'Good Stock',
    cost: '$85/ton'
  },
  {
    id: 'RM002',
    name: 'Coal',
    category: 'Fuel',
    currentStock: 800,
    minimumStock: 300,
    unit: 'tons',
    location: 'Storage B',
    supplier: 'Coal Industries',
    lastUpdated: '2024-02-27',
    status: 'Good Stock',
    cost: '$120/ton'
  },
  {
    id: 'RM003',
    name: 'Limestone',
    category: 'Flux Material',
    currentStock: 200,
    minimumStock: 250,
    unit: 'tons',
    location: 'Warehouse C',
    supplier: 'Stone Quarries Inc',
    lastUpdated: '2024-02-28',
    status: 'Low Stock',
    cost: '$45/ton'
  },
  {
    id: 'RM004',
    name: 'Scrap Steel',
    category: 'Recycled Material',
    currentStock: 650,
    minimumStock: 200,
    unit: 'tons',
    location: 'Scrap Yard',
    supplier: 'Metal Recyclers',
    lastUpdated: '2024-02-28',
    status: 'Good Stock',
    cost: '$350/ton'
  },
  {
    id: 'RM005',
    name: 'Alloy Elements',
    category: 'Additives',
    currentStock: 80,
    minimumStock: 100,
    unit: 'kg',
    location: 'Secure Storage',
    supplier: 'Specialty Metals',
    lastUpdated: '2024-02-26',
    status: 'Critical',
    cost: '$15/kg'
  },
]

function getStatusBadge(status: string, currentStock: number, minimumStock: number) {
  const percentage = (currentStock / minimumStock) * 100
  
  if (percentage < 80) {
    return <Badge variant="destructive" className="text-xs">Critical</Badge>
  } else if (percentage < 120) {
    return <Badge variant="secondary" className="text-xs">Low Stock</Badge>
  } else {
    return <Badge variant="default" className="bg-green-100 text-green-800 text-xs">Good Stock</Badge>
  }
}

function getStockPercentage(currentStock: number, minimumStock: number) {
  return Math.min((currentStock / minimumStock) * 100, 100)
}

export default function RawMaterialsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
              <Package className="w-8 h-8 text-primary" />
              Raw Materials Management
            </h1>
            <p className="text-muted-foreground">
              Monitor and manage raw material inventory, suppliers, and stock levels
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Download className="w-4 h-4 mr-2" />
              Export
            </Button>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              Add Material
            </Button>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <Card className="border-l-4 border-l-blue-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Total Materials</CardTitle>
              <Package className="h-4 w-4 text-blue-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">47</div>
              <p className="text-xs text-muted-foreground">Active materials</p>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-green-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Good Stock</CardTitle>
              <CheckCircle className="h-4 w-4 text-green-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">32</div>
              <div className="flex items-center space-x-1">
                <TrendingUp className="h-3 w-3 text-green-500" />
                <p className="text-xs text-green-600">68% of total</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-yellow-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Low Stock</CardTitle>
              <AlertTriangle className="h-4 w-4 text-yellow-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">12</div>
              <div className="flex items-center space-x-1">
                <TrendingDown className="h-3 w-3 text-yellow-500" />
                <p className="text-xs text-yellow-600">Need reorder</p>
              </div>
            </CardContent>
          </Card>

          <Card className="border-l-4 border-l-red-500">
            <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
              <CardTitle className="text-sm font-medium">Critical Items</CardTitle>
              <AlertTriangle className="h-4 w-4 text-red-500" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">3</div>
              <p className="text-xs text-red-600">Immediate attention</p>
            </CardContent>
          </Card>
        </div>

        {/* Filter and Search */}
        <Card>
          <CardHeader>
            <CardTitle>Material Inventory</CardTitle>
            <CardDescription>
              Complete list of raw materials with current stock levels
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col sm:flex-row gap-4 mb-6">
              <div className="flex-1">
                <div className="relative">
                  <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                  <Input
                    placeholder="Search materials..."
                    className="pl-9"
                  />
                </div>
              </div>
              <Button variant="outline" size="sm">
                <Filter className="w-4 h-4 mr-2" />
                Filter
              </Button>
            </div>

            <div className="rounded-md border">
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Material ID</TableHead>
                    <TableHead>Name & Category</TableHead>
                    <TableHead>Stock Level</TableHead>
                    <TableHead>Location</TableHead>
                    <TableHead>Supplier</TableHead>
                    <TableHead>Cost</TableHead>
                    <TableHead>Status</TableHead>
                    <TableHead>Actions</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  {rawMaterials.map((material) => (
                    <TableRow key={material.id} className="hover:bg-muted/50">
                      <TableCell className="font-medium">{material.id}</TableCell>
                      <TableCell>
                        <div>
                          <p className="font-medium">{material.name}</p>
                          <p className="text-sm text-muted-foreground">{material.category}</p>
                        </div>
                      </TableCell>
                      <TableCell>
                        <div className="space-y-2">
                          <div className="flex items-center justify-between text-sm">
                            <span>{material.currentStock} {material.unit}</span>
                            <span className="text-muted-foreground">
                              Min: {material.minimumStock}
                            </span>
                          </div>
                          <Progress 
                            value={getStockPercentage(material.currentStock, material.minimumStock)} 
                            className="h-2"
                          />
                        </div>
                      </TableCell>
                      <TableCell>{material.location}</TableCell>
                      <TableCell>
                        <div>
                          <p className="text-sm">{material.supplier}</p>
                          <p className="text-xs text-muted-foreground">
                            Updated: {material.lastUpdated}
                          </p>
                        </div>
                      </TableCell>
                      <TableCell className="font-medium">{material.cost}</TableCell>
                      <TableCell>
                        {getStatusBadge(material.status, material.currentStock, material.minimumStock)}
                      </TableCell>
                      <TableCell>
                        <div className="flex items-center gap-2">
                          <Button variant="ghost" size="sm">Edit</Button>
                          <Button variant="ghost" size="sm">Reorder</Button>
                        </div>
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </div>
          </CardContent>
        </Card>
      </div>
    </DashboardLayout>
  )
}