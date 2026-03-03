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
  ShieldCheck,
  Plus,
  Search,
  Download,
  CheckCircle,
  XCircle,
  AlertTriangle,
  RotateCcw,
  FileText,
  BarChart3,
  TrendingUp,
  Clock,
  Award
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
  Cell,
  ScatterChart,
  Scatter
} from 'recharts'

const qualityTests = [
  {
    id: 'QT-2024-001',
    batchId: 'BATCH-A2847',
    productName: 'Steel Beams - Grade A',
    testType: 'Tensile Strength',
    testDate: '2024-02-28',
    inspector: 'Dr. Sarah Johnson',
    status: 'Passed',
    result: '450 MPa',
    requirement: '≥420 MPa',
    notes: 'Excellent quality, exceeds specifications',
    certificateId: 'CERT-001',
    nextTest: '2024-03-15'
  },
  {
    id: 'QT-2024-002',
    batchId: 'BATCH-B1245',
    productName: 'Steel Plates - Grade B',
    testType: 'Chemical Analysis',
    testDate: '2024-02-27',
    inspector: 'Michael Chen',
    status: 'Failed',
    result: 'Carbon: 0.25%',
    requirement: 'Carbon: ≤0.22%',
    notes: 'Carbon content exceeds limit, requires rework',
    certificateId: null,
    nextTest: '2024-03-01'
  },
  {
    id: 'QT-2024-003',
    batchId: 'BATCH-C0891',
    productName: 'Wire Rods',
    testType: 'Surface Quality',
    testDate: '2024-02-28',
    inspector: 'Lisa Wong',
    status: 'Pending',
    result: 'In Progress',
    requirement: 'No surface defects',
    notes: 'Visual inspection underway',
    certificateId: null,
    nextTest: null
  },
  {
    id: 'QT-2024-004',
    batchId: 'BATCH-D5623',
    productName: 'Steel Tubes',
    testType: 'Dimensional Check',
    testDate: '2024-02-26',
    inspector: 'Robert Davis',
    status: 'Rework',
    result: 'Diameter: 102.5mm',
    requirement: 'Diameter: 100±1mm',
    notes: 'Outer diameter slightly oversized',
    certificateId: null,
    nextTest: '2024-03-02'
  },
  {
    id: 'QT-2024-005',
    batchId: 'BATCH-E3456',
    productName: 'Galvanized Sheets',
    testType: 'Coating Thickness',
    testDate: '2024-02-25',
    inspector: 'Emma Thompson',
    status: 'Passed',
    result: '85 μm',
    requirement: '≥80 μm',
    notes: 'Coating within acceptable range',
    certificateId: 'CERT-002',
    nextTest: '2024-03-10'
  },
]

const qualityMetrics = [
  {
    metric: 'Overall Pass Rate',
    value: 94.2,
    target: 96.0,
    trend: '+1.2%',
    status: 'good'
  },
  {
    metric: 'First Time Pass Rate',
    value: 87.5,
    target: 90.0,
    trend: '+0.8%',
    status: 'warning'
  },
  {
    metric: 'Rework Rate',
    value: 8.3,
    target: 5.0,
    trend: '-0.5%',
    status: 'warning'
  },
  {
    metric: 'Rejection Rate',
    value: 4.2,
    target: 3.0,
    trend: '-0.3%',
    status: 'warning'
  }
]

const inspectors = [
  {
    id: 'INS-001',
    name: 'Dr. Sarah Johnson',
    specialization: 'Mechanical Testing',
    testsCompleted: 45,
    passRate: 96.7,
    certification: 'Level III NDT',
    availability: 'Available'
  },
  {
    id: 'INS-002',
    name: 'Michael Chen',
    specialization: 'Chemical Analysis',
    testsCompleted: 38,
    passRate: 89.5,
    certification: 'AWS CWI',
    availability: 'Busy'
  },
  {
    id: 'INS-003',
    name: 'Lisa Wong',
    specialization: 'Surface Quality',
    testsCompleted: 52,
    passRate: 94.2,
    certification: 'ASNT Level II',
    availability: 'Available'
  },
  {
    id: 'INS-004',
    name: 'Robert Davis',
    specialization: 'Dimensional Inspection',
    testsCompleted: 41,
    passRate: 92.7,
    certification: 'CMM Certified',
    availability: 'On Leave'
  },
]

