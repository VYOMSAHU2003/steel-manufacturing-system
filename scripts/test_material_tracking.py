"""
Test Script for Automatic Material Consumption Tracking
This script demonstrates the automatic low stock alert system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.database_models import RawMaterial, MaterialConsumption
from utils.material_tracking import MaterialTracker
from datetime import datetime, timedelta
import random

def test_consumption_tracking():
    """Test the automatic material consumption and alert system"""
    
    print("🧪 Testing Automatic Material Consumption Tracking System...")
    
    db = SessionLocal()
    tracker = MaterialTracker()
    
    try:
        # Get all available materials
        materials = db.query(RawMaterial).all()
        
        if not materials:
            print("❌ No materials found. Run add_sample_data.py first.")
            return
        
        print(f"📦 Found {len(materials)} materials in inventory")
        
        # Simulate material consumption for the last few days
        print("\n🔄 Simulating material consumption over last 7 days...")
        
        for i in range(7):  # Last 7 days
            date = datetime.utcnow() - timedelta(days=i)
            
            # Consume random materials each day
            for _ in range(random.randint(2, 5)):  # 2-5 consumption events per day
                material = random.choice(materials)
                
                # Only consume if material has enough stock
                if material.quantity_available > 1:
                    
                    # Random consumption between 1-10% of available stock
                    max_consume = min(material.quantity_available * 0.1, 50)
                    consume_amount = random.uniform(1, max_consume)
                    
                    consumption_type = random.choice(["production", "testing", "maintenance", "quality_check"])
                    
                    print(f"  📉 Consuming {consume_amount:.1f} {material.unit} of {material.material_name} on {date.strftime('%Y-%m-%d')}")
                    
                    # Create consumption record with specific date
                    consumption = MaterialConsumption(
                        material_id=material.material_id,
                        consumed_quantity=consume_amount,
                        consumption_type=consumption_type,
                        consumed_by=1,
                        notes=f"Simulated consumption for testing - {consumption_type}",
                        old_stock=material.quantity_available,
                        new_stock=material.quantity_available - consume_amount,
                        consumption_date=date,
                        created_at=date
                    )
                    
                    # Update material stock
                    material.quantity_available -= consume_amount
                    
                    db.add(consumption)
                    
                    # Manually check for alerts (since we're simulating past dates)
                    if material.quantity_available <= 5:
                        print(f"    🚨 CRITICAL ALERT: {material.material_name} is critically low! ({material.quantity_available:.1f} {material.unit})")
                    elif material.quantity_available <= 15:
                        print(f"    ⚠️ WARNING: {material.material_name} is running low! ({material.quantity_available:.1f} {material.unit})")
        
        db.commit()
        
        # Test direct material consumption through the tracker
        print("\n🎯 Testing Real-Time Consumption Tracking...")
        
        # Find a material with good stock for testing
        test_material = None
        for material in materials:
            if material.quantity_available > 20:
                test_material = material
                break
        
        if test_material:
            old_stock = test_material.quantity_available
            
            print(f"📋 Testing consumption of {test_material.material_name}")
            print(f"  Current stock: {old_stock:.1f} {test_material.unit}")
            
            # Consume material using the tracker
            result = tracker.consume_material(
                material_id=test_material.material_id,
                quantity=10.0,
                consumption_type="production",
                consumed_by=1,
                notes="Test consumption from script"
            )
            
            if result["success"]:
                print(f"  ✅ Successfully consumed 10.0 {test_material.unit}")
                print(f"  📊 New stock: {result['new_stock']:.1f} {test_material.unit}")
                print(f"  🆔 Consumption ID: {result['consumption_id']}")
            else:
                print(f"  ❌ Consumption failed: {result['message']}")
        
        # Check and display alerts
        print("\n🚨 Checking for Low Stock Alerts...")
        alerts = tracker.get_active_alerts()
        
        if alerts:
            print(f"📢 Found {len(alerts)} active alerts:")
            for alert in alerts:
                alert_emoji = "🔴" if alert.alert_type == "critical" else "🟡"
                print(f"  {alert_emoji} {alert.alert_type.upper()}: {alert.alert_message}")
        else:
            print("  ✅ No active alerts found")
        
        # Check reorder suggestions
        print("\n📋 Checking for Reorder Suggestions...")
        suggestions = tracker.get_reorder_suggestions()
        
        if suggestions:
            print(f"💡 Found {len(suggestions)} reorder suggestions:")
            for suggestion in suggestions:
                urgency_emoji = {"urgent": "🔴", "high": "🟠", "medium": "🟡", "low": "🟢"}
                emoji = urgency_emoji.get(suggestion.urgency_level, "⚪")
                print(f"  {emoji} {suggestion.urgency_level.upper()}: Order {suggestion.suggested_order_quantity:.0f} units in {suggestion.days_until_stockout} days")
        else:
            print("  ✅ No reorder suggestions at this time")
        
        # Show consumption summary
        print("\n📊 Consumption Summary (Last 7 days):")
        recent_consumptions = tracker.get_consumption_history(days=7)
        
        if recent_consumptions:
            total_consumed = sum(c.consumed_quantity for c in recent_consumptions)
            unique_materials = len(set(c.material_id for c in recent_consumptions))
            total_events = len(recent_consumptions)
            
            print(f"  📈 Total consumption events: {total_events}")
            print(f"  📦 Materials consumed: {unique_materials}")
            print(f"  ⚖️ Total quantity consumed: {total_consumed:.1f} units")
            
            # Show by consumption type
            type_summary = {}
            for consumption in recent_consumptions:
                cons_type = consumption.consumption_type
                if cons_type not in type_summary:
                    type_summary[cons_type] = 0
                type_summary[cons_type] += consumption.consumed_quantity
            
            print("  🏷️ Consumption by type:")
            for cons_type, quantity in type_summary.items():
                print(f"    • {cons_type.title()}: {quantity:.1f} units")
        
        print("\n🎉 Material Consumption Tracking Test Completed Successfully!")
        print("\n💡 Now visit the Raw Materials module → 'Consume Material' tab to see the interface")
        print("🚨 Check the sidebar for low stock alerts when you run the Streamlit app")
        
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    test_consumption_tracking()