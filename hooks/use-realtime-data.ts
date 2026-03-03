"use client"

import { useEffect, useState } from 'react'

// Real-time data streaming hook
export function useRealTimeData() {
  const [isConnected, setIsConnected] = useState(false)
  const [lastUpdate, setLastUpdate] = useState<Date | null>(null)

  useEffect(() => {
    // Attempt to connect to Streamlit backend for real-time updates
    const connectToStream = () => {
      try {
        // In a production environment, this would use WebSocket or Server-Sent Events
        // For now, we'll simulate real-time updates with polling
        const interval = setInterval(() => {
          // Simulate connection check
          fetch('http://localhost:8502/health')
            .then(() => {
              setIsConnected(true)
              setLastUpdate(new Date())
            })
            .catch(() => {
              setIsConnected(false)
            })
        }, 5000) // Check every 5 seconds

        return interval
      } catch (error) {
        console.error('Failed to connect to real-time stream:', error)
        return null
      }
    }

    const interval = connectToStream()
    
    return () => {
      if (interval) clearInterval(interval)
    }
  }, [])

  return { isConnected, lastUpdate }
}

// Production metrics streaming
export function useProductionMetrics() {
  const [metrics, setMetrics] = useState({
    efficiency: 89,
    output: 2847,
    quality: 94.2,
    activeLines: 4
  })

  useEffect(() => {
    const interval = setInterval(() => {
      // Simulate real-time production metrics updates
      setMetrics(prev => ({
        efficiency: prev.efficiency + (Math.random() - 0.5) * 2,
        output: prev.output + Math.floor(Math.random() * 10),
        quality: Math.min(100, Math.max(85, prev.quality + (Math.random() - 0.5) * 1.5)),
        activeLines: prev.activeLines
      }))
    }, 3000)

    return () => clearInterval(interval)
  }, [])

  return metrics
}

// Alert system
export function useAlertSystem() {
  const [alerts, setAlerts] = useState([
    { 
      id: 1,
      type: 'success', 
      message: 'Quality check passed - Batch #A2847', 
      time: new Date(Date.now() - 2 * 60 * 1000) // 2 minutes ago
    },
    { 
      id: 2,
      type: 'warning', 
      message: 'Low inventory alert - Iron ore', 
      time: new Date(Date.now() - 5 * 60 * 1000) // 5 minutes ago
    },
  ])

  const addAlert = (alert: { type: string; message: string }) => {
    const newAlert = {
      id: Date.now(),
      ...alert,
      time: new Date()
    }
    setAlerts(prev => [newAlert, ...prev.slice(0, 9)]) // Keep only 10 most recent
  }

  const removeAlert = (id: number) => {
    setAlerts(prev => prev.filter(alert => alert.id !== id))
  }

  // Simulate automatic alerts
  useEffect(() => {
    const interval = setInterval(() => {
      const alertTypes = ['info', 'warning', 'success']
      const messages = [
        'Production order completed successfully',
        'Quality inspection scheduled',
        'Maintenance reminder for Line 3',
        'New shipment dispatched',
        'Inventory level updated',
        'System backup completed'
      ]

      const randomType = alertTypes[Math.floor(Math.random() * alertTypes.length)]
      const randomMessage = messages[Math.floor(Math.random() * messages.length)]
      
      if (Math.random() < 0.3) { // 30% chance every 10 seconds
        addAlert({ type: randomType, message: randomMessage })
      }
    }, 10000)

    return () => clearInterval(interval)
  }, [])

  return { alerts, addAlert, removeAlert }
}