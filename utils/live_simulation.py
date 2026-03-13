"""
Live Data Simulation Engine for Real-Time Steel Plant Demo

This module provides comprehensive live data simulation capabilities for demonstrating
real-time steel plant operations including material consumption, production updates,
quality events, and plant metrics updates.

Author: BSP Digital Team
Version: 1.0
"""

import time
import random
import threading
from datetime import datetime, timedelta
from typing import Dict, Any, List
from dataclasses import dataclass, asdict
import streamlit as st

# Global variables for simulation state
_simulation_thread = None
_simulation_active = False
_simulation_metrics = {
    "production_rate": 95.5,
    "furnace_temp": 1665,
    "power_status": "STABLE",
    "total_updates": 0,
    "last_update": None,
    "material_consumption": {},
    "quality_score": 98.2,
    "energy_consumption": 245,
    "safety_score": 99.8
}

@dataclass
class LiveMetrics:
    """Data class for holding live simulation metrics"""
    production_rate: float
    furnace_temp: int
    power_status: str
    total_updates: int
    last_update: str
    quality_score: float
    energy_consumption: float
    safety_score: float
    material_consumption: Dict[str, float]

class LiveDataSimulator:
    """
    Advanced Live Data Simulation Engine
    
    This class provides comprehensive real-time data simulation for steel plant operations.
    It runs in background threads and continuously updates plant metrics to demonstrate
    live system capabilities.
    """
    
    def __init__(self, update_interval: int = 60):
        """
        Initialize the live data simulator
        
        Args:
            update_interval: Time in seconds between updates (default: 60 seconds)
        """
        self.update_interval = update_interval
        self.is_running = False
        self.thread = None
        self.metrics = _simulation_metrics.copy()
        
        # Material list for consumption simulation
        self.materials = [
            "Iron Ore", "Coal", "Limestone", "Scrap Steel", 
            "Flux", "Alloys", "Refractory Materials", "Oxygen"
        ]
        
        print(f"🔧 LiveDataSimulator initialized with {update_interval}s intervals")
    
    def start_simulation(self):
        """Start the background simulation thread"""
        if not self.is_running:
            self.is_running = True
            self.thread = threading.Thread(target=self._simulation_loop, daemon=True)
            self.thread.start()
            print("🟢 Live data simulation started")
            return True
        else:
            print("⚠️ Simulation already running")
            return False
    
    def stop_simulation(self):
        """Stop the simulation thread"""
        if self.is_running:
            self.is_running = False
            if self.thread and self.thread.is_alive():
                self.thread.join(timeout=5)
            print("🔴 Live data simulation stopped")
            return True
        else:
            print("ℹ️ Simulation was not running")
            return False
    
    def _simulation_loop(self):
        """Main simulation loop that runs in background"""
        print("🔄 Starting simulation loop...")
        
        while self.is_running:
            try:
                # Update all metrics
                self._update_production_metrics()
                self._update_material_consumption()
                self._update_quality_metrics() 
                self._update_energy_metrics()
                self._update_plant_metrics()
                
                # Update global metrics
                global _simulation_metrics
                _simulation_metrics.update(self.metrics)
                _simulation_metrics["total_updates"] += 1
                _simulation_metrics["last_update"] = datetime.now().isoformat()
                
                print(f"📊 Simulation update #{_simulation_metrics['total_updates']} at {datetime.now().strftime('%H:%M:%S')}")
                
                # Wait for next update
                time.sleep(self.update_interval)
                
            except Exception as e:
                print(f"❌ Error in simulation loop: {e}")
                time.sleep(5)  # Wait before retrying
    
    def _update_production_metrics(self):
        """Update production-related metrics"""
        # Production rate varies between 88% and 98%
        current_rate = self.metrics["production_rate"]
        change = random.uniform(-2, 2)
        new_rate = max(88, min(98, current_rate + change))
        self.metrics["production_rate"] = round(new_rate, 1)
        
        # Furnace temperature varies between 1620°C and 1700°C
        current_temp = self.metrics["furnace_temp"]
        temp_change = random.randint(-15, 15)
        new_temp = max(1620, min(1700, current_temp + temp_change))
        self.metrics["furnace_temp"] = new_temp
        
        # Power status simulation
        if random.random() < 0.95:  # 95% chance of stable power
            self.metrics["power_status"] = "STABLE"
        elif random.random() < 0.03:  # 3% chance of fluctuation
            self.metrics["power_status"] = "FLUCTUATING"
        else:  # 2% chance of backup
            self.metrics["power_status"] = "BACKUP"
    
    def _update_material_consumption(self):
        """Update material consumption simulation"""
        consumption = {}
        
        for material in self.materials:
            # Base consumption rates (tons per hour)
            base_rates = {
                "Iron Ore": (80, 120),
                "Coal": (60, 90),
                "Limestone": (15, 25),
                "Scrap Steel": (20, 40),
                "Flux": (5, 15),
                "Alloys": (2, 8),
                "Refractory Materials": (1, 5),
                "Oxygen": (30, 50)
            }
            
            min_rate, max_rate = base_rates.get(material, (10, 50))
            
            # Add production rate influence
            prod_influence = (self.metrics["production_rate"] - 90) / 10
            adjusted_max = max_rate * (1 + prod_influence * 0.1)
            adjusted_min = min_rate * (1 + prod_influence * 0.05)
            
            current_consumption = random.uniform(adjusted_min, adjusted_max)
            consumption[material] = round(current_consumption, 2)
        
        self.metrics["material_consumption"] = consumption
    
    def _update_quality_metrics(self):
        """Update quality-related metrics"""
        # Quality score varies between 96% and 99.5%
        current_quality = self.metrics["quality_score"]
        quality_change = random.uniform(-0.5, 0.3)  # Slight bias towards improvements
        new_quality = max(96.0, min(99.5, current_quality + quality_change))
        self.metrics["quality_score"] = round(new_quality, 1)
    
    def _update_energy_metrics(self):
        """Update energy consumption metrics"""
        # Energy consumption varies between 220 MW and 270 MW
        current_energy = self.metrics["energy_consumption"]
        energy_change = random.uniform(-10, 8)
        
        # Energy correlates with production rate
        prod_factor = self.metrics["production_rate"] / 95.0
        base_energy = 245 * prod_factor
        
        new_energy = max(220, min(270, base_energy + energy_change))
        self.metrics["energy_consumption"] = round(new_energy, 1)
    
    def _update_plant_metrics(self):
        """Update general plant metrics"""
        # Safety score should generally be very high
        current_safety = self.metrics["safety_score"]
        safety_change = random.uniform(-0.1, 0.05)  # Rare decreases
        new_safety = max(98.5, min(100.0, current_safety + safety_change))
        self.metrics["safety_score"] = round(new_safety, 1)
    
    def get_current_metrics(self) -> LiveMetrics:
        """Get current simulation metrics"""
        return LiveMetrics(
            production_rate=self.metrics["production_rate"],
            furnace_temp=self.metrics["furnace_temp"],
            power_status=self.metrics["power_status"],
            total_updates=_simulation_metrics["total_updates"],
            last_update=_simulation_metrics.get("last_update", ""),
            quality_score=self.metrics["quality_score"],
            energy_consumption=self.metrics["energy_consumption"],
            safety_score=self.metrics["safety_score"],
            material_consumption=self.metrics["material_consumption"]
        )
    
    def simulate_material_usage(self, material_name: str, quantity_used: float):
        """Simulate specific material usage event"""
        if "material_events" not in self.metrics:
            self.metrics["material_events"] = []
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "material": material_name,
            "quantity_used": quantity_used,
            "event_type": "consumption"
        }
        
        self.metrics["material_events"].append(event)
        print(f"📦 Material event: {quantity_used}t of {material_name} consumed")
    
    def simulate_quality_event(self, defect_type: str, severity: str):
        """Simulate a quality control event"""
        if "quality_events" not in self.metrics:
            self.metrics["quality_events"] = []
        
        event = {
            "timestamp": datetime.now().isoformat(),
            "defect_type": defect_type,
            "severity": severity,
            "event_type": "quality_issue"
        }
        
        self.metrics["quality_events"].append(event)
        
        # Temporarily adjust quality score based on severity
        if severity == "critical":
            self.metrics["quality_score"] = max(95, self.metrics["quality_score"] - 1.5)
        elif severity == "major":
            self.metrics["quality_score"] = max(96, self.metrics["quality_score"] - 0.8)
        else:
            self.metrics["quality_score"] = max(97, self.metrics["quality_score"] - 0.3)
        
        print(f"⚠️ Quality event: {defect_type} ({severity})")
    
    def get_simulation_status(self) -> Dict[str, Any]:
        """Get comprehensive simulation status"""
        return {
            "is_running": self.is_running,
            "update_interval": self.update_interval,
            "total_updates": _simulation_metrics["total_updates"],
            "last_update": _simulation_metrics.get("last_update"),
            "thread_active": self.thread.is_alive() if self.thread else False,
            "metrics_count": len(self.metrics)
        }

