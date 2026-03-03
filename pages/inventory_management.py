import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
from config.database import SessionLocal
from models.database_models import RawMaterial, InventoryLog, ProductionOrder
from utils.helpers import (
    display_success_message, display_error_message, display_info_message,
    format_currency, format_date
)

def show():
    """Display Inventory Management module"""
    st.title("📊 Inventory Management")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Dashboard", "Transactions", "Low Stock", "Forecasting"])
    
    with tab1:
        show_dashboard()
    
    with tab2:
        show_transactions()
    
    with tab3:
        show_low_stock_alerts()
    
    with tab4:
        show_forecasting()

def show_dashboard():
    """Display inventory dashboard"""
    st.subheader("Inventory Dashboard")
    
    db = SessionLocal()
    try:
        materials = db.query(RawMaterial).all()
        
        if not materials:
            display_info_message("No materials in inventory")
            return
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_value = sum(m.quantity_available * m.cost_per_unit for m in materials)
        total_quantity = sum(m.quantity_available for m in materials)
        critical_count = sum(1 for m in materials if m.quantity_available < 10)
        
        with col1:
            st.metric("Total Items", len(materials))
        with col2:
            st.metric("Total Quantity", f"{total_quantity:.0f}")
        with col3:
            st.metric("Total Value", format_currency(total_value))
        with col4:
            st.metric("Critical Low Stock", critical_count)
        
        # Category-wise breakdown
        st.subheader("Category Breakdown")
        
        categories = {}
        for m in materials:
            cat = m.material_type
            if cat not in categories:
                categories[cat] = {"quantity": 0, "value": 0}
            categories[cat]["quantity"] += m.quantity_available
            categories[cat]["value"] += m.quantity_available * m.cost_per_unit
        
        cat_data = []
        for cat, data in categories.items():
            cat_data.append({
                "Category": cat,
                "Quantity": data["quantity"],
                "Value": data["value"]
            })
        
        col1, col2 = st.columns(2)
        
        with col1:
            df = pd.DataFrame(cat_data)
            fig = px.bar(df, x="Category", y="Quantity", title="Quantity by Category")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            fig = px.pie(df, values="Value", names="Category", title="Value by Category")
            st.plotly_chart(fig, width='stretch')
        
        # Material details table
        st.subheader("Material Details")
        
        data = []
        for m in materials:
            data.append({
                "Material": m.material_name,
                "Type": m.material_type,
                "Quantity": f"{m.quantity_available:.2f}",
                "Unit": m.unit,
                "Cost/Unit": format_currency(m.cost_per_unit),
                "Total Value": format_currency(m.quantity_available * m.cost_per_unit),
                "Status": m.status.value.upper()
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
        
    except Exception as e:
        display_error_message(f"Error loading dashboard: {e}")
    finally:
        db.close()

def show_transactions():
    """Display inventory transaction history"""
    st.subheader("Transaction History")
    
    db = SessionLocal()
    try:
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            transaction_type = st.multiselect(
                "Transaction Type",
                options=["IN", "OUT", "ADJUST"],
                default=["IN", "OUT", "ADJUST"]
            )
        
        with col2:
            days_back = st.slider("Show last N days", 1, 90, 30)
        
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days_back)
        
        logs = db.query(InventoryLog).filter(
            InventoryLog.transaction_type.in_(transaction_type),
            InventoryLog.recorded_at >= cutoff_date
        ).order_by(InventoryLog.recorded_at.desc()).all()
        
        if not logs:
            display_info_message("No transactions in selected period")
            return
        
        data = []
        for log in logs:
            material = db.query(RawMaterial).filter(RawMaterial.material_id == log.material_id).first()
            data.append({
                "Date": format_date(log.recorded_at),
                "Material": material.material_name if material else "Unknown",
                "Type": log.transaction_type,
                "Qty Change": f"{log.quantity_change:+.2f}",
                "Before": f"{log.quantity_before:.2f}",
                "After": f"{log.quantity_after:.2f}",
                "Reference": log.reference_id or "-",
                "Notes": log.notes or "-"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
        
        # Summary statistics
        st.subheader("Transaction Summary")
        
        col1, col2, col3 = st.columns(3)
        
        total_in = sum(l.quantity_change for l in logs if l.transaction_type == "IN")
        total_out = sum(l.quantity_change for l in logs if l.transaction_type == "OUT")
        total_adjust = sum(abs(l.quantity_change) for l in logs if l.transaction_type == "ADJUST")
        
        with col1:
            st.metric("Total In", f"{total_in:.0f}")
        with col2:
            st.metric("Total Out", f"{abs(total_out):.0f}")
        with col3:
            st.metric("Total Adjustments", f"{total_adjust:.0f}")
        
    except Exception as e:
        display_error_message(f"Error loading transactions: {e}")
    finally:
        db.close()

def show_low_stock_alerts():
    """Display low stock alerts"""
    st.subheader("Low Stock Alerts")
    
    db = SessionLocal()
    try:
        # Set threshold
        threshold = st.slider("Low Stock Threshold", 1, 100, 20)
        
        materials = db.query(RawMaterial).filter(RawMaterial.quantity_available < threshold).all()
        
        if not materials:
            st.success("✓ No materials below threshold")
            return
        
        # Critical items (less than 5)
        critical = [m for m in materials if m.quantity_available < 5]
        
        if critical:
            st.warning("⚠️ CRITICAL - Reorder Immediately")
            
            data = []
            for m in critical:
                data.append({
                    "Material": m.material_name,
                    "Current Qty": f"{m.quantity_available:.2f}",
                    "Unit": m.unit,
                    "Supplier": m.supplier,
                    "Cost/Unit": format_currency(m.cost_per_unit)
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, width='stretch', hide_index=True)
        
        # Low items (5 to threshold)
        low = [m for m in materials if 5 <= m.quantity_available < threshold]
        
        if low:
            st.info("ℹ LOW STOCK - Plan Reorder")
            
            data = []
            for m in low:
                data.append({
                    "Material": m.material_name,
                    "Current Qty": f"{m.quantity_available:.2f}",
                    "Unit": m.unit,
                    "Supplier": m.supplier,
                    "Cost/Unit": format_currency(m.cost_per_unit)
                })
            
            df = pd.DataFrame(data)
            st.dataframe(df, width='stretch', hide_index=True)
        
        # Action items
        st.subheader("Recommended Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if critical:
                st.error(f"🚨 Order {len(critical)} material(s) immediately")
        
        with col2:
            if low:
                st.warning(f"⚠️ Plan orders for {len(low)} material(s)")
        
    except Exception as e:
        display_error_message(f"Error loading alerts: {e}")
    finally:
        db.close()

def show_forecasting():
    """Display inventory forecasting"""
    st.subheader("Inventory Forecasting")
    
    db = SessionLocal()
    try:
        # Get active production orders
        orders = db.query(ProductionOrder).filter(
            ProductionOrder.status.in_(["pending", "in_progress"])
        ).all()
        
        if not orders:
            display_info_message("No active production orders for forecasting")
            return
        
        materials = db.query(RawMaterial).all()
        
        st.info("This section forecasts material consumption based on active orders")
        
        # Forecast data
        forecast_data = []
        for m in materials:
            current_qty = m.quantity_available
            
            # Estimate consumption (simplified - 10% per day)
            daily_consumption = (current_qty * 0.1) if current_qty > 0 else 0
            days_until_empty = (current_qty / daily_consumption) if daily_consumption > 0 else 999
            
            forecast_data.append({
                "Material": m.material_name,
                "Current Qty": f"{current_qty:.2f}",
                "Daily Consumption": f"{daily_consumption:.2f}",
                "Days Until Low": f"{min(days_until_empty, 999):.0f}",
                "Status": "Critical" if days_until_empty < 7 else "Low" if days_until_empty < 14 else "Adequate"
            })
        
        df = pd.DataFrame(forecast_data)
        st.dataframe(df, width='stretch', hide_index=True)
        
        # Forecast chart
        df_numeric = pd.DataFrame([
            {"Material": row["Material"], "Days Until Low": float(row["Days Until Low"].split()[0])}
            for row in forecast_data
        ])
        
        fig = px.bar(
            df_numeric,
            x="Material",
            y="Days Until Low",
            title="Days Until Stock Runs Low",
            color_discrete_sequence=["#ff0000"]
        )
        
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading forecast: {e}")
    finally:
        db.close()
