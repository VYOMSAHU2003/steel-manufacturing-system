import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime
from config.database import SessionLocal
from models.database_models import QualityInspection, ProductionOrder, User
from utils.helpers import (
    display_success_message, display_error_message, display_info_message,
    format_date, get_quality_status_color
)

def show():
    """Display Quality Assurance module"""
    st.title("✅ Quality Assurance")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Inspections", "Create Inspection", "Reports", "Metrics"])
    
    with tab1:
        show_inspections()
    
    with tab2:
        show_create_inspection()
    
    with tab3:
        show_reports()
    
    with tab4:
        show_metrics()

def show_inspections():
    """Display all quality inspections"""
    st.subheader("Quality Inspections")
    
    db = SessionLocal()
    try:
        inspections = db.query(QualityInspection).all()
        
        if not inspections:
            display_info_message("No quality inspections recorded")
            return
        
        # Filter options
        col1, col2 = st.columns(2)
        
        with col1:
            status_filter = st.multiselect(
                "Filter by Status",
                options=["pass", "fail", "rework"],
                default=["pass", "fail", "rework"]
            )
        
        with col2:
            sort_by = st.selectbox("Sort by", options=["Date", "Status", "Order"])
        
        # Filter inspections
        filtered_inspections = [i for i in inspections if i.status.value in status_filter]
        
        if not filtered_inspections:
            display_info_message("No inspections match filters")
            return
        
        # Create display dataframe
        data = []
        for insp in filtered_inspections:
            order = db.query(ProductionOrder).filter(ProductionOrder.order_id == insp.order_id).first()
            tester = db.query(User).filter(User.user_id == insp.tested_by).first() if insp.tested_by else None
            
            data.append({
                "Inspection ID": insp.inspection_id,
                "Order": order.order_number if order else "Unknown",
                "Date": format_date(insp.inspection_date),
                "Status": f"{get_quality_status_color(insp.status.value)} {insp.status.value.upper()}",
                "Tensile (MPa)": f"{insp.tensile_strength:.1f}" if insp.tensile_strength else "-",
                "Hardness": f"{insp.hardness:.1f}" if insp.hardness else "-",
                "Ductility": f"{insp.ductility:.1f}" if insp.ductility else "-",
                "Surface": insp.surface_quality or "-",
                "Tested By": tester.full_name if tester else "Unknown",
                "Rework": "Yes" if insp.rework_required else "No"
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, width='stretch', hide_index=True)
        
    except Exception as e:
        display_error_message(f"Error loading inspections: {e}")
    finally:
        db.close()

def show_create_inspection():
    """Display form to create new inspection"""
    st.subheader("Create Quality Inspection")
    
    db = SessionLocal()
    try:
        # Get active orders
        orders = db.query(ProductionOrder).filter(
            ProductionOrder.status.in_(["in_progress", "completed"])
        ).all()
        
        if not orders:
            display_info_message("No active orders for inspection")
            return
        
        inspectors = db.query(User).filter(User.role == "quality").all()
        
        with st.form("create_inspection_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                selected_order = st.selectbox(
                    "Order to Inspect",
                    options=[(o.order_id, o.order_number) for o in orders],
                    format_func=lambda x: x[1]
                )
                
                tensile_strength = st.number_input(
                    "Tensile Strength (MPa)",
                    min_value=0.0,
                    step=0.1,
                    help="Minimum acceptable: 250 MPa for standard steel"
                )
            
            with col2:
                hardness = st.number_input(
                    "Hardness (HB)",
                    min_value=0.0,
                    step=0.1,
                    help="Brinell Hardness"
                )
                
                ductility = st.number_input(
                    "Ductility (%)",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.1,
                    help="Minimum acceptable: 20%"
                )
            
            col1, col2 = st.columns(2)
            
            with col1:
                surface_quality = st.selectbox(
                    "Surface Quality",
                    options=["Excellent", "Good", "Acceptable", "Poor", "Defective"]
                )
                
                inspector = st.selectbox(
                    "Inspector",
                    options=[(u.user_id, u.full_name) for u in inspectors] if inspectors else [],
                    format_func=lambda x: x[1] if x else "No inspectors available"
                ) if inspectors else None
            
            with col2:
                # Determine status based on criteria
                st.write("**Assessment Criteria:**")
                st.caption("• Tensile ≥ 250 MPa")
                st.caption("• Ductility ≥ 20%")
                st.caption("• Surface: Good or Better")
            
            defects_found = st.text_area("Defects Found", placeholder="List any defects...")
            
            rework_required = st.checkbox("Rework Required")
            
            notes = st.text_area("Additional Notes", placeholder="Inspector notes...")
            
            submitted = st.form_submit_button("Create Inspection", width='stretch', type="primary")
            
            if submitted:
                if not selected_order:
                    display_error_message("Please select an order")
                else:
                    try:
                        # Determine status
                        status = "pass"
                        if (tensile_strength < 250 or ductility < 20 or 
                            surface_quality in ["Poor", "Defective"] or defects_found):
                            status = "fail"
                        elif rework_required:
                            status = "rework"
                        
                        new_inspection = QualityInspection(
                            order_id=selected_order[0],
                            inspection_date=datetime.utcnow(),
                            tested_by=inspector[0] if inspector else None,
                            status=status,
                            tensile_strength=tensile_strength if tensile_strength > 0 else None,
                            hardness=hardness if hardness > 0 else None,
                            ductility=ductility if ductility > 0 else None,
                            surface_quality=surface_quality,
                            defects_found=defects_found if defects_found else None,
                            rework_required=rework_required,
                            notes=notes if notes else None
                        )
                        
                        db.add(new_inspection)
                        db.commit()
                        
                        display_success_message(f"Inspection created with status: {status.upper()}")
                        st.balloons()
                        st.rerun()
                    except Exception as e:
                        display_error_message(f"Error creating inspection: {e}")
    
    finally:
        db.close()

def show_reports():
    """Display quality reports"""
    st.subheader("Quality Reports")
    
    db = SessionLocal()
    try:
        inspections = db.query(QualityInspection).all()
        
        if not inspections:
            display_info_message("No inspection data available")
            return
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_inspections = len(inspections)
        passed = sum(1 for i in inspections if i.status.value == "pass")
        failed = sum(1 for i in inspections if i.status.value == "fail")
        rework = sum(1 for i in inspections if i.status.value == "rework")
        
        pass_rate = (passed / total_inspections * 100) if total_inspections > 0 else 0
        
        with col1:
            st.metric("Total Inspections", total_inspections)
        with col2:
            st.metric("Pass Rate", f"{pass_rate:.1f}%")
        with col3:
            st.metric("Failed", failed)
        with col4:
            st.metric("Rework Required", rework)
        
        # Status distribution
        col1, col2 = st.columns(2)
        
        with col1:
            status_data = [
                {"Status": "Pass", "Count": passed},
                {"Status": "Fail", "Count": failed},
                {"Status": "Rework", "Count": rework}
            ]
            
            df = pd.DataFrame(status_data)
            fig = px.pie(df, values="Count", names="Status", title="Inspection Status Distribution")
            st.plotly_chart(fig, width='stretch')
        
        with col2:
            fig = px.bar(df, x="Status", y="Count", title="Inspection Results", color="Status")
            st.plotly_chart(fig, width='stretch')
        
        # Trend over time
        st.subheader("Inspection Trend")
        
        # Group by date
        date_status = {}
        for insp in inspections:
            date = insp.inspection_date.strftime("%Y-%m-%d")
            if date not in date_status:
                date_status[date] = {"pass": 0, "fail": 0, "rework": 0}
            date_status[date][insp.status.value] += 1
        
        trend_data = []
        for date in sorted(date_status.keys()):
            for status, count in date_status[date].items():
                trend_data.append({"Date": date, "Status": status, "Count": count})
        
        df = pd.DataFrame(trend_data)
        fig = px.line(df, x="Date", y="Count", color="Status", title="Inspection Trend")
        st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading reports: {e}")
    finally:
        db.close()

def show_metrics():
    """Display quality metrics"""
    st.subheader("Quality Metrics")
    
    db = SessionLocal()
    try:
        inspections = db.query(QualityInspection).all()
        
        if not inspections:
            display_info_message("No inspection data available")
            return
        
        # Tensile strength analysis
        st.write("**Tensile Strength Analysis**")
        
        col1, col2, col3 = st.columns(3)
        
        tensile_values = [i.tensile_strength for i in inspections if i.tensile_strength]
        
        if tensile_values:
            with col1:
                st.metric("Avg Tensile Strength", f"{np.mean(tensile_values):.1f} MPa")
            with col2:
                st.metric("Min Tensile Strength", f"{np.min(tensile_values):.1f} MPa")
            with col3:
                st.metric("Max Tensile Strength", f"{np.max(tensile_values):.1f} MPa")
            
            # Histogram
            hist_data = pd.DataFrame({"Tensile Strength (MPa)": tensile_values})
            fig = px.histogram(hist_data, x="Tensile Strength (MPa)", nbins=20, title="Tensile Strength Distribution")
            st.plotly_chart(fig, width='stretch')
        
        # Ductility analysis
        st.write("**Ductility Analysis**")
        
        col1, col2, col3 = st.columns(3)
        
        ductility_values = [i.ductility for i in inspections if i.ductility is not None]
        
        if ductility_values:
            with col1:
                st.metric("Avg Ductility", f"{np.mean(ductility_values):.1f}%")
            with col2:
                st.metric("Min Ductility", f"{np.min(ductility_values):.1f}%")
            with col3:
                st.metric("Max Ductility", f"{np.max(ductility_values):.1f}%")
            
            # Histogram
            hist_data = pd.DataFrame({"Ductility (%)": ductility_values})
            fig = px.histogram(hist_data, x="Ductility (%)", nbins=20, title="Ductility Distribution")
            st.plotly_chart(fig, width='stretch')
        
        # Surface quality distribution
        st.write("**Surface Quality Distribution**")
        
        surface_counts = {}
        for insp in inspections:
            if insp.surface_quality:
                surface_counts[insp.surface_quality] = surface_counts.get(insp.surface_quality, 0) + 1
        
        if surface_counts:
            df = pd.DataFrame(list(surface_counts.items()), columns=["Quality", "Count"])
            fig = px.bar(df, x="Quality", y="Count", title="Surface Quality Distribution")
            st.plotly_chart(fig, width='stretch')
        
    except Exception as e:
        display_error_message(f"Error loading metrics: {e}")
    finally:
        db.close()