# Global simulator instance
_global_simulator = None

def initialize_live_simulation():
    """Initialize the global live simulation system"""
    global _global_simulator, _simulation_active
    
    if 'live_simulation_initialized' not in st.session_state:
        st.session_state.live_simulation_initialized = True
        
        if _global_simulator is None:
            _global_simulator = LiveDataSimulator(update_interval=60)
            print("🚀 Initializing live simulation system...")
        
        if not _simulation_active:
            success = _global_simulator.start_simulation()
            if success:
                _simulation_active = True
                print("✅ Live simulation system activated")
            else:
                print("❌ Failed to start live simulation")
    
    return _global_simulator

def start_background_simulation():
    """Start the background simulation (simplified interface)"""
    return initialize_live_simulation()

def get_live_metrics() -> Dict[str, Any]:
    """
    Get current live metrics from the simulation
    
    Returns:
        Dictionary containing current live metrics
    """
    global _global_simulator, _simulation_metrics
    
    # Ensure simulator is initialized
    if _global_simulator is None:
        initialize_live_simulation()
    
    # Return current metrics
    return _simulation_metrics.copy()

def stop_live_simulation():
    """Stop the live simulation system"""
    global _global_simulator, _simulation_active
    
    if _global_simulator and _simulation_active:
        _global_simulator.stop_simulation()
        _simulation_active = False
        print("🛑 Live simulation stopped")

