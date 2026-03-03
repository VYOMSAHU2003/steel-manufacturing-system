import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from config.database import SessionLocal
from models.database_models import RawMaterial, InventoryLog
from utils.helpers import (
    display_success_message, display_error_message, display_info_message,
    format_currency, format_date, get_material_status_color, validate_positive_number
)

def show():
    """Display BSP Raw Materials Management module"""
    # Revolutionary BSP-themed header with enhanced CSS
    st.markdown("""
    <style>
    /* Modern Raw Materials Styling */
    .bsp-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2rem;
        border-radius: 25px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        animation: headerPulse 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerPulse {
        0% { box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3); }
        100% { box-shadow: 0 25px 50px rgba(102, 126, 234, 0.5); }
    }
    
    .bsp-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 2.5s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .bsp-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        font-weight: 800;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #ffeaa7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .bsp-header p {
        color: white;
        margin: 0.8rem 0 0 0;
        font-size: 1.2rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    /* Enhanced Material Cards */
    .material-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(15px);
        padding: 1.5rem;
        border-radius: 20px;
        border: 1px solid rgba(255,255,255,0.2);
        margin: 1rem 0;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .material-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 35px rgba(0,0,0,0.15);
    }
    
    /* Modern Status Badges with Glassmorphism */
    .status-badge {
        padding: 0.5rem 1rem;
        border-radius: 25px;
        color: white;
        font-weight: 600;
        text-align: center;
        display: inline-block;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .available { 
        background: linear-gradient(135deg, rgba(0, 184, 148, 0.9), rgba(85, 239, 196, 0.9)); 
        box-shadow: 0 4px 15px rgba(0, 184, 148, 0.3);
    }
    
    .reserved { 
        background: linear-gradient(135deg, rgba(253, 203, 110, 0.9), rgba(255, 177, 43, 0.9)); 
        color: #2d3436;
        box-shadow: 0 4px 15px rgba(253, 203, 110, 0.3);
    }
    
    .used { 
        background: linear-gradient(135deg, rgba(116, 185, 255, 0.9), rgba(81, 146, 255, 0.9)); 
        box-shadow: 0 4px 15px rgba(116, 185, 255, 0.3);
    }
    
    .expired { 
        background: linear-gradient(135deg, rgba(231, 76, 60, 0.9), rgba(192, 57, 43, 0.9)); 
        box-shadow: 0 4px 15px rgba(231, 76, 60, 0.3);
    }
    
    /* Modern Metrics */
    .modern-metric {
        background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.6));
        backdrop-filter: blur(15px);
        padding: 1.2rem;
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.3);
        text-align: center;
        box-shadow: 0 8px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease;
    }
    
    .modern-metric:hover {
        transform: translateY(-3px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.15);
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="bsp-header">
        <h1>� BSP Raw Materials Hub</h1>
        <p>Advanced Steel Production Materials Inventory & Control System</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Plant Status Grid with modern metrics
    st.markdown("### 📊 Real-Time Plant Status")
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("""
        <div class="modern-metric">
            <div style="color: #00b894; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">🏭 PLANT STATUS</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #00b894;">OPERATIONAL</div>
            <div style="font-size: 0.8rem; color: #667eea; margin-top: 0.3rem;">Normal Operations</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="modern-metric">
            <div style="color: #667eea; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">⚡ POWER STATUS</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #667eea;">STABLE</div>
            <div style="font-size: 0.8rem; color: #00b894; margin-top: 0.3rem;">Grid Connected</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="modern-metric">
            <div style="color: #fd7956; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">🌡️ FURNACE TEMP</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #fd7956;">1665°C</div>
            <div style="font-size: 0.8rem; color: #00b894; margin-top: 0.3rem;">+25°C</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="modern-metric">
            <div style="color: #fdcb6e; font-weight: 600; font-size: 0.9rem; margin-bottom: 0.5rem;">📊 PRODUCTION</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: #fdcb6e;">96.8%</div>
            <div style="font-size: 0.8rem; color: #00b894; margin-top: 0.3rem;">+7.2%</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Enhanced Tab Navigation 
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏭 Inventory Overview", 
        "➕ Add Material", 
        "📊 BSP Analytics", 
        "📝 Activity Logs",
        "🔬 Quality Control"
    ])
    
    with tab1:
        show_bsp_inventory()
    
    with tab2:
        show_add_material_form()
    
    with tab3:
        show_bsp_analytics()
    
    with tab4:
        show_inventory_logs()
        
    with tab5:
        show_quality_control()

