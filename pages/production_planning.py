import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from config.database import SessionLocal
from models.database_models import ProductionOrder, User
from utils.helpers import (
    display_success_message, display_error_message, display_info_message,
    format_date, get_order_status_color
)

def show():
    """Display BSP Production Planning module"""
    # BSP-themed header with custom CSS
    st.markdown("""
    <style>
    .bsp-production-header {
        background: linear-gradient(135deg, #2E4A62 0%, #4A6741 100%);
        padding: 25px;
        border-radius: 15px;
        margin-bottom: 30px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(46, 74, 98, 0.2);
    }
    .bsp-production-header h1 {
        color: white;
        font-size: 2.5rem;
        margin: 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .bsp-production-header p {
        color: #E8F4F8;
        margin: 15px 0 0 0;
        font-size: 1.2rem;
    }
    .production-metric-card {
        background: #f8f9fa;
        padding: 15px;
        border-radius: 10px;
        border-left: 4px solid #2E4A62;
        margin: 10px 0;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    .furnace-status {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        padding: 10px;
        border-radius: 8px;
        text-align: center;
        margin: 5px 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="bsp-production-header">
        <h1>🔥 BSP Production Planning & Control</h1>
        <p>Integrated Steel Manufacturing Operations Management</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Real-time plant status dashboard
    st.markdown("### 🏭 Live Production Status")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.metric("🔥 Blast Furnace #1", "1680°C", delta="Normal")
    with col2:
        st.metric("🔥 Blast Furnace #2", "1625°C", delta="-55°C")
    with col3:
        st.metric("⚡ Steel Production", "2,450 tons", delta="12 tons/hr")
    with col4:
        st.metric("📊 Efficiency", "94.2%", delta="2.3%")
    with col5:
        st.metric("🎯 Target Achievement", "98.1%", delta="1.2%")
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "🏗️ Production Orders", 
        "➕ Create Order", 
        "📅 Production Timeline", 
        "📊 Plant Status",
        "🔧 Equipment Control"
    ])
    
    with tab1:
        show_bsp_orders()
    
    with tab2:
        show_create_order()
    
    with tab3:
        show_timeline()
    
    with tab4:
        show_bsp_status_overview()
        
    with tab5:
        show_equipment_control()

def show_bsp_orders():
    """Display BSP-enhanced production orders"""
    st.subheader("🏗️ BSP Production Orders Management")
    
    # Quick action buttons
    action_col1, action_col2, action_col3 = st.columns(3)
    with action_col1:
        if st.button("🚨 Emergency Production", type="secondary"):
            st.info("Emergency production protocol initiated")
    with action_col2:
        if st.button("⏸️ Pause All Orders", type="secondary"):
            st.warning("Production pause requested")  
    with action_col3:
        if st.button("🔄 Refresh Status", type="primary"):
            st.success("Production data refreshed")
    
    st.markdown("---")
    
    db = SessionLocal()
    try:
        orders = db.query(ProductionOrder).all()
        
        if not orders:
            display_info_message("No production orders")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=["pending", "in_progress", "completed", "cancelled"],
                default=["pending", "in_progress"]
            )
        
        with col2:
            sort_by = st.selectbox("Sort by", options=["Order Number", "Expected Completion", "Status"])
        
        with col3:
            search_term = st.text_input("Search Order Number")
        
        # Filter orders
        filtered_orders = [o for o in orders if o.status.value in status_filter]
        
        if search_term:
            filtered_orders = [o for o in filtered_orders if search_term.lower() in o.order_number.lower()]
        
        if not filtered_orders:
            display_info_message("No orders match filters")
            return
        
        # Create display dataframe
        data = []
        for order in filtered_orders:
            assigned_user = db.query(User).filter(User.user_id == order.assigned_to).first() if order.assigned_to else None
            data.append({
                "Order ID": order.order_id,
                "Order Number": order.order_number,
                "Product": order.product_name,
                "Qty Ordered": f"{order.quantity_ordered:.2f}",
                "Qty Produced": f"{order.quantity_produced:.2f}",
                "Progress": f"{(order.quantity_produced/order.quantity_ordered*100):.1f}%" if order.quantity_ordered > 0 else "0%",
                "Status": f"{get_order_status_color(order.status.value)} {order.status.value.upper()}",
                "Expected": format_date(order.expected_completion),
                "Assigned To": assigned_user.full_name if assigned_user else "Unassigned"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
        
        # Update order
        st.subheader("Update Order")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            selected_order = st.selectbox(
                "Select Order",
                options=[(o.order_id, o.order_number) for o in filtered_orders],
                format_func=lambda x: x[1],
                key="order_select"
            )
        
        if selected_order:
            order_id = selected_order[0]
            order = next((o for o in filtered_orders if o.order_id == order_id), None)
            
            with col2:
                quantity_produced = st.number_input(
                    "Quantity Produced",
                    value=float(order.quantity_produced),
                    step=1.0,
                    min_value=0.0,
                    max_value=float(order.quantity_ordered)
                )
            
            with col3:
                new_status = st.selectbox(
                    "Status",
                    options=["pending", "in_progress", "completed", "cancelled"],
                    index=["pending", "in_progress", "completed", "cancelled"].index(order.status.value)
                )
            
            if st.button("Update Order", width='stretch'):
                try:
                    order.quantity_produced = quantity_produced
                    order.status = new_status
                    if new_status == "in_progress" and not order.start_date:
                        order.start_date = datetime.utcnow()
                    if new_status == "completed":
                        order.actual_completion = datetime.utcnow()
                    order.updated_at = datetime.utcnow()
                    db.commit()
                    display_success_message(f"Order '{order.order_number}' updated")
                    st.rerun()
                except Exception as e:
                    display_error_message(f"Error updating order: {e}")
    
    except Exception as e:
        display_error_message(f"Error loading orders: {e}")
    finally:
        db.close()

def show_create_order():
    """Display form to create new production order"""
    st.subheader("Create New Production Order")
    
    db = SessionLocal()
    try:
        operators = db.query(User).filter(User.role == "operator").all()
        
        with st.form("create_order_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                order_number = st.text_input("Order Number", placeholder="ORD-2024-001")
                product_name = st.text_input("Product Name", placeholder="Steel Coil")
                quantity_ordered = st.number_input("Quantity", min_value=0.0, step=1.0)
            
            with col2:
                unit = st.selectbox("Unit", options=["kg", "ton", "meter", "piece", "other"])
                expected_completion = st.date_input("Expected Completion Date")
                assigned_to = st.selectbox(
                    "Assign To Operator",
                    options=[(u.user_id, u.full_name) for u in operators] if operators else [],
                    format_func=lambda x: x[1] if x else "No operators available"
                ) if operators else None
            
            notes = st.text_area("Notes", placeholder="Additional order details...")
            
            submitted = st.form_submit_button("Create Order", width='stretch', type="primary")
            
            if submitted:
                if not order_number or not product_name or quantity_ordered <= 0 or not expected_completion:
                    display_error_message("Please fill in all required fields")
                else:
                    try:
                        new_order = ProductionOrder(
                            order_number=order_number,
                            product_name=product_name,
                            quantity_ordered=quantity_ordered,
                            unit=unit,
                            expected_completion=datetime.combine(expected_completion, datetime.min.time()),
                            assigned_to=assigned_to[0] if assigned_to else None,
                            notes=notes
                        )
                        db.add(new_order)
                        db.commit()
                        display_success_message(f"Order '{order_number}' created")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        display_error_message(f"Error creating order: {e}")
    
    finally:
        db.close()

def show_timeline():
    """Display production timeline"""
    st.subheader("Production Timeline")
    
    db = SessionLocal()
    try:
        orders = db.query(ProductionOrder).filter(ProductionOrder.status != "cancelled").all()
        
        if not orders:
            display_info_message("No active orders")
            return
        
        # Create timeline chart
        data = []
        for order in orders:
            start = order.start_date or order.expected_completion - timedelta(days=7)
            end = order.actual_completion or order.expected_completion
            
            data.append({
                "Order": order.order_number,
                "Start": start,
                "End": end,
                "Status": order.status.value
            })
        
        df = pd.DataFrame(data)
        
        fig = px.timeline(
            df,
            x_start="Start",
            x_end="End",
            y="Order",
            color="Status",
            title="Production Timeline"
        )
        
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading timeline: {e}")
    finally:
        db.close()

def show_status_overview():
    """Display production status overview"""
    st.subheader("Production Status Overview")
    
    db = SessionLocal()
    try:
        orders = db.query(ProductionOrder).all()
        
        if not orders:
            display_info_message("No orders available")
            return
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        pending = sum(1 for o in orders if o.status.value == "pending")
        in_progress = sum(1 for o in orders if o.status.value == "in_progress")
        completed = sum(1 for o in orders if o.status.value == "completed")
        cancelled = sum(1 for o in orders if o.status.value == "cancelled")
        
        with col1:
            st.metric("Total Orders", len(orders))
        with col2:
            st.metric("Pending", pending)
        with col3:
            st.metric("In Progress", in_progress)
        with col4:
            st.metric("Completed", completed)
        with col5:
            st.metric("Cancelled", cancelled)
        
        # Status distribution chart
        status_data = [
            {"Status": "Pending", "Count": pending},
            {"Status": "In Progress", "Count": in_progress},
            {"Status": "Completed", "Count": completed},
            {"Status": "Cancelled", "Count": cancelled}
        ]
        
        df = pd.DataFrame(status_data)
        fig = px.bar(df, x="Status", y="Count", title="Orders by Status", color="Status")
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading status: {e}")
    finally:
        db.close()

def show_bsp_status_overview():
    """BSP Plant Status Overview"""
    st.subheader("🏭 BSP Plant Production Status")
    
    # Real-time plant metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
        <div class="production-metric-card">
            <h4>🔥 Blast Furnaces</h4>
            <p><strong>BF-1:</strong> 1680°C - Operating</p>
            <p><strong>BF-2:</strong> 1625°C - Operating</p>
            <p><strong>BF-3:</strong> Maintenance</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="production-metric-card">
            <h4>🏗️ Steel Making Shop</h4>
            <p><strong>BOF-1:</strong> Active - 95 tons</p>
            <p><strong>BOF-2:</strong> Charging</p>
            <p><strong>EAF:</strong> Ready - Standby</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="production-metric-card">
            <h4>🎯 Rolling Mills</h4>
            <p><strong>Hot Strip:</strong> 87% capacity</p>
            <p><strong>Cold Rolling:</strong> 92% capacity</p>
            <p><strong>Bar Mill:</strong> 78% capacity</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Production flow visualization
    st.markdown("### 🔄 Production Flow Status")
    
    flow_data = {
        "Stage": ["Iron Making", "Steel Making", "Continuous Casting", "Hot Rolling", "Cold Rolling", "Finishing"],
        "Throughput (%)": [95, 88, 92, 87, 85, 90],
        "Status": ["Normal", "Normal", "Normal", "High Load", "Normal", "Normal"]
    }
    
    df_flow = pd.DataFrame(flow_data)
    fig_flow = px.bar(df_flow, x="Stage", y="Throughput (%)", color="Status",
                     title="Production Stage Throughput")
    st.plotly_chart(fig_flow, width='stretch')
    
    # Quality metrics
    st.markdown("### 📊 Quality & Performance Metrics")
    
    quality_col1, quality_col2, quality_col3, quality_col4 = st.columns(4)
    with quality_col1:
        st.metric("🎯 Quality Grade A", "94.2%", delta="2.1%")
    with quality_col2:
        st.metric("⚡ Energy Efficiency", "91.5%", delta="-0.8%")
    with quality_col3:
        st.metric("🔧 Equipment OEE", "87.3%", delta="1.5%")
    with quality_col4:
        st.metric("🌱 Environmental Score", "89.7%", delta="0.3%")

def show_equipment_control():
    """BSP Equipment Control Interface"""
    st.subheader("🔧 BSP Equipment Control Center")
    
    # Equipment status grid
    st.markdown("### 🏭 Major Equipment Status")
    
    equipment_col1, equipment_col2 = st.columns(2)
    
    with equipment_col1:
        st.markdown("**🔥 Blast Furnace Operations**")
        
        # BF controls
        bf_tabs = st.tabs(["BF-1", "BF-2", "BF-3"])
        
        with bf_tabs[0]:
            st.success("✅ BF-1: OPERATIONAL")
            st.metric("Temperature", "1680°C", delta="Normal")
            st.metric("Pressure", "2.1 atm", delta="Stable")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔧 Adjust Parameters", key="bf1_adjust"):
                    st.info("Parameter adjustment interface opened")
            with col2:
                if st.button("📊 View Trends", key="bf1_trends"):
                    st.info("Historical trends displayed")
        
        with bf_tabs[1]:
            st.success("✅ BF-2: OPERATIONAL")
            st.metric("Temperature", "1625°C", delta="-55°C")
            st.metric("Pressure", "2.0 atm", delta="Monitoring")
            if st.button("⚠️ Temperature Check Required", key="bf2_check"):
                st.warning("Temperature monitoring protocol initiated")
        
        with bf_tabs[2]:
            st.error("🔧 BF-3: MAINTENANCE MODE")
            st.info("Scheduled maintenance: Refractory lining replacement")
            st.progress(65, text="Maintenance Progress: 65%")
            if st.button("📅 View Maintenance Schedule", key="bf3_schedule"):
                st.info("Maintenance schedule: Complete by Jan 20, 2024")
    
    with equipment_col2:
        st.markdown("**⚙️ Steel Making Operations**")
        
        # BOF controls
        bof_tabs = st.tabs(["BOF-1", "BOF-2", "EAF"])
        
        with bof_tabs[0]:
            st.success("🔥 BOF-1: ACTIVE HEAT")
            st.metric("Current Heat", "95 tons", delta="Processing")
            st.metric("Oxygen Flow", "850 Nm³/min", delta="Optimal")
            if st.button("🎯 Lance Position Control", key="bof1_lance"):
                st.info("Lance position control panel activated")
        
        with bof_tabs[1]:
            st.warning("🔄 BOF-2: CHARGING")
            st.metric("Scrap Charged", "25 tons", delta="In progress")
            st.progress(40, text="Charging Progress: 40%")
        
        with bof_tabs[2]:
            st.info("⏱️ EAF: STANDBY")
            st.metric("Status", "Ready", delta="Available")
            if st.button("🚀 Start EAF Operation", key="eaf_start"):
                st.success("EAF startup sequence initiated")
    
    # Rolling mill controls
    st.markdown("---")
    st.markdown("### 🎯 Rolling Mill Operations")
    
    mill_col1, mill_col2, mill_col3 = st.columns(3)
    
    with mill_col1:
        st.markdown("**Hot Strip Mill**")
        st.metric("Capacity", "87%", delta="High Load")
        st.metric("Current Speed", "12 m/s", delta="Normal")
        if st.button("⚙️ Adjust Speed", key="hsm_speed"):
            st.info("Speed adjustment panel opened")
    
    with mill_col2:
        st.markdown("**Cold Rolling Mill**")
        st.metric("Capacity", "92%", delta="Normal")
        st.metric("Reduction Ratio", "65%", delta="Optimal")
        if st.button("🔧 Roll Change", key="crm_change"):
            st.info("Roll change procedure initiated")
    
    with mill_col3:
        st.markdown("**Bar Mill**")
        st.metric("Capacity", "78%", delta="Normal")
        st.metric("Product Grade", "Fe-500", delta="Standard")
        if st.button("📏 Set Dimensions", key="bar_dim"):
            st.info("Dimension setting interface activated")
    
    # Emergency controls
    st.markdown("---")
    st.markdown("### 🚨 Emergency Controls")
    
    emergency_col1, emergency_col2, emergency_col3 = st.columns(3)
    
    with emergency_col1:
        if st.button("🛑 EMERGENCY STOP ALL", type="secondary", key="emergency_stop"):
            st.error("⚠️ Emergency stop initiated - All operations halting")
    
    with emergency_col2:
        if st.button("🚨 Fire Suppression", type="secondary", key="fire_suppress"):
            st.warning("Fire suppression systems activated")
    
    with emergency_col3:
        if st.button("📞 Emergency Contact", type="secondary", key="emergency_contact"):
            st.info("Emergency response team contacted")

def show_orders():
    """Legacy function - redirects to BSP orders"""
    show_bsp_orders()
