"""
Create Sample Defect Data for Defect Rate Analytics
Steel Plant Quality Control Tracking System
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import SessionLocal
from models.database_models import (
    DefectTracking, FinishedProduct, DefectType
)
from datetime import datetime, timedelta
import random

def create_defect_samples():
    """Create comprehensive defect tracking samples for analytics"""
    
    print("🔍 Creating Defect Rate Analytics Sample Data...")
    
    db = SessionLocal()
    
    try:
        # BSP Steel Products and typical defect scenarios
        steel_products_defects = {
            "Railway Rails": {
                "defect_types": [DefectType.SURFACE_DEFECT, DefectType.STRUCTURAL, DefectType.DIMENSIONAL],
                "typical_reasons": [
                    "Rolling temperature variation",
                    "Inclusion in raw material",
                    "Improper cooling process",
                    "Mechanical stress during handling",
                    "Surface oxidation"
                ],
                "production_batches": ["RR-2024-001", "RR-2024-002", "RR-2024-003", "RR-2024-004"],
                "cost_per_unit": 85000,
                "unit": "tons"
            },
            "Steel Plates": {
                "defect_types": [DefectType.SURFACE_DEFECT, DefectType.DIMENSIONAL, DefectType.CHEMICAL_COMPOSITION],
                "typical_reasons": [
                    "Uneven thickness rolling",
                    "Surface scratches during transport",
                    "Chemical composition deviation",
                    "Edge cracking during cutting",
                    "Heat treatment issues"
                ],
                "production_batches": ["SP-2024-001", "SP-2024-002", "SP-2024-003"],
                "cost_per_unit": 65000,
                "unit": "tons"
            },
            "Structural Steel - Angles": {
                "defect_types": [DefectType.DIMENSIONAL, DefectType.STRUCTURAL, DefectType.SURFACE_DEFECT],
                "typical_reasons": [
                    "Dimensional tolerance exceeded",
                    "Bending deformation",
                    "Weld defects in joints",
                    "Corrosion spots",
                    "Improper cutting angles"
                ],
                "production_batches": ["SSA-2024-001", "SSA-2024-002"],
                "cost_per_unit": 70000,
                "unit": "tons"
            },
            "Steel Sheets": {
                "defect_types": [DefectType.SURFACE_DEFECT, DefectType.DIMENSIONAL],
                "typical_reasons": [
                    "Surface roughness variation",
                    "Thickness non-uniformity",
                    "Edge defects",
                    "Coating defects",
                    "Flatness issues"
                ],
                "production_batches": ["SS-2024-001", "SS-2024-002", "SS-2024-003"],
                "cost_per_unit": 72000,
                "unit": "tons"
            },
            "Wire Rods": {
                "defect_types": [DefectType.SURFACE_DEFECT, DefectType.CHEMICAL_COMPOSITION, DefectType.DIMENSIONAL],
                "typical_reasons": [
                    "Wire drawing defects",
                    "Surface oxidation",
                    "Diameter variation",
                    "Chemical impurities",
                    "Coiling problems"
                ],
                "production_batches": ["WR-2024-001", "WR-2024-002"],
                "cost_per_unit": 68000,
                "unit": "tons"
            }
        }
        
        # Create defect records over the last 30 days
        defect_records = []
        
        print("📊 Generating defect data for different products...")
        
        for product_name, product_info in steel_products_defects.items():
            print(f"  🔧 Creating defects for {product_name}")
            
            for batch in product_info["production_batches"]:
                # Generate 3-8 defect records per batch over last 30 days
                num_defects = random.randint(3, 8)
                
                for _ in range(num_defects):
                    # Random date within last 30 days
                    days_ago = random.randint(1, 30)
                    inspection_date = datetime.utcnow() - timedelta(days=days_ago)
                    
                    # Random defect data
                    defect_type = random.choice(product_info["defect_types"])
                    reason = random.choice(product_info["typical_reasons"])
                    
                    # Realistic defect quantities (small percentage of production)
                    production_quantity = random.uniform(50, 200)  # Typical batch size
                    defect_rate_percentage = random.uniform(0.5, 5.0)  # 0.5% to 5% defect rate
                    
                    defective_quantity = production_quantity * (defect_rate_percentage / 100)
                    scrap_quantity = defective_quantity * random.uniform(0.3, 0.8)  # 30-80% becomes scrap
                    
                    estimated_loss = defective_quantity * product_info["cost_per_unit"]
                    
                    # Corrective actions based on defect type
                    corrective_actions = {
                        DefectType.SURFACE_DEFECT: [
                            "Improved surface cleaning process",
                            "Better material handling procedures",
                            "Enhanced quality checks at rolling stage"
                        ],
                        DefectType.DIMENSIONAL: [
                            "Calibration of measuring equipment", 
                            "Stricter tolerance monitoring",
                            "Process parameter adjustment"
                        ],
                        DefectType.CHEMICAL_COMPOSITION: [
                            "Raw material composition verification",
                            "Improved mixing procedures",
                            "Enhanced laboratory testing"
                        ],
                        DefectType.STRUCTURAL: [
                            "Heat treatment optimization",
                            "Stress relief process improvement",
                            "Material grade verification"
                        ]
                    }
                    
                    corrective_action = random.choice(corrective_actions.get(defect_type, ["General process improvement"]))
                    
                    defect_record = DefectTracking(
                        product_name=product_name,
                        production_batch=batch,
                        defective_quantity=round(defective_quantity, 2),
                        scrap_quantity=round(scrap_quantity, 2),
                        unit=product_info["unit"],
                        defect_type=defect_type,
                        reason_for_defect=reason,
                        inspection_date=inspection_date,
                        inspected_by=1,  # Default inspector
                        estimated_loss=round(estimated_loss, 2),
                        corrective_action=corrective_action,
                        prevention_measure=f"Enhanced monitoring for {defect_type.value.replace('_', ' ')} prevention",
                        created_at=inspection_date
                    )
                    
                    defect_records.append(defect_record)
        
        # Add all records to database
        print(f"💾 Saving {len(defect_records)} defect records to database...")
        for record in defect_records:
            db.add(record)
        
        db.commit()
        
        # Create summary analytics
        print("\n📊 DEFECT RATE ANALYTICS SUMMARY:")
        
        # Calculate defect rates by product
        product_defect_summary = {}
        
        for product_name, product_info in steel_products_defects.items():
            product_defects = [r for r in defect_records if r.product_name == product_name]
            
            total_defective = sum(d.defective_quantity for d in product_defects)
            total_scrap = sum(d.scrap_quantity for d in product_defects)
            total_loss = sum(d.estimated_loss for d in product_defects)
            defect_incidents = len(product_defects)
            
            # Estimate production quantity (defects are typically 1-5% of production)
            estimated_production = total_defective * random.uniform(20, 100)  # Reverse estimate
            defect_rate = (total_defective / estimated_production) * 100 if estimated_production > 0 else 0
            
            product_defect_summary[product_name] = {
                "defect_incidents": defect_incidents,
                "total_defective": total_defective,
                "total_scrap": total_scrap,
                "estimated_loss": total_loss,
                "defect_rate_percentage": defect_rate
            }
            
            print(f"\n🔧 {product_name}:")
            print(f"  📊 Defect Rate: {defect_rate:.2f}%")
            print(f"  📈 Defect Incidents: {defect_incidents}")
            print(f"  ⚖️  Total Defective: {total_defective:.1f} {product_info['unit']}")
            print(f"  🗑️  Total Scrap: {total_scrap:.1f} {product_info['unit']}")
            print(f"  💰 Financial Loss: ₹{total_loss:,.0f}")
        
        # Overall summary
        total_incidents = sum(s["defect_incidents"] for s in product_defect_summary.values())
        total_financial_loss = sum(s["estimated_loss"] for s in product_defect_summary.values())
        avg_defect_rate = sum(s["defect_rate_percentage"] for s in product_defect_summary.values()) / len(product_defect_summary)
        
        print(f"\n🏭 OVERALL BSP PLANT QUALITY METRICS:")
        print(f"  📊 Total Defect Incidents: {total_incidents}")
        print(f"  📈 Average Defect Rate: {avg_defect_rate:.2f}%")
        print(f"  💰 Total Financial Impact: ₹{total_financial_loss:,.0f}")
        
        # Defect type distribution
        defect_type_counts = {}
        for record in defect_records:
            if record.defect_type not in defect_type_counts:
                defect_type_counts[record.defect_type] = 0
            defect_type_counts[record.defect_type] += 1
        
        print(f"\n🔍 DEFECT TYPE DISTRIBUTION:")
        for defect_type, count in defect_type_counts.items():
            percentage = (count / total_incidents) * 100
            print(f"  • {defect_type.value.replace('_', ' ').title()}: {count} incidents ({percentage:.1f}%)")
        
        print(f"\n✅ Defect Rate Analytics Sample Data Created Successfully!")
        print(f"\n🎯 NEXT STEPS:")
        print(f"1. Visit the Streamlit app: http://localhost:8503")
        print(f"2. Go to 'Inventory Management' → 'Defect Tracking' tab")
        print(f"3. View detailed defect analytics and trends")
        print(f"4. Check 'Quality Assurance' module for quality metrics")
        print(f"5. See defect rate charts and corrective action tracking")
        
        # Create some critical defect alerts
        critical_defects = [r for r in defect_records if r.defective_quantity > 5.0]
        print(f"\n🚨 CRITICAL DEFECTS ALERT: {len(critical_defects)} high-quantity defect incidents require attention!")
        
    except Exception as e:
        print(f"❌ Error creating defect samples: {e}")
        db.rollback()
        
    finally:
        db.close()

if __name__ == "__main__":
    create_defect_samples()