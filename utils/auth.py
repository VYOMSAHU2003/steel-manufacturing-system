import bcrypt
import streamlit as st
from config.database import SessionLocal
from models.database_models import User

def hash_password(password: str) -> str:
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

def verify_password(password: str, hash: str) -> bool:
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode(), hash.encode())

def authenticate_user(username: str, password: str) -> dict:
    """Authenticate user and return user info if successful"""
    db = SessionLocal()
    try:
        # Validate input
        if not username or not password:
            return None
            
        # Query user from database
        user = db.query(User).filter(User.username == username).first()
        
        if user and user.is_active and verify_password(password, user.password_hash):
            return {
                "user_id": user.user_id,
                "username": user.username,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role.value
            }
        return None
    except Exception as e:
        # Log error but don't expose internal details to user
        print(f"Authentication error: {e}")
        return None
    finally:
        db.close()

def require_role(required_roles):
    """Decorator to require specific roles"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            user_role = st.session_state.get("role")
            if user_role not in required_roles:
                st.error(f"You do not have permission to access this page. Required role: {', '.join(required_roles)}")
                return
            return func(*args, **kwargs)
        return wrapper
    return decorator
