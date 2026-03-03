import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
from config.database import SessionLocal
from models.database_models import Shipment, ProductionOrder, User
from utils.helpers import (
    display_success_message, display_error_message, display_info_message,
    format_date, get_shipment_status_color
)

def show():
    """Display Logistics & Shipment module"""
    st.title("🚚 Logistics & Shipment")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Shipments", "Create Shipment", "Tracking", "Analytics"])
    
    with tab1:
        show_shipments()
    
    with tab2:
        show_create_shipment()
    
    with tab3:
        show_tracking()
    
    with tab4:
        show_analytics()

def show_shipments():
    """Display all shipments"""
    st.subheader("Shipments")
    
    db = SessionLocal()
    try:
        shipments = db.query(Shipment).all()
        
        if not shipments:
            display_info_message("No shipments recorded")
            return
        
        # Filter options
        col1, col2, col3 = st.columns(3)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=["pending", "in_transit", "delivered", "cancelled"],
                default=["pending", "in_transit"]
            )
        
        with col2:
            sort_by = st.selectbox("Sort by", options=["Shipment Number", "Status", "Delivery Date"])
        
        with col3:
            search_term = st.text_input("Search Shipment Number")
        
        # Filter shipments
        filtered_shipments = [s for s in shipments if s.status.value in status_filter]
        
        if search_term:
            filtered_shipments = [s for s in filtered_shipments if search_term.lower() in s.shipment_number.lower()]
        
        if not filtered_shipments:
            display_info_message("No shipments match filters")
            return
        
        # Create display dataframe
        data = []
        for shipment in filtered_shipments:
            order = db.query(ProductionOrder).filter(ProductionOrder.order_id == shipment.order_id).first()
            handler = db.query(User).filter(User.user_id == shipment.logistics_handler).first() if shipment.logistics_handler else None
            
            data.append({
                "Shipment ID": shipment.shipment_id,
                "Shipment Number": shipment.shipment_number,
                "Order": order.order_number if order else "Unknown",
                "Destination": shipment.destination,
                "Quantity": f"{shipment.quantity_shipped:.2f}",
                "Unit": shipment.unit,
                "Status": f"{get_shipment_status_color(shipment.status.value)} {shipment.status.value.upper()}",
                "Expected Delivery": format_date(shipment.expected_delivery),
                "Carrier": shipment.carrier or "-",
                "Tracking": shipment.tracking_number or "-",
                "Handler": handler.full_name if handler else "Unassigned"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
        
        # Update shipment
        st.subheader("Update Shipment")
        
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            selected_shipment = st.selectbox(
                "Select Shipment",
                options=[(s.shipment_id, s.shipment_number) for s in filtered_shipments],
                format_func=lambda x: x[1],
                key="shipment_select"
            )
        
        if selected_shipment:
            shipment_id = selected_shipment[0]
            shipment = next((s for s in filtered_shipments if s.shipment_id == shipment_id), None)
            
            with col2:
                new_status = st.selectbox(
                    "Status",
                    options=["pending", "in_transit", "delivered", "cancelled"],
                    index=["pending", "in_transit", "delivered", "cancelled"].index(shipment.status.value)
                )
            
            with col3:
                tracking_number = st.text_input("Tracking Number", value=shipment.tracking_number or "")
            
            if st.button("Update Shipment", width='stretch'):
                try:
                    shipment.status = new_status
                    shipment.tracking_number = tracking_number
                    
                    if new_status == "in_transit" and not shipment.actual_ship_date:
                        shipment.actual_ship_date = datetime.utcnow()
                    if new_status == "delivered":
                        shipment.actual_delivery = datetime.utcnow()
                    
                    shipment.updated_at = datetime.utcnow()
                    db.commit()
                    display_success_message(f"Shipment '{shipment.shipment_number}' updated")
                    st.rerun()
                except Exception as e:
                    display_error_message(f"Error updating shipment: {e}")
    
    except Exception as e:
        display_error_message(f"Error loading shipments: {e}")
    finally:
        db.close()

def show_create_shipment():
    """Display form to create new shipment"""
    st.subheader("Create New Shipment")
    
    db = SessionLocal()
    try:
        # Get completed orders
        orders = db.query(ProductionOrder).filter(ProductionOrder.status == "completed").all()
        
        if not orders:
            display_info_message("No completed orders available for shipment")
            return
        
        handlers = db.query(User).filter(User.role == "logistics").all()
        
        with st.form("create_shipment_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                shipment_number = st.text_input("Shipment Number", placeholder="SHIP-2024-001")
                
                selected_order = st.selectbox(
                    "Select Completed Order",
                    options=[(o.order_id, o.order_number, o.quantity_ordered, o.unit) for o in orders],
                    format_func=lambda x: f"{x[1]} ({x[2]:.0f} {x[3]})"
                )
                
                quantity_shipped = st.number_input(
                    "Quantity to Ship",
                    min_value=0.0,
                    step=1.0
                )
            
            with col2:
                destination = st.text_input("Destination", placeholder="City, Country")
                
                carrier = st.selectbox(
                    "Carrier",
                    options=["DHL", "FedEx", "UPS", "Local Transport", "Custom"]
                )
                
                expected_delivery = st.date_input("Expected Delivery Date")
            
            handler = st.selectbox(
                "Logistics Handler",
                options=[(u.user_id, u.full_name) for u in handlers] if handlers else [],
                format_func=lambda x: x[1] if x else "No handlers available"
            ) if handlers else None
            
            notes = st.text_area("Notes", placeholder="Shipment details...")
            
            submitted = st.form_submit_button("Create Shipment", width='stretch', type="primary")
            
            if submitted:
                if not shipment_number or not selected_order or quantity_shipped <= 0 or not destination:
                    display_error_message("Please fill in all required fields")
                elif quantity_shipped > selected_order[2]:
                    display_error_message(f"Quantity cannot exceed order quantity ({selected_order[2]})")
                else:
                    try:
                        new_shipment = Shipment(
                            shipment_number=shipment_number,
                            order_id=selected_order[0],
                            destination=destination,
                            quantity_shipped=quantity_shipped,
                            unit=selected_order[3],
                            scheduled_date=datetime.utcnow(),
                            expected_delivery=datetime.combine(expected_delivery, datetime.min.time()),
                            carrier=carrier,
                            logistics_handler=handler[0] if handler else None,
                            notes=notes if notes else None
                        )
                        db.add(new_shipment)
                        db.commit()
                        display_success_message(f"Shipment '{shipment_number}' created")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        display_error_message(f"Error creating shipment: {e}")
    
    finally:
        db.close()

def show_tracking():
    """Display shipment tracking"""
    st.subheader("Shipment Tracking")
    
    db = SessionLocal()
    try:
        shipments = db.query(Shipment).all()
        
        if not shipments:
            display_info_message("No shipments for tracking")
            return
        
        # Search shipment
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_shipment = st.text_input("Search Shipment Number")
        
        # Find matching shipment
        matching_shipments = [s for s in shipments if search_shipment.lower() in s.shipment_number.lower()] if search_shipment else []
        
        if search_shipment and matching_shipments:
            selected = matching_shipments[0]
            
            # Display tracking details
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Shipment Details**")
                st.write(f"**Number:** {selected.shipment_number}")
                st.write(f"**Status:** {get_shipment_status_color(selected.status.value)} {selected.status.value.upper()}")
                st.write(f"**Destination:** {selected.destination}")
                st.write(f"**Quantity:** {selected.quantity_shipped:.2f} {selected.unit}")
            
            with col2:
                st.write("**Timing**")
                st.write(f"**Scheduled:** {format_date(selected.scheduled_date)}")
                st.write(f"**Shipped:** {format_date(selected.actual_ship_date) if selected.actual_ship_date else 'Pending'}")
                st.write(f"**Expected Delivery:** {format_date(selected.expected_delivery)}")
                st.write(f"**Delivered:** {format_date(selected.actual_delivery) if selected.actual_delivery else 'In Transit'}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Carrier Information**")
                st.write(f"**Carrier:** {selected.carrier or 'N/A'}")
                st.write(f"**Tracking Number:** {selected.tracking_number or 'N/A'}")
            
            with col2:
                st.write("**Handler**")
                if selected.logistics_handler:
                    handler = db.query(User).filter(User.user_id == selected.logistics_handler).first()
                    st.write(f"**Name:** {handler.full_name if handler else 'Unknown'}")
                    st.write(f"**Email:** {handler.email if handler else 'N/A'}")
            
            if selected.notes:
                st.write("**Notes**")
                st.info(selected.notes)
        
        elif search_shipment:
            display_info_message("No shipment found")
        
        else:
            st.info("Enter a shipment number above to track")
        
        # Delivery timeline
        st.subheader("Delivery Timeline")
        
        pending = [s for s in shipments if s.status.value == "pending"]
        in_transit = [s for s in shipments if s.status.value == "in_transit"]
        delivered = [s for s in shipments if s.status.value == "delivered"]
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Pending", len(pending))
        with col2:
            st.metric("In Transit", len(in_transit))
        with col3:
            st.metric("Delivered", len(delivered))
        with col4:
            total_shipped = sum(s.quantity_shipped for s in shipments)
            st.metric("Total Shipped", f"{total_shipped:.0f}")
        
    except Exception as e:
        display_error_message(f"Error loading tracking: {e}")
    finally:
        db.close()

def show_analytics():
    """Display logistics analytics"""
    st.subheader("Logistics Analytics")
    
    db = SessionLocal()
    try:
        shipments = db.query(Shipment).all()
        
        if not shipments:
            display_info_message("No shipment data available")
            return
        
        col1, col2 = st.columns(2)
        
        # Shipment status distribution
        with col1:
            status_counts = {}
            for s in shipments:
                status = s.status.value
                status_counts[status] = status_counts.get(status, 0) + 1
            
            df = pd.DataFrame(list(status_counts.items()), columns=["Status", "Count"])
            fig = px.pie(df, values="Count", names="Status", title="Shipment Status Distribution")
            st.plotly_chart(fig, width='stretch')
        
        # Quantity shipped by destination
        with col2:
            dest_data = {}
            for s in shipments:
                dest = s.destination
                dest_data[dest] = dest_data.get(dest, 0) + s.quantity_shipped
            
            df = pd.DataFrame(list(dest_data.items()), columns=["Destination", "Quantity"])
            fig = px.bar(df, x="Destination", y="Quantity", title="Quantity Shipped by Destination")
            st.plotly_chart(fig, width='stretch')
        
        # Carrier comparison
        st.subheader("Carrier Performance")
        
        carrier_data = {}
        for s in shipments:
            carrier = s.carrier or "Unknown"
            if carrier not in carrier_data:
                carrier_data[carrier] = {"count": 0, "quantity": 0}
            carrier_data[carrier]["count"] += 1
            carrier_data[carrier]["quantity"] += s.quantity_shipped
        
        df = pd.DataFrame([
            {"Carrier": c, "Shipments": d["count"], "Total Quantity": d["quantity"]}
            for c, d in carrier_data.items()
        ])
        
        fig = px.bar(df, x="Carrier", y=["Shipments", "Total Quantity"], barmode="group", title="Carrier Comparison")
        st.plotly_chart(fig, width='stretch')
        
        # Delivery time analysis
        st.subheader("Delivery Performance")
        
        on_time = 0
        delayed = 0
        pending = 0
        
        for s in shipments:
            if s.status.value == "delivered":
                if s.actual_delivery and s.expected_delivery:
                    if s.actual_delivery <= s.expected_delivery:
                        on_time += 1
                    else:
                        delayed += 1
            elif s.status.value == "in_transit":
                if s.expected_delivery and s.expected_delivery < datetime.utcnow():
                    delayed += 1
                else:
                    pending += 1
        
        perf_data = [
            {"Performance": "On Time", "Count": on_time},
            {"Performance": "Delayed", "Count": delayed},
            {"Performance": "Pending", "Count": pending}
        ]
        
        df = pd.DataFrame(perf_data)
        fig = px.bar(df, x="Performance", y="Count", title="Delivery Performance", color="Performance")
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading analytics: {e}")
    finally:
        db.close()
