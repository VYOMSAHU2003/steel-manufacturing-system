"""
Automatic Material Consumption Tracking and Low Stock Alert System
For BSP Steel Plant Management
"""
import streamlit as st
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from config.database import SessionLocal
from models.database_models import (
    RawMaterial, MaterialConsumption, LowStockAlert, 
    MaterialReorderSuggestion, User
)
from utils.email_notifications import send_low_stock_email_notification

class MaterialTracker:
    """Automatic material consumption tracking and alert system"""
    
    def __init__(self):
        self.db = SessionLocal()
        
    def __del__(self):
        if hasattr(self, 'db'):
            self.db.close()
    
    def consume_material(self, material_id: int, quantity: float, 
                        consumption_type: str = "production", 
                        consumed_by: int = 1, notes: str = ""):
        """
        Automatically deduct material from inventory and log consumption
        
        Args:
            material_id: ID of the material to consume
            quantity: Amount to consume 
            consumption_type: Type of consumption (production, testing, maintenance)
            consumed_by: User ID who consumed the material
            notes: Additional notes
            
        Returns:
            dict: Result with success status and message
        """
        try:
            # Get material details
            material = self.db.query(RawMaterial).filter(
                RawMaterial.material_id == material_id
            ).first()
            
            if not material:
                return {"success": False, "message": "Material not found"}
            
            # Check if sufficient stock available
            if material.quantity_available < quantity:
                return {
                    "success": False, 
                    "message": f"Insufficient stock! Available: {material.quantity_available}, Required: {quantity}"
                }
            
            # Store old stock for logging
            old_stock = material.quantity_available
            
            # Deduct material
            material.quantity_available -= quantity
            new_stock = material.quantity_available
            
            # Create consumption record
            consumption = MaterialConsumption(
                material_id=material_id,
                consumed_quantity=quantity,
                consumption_type=consumption_type,
                consumed_by=consumed_by,
                notes=notes,
                old_stock=old_stock,
                new_stock=new_stock
            )
            
            self.db.add(consumption)
            self.db.commit()
            
            # Check for low stock and create alerts
            self._check_low_stock_alert(material)
            
            # Create reorder suggestion if needed
            self._create_reorder_suggestion(material)
            
            return {
                "success": True, 
                "message": f"Consumed {quantity} units. New stock: {new_stock}",
                "new_stock": new_stock,
                "consumption_id": consumption.consumption_id
            }
            
        except Exception as e:
            self.db.rollback()
            return {"success": False, "message": f"Error: {str(e)}"}
    
    def _check_low_stock_alert(self, material: RawMaterial):
        """Check if material needs low stock alert"""
        current_stock = material.quantity_available
        
        # Define thresholds (can be made configurable)
        critical_threshold = 5.0  # Critical level
        warning_threshold = 15.0  # Warning level
        
        alert_type = None
        threshold = 0
        
        if current_stock <= critical_threshold:
            alert_type = "critical"
            threshold = critical_threshold
        elif current_stock <= warning_threshold:
            alert_type = "warning" 
            threshold = warning_threshold
        
        if alert_type:
            # Check if alert already exists for this material
            existing_alert = self.db.query(LowStockAlert).filter(
                LowStockAlert.material_id == material.material_id,
                LowStockAlert.is_acknowledged == False
            ).first()
            
            if not existing_alert:
                # Create new alert
                alert_message = f"🚨 {alert_type.upper()}: {material.material_name} is running low! Current stock: {current_stock:.1f} {material.unit}"
                
                alert = LowStockAlert(
                    material_id=material.material_id,
                    alert_type=alert_type,
                    current_stock=current_stock,
                    minimum_threshold=threshold,
                    alert_message=alert_message
                )
                
                self.db.add(alert)
                self.db.commit()

                # Notify management by email when a new active alert is created.
                email_result = send_low_stock_email_notification(
                    db_session=self.db,
                    material_name=material.material_name,
                    material_type=material.material_type,
                    current_stock=current_stock,
                    unit=material.unit,
                    threshold=threshold,
                    alert_type=alert_type,
                )
                if email_result.get("success") != "true":
                    print(f"Low stock email notification skipped/failed: {email_result.get('message')}")
    
    def _create_reorder_suggestion(self, material: RawMaterial):
        """Create automatic reorder suggestion based on consumption patterns"""
        try:
            # Get consumption history for last 30 days
            thirty_days_ago = datetime.utcnow() - timedelta(days=30)
            
            consumptions = self.db.query(MaterialConsumption).filter(
                MaterialConsumption.material_id == material.material_id,
                MaterialConsumption.consumption_date >= thirty_days_ago
            ).all()
            
            if not consumptions:
                return  # No consumption history
            
            # Calculate average daily consumption
            total_consumed = sum(c.consumed_quantity for c in consumptions)
            days_with_data = len(set(c.consumption_date.date() for c in consumptions))
            
            if days_with_data == 0:
                return
            
            avg_daily_consumption = total_consumed / days_with_data
            
            if avg_daily_consumption <= 0:
                return
            
            # Calculate days until stockout
            current_stock = material.quantity_available
            days_until_stockout = int(current_stock / avg_daily_consumption)
            
            # Only create suggestion if stock will run out soon
            if days_until_stockout <= 14:  # 2 weeks
                
                # Calculate suggested order quantity (30 days supply)
                suggested_quantity = avg_daily_consumption * 30
                
                # Determine urgency
                urgency = "low"
                if days_until_stockout <= 3:
                    urgency = "urgent"
                elif days_until_stockout <= 7:
                    urgency = "high" 
                elif days_until_stockout <= 14:
                    urgency = "medium"
                
                # Check if suggestion already exists
                existing_suggestion = self.db.query(MaterialReorderSuggestion).filter(
                    MaterialReorderSuggestion.material_id == material.material_id,
                    MaterialReorderSuggestion.is_processed == False
                ).first()
                
                if not existing_suggestion:
                    suggestion = MaterialReorderSuggestion(
                        material_id=material.material_id,
                        current_stock=current_stock,
                        average_daily_consumption=avg_daily_consumption,
                        days_until_stockout=days_until_stockout,
                        suggested_order_quantity=suggested_quantity,
                        suggested_order_date=datetime.utcnow() + timedelta(days=2),
                        urgency_level=urgency
                    )
                    
                    self.db.add(suggestion)
                    self.db.commit()
                    
        except Exception as e:
            print(f"Error creating reorder suggestion: {e}")
    
    def get_active_alerts(self) -> list:
        """Get all unacknowledged low stock alerts"""
        try:
            alerts = self.db.query(LowStockAlert).filter(
                LowStockAlert.is_acknowledged == False
            ).order_by(LowStockAlert.created_at.desc()).all()
            
            return alerts
        except Exception as e:
            print(f"Error fetching alerts: {e}")
            return []
    
    def get_reorder_suggestions(self) -> list:
        """Get unprocessed reorder suggestions"""
        try:
            suggestions = self.db.query(MaterialReorderSuggestion).filter(
                MaterialReorderSuggestion.is_processed == False
            ).order_by(MaterialReorderSuggestion.urgency_level.desc()).all()
            
            return suggestions
        except Exception as e:
            print(f"Error fetching suggestions: {e}")
            return []
    
    def acknowledge_alert(self, alert_id: int, user_id: int = 1):
        """Mark alert as acknowledged"""
        try:
            alert = self.db.query(LowStockAlert).filter(
                LowStockAlert.alert_id == alert_id
            ).first()
            
            if alert:
                alert.is_acknowledged = True
                alert.acknowledged_by = user_id
                alert.acknowledged_at = datetime.utcnow()
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error acknowledging alert: {e}")
            return False
    
    def process_reorder_suggestion(self, suggestion_id: int, user_id: int = 1):
        """Mark reorder suggestion as processed"""
        try:
            suggestion = self.db.query(MaterialReorderSuggestion).filter(
                MaterialReorderSuggestion.suggestion_id == suggestion_id 
            ).first()
            
            if suggestion:
                suggestion.is_processed = True
                suggestion.processed_by = user_id
                suggestion.processed_at = datetime.utcnow()
                self.db.commit()
                return True
            return False
        except Exception as e:
            print(f"Error processing suggestion: {e}")
            return False
    
    def get_consumption_history(self, material_id: int = None, days: int = 30) -> list:
        """Get material consumption history"""
        try:
            start_date = datetime.utcnow() - timedelta(days=days)
            
            query = self.db.query(MaterialConsumption).filter(
                MaterialConsumption.consumption_date >= start_date
            )
            
            if material_id:
                query = query.filter(MaterialConsumption.material_id == material_id)
            
            consumptions = query.order_by(MaterialConsumption.consumption_date.desc()).all()
            return consumptions
        except Exception as e:
            print(f"Error fetching consumption history: {e}")
            return []

# Global tracker instance
material_tracker = MaterialTracker()

def quick_consume_material(material_id: int, quantity: float, consumption_type: str = "production"):
    """Quick function to consume material from anywhere in the app"""
    return material_tracker.consume_material(
        material_id=material_id,
        quantity=quantity, 
        consumption_type=consumption_type
    )

def get_low_stock_alerts():
    """Quick function to get low stock alerts"""
    return material_tracker.get_active_alerts()

def display_alert_notifications():
    """Display alert notifications in Streamlit sidebar"""
    alerts = get_low_stock_alerts()
    
    if alerts:
        with st.sidebar:
            st.markdown("### 🚨 Low Stock Alerts")
            
            for alert in alerts[:5]:  # Show top 5 alerts
                if alert.alert_type == "critical":
                    st.error(f"🔴 CRITICAL: {alert.alert_message}")
                else:
                    st.warning(f"🟡 WARNING: {alert.alert_message}")
                
                if st.button(f"Acknowledge", key=f"ack_{alert.alert_id}"):
                    material_tracker.acknowledge_alert(alert.alert_id)
                    st.rerun()
            
            if len(alerts) > 5:
                st.info(f"... and {len(alerts) - 5} more alerts")