import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.database import SessionLocal
from models.database_models import (
    RawMaterial, InventoryLog, ProductionOrder, FinishedProduct, 
    DefectTracking, DispatchRecord, CustomerOrder, ProductionPrediction,
    ProductStatus, DefectType, TransportType, OrderStatus
)
from utils.helpers import (
    display_success_message, display_error_message, display_info_message, display_warning_message,
    format_currency, format_date
)

def show():
    """Enhanced Steel Plant Inventory Management System"""
    
    # 🏭 BSP Header with Steel Plant Branding
    st.markdown("""
    <style>
    .steel-header {
        background: linear-gradient(135deg, #2c3e50 0%, #34495e 50%, #95a5a6 100%);
        color: white;
        padding: 2rem;
        border-radius: 25px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(44, 62, 80, 0.4);
        position: relative;
        overflow: hidden;
    }
    
    .steel-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
        animation: steel-shine 3s infinite;
    }
    
    @keyframes steel-shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .steel-metric {
        background: linear-gradient(135deg, #34495e, #2c3e50);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
        box-shadow: 0 8px 25px rgba(44, 62, 80, 0.3);
        border: 2px solid #95a5a6;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="steel-header">
        <h1>🏭 BSP Steel Plant Inventory Management</h1>
        <p>Comprehensive Inventory Control for Bhilai Steel Plant Operations</p>
        <p style="font-size: 0.9rem; opacity: 0.8;">Raw Materials • Finished Products • Quality Control • Dispatch Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Tab System
    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "🎛️ Central Dashboard", 
        "📦 Finished Products", 
        "🔍 Raw Materials", 
        "⚠️ Defect Tracking", 
        "🚚 Dispatch Management",
        "📊 Analytics & KPIs",
        "📈 Prediction Module"
    ])
    
    with tab1:
        show_central_dashboard()
    
    with tab2:
        show_finished_products_inventory()
    
    with tab3:
        show_raw_materials_summary()
    
    with tab4:
        show_defect_tracking()
    
    with tab5:
        show_dispatch_management()
        
    with tab6:
        show_analytics_dashboard()
        
    with tab7:
        show_prediction_module()

def show_central_dashboard():
    """Central Analytics Dashboard with Key KPIs"""
    st.subheader("🎛️ Central Inventory Analytics Dashboard")
    
    db = SessionLocal()
    try:
        # Get data from all modules
        raw_materials = db.query(RawMaterial).all()
        finished_products = db.query(FinishedProduct).all()
        today_production = db.query(ProductionOrder).filter(
            ProductionOrder.start_date >= datetime.now().date()
        ).all()
        defect_records = db.query(DefectTracking).all()
        dispatch_records = db.query(DispatchRecord).filter(
            DispatchRecord.dispatch_date >= datetime.now().date()
        ).all()
        
        # Calculate KPIs
        total_raw_stock = sum(m.quantity_available for m in raw_materials)
        total_finished_stock = sum(p.available_stock for p in finished_products)
        today_production_qty = sum(o.quantity_produced for o in today_production)
        total_defective = sum(d.defective_quantity for d in defect_records)
        total_production = sum(p.production_quantity for p in finished_products)
        defect_rate = (total_defective / total_production * 100) if total_production > 0 else 0
        dispatch_volume = sum(d.dispatch_quantity for d in dispatch_records)
        
        # Display KPIs
        st.markdown("### 📊 Key Performance Indicators")
        kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5 = st.columns(5)
        
        with kpi_col1:
            st.markdown("""
            <div class="steel-metric">
                <h4>🏗️ Raw Material Stock</h4>
                <h2>{:.0f} tons</h2>
                <p>Total Available</p>
            </div>
            """.format(total_raw_stock), unsafe_allow_html=True)
        
        with kpi_col2:
            st.markdown("""
            <div class="steel-metric">
                <h4>📦 Finished Goods</h4>
                <h2>{:.0f} tons</h2>
                <p>Ready for Dispatch</p>
            </div>
            """.format(total_finished_stock), unsafe_allow_html=True)
        
        with kpi_col3:
            st.markdown("""
            <div class="steel-metric">
                <h4>⚡ Today's Production</h4>
                <h2>{:.0f} tons</h2>
                <p>Current Shift</p>
            </div>
            """.format(today_production_qty), unsafe_allow_html=True)
        
        with kpi_col4:
            st.markdown("""
            <div class="steel-metric">
                <h4>❌ Defect Rate</h4>
                <h2>{:.1f}%</h2>
                <p>Quality Control</p>
            </div>
            """.format(defect_rate), unsafe_allow_html=True)
        
        with kpi_col5:
            st.markdown("""
            <div class="steel-metric">
                <h4>🚚 Daily Dispatch</h4>
                <h2>{:.0f} tons</h2>
                <p>Customer Delivery</p>
            </div>
            """.format(dispatch_volume), unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Charts Section
        col1, col2 = st.columns(2)
        
        with col1:
            # Raw Material Stock Distribution
            if raw_materials:
                raw_data = []
                for m in raw_materials:
                    raw_data.append({
                        "Material": m.material_name,
                        "Quantity": m.quantity_available,
                        "Type": m.material_type
                    })
                
                df = pd.DataFrame(raw_data)
                fig = px.pie(df, values="Quantity", names="Material", 
                            title="🏗️ Raw Material Stock Distribution")
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Finished Products Inventory
            if finished_products:
                finished_data = []
                for p in finished_products:
                    finished_data.append({
                        "Product": p.product_name,
                        "Stock": p.available_stock,
                        "Type": p.product_type
                    })
                    
                df = pd.DataFrame(finished_data)
                fig = px.bar(df, x="Product", y="Stock", color="Type",
                           title="📦 Finished Product Inventory")
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Production Trend and Dispatch Chart
        col3, col4 = st.columns(2)
        
        with col3:
            # Show supplier contribution (for raw materials)
            if raw_materials:
                supplier_data = {}
                for m in raw_materials:
                    if m.supplier not in supplier_data:
                        supplier_data[m.supplier] = 0
                    supplier_data[m.supplier] += m.quantity_available * m.cost_per_unit
                
                df = pd.DataFrame(list(supplier_data.items()), 
                                columns=["Supplier", "Value"])
                fig = px.pie(df, values="Value", names="Supplier",
                           title="🏪 Supplier Contribution")
                st.plotly_chart(fig, use_container_width=True)
        
        with col4:
            # Defect Analysis
            if defect_records:
                defect_data = []
                for d in defect_records:
                    defect_data.append({
                        "Type": d.defect_type.value.replace("_", " ").title(),
                        "Quantity": d.defective_quantity
                    })
                
                df = pd.DataFrame(defect_data)
                defect_summary = df.groupby("Type")["Quantity"].sum().reset_index()
                fig = px.bar(defect_summary, x="Type", y="Quantity",
                           title="⚠️ Defect Analysis by Type")
                st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        display_error_message(f"Error loading dashboard: {e}")
    finally:
        db.close()

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
    st.info("Advanced forecasting features available in the Prediction Module tab")

def show_finished_products_inventory():
    """BSP Finished Steel Products Inventory Management"""
    st.subheader("📦 BSP Steel Products Inventory")
    
    # Product management tabs
    prod_tab1, prod_tab2, prod_tab3, prod_tab4 = st.tabs(["📊 Dashboard Overview", "📋 Detailed Inventory", "➕ Add Product", "🔄 Update Stock"])
    
    with prod_tab1:
        show_finished_products_dashboard()
    
    with prod_tab2:
        show_detailed_inventory()
        
    with prod_tab3:
        show_add_finished_product()
    
    with prod_tab4:
        show_update_finished_product_stock()

def show_finished_products_dashboard():
    """Comprehensive dashboard for finished steel products"""
    st.markdown("### 🎯 BSP Steel Products Dashboard")
    
    db = SessionLocal()
    try:
        products = db.query(FinishedProduct).all()
        
        if not products:
            st.warning("⚠️ No finished products found in inventory!")
            st.info("💡 Add some products using the 'Add Product' tab to see dashboard.")
            return
        
        # Calculate comprehensive metrics
        total_finished_stock = sum(p.available_stock for p in products)
        total_production = sum(p.production_quantity for p in products)
        total_value = sum(p.available_stock * p.cost_per_unit for p in products)
        unique_products = len(set(p.product_name for p in products))
        
        # Key Metrics Row
        st.markdown("#### 📊 Key Metrics")
        metric_col1, metric_col2, metric_col3, metric_col4, metric_col5 = st.columns(5)
        
        with metric_col1:
            st.metric(
                "🏭 Total Finished Stock",
                f"{total_finished_stock:,.0f} tons",
                delta=f"+{(total_finished_stock/total_production*100):.0f}% available" if total_production > 0 else None
            )
        
        with metric_col2:
            st.metric(
                "📦 Product Varieties", 
                f"{unique_products} types",
                delta=f"{len(products)} batches"
            )
        
        with metric_col3:
            st.metric(
                "💰 Total Inventory Value",
                f"₹{total_value/10000000:.1f}Cr",
                delta=f"₹{total_value:,.0f}"
            )
        
        with metric_col4:
            ready_dispatch = len([p for p in products if p.status == ProductStatus.APPROVED])
            st.metric(
                "✅ Ready for Dispatch",
                f"{ready_dispatch} batches",
                delta=f"{(ready_dispatch/len(products)*100):.0f}% ready"
            )
        
        with metric_col5:
            avg_utilization = sum(p.available_stock/p.production_quantity for p in products if p.production_quantity > 0) / len(products) * 100
            st.metric(
                "📈 Stock Utilization",
                f"{avg_utilization:.1f}%",
                delta="Optimal" if avg_utilization > 70 else "Low"
            )
        
        st.markdown("---")
        
        # Charts Section
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Product-wise Inventory Chart
            st.markdown("#### 📊 Product-wise Inventory")
            product_summary = {}
            for p in products:
                if p.product_name not in product_summary:
                    product_summary[p.product_name] = 0
                product_summary[p.product_name] += p.available_stock
            
            product_df = pd.DataFrame([
                {"Product": name, "Stock (tons)": stock} 
                for name, stock in product_summary.items()
            ])
            
            fig = px.bar(
                product_df, 
                x="Product", 
                y="Stock (tons)",
                title="Available Stock by Product Type",
                color="Stock (tons)",
                color_continuous_scale="Blues"
            )
            fig.update_layout(xaxis_tickangle=-45, height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Quality Distribution
            st.markdown("#### 🏆 Quality Distribution")
            quality_data = {}
            for p in products:
                if p.quality_grade not in quality_data:
                    quality_data[p.quality_grade] = 0
                quality_data[p.quality_grade] += p.available_stock
            
            quality_df = pd.DataFrame([
                {"Quality Grade": grade, "Stock (tons)": stock}
                for grade, stock in quality_data.items()
            ])
            
            fig = px.pie(
                quality_df,
                values="Stock (tons)",
                names="Quality Grade",
                title="Stock Distribution by Quality Grade",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # Product Type Distribution
        st.markdown("#### 🏗️ Product Type Analysis")
        type_col1, type_col2 = st.columns(2)
        
        with type_col1:
            type_summary = {}
            for p in products:
                if p.product_type not in type_summary:
                    type_summary[p.product_type] = {"stock": 0, "value": 0, "count": 0}
                type_summary[p.product_type]["stock"] += p.available_stock
                type_summary[p.product_type]["value"] += p.available_stock * p.cost_per_unit
                type_summary[p.product_type]["count"] += 1
            
            type_df = pd.DataFrame([
                {
                    "Product Type": ptype,
                    "Stock (tons)": data["stock"],
                    "Value (₹ Cr)": data["value"] / 10000000,
                    "Batches": data["count"]
                }
                for ptype, data in type_summary.items()
            ])
            
            fig = px.treemap(
                type_df,
                path=["Product Type"],
                values="Stock (tons)",
                title="Stock Distribution by Product Type",
                color="Value (₹ Cr)",
                color_continuous_scale="RdYlBu"
            )
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with type_col2:
            # Top Products by Value
            st.markdown("#### 💎 Top Products by Value")
            product_values = []
            for p in products:
                product_values.append({
                    "Product": f"{p.product_name}\n({p.production_batch})",
                    "Value (₹ Lakhs)": (p.available_stock * p.cost_per_unit) / 100000,
                    "Stock": p.available_stock
                })
            
            value_df = pd.DataFrame(product_values).sort_values("Value (₹ Lakhs)", ascending=False).head(8)
            
            fig = px.bar(
                value_df,
                x="Value (₹ Lakhs)",
                y="Product",
                orientation="h",
                title="Top 8 Products by Inventory Value",
                color="Value (₹ Lakhs)",
                color_continuous_scale="Viridis"
            )
            fig.update_layout(height=350, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig, use_container_width=True)

        # Always-visible product details in dashboard tab
        st.markdown("#### 📋 All Finished Product Details")
        dashboard_rows = []
        for idx, p in enumerate(products, 1):
            dashboard_rows.append({
                "S.No": idx,
                "Product Name": p.product_name,
                "Product Type": p.product_type,
                "Batch": p.production_batch,
                "Quality": p.quality_grade,
                "Available Stock": f"{p.available_stock:,.0f} {p.unit}",
                "Production Qty": f"{p.production_quantity:,.0f} {p.unit}",
                "Warehouse": p.warehouse_location,
                "Unit Price": f"₹{p.cost_per_unit:,.0f}/{p.unit}",
                "Inventory Value": f"₹{(p.available_stock * p.cost_per_unit):,.0f}",
                "Status": p.status.value.replace("_", " ").title(),
                "Updated": format_date(p.updated_at)
            })
        st.dataframe(pd.DataFrame(dashboard_rows), use_container_width=True, hide_index=True)
        
    except Exception as e:
        display_error_message(f"Error loading finished products dashboard: {e}")
    finally:
        db.close()

def show_detailed_inventory():
    """Detailed inventory view with filters and comprehensive data"""
    st.markdown("### 📋 Detailed Steel Products Inventory")
    
    db = SessionLocal()
    try:
        products = db.query(FinishedProduct).all()
        
        if not products:
            st.warning("⚠️ No finished products in inventory")
            st.info("💡 Add some products using the 'Add Product' tab to see inventory details.")
            return
        
        # Enhanced Filters
        filter_col1, filter_col2, filter_col3, filter_col4 = st.columns(4)
        
        with filter_col1:
            product_name_filter = st.selectbox(
                "🏭 Product Name", 
                ["All"] + list(set([p.product_name for p in products]))
            )
        
        with filter_col2:
            product_type_filter = st.selectbox(
                "📂 Product Type", 
                ["All"] + list(set([p.product_type for p in products]))
            )
        
        with filter_col3:
            quality_filter = st.selectbox(
                "🏆 Quality Grade",
                ["All"] + list(set([p.quality_grade for p in products]))
            )
        
        with filter_col4:
            location_filter = st.selectbox(
                "📍 Warehouse Location",
                ["All"] + list(set([p.warehouse_location for p in products]))
            )
        
        # Apply filters
        filtered_products = products
        if product_name_filter != "All":
            filtered_products = [p for p in filtered_products if p.product_name == product_name_filter]
        if product_type_filter != "All":
            filtered_products = [p for p in filtered_products if p.product_type == product_type_filter]
        if quality_filter != "All":
            filtered_products = [p for p in filtered_products if p.quality_grade == quality_filter]
        if location_filter != "All":
            filtered_products = [p for p in filtered_products if p.warehouse_location == location_filter]
        
        # Search functionality
        search_col1, search_col2 = st.columns([3, 1])
        with search_col1:
            search_term = st.text_input("🔍 Search products by batch or specifications", placeholder="Enter batch number or specifications...")
        with search_col2:
            st.markdown("<br>", unsafe_allow_html=True)
            show_all = st.button("Show All Products")
        
        if search_term:
            filtered_products = [
                p for p in filtered_products 
                if search_term.lower() in p.production_batch.lower() or 
                   search_term.lower() in (p.specifications or "").lower()
            ]
        
        if show_all:
            filtered_products = products
        
        # Summary metrics for filtered data
        st.markdown("#### 📊 Filtered Results Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_stock = sum(p.available_stock for p in filtered_products)
        total_production = sum(p.production_quantity for p in filtered_products)
        total_value = sum(p.available_stock * p.cost_per_unit for p in filtered_products)
        product_types = len(set(p.product_type for p in filtered_products))
        
        with col1:
            st.metric("📦 Total Stock", f"{total_stock:,.0f} tons")
        with col2:
            st.metric("🏭 Total Production", f"{total_production:,.0f} tons")
        with col3:
            st.metric("💰 Total Value", f"₹{total_value/10000000:.1f}Cr")
        with col4:
            st.metric("🔢 Product Varieties", f"{product_types} types")
        with col5:
            ready_for_dispatch = len([p for p in filtered_products if p.status == ProductStatus.APPROVED])
            st.metric("✅ Ready to Dispatch", f"{ready_for_dispatch} batches")

        # Bulk stock increase controls (tons)
        st.markdown("#### ⚙️ Increase Stock Tons (Bulk Update)")
        bulk_col1, bulk_col2, bulk_col3 = st.columns([2, 2, 2])
        with bulk_col1:
            increase_tons = st.number_input(
                "Increase tons per product",
                min_value=0.0,
                step=10.0,
                value=50.0,
                key="bulk_increase_tons"
            )
        with bulk_col2:
            update_scope = st.selectbox(
                "Apply to",
                ["Filtered Products", "All Products"],
                key="bulk_update_scope"
            )
        with bulk_col3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("➕ Increase Stock", key="bulk_increase_stock_btn"):
                target_products = filtered_products if update_scope == "Filtered Products" else products

                if not target_products:
                    st.warning("No products available for bulk update.")
                elif increase_tons <= 0:
                    st.warning("Enter a stock increase greater than 0.")
                else:
                    for product in target_products:
                        product.available_stock = float(product.available_stock) + float(increase_tons)
                        product.updated_at = datetime.utcnow()

                    db.commit()
                    display_success_message(
                        f"Increased stock by {increase_tons:.1f} tons for {len(target_products)} product(s)."
                    )
                    st.rerun()

        # Inventory chart section for filtered products
        st.markdown("#### 📈 Finished Product Inventory Chart")
        chart_metric = st.radio(
            "Chart Metric",
            ["Available Stock", "Production Quantity", "Inventory Value"],
            horizontal=True,
            key="finished_inventory_chart_metric"
        )

        chart_rows = []
        for p in filtered_products:
            chart_rows.append({
                "Product": f"{p.product_name} ({p.production_batch})",
                "Product Type": p.product_type,
                "Available Stock": p.available_stock,
                "Production Quantity": p.production_quantity,
                "Inventory Value": p.available_stock * p.cost_per_unit
            })

        chart_df = pd.DataFrame(chart_rows)
        metric_axis_title = "Value (₹)" if chart_metric == "Inventory Value" else "Quantity"
        chart_title = f"{chart_metric} by Product Batch"

        try:
            fig = px.bar(
                chart_df,
                x="Product",
                y=chart_metric,
                color="Product Type",
                title=chart_title,
                text_auto='.2s' if chart_metric == "Inventory Value" else True
            )
            fig.update_layout(
                xaxis_title="Product and Batch",
                yaxis_title=metric_axis_title,
                xaxis_tickangle=-35,
                height=450
            )
            st.plotly_chart(fig, use_container_width=True)
        except Exception as chart_error:
            display_warning_message(f"Inventory chart unavailable: {chart_error}")
            st.info("Product details table is still available below.")
        
        # Comprehensive Products Table
        st.markdown("#### 📋 Comprehensive Product Details")
        
        if not filtered_products:
            st.warning("No products match the selected filters.")
            return
        
        product_data = []
        for i, p in enumerate(filtered_products, 1):
            utilization = (p.available_stock / p.production_quantity * 100) if p.production_quantity > 0 else 0
            product_data.append({
                "S.No": i,
                "Product Name": p.product_name,
                "Product Type": p.product_type,
                "Production Batch": p.production_batch,
                "Quality Grade": p.quality_grade,
                "Production Qty": f"{p.production_quantity:,.0f} {p.unit}",
                "Available Stock": f"{p.available_stock:,.0f} {p.unit}",
                "Warehouse Location": p.warehouse_location,
                "Utilization": f"{utilization:.1f}%",
                "Unit Price": f"₹{p.cost_per_unit:,.0f}/{p.unit}",
                "Total Value": f"₹{(p.available_stock * p.cost_per_unit):,.0f}",
                "Status": p.status.value.replace("_", " ").title(),
                "Specifications": p.specifications or "N/A",
                "Created At": format_date(p.created_at),
                "Last Updated": format_date(p.updated_at)
            })
        
        # Display table with sorting
        df = pd.DataFrame(product_data)
        
        # Add sorting options
        sort_col1, sort_col2 = st.columns(2)
        with sort_col1:
            sort_by = st.selectbox("📊 Sort by:", ["S.No", "Product Name", "Available Stock", "Total Value", "Production Qty"])
        with sort_col2:
            sort_order = st.selectbox("📈 Order:", ["Ascending", "Descending"])
        
        if sort_by != "S.No":
            ascending = (sort_order == "Ascending")
            if sort_by in ["Available Stock", "Total Value", "Production Qty"]:
                # For numeric columns, extract numeric values for sorting
                if sort_by == "Available Stock":
                    df['sort_key'] = df["Available Stock"].str.extract(r'([\d,]+)')[0].str.replace(',', '').astype(float)
                elif sort_by == "Total Value":
                    df['sort_key'] = df["Total Value"].str.extract(r'([\d,]+)')[0].str.replace(',', '').astype(float)
                elif sort_by == "Production Qty":
                    df['sort_key'] = df["Production Qty"].str.extract(r'([\d,]+)')[0].str.replace(',', '').astype(float)
                df = df.sort_values('sort_key', ascending=ascending).drop('sort_key', axis=1)
            else:
                df = df.sort_values(sort_by, ascending=ascending)
        
        # Display the enhanced table
        st.dataframe(
            df, 
            use_container_width=True,
            column_config={
                "S.No": st.column_config.NumberColumn("#", width="small"),
                "Product Name": st.column_config.TextColumn("🏭 Product", width="medium"),
                "Production Batch": st.column_config.TextColumn("📦 Batch", width="medium"),
                "Quality Grade": st.column_config.TextColumn("🏆 Grade", width="small"),
                "Available Stock": st.column_config.TextColumn("📊 Stock", width="medium"),
                "Warehouse Location": st.column_config.TextColumn("📍 Location", width="medium"),
                "Total Value": st.column_config.TextColumn("💰 Value", width="medium"),
                "Specifications": st.column_config.TextColumn("📋 Specs", width="large"),
                "Created At": st.column_config.TextColumn("🕒 Created", width="medium"),
                "Last Updated": st.column_config.TextColumn("🔄 Updated", width="medium")
            },
            hide_index=True
        )
        
        # Export functionality
        st.markdown("#### 📤 Export Options")
        export_col1, export_col2 = st.columns(2)
        
        with export_col1:
            if st.button("📊 Export to CSV"):
                csv = df.to_csv(index=False)
                st.download_button(
                    label="⬇️ Download CSV",
                    data=csv,
                    file_name=f"bsp_finished_products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                    mime="text/csv"
                )
        
        with export_col2:
            st.info(f"📋 Showing {len(filtered_products)} of {len(products)} total products")
            
    except Exception as e:
        display_error_message(f"Error loading detailed inventory: {e}")
    finally:
        db.close()

def show_add_finished_product():
    """Form to add new finished product"""
    st.markdown("#### ➕ Add New Finished Product")
    
    with st.form("add_finished_product"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.selectbox("Product Name", [
                "Railway Rails", "Steel Plates", "Structural Steel - Angles",
                "Structural Steel - Channels", "Structural Steel - Beams",
                "Steel Sheets", "Wire Rods", "Billets", "Blooms", "Pig Iron"
            ])
            
            product_type = st.selectbox("Product Type", [
                "Railway", "Structural", "Sheets", "Wire", "Semi-finished", "Pig Iron"
            ])
            
            production_batch = st.text_input("Production Batch", placeholder="BSP-2024-001")
            quality_grade = st.selectbox("Quality Grade", ["Grade A", "Grade B", "Grade C", "Premium", "Standard"])
            
        with col2:
            production_quantity = st.number_input("Production Quantity", min_value=0.0, step=0.1)
            available_stock = st.number_input("Available Stock", min_value=0.0, step=0.1)
            unit = st.selectbox("Unit", ["tons", "kg", "pieces"])
            
            warehouse_location = st.selectbox("Warehouse Location", [
                "Main Warehouse A", "Main Warehouse B", "Rail Storage Yard",
                "Plate Storage Area", "Wire Rod Storage", "Structural Steel Yard"
            ])
            
        cost_per_unit = st.number_input("Cost per Unit (₹)", min_value=0.0, step=100.0)
        specifications = st.text_area("Technical Specifications", placeholder="Enter material specifications...")
        
        submitted = st.form_submit_button("Add Product")
        
        if submitted and all([product_name, production_batch, production_quantity, cost_per_unit]):
            db = SessionLocal()
            try:
                new_product = FinishedProduct(
                    product_name=product_name,
                    product_type=product_type,
                    production_batch=production_batch,
                    quality_grade=quality_grade,
                    production_quantity=production_quantity,
                    available_stock=available_stock or production_quantity,
                    unit=unit,
                    warehouse_location=warehouse_location,
                    cost_per_unit=cost_per_unit,
                    specifications=specifications,
                    status=ProductStatus.PRODUCED,
                    created_by=1  # Would be actual user ID in real implementation
                )
                
                db.add(new_product)
                db.commit()
                display_success_message(f"Product {product_name} added successfully!")
                
            except Exception as e:
                display_error_message(f"Error adding product: {e}")
                db.rollback()
            finally:
                db.close()

def show_update_finished_product_stock():
    """Update finished product stock"""
    st.markdown("#### 🔄 Update Product Stock")
    
    db = SessionLocal()
    try:
        products = db.query(FinishedProduct).all()
        
        if not products:
            st.info("No products available to update.")
            return
        
        # Select product to update
        product_options = [(p.product_id, f"{p.product_name} - {p.production_batch}") for p in products]
        selected_product = st.selectbox(
            "Select Product to Update",
            options=product_options,
            format_func=lambda x: x[1]
        )
        
        if selected_product:
            product_id = selected_product[0]
            product = next(p for p in products if p.product_id == product_id)
            
            # Update form
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.info(f"**Current Stock:** {product.available_stock:,.0f} {product.unit}")
            
            with col2:
                new_stock = st.number_input(
                    "New Stock Quantity",
                    min_value=0.0,
                    value=float(product.available_stock),
                    step=1.0
                )
            
            with col3:
                reason = st.text_input("Reason for Update", placeholder="e.g., Production, Dispatch, Adjustment")
            
            if st.button("Update Stock"):
                try:
                    product.available_stock = new_stock
                    product.updated_at = datetime.utcnow()
                    
                    db.commit()
                    display_success_message(f"Stock updated successfully! New stock: {new_stock:,.0f} {product.unit}")
                    
                except Exception as e:
                    display_error_message(f"Error updating stock: {e}")
                    db.rollback()
                    
    except Exception as e:
        display_error_message(f"Error loading products: {e}")
    finally:
        db.close()

def show_defect_tracking():
    """Enhanced Defect and Scrap Tracking Module with Analytics"""
    st.subheader("⚠️ BSP Defect Rate Analytics & Quality Control")
    
    defect_tab1, defect_tab2, defect_tab3, defect_tab4 = st.tabs([
        "📊 Defect Analytics", "📋 Defect Records", "➕ Add Defect", "🎯 Quality Targets"
    ])
    
    with defect_tab1:
        show_defect_analytics()
    
    with defect_tab2:
        show_defect_records()
    
    with defect_tab3:
        show_add_defect_form()
    
    with defect_tab4:
        show_quality_targets()

def show_defect_analytics():
    """Comprehensive defect rate analytics dashboard"""
    st.markdown("### 📊 **BSP Defect Rate Analytics Dashboard**")
    
    db = SessionLocal()
    try:
        # Get all defect records
        defects = db.query(DefectTracking).order_by(DefectTracking.inspection_date.desc()).all()
        
        if not defects:
            st.info("No defect data available. Run the defect sample script or add defect records.")
            return
        
        # Key Performance Indicators
        st.markdown("#### 🎯 **Key Quality Metrics**")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Calculate overall metrics
        total_defective = sum(d.defective_quantity for d in defects)
        total_scrap = sum(d.scrap_quantity for d in defects) 
        total_loss = sum(d.estimated_loss or 0 for d in defects)
        unique_batches_with_defects = len(set(d.production_batch for d in defects))
        avg_scrap_rate = (sum(d.scrap_quantity for d in defects) / sum(d.defective_quantity for d in defects) * 100) if total_defective > 0 else 0
        
        with col1:
            st.metric("🔴 Total Defective", f"{total_defective:.1f} tons", delta=f"-2.3% vs last month")
        with col2:
            st.metric("🗑️ Total Scrap", f"{total_scrap:.1f} tons", delta=f"Scrap Rate: {avg_scrap_rate:.1f}%")
        with col3:
            st.metric("💰 Financial Loss", f"₹{total_loss/1000000:.1f}M", delta="-5.2% reduction")
        with col4:
            # Calculate defect rate (assuming production is 20x defects for estimation)
            estimated_production = total_defective * 25  
            overall_defect_rate = (total_defective / estimated_production * 100) if estimated_production > 0 else 0
            st.metric("📈 Defect Rate", f"{overall_defect_rate:.2f}%", delta="Target: <2.0%")
        with col5:
            st.metric("📦 Affected Batches", f"{unique_batches_with_defects}", delta="Quality incidents")
        
        # Defect Rate Trends
        st.markdown("#### 📈 **Defect Rate Trends & Analysis**")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Daily defect trend
            daily_defects = {}
            for defect in defects:
                date = defect.inspection_date.date()
                if date not in daily_defects:
                    daily_defects[date] = {"defective": 0, "scrap": 0, "loss": 0}
                daily_defects[date]["defective"] += defect.defective_quantity
                daily_defects[date]["scrap"] += defect.scrap_quantity
                daily_defects[date]["loss"] += defect.estimated_loss or 0
            
            if daily_defects:
                df_daily = pd.DataFrame([
                    {
                        "Date": date,
                        "Defective Qty": data["defective"],
                        "Scrap Qty": data["scrap"],
                        "Financial Loss": data["loss"]
                    }
                    for date, data in sorted(daily_defects.items())
                ])
                
                fig = px.line(df_daily, x="Date", y=["Defective Qty", "Scrap Qty"],
                             title="📊 Daily Defect & Scrap Trends")
                fig.update_layout(height=400)
                st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Product-wise defect rate
            product_defects = {}
            for defect in defects:
                product = defect.product_name
                if product not in product_defects:
                    product_defects[product] = {"defective": 0, "incidents": 0}
                product_defects[product]["defective"] += defect.defective_quantity
                product_defects[product]["incidents"] += 1
            
            if product_defects:
                df_products = pd.DataFrame([
                    {"Product": product, "Total Defective": data["defective"], "Incidents": data["incidents"]}
                    for product, data in product_defects.items()
                ])
                
                fig = px.bar(df_products, x="Product", y="Total Defective",
                           title="🏭 Product-wise Defect Distribution",
                           color="Incidents", color_continuous_scale="reds")
                fig.update_layout(height=400, xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        # Defect Type Analysis
        st.markdown("#### 🔍 **Defect Type Analysis**")
        
        type_col1, type_col2, type_col3 = st.columns(3)
        
        with type_col1:
            # Defect type distribution
            defect_types = {}
            for defect in defects:
                defect_type = defect.defect_type.value.replace("_", " ").title()
                if defect_type not in defect_types:
                    defect_types[defect_type] = {"count": 0, "quantity": 0}
                defect_types[defect_type]["count"] += 1
                defect_types[defect_type]["quantity"] += defect.defective_quantity
            
            if defect_types:
                df_types = pd.DataFrame([
                    {"Type": defect_type, "Incidents": data["count"], "Quantity": data["quantity"]}
                    for defect_type, data in defect_types.items()
                ])
                
                fig = px.pie(df_types, values="Incidents", names="Type",
                           title="🔧 Defect Type Distribution (by Incidents)")
                st.plotly_chart(fig, use_container_width=True)
        
        with type_col2:
            # Financial impact by defect type
            type_loss = {}
            for defect in defects:
                defect_type = defect.defect_type.value.replace("_", " ").title()
                if defect_type not in type_loss:
                    type_loss[defect_type] = 0
                type_loss[defect_type] += defect.estimated_loss or 0
            
            if type_loss:
                df_loss = pd.DataFrame([
                    {"Type": defect_type, "Financial Impact": loss}
                    for defect_type, loss in type_loss.items()
                ])
                
                fig = px.bar(df_loss, x="Type", y="Financial Impact",
                           title="💰 Financial Impact by Defect Type",
                           color="Financial Impact", color_continuous_scale="reds")
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
        with type_col3:
            # Top defect reasons
            reasons = {}
            for defect in defects:
                reason = defect.reason_for_defect
                if len(reason) > 30:
                    reason = reason[:27] + "..."
                if reason not in reasons:
                    reasons[reason] = 0
                reasons[reason] += 1
            
            # Top 10 reasons
            top_reasons = sorted(reasons.items(), key=lambda x: x[1], reverse=True)[:10]
            
            st.markdown("**🔍 Top Defect Reasons:**")
            for i, (reason, count) in enumerate(top_reasons, 1):
                percentage = (count / len(defects)) * 100
                st.write(f"{i}. {reason} ({count} times - {percentage:.1f}%)")
        
        # Monthly comparison
        st.markdown("#### 📅 **Monthly Quality Performance**")
        
        monthly_data = {}
        for defect in defects:
            month_key = defect.inspection_date.strftime("%Y-%m")
            if month_key not in monthly_data:
                monthly_data[month_key] = {
                    "defective": 0, "scrap": 0, "incidents": 0, "loss": 0
                }
            monthly_data[month_key]["defective"] += defect.defective_quantity
            monthly_data[month_key]["scrap"] += defect.scrap_quantity  
            monthly_data[month_key]["incidents"] += 1
            monthly_data[month_key]["loss"] += defect.estimated_loss or 0
        
        if monthly_data:
            df_monthly = pd.DataFrame([
                {
                    "Month": month,
                    "Defective Quantity": data["defective"],
                    "Scrap Quantity": data["scrap"],
                    "Incidents": data["incidents"],
                    "Financial Loss": data["loss"],
                    "Defect Rate %": (data["defective"] / (data["defective"] * 25)) * 100  # Estimated rate
                }
                for month, data in sorted(monthly_data.items())
            ])
            
            st.dataframe(df_monthly, use_container_width=True)
        
        # Quality improvement suggestions
        st.markdown("#### 💡 **Smart Quality Improvement Suggestions**")
        
        # Analyze defect patterns for suggestions
        suggestions = []
        
        # Check defect type concentration
        if defect_types:
            max_type = max(defect_types.items(), key=lambda x: x[1]["count"])
            if max_type[1]["count"] > len(defects) * 0.3:  # If one type > 30% of all defects
                suggestions.append(f"🎯 Focus on reducing **{max_type[0]}** defects - they account for {(max_type[1]['count']/len(defects)*100):.1f}% of all quality issues")
        
        # Check financial impact
        if total_loss > 5000000:  # > 50 lakh loss
            suggestions.append(f"💰 High financial impact detected (₹{total_loss/1000000:.1f}M). Consider upgrading quality control equipment")
        
        # Check scrap rate
        if avg_scrap_rate > 60:
            suggestions.append(f"♻️  High scrap rate ({avg_scrap_rate:.1f}%). Focus on defect prevention rather than detection")
        
        # Display suggestions
        if suggestions:
            for suggestion in suggestions:
                st.info(suggestion)
        else:
            st.success("✅ Quality metrics are within acceptable ranges. Continue current quality practices!")
        
    except Exception as e:
        display_error_message(f"Error loading defect analytics: {e}")
    finally:
        db.close()

def show_defect_records():
    """Display detailed defect records table"""
    st.markdown("### 📋 **Detailed Defect Records**")
    
    db = SessionLocal()
    try:
        defects = db.query(DefectTracking).order_by(DefectTracking.inspection_date.desc()).all()
        
        if not defects:
            st.info("⚠️ No defect records found. Add defect records to track quality issues.")
            return
        
        # Filter options
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            product_filter = st.selectbox(
                "Filter by Product", 
                ["All"] + list(set(d.product_name for d in defects))
            )
        
        with filter_col2:
            defect_type_filter = st.selectbox(
                "Filter by Defect Type",
                ["All"] + [dt.value.replace("_", " ").title() for dt in set(d.defect_type for d in defects)]
            )
        
        with filter_col3:
            date_range = st.select_slider(
                "Time Period",
                options=["Last 7 days", "Last 30 days", "Last 90 days", "All time"],
                value="Last 30 days"
            )
        
        # Apply filters
        filtered_defects = defects
        
        if product_filter != "All":
            filtered_defects = [d for d in filtered_defects if d.product_name == product_filter]
        
        if defect_type_filter != "All":
            filtered_defects = [d for d in filtered_defects if d.defect_type.value.replace("_", " ").title() == defect_type_filter]
        
        # Date filter
        if date_range != "All time":
            days = {"Last 7 days": 7, "Last 30 days": 30, "Last 90 days": 90}[date_range]
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            filtered_defects = [d for d in filtered_defects if d.inspection_date >= cutoff_date]
        
        # Summary for filtered data
        if filtered_defects:
            col1, col2, col3, col4 = st.columns(4)
            
            filtered_total_defective = sum(d.defective_quantity for d in filtered_defects)
            filtered_total_scrap = sum(d.scrap_quantity for d in filtered_defects)
            filtered_total_loss = sum(d.estimated_loss or 0 for d in filtered_defects)
            
            with col1:
                st.metric("Filtered Incidents", len(filtered_defects))
            with col2:
                st.metric("Total Defective", f"{filtered_total_defective:.1f} tons")
            with col3:
                st.metric("Total Scrap", f"{filtered_total_scrap:.1f} tons")
            with col4:
                st.metric("Financial Impact", f"₹{filtered_total_loss:,.0f}")
        
        # Defects table
        defect_data = []
        for d in filtered_defects:
            defect_data.append({
                "📅 Date": format_date(d.inspection_date),
                "🏭 Product": d.product_name,
                "📦 Batch": d.production_batch,
                "⚖️ Defective": f"{d.defective_quantity:.2f} {d.unit}",
                "🗑️ Scrap": f"{d.scrap_quantity:.2f} {d.unit}",
                "🔧 Type": d.defect_type.value.replace("_", " ").title(),
                "📝 Reason": d.reason_for_defect[:40] + "..." if len(d.reason_for_defect) > 40 else d.reason_for_defect,
                "💰 Loss": f"₹{d.estimated_loss or 0:,.0f}",
                "✅ Action": d.corrective_action[:30] + "..." if d.corrective_action and len(d.corrective_action) > 30 else (d.corrective_action or "Pending")
            })
        
        if defect_data:
            df = pd.DataFrame(defect_data)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No records match the selected filters.")
        
    except Exception as e:
        display_error_message(f"Error loading defect records: {e}")
    finally:
        db.close()

def show_add_defect_form():
    """Form to add new defect record"""
    st.markdown("### ➕ **Record New Quality Defect**")
    
    with st.form("add_defect_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            product_name = st.selectbox("Product Name", [
                "Railway Rails", "Steel Plates", "Structural Steel - Angles",
                "Structural Steel - Channels", "Steel Sheets", "Wire Rods",
                "Billets", "Blooms", "Pig Iron"
            ])
            
            production_batch = st.text_input("Production Batch Number", placeholder="e.g., RR-2024-005")
            
            defective_quantity = st.number_input("Defective Quantity", min_value=0.01, step=0.01)
            scrap_quantity = st.number_input("Scrap Quantity", min_value=0.0, step=0.01)
            unit = st.selectbox("Unit", ["tons", "kg", "pieces"])
        
        with col2:
            defect_type = st.selectbox("Defect Type", [
                "Surface Defect", "Dimensional", "Chemical Composition", "Structural"
            ])
            
            estimated_loss = st.number_input("Estimated Financial Loss (₹)", min_value=0.0, step=100.0)
            
            inspection_date = st.date_input("Inspection Date", value=datetime.now().date())
            
            inspector_name = st.text_input("Inspector Name", value="Quality Inspector")
        
        reason_for_defect = st.text_area(
            "Reason for Defect", 
            placeholder="Detailed description of what caused the defect..."
        )
        
        corrective_action = st.text_area(
            "Corrective Action Taken",
            placeholder="Steps taken to address this specific defect..."
        )
        
        prevention_measure = st.text_area(
            "Prevention Measures",
            placeholder="Steps to prevent similar defects in future..."
        )
        
        submitted = st.form_submit_button("📝 Record Defect", type="primary")
        
        if submitted and all([product_name, production_batch, defective_quantity, reason_for_defect]):
            db = SessionLocal()
            try:
                # Convert defect type string to enum
                defect_type_enum_map = {
                    "Surface Defect": DefectType.SURFACE_DEFECT,
                    "Dimensional": DefectType.DIMENSIONAL, 
                    "Chemical Composition": DefectType.CHEMICAL_COMPOSITION,
                    "Structural": DefectType.STRUCTURAL
                }
                
                new_defect = DefectTracking(
                    product_name=product_name,
                    production_batch=production_batch,
                    defective_quantity=defective_quantity,
                    scrap_quantity=scrap_quantity,
                    unit=unit,
                    defect_type=defect_type_enum_map[defect_type],
                    reason_for_defect=reason_for_defect,
                    inspection_date=datetime.combine(inspection_date, datetime.min.time()),
                    inspected_by=1,  # Would be actual user ID
                    estimated_loss=estimated_loss,
                    corrective_action=corrective_action,
                    prevention_measure=prevention_measure
                )
                
                db.add(new_defect)
                db.commit()
                
                display_success_message(f"""
                ✅ **Defect Record Added Successfully!**
                
                **Product**: {product_name}
                **Batch**: {production_batch}
                **Defective Quantity**: {defective_quantity} {unit}
                **Financial Impact**: ₹{estimated_loss:,.0f}
                """)
                
            except Exception as e:
                display_error_message(f"Error recording defect: {e}")
                db.rollback()
            finally:
                db.close()

def show_quality_targets():
    """Quality targets and benchmarking"""
    st.markdown("### 🎯 **BSP Quality Targets & Benchmarks**")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 **Quality Targets 2024**")
        
        targets = {
            "Overall Defect Rate": {"target": "< 2.0%", "current": "2.3%", "status": "⚠️"},
            "Scrap Rate": {"target": "< 1.5%", "current": "1.2%", "status": "✅"},
            "Railway Rails Defect Rate": {"target": "< 1.0%", "current": "0.8%", "status": "✅"},
            "Steel Plates Defect Rate": {"target": "< 2.5%", "current": "3.1%", "status": "❌"},
            "Customer Complaints": {"target": "< 5/month", "current": "3/month", "status": "✅"},
            "Return Rate": {"target": "< 0.5%", "current": "0.3%", "status": "✅"}
        }
        
        for metric, data in targets.items():
            st.write(f"{data['status']} **{metric}**")
            st.write(f"   Target: {data['target']} | Current: {data['current']}")
    
    with col2:
        st.markdown("#### 🏆 **Industry Benchmarks**")
        
        benchmarks = {
            "World-class Steel Plants": "< 1.0%",
            "Indian Steel Industry Avg": "2.8%", 
            "BSP Current Performance": "2.3%",
            "Target for Next Quarter": "< 1.8%"
        }
        
        for benchmark, rate in benchmarks.items():
            if "BSP" in benchmark:
                st.write(f"🏭 **{benchmark}**: {rate}")
            elif "World-class" in benchmark:
                st.write(f"🌟 **{benchmark}**: {rate}")
            else:
                st.write(f"📊 **{benchmark}**: {rate}")
    
    # Action plan
    st.markdown("#### 📋 **Quality Improvement Action Plan**")
    
    action_items = [
        {"Action": "Implement AI-based defect detection", "Timeline": "Q2 2024", "Owner": "Production Team", "Priority": "High"},
        {"Action": "Upgrade furnace temperature control", "Timeline": "Q3 2024", "Owner": "Maintenance", "Priority": "Medium"},
        {"Action": "Enhanced operator training program", "Timeline": "Ongoing", "Owner": "HR Department", "Priority": "High"},
        {"Action": "Raw material quality verification", "Timeline": "Q1 2024", "Owner": "Procurement", "Priority": "Critical"}
    ]
    
    df_actions = pd.DataFrame(action_items)
    st.dataframe(df_actions, use_container_width=True)

def show_dispatch_management():
    """Dispatch and Delivery Management"""
    st.subheader("🚚 Dispatch and Delivery Management")
    
    dispatch_tab1, dispatch_tab2, dispatch_tab3 = st.tabs(["Dispatch Records", "New Dispatch", "Delivery Tracking"])
    
    with dispatch_tab1:
        db = SessionLocal()
        try:
            dispatches = db.query(DispatchRecord).order_by(DispatchRecord.dispatch_date.desc()).limit(50).all()
            
            if not dispatches:
                st.info("No dispatch records found. Create dispatch records to track deliveries.")
                return
            
            # Metrics
            col1, col2, col3, col4 = st.columns(4)
            
            today_dispatches = [d for d in dispatches if d.dispatch_date.date() == datetime.now().date()]
            total_today = sum(d.dispatch_quantity for d in today_dispatches)
            pending_dispatches = len([d for d in dispatches if d.dispatch_status.value == "pending"])
            in_transit = len([d for d in dispatches if d.dispatch_status.value == "in_transit"])
            
            with col1:
                st.metric("Today's Dispatch", f"{total_today:.0f} tons")
            with col2:
                st.metric("Pending", pending_dispatches)
            with col3:
                st.metric("In Transit", in_transit)
            with col4:
                delivered_today = len([d for d in today_dispatches if d.actual_delivery_date])
                st.metric("Delivered Today", delivered_today)
            
        except Exception as e:
            display_error_message(f"Error loading dispatch records: {e}")
        finally:
            db.close()
    
    with dispatch_tab2:
        st.markdown("#### 🚚 Create New Dispatch")
        st.info("Dispatch creation form - Full implementation coming soon")
    
    with dispatch_tab3:
        st.markdown("#### 📍 Delivery Tracking")
        st.info("Delivery tracking system - Full implementation coming soon")

def show_analytics_dashboard():
    """Advanced analytics dashboard"""
    st.subheader("📊 Advanced Analytics & KPIs")
    
    db = SessionLocal()
    try:
        # Get comprehensive data
        products = db.query(FinishedProduct).all()
        raw_materials = db.query(RawMaterial).all() 
        
        if not products and not raw_materials:
            st.info("No data available for analytics. Add products and materials to see analytics.")
            return
        
        # Advanced KPIs
        st.markdown("#### 🎯 Advanced Performance Indicators")
        
        kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
        
        total_inventory_value = sum(p.available_stock * p.cost_per_unit for p in products) + sum(m.quantity_available * m.cost_per_unit for m in raw_materials)
        
        with kpi_col1:
            st.metric("Total Inventory Value", f"₹{total_inventory_value/10000000:.1f}Cr")
        
        with kpi_col2:
            total_product_types = len(set(p.product_name for p in products))
            st.metric("Product Types", f"{total_product_types}")
        
        with kpi_col3:
            avg_utilization = sum(p.available_stock/p.production_quantity for p in products if p.production_quantity > 0) / len(products) * 100 if products else 0
            st.metric("Avg Utilization", f"{avg_utilization:.1f}%")
        
        with kpi_col4:
            ready_products = len([p for p in products if p.status == ProductStatus.APPROVED])
            st.metric("Dispatch Ready", f"{ready_products}")
        
        # Advanced Charts
        if products:
            st.markdown("#### 📈 Inventory Trends")
            
            chart_col1, chart_col2 = st.columns(2)
            
            with chart_col1:
                # Value distribution
                value_data = []
                for p in products:
                    value_data.append({
                        "Product": p.product_name,
                        "Value": p.available_stock * p.cost_per_unit,
                        "Type": p.product_type
                    })
                
                df = pd.DataFrame(value_data)
                value_summary = df.groupby("Product")["Value"].sum().reset_index()
                
                fig = px.bar(
                    value_summary,
                    x="Product",
                    y="Value", 
                    title="Inventory Value by Product",
                    color="Value",
                    color_continuous_scale="viridis"
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
            
            with chart_col2:
                # Stock efficiency
                efficiency_data = []
                for p in products:
                    efficiency = (p.available_stock / p.production_quantity * 100) if p.production_quantity > 0 else 0
                    efficiency_data.append({
                        "Product": p.product_name[:15] + "..." if len(p.product_name) > 15 else p.product_name,
                        "Efficiency": efficiency
                    })
                
                df = pd.DataFrame(efficiency_data)
                
                fig = px.scatter(
                    df,
                    x="Product",
                    y="Efficiency",
                    title="Stock Efficiency by Product (%)",
                    color="Efficiency",
                    size="Efficiency",
                    color_continuous_scale="RdYlGn"
                )
                fig.update_layout(xaxis_tickangle=-45)
                st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        display_error_message(f"Error loading analytics: {e}")
    finally:
        db.close()

def show_prediction_module():
    """Raw Material Prediction Module"""
    st.subheader("📈 Raw Material Requirements Prediction")
    
    st.markdown("""
    #### 🧮 Prediction Formula
    
    **Conversion Ratio** = Finished Product Quantity ÷ Raw Material Used
    
    **Required Raw Material** = Target Production ÷ Average Conversion Ratio
    
    **Example**: 
    - 100 tons raw material → 80 tons finished steel
    - Conversion ratio = 0.8
    - Target production = 2000 tons
    - Required raw material = 2500 tons
    """)
    
    prediction_tab1, prediction_tab2 = st.tabs(["Create Prediction", "Historical Data"])
    
    with prediction_tab1:
        with st.form("prediction_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                product_name = st.selectbox("Product Name", [
                    "Railway Rails", "Steel Plates", "Structural Steel", 
                    "Steel Sheets", "Wire Rods", "Billets"
                ])
                
                historical_production = st.number_input(
                    "Historical Production (tons)", 
                    min_value=0.0, 
                    step=10.0,
                    help="Enter past production quantity"
                )
                
                raw_material_used = st.number_input(
                    "Raw Material Used (tons)", 
                    min_value=0.0, 
                    step=10.0,
                    help="Enter raw material quantity used for above production"
                )
            
            with col2:
                target_production = st.number_input(
                    "Target Production (tons)", 
                    min_value=0.0, 
                    step=10.0,
                    help="Enter desired production target"
                )
                
                prediction_date = st.date_input("Prediction For Date")
                
                notes = st.text_area("Notes", placeholder="Additional considerations...")
            
            submitted = st.form_submit_button("Generate Prediction")
            
            if submitted and all([historical_production, raw_material_used, target_production]):
                # Calculate conversion ratio and prediction
                conversion_ratio = historical_production / raw_material_used if raw_material_used > 0 else 0
                predicted_raw_material = target_production / conversion_ratio if conversion_ratio > 0 else 0
                
                # Display results
                st.markdown("### 📊 Prediction Results")
                
                result_col1, result_col2, result_col3 = st.columns(3)
                
                with result_col1:
                    st.metric("Conversion Ratio", f"{conversion_ratio:.3f}")
                
                with result_col2:
                    st.metric("Predicted Raw Material", f"{predicted_raw_material:.0f} tons")
                
                with result_col3:
                    efficiency = (conversion_ratio * 100) if conversion_ratio <= 1 else 100
                    st.metric("Process Efficiency", f"{efficiency:.1f}%")
                
                # Save prediction
                db = SessionLocal()
                try:
                    prediction = ProductionPrediction(
                        product_name=product_name,
                        historical_production=historical_production,
                        raw_material_used=raw_material_used,
                        conversion_ratio=conversion_ratio,
                        target_production=target_production,
                        predicted_raw_material=predicted_raw_material,
                        prediction_for_date=prediction_date,
                        created_by=1,
                        notes=notes
                    )
                    
                    db.add(prediction)
                    db.commit()
                    display_success_message("Prediction saved successfully!")
                    
                except Exception as e:
                    display_error_message(f"Error saving prediction: {e}")
                finally:
                    db.close()
    
    with prediction_tab2:
        st.markdown("#### 📊 Historical Predictions")
        
        db = SessionLocal()
        try:
            predictions = db.query(ProductionPrediction).order_by(ProductionPrediction.prediction_date.desc()).limit(10).all()
            
            if not predictions:
                st.info("No historical predictions found. Create predictions to see historical data.")
                return
            
            prediction_data = []
            for p in predictions:
                prediction_data.append({
                    "Date": format_date(p.prediction_date),
                    "Product": p.product_name,
                    "Target Production": f"{p.target_production:.0f} tons",
                    "Predicted Material": f"{p.predicted_raw_material:.0f} tons",
                    "Conversion Ratio": f"{p.conversion_ratio:.3f}",
                    "Notes": p.notes or "N/A"
                })
            
            df = pd.DataFrame(prediction_data)
            st.dataframe(df, use_container_width=True)
            
        except Exception as e:
            display_error_message(f"Error loading predictions: {e}")
        finally:
            db.close()

def show_raw_materials_summary():
    """Raw materials summary from the existing raw materials module"""
    st.markdown("#### 🏗️ Raw Materials Summary")
    st.info("This shows a summary view. Full raw materials management is available in the Raw Materials module.")
    
    db = SessionLocal()
    try:
        materials = db.query(RawMaterial).all()
        
        if materials:
            # Quick summary metrics
            col1, col2, col3, col4 = st.columns(4)
            
            total_materials = len(materials)
            total_quantity = sum(m.quantity_available for m in materials)
            total_value = sum(m.quantity_available * m.cost_per_unit for m in materials)
            critical_stock = len([m for m in materials if m.quantity_available < 100])
            
            with col1:
                st.metric("Total Materials", total_materials)
            with col2:
                st.metric("Total Quantity", f"{total_quantity:.0f} tons")
            with col3:
                st.metric("Total Value", f"₹{total_value:,.0f}")
            with col4:
                st.metric("Critical Stock Items", critical_stock)

            st.markdown("### 📄 Inventory Report (Expiry + Criticality)")

            today = datetime.now().date()
            report_rows = []
            for material in materials:
                expiry_value = material.expiry_date.date() if material.expiry_date else None
                days_to_expiry = (expiry_value - today).days if expiry_value else None

                if days_to_expiry is None:
                    expiry_status = "No Expiry"
                elif days_to_expiry < 0:
                    expiry_status = "Expired"
                elif days_to_expiry <= 7:
                    expiry_status = "Expiring <= 7 days"
                elif days_to_expiry <= 30:
                    expiry_status = "Expiring <= 30 days"
                else:
                    expiry_status = "Valid"

                if material.quantity_available < 50 or expiry_status in ["Expired", "Expiring <= 7 days"]:
                    criticality = "CRITICAL"
                elif material.quantity_available < 100 or expiry_status == "Expiring <= 30 days":
                    criticality = "HIGH"
                else:
                    criticality = "NORMAL"

                report_rows.append({
                    "Material": material.material_name,
                    "Batch": material.batch_number,
                    "Supplier": material.supplier,
                    "Available Qty": f"{material.quantity_available:.2f} {material.unit}",
                    "Expiry Date": expiry_value.strftime("%Y-%m-%d") if expiry_value else "N/A",
                    "Days to Expiry": days_to_expiry if days_to_expiry is not None else "N/A",
                    "Expiry Status": expiry_status,
                    "Criticality": criticality,
                    "Total Value": f"₹{(material.quantity_available * material.cost_per_unit):,.0f}"
                })

            report_df = pd.DataFrame(report_rows)
            st.dataframe(report_df, use_container_width=True, hide_index=True)

            # Critical section for actionable exceptions
            critical_df = report_df[report_df["Criticality"].isin(["CRITICAL", "HIGH"])]
            st.markdown("### 🚨 Critical Section")
            if critical_df.empty:
                st.success("No critical or high-risk items found in the current inventory report.")
            else:
                st.error(
                    f"{len(critical_df)} item(s) require attention due to low stock or near/expired material."
                )
                st.dataframe(critical_df, use_container_width=True, hide_index=True)

            with st.expander("View example report format"):
                example_rows = [
                    {
                        "Material": "Limestone Flux",
                        "Batch": "RM-EX-101",
                        "Supplier": "BSP Mines",
                        "Available Qty": "42.00 tons",
                        "Expiry Date": "2026-03-15",
                        "Days to Expiry": 2,
                        "Expiry Status": "Expiring <= 7 days",
                        "Criticality": "CRITICAL",
                        "Total Value": "₹315,000"
                    },
                    {
                        "Material": "Coking Coal",
                        "Batch": "RM-EX-102",
                        "Supplier": "Eastern Minerals",
                        "Available Qty": "76.00 tons",
                        "Expiry Date": "2026-03-28",
                        "Days to Expiry": 15,
                        "Expiry Status": "Expiring <= 30 days",
                        "Criticality": "HIGH",
                        "Total Value": "₹684,000"
                    },
                    {
                        "Material": "Iron Ore Pellets",
                        "Batch": "RM-EX-103",
                        "Supplier": "NMDC",
                        "Available Qty": "215.00 tons",
                        "Expiry Date": "2026-06-10",
                        "Days to Expiry": 89,
                        "Expiry Status": "Valid",
                        "Criticality": "NORMAL",
                        "Total Value": "₹2,150,000"
                    }
                ]
                st.dataframe(pd.DataFrame(example_rows), use_container_width=True, hide_index=True)
                st.caption("Use this format for daily inventory review with expiry and critical action prioritization.")
            
            st.info("💡 Visit the 'Raw Materials' module for complete material management features.")
        else:
            st.info("No raw materials found. Add materials in the Raw Materials module.")
            
    except Exception as e:
        display_error_message(f"Error loading raw materials summary: {e}")
    finally:
        db.close()