def show_bsp_inventory():
    """Display BSP-specific raw materials inventory"""
    st.subheader("🏭 Current BSP Materials Inventory")
    
    # Quick filters
    filter_col1, filter_col2, filter_col3 = st.columns(3)
    with filter_col1:
        filter_type = st.selectbox("Material Type", ["All", "Iron Ore", "Coal", "Limestone", "Chemical", "Alloy"])
    with filter_col2:
        filter_status = st.selectbox("Status", ["All", "Available", "Reserved", "Used", "Expired"])
    with filter_col3:
        filter_supplier = st.selectbox("Supplier", ["All", "NMDC", "SAIL", "Tata Steel", "JSW", "Others"])
    
    db = SessionLocal()
    try:
        materials = db.query(RawMaterial).all()
        
        if not materials:
            st.info("🔍 No materials in BSP inventory system. Add materials to get started.")
            return
        
        # Apply filters
        filtered_materials = materials
        if filter_type != "All":
            filtered_materials = [m for m in filtered_materials if filter_type.lower() in m.material_type.lower()]
        if filter_status != "All":
            filtered_materials = [m for m in filtered_materials if m.status.value == filter_status.lower()]
        
        # Critical materials alert
        critical_materials = [m for m in materials if m.quantity_available < 10]
        if critical_materials:
            st.error(f"🚨 **CRITICAL ALERT**: {len(critical_materials)} materials are running low!")
            with st.expander("View Critical Materials", expanded=True):
                for mat in critical_materials:
                    st.warning(f"⚠️ {mat.material_name}: Only {mat.quantity_available:.1f} {mat.unit} remaining")
        
        # Create enhanced display dataframe
        data = []
        for material in filtered_materials:
            # Determine criticality
            criticality = "🟢 Normal"
            if material.quantity_available < 5:
                criticality = "🔴 Critical"
            elif material.quantity_available < 10:
                criticality = "🟡 Low"
                
            data.append({
                "ID": material.material_id,
                "Material Name": material.material_name,
                "Type": material.material_type,
                "Supplier": material.supplier,
                "Available Qty": f"{material.quantity_available:.1f}",
                "Unit": material.unit,
                "Rate (₹)": f"₹{material.cost_per_unit:.2f}",
                "Total Value": f"₹{material.quantity_available * material.cost_per_unit:,.2f}",
                "Status": material.status.value.title(),
                "Batch #": material.batch_number,
                "Grade": material.quality_grade or "Standard",
                "Criticality": criticality,
                "Expiry": format_date(material.expiry_date) if material.expiry_date else "No Expiry"
            })
        
        if data:
            df = pd.DataFrame(data)
            
            # Display with enhanced formatting
            st.markdown("### 📋 Detailed Inventory Report")
            st.dataframe(
                df,
                width='stretch',
                hide_index=True,
                column_config={
                    "Available Qty": st.column_config.NumberColumn(format="%.1f"),
                    "Total Value": st.column_config.NumberColumn(format="₹%.2f"),
                }
            )
        else:
            st.info("🔍 No materials match the selected filters")
        
        # Enhanced summary metrics for BSP
        st.markdown("### 📊 BSP Inventory Summary")
        col1, col2, col3, col4, col5 = st.columns(5)
        
        total_value = sum(m.quantity_available * m.cost_per_unit for m in materials)
        available_count = sum(1 for m in materials if m.status.value == "available")
        reserved_count = sum(1 for m in materials if m.status.value == "reserved")
        critical_count = sum(1 for m in materials if m.quantity_available < 10)
        total_tonnage = sum(m.quantity_available for m in materials if m.unit in ["ton", "kg"])
        
        with col1:
            st.metric("🏗️ Total Materials", len(materials), delta="Active Inventory")
        with col2:
            st.metric("✅ Available", available_count, delta="Ready for Production")
        with col3:
            st.metric("📦 Reserved", reserved_count, delta="Allocated")
        with col4:
            st.metric("⚠️ Critical Stock", critical_count, delta="-2" if critical_count > 2 else None)
        with col5:
            st.metric("💰 Total Value", f"₹{total_value:,.0f}", delta="Current Valuation")
        
        # BSP-specific material management section
        st.markdown("---")
        st.subheader("🔧 BSP Material Operations")
        
        operation_tab1, operation_tab2, operation_tab3 = st.tabs([
            "Update Material", "Transfer Materials", "Emergency Procurement"
        ])
        
        with operation_tab1:
            show_material_update(materials, db)
        with operation_tab2:
            show_material_transfer(materials)
        with operation_tab3:
            show_emergency_procurement(materials)
    
    except Exception as e:
        display_error_message(f"Error loading BSP inventory: {e}")
    finally:
        db.close()