def get_material_consumption_data() -> Dict[str, float]:
    """Get current material consumption rates"""
    metrics = get_live_metrics()
    return metrics.get("material_consumption", {})

def simulate_manual_event(event_type: str, **kwargs):
    """Trigger a manual simulation event"""
    global _global_simulator
    
    if _global_simulator:
        if event_type == "material_usage":
            _global_simulator.simulate_material_usage(
                kwargs.get("material_name", "Unknown"),
                kwargs.get("quantity", 0)
            )
        elif event_type == "quality_event":
            _global_simulator.simulate_quality_event(
                kwargs.get("defect_type", "Unknown"),
                kwargs.get("severity", "minor")
            )
        
        print(f"🎯 Manual event triggered: {event_type}")

def get_simulation_dashboard_data() -> Dict[str, Any]:
    """Get comprehensive data for simulation dashboard"""
    metrics = get_live_metrics()
    
    # Calculate additional derived metrics
    efficiency_score = (
        metrics.get("production_rate", 95) * 0.4 +
        metrics.get("quality_score", 98) * 0.3 +
        metrics.get("safety_score", 99) * 0.3
    )
    
    # Determine overall plant health
    if efficiency_score >= 97:
        plant_health = "EXCELLENT"
        health_color = "#00b894"
    elif efficiency_score >= 94:
        plant_health = "GOOD"
        health_color = "#fdcb6e"
    elif efficiency_score >= 90:
        plant_health = "FAIR"
        health_color = "#e17055"
    else:
        plant_health = "NEEDS_ATTENTION"
        health_color = "#e74c3c"
    
    return {
        "metrics": metrics,
        "efficiency_score": round(efficiency_score, 1),
        "plant_health": plant_health,
        "health_color": health_color,
        "total_updates": metrics.get("total_updates", 0),
        "simulation_active": _simulation_active,
        "last_update": metrics.get("last_update")
    }

