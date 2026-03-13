"""
Create Materials with Low Stock to Trigger Alert System
This demonstrates the automatic low stock notification system
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.database_models import RawMaterial, MaterialStatus, MaterialConsumption
from utils.material_tracking import MaterialTracker
from datetime import datetime, timedelta

def create_low_stock_scenario():
    """Create materials with low stock to trigger alerts"""
    
    print("🚨 Creating Low Stock Alert Scenario...")
    
    db = SessionLocal()
    tracker = MaterialTracker()
    
    try:
        # Update existing materials to have low stock
        materials_to_update = [
            ("Iron Ore", 2.5),          # Critical level (below 5)
            ("Coal", 3.8),              # Critical level 
            ("Limestone", 4.2),         # Critical level
            ("Flux Powder", 8.5),       # Warning level (below 15)
            ("Chromium", 12.0),         # Warning level
        ]
        
        print("📉 Setting materials to low stock levels...")
        
        for material_name, new_stock in materials_to_update:
            material = db.query(RawMaterial).filter(
                RawMaterial.material_name.ilike(f"%{material_name}%")
            ).first()
            
            if material:
                old_stock = material.quantity_available
                material.quantity_available = new_stock
                
                print(f"  ⚠️  {material_name}: {old_stock:.1f} → {new_stock:.1f} {material.unit}")
                
                # Force check for low stock alerts
                tracker._check_low_stock_alert(material)
        
        db.commit()
        
        # Add some critical materials with very low stock
        critical_materials = [
            {
                "material_name": "Emergency Iron Ore Reserve",
                "material_type": "Iron Ore",
                "supplier": "Emergency Supplier",
                "quantity_available": 1.2,  # Critical!
                "unit": "tons",
                "cost_per_unit": 12000.0,
                "batch_number": "EMRG-001",
                "status": MaterialStatus.AVAILABLE
            },
            {
                "material_name": "Critical Coal Reserve",
                "material_type": "Coal",
                "supplier": "Emergency Supplier",
                "quantity_available": 0.8,  # Very critical!
                "unit": "tons",
                "cost_per_unit": 8500.0,
                "batch_number": "EMRG-002",
                "status": MaterialStatus.AVAILABLE
            }
        ]
        
        print("🚨 Adding critical emergency materials...")
        
        for material_data in critical_materials:
            # Check if already exists
            existing = db.query(RawMaterial).filter(
                RawMaterial.material_name == material_data["material_name"]
            ).first()
            
            if not existing:
                material = RawMaterial(**material_data)
                db.add(material)
                db.commit()
                
                print(f"  🔴 Added: {material.material_name} ({material.quantity_available} {material.unit})")
                
                # Generate alert for this critical material
                tracker._check_low_stock_alert(material)
        
        # Create some recent consumption to trigger reorder suggestions
        print("📊 Creating recent consumption patterns...")
        
        materials = db.query(RawMaterial).all()
        for material in materials[:5]:  # First 5 materials
            if material.quantity_available > 5:  # Only if not already critical
                
                # Create consumption over last few days
                for days_ago in range(1, 4):  # Last 3 days
                    consumption_date = datetime.utcnow() - timedelta(days=days_ago)
                    
                    # Consume 5-15% of current stock per day to simulate heavy usage
                    consume_amount = material.quantity_available * 0.1
                    
                    if consume_amount > 0.1:
                        consumption = MaterialConsumption(
                            material_id=material.material_id,
                            consumed_quantity=consume_amount,
                            consumption_type="production",
                            consumed_by=1,
                            notes=f"Heavy production usage - Day {days_ago}",
                            old_stock=material.quantity_available + consume_amount,
                            new_stock=material.quantity_available,
                            consumption_date=consumption_date,
                            created_at=consumption_date
                        )
                        
                        db.add(consumption)
        
        db.commit()
        
        # Generate reorder suggestions for all materials
        print("💡 Generating reorder suggestions...")
        for material in materials:
            tracker._create_reorder_suggestion(material)
        
        # Display final alert summary
        print("\n🚨 ALERT SUMMARY:")
        alerts = tracker.get_active_alerts()
        
        if alerts:
            print(f"📢 Created {len(alerts)} active alerts:")
            for alert in alerts:
                alert_emoji = "🔴" if alert.alert_type == "critical" else "🟡"
                
                # Get material name for alert
                material = db.query(RawMaterial).filter(
                    RawMaterial.material_id == alert.material_id
                ).first()
                material_name = material.material_name if material else "Unknown"
                
                print(f"  {alert_emoji} {alert.alert_type.upper()}: {material_name} - {alert.current_stock:.1f} units")
        
        suggestions = tracker.get_reorder_suggestions()
        if suggestions:
            print(f"💡 Created {len(suggestions)} reorder suggestions")
        
        print("\n✅ Low Stock Alert Scenario Created Successfully!")
        print("\n🎯 NEXT STEPS:")
        print("1. Visit http://localhost:8503 in your browser")
        print("2. Login with admin/admin123")
        print("3. Check the SIDEBAR for low stock alerts 🚨")
        print("4. Go to 'Raw Materials' → 'Consume Material' tab")
        print("5. Try consuming materials to see automatic stock updates")
        print("6. Watch alerts appear in real-time!")
        
    except Exception as e:
        print(f"❌ Error creating low stock scenario: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    create_low_stock_scenario()