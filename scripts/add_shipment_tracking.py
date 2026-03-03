"""
Add additional shipment tracking records to the Steel Manufacturing System
Adds 10 more shipments with detailed tracking information
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.database_models import *
from datetime import datetime, timedelta
import random

def add_tracking_shipments(db):
    """Add 10 additional shipments with comprehensive tracking data"""
    print("Adding shipment tracking records...")
    
    # Get some production orders for reference (create more if needed)
    existing_orders = db.query(ProductionOrder).all()
    
    # Create additional production orders if we don't have enough
    if len(existing_orders) < 10:
        print("Creating additional production orders for shipments...")
        additional_orders = []
        for i in range(len(existing_orders), 15):  # Create up to 15 orders total
            order = ProductionOrder(
                order_number=f"PO-2024-{str(i+6).zfill(3)}",
                product_name=f"Steel Product Batch {i+6}",
                quantity_ordered=random.uniform(50, 500),
                quantity_produced=random.uniform(45, 500),
                unit=random.choice(["tons", "meters", "pieces"]),
                status=random.choice([OrderStatus.COMPLETED, OrderStatus.IN_PROGRESS]),
                expected_completion=datetime.now() + timedelta(days=random.randint(1, 30)),
                assigned_to=random.choice([2, 3]),  # manager or operator
                notes=f"Production order {i+6} for shipment"
            )
            if order.status == OrderStatus.COMPLETED:
                order.start_date = datetime.now() - timedelta(days=random.randint(5, 20))
                order.actual_completion = datetime.now() - timedelta(days=random.randint(1, 5))
            additional_orders.append(order)
        
        for order in additional_orders:
            db.add(order)
        db.commit()
        
        # Refresh the orders list
        existing_orders = db.query(ProductionOrder).all()
    
    # Sample carriers and their tracking formats
    carriers = [
        {"name": "Steel Transport Inc", "prefix": "ST", "digits": 7},
        {"name": "Heavy Freight Solutions", "prefix": "HF", "digits": 7},
        {"name": "Industrial Logistics Co", "prefix": "IL", "digits": 8},
        {"name": "Global Steel Shipping", "prefix": "GSS", "digits": 6},
        {"name": "Metro Transport Ltd", "prefix": "MT", "digits": 9},
        {"name": "Express Steel Delivery", "prefix": "ESD", "digits": 7},
        {"name": "Prime Logistics Corp", "prefix": "PLC", "digits": 8},
        {"name": "Nationwide Freight", "prefix": "NF", "digits": 6}
    ]
    
    # Sample destinations
    destinations = [
        "ABC Manufacturing, Detroit MI",
        "XYZ Construction, Houston TX", 
        "Steel Works Inc, Pittsburgh PA",
        "Industrial Solutions, Chicago IL",
        "Metro Builders, Los Angeles CA",
        "Prime Steel Corp, Atlanta GA",
        "Advanced Manufacturing, Phoenix AZ",
        "Steel Dynamics, Cleveland OH",
        "Precision Steel Co, Denver CO",
        "American Steel Works, Miami FL",
        "National Construction, Seattle WA",
        "Heavy Industries Ltd, Boston MA"
    ]
    
    tracking_shipments = []
    
    for i in range(10):
        carrier = random.choice(carriers)
        order = random.choice(existing_orders)
        
        # Generate tracking number
        tracking_num = f"{carrier['prefix']}{random.randint(10**(carrier['digits']-1), 10**carrier['digits']-1)}"
        
        # Random shipment dates
        ship_date = datetime.now() - timedelta(days=random.randint(0, 15))
        expected_delivery = ship_date + timedelta(days=random.randint(2, 10))
        
        # Determine shipment status based on dates
        if ship_date < datetime.now() - timedelta(days=7):
            status = random.choice([ShipmentStatus.DELIVERED, ShipmentStatus.IN_TRANSIT])
            actual_delivery = ship_date + timedelta(days=random.randint(2, 8)) if status == ShipmentStatus.DELIVERED else None
        elif ship_date < datetime.now() - timedelta(days=2):
            status = ShipmentStatus.IN_TRANSIT
            actual_delivery = None
        else:
            status = ShipmentStatus.PENDING
            actual_delivery = None
            ship_date = None  # Future shipment
        
        shipment_data = {
            "shipment_number": f"SH-2024-{str(i+3).zfill(3)}",
            "order_id": order.order_id,
            "destination": random.choice(destinations),
            "quantity_shipped": round(random.uniform(order.quantity_produced * 0.8, order.quantity_produced), 2),
            "unit": order.unit,
            "status": status,
            "scheduled_date": ship_date or datetime.now() + timedelta(days=random.randint(1, 5)),
            "actual_ship_date": ship_date,
            "expected_delivery": expected_delivery,
            "actual_delivery": actual_delivery,
            "carrier": carrier["name"],
            "tracking_number": tracking_num,
            "logistics_handler": 5,  # logistics user
            "notes": f"Shipment via {carrier['name']} - Track: {tracking_num}"
        }
        
        tracking_shipments.append(shipment_data)
    
    # Add all shipments to database
    for shipment_data in tracking_shipments:
        shipment = Shipment(**shipment_data)
        db.add(shipment)
    
    db.commit()
    print(f"✓ {len(tracking_shipments)} tracking shipments added")
    
    # Print summary of tracking information
    print("\n📦 Shipment Tracking Summary:")
    print("=" * 60)
    all_shipments = db.query(Shipment).all()
    
    status_counts = {}
    for shipment in all_shipments:
        status = shipment.status.value
        status_counts[status] = status_counts.get(status, 0) + 1
    
    for status, count in status_counts.items():
        print(f"  {status.upper()}: {count} shipments")
    
    print(f"\nTotal Shipments: {len(all_shipments)}")
    print("\n🚛 Recent Shipments:")
    print("-" * 60)
    
    recent_shipments = db.query(Shipment).order_by(Shipment.created_at.desc()).limit(5).all()
    for shipment in recent_shipments:
        status_emoji = {
            "pending": "⏳",
            "in_transit": "🚛",
            "delivered": "✅",
            "cancelled": "❌"
        }
        emoji = status_emoji.get(shipment.status.value, "📦")
        print(f"  {emoji} {shipment.shipment_number} → {shipment.destination[:30]}...")
        print(f"     Carrier: {shipment.carrier} | Track: {shipment.tracking_number}")
        print(f"     Status: {shipment.status.value.upper()}")
        print()

def main():
    """Main function to add tracking shipments"""
    print("🚛 Adding shipment tracking data to Steel Manufacturing System...")
    
    db = SessionLocal()
    
    try:
        # Get current shipment count
        current_shipments = db.query(Shipment).count()
        print(f"Current shipments in system: {current_shipments}")
        
        # Add tracking shipments
        add_tracking_shipments(db)
        
        # Final count
        total_shipments = db.query(Shipment).count()
        print(f"\n✅ Shipment tracking data added successfully!")
        print(f"Total shipments now: {total_shipments}")
        
    except Exception as e:
        print(f"❌ Error adding shipment tracking data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    main()