# Utility functions for integration
def create_live_chart_data(metric_name: str, hours: int = 24) -> List[Dict]:
    """Generate live chart data for visualization"""
    current_value = get_live_metrics().get(metric_name, 100)
    
    data = []
    for i in range(hours):
        # Simulate some variation around current value
        variation = random.uniform(-5, 5)
        value = max(0, current_value + variation)
        
        timestamp = datetime.now() - timedelta(hours=hours-i)
        data.append({
            "timestamp": timestamp.strftime("%H:%M"),
            "value": round(value, 2),
            "hour": i
        })
    
    return data

def get_alert_level() -> str:
    """Determine current alert level based on live metrics"""
    metrics = get_live_metrics()
    
    production_rate = metrics.get("production_rate", 95)
    quality_score = metrics.get("quality_score", 98)
    safety_score = metrics.get("safety_score", 99)
    
    critical_conditions = [
        production_rate < 85,
        quality_score < 95,
        safety_score < 98
    ]
    
    warning_conditions = [
        production_rate < 92,
        quality_score < 97,
        safety_score < 99.5
    ]
    
    if any(critical_conditions):
        return "CRITICAL"
    elif any(warning_conditions):
        return "WARNING"
    else:
        return "NORMAL"

# Context manager for simulation control
class SimulationContext:
    """Context manager for controlled simulation sessions"""
    
    def __init__(self, auto_start=True):
        self.auto_start = auto_start
        self.simulator = None
    
    def __enter__(self):
        if self.auto_start:
            self.simulator = initialize_live_simulation()
        return self.simulator
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            print(f"⚠️ Simulation context error: {exc_val}")
        return False

# Enhanced debugging and monitoring
def print_simulation_status():
    """Print comprehensive simulation status for debugging"""
    global _global_simulator, _simulation_active
    
    print("\n" + "="*60)
    print("🔍 LIVE SIMULATION STATUS REPORT")
    print("="*60)
    
    print(f"Global Simulator: {'✅ Active' if _global_simulator else '❌ Not initialized'}")
    print(f"Simulation Active: {'✅ Yes' if _simulation_active else '❌ No'}")
    
    if _global_simulator:
        status = _global_simulator.get_simulation_status()
        print(f"Thread Running: {'✅ Yes' if status['is_running'] else '❌ No'}")
        print(f"Update Interval: {status['update_interval']} seconds")
        print(f"Total Updates: {status['total_updates']}")
        print(f"Last Update: {status['last_update']}")
    
    metrics = get_live_metrics()
    print(f"\nCurrent Metrics:")
    print(f"  🏭 Production Rate: {metrics.get('production_rate', 'N/A')}%")
    print(f"  🌡️ Furnace Temp: {metrics.get('furnace_temp', 'N/A')}°C")
    print(f"  ⚡ Power Status: {metrics.get('power_status', 'N/A')}")
    print(f"  ✅ Quality Score: {metrics.get('quality_score', 'N/A')}%")
    
    alert_level = get_alert_level()
    print(f"\nAlert Level: {alert_level}")
    
    print("="*60 + "\n")

if __name__ == "__main__":
    # Demo/testing mode
    print("🧪 Live Simulation Engine - Test Mode")
    
    simulator = LiveDataSimulator(update_interval=5)  # 5 second intervals for testing
    
    try:
        print("Starting simulation...")
        simulator.start_simulation()
        
        # Run for 30 seconds
        time.sleep(30)
        
        print("\nGetting current metrics...")
        metrics = simulator.get_current_metrics()
        print(f"Production Rate: {metrics.production_rate}%")
        print(f"Furnace Temperature: {metrics.furnace_temp}°C")
        print(f"Quality Score: {metrics.quality_score}%")
        
        print("\nTriggering test events...")
        simulator.simulate_material_usage("Iron Ore", 150.5)
        simulator.simulate_quality_event("Surface Defect", "minor")
        
        print("\nStopping simulation...")
        simulator.stop_simulation()
        
        print("✅ Test completed successfully")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        simulator.stop_simulation()