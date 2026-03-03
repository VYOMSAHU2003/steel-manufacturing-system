"use client"

import React, { createContext, useContext, useEffect, useState, useCallback } from 'react'
import { apiService } from '@/lib/api-service'

interface DataContextType {
  // Raw Materials
  rawMaterials: any[]
  loadRawMaterials: () => Promise<void>
  updateRawMaterial: (id: string, data: any) => Promise<void>

  // Production
  productionOrders: any[]
  loadProductionOrders: () => Promise<void>
  createProductionOrder: (data: any) => Promise<void>

  // Inventory
  inventoryItems: any[]
  loadInventoryItems: () => Promise<void>

  // Quality
  qualityTests: any[]
  loadQualityTests: () => Promise<void>
  createQualityTest: (data: any) => Promise<void>

  // Logistics
  shipments: any[]
  loadShipments: () => Promise<void>
  createShipment: (data: any) => Promise<void>

  // Dashboard
  dashboardMetrics: any
  loadDashboardMetrics: () => Promise<void>

  // Loading states
  isLoading: boolean
  refreshAll: () => Promise<void>
}

const DataContext = createContext<DataContextType | undefined>(undefined)

export function DataProvider({ children }: { children: React.ReactNode }) {
  const [rawMaterials, setRawMaterials] = useState<any[]>([])
  const [productionOrders, setProductionOrders] = useState<any[]>([])
  const [inventoryItems, setInventoryItems] = useState<any[]>([])
  const [qualityTests, setQualityTests] = useState<any[]>([])
  const [shipments, setShipments] = useState<any[]>([])
  const [dashboardMetrics, setDashboardMetrics] = useState<any>({})
  const [isLoading, setIsLoading] = useState(false)

  // Raw Materials
  const loadRawMaterials = useCallback(async () => {
    try {
      const data = await apiService.getRawMaterials()
      setRawMaterials(data || [])
    } catch (error) {
      console.error('Failed to load raw materials:', error)
    }
  }, [])

  const updateRawMaterial = useCallback(async (id: string, data: any) => {
    try {
      const updated = await apiService.updateRawMaterial(id, data)
      if (updated) {
        setRawMaterials(prev => prev.map(item => item.id === id ? { ...item, ...updated } : item))
      }
    } catch (error) {
      console.error('Failed to update raw material:', error)
    }
  }, [])

  // Production
  const loadProductionOrders = useCallback(async () => {
    try {
      const data = await apiService.getProductionOrders()
      setProductionOrders(data || [])
    } catch (error) {
      console.error('Failed to load production orders:', error)
    }
  }, [])

  const createProductionOrder = useCallback(async (data: any) => {
    try {
      const newOrder = await apiService.createProductionOrder(data)
      if (newOrder) {
        setProductionOrders(prev => [newOrder, ...prev])
      }
    } catch (error) {
      console.error('Failed to create production order:', error)
    }
  }, [])

  // Inventory
  const loadInventoryItems = useCallback(async () => {
    try {
      const data = await apiService.getInventoryItems()
      setInventoryItems(data || [])
    } catch (error) {
      console.error('Failed to load inventory items:', error)
    }
  }, [])

  // Quality
  const loadQualityTests = useCallback(async () => {
    try {
      const data = await apiService.getQualityTests()
      setQualityTests(data || [])
    } catch (error) {
      console.error('Failed to load quality tests:', error)
    }
  }, [])

  const createQualityTest = useCallback(async (data: any) => {
    try {
      const newTest = await apiService.createQualityTest(data)
      if (newTest) {
        setQualityTests(prev => [newTest, ...prev])
      }
    } catch (error) {
      console.error('Failed to create quality test:', error)
    }
  }, [])

  // Logistics
  const loadShipments = useCallback(async () => {
    try {
      const data = await apiService.getShipments()
      setShipments(data || [])
    } catch (error) {
      console.error('Failed to load shipments:', error)
    }
  }, [])

  const createShipment = useCallback(async (data: any) => {
    try {
      const newShipment = await apiService.createShipment(data)
      if (newShipment) {
        setShipments(prev => [newShipment, ...prev])
      }
    } catch (error) {
      console.error('Failed to create shipment:', error)
    }
  }, [])

  // Dashboard
  const loadDashboardMetrics = useCallback(async () => {
    try {
      const data = await apiService.getDashboardMetrics()
      setDashboardMetrics(data || {})
    } catch (error) {
      console.error('Failed to load dashboard metrics:', error)
    }
  }, [])

  // Refresh all data
  const refreshAll = useCallback(async () => {
    setIsLoading(true)
    try {
      await Promise.all([
        loadRawMaterials(),
        loadProductionOrders(),
        loadInventoryItems(),
        loadQualityTests(),
        loadShipments(),
        loadDashboardMetrics(),
      ])
    } finally {
      setIsLoading(false)
    }
  }, [
    loadRawMaterials,
    loadProductionOrders,
    loadInventoryItems,
    loadQualityTests,
    loadShipments,
    loadDashboardMetrics,
  ])

  // Initial data load
  useEffect(() => {
    refreshAll()
  }, [refreshAll])

  // Auto-refresh dashboard metrics every 30 seconds
  useEffect(() => {
    const interval = setInterval(loadDashboardMetrics, 30000)
    return () => clearInterval(interval)
  }, [loadDashboardMetrics])

  const value: DataContextType = {
    rawMaterials,
    loadRawMaterials,
    updateRawMaterial,
    productionOrders,
    loadProductionOrders,
    createProductionOrder,
    inventoryItems,
    loadInventoryItems,
    qualityTests,
    loadQualityTests,
    createQualityTest,
    shipments,
    loadShipments,
    createShipment,
    dashboardMetrics,
    loadDashboardMetrics,
    isLoading,
    refreshAll,
  }

  return <DataContext.Provider value={value}>{children}</DataContext.Provider>
}

export function useData() {
  const context = useContext(DataContext)
  if (context === undefined) {
    throw new Error('useData must be used within a DataProvider')
  }
  return context
}