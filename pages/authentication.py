import streamlit as st
from utils.auth import authenticate_user, hash_password

def show_login_page():
    """Display the modern BSP-enhanced login page"""
    # Revolutionary CSS for BSP-themed login with modern design
    st.markdown("""
    <style>
    /* Modern Login Styling */
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);
        padding: 2.5rem 1.5rem;
        border-radius: 25px;
        margin-bottom: 2rem;
        box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3);
        position: relative;
        overflow: hidden;
        animation: headerGlow 3s ease-in-out infinite alternate;
    }
    
    @keyframes headerGlow {
        0% { box-shadow: 0 20px 40px rgba(102, 126, 234, 0.3); }
        100% { box-shadow: 0 25px 50px rgba(102, 126, 234, 0.5); }
    }
    
    .main-header::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
        animation: shine 3s infinite;
    }
    
    @keyframes shine {
        0% { left: -100%; }
        100% { left: 100%; }
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
        font-weight: 800;
        text-shadow: 2px 2px 8px rgba(0,0,0,0.3);
        background: linear-gradient(45deg, #ffffff, #ffeaa7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .main-header p {
        color: white;
        font-size: 1.3rem;
        margin: 0;
        opacity: 0.95;
        font-weight: 500;
    }
    
    .login-container {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(15px);
        padding: 3rem;
        border-radius: 25px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        max-width: 500px;
        margin: 0 auto;
    }
    
    .plant-info {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.2), rgba(118, 75, 162, 0.2));
        backdrop-filter: blur(10px);
        color: #667eea;
        padding: 1.5rem;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 2rem;
        border: 1px solid rgba(102, 126, 234, 0.3);
    }
    
    .credentials-card {
        background: linear-gradient(135deg, rgba(255,255,255,0.8), rgba(255,255,255,0.6));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 20px;
        padding: 1.5rem;
        margin-top: 1.5rem;
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
    }
    
    .role-badge {
        display: inline-block;
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        margin: 0.2rem 0.3rem;
        box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
    }
    
    /* Enhanced Input Styling */
    .stTextInput > div > div > input {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
        padding: 0.8rem 1rem;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
    }
    
    .stSelectbox > div > div > div {
        background: linear-gradient(135deg, rgba(255,255,255,0.9), rgba(255,255,255,0.7));
        backdrop-filter: blur(10px);
        border: 2px solid rgba(102, 126, 234, 0.3);
        border-radius: 15px;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown("""
    <div class="main-header">
        <h1>🏭 BHILAI STEEL PLANT</h1>
        <p>Integrated Production Management System</p>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Plant information
        st.markdown("""
        <div class="plant-info">
            <h3>🏭 Plant Operations Center</h3>
            <p>Real-time monitoring and control system for steel production operations</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Login form
        username = st.text_input("👤 Employee ID / Username", placeholder="Enter your employee ID")
        password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
        
        # Role selection helper
        st.markdown("**🏭 Select Your Department:**")
        role_cols = st.columns(3)
        with role_cols[0]:
            st.markdown('<span class="role-badge">👨‍💼 Management</span>', unsafe_allow_html=True)
        with role_cols[1]:
            st.markdown('<span class="role-badge">⚙️ Production</span>', unsafe_allow_html=True)
        with role_cols[2]:
            st.markdown('<span class="role-badge">🔬 Quality</span>', unsafe_allow_html=True)
        
        st.write("")
        
        # Login button
        if st.button("🔓 Login to Plant System", type="primary", key="login_btn", width='stretch'):
            if not username or not password:
                st.error("⚠️ Please enter both Employee ID and password")
            elif not username.strip() or not password.strip():
                st.error("⚠️ Employee ID and password cannot be empty")
            else:
                with st.spinner("🔄 Authenticating with BSP Systems..."):
                    try:
                        user_data = authenticate_user(username, password)
                        if user_data:
                            # Set all required session state variables
                            st.session_state.user = user_data["full_name"]
                            st.session_state.username = user_data["username"]
                            st.session_state.user_id = user_data["user_id"]
                            st.session_state.role = user_data["role"]
                            st.session_state.email = user_data["email"]
                            
                            # Set additional BSP-specific session variables
                            st.session_state.plant_section = 'Main Plant'
                            st.session_state.shift = 'Day Shift'
                            st.session_state.authenticated = True
                            
                            st.success(f"✅ Welcome to BSP Plant System, {user_data['full_name']}!")
                            
                            # Force a rerun to refresh the app immediately
                            st.rerun()
                        else:
                            st.error("❌ Invalid credentials. Please verify your Employee ID and password.")
                    except Exception as e:
                        st.error(f"❌ System error during authentication: {str(e)}")
        
        # Plant shift information
        st.markdown("""
        <div style="background: #f0f8ff; padding: 15px; border-radius: 8px; margin: 20px 0;">
            <h4 style="color: #2E4A62; margin: 0;">🕒 Current Shift Information</h4>
            <p style="margin: 5px 0 0 0; color: #666;">Shift A: 06:00 - 14:00 | Shift B: 14:00 - 22:00 | Shift C: 22:00 - 06:00</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Demo credentials section
        with st.expander("📋 Demo Access Credentials", expanded=False):
            st.markdown('<div class="credentials-card">', unsafe_allow_html=True)
            st.markdown("### 🏭 BSP System Demo Accounts")
            
            cred_cols = st.columns(2)
            
            with cred_cols[0]:
                st.markdown("""
                **🔧 Plant Administrator**
                - ID: `admin`
                - Password: `admin123`
                - Access: Full system control
                
                **👨‍💼 Production Manager** 
                - ID: `manager`
                - Password: `manager123`
                - Access: Production oversight
                
                **⚙️ Plant Operator**
                - ID: `operator` 
                - Password: `operator123`
                - Access: Equipment operation
                """)
            
            with cred_cols[1]:
                st.markdown("""
                **🔬 Quality Controller**
                - ID: `quality`
                - Password: `quality123`
                - Access: Quality systems
                
                **🚛 Logistics Coordinator**
                - ID: `logistics`
                - Password: `logistics123`  
                - Access: Material flow
                
                **📊 Shift Supervisor**
                - ID: `supervisor`
                - Password: `super123`
                - Access: Shift management
                """)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Security notice
        st.markdown("""
        <div style="text-align: center; color: #666; font-size: 0.9rem; margin-top: 30px;">
            🔒 This system is for authorized BSP personnel only. All activities are logged and monitored.
        </div>
        """, unsafe_allow_html=True)


def show():
    """Display authentication page - wrapper function for app.py"""
    show_login_page()
