"""
Add sample data to the Steel Manufacturing System
Includes inventory, production orders, quality inspections, and shipments
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.database_models import *
from datetime import datetime, timedelta
import random

def add_sample_raw_materials(db):
    """Add 10 sample raw materials to inventory"""
    print("Adding sample raw materials...")
    
    sample_materials = [
        {
            "material_name": "Iron Ore",
            "material_type": "Raw Material",
            "supplier": "Mining Corp Ltd",
            "quantity_available": 1500.0,
            "unit": "tons",
            "cost_per_unit": 85.50,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "IRN-2024-001",
            "quality_grade": "Grade A"
        },
        {
            "material_name": "Coal",
            "material_type": "Fuel",
            "supplier": "Energy Solutions Inc",
            "quantity_available": 800.0,
            "unit": "tons",
            "cost_per_unit": 120.00,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "COL-2024-002",
            "quality_grade": "Premium"
        },
        {
            "material_name": "Limestone",
            "material_type": "Flux",
            "supplier": "Quarry Holdings",
            "quantity_available": 600.0,
            "unit": "tons",
            "cost_per_unit": 45.75,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "LIM-2024-003",
            "quality_grade": "Standard"
        },
        {
            "material_name": "Scrap Steel",
            "material_type": "Recycled Material",
            "supplier": "Metro Recycling",
            "quantity_available": 350.0,
            "unit": "tons",
            "cost_per_unit": 240.00,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "SCR-2024-004",
            "quality_grade": "Grade B"
        },
        {
            "material_name": "Manganese Ore",
            "material_type": "Alloy Material",
            "supplier": "Global Alloys",
            "quantity_available": 75.0,
            "unit": "tons",
            "cost_per_unit": 890.00,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "MNG-2024-005",
            "quality_grade": "High Grade"
        },
        {
            "material_name": "Chromium",
            "material_type": "Alloy Material",
            "supplier": "Specialty Metals Co",
            "quantity_available": 25.0,
            "unit": "tons",
            "cost_per_unit": 1250.00,
            "status": MaterialStatus.RESERVED,
            "batch_number": "CHR-2024-006",
            "quality_grade": "Premium"
        },
        {
            "material_name": "Refractory Bricks",
            "material_type": "Furnace Material",
            "supplier": "Heat-Tech Industries",
            "quantity_available": 2000.0,
            "unit": "pieces",
            "cost_per_unit": 12.50,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "REF-2024-007",
            "quality_grade": "Fire Grade"
        },
        {
            "material_name": "Oxygen",
            "material_type": "Gas",
            "supplier": "Industrial Gases Ltd",
            "quantity_available": 500.0,
            "unit": "cubic meters",
            "cost_per_unit": 0.85,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "OXY-2024-008",
            "quality_grade": "99.5% Pure"
        },
        {
            "material_name": "Argon",
            "material_type": "Inert Gas",
            "supplier": "Noble Gas Supply",
            "quantity_available": 150.0,
            "unit": "cubic meters",
            "cost_per_unit": 2.40,
            "status": MaterialStatus.AVAILABLE,
            "batch_number": "ARG-2024-009",
            "quality_grade": "99.9% Pure"
        },
        {
            "material_name": "Flux Powder",
            "material_type": "Chemical",
            "supplier": "Chemical Works Inc",
            "quantity_available": 45.0,
            "unit": "tons",
            "cost_per_unit": 180.00,
            "status": MaterialStatus.USED,
            "batch_number": "FLX-2024-010",
            "quality_grade": "Industrial Grade"
        }
    ]
    
    for material_data in sample_materials:
        material = RawMaterial(
            **material_data,
            created_by=1,  # admin user
            expiry_date=datetime.now() + timedelta(days=365)
        )
        db.add(material)
    
    db.commit()
    print("✓ 10 raw materials added to inventory")

def add_sample_production_orders(db):
    """Add sample production orders"""
    print("Adding sample production orders...")
    
    orders = [
        {
            "order_number": "PO-2024-001",
            "product_name": "Steel Beams (I-section)",
            "quantity_ordered": 150.0,
            "quantity_produced": 145.0,
            "unit": "tons",
            "status": OrderStatus.COMPLETED,
            "start_date": datetime.now() - timedelta(days=15),
            "expected_completion": datetime.now() - timedelta(days=1),
            "actual_completion": datetime.now() - timedelta(days=2),
            "assigned_to": 2,  # manager
            "notes": "High priority order for construction project"
        },
        {
            "order_number": "PO-2024-002", 
            "product_name": "Steel Sheets (Hot Rolled)",
            "quantity_ordered": 200.0,
            "quantity_produced": 120.0,
            "unit": "tons",
            "status": OrderStatus.IN_PROGRESS,
            "start_date": datetime.now() - timedelta(days=5),
            "expected_completion": datetime.now() + timedelta(days=3),
            "assigned_to": 3,  # operator
            "notes": "Standard thickness sheets for automotive industry"
        },
        {
            "order_number": "PO-2024-003",
            "product_name": "Stainless Steel Rods",
            "quantity_ordered": 80.0,
            "quantity_produced": 0.0,
            "unit": "tons",
            "status": OrderStatus.PENDING,
            "expected_completion": datetime.now() + timedelta(days=10),
            "assigned_to": 2,
            "notes": "Premium grade rods for medical equipment manufacturing"
        },
        {
            "order_number": "PO-2024-004",
            "product_name": "Carbon Steel Pipes",
            "quantity_ordered": 300.0,
            "quantity_produced": 300.0,
            "unit": "meters",
            "status": OrderStatus.COMPLETED,
            "start_date": datetime.now() - timedelta(days=20),
            "expected_completion": datetime.now() - timedelta(days=5),
            "actual_completion": datetime.now() - timedelta(days=3),
            "assigned_to": 3,
            "notes": "Large diameter pipes for oil & gas industry"
        },
        {
            "order_number": "PO-2024-005",
            "product_name": "Steel Wire Mesh",
            "quantity_ordered": 500.0,
            "quantity_produced": 250.0,
            "unit": "square meters",
            "status": OrderStatus.IN_PROGRESS,
            "start_date": datetime.now() - timedelta(days=8),
            "expected_completion": datetime.now() + timedelta(days=5),
            "assigned_to": 3,
            "notes": "Reinforcement mesh for concrete applications"
        }
    ]
    
    for order_data in orders:
        order = ProductionOrder(**order_data)
        db.add(order)
    
    db.commit()
    print("✓ 5 production orders added")

def add_sample_inventory_logs(db):
    """Add sample inventory transaction logs"""
    print("Adding sample inventory logs...")
    
    # Get material IDs for reference
    materials = db.query(RawMaterial).limit(5).all()
    
    for i, material in enumerate(materials):
        # Add initial stock entry
        log = InventoryLog(
            material_id=material.material_id,
            transaction_type="IN",
            quantity_change=material.quantity_available,
            quantity_before=0.0,
            quantity_after=material.quantity_available,
            reference_id=f"INIT-{material.material_id}",
            notes="Initial stock entry",
            recorded_by=1
        )
        db.add(log)
        
        # Add some usage entries
        if i < 3:  # Only for first 3 materials
            usage = random.uniform(10, 50)
            usage_log = InventoryLog(
                material_id=material.material_id,
                transaction_type="OUT",
                quantity_change=-usage,
                quantity_before=material.quantity_available,
                quantity_after=material.quantity_available - usage,
                reference_id=f"PO-2024-00{i+1}",
                notes=f"Material consumption for production order",
                recorded_by=3
            )
            db.add(usage_log)
    
    db.commit()
    print("✓ Inventory transaction logs added")

def add_sample_quality_inspections(db):
    """Add sample quality inspection records"""
    print("Adding sample quality inspections...")
    
    # Get production orders for reference
    orders = db.query(ProductionOrder).limit(3).all()
    
    inspections = [
        {
            "order_id": orders[0].order_id,
            "tested_by": 4,  # quality user
            "status": QualityStatus.PASS,
            "tensile_strength": 580.5,
            "hardness": 220.0,
            "ductility": 25.8,
            "surface_quality": "Excellent",
            "defects_found": "None detected",
            "rework_required": False,
            "passed_date": datetime.now() - timedelta(days=1),
            "notes": "All parameters within specification"
        },
        {
            "order_id": orders[1].order_id,
            "tested_by": 4,
            "status": QualityStatus.REWORK,
            "tensile_strength": 520.0,
            "hardness": 190.5,
            "ductility": 22.1,
            "surface_quality": "Good",
            "defects_found": "Minor surface irregularities",
            "rework_required": True,
            "notes": "Requires surface finishing before acceptance"
        },
        {
            "order_id": orders[2].order_id if len(orders) > 2 else orders[0].order_id,
            "tested_by": 4,
            "status": QualityStatus.PASS,
            "tensile_strength": 610.2,
            "hardness": 235.8,
            "ductility": 28.5,
            "surface_quality": "Excellent",
            "defects_found": "None detected",
            "rework_required": False,
            "passed_date": datetime.now(),
            "notes": "Premium quality - exceeds specifications"
        }
    ]
    
    for inspection_data in inspections:
        inspection = QualityInspection(**inspection_data)
        db.add(inspection)
    
    db.commit()
    print("✓ Quality inspection records added")

def add_sample_shipments(db):
    """Add sample shipment records"""
    print("Adding sample shipments...")
    
    # Get completed orders for reference
    completed_orders = db.query(ProductionOrder).filter(
        ProductionOrder.status == OrderStatus.COMPLETED
    ).limit(2).all()
    
    shipments = [
        {
            "shipment_number": "SH-2024-001",
            "order_id": completed_orders[0].order_id,
            "destination": "ABC Construction, New York",
            "quantity_shipped": 145.0,
            "unit": "tons",
            "status": ShipmentStatus.DELIVERED,
            "scheduled_date": datetime.now() - timedelta(days=3),
            "actual_ship_date": datetime.now() - timedelta(days=3),
            "expected_delivery": datetime.now() - timedelta(days=1),
            "actual_delivery": datetime.now() - timedelta(days=1),
            "carrier": "Steel Transport Inc",
            "tracking_number": "ST2024001",
            "logistics_handler": 5,  # logistics user
            "notes": "Delivered on time, customer satisfied"
        },
        {
            "shipment_number": "SH-2024-002",
            "order_id": completed_orders[1].order_id if len(completed_orders) > 1 else completed_orders[0].order_id,
            "destination": "XYZ Pipeline Corp, Texas",
            "quantity_shipped": 300.0,
            "unit": "meters",
            "status": ShipmentStatus.IN_TRANSIT,
            "scheduled_date": datetime.now() - timedelta(days=1),
            "actual_ship_date": datetime.now() - timedelta(days=1),
            "expected_delivery": datetime.now() + timedelta(days=2),
            "carrier": "Heavy Freight Solutions",
            "tracking_number": "HF2024002",
            "logistics_handler": 5,
            "notes": "Large shipment, special handling required"
        }
    ]
    
    for shipment_data in shipments:
        shipment = Shipment(**shipment_data)
        db.add(shipment)
    
    db.commit()
    print("✓ Shipment records added")

def main():
    """Main function to add all sample data"""
    print("🏭 Adding sample data to Steel Manufacturing System...")
    
    db = SessionLocal()
    
    try:
        # Check if sample data already exists
        existing_materials = db.query(RawMaterial).count()
        if existing_materials > 0:
            print("⚠️  Sample data already exists. Skipping...")
            return
        
        # Add all sample data
        add_sample_raw_materials(db)
        add_sample_production_orders(db)
        add_sample_inventory_logs(db)
        add_sample_quality_inspections(db)
        add_sample_shipments(db)
        
        print("\n✅ Sample data added successfully!")
        print("\nSummary:")
        print(f"  • {db.query(RawMaterial).count()} Raw Materials in inventory")
        print(f"  • {db.query(ProductionOrder).count()} Production Orders")
        print(f"  • {db.query(InventoryLog).count()} Inventory Transactions")
        print(f"  • {db.query(QualityInspection).count()} Quality Inspections")
        print(f"  • {db.query(Shipment).count()} Shipments")
        
    except Exception as e:
        print(f"❌ Error adding sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()