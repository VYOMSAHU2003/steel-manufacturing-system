import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pages import (
    authentication,
    raw_materials,
    production_planning,
    inventory_management,
    quality_assurance,
    logistics_shipment
)

def main():
    st.set_page_config(
        page_title="BSP Digital Manufacturing System",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Enhanced CSS for BSP branding and modern UI with creative design
    st.markdown("""
        <style>
        /* Import Modern Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800&family=Roboto:wght@300;400;500;700&display=swap');
        
        /* Global Styles with Enhanced Spacing */
        .main {
            padding: 0.5rem 1.5rem;
            font-family: 'Poppins', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }
        
        /* Revolutionary Header Design */
        .bsp-header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
            color: white;
            padding: 2rem;
            border-radius: 25px;
            margin-bottom: 1.5rem;
            box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4);
            text-align: center;
            position: relative;
            overflow: hidden;
            animation: headerPulse 3s ease-in-out infinite alternate;
        }
        
        @keyframes headerPulse {
            0% { box-shadow: 0 20px 40px rgba(102, 126, 234, 0.4); }
            100% { box-shadow: 0 25px 50px rgba(102, 126, 234, 0.6); }
        }
        
        .bsp-header::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
            animation: shine 2s infinite;
        }
        
        @keyframes shine {
            0% { left: -100%; }
            100% { left: 100%; }
        }
        
        .bsp-title {
            font-size: 3rem;
            font-weight: 800;
            margin: 0;
            background: linear-gradient(45deg, #ffffff, #ffeaa7, #fab1a0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            animation: titleGlow 2s ease-in-out infinite alternate;
        }
        
        @keyframes titleGlow {
            0% { filter: drop-shadow(0 0 5px rgba(255,255,255,0.5)); }
            100% { filter: drop-shadow(0 0 20px rgba(255,255,255,0.8)); }
        }
        
        .bsp-subtitle {
            font-size: 1.3rem;
            font-weight: 400;
            margin: 0.5rem 0 0 0;
            opacity: 0.95;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Modern Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, rgba(255,255,255,0.95) 0%, rgba(248,249,250,0.95) 100%);
            backdrop-filter: blur(10px);
            border-right: none;
            border-radius: 0 20px 20px 0;
            box-shadow: 5px 0 25px rgba(0,0,0,0.1);
        }
        
        /* Revolutionary Metrics Cards */
        .metric-card {
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
            backdrop-filter: blur(15px);
            padding: 1.8rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            margin: 0.8rem 0;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            position: relative;
            overflow: hidden;
        }
        
        .metric-card::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(90deg, transparent, rgba(102, 126, 234, 0.1), transparent);
            transition: left 0.5s;
        }
        
        .metric-card:hover {
            transform: translateY(-8px) scale(1.02);
            box-shadow: 0 20px 40px rgba(0,0,0,0.2);
            border-color: rgba(102, 126, 234, 0.3);
        }
        
        .metric-card:hover::before {
            left: 100%;
        }
        
        .metric-title {
            font-size: 0.95rem;
            color: #667eea;
            font-weight: 600;
            margin-bottom: 0.8rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .metric-value {
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
        }
        
        .metric-change {
            font-size: 0.9rem;
            color: #00b894;
            font-weight: 600;
            margin-top: 0.5rem;
        }
        
        /* Modern Status Indicators with Glassmorphism */
        .status-online {
            background: linear-gradient(135deg, rgba(0, 184, 148, 0.2), rgba(85, 239, 196, 0.2));
            backdrop-filter: blur(10px);
            color: #00b894;
            border: 1px solid rgba(0, 184, 148, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            margin: 0.3rem 0;
            animation: statusPulse 2s infinite;
        }
        
        .status-warning {
            background: linear-gradient(135deg, rgba(253, 203, 110, 0.2), rgba(255, 177, 43, 0.2));
            backdrop-filter: blur(10px);
            color: #fdcb6e;
            border: 1px solid rgba(253, 203, 110, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            margin: 0.3rem 0;
        }
        
        .status-offline {
            background: linear-gradient(135deg, rgba(231, 76, 60, 0.2), rgba(192, 57, 43, 0.2));
            backdrop-filter: blur(10px);
            color: #e74c3c;
            border: 1px solid rgba(231, 76, 60, 0.3);
            padding: 0.5rem 1rem;
            border-radius: 25px;
            font-size: 0.9rem;
            font-weight: 600;
            margin: 0.3rem 0;
        }
        
        @keyframes statusPulse {
            0% { box-shadow: 0 0 0 0 rgba(0, 184, 148, 0.4); }
            70% { box-shadow: 0 0 0 10px rgba(0, 184, 148, 0); }
            100% { box-shadow: 0 0 0 0 rgba(0, 184, 148, 0); }
        }
        
        /* Hide Streamlit branding */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stDeployButton {display:none;}
        
        /* Revolutionary Tab Design */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
            backdrop-filter: blur(15px);
            padding: 0.8rem;
            border-radius: 20px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            margin-bottom: 1rem;
        }
        
        .stTabs [data-baseweb="tab-list"] button {
            background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.6));
            backdrop-filter: blur(10px);
            border-radius: 15px;
            border: 1px solid rgba(255,255,255,0.3);
            padding: 1rem 1.8rem;
            font-weight: 600;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            color: #667eea;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-size: 0.85rem;
        }
        
        .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
            transform: translateY(-2px);
        }
        
        .stTabs [data-baseweb="tab-list"] button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        /* Enhanced Button Styling */
        .stButton > button {
            border-radius: 15px;
            font-weight: 600;
            transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            background: linear-gradient(135deg, #667eea, #764ba2);
            color: white;
            border: none;
            padding: 0.8rem 1.5rem;
            font-size: 0.9rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        .stButton > button:hover {
            transform: translateY(-3px) scale(1.05);
            box-shadow: 0 15px 35px rgba(102, 126, 234, 0.4);
            background: linear-gradient(135deg, #764ba2, #667eea);
        }
        
        /* Revolutionary Navbar */
        .bsp-navbar {
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1));
            backdrop-filter: blur(20px);
            padding: 1rem 1.5rem;
            border-radius: 25px;
            margin: 1rem 0;
            box-shadow: 0 15px 35px rgba(0,0,0,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            display: flex;
            flex-wrap: wrap;
            gap: 0.5rem;
            align-items: center;
            justify-content: center;
        }
        
        /* User Info Bar Enhancement */
        .user-info-bar {
            background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
            backdrop-filter: blur(15px);
            padding: 1rem;
            border-radius: 20px;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.2);
        }
        
        /* Content Container */
        .content-container {
            background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
            backdrop-filter: blur(15px);
            padding: 2rem;
            border-radius: 25px;
            margin: 1rem 0;
            border: 1px solid rgba(255,255,255,0.2);
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Enhanced session state management
    session_defaults = {
        'user': None,
        'role': None,
        'username': None,
        'user_id': None,
        'email': None,
        'plant_section': 'Main Plant',
        'shift': 'Day Shift',
        'authenticated': False
    }
    
    for key, default_value in session_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value
    
    # Check if user is logged in - simplified check
    is_authenticated = (
        st.session_state.user is not None and 
        st.session_state.role is not None and
        st.session_state.username is not None
    )
    
    if not is_authenticated:
        authentication.show_login_page()
    else:
        show_main_application()

def show_main_application():
    """Enhanced main application with modern BSP-specific features"""
    
    # Revolutionary BSP Header with animations
    st.markdown(f"""
        <div class="bsp-header">
            <h1 class="bsp-title">🏭 Bhilai Steel Plant</h1>
            <p class="bsp-subtitle">Digital Manufacturing System | Industry 4.0 Platform</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 1rem; opacity: 0.9; font-weight: 500;">
                🔴 LIVE • {datetime.now().strftime("%d %B %Y, %I:%M %p")} • {st.session_state.shift}
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    # Modern Horizontal Navigation
    show_navbar()
    
    # Enhanced User Info Bar with modern glassmorphism design 
    st.markdown('<div class="user-info-bar">', unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns([2.5, 2.5, 2.5, 1.5])
    with col1:
        st.markdown(f"""<div style="color: #667eea; font-weight: 600; font-size: 1rem;">
            👤 {st.session_state.user} | <span style="color: #764ba2;">{st.session_state.role.upper()}</span>
            </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""<div style="color: #667eea; font-weight: 600; font-size: 1rem;">
            🏭 {st.session_state.plant_section} | <span style="color: #764ba2;">{st.session_state.shift}</span>
            </div>""", unsafe_allow_html=True)
    with col3:
        plant_status = get_plant_status()
        online_count = sum(1 for status in plant_status.values() if status == "Online")
        st.markdown(f"""<div style="color: #00b894; font-weight: 600; font-size: 1rem;">
            ⚡ Plant: <span style="color: #667eea;">{online_count}/{len(plant_status)} Online</span>
            </div>""", unsafe_allow_html=True)
    with col4:
        if st.button("🚪 Logout", type="secondary", use_container_width=True):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Modern Content Container
    st.markdown('<div class="content-container">', unsafe_allow_html=True)
    
    # Compact Enhanced Sidebar
    with st.sidebar:
        st.markdown("### 🏭 Live Plant Monitoring")
        
        # Real-time status with modern indicators
        plant_status = get_plant_status()
        for unit, status in plant_status.items():
            color_class = ("status-online" if status == "Online" 
                          else "status-warning" if status == "Maintenance" 
                          else "status-offline")
            emoji = "🟢" if status == "Online" else "🟡" if status == "Maintenance" else "🔴"
            st.markdown(f'<div class="{color_class}">{emoji} {unit}: {status}</div>', 
                       unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Enhanced Quick Statistics with modern cards
        st.markdown("### 📊 Real-Time Stats")
        
        online_count = sum(1 for status in plant_status.values() if status == "Online")
        maintenance_count = sum(1 for status in plant_status.values() if status == "Maintenance")
        
        # Modern metric cards for sidebar
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(0, 184, 148, 0.1), rgba(85, 239, 196, 0.1)); 
                    backdrop-filter: blur(10px); padding: 1rem; border-radius: 15px; 
                    border: 1px solid rgba(0, 184, 148, 0.2); margin: 0.5rem 0;">
            <div style="color: #00b894; font-weight: 600; font-size: 0.9rem;">🟢 ONLINE UNITS</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #00b894;">{online_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(253, 203, 110, 0.1), rgba(255, 177, 43, 0.1)); 
                    backdrop-filter: blur(10px); padding: 1rem; border-radius: 15px; 
                    border: 1px solid rgba(253, 203, 110, 0.2); margin: 0.5rem 0;">
            <div style="color: #fdcb6e; font-weight: 600; font-size: 0.9rem;">🟡 MAINTENANCE</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #fdcb6e;">{maintenance_count}</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
                    backdrop-filter: blur(10px); padding: 1rem; border-radius: 15px; 
                    border: 1px solid rgba(102, 126, 234, 0.2); margin: 0.5rem 0;">
            <div style="color: #667eea; font-weight: 600; font-size: 0.9rem;">⚡ EFFICIENCY</div>
            <div style="font-size: 1.8rem; font-weight: 700; color: #667eea;">95.4%</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Enhanced Emergency Controls
        st.markdown("---")
        st.markdown("### 🚨 Emergency Controls")
        
        if st.button("🛑 Emergency Stop", type="secondary", use_container_width=True):
            st.error("🚨 Emergency stop initiated! All operations halted.")
            
        if st.button("🚨 Alert Management", type="secondary", use_container_width=True):
            st.warning("📢 Alert system activated - Management notified")
            
        # Enhanced Admin Controls
        if st.session_state.role in ['admin', 'manager']:
            st.markdown("---")
            st.markdown("### ⚡ Admin Control Panel")
            
            if st.button("📊 System Diagnostics", use_container_width=True):
                st.success("🔧 Running comprehensive system diagnostics...")
                
            if st.button("🔧 Maintenance Mode", use_container_width=True):
                st.info("⚙️ Maintenance mode activated - Limited access enabled")
    
    # Route to the selected module
    if 'selected_module' in st.session_state:
        route_to_module(st.session_state.selected_module)
    else:
        show_plant_overview()
        
    st.markdown('</div>', unsafe_allow_html=True)

def get_plant_status():
    """Get real-time plant status simulation"""
    statuses = ["Online", "Maintenance", "Offline"]
    weights = [0.8, 0.15, 0.05]  # 80% online, 15% maintenance, 5% offline
    
    return {
        "Blast Furnace #8": np.random.choice(statuses, p=weights),
        "SMS #3": np.random.choice(statuses, p=weights), 
        "Rolling Mill #2": np.random.choice(statuses, p=weights),
        "Coke Plant": np.random.choice(statuses, p=weights),
        "Power Plant": "Online",  # Always online
        "Sinter Plant": np.random.choice(statuses, p=weights)
    }

def get_navigation_options(role):
    """Get role-based navigation options"""
    base_options = [
        "🏭 Plant Overview",
        "📦 Raw Materials", 
        "🔥 Production Planning",
        "📊 Inventory Management",
        "✅ Quality Assurance",
        "🚚 Logistics & Shipment"
    ]
    
    if role in ['admin', 'manager']:
        base_options.extend([
            "⚡ Energy Management",
            "🛡️ Safety & Environment", 
            "🤖 AI Analytics"
        ])
    
    return base_options

def show_navbar():
    """Display modern horizontal navigation bar with enhanced UX"""
    nav_options = get_navigation_options(st.session_state.role)
    
    if 'selected_module' not in st.session_state:
        st.session_state.selected_module = nav_options[0]
    
    # Modern navbar container with glassmorphism
    st.markdown('<div class="bsp-navbar">', unsafe_allow_html=True)
    
    # Calculate optimal columns based on number of options
    num_options = len(nav_options)
    cols = st.columns(num_options)
    
    for i, option in enumerate(nav_options):
        with cols[i]:
            button_key = f"nav_btn_{option.replace(' ', '_').replace('&', 'and')}"
            
            # Enhanced button styling based on selection state
            is_selected = st.session_state.selected_module == option
            button_type = "primary" if is_selected else "secondary"
            
            # Create custom styled button
            if st.button(
                option, 
                key=button_key, 
                use_container_width=True,
                type=button_type,
                help=f"Navigate to {option.replace('🏭 ', '').replace('📦 ', '').replace('🔥 ', '').replace('📊 ', '').replace('✅ ', '').replace('🚚 ', '').replace('⚡ ', '').replace('🛡️ ', '').replace('🤖 ', '')} module"
            ):
                st.session_state.selected_module = option
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def route_to_module(selected_module):
    """Route to the selected module"""
    if selected_module == "🏭 Plant Overview":
        show_plant_overview()
    elif selected_module == "📦 Raw Materials":
        raw_materials.show()
    elif selected_module == "🔥 Production Planning":
        production_planning.show()
    elif selected_module == "📊 Inventory Management":
        inventory_management.show()
    elif selected_module == "✅ Quality Assurance":
        quality_assurance.show()
    elif selected_module == "🚚 Logistics & Shipment":
        logistics_shipment.show()
    elif selected_module == "⚡ Energy Management":
        show_energy_management()
    elif selected_module == "🛡️ Safety & Environment":
        show_safety_environment()
    elif selected_module == "🤖 AI Analytics":
        show_ai_analytics()

def show_plant_overview():
    """Revolutionary plant overview dashboard with modern design"""
    st.markdown("## 🏭 Live Production Command Center")
    
    # Enhanced Key Metrics Grid with modern cards
    st.markdown("### 📊 Real-Time Performance Metrics")
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    with col1:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">🔥 Steel Production Today</div>
                <div class="metric-value">12,847</div>
                <div style="font-size: 0.95rem; color: #667eea; margin: 0.5rem 0;">MT (Target: 13,000)</div>
                <div class="metric-change">▲ 98.8% Target Achievement</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">⚡ Energy Efficiency</div>
                <div class="metric-value">95.4%</div>
                <div style="font-size: 0.95rem; color: #667eea; margin: 0.5rem 0;">Power Optimization</div>
                <div class="metric-change">▲ +3.2% from yesterday</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">✅ Quality Score</div>
                <div class="metric-value">99.2%</div>
                <div style="font-size: 0.95rem; color: #667eea; margin: 0.5rem 0;">Zero Defects</div>
                <div class="metric-change">▲ Above Industry Standard</div>
            </div>
        """, unsafe_allow_html=True)
        
    with col4:
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">🛡️ Safety Record</div>
                <div class="metric-value">852</div>
                <div style="font-size: 0.95rem; color: #667eea; margin: 0.5rem 0;">Accident-Free Days</div>
                <div class="metric-change">▲ Exceptional Safety Record</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Enhanced Production Analytics
    st.markdown("---")
    st.markdown("### 📈 Advanced Production Analytics")
    
    col1, col2 = st.columns(2, gap="large")
    
    with col1:
        # Enhanced hourly production trend
        hours = list(range(24))
        production = [520 + 60*np.sin(h*0.3) + np.random.normal(0, 15) for h in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=hours, 
            y=production, 
            mode='lines+markers',
            name='Hourly Production',
            line=dict(color='#667eea', width=4),
            marker=dict(size=8, color='#764ba2'),
            fill='tonexty',
            fillcolor='rgba(102, 126, 234, 0.2)'
        ))
        fig.update_layout(
            title={
                'text': "📈 24-Hour Production Trend (MT/Hour)",
                'x': 0.5,
                'font': {'size': 18, 'color': '#667eea'}
            },
            xaxis_title="Hour of Day",
            yaxis_title="Production (MT)",
            height=450,
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(gridcolor='rgba(102, 126, 234, 0.2)')
        fig.update_yaxes(gridcolor='rgba(102, 126, 234, 0.2)')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Enhanced production unit efficiency with gradient bars
        units = ['Blast Furnace #8', 'SMS #3', 'Rolling Mill #2', 'Sinter Plant']
        efficiency = [96.5, 94.2, 91.8, 93.7]
        colors = ['#00b894' if e > 95 else '#fdcb6e' if e > 90 else '#e74c3c' for e in efficiency]
        
        fig = go.Figure(data=go.Bar(
            x=units,
            y=efficiency,
            marker=dict(
                color=colors,
                line=dict(color='rgba(255,255,255,0.6)', width=2)
            ),
            text=[f"{e}%" for e in efficiency],
            textposition='auto',
            textfont=dict(size=14, color='white')
        ))
        fig.update_layout(
            title={
                'text': "🏭 Production Unit Efficiency",
                'x': 0.5,
                'font': {'size': 18, 'color': '#667eea'}
            },
            yaxis_title="Efficiency (%)",
            height=450,
            template="plotly_white",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        fig.update_xaxes(gridcolor='rgba(102, 126, 234, 0.2)')
        fig.update_yaxes(gridcolor='rgba(102, 126, 234, 0.2)')
        st.plotly_chart(fig, use_container_width=True)
    
    # Additional insights section
    st.markdown("---")
    st.markdown("### 🔍 Production Insights")
    
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(0, 184, 148, 0.1), rgba(85, 239, 196, 0.1)); 
                    backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 15px; 
                    border: 1px solid rgba(0, 184, 148, 0.2);">
            <h4 style="color: #00b894; margin: 0 0 0.5rem 0;">🎯 Today's Achievement</h4>
            <p style="color: #2d3436; margin: 0; font-size: 0.95rem;">
                Production target exceeded by <strong>2.3%</strong> with exceptional quality metrics.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(253, 203, 110, 0.1), rgba(255, 177, 43, 0.1)); 
                    backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 15px; 
                    border: 1px solid rgba(253, 203, 110, 0.2);">
            <h4 style="color: #fdcb6e; margin: 0 0 0.5rem 0;">⚡ Energy Optimization</h4>
            <p style="color: #2d3436; margin: 0; font-size: 0.95rem;">
                Power consumption reduced by <strong>8.5%</strong> through AI-driven optimization.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1), rgba(118, 75, 162, 0.1)); 
                    backdrop-filter: blur(10px); padding: 1.5rem; border-radius: 15px; 
                    border: 1px solid rgba(102, 126, 234, 0.2);">
            <h4 style="color: #667eea; margin: 0 0 0.5rem 0;">🔬 Quality Excellence</h4>
            <p style="color: #2d3436; margin: 0; font-size: 0.95rem;">
                Zero defects achieved for <strong>15 consecutive days</strong> across all units.
            </p>
        </div>
        """, unsafe_allow_html=True)

def show_energy_management():
    """Energy management module"""
    st.markdown("## ⚡ BSP Energy Management System")
    
    tab1, tab2, tab3 = st.tabs(["🔋 Power Generation", "🏭 Plant Consumption", "💡 Efficiency Analytics"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Generation", "850 MW", "+25 MW")
        with col2:
            st.metric("Self Consumption", "780 MW", "-15 MW")  
        with col3:
            st.metric("Grid Export", "70 MW", "+40 MW")
        
        # Power generation trend
        hours = list(range(24))
        power_gen = [820 + 30*np.sin(h*0.3) + np.random.normal(0, 10) for h in hours]
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=hours, y=power_gen, mode='lines', fill='tonexty', name='Generation'))
        fig.update_layout(title="Power Generation - Last 24 Hours", height=300)
        st.plotly_chart(fig, use_container_width=True)

def show_safety_environment():
    """Safety and environmental module"""
    st.markdown("## 🛡️ Safety & Environmental Compliance")
    
    tab1, tab2 = st.tabs(["🏥 Safety Metrics", "🌍 Environmental Data"])
    
    with tab1:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Safety Score", "9.8/10")
        with col2:
            st.metric("Incident-Free Days", "847")
        with col3:
            st.metric("Training Completion", "98.5%")

def show_ai_analytics():
    """AI analytics module"""
    st.markdown("## 🤖 AI-Powered Analytics")
    
    st.info("🔮 Predictive models analyzing 10,000+ data points every minute")
    
    # Equipment health prediction
    equipment = ['Blast Furnace', 'SMS Converter', 'Rolling Mill', 'Coke Oven']
    health_scores = [95, 87, 76, 92]
    
    fig = go.Figure(data=go.Bar(
        x=equipment,
        y=health_scores,
        marker_color=['green' if s > 90 else 'orange' if s > 75 else 'red' for s in health_scores]
    ))
    fig.update_layout(title="🔧 Equipment Health Prediction", height=300)
    st.plotly_chart(fig, use_container_width=True)

def show_emergency_alert():
    """Show emergency alert"""
    st.error("🚨 Emergency Alert System Activated")
    st.warning("⚠️ All department heads have been notified")

if __name__ == "__main__":
    main()
