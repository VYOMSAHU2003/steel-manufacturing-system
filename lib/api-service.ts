// API Service to connect Frontend with Backend
class ApiService {
  private baseUrl = 'http://localhost:8502'  // Streamlit backend URL

  // Authentication endpoints
  async authenticate(username: string, password: string) {
    try {
      // In a real implementation, this would call your backend auth API
      // For now, we'll use local authentication with predefined users
      const response = await fetch(`${this.baseUrl}/api/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      }).catch(() => {
        // If backend is not available, use local auth
        return null
      })

      if (response && response.ok) {
        return await response.json()
      }

      // Fallback to local auth
      const defaultUsers = [
        { username: 'admin', password: 'admin123', role: 'admin' },
        { username: 'manager', password: 'manager123', role: 'manager' },
        { username: 'operator', password: 'operator123', role: 'operator' },
        { username: 'quality', password: 'quality123', role: 'quality' },
      ]

      const user = defaultUsers.find(u => u.username === username && u.password === password)
      return user || null
    } catch (error) {
      console.error('Authentication error:', error)
      return null
    }
  }

  // Raw Materials API
  async getRawMaterials() {
    try {
      const response = await fetch(`${this.baseUrl}/api/raw-materials`)
      if (response.ok) {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          return await response.json()
        }
        // If response is not JSON, fall back to mock data
        console.log('Backend returned non-JSON response, using mock data')
        return this.getMockRawMaterials()
      }
    } catch (error) {
      console.log('Failed to fetch raw materials from backend, using mock data:', error)
    }

    // Return mock data if backend unavailable
    return this.getMockRawMaterials()
  }

  async updateRawMaterial(id: string, data: any) {
    try {
      const response = await fetch(`${this.baseUrl}/api/raw-materials/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data),
      })
      return response.ok ? await response.json() : null
    } catch (error) {
      console.error('Failed to update raw material:', error)
      return null
    }
  }

  // Production API
  async getProductionOrders() {
    try {
      const response = await fetch(`${this.baseUrl}/api/production/orders`)
      if (response.ok) {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          return await response.json()
        }
        console.log('Backend returned non-JSON response, using mock data')
        return this.getMockProductionOrders()
      }
    } catch (error) {
      console.log('Failed to fetch production orders from backend, using mock data:', error)
    }

    return this.getMockProductionOrders()
  }

  async createProductionOrder(orderData: any) {
    try {
      const response = await fetch(`${this.baseUrl}/api/production/orders`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(orderData),
      })
      return response.ok ? await response.json() : null
    } catch (error) {
      console.error('Failed to create production order:', error)
      return null
    }
  }

  // Inventory API
  async getInventoryItems() {
    try {
      const response = await fetch(`${this.baseUrl}/api/inventory`)
      if (response.ok) {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          return await response.json()
        }
        console.log('Backend returned non-JSON response, using mock data')
        return this.getMockInventoryItems()
      }
    } catch (error) {
      console.log('Failed to fetch inventory from backend, using mock data:', error)
    }

    return this.getMockInventoryItems()
  }

  // Quality API
  async getQualityTests() {
    try {
      const response = await fetch(`${this.baseUrl}/api/quality/tests`)
      if (response.ok) {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          return await response.json()
        }
        console.log('Backend returned non-JSON response, using mock data')
        return this.getMockQualityTests()
      }
    } catch (error) {
      console.log('Failed to fetch quality tests from backend, using mock data:', error)
    }

    return this.getMockQualityTests()
  }

  async createQualityTest(testData: any) {
    try {
      const response = await fetch(`${this.baseUrl}/api/quality/tests`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData),
      })
      return response.ok ? await response.json() : null
    } catch (error) {
      console.error('Failed to create quality test:', error)
      return null
    }
  }

  // Logistics API
  async getShipments() {
    try {
      const response = await fetch(`${this.baseUrl}/api/logistics/shipments`)
      if (response.ok) {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          return await response.json()
        }
        console.log('Backend returned non-JSON response, using mock data')
        return this.getMockShipments()
      }
    } catch (error) {
      console.log('Failed to fetch shipments from backend, using mock data:', error)
    }

    return this.getMockShipments()
  }

  async createShipment(shipmentData: any) {
    try {
      const response = await fetch(`${this.baseUrl}/api/logistics/shipments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(shipmentData),
      })
      return response.ok ? await response.json() : null
    } catch (error) {
      console.error('Failed to create shipment:', error)
      return null
    }
  }

  // Real-time updates
  async getDashboardMetrics() {
    try {
      const response = await fetch(`${this.baseUrl}/api/dashboard/metrics`)
      if (response.ok) {
        const contentType = response.headers.get('content-type')
        if (contentType && contentType.includes('application/json')) {
          return await response.json()
        }
        console.log('Backend returned non-JSON response, using mock data')
        return this.getMockDashboardMetrics()
      }
    } catch (error) {
      console.log('Failed to fetch dashboard metrics from backend, using mock data:', error)
    }

    return this.getMockDashboardMetrics()
  }

  // Mock data methods (fallbacks when backend unavailable)
  private getMockRawMaterials() {
    return [
      {
        id: 'RM001',
        name: 'Iron Ore',
        category: 'Primary Material',
        currentStock: 1500,
        minimumStock: 500,
        unit: 'tons',
        supplier: 'Mining Corp Ltd',
        status: 'Good Stock',
        lastUpdated: new Date().toISOString(),
        costPerUnit: 85.50
      },
      {
        id: 'RM002',
        name: 'Coal',
        category: 'Fuel',
        currentStock: 800,
        minimumStock: 300,
        unit: 'tons',
        supplier: 'Coal Industries Inc',
        status: 'Good Stock',
        lastUpdated: new Date().toISOString(),
        costPerUnit: 120.00
      },
      {
        id: 'RM003',
        name: 'Limestone',
        category: 'Flux',
        currentStock: 450,
        minimumStock: 600,
        unit: 'tons',
        supplier: 'Quarry Solutions Ltd',
        status: 'Low Stock',
        lastUpdated: new Date().toISOString(),
        costPerUnit: 45.75
      },
      {
        id: 'RM004',
        name: 'Scrap Metal',
        category: 'Recycled Material',
        currentStock: 1200,
        minimumStock: 400,
        unit: 'tons',
        supplier: 'MetalRecycle Co',
        status: 'Good Stock',
        lastUpdated: new Date().toISOString(),
        costPerUnit: 340.00
      }
    ]
  }

  private getMockProductionOrders() {
    return [
      {
        id: 'PO-2024-001',
        product: 'Steel Beams - Grade A',
        productCode: 'SB-GA-001',
        quantity: 500,
        status: 'In Progress',
        progress: 65,
        startDate: '2024-02-25',
        expectedEndDate: '2024-03-10',
        priority: 'High',
        line: 'Production Line 1',
        orderValue: 125000,
        customer: 'Construction Corp Ltd'
      },
      {
        id: 'PO-2024-002',
        product: 'Steel Sheets - Standard',
        productCode: 'SS-STD-002',
        quantity: 200,
        status: 'Completed',
        progress: 100,
        startDate: '2024-02-20',
        expectedEndDate: '2024-02-28',
        priority: 'Medium',
        line: 'Production Line 2',
        orderValue: 85000,
        customer: 'Manufacturing Inc'
      },
      {
        id: 'PO-2024-003',
        product: 'Steel Rods - Heavy Duty',
        productCode: 'SR-HD-003',
        quantity: 1000,
        status: 'Planned',
        progress: 0,
        startDate: '2024-03-05',
        expectedEndDate: '2024-03-20',
        priority: 'Medium',
        line: 'Production Line 3',
        orderValue: 180000,
        customer: 'Infrastructure Ltd'
      }
    ]
  }

  private getMockInventoryItems() {
    return [
      {
        id: 'INV-001',
        name: 'Steel Beams - A Grade',
        category: 'Finished Goods',
        currentStock: 150,
        availableStock: 120,
        reservedStock: 30,
        status: 'Good Stock',
        location: 'Warehouse A',
        unitCost: 250.00,
        totalValue: 37500,
        lastMovement: '2024-02-27'
      },
      {
        id: 'INV-002',
        name: 'Steel Sheets - Standard',
        category: 'Finished Goods',
        currentStock: 85,
        availableStock: 85,
        reservedStock: 0,
        status: 'Good Stock',
        location: 'Warehouse B',
        unitCost: 425.00,
        totalValue: 36125,
        lastMovement: '2024-02-26'
      },
      {
        id: 'INV-003',
        name: 'Steel Rods - Heavy Duty',
        category: 'Finished Goods',
        currentStock: 25,
        availableStock: 15,
        reservedStock: 10,
        status: 'Low Stock',
        location: 'Warehouse A',
        unitCost: 180.00,
        totalValue: 4500,
        lastMovement: '2024-02-28'
      }
    ]
  }

  private getMockQualityTests() {
    return [
      {
        id: 'QT-2024-001',
        productName: 'Steel Beams - Grade A',
        testType: 'Tensile Strength',
        status: 'Passed',
        result: '520 MPa',
        specification: '≥ 500 MPa',
        inspector: 'Dr. Sarah Johnson',
        testDate: '2024-02-28',
        batchNumber: 'B2024-045',
        compliance: 'ISO 3581'
      },
      {
        id: 'QT-2024-002',
        productName: 'Steel Sheets - Standard',
        testType: 'Chemical Composition',
        status: 'Passed',
        result: 'C: 0.18%, Mn: 1.2%',
        specification: 'C ≤ 0.2%, Mn ≤ 1.5%',
        inspector: 'James Anderson',
        testDate: '2024-02-27',
        batchNumber: 'B2024-044',
        compliance: 'ASTM A36'
      },
      {
        id: 'QT-2024-003',
        productName: 'Steel Rods - Heavy Duty',
        testType: 'Hardness Test',
        status: 'Failed',
        result: '180 HB',
        specification: '≥ 200 HB',
        inspector: 'Emma Wilson',
        testDate: '2024-02-28',
        batchNumber: 'B2024-046',
        compliance: 'ISO 6506'
      }
    ]
  }

  private getMockShipments() {
    return [
      {
        id: 'SH-2024-001',
        customer: 'ABC Construction Ltd.',
        product: 'Steel Beams - Grade A',
        quantity: 150,
        status: 'In Transit',
        progress: 65,
        shipDate: '2024-02-26',
        expectedDelivery: '2024-03-02',
        carrier: 'Heavy Transport Co',
        trackingNumber: 'HTC-789456123',
        destination: 'New York, NY',
        value: 37500
      },
      {
        id: 'SH-2024-002',
        customer: 'XYZ Manufacturing Inc.',
        product: 'Steel Sheets - Standard',
        quantity: 85,
        status: 'Delivered',
        progress: 100,
        shipDate: '2024-02-24',
        expectedDelivery: '2024-02-27',
        carrier: 'Logistics Express',
        trackingNumber: 'LE-456789321',
        destination: 'Chicago, IL',
        value: 36125
      },
      {
        id: 'SH-2024-003',
        customer: 'Steel Works Corp.',
        product: 'Steel Rods - Heavy Duty',
        quantity: 10,
        status: 'Preparing',
        progress: 15,
        shipDate: '2024-03-01',
        expectedDelivery: '2024-03-05',
        carrier: 'Freight Masters',
        trackingNumber: 'FM-654321789',
        destination: 'Los Angeles, CA',
        value: 1800
      }
    ]
  }

  private getMockDashboardMetrics() {
    return {
      productionOutput: { value: 2847, unit: 'tons', change: '+12%' },
      inventoryStatus: { value: 1245, status: 'Optimal' },
      qualityScore: { value: 94.2, target: 96.0 },
      activeOrders: { value: 47, onTime: 92 },
      alerts: [
        { type: 'success', message: 'Quality check passed - Batch #A2847', time: '2 min ago' },
        { type: 'warning', message: 'Low inventory alert - Iron ore', time: '5 min ago' },
        { type: 'info', message: 'Production line 2 maintenance scheduled', time: '10 min ago' },
        { type: 'error', message: 'Quality test failed - Batch #B2846', time: '15 min ago' }
      ],
      // Additional chart data
      productionTrends: [
        { month: 'Feb 20', output: 2400, target: 2500 },
        { month: 'Feb 21', output: 2500, target: 2500 },
        { month: 'Feb 22', output: 2300, target: 2500 },
        { month: 'Feb 23', output: 2780, target: 2500 },
        { month: 'Feb 24', output: 2650, target: 2500 },
        { month: 'Feb 25', output: 2890, target: 2500 },
        { month: 'Feb 26', output: 2847, target: 2500 }
      ],
      equipmentEfficiency: [
        { equipment: 'Blast Furnace 1', efficiency: 94.2 },
        { equipment: 'Blast Furnace 2', efficiency: 87.8 },
        { equipment: 'Rolling Mill 1', efficiency: 91.5 },
        { equipment: 'Rolling Mill 2', efficiency: 89.3 },
        { equipment: 'Quality Station', efficiency: 96.1 }
      ],
      qualityMetrics: [
        { test: 'Tensile', passed: 92, failed: 8 },
        { test: 'Chemical', passed: 95, failed: 5 },
        { test: 'Hardness', passed: 88, failed: 12 },
        { test: 'Surface', passed: 97, failed: 3 }
      ]
    }
  }
}

export const apiService = new ApiService()