function getStatusBadge(status: string) {
  switch (status) {
    case 'Passed':
      return <Badge className="bg-green-100 text-green-800">Passed</Badge>
    case 'Failed':
      return <Badge variant="destructive">Failed</Badge>
    case 'Pending':
      return <Badge className="bg-blue-100 text-blue-800">Pending</Badge>
    case 'Rework':
      return <Badge className="bg-orange-100 text-orange-800">Rework</Badge>
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}

function getAvailabilityBadge(status: string) {
  switch (status) {
    case 'Available':
      return <Badge className="bg-green-100 text-green-800">Available</Badge>
    case 'Busy':
      return <Badge className="bg-yellow-100 text-yellow-800">Busy</Badge>
    case 'On Leave':
      return <Badge variant="secondary">On Leave</Badge>
    default:
      return <Badge variant="outline">{status}</Badge>
  }
}

function getMetricIcon(status: string) {
  switch (status) {
    case 'good':
      return <CheckCircle className="h-4 w-4 text-green-500" />
    case 'warning':
      return <AlertTriangle className="h-4 w-4 text-yellow-500" />
    case 'critical':
      return <XCircle className="h-4 w-4 text-red-500" />
    default:
      return <BarChart3 className="h-4 w-4 text-muted-foreground" />
  }
}

export default function QualityPage() {
  // Sample data for quality charts
  const qualityTrends = [
    { date: '2024-02-20', passRate: 94.2, defectRate: 5.8, inspections: 145 },
    { date: '2024-02-21', passRate: 95.8, defectRate: 4.2, inspections: 152 },
    { date: '2024-02-22', passRate: 93.1, defectRate: 6.9, inspections: 138 },
    { date: '2024-02-23', passRate: 96.4, defectRate: 3.6, inspections: 167 },
    { date: '2024-02-24', passRate: 95.2, defectRate: 4.8, inspections: 159 },
    { date: '2024-02-25', passRate: 97.1, defectRate: 2.9, inspections: 143 },
    { date: '2024-02-26', passRate: 94.8, defectRate: 5.2, inspections: 154 }
  ]

  const defectCategories = [
    { category: 'Surface Defects', count: 23, percentage: 35 },
    { category: 'Dimensional', count: 18, percentage: 27 },
    { category: 'Chemical Composition', count: 12, percentage: 18 },
    { category: 'Mechanical Properties', count: 8, percentage: 12 },
    { category: 'Other', count: 5, percentage: 8 }
  ]

  const processCapability = [
    { process: 'Chemical Analysis', cpk: 1.45, target: 1.33, status: 'good' },
    { process: 'Dimensional Check', cpk: 1.28, target: 1.33, status: 'warning' },
    { process: 'Surface Inspection', cpk: 1.67, target: 1.33, status: 'excellent' },
    { process: 'Tensile Testing', cpk: 1.38, target: 1.33, status: 'good' }
  ]

  const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8']
  return (
    <DashboardLayout>
      <div className="space-y-6">
        {/* Header */}
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight flex items-center gap-2">
              <ShieldCheck className="w-8 h-8 text-primary" />
              Quality Assurance
            </h1>
            <p className="text-muted-foreground">
              Monitor quality control processes, test results, and compliance metrics
            </p>
          </div>
          <div className="flex items-center gap-2">
            <Button variant="outline" size="sm">
              <Download className="w-4 h-4 mr-2" />
              Export Reports
            </Button>
            <Button size="sm">
              <Plus className="w-4 h-4 mr-2" />
              New Test
            </Button>
          </div>
        </div>

        {/* Quality Metrics */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {qualityMetrics.map((metric, index) => (
            <Card key={index} className={`border-l-4 ${
              metric.status === 'good' ? 'border-l-green-500' :
              metric.status === 'warning' ? 'border-l-yellow-500' :
              'border-l-red-500'
            }`}>
              <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                <CardTitle className="text-sm font-medium">{metric.metric}</CardTitle>
                {getMetricIcon(metric.status)}
              </CardHeader>
              <CardContent>
                <div className="text-2xl font-bold">{metric.value}%</div>
                <div className="flex items-center justify-between">
                  <div className="flex items-center space-x-1">
                    <TrendingUp className="h-3 w-3 text-green-500" />
                    <p className="text-xs text-green-600">{metric.trend}</p>
                  </div>
                  <p className="text-xs text-muted-foreground">Target: {metric.target}%</p>
                </div>
                <Progress value={metric.value} className="mt-2 h-1" />
              </CardContent>
            </Card>
          ))}
        </div>

        {/* Quality Analytics */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5" />
                Quality Trends
              </CardTitle>
              <CardDescription>Daily quality metrics and inspection results</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={qualityTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="date" />
                    <YAxis yAxisId="rate" domain={[85, 100]} />
                    <YAxis yAxisId="count" orientation="right" domain={[0, 200]} />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + (name === 'inspections' ? ' tests' : '%'),
                        name === 'passRate' ? 'Pass Rate' : 
                        name === 'defectRate' ? 'Defect Rate' : 'Inspections'
                      ]}
                    />
                    <Area yAxisId="rate" type="monotone" dataKey="passRate" stroke="#10b981" fill="#10b981" fillOpacity={0.3} strokeWidth={2} />
                    <Line yAxisId="rate" type="monotone" dataKey="defectRate" stroke="#ef4444" strokeWidth={2} />
                    <Bar yAxisId="count" dataKey="inspections" fill="#3b82f6" opacity={0.7} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <AlertTriangle className="h-5 w-5" />
                Defect Analysis
              </CardTitle>
              <CardDescription>Distribution of defects by category</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <PieChart>
                    <Pie
                      data={defectCategories}
                      cx="50%"
                      cy="50%"
                      outerRadius={100}
                      fill="#8884d8"
                      dataKey="count"
                      label={({ category, percentage }) => `${category}: ${percentage}%`}
                    >
                      {defectCategories.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Pie>
                    <Tooltip formatter={(value) => [value, 'Defects']} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        <div className="grid gap-6 md:grid-cols-2">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Award className="h-5 w-5" />
                Process Capability (Cpk)
              </CardTitle>
              <CardDescription>Statistical process control metrics</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={processCapability}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="process" angle={-45} textAnchor="end" height={80} />
                    <YAxis domain={[1.0, 1.8]} />
                    <Tooltip 
                      formatter={(value, name) => [
                        value,
                        name === 'cpk' ? 'Current Cpk' : 'Target Cpk'
                      ]}
                    />
                    <Bar dataKey="target" fill="#e5e7eb" name="target" />
                    <Bar dataKey="cpk" name="cpk">
                      {processCapability.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={
                          entry.status === 'excellent' ? '#10b981' :
                          entry.status === 'good' ? '#3b82f6' :
                          '#f59e0b'
                        } />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5" />
                Quality Performance Matrix
              </CardTitle>
              <CardDescription>Correlation between inspection volume and quality</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <ScatterChart data={qualityTrends}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis type="number" dataKey="inspections" name="Inspections" domain={[130, 170]} />
                    <YAxis type="number" dataKey="passRate" name="Pass Rate" domain={[92, 98]} />
                    <Tooltip 
                      formatter={(value, name) => [
                        value + (name === 'Pass Rate' ? '%' : ' tests'),
                        name
                      ]}
                      labelFormatter={() => 'Quality vs Volume'}
                    />
                    <Scatter name="Daily Performance" dataKey="passRate" fill="#8884d8" />
                  </ScatterChart>
                </ResponsiveContainer>
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Main Content Tabs */}
        <Tabs defaultValue="tests" className="space-y-6">
          <TabsList className="grid w-full grid-cols-3">
            <TabsTrigger value="tests">Quality Tests</TabsTrigger>
            <TabsTrigger value="inspectors">Inspectors</TabsTrigger>
            <TabsTrigger value="compliance">Compliance</TabsTrigger>
          </TabsList>

          <TabsContent value="tests" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Quality Test Results</CardTitle>
                <CardDescription>
                  Track all quality tests, inspections, and compliance checks
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col sm:flex-row gap-4 mb-6">
                  <div className="flex-1">
                    <div className="relative">
                      <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />
                      <Input placeholder="Search tests..." className="pl-9" />
                    </div>
                  </div>
                  <Button variant="outline" size="sm">
                    Filter by Status
                  </Button>
                  <Button variant="outline" size="sm">
                    Filter by Product
                  </Button>
                </div>

                <div className="rounded-md border">
                  <Table>
                    <TableHeader>
                      <TableRow>
                        <TableHead>Test ID</TableHead>
                        <TableHead>Product & Batch</TableHead>
                        <TableHead>Test Type</TableHead>
                        <TableHead>Inspector</TableHead>
                        <TableHead>Results</TableHead>
                        <TableHead>Status</TableHead>
                        <TableHead>Date</TableHead>
                        <TableHead>Actions</TableHead>
                      </TableRow>
                    </TableHeader>
                    <TableBody>
                      {qualityTests.map((test) => (
                        <TableRow key={test.id} className="hover:bg-muted/50">
                          <TableCell className="font-medium">{test.id}</TableCell>
                          <TableCell>
                            <div>
                              <p className="font-medium">{test.productName}</p>
                              <p className="text-sm text-muted-foreground">Batch: {test.batchId}</p>
                            </div>
                          </TableCell>
                          <TableCell>{test.testType}</TableCell>
                          <TableCell>{test.inspector}</TableCell>
                          <TableCell>
                            <div>
                              <p className="text-sm font-medium">{test.result}</p>
                              <p className="text-xs text-muted-foreground">
                                Req: {test.requirement}
                              </p>
                            </div>
                          </TableCell>
                          <TableCell>{getStatusBadge(test.status)}</TableCell>
                          <TableCell>{test.testDate}</TableCell>
                          <TableCell>
                            <div className="flex items-center gap-1">
                              <Button variant="ghost" size="sm">
                                <FileText className="w-4 h-4" />
                              </Button>
                              {test.status === 'Failed' || test.status === 'Rework' ? (
                                <Button variant="ghost" size="sm">
                                  <RotateCcw className="w-4 h-4" />
                                </Button>
                              ) : null}
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

          <TabsContent value="inspectors" className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Quality Inspectors</CardTitle>
                <CardDescription>
                  Manage inspector assignments, certifications, and performance
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {inspectors.map((inspector) => (
                    <Card key={inspector.id} className="border hover:shadow-lg transition-shadow">
                      <CardHeader>
                        <CardTitle className="flex items-center justify-between">
                          <span>{inspector.name}</span>
                          {getAvailabilityBadge(inspector.availability)}
                        </CardTitle>
                        <CardDescription>{inspector.specialization}</CardDescription>
                      </CardHeader>
                      <CardContent className="space-y-4">
                        <div className="grid grid-cols-2 gap-4 text-sm">
                          <div>
                            <p className="text-muted-foreground">Tests Completed</p>
                            <p className="font-medium">{inspector.testsCompleted}</p>
                          </div>
                          <div>
                            <p className="text-muted-foreground">Pass Rate</p>
                            <p className="font-medium">{inspector.passRate}%</p>
                          </div>
                        </div>
                        
                        <div>
                          <p className="text-sm text-muted-foreground">Certification</p>
                          <p className="font-medium">{inspector.certification}</p>
                        </div>

                        <Progress value={inspector.passRate} className="h-2" />

                        <div className="flex gap-2">
                          <Button variant="outline" size="sm" className="flex-1">
                            View Profile
                          </Button>
                          <Button 
                            variant="outline" 
                            size="sm"
                            disabled={inspector.availability !== 'Available'}
                          >
                            Assign Test
                          </Button>
                        </div>
                      </CardContent>
                    </Card>
                  ))}
                </div>
              </CardContent>
            </Card>
          </TabsContent>

          <TabsContent value="compliance" className="space-y-6">
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <FileText className="w-5 h-5" />
                    Compliance Standards
                  </CardTitle>
                  <CardDescription>
                    Industry standards and certifications
                  </CardDescription>
                </CardHeader>
                <CardContent className="space-y-4">
                  {[
                    { standard: 'ASTM A36', status: 'Compliant', validity: '2024-12-31' },
                    { standard: 'ISO 9001:2015', status: 'Compliant', validity: '2024-11-15' },
                    { standard: 'AWS D1.1', status: 'Under Review', validity: '2024-06-30' },
                    { standard: 'API 5L', status: 'Compliant', validity: '2025-01-20' },
                  ].map((item, index) => (
                    <div key={index} className="flex items-center justify-between p-3 border rounded-lg">
                      <div>
                        <p className="font-medium">{item.standard}</p>
                        <p className="text-sm text-muted-foreground">Valid until: {item.validity}</p>
                      </div>
                      <Badge variant={item.status === 'Compliant' ? 'default' : 'secondary'}>
                        {item.status}
                      </Badge>
                    </div>
                  ))}
                </CardContent>
              </Card>

              <Card>
                <CardHeader>
                  <CardTitle className="flex items-center gap-2">
                    <BarChart3 className="w-5 h-5" />
                    Quality Trends
                  </CardTitle>
                  <CardDescription>
                    Quality metrics over time
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="text-center py-12 text-muted-foreground">
                    <BarChart3 className="w-12 h-12 mx-auto mb-4" />
                    <p>Quality trends chart coming soon...</p>
                  </div>
                </CardContent>
              </Card>
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </DashboardLayout>
  )
}