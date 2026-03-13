import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
import time
import random
from datetime import datetime, timedelta
from pages import (
    authentication,
    raw_materials,
    production_planning,
    inventory_management,
    quality_assurance,
    logistics_shipment
)
from utils.material_tracking import display_alert_notifications

# Try to import live simulation, with fallbacks if it fails
try:
    from utils.live_simulation import get_live_metrics, start_background_simulation, initialize_live_simulation
except ImportError:
    # Create fallback functions if live_simulation module is not available
    def get_live_metrics():
        import random
        return {
            "production_rate": 95.5 + random.uniform(-2, 2),
            "furnace_temp": 1665 + random.randint(-10, 10),
            "power_status": "STABLE",
            "total_updates": random.randint(50, 200),
            "last_update": None
        }
    
    def start_background_simulation():
        pass
    
    def initialize_live_simulation():
        pass

def main():
    st.set_page_config(
        page_title="BSP Digital Manufacturing System",
        page_icon="🏭",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize live simulation on app start
    if 'simulation_started' not in st.session_state:
        st.session_state.simulation_started = True
        start_background_simulation()
    
    # Auto-refresh every 60 seconds (Demo Mode)
    if 'auto_refresh' not in st.session_state:
        st.session_state.auto_refresh = True
    
    # Add refresh controls in sidebar
    with st.sidebar:
        st.markdown("### 🔄 **LIVE DEMO MODE**")
        
        # Live status indicators
        live_metrics = get_live_metrics()
        
        col1, col2 = st.columns(2)
        with col1:
            # Create a unique key using session ID and current frame counter
            import hashlib
            import uuid
            
            if 'session_id' not in st.session_state:
                st.session_state.session_id = str(uuid.uuid4())[:8]
            
            if 'button_counter' not in st.session_state:
                st.session_state.button_counter = 0
            
            refresh_key = f"refresh_{st.session_state.session_id}_{st.session_state.button_counter}"
            
            if st.button("🔄 Manual Refresh", key=refresh_key, help="Refresh data now"):
                st.session_state.button_counter += 1
                st.rerun()
        
        with col2:
            auto_refresh = st.toggle("⚡ Auto Refresh", value=st.session_state.auto_refresh, 
                                   help="Auto refresh every 60 seconds")
            st.session_state.auto_refresh = auto_refresh
        
        # Live metrics display
        st.markdown("#### 📊 **Live Plant Status**")
        
        production_rate = live_metrics.get("production_rate", 95.5)
        furnace_temp = live_metrics.get("furnace_temp", 1665)
        power_status = live_metrics.get("power_status", "STABLE")
        total_updates = live_metrics.get("total_updates", 0)
        last_update = live_metrics.get("last_update")
        
        # Production rate indicator
        prod_color = "🟢" if production_rate > 95 else "🟡" if production_rate > 90 else "🔴"
        st.write(f"{prod_color} **Production**: {production_rate:.1f}%")
        
        # Furnace temperature
        temp_color = "🟢" if 1650 <= furnace_temp <= 1680 else "🟡" if 1620 <= furnace_temp <= 1700 else "🔴"
        st.write(f"{temp_color} **Furnace**: {furnace_temp}°C")
        
        # Power status
        power_color = "🟢" if power_status == "STABLE" else "🟡"
        st.write(f"{power_color} **Power**: {power_status}")
        
        # Update counter
        st.write(f"🔄 **Updates**: {total_updates}")
        
        if last_update:
            try:
                from datetime import datetime
                if isinstance(last_update, str):
                    update_time = datetime.fromisoformat(last_update.replace('Z', '+00:00'))
                else:
                    update_time = last_update
                st.write(f"⏰ **Last**: {update_time.strftime('%H:%M:%S')}")
            except:
                st.write(f"⏰ **Last**: Just now")
        
        st.markdown("---")
    
    # Auto-refresh logic
    if st.session_state.auto_refresh:
        # Create a placeholder for countdown
        countdown_placeholder = st.empty()
        
        # Auto-refresh every 60 seconds
        refresh_interval = 60  # seconds
        
        # Check if we need to refresh (simple time-based check)
        current_time = time.time()
        if 'last_refresh_time' not in st.session_state:
            st.session_state.last_refresh_time = current_time
        
        time_since_refresh = current_time - st.session_state.last_refresh_time
        
        if time_since_refresh >= refresh_interval:
            st.session_state.last_refresh_time = current_time
            st.rerun()
        
        # Show countdown in main area
        time_remaining = refresh_interval - int(time_since_refresh)
        if time_remaining > 0:
            countdown_placeholder.info(
                f"🔄 **LIVE DEMO MODE**: Next auto-refresh in {time_remaining} seconds | "
                f"✨ Data updating automatically every minute | "
                f"🏭 Real-time steel plant simulation active"
            )
        
        # Use JavaScript to refresh page (as fallback)
        if time_remaining <= 1:
            st.rerun()
    
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
        # Create unique logout button key
        if 'logout_session_id' not in st.session_state:
            import uuid
            st.session_state.logout_session_id = str(uuid.uuid4())[:8]
            
        logout_key = f"logout_{st.session_state.logout_session_id}"
        
        if st.button("🚪 Logout", key=logout_key, type="secondary", width="stretch"):
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
        
        # Create unique emergency button keys
        if 'emergency_session_id' not in st.session_state:
            import uuid
            st.session_state.emergency_session_id = str(uuid.uuid4())[:8]
        
        emergency_key = f"emergency_{st.session_state.emergency_session_id}"
        alert_key = f"alert_{st.session_state.emergency_session_id}"
        
        if st.button("🛑 Emergency Stop", key=emergency_key, type="secondary", width="stretch"):
            st.error("🚨 Emergency stop initiated! All operations halted.")
            
        if st.button("🚨 Alert Management", key=alert_key, type="secondary", width="stretch"):
            st.warning("📢 Alert system activated - Management notified")
            
        # Enhanced Admin Controls
        if st.session_state.role in ['admin', 'manager']:
            st.markdown("---")
            st.markdown("### ⚡ Admin Control Panel")
            
            # Create unique admin button keys
            if 'admin_session_id' not in st.session_state:
                import uuid
                st.session_state.admin_session_id = str(uuid.uuid4())[:8]
            
            diag_key = f"diag_{st.session_state.admin_session_id}"
            maint_key = f"maint_{st.session_state.admin_session_id}"
            
            if st.button("📊 System Diagnostics", key=diag_key, width="stretch"):
                st.success("🔧 Running comprehensive system diagnostics...")
                
            if st.button("🔧 Maintenance Mode", key=maint_key, width="stretch"):
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
            # Create unique button key with session ID
            if 'nav_session_id' not in st.session_state:
                import uuid
                st.session_state.nav_session_id = str(uuid.uuid4())[:8]
            
            button_key = f"nav_{st.session_state.nav_session_id}_{option.replace(' ', '_').replace('&', 'and')}"
            
            # Enhanced button styling based on selection state
            is_selected = st.session_state.selected_module == option
            button_type = "primary" if is_selected else "secondary"
            
            # Create custom styled button
            if st.button(
                option, 
                key=button_key, 
                width="stretch",
                type=button_type,
                help=f"Navigate to {option.replace('🏭 ', '').replace('📦 ', '').replace('🔥 ', '').replace('📊 ', '').replace('✅ ', '').replace('🚚 ', '').replace('⚡ ', '').replace('🛡️ ', '').replace('🤖 ', '')} module"
            ):
                st.session_state.selected_module = option
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

def route_to_module(selected_module):
    """Route to the selected module"""
    
    # Display low stock alerts on every page in sidebar
    try:
        display_alert_notifications()
    except Exception as e:
        # Silently handle any alert display errors
        pass
    
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
    """Revolutionary plant overview dashboard with LIVE DATA"""
    
    # Live Demo Header
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #ff6b6b 0%, #4ecdc4 50%, #45b7d1 100%); 
                padding: 1rem; border-radius: 15px; margin-bottom: 1rem; text-align: center;">
        <h3 style="color: white; margin: 0;">
            🔴 LIVE DEMO MODE | 🔄 Auto-Updating Every 60 Seconds | 
            ⏰ {datetime.now().strftime('%H:%M:%S')}
        </h3>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("## 🏭 Live Production Command Center")
    
    # Get live metrics
    live_metrics = get_live_metrics()
    
    # Enhanced Key Metrics Grid with LIVE DATA
    st.markdown("### 📊 Real-Time Performance Metrics")
    col1, col2, col3, col4 = st.columns(4, gap="medium")
    
    # Live production data
    production_rate = live_metrics.get("production_rate", 95.5)
    furnace_temp = live_metrics.get("furnace_temp", 1665) 
    total_updates = live_metrics.get("total_updates", 0)
    
    # Calculate dynamic values based on live data
    daily_production = int(12847 + (production_rate - 95) * 200)
    target_achievement = (daily_production / 13000) * 100
    
    with col1:
        delta_color = "normal" if target_achievement >= 98 else "inverse"
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">🔥 Steel Production Today</div>
                <div class="metric-value">""" + f"{daily_production:,}" + """</div>
                <div style="font-size: 0.95rem; color: #667eea; margin: 0.5rem 0;">MT (Target: 13,000)</div>
                <div class="metric-change">""" + f"▲ {target_achievement:.1f}% Target Achievement" + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        efficiency = min(99.5, production_rate + random.uniform(0, 3))
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">⚡ Plant Efficiency</div>
                <div class="metric-value">""" + f"{efficiency:.1f}%" + """</div>
                <div style="font-size: 0.95rem; color: #00b894; margin: 0.5rem 0;">Running Optimally</div>
                <div class="metric-change">""" + f"📈 Live: {production_rate:.1f}% Production Rate" + """</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        quality_rate = max(95, min(99.8, 98.2 + random.uniform(-1, 1)))
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">✅ Quality Rate</div>
                <div class="metric-value">""" + f"{quality_rate:.1f}%" + """</div>
                <div style="font-size: 0.95rem; color: #fd7956; margin: 0.5rem 0;">BSP Standard</div>
                <div class="metric-change">🎯 Target: >98.0%</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col4:
        furnace_status = "🟢 OPTIMAL" if 1650 <= furnace_temp <= 1680 else "🟡 WATCH" if 1620 <= furnace_temp <= 1700 else "🔴 ALERT"
        st.markdown("""
            <div class="metric-card">
                <div class="metric-title">🌡️ Furnace Status</div>
                <div class="metric-value">""" + f"{furnace_temp}°C" + """</div>
                <div style="font-size: 0.95rem; color: #fdcb6e; margin: 0.5rem 0;">""" + furnace_status + """</div>
                <div class="metric-change">🔥 Live Temperature</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Live Data Simulation Status
    st.markdown("### 🔄 Live Simulation Status")
    
    sim_col1, sim_col2, sim_col3, sim_col4 = st.columns(4)
    
    with sim_col1:
        st.metric("🔄 Total Updates", f"{total_updates}", delta="Live simulation active")
    
    with sim_col2:
        power_status = live_metrics.get("power_status", "STABLE")
        power_color = "normal" if power_status == "STABLE" else "inverse"
        st.metric("⚡ Power Grid", power_status, delta="Real-time monitoring", delta_color=power_color)
    
    with sim_col3:
        # Simulate material alerts count
        from utils.material_tracking import get_low_stock_alerts
        try:
            alerts = get_low_stock_alerts()
            alert_count = len(alerts) if alerts else 0
        except:
            alert_count = random.randint(3, 8)
        
        alert_color = "inverse" if alert_count > 5 else "normal"
        st.metric("🚨 Active Alerts", f"{alert_count}", delta="Stock notifications", delta_color=alert_color)
    
    with sim_col4:
        # Live consumption rate
        consumption_rate = random.uniform(85, 120)
        st.metric("📉 Material Usage", f"{consumption_rate:.1f}t/hr", delta="Live tracking")
    
    # Live Production Charts
    st.markdown("### 📈 Live Production Trends")
    
    chart_col1, chart_col2 = st.columns(2)
    
    with chart_col1:
        # Generate live production data
        hours = [(datetime.now() - timedelta(hours=i)).hour for i in range(24, 0, -1)]
        production_values = []
        
        for i, hour in enumerate(hours):
            base_production = 550  # Base hourly production
            variation = random.uniform(-50, 100)
            # Make current hour reflect live production rate
            if i == len(hours) - 1:  # Current hour
                variation += (production_rate - 95) * 10
            production_values.append(max(400, base_production + variation))
        
        df_production = pd.DataFrame({
            "Hour": [f"{h:02d}:00" for h in hours],
            "Production (MT)": production_values
        })
        
        fig_production = px.line(df_production, x="Hour", y="Production (MT)",
                               title="🔥 24-Hour Production Trend (LIVE)",
                               markers=True)
        fig_production.add_hline(y=550, line_dash="dash", line_color="green", 
                               annotation_text="Target: 550 MT/hr")
        fig_production.update_traces(line_color="#ff6b6b", line_width=3)
        st.plotly_chart(fig_production, width="stretch")
    
    with chart_col2:
        # Live material consumption
        materials = ["Iron Ore", "Coal", "Limestone", "Scrap Steel", "Flux"]
        current_consumption = [random.uniform(50, 150) for _ in materials]
        
        df_consumption = pd.DataFrame({
            "Material": materials,
            "Consumption (t/hr)": current_consumption
        })
        
        fig_consumption = px.bar(df_consumption, x="Material", y="Consumption (t/hr)",
                               title="📉 Live Material Consumption",
                               color="Consumption (t/hr)", color_continuous_scale="viridis")
        st.plotly_chart(fig_consumption, width="stretch")
    
    # Real-time alerts section
    st.markdown("### 🚨 Real-Time System Alerts")
    
    alert_col1, alert_col2 = st.columns(2)
    
    with alert_col1:
        # Live material alerts
        try:
            from utils.material_tracking import get_low_stock_alerts
            alerts = get_low_stock_alerts()
            
            if alerts:
                st.markdown("#### 📦 **Material Alerts**")
                for alert in alerts[:3]:  # Show top 3
                    alert_type = "🔴" if alert.alert_type == "critical" else "🟡"
                    st.warning(f"{alert_type} {alert.alert_message}")
            else:
                st.success("✅ All material stocks are adequate")
        except Exception as e:
            st.info("🔄 Material alerts loading...")
    
    with alert_col2:
        # Live quality alerts  
        st.markdown("#### ⚠️ **Quality Status**")
        
        quality_alerts = []
        
        # Generate dynamic quality alerts based on live data
        if quality_rate < 98:
            quality_alerts.append(f"🟡 Quality rate below target: {quality_rate:.1f}%")
        
        if furnace_temp > 1690:
            quality_alerts.append(f"🔴 Furnace temperature high: {furnace_temp}°C")
        elif furnace_temp < 1640:
            quality_alerts.append(f"🟡 Furnace temperature low: {furnace_temp}°C")
        
        if production_rate < 90:
            quality_alerts.append(f"🔴 Production efficiency low: {production_rate:.1f}%")
        
        if quality_alerts:
            for alert in quality_alerts:
                if "🔴" in alert:
                    st.error(alert)
                else:
                    st.warning(alert)
        else:
            st.success("✅ All quality parameters normal")
    
    # Live update timestamp
    st.markdown("---")
    st.info(f"🔄 **Live Data** | Last Update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} | Updates automatically every 60 seconds | Total Simulation Updates: {total_updates}")
    
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
        st.plotly_chart(fig, width="stretch")
    
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
        st.plotly_chart(fig, width="stretch")
    
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
    st.markdown("## ⚡ Energy Management")
    st.info("🔧 Energy management module - Advanced power optimization features coming soon!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Power Consumption", "245 MW", delta="-5 MW")
        st.metric("Energy Efficiency", "94.2%", delta="+1.2%")
    
    with col2:
        st.metric("Cost Savings", "₹2.3 Cr", delta="+15%")
        st.metric("Carbon Footprint", "1,247 tons CO2", delta="-8%")

def show_safety_environment():
    """Safety and environment module"""
    st.markdown("## 🛡️ Safety & Environment")
    st.info("🔧 Safety & Environment module - Comprehensive monitoring features coming soon!")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Safety Score", "99.8%", delta="▲ Excellent")
        st.metric("Incident-Free Days", "851", delta="+1")
    
    with col2:
        st.metric("Air Quality Index", "Good", delta="Normal")
        st.metric("Water Treatment", "98.5%", delta="+0.3%")
    
    with col3:
        st.metric("Waste Reduction", "87%", delta="+5%")
        st.metric("Compliance Score", "100%", delta="Perfect")

def show_ai_analytics():
    """AI Analytics module"""
    st.markdown("## 🤖 AI Analytics")
    st.info("🔧 AI Analytics module - Machine learning insights coming soon!")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Predictive Accuracy", "96.7%", delta="▲ High")
        st.metric("Cost Optimization", "₹15.2 Cr", delta="+22%")
    
    with col2:
        st.metric("Anomaly Detection", "Active", delta="98.9% accuracy")
        st.metric("Forecast Reliability", "94.1%", delta="+2.3%")

if __name__ == "__main__":
    main()
