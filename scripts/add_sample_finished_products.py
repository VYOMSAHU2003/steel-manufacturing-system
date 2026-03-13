"""
Add sample finished products data for BSP Steel Plant
This script adds sample data for all major steel products
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.database_models import FinishedProduct, ProductStatus
from datetime import datetime
import random

def add_sample_finished_products():
    """Add sample finished products to database"""
    db = SessionLocal()
    
    try:
        # Check if finished products already exist
        existing_products = db.query(FinishedProduct).count()
        if existing_products > 0:
            print("✓ Finished products already exist, skipping sample data")
            return
        
        print("Adding sample finished products...")
        
        # Sample products data for BSP Steel Plant
        products_data = [
            # Railway Rails
            {
                "product_name": "Railway Rails",
                "product_type": "Railway",
                "production_batch": "BSP-RAIL-2024-001",
                "quality_grade": "Grade A",
                "production_quantity": 500.0,
                "available_stock": 450.0,
                "unit": "tons",
                "warehouse_location": "Rail Storage Yard",
                "cost_per_unit": 75000.0,
                "specifications": "90kg/m rail, 13m length, IS:2062 standard"
            },
            {
                "product_name": "Railway Rails", 
                "product_type": "Railway",
                "production_batch": "BSP-RAIL-2024-002",
                "quality_grade": "Grade B",
                "production_quantity": 300.0,
                "available_stock": 280.0,
                "unit": "tons",
                "warehouse_location": "Rail Storage Yard",
                "cost_per_unit": 72000.0,
                "specifications": "60kg/m rail, 13m length, IS:2062 standard"
            },
            
            # Steel Plates
            {
                "product_name": "Steel Plates",
                "product_type": "Plates",
                "production_batch": "BSP-PLATE-2024-001",
                "quality_grade": "Premium",
                "production_quantity": 800.0,
                "available_stock": 650.0,
                "unit": "tons",
                "warehouse_location": "Plate Storage Area",
                "cost_per_unit": 65000.0,
                "specifications": "20mm thick, 2m x 6m, IS:2062 Fe410W"
            },
            {
                "product_name": "Steel Plates",
                "product_type": "Plates", 
                "production_batch": "BSP-PLATE-2024-002",
                "quality_grade": "Standard",
                "production_quantity": 600.0,
                "available_stock": 520.0,
                "unit": "tons",
                "warehouse_location": "Plate Storage Area",
                "cost_per_unit": 62000.0,
                "specifications": "16mm thick, 2m x 6m, IS:2062 Fe250"
            },
            
            # Structural Steel - Angles
            {
                "product_name": "Structural Steel - Angles",
                "product_type": "Structural",
                "production_batch": "BSP-ANG-2024-001",
                "quality_grade": "Grade A",
                "production_quantity": 400.0,
                "available_stock": 350.0,
                "unit": "tons",
                "warehouse_location": "Structural Steel Yard",
                "cost_per_unit": 58000.0,
                "specifications": "Equal angles 75x75x8mm, 12m length"
            },
            
            # Structural Steel - Channels
            {
                "product_name": "Structural Steel - Channels",
                "product_type": "Structural",
                "production_batch": "BSP-CHN-2024-001",
                "quality_grade": "Grade A",
                "production_quantity": 350.0,
                "available_stock": 300.0,
                "unit": "tons",
                "warehouse_location": "Structural Steel Yard",
                "cost_per_unit": 60000.0,
                "specifications": "ISMC 200x50x7.5mm, 12m length"
            },
            
            # Structural Steel - Beams
            {
                "product_name": "Structural Steel - Beams",
                "product_type": "Structural",
                "production_batch": "BSP-BEAM-2024-001",
                "quality_grade": "Premium",
                "production_quantity": 450.0,
                "available_stock": 380.0,
                "unit": "tons",
                "warehouse_location": "Structural Steel Yard",
                "cost_per_unit": 68000.0,
                "specifications": "ISMB 300x140x7mm, 12m length"
            },
            
            # Steel Sheets
            {
                "product_name": "Steel Sheets",
                "product_type": "Sheets",
                "production_batch": "BSP-SHEET-2024-001",
                "quality_grade": "Standard",
                "production_quantity": 700.0,
                "available_stock": 550.0,
                "unit": "tons",
                "warehouse_location": "Sheet Storage Area",
                "cost_per_unit": 55000.0,
                "specifications": "2mm thick, 1.2m x 2.4m, Cold rolled"
            },
            {
                "product_name": "Steel Sheets",
                "product_type": "Sheets",
                "production_batch": "BSP-SHEET-2024-002", 
                "quality_grade": "Premium",
                "production_quantity": 500.0,
                "available_stock": 420.0,
                "unit": "tons",
                "warehouse_location": "Sheet Storage Area",
                "cost_per_unit": 58000.0,
                "specifications": "1.5mm thick, 1.2m x 2.4m, Hot rolled"
            },
            
            # Wire Rods
            {
                "product_name": "Wire Rods",
                "product_type": "Wire",
                "production_batch": "BSP-WIRE-2024-001",
                "quality_grade": "Grade A",
                "production_quantity": 600.0,
                "available_stock": 480.0,
                "unit": "tons",
                "warehouse_location": "Wire Rod Storage",
                "cost_per_unit": 52000.0,
                "specifications": "8mm diameter, Fe500D grade"
            },
            {
                "product_name": "Wire Rods",
                "product_type": "Wire",
                "production_batch": "BSP-WIRE-2024-002",
                "quality_grade": "Standard",
                "production_quantity": 400.0,
                "available_stock": 350.0,
                "unit": "tons", 
                "warehouse_location": "Wire Rod Storage",
                "cost_per_unit": 50000.0,
                "specifications": "6mm diameter, Fe415 grade"
            },
            
            # Billets
            {
                "product_name": "Billets",
                "product_type": "Semi-finished",
                "production_batch": "BSP-BILL-2024-001",
                "quality_grade": "Standard",
                "production_quantity": 1200.0,
                "available_stock": 900.0,
                "unit": "tons",
                "warehouse_location": "Billet Storage Yard",
                "cost_per_unit": 45000.0,
                "specifications": "120mm x 120mm, 6m length, Carbon steel"
            },
            {
                "product_name": "Billets",
                "product_type": "Semi-finished",
                "production_batch": "BSP-BILL-2024-002",
                "quality_grade": "Premium",
                "production_quantity": 800.0,
                "available_stock": 650.0,
                "unit": "tons",
                "warehouse_location": "Billet Storage Yard", 
                "cost_per_unit": 47000.0,
                "specifications": "150mm x 150mm, 6m length, Alloy steel"
            },
            
            # Blooms
            {
                "product_name": "Blooms",
                "product_type": "Semi-finished",
                "production_batch": "BSP-BLOOM-2024-001",
                "quality_grade": "Grade A",
                "production_quantity": 900.0,
                "available_stock": 750.0,
                "unit": "tons",
                "warehouse_location": "Bloom Storage Yard",
                "cost_per_unit": 46000.0,
                "specifications": "250mm x 300mm, 6m length"
            },
            
            # Pig Iron
            {
                "product_name": "Pig Iron",
                "product_type": "Pig Iron",
                "production_batch": "BSP-PIG-2024-001",
                "quality_grade": "Standard",
                "production_quantity": 2000.0,
                "available_stock": 1500.0,
                "unit": "tons",
                "warehouse_location": "Pig Iron Storage",
                "cost_per_unit": 35000.0,
                "specifications": "High phosphorus pig iron, Carbon 3.5-4.5%"
            },
            {
                "product_name": "Pig Iron",
                "product_type": "Pig Iron",
                "production_batch": "BSP-PIG-2024-002",
                "quality_grade": "Premium",
                "production_quantity": 1500.0,
                "available_stock": 1200.0,
                "unit": "tons",
                "warehouse_location": "Pig Iron Storage",
                "cost_per_unit": 38000.0,
                "specifications": "Low phosphorus pig iron, Carbon 4.0-4.5%"
            }
        ]
        
        # Add products to database
        for product_data in products_data:
            product = FinishedProduct(
                product_name=product_data["product_name"],
                product_type=product_data["product_type"],
                production_batch=product_data["production_batch"],
                quality_grade=product_data["quality_grade"],
                production_quantity=product_data["production_quantity"],
                available_stock=product_data["available_stock"],
                unit=product_data["unit"],
                warehouse_location=product_data["warehouse_location"],
                cost_per_unit=product_data["cost_per_unit"], 
                specifications=product_data["specifications"],
                status=ProductStatus.APPROVED,
                created_by=1  # Admin user
            )
            db.add(product)
        
        db.commit()
        print(f"✓ Successfully added {len(products_data)} finished products!")
        print("\n📦 Products Added:")
        for product_data in products_data:
            print(f"   • {product_data['product_name']} - {product_data['available_stock']} {product_data['unit']} ({product_data['quality_grade']})")
        
    except Exception as e:
        db.rollback()
        print(f"Error adding sample products: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    add_sample_finished_products()
    print("\n✓ Sample finished products data added!")