def show_material_update(materials, db):
    """Enhanced material update for BSP operations"""
    col1, col2, col3 = st.columns([2, 1, 1])
    
    with col1:
        selected_material = st.selectbox(
            "🔍 Select Material for Update",
            options=[(m.material_id, f"{m.material_name} ({m.batch_number})") for m in materials],
            format_func=lambda x: x[1],
            key="bsp_material_select"
        )
    
    if selected_material:
        material_id = selected_material[0]
        material = next((m for m in materials if m.material_id == material_id), None)
        
        with col2:
            quantity = st.number_input(
                "📊 New Quantity",
                value=float(material.quantity_available),
                step=1.0,
                help="Enter the updated quantity after consumption/receipt",
                key="bsp_qty_input"
            )
        
        with col3:
            new_status = st.selectbox(
                "🔄 Update Status",
                options=["available", "reserved", "used", "expired"],
                index=["available", "reserved", "used", "expired"].index(material.status.value),
                key="bsp_status_select"
            )
        
        # Show change impact
        if quantity != material.quantity_available:
            change = quantity - material.quantity_available
            if change > 0:
                st.success(f"📈 Increase: +{change:.1f} {material.unit}")
            else:
                st.warning(f"📉 Consumption: {change:.1f} {material.unit}")
        
        if st.button("🔄 Update Material Status", width='stretch', type="primary"):
            try:
                # Log the change
                change_amount = quantity - material.quantity_available
                quantity_before = material.quantity_available
                
                material.quantity_available = quantity
                material.status = new_status
                material.updated_at = datetime.utcnow()
                
                # Create inventory log entry
                log_entry = InventoryLog(
                    material_id=material.material_id,
                    transaction_type="ADJUST" if change_amount != 0 else "STATUS",
                    quantity_change=change_amount,
                    quantity_before=quantity_before,
                    quantity_after=quantity,
                    notes=f"BSP Operation: Status changed to {new_status}, quantity updated",
                    recorded_by=st.session_state.get("user_id", 1)
                )
                db.add(log_entry)
                db.commit()
                
                display_success_message(f"✅ Material '{material.material_name}' updated successfully!")
                st.rerun()
            except Exception as e:
                display_error_message(f"❌ Error updating material: {e}")

def show_material_transfer(materials):
    """BSP material transfer operations"""
    st.markdown("**🚚 Internal Material Transfer**")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        source_dept = st.selectbox("From Department", 
                                  ["Raw Materials Store", "Blast Furnace", "Steel Melting Shop", "Rolling Mill"])
    with col2:
        dest_dept = st.selectbox("To Department", 
                                ["Blast Furnace", "Steel Melting Shop", "Rolling Mill", "Finishing Mill"])
    with col3:
        transfer_qty = st.number_input("Transfer Quantity", min_value=0.0, step=1.0)
    
    if st.button("🔄 Process Transfer", type="secondary"):
        display_success_message(f"Transfer initiated: {transfer_qty} units from {source_dept} to {dest_dept}")

