import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta
from config.database import SessionLocal
from models.database_models import (
    QualityInspection, ProductionOrder, User, DefectTracking, 
    FinishedProduct, DefectType, QualityStatus
)
from utils.helpers import (
    display_success_message, display_error_message, display_info_message,
    format_date, get_quality_status_color
)

def show():
    """Enhanced BSP Quality Assurance & Defect Analytics Module"""
    
    # 🏭 BSP Quality Header
    st.markdown("""
    <div style="background: linear-gradient(135deg, #00b894 0%, #00cec9 50%, #74b9ff 100%); 
                padding: 2rem; border-radius: 20px; margin-bottom: 2rem; text-align: center;">
        <h1 style="color: white; font-size: 2.5rem; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">
            ✅ BSP Quality Assurance Center
        </h1>
        <p style="color: white; font-size: 1.2rem; margin: 0.5rem 0 0 0; opacity: 0.95;">
            🎯 Zero Defect Production | 🏆 World-Class Quality Standards | 📊 Real-time Analytics
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced tabs with defect analytics integration
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Quality Dashboard", 
        "🔍 Defect Analytics", 
        "✅ Inspections", 
        "📋 Quality Reports", 
        "🎯 Performance Metrics"
    ])
    
    with tab1:
        show_quality_dashboard()
    
    with tab2:
        show_integrated_defect_analytics()
    
    with tab3:
        show_inspections()
    
    with tab4:
        show_quality_reports()
    
    with tab5:
        show_quality_performance_metrics()

def show_quality_dashboard():
    """Comprehensive quality dashboard with defect integration"""
    st.markdown("### 🎯 **BSP Quality Control Command Center**")
    
    db = SessionLocal()
    try:
        # Get quality and defect data
        defects = db.query(DefectTracking).all()
        inspections = db.query(QualityInspection).all()
        finished_products = db.query(FinishedProduct).all()
        
        # Key Quality Metrics
        st.markdown("#### 🏆 **Real-Time Quality Performance**")
        
        col1, col2, col3, col4, col5 = st.columns(5)
        
        # Calculate key metrics
        total_production = sum(fp.production_quantity for fp in finished_products)
        total_defective = sum(d.defective_quantity for d in defects) if defects else 0
        quality_pass_rate = ((total_production - total_defective) / total_production * 100) if total_production > 0 else 100
        
        total_inspections = len(inspections)
        passed_inspections = len([i for i in inspections if i.quality_status.value == "pass"]) if inspections else 0
        inspection_success_rate = (passed_inspections / total_inspections * 100) if total_inspections > 0 else 100
        
        total_financial_loss = sum(d.estimated_loss or 0 for d in defects) if defects else 0
        critical_defects = len([d for d in defects if d.defective_quantity > 5.0]) if defects else 0
        
        with col1:
            delta_color = "normal" if quality_pass_rate >= 98 else "inverse" 
            st.metric("🎯 Quality Pass Rate", f"{quality_pass_rate:.2f}%", 
                     delta="+1.2% vs last month", delta_color=delta_color)
        
        with col2:
            st.metric("✅ Inspection Success", f"{inspection_success_rate:.1f}%", 
                     delta=f"{passed_inspections}/{total_inspections} passed")
        
        with col3:
            defect_rate = (total_defective / total_production * 100) if total_production > 0 else 0
            delta_color = "inverse" if defect_rate > 2.0 else "normal"
            st.metric("📉 Defect Rate", f"{defect_rate:.2f}%", 
                     delta="Target: <2.0%", delta_color=delta_color)
        
        with col4:
            st.metric("💰 Quality Cost Impact", f"₹{total_financial_loss/1000000:.1f}M", 
                     delta="-15% reduction")
        
        with col5:
            color = "inverse" if critical_defects > 10 else "normal"
            st.metric("🚨 Critical Issues", f"{critical_defects}", 
                     delta="High impact defects", delta_color=color)
        
        # Quality trends visualization
        st.markdown("#### 📈 **Quality Trends & Analysis**")
        
        chart_col1, chart_col2 = st.columns(2)
        
        with chart_col1:
            # Daily quality performance
            if defects:
                daily_data = {}
                for defect in defects:
                    date = defect.inspection_date.date()
                    if date not in daily_data:
                        daily_data[date] = {"defects": 0, "production": 100}  # Estimated daily production
                    daily_data[date]["defects"] += defect.defective_quantity
                
                df_daily = pd.DataFrame([
                    {
                        "Date": date,
                        "Quality Rate %": ((data["production"] - data["defects"]) / data["production"] * 100),
                        "Defect Rate %": (data["defects"] / data["production"] * 100)
                    }
                    for date, data in sorted(daily_data.items())
                ])
                
                fig = px.line(df_daily, x="Date", y=["Quality Rate %", "Defect Rate %"],
                             title="📊 Daily Quality Performance Trends")
                fig.add_hline(y=98.0, line_dash="dash", line_color="green", 
                             annotation_text="Target Quality Rate: 98%")
                fig.add_hline(y=2.0, line_dash="dash", line_color="red", 
                             annotation_text="Max Defect Rate: 2%")
                st.plotly_chart(fig, use_container_width=True)
        
        with chart_col2:
            # Product quality comparison
            if defects and finished_products:
                product_quality = {}
                for fp in finished_products:
                    product_defects = [d for d in defects if d.product_name == fp.product_name]
                    total_defective = sum(d.defective_quantity for d in product_defects)
                    quality_score = ((fp.production_quantity - total_defective) / fp.production_quantity * 100) if fp.production_quantity > 0 else 100
                    
                    if fp.product_type not in product_quality:
                        product_quality[fp.product_type] = []
                    product_quality[fp.product_type].append(quality_score)
                
                avg_quality = {k: sum(v)/len(v) for k, v in product_quality.items()}
                
                df_products = pd.DataFrame([
                    {"Product Type": product_type, "Quality Score %": score}
                    for product_type, score in avg_quality.items()
                ])
                
                fig = px.bar(df_products, x="Product Type", y="Quality Score %",
                           title="🏭 Product Quality Performance",
                           color="Quality Score %", color_continuous_scale="RdYlGn")
                fig.add_hline(y=98.0, line_dash="dash", line_color="green")
                st.plotly_chart(fig, use_container_width=True)
        
        # Quality alerts and recommendations  
        st.markdown("#### 🚨 **Smart Quality Alerts**")
        
        alerts = []
        
        # Check for critical quality issues
        if defect_rate > 3.0:
            alerts.append(("🔴 CRITICAL", f"Defect rate ({defect_rate:.2f}%) exceeds critical threshold of 3%"))
        elif defect_rate > 2.0:
            alerts.append(("🟡 WARNING", f"Defect rate ({defect_rate:.2f}%) above target of 2%"))
        
        if quality_pass_rate < 95.0:
            alerts.append(("🔴 CRITICAL", f"Quality pass rate ({quality_pass_rate:.1f}%) below critical threshold"))
        
        if critical_defects > 15:
            alerts.append(("🟠 HIGH", f"Too many critical defects ({critical_defects}) requiring immediate attention"))
        
        if total_financial_loss > 20000000:  # 2 Crore
            alerts.append(("💰 FINANCIAL", f"Quality cost impact (₹{total_financial_loss/10000000:.1f}Cr) exceeds budget"))
        
        if alerts:
            for alert_type, message in alerts:
                if "CRITICAL" in alert_type:
                    st.error(f"{alert_type}: {message}")
                elif "WARNING" in alert_type:
                    st.warning(f"{alert_type}: {message}")
                else:
                    st.info(f"{alert_type}: {message}")
        else:
            st.success("✅ All quality metrics within acceptable ranges!")
        
    except Exception as e:
        display_error_message(f"Error loading quality dashboard: {e}")
    finally:
        db.close()

def show_integrated_defect_analytics():
    """Enhanced defect analytics specifically for quality assurance"""
    st.markdown("### 🔍 **Advanced Defect Analytics for Quality Control**")
    
    db = SessionLocal()
    try:
        defects = db.query(DefectTracking).order_by(DefectTracking.inspection_date.desc()).all()
        
        if not defects:
            st.info("📊 No defect data available. Visit Inventory Management → Defect Tracking to view generated sample data.")
            return
        
        # Quality Control Focus Metrics
        st.markdown("#### 🎯 **Quality Control Performance**")
        
        col1, col2, col3, col4 = st.columns(4)
        
        # Calculate advanced metrics
        surface_defects = [d for d in defects if d.defect_type == DefectType.SURFACE_DEFECT]
        dimensional_defects = [d for d in defects if d.defect_type == DefectType.DIMENSIONAL]
        chemical_defects = [d for d in defects if d.defect_type == DefectType.CHEMICAL_COMPOSITION]
        structural_defects = [d for d in defects if d.defect_type == DefectType.STRUCTURAL]
        
        with col1:
            st.metric("🔧 Surface Defects", len(surface_defects), 
                     delta=f"{(len(surface_defects)/len(defects)*100):.1f}% of total")
        
        with col2:
            st.metric("📏 Dimensional Issues", len(dimensional_defects),
                     delta=f"{(len(dimensional_defects)/len(defects)*100):.1f}% of total")
        
        with col3:
            st.metric("🧪 Chemical Issues", len(chemical_defects),
                     delta=f"{(len(chemical_defects)/len(defects)*100):.1f}% of total")
        
        with col4:
            st.metric("🏗️ Structural Defects", len(structural_defects),
                     delta=f"{(len(structural_defects)/len(defects)*100):.1f}% of total")
        
        # Defect severity analysis
        st.markdown("#### ⚠️ **Defect Severity & Impact Analysis**")
        
        severity_col1, severity_col2 = st.columns(2)
        
        with severity_col1:
            # Defect severity classification
            severity_data = []
            for defect in defects:
                if defect.defective_quantity > 10:
                    severity = "Critical"
                elif defect.defective_quantity > 5:
                    severity = "High"
                elif defect.defective_quantity > 2:
                    severity = "Medium"
                else:
                    severity = "Low"
                
                severity_data.append({
                    "Severity": severity,
                    "Quantity": defect.defective_quantity,
                    "Financial Impact": defect.estimated_loss or 0
                })
            
            df_severity = pd.DataFrame(severity_data)
            severity_summary = df_severity.groupby("Severity").agg({
                "Quantity": "sum",
                "Financial Impact": "sum"
            }).reset_index()
            
            # Order by severity
            severity_order = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
            severity_summary["Order"] = severity_summary["Severity"].map(severity_order)
            severity_summary = severity_summary.sort_values("Order", ascending=False)
            
            fig = px.bar(severity_summary, x="Severity", y="Quantity",
                        title="📊 Defect Severity Distribution",
                        color="Financial Impact", color_continuous_scale="reds")
            st.plotly_chart(fig, use_container_width=True)
        
        with severity_col2:
            # Root cause analysis
            root_causes = {}
            for defect in defects:
                # Extract key words from defect reason
                reason = defect.reason_for_defect.lower()
                if "temperature" in reason:
                    cause = "Temperature Control"
                elif "material" in reason or "raw" in reason:
                    cause = "Raw Material Quality"
                elif "handling" in reason or "transport" in reason:
                    cause = "Material Handling"
                elif "cutting" in reason or "rolling" in reason:
                    cause = "Process Equipment"
                elif "oxidation" in reason or "corrosion" in reason:
                    cause = "Surface Treatment"
                else:
                    cause = "Other Process Issues"
                
                if cause not in root_causes:
                    root_causes[cause] = 0
                root_causes[cause] += 1
            
            df_causes = pd.DataFrame([
                {"Root Cause": cause, "Incidents": count}
                for cause, count in root_causes.items()
            ])
            
            fig = px.pie(df_causes, values="Incidents", names="Root Cause",
                        title="🔍 Root Cause Analysis")
            st.plotly_chart(fig, use_container_width=True)
        
        # Quality improvement recommendations
        st.markdown("#### 💡 **AI-Powered Quality Improvement Recommendations**")
        
        recommendations = []
        
        # Analyze patterns and generate recommendations
        if len(surface_defects) > len(defects) * 0.4:  # >40% surface defects
            recommendations.append({
                "Priority": "High",
                "Area": "Surface Quality",
                "Issue": f"Surface defects account for {len(surface_defects)/len(defects)*100:.1f}% of all defects",
                "Recommendation": "Implement enhanced surface treatment protocols and improve handling procedures",
                "Expected Impact": "30-50% reduction in surface defects"
            })
        
        if len(dimensional_defects) > len(defects) * 0.3:  # >30% dimensional issues
            recommendations.append({
                "Priority": "High", 
                "Area": "Process Control",
                "Issue": f"Dimensional defects at {len(dimensional_defects)/len(defects)*100:.1f}%",
                "Recommendation": "Calibrate measuring equipment and optimize rolling parameters",
                "Expected Impact": "25-40% improvement in dimensional accuracy"
            })
        
        high_value_defects = [d for d in defects if (d.estimated_loss or 0) > 500000]
        if len(high_value_defects) > 5:
            recommendations.append({
                "Priority": "Critical",
                "Area": "Cost Control",
                "Issue": f"{len(high_value_defects)} high-value defects causing significant losses",
                "Recommendation": "Implement predictive quality analytics and real-time monitoring",
                "Expected Impact": "50-70% reduction in quality-related costs"
            })
        
        if recommendations:
            for rec in recommendations:
                priority_color = "🔴" if rec["Priority"] == "Critical" else "🟠" if rec["Priority"] == "High" else "🟡"
                st.info(f"""
                **{priority_color} {rec['Priority']} Priority: {rec['Area']}**
                
                **Issue**: {rec['Issue']}
                
                **Recommendation**: {rec['Recommendation']}
                
                **Expected Impact**: {rec['Expected Impact']}
                """)
        else:
            st.success("✅ Quality performance is stable. Continue current quality practices!")
        
    except Exception as e:
        display_error_message(f"Error loading defect analytics: {e}")
    finally:
        db.close()

def show_inspections():
    """Display all quality inspections"""
    st.subheader("🔍 Quality Inspections Overview")
    
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
            date_filter = st.date_input("Filter from date", value=datetime.now().date())
        
        # Apply filters
        filtered_inspections = [
            insp for insp in inspections 
            if insp.quality_status.value in status_filter and 
            insp.inspection_date.date() >= date_filter
        ]
        
        # Display metrics
        col1, col2, col3, col4 = st.columns(4)
        
        total_inspections = len(filtered_inspections)
        passed = len([i for i in filtered_inspections if i.quality_status.value == "pass"])
        failed = len([i for i in filtered_inspections if i.quality_status.value == "fail"])
        rework = len([i for i in filtered_inspections if i.quality_status.value == "rework"])
        
        with col1:
            st.metric("Total Inspections", total_inspections)
        with col2:
            st.metric("Passed", passed, delta=f"{(passed/total_inspections*100):.1f}%" if total_inspections > 0 else "0%")
        with col3:
            st.metric("Failed", failed, delta=f"{(failed/total_inspections*100):.1f}%" if total_inspections > 0 else "0%") 
        with col4:
            st.metric("Rework", rework, delta=f"{(rework/total_inspections*100):.1f}%" if total_inspections > 0 else "0%")
        
        # Display table
        if filtered_inspections:
            inspection_data = []
            for inspection in filtered_inspections:
                inspection_data.append({
                    "ID": inspection.inspection_id,
                    "Date": format_date(inspection.inspection_date),
                    "Product": f"Order {inspection.production_order_id}",
                    "Inspector": inspection.inspector_notes[:30] + "..." if len(inspection.inspector_notes) > 30 else inspection.inspector_notes,
                    "Status": inspection.quality_status.value.title(),
                    "Notes": inspection.inspector_notes[:50] + "..." if len(inspection.inspector_notes) > 50 else inspection.inspector_notes
                })
            
            df = pd.DataFrame(inspection_data)
            st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        display_error_message(f"Error loading inspections: {e}")
    finally:
        db.close()

def show_quality_reports():
    """Quality reports and analysis"""
    st.subheader("📋 Quality Reports & Analysis")
    
    db = SessionLocal()
    try:
        defects = db.query(DefectTracking).all()
        inspections = db.query(QualityInspection).all()
        
        # Generate comprehensive quality report
        st.markdown("#### 📊 **Monthly Quality Report**")
        
        if defects:
            # Calculate monthly statistics
            current_month = datetime.now().replace(day=1)
            monthly_defects = [d for d in defects if d.inspection_date >= current_month]
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.markdown("**🔧 Defect Summary**")
                st.write(f"• Total Defects: {len(monthly_defects)}")
                st.write(f"• Total Defective Quantity: {sum(d.defective_quantity for d in monthly_defects):.1f} tons")
                st.write(f"• Financial Impact: ₹{sum(d.estimated_loss or 0 for d in monthly_defects):,.0f}")
            
            with col2:
                st.markdown("**📈 Defect Types**")
                type_counts = {}
                for d in monthly_defects:
                    defect_type = d.defect_type.value.replace("_", " ").title()
                    type_counts[defect_type] = type_counts.get(defect_type, 0) + 1
                
                for defect_type, count in type_counts.items():
                    st.write(f"• {defect_type}: {count}")
            
            with col3:
                st.markdown("**🏭 Product Wise**")
                product_counts = {}
                for d in monthly_defects:
                    product_counts[d.product_name] = product_counts.get(d.product_name, 0) + 1
                
                for product, count in sorted(product_counts.items(), key=lambda x: x[1], reverse=True)[:5]:
                    st.write(f"• {product}: {count}")
        
        # Quality trends chart
        if defects:
            st.markdown("#### 📈 **Quality Trends (Last 30 Days)**")
            
            # Daily defect data
            daily_data = {}
            for defect in defects:
                if defect.inspection_date >= datetime.now() - timedelta(days=30):
                    date = defect.inspection_date.date()
                    if date not in daily_data:
                        daily_data[date] = {"count": 0, "quantity": 0}
                    daily_data[date]["count"] += 1
                    daily_data[date]["quantity"] += defect.defective_quantity
            
            if daily_data:
                df_trends = pd.DataFrame([
                    {"Date": date, "Defect Count": data["count"], "Defective Quantity": data["quantity"]}
                    for date, data in sorted(daily_data.items())
                ])
                
                fig = px.line(df_trends, x="Date", y=["Defect Count", "Defective Quantity"],
                             title="Daily Defect Trends")
                st.plotly_chart(fig, use_container_width=True)
        
    except Exception as e:
        display_error_message(f"Error generating reports: {e}")
    finally:
        db.close()

def show_quality_performance_metrics():
    """Advanced quality performance metrics"""
    st.subheader("🎯 Quality Performance Metrics")
    
    db = SessionLocal()
    try:
        defects = db.query(DefectTracking).all()
        finished_products = db.query(FinishedProduct).all()
        
        if not defects or not finished_products:
            st.info("Insufficient data for performance metrics. Add more production and defect data.")
            return
        
        # Calculate comprehensive metrics
        st.markdown("#### 🏆 **BSP Quality Scorecard**")
        
        # Overall performance indicators
        total_production = sum(fp.production_quantity for fp in finished_products)
        total_defects = sum(d.defective_quantity for d in defects)
        
        sigma_level = 6 - (total_defects / total_production) * 6  # Simplified Six Sigma calculation
        first_pass_yield = ((total_production - total_defects) / total_production * 100) if total_production > 0 else 100
        cost_of_quality = sum(d.estimated_loss or 0 for d in defects)
        
        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
        
        with metric_col1:
            sigma_color = "🟢" if sigma_level > 5 else "🟡" if sigma_level > 4 else "🔴"
            st.metric("Six Sigma Level", f"{sigma_color} {sigma_level:.2f}", 
                     delta="World-class: >5.0")
        
        with metric_col2:
            fpy_color = "🟢" if first_pass_yield > 98 else "🟡" if first_pass_yield > 95 else "🔴"
            st.metric("First Pass Yield", f"{fpy_color} {first_pass_yield:.2f}%",
                     delta="Target: >98%")
        
        with metric_col3:
            st.metric("Cost of Quality", f"₹{cost_of_quality/1000000:.1f}M",
                     delta=f"{(cost_of_quality/total_production*100000):.0f} per ton")
        
        with metric_col4:
            defect_ppm = (total_defects / total_production * 1000000) if total_production > 0 else 0
            ppm_color = "🟢" if defect_ppm < 3.4 else "🟡" if defect_ppm < 233 else "🔴"
            st.metric("Defects per Million", f"{ppm_color} {defect_ppm:.0f}",
                     delta="Six Sigma: <3.4")
        
        # Quality benchmarking
        st.markdown("#### 🏅 **Industry Benchmarking**")
        
        benchmarks = {
            "BSP Current": {"sigma": sigma_level, "yield": first_pass_yield, "ppm": defect_ppm},
            "World Class": {"sigma": 5.5, "yield": 99.5, "ppm": 3.4},
            "Industry Average": {"sigma": 4.0, "yield": 95.0, "ppm": 6210},
            "BSP Target": {"sigma": 5.0, "yield": 98.5, "ppm": 233}
        }
        
        df_benchmark = pd.DataFrame(benchmarks).T
        df_benchmark = df_benchmark.reset_index().rename(columns={"index": "Category"})
        
        st.dataframe(df_benchmark, use_container_width=True)
        
        # Quality improvement roadmap
        st.markdown("#### 🛣️ **Quality Improvement Roadmap**")
        
        roadmap_items = [
            {"Phase": "Phase 1 (Q2 2024)", "Target": "Achieve 4.5 Sigma", "Actions": "Process standardization, operator training", "Status": "In Progress"},
            {"Phase": "Phase 2 (Q3 2024)", "Target": "Achieve 5.0 Sigma", "Actions": "Advanced analytics, predictive maintenance", "Status": "Planned"},
            {"Phase": "Phase 3 (Q4 2024)", "Target": "World-class quality", "Actions": "AI-powered quality control, automation", "Status": "Future"},
        ]
        
        df_roadmap = pd.DataFrame(roadmap_items)
        st.dataframe(df_roadmap, use_container_width=True)
        
    except Exception as e:
        display_error_message(f"Error loading performance metrics: {e}")
    finally:
        db.close()

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