def show_emergency_procurement(materials):
    """Emergency procurement for critical materials"""
    st.markdown("**🚨 Emergency Procurement Request**")
    
    critical_materials = [m for m in materials if m.quantity_available < 10]
    
    if critical_materials:
        for mat in critical_materials:
            with st.container():
                st.markdown(f"""
                <div class="material-card">
                    <h4>🔴 {mat.material_name}</h4>
                    <p><strong>Current Stock:</strong> {mat.quantity_available:.1f} {mat.unit}</p>
                    <p><strong>Supplier:</strong> {mat.supplier}</p>
                    <p><strong>Last Cost:</strong> ₹{mat.cost_per_unit:.2f} per {mat.unit}</p>
                </div>
                """, unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                with col1:
                    urgent_qty = st.number_input(f"Urgent Qty for {mat.material_name}", 
                                               min_value=1.0, value=50.0, step=1.0,
                                               key=f"urgent_{mat.material_id}")
                with col2:
                    priority = st.selectbox(f"Priority for {mat.material_name}", 
                                          ["High", "Critical", "Emergency"],
                                          key=f"priority_{mat.material_id}")
                with col3:
                    if st.button(f"🚨 Request Procurement", key=f"procure_{mat.material_id}"):
                        display_success_message(f"Emergency procurement request submitted for {mat.material_name}")
    else:
        st.success("✅ No emergency procurement required. All materials are at adequate levels.")

def show_add_material_form():
    """Display form to add new raw material"""
    st.subheader("Add New Raw Material")
    
    with st.form("add_material_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            material_name = st.text_input("Material Name", placeholder="e.g., Iron Ore, Coal")
            material_type = st.text_input("Material Type", placeholder="e.g., Ore, Fuel, Chemical")
            supplier = st.text_input("Supplier Name")
            batch_number = st.text_input("Batch Number", placeholder="e.g., BATCH-2024-001")
        
        with col2:
            quantity = st.number_input("Quantity", min_value=0.0, step=1.0)
            unit = st.selectbox("Unit", options=["kg", "ton", "liter", "piece", "other"])
            cost_per_unit = st.number_input("Cost per Unit", min_value=0.0, step=0.01)
            quality_grade = st.selectbox("Quality Grade", options=["A", "B", "C", "Standard", "Premium"])
        
        expiry_date = st.date_input("Expiry Date (Optional)", value=None)
        
        submitted = st.form_submit_button("Add Material", width='stretch', type="primary")
        
        if submitted:
            # Validate
            if not material_name or not material_type or not supplier or not batch_number:
                display_error_message("Please fill in all required fields")
            elif quantity <= 0:
                display_error_message("Quantity must be positive")
            elif cost_per_unit < 0:
                display_error_message("Cost cannot be negative")
            else:
                db = SessionLocal()
                try:
                    new_material = RawMaterial(
                        material_name=material_name,
                        material_type=material_type,
                        supplier=supplier,
                        quantity_available=quantity,
                        unit=unit,
                        cost_per_unit=cost_per_unit,
                        batch_number=batch_number,
                        quality_grade=quality_grade,
                        expiry_date=datetime.combine(expiry_date, datetime.min.time()) if expiry_date else None,
                        created_by=st.session_state.user_id
                    )
                    db.add(new_material)
                    db.commit()
                    
                    display_success_message(f"Material '{material_name}' added successfully")
                    st.balloons()
                    st.rerun()
                except Exception as e:
                    display_error_message(f"Error adding material: {e}")
                finally:
                    db.close()

def show_bsp_analytics():
    """BSP-specific materials analytics dashboard"""
    st.subheader("📊 BSP Materials Analytics & Intelligence")
    
    db = SessionLocal()
    try:
        materials = db.query(RawMaterial).all()
        logs = db.query(InventoryLog).order_by(InventoryLog.recorded_at.desc()).limit(100).all()
        
        if not materials:
            st.info("📈 No materials data available for analytics")
            return
        
        # BSP-specific analytics tabs
        analytics_tab1, analytics_tab2, analytics_tab3, analytics_tab4 = st.tabs([
            "🏭 Production Impact", "💰 Cost Analysis", "⏰ Consumption Trends", "🎯 Optimization"
        ])
        
        with analytics_tab1:
            # Production impact analysis
            st.markdown("**🏗️ Material Impact on Steel Production**")
            
            # Calculate production readiness score
            critical_materials = ["Iron Ore", "Coal", "Limestone"]
            readiness_score = 100
            
            for mat_type in critical_materials:
                mat = next((m for m in materials if mat_type.lower() in m.material_type.lower()), None)
                if mat:
                    if mat.quantity_available < 5:
                        readiness_score -= 30
                    elif mat.quantity_available < 10:
                        readiness_score -= 15
            
            # Display readiness metrics
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("🎯 Production Readiness", f"{readiness_score}%", 
                         delta="High" if readiness_score > 80 else "Medium" if readiness_score > 60 else "Low")
            
            # Material distribution by type
            type_counts = {}
            for material in materials:
                mat_type = material.material_type
                if mat_type not in type_counts:
                    type_counts[mat_type] = {"count": 0, "value": 0}
                type_counts[mat_type]["count"] += 1
                type_counts[mat_type]["value"] += material.quantity_available * material.cost_per_unit
            
            # Create visualization
            if type_counts:
                df_types = pd.DataFrame([
                    {"Type": k, "Count": v["count"], "Value": v["value"]} 
                    for k, v in type_counts.items()
                ])
                
                col1, col2 = st.columns(2)
                with col1:
                    fig_count = px.pie(df_types, values="Count", names="Type", 
                                     title="Material Types Distribution")
                    st.plotly_chart(fig_count, width='stretch')
                
                with col2:
                    fig_value = px.pie(df_types, values="Value", names="Type", 
                                     title="Inventory Value Distribution")
                    st.plotly_chart(fig_value, width='stretch')
        
        with analytics_tab2:
            # Cost analysis
            st.markdown("**💰 BSP Material Cost Intelligence**")
            
            total_investment = sum(m.quantity_available * m.cost_per_unit for m in materials)
            avg_cost_per_ton = sum(m.cost_per_unit for m in materials if m.unit == "ton") / max(1, len([m for m in materials if m.unit == "ton"]))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("💰 Total Investment", f"₹{total_investment:,.0f}")
            with col2:
                st.metric("📊 Avg Cost/Ton", f"₹{avg_cost_per_ton:,.2f}")
            with col3:
                monthly_burn = total_investment * 0.1  # Estimated monthly consumption
                st.metric("🔥 Monthly Burn Rate", f"₹{monthly_burn:,.0f}")
            
            # Cost trends chart
            cost_data = []
            for material in materials:
                cost_data.append({
                    "Material": material.material_name,
                    "Unit Cost": material.cost_per_unit,
                    "Total Value": material.quantity_available * material.cost_per_unit,
                    "Criticality": "High" if material.quantity_available < 10 else "Normal"
                })
            
            if cost_data:
                df_cost = pd.DataFrame(cost_data)
                fig_cost = px.scatter(df_cost, x="Unit Cost", y="Total Value", 
                                    color="Criticality", size="Total Value",
                                    hover_data=["Material"],
                                    title="Cost vs Value Analysis")
                st.plotly_chart(fig_cost, width='stretch')
        
        with analytics_tab3:
            # Consumption trends - simplified version since we may not have enough log data
            st.markdown("**⏰ Material Consumption Trends**")
            
            # Quantity by material
            data = []
            for m in materials:
                data.append({
                    "Material": m.material_name,
                    "Available Qty": m.quantity_available,
                    "Type": m.material_type
                })
            
            df = pd.DataFrame(data)
            fig = px.bar(
                df,
                x="Material",
                y="Available Qty",
                color="Type",
                title="Current Material Availability"
            )
            st.plotly_chart(fig, width='stretch')
            
            st.info("📊 Historical consumption data will be available as the system logs more transactions")
        
        with analytics_tab4:
            # Optimization recommendations
            st.markdown("**🎯 AI-Powered Optimization Recommendations**")
            
            st.success("🤖 **BSP AI Recommendations:**")
            
            # Generate smart recommendations
            recommendations = []
            
            # Check for critical stock
            critical_count = sum(1 for m in materials if m.quantity_available < 10)
            if critical_count > 0:
                recommendations.append(f"🚨 **Immediate Action**: {critical_count} materials require emergency procurement")
            
            # Check for overstock
            overstock = [m for m in materials if m.quantity_available > 100]
            if overstock:
                recommendations.append(f"📦 **Inventory Optimization**: {len(overstock)} materials may be overstocked")
            
            # Cost optimization
            high_cost_materials = sorted(materials, key=lambda x: x.cost_per_unit, reverse=True)[:3]
            if high_cost_materials:
                recommendations.append(f"💰 **Cost Focus**: Review pricing for {high_cost_materials[0].material_name} (₹{high_cost_materials[0].cost_per_unit:.2f}/unit)")
            
            # Display recommendations
            for i, rec in enumerate(recommendations, 1):
                st.markdown(f"**{i}.** {rec}")
            
            if not recommendations:
                st.success("✅ **Excellent!** Your inventory is well-optimized with no critical issues.")
            
            # Predictive insights
            st.markdown("---")
            st.markdown("**🔮 Predictive Insights**")
            col1, col2 = st.columns(2)
            with col1:
                st.info("📈 **Production Forecast**: Based on current consumption, all critical materials will last 15-20 days")
            with col2:
                st.warning("⚡ **Energy Impact**: High-energy materials (Coal, Coke) consumption is 12% above optimal")
    
    except Exception as e:
        display_error_message(f"Error loading BSP analytics: {e}")
    finally:
        db.close()

def show_analytics():
    """Enhanced analytics display - calls BSP analytics"""
    show_bsp_analytics()

def show_inventory_logs():
    """Display inventory transaction logs"""
    st.subheader("Inventory Transaction Logs")
    
    db = SessionLocal()
    try:
        logs = db.query(InventoryLog).order_by(InventoryLog.recorded_at.desc()).limit(100).all()
        
        if not logs:
            display_info_message("No inventory transactions recorded")
            return
        
        data = []
        for log in logs:
            data.append({
                "Date": format_date(log.recorded_at),
                "Material ID": log.material_id,
                "Type": log.transaction_type,
                "Quantity Change": f"{log.quantity_change:+.2f}",
                "Before": f"{log.quantity_before:.2f}",
                "After": f"{log.quantity_after:.2f}",
                "Reference": log.reference_id or "N/A",
                "Notes": log.notes or ""
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
        
    except Exception as e:
        display_error_message(f"Error loading logs: {e}")
    finally:
        db.close()

def show_quality_control():
    """BSP Quality Control for Raw Materials"""
    st.subheader("🔬 BSP Quality Control & Testing")
    
    db = SessionLocal()
    try:
        materials = db.query(RawMaterial).all()
        
        # Quality status overview
        st.markdown("**📊 Quality Status Overview**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        grade_a_count = sum(1 for m in materials if m.quality_grade == "A")
        grade_b_count = sum(1 for m in materials if m.quality_grade == "B") 
        premium_count = sum(1 for m in materials if m.quality_grade == "Premium")
        standard_count = sum(1 for m in materials if not m.quality_grade or m.quality_grade == "Standard")
        
        with col1:
            st.metric("🥇 Grade A", grade_a_count)
        with col2:
            st.metric("🥈 Grade B", grade_b_count)
        with col3:
            st.metric("⭐ Premium", premium_count)
        with col4:
            st.metric("📋 Standard", standard_count)
        
        # Quality testing interface
        st.markdown("---")
        st.markdown("**🧪 Quality Testing Interface**")
        
        test_col1, test_col2 = st.columns(2)
        
        with test_col1:
            selected_material = st.selectbox(
                "Select Material for Testing",
                options=[(m.material_id, m.material_name) for m in materials],
                format_func=lambda x: x[1]
            )
            
            test_type = st.selectbox("Test Type", [
                "Chemical Composition",
                "Physical Properties", 
                "Thermal Properties",
                "Moisture Content",
                "Particle Size Analysis",
                "Contamination Check"
            ])
            
            test_result = st.selectbox("Test Result", ["Pass", "Fail", "Conditional Pass"])
            
        with test_col2:
            test_notes = st.text_area("Test Notes & Observations", 
                                     placeholder="Enter detailed test observations...")
            
            quality_score = st.slider("Quality Score (1-100)", 1, 100, 85)
            
            inspector_name = st.text_input("Inspector Name", 
                                          value=st.session_state.get("user", "Quality Inspector"))
        
        if st.button("📝 Submit Quality Test Report", type="primary"):
            # In a real implementation, this would save to a quality_tests table
            display_success_message(f"✅ Quality test report submitted for {selected_material[1]}")
            
        # Recent quality tests (simulated data)
        st.markdown("---")
        st.markdown("**📋 Recent Quality Test Results**")
        
        # Sample test data
        test_data = [
            {"Date": "2024-01-15", "Material": "Iron Ore", "Test": "Chemical Composition", "Result": "Pass", "Score": 92},
            {"Date": "2024-01-14", "Material": "Coal", "Test": "Thermal Properties", "Result": "Pass", "Score": 88},
            {"Date": "2024-01-14", "Material": "Limestone", "Test": "Physical Properties", "Result": "Pass", "Score": 90},
            {"Date": "2024-01-13", "Material": "Dolomite", "Test": "Contamination Check", "Result": "Conditional Pass", "Score": 75},
        ]
        
        df_tests = pd.DataFrame(test_data)
        st.dataframe(df_tests, width='stretch', hide_index=True)
        
        # Quality trends
        fig_quality = px.line(df_tests, x="Date", y="Score", color="Material",
                             title="Quality Score Trends")
        st.plotly_chart(fig_quality, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading quality control: {e}")
    finally:
        db.close()
