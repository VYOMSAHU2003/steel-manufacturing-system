"""
Test authentication functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.auth import authenticate_user
from config.database import SessionLocal
from models.database_models import User

def test_authentication():
    """Test the authentication system"""
    print("🔍 Testing Authentication System...")
    print("=" * 50)
    
    # Test database connection
    db = SessionLocal()
    try:
        users = db.query(User).all()
        print(f"✅ Database connected: {len(users)} users found")
        
        for user in users:
            print(f"   - {user.username} ({user.role.value})")
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False
    finally:
        db.close()
    
    # Test authentication function
    test_credentials = [
        ("admin", "admin123"),
        ("manager", "manager123"),
        ("invalid", "wrong"),
        ("", ""),
        ("admin", "wrong_password")
    ]
    
    print("\n🔐 Testing Authentication...")
    for username, password in test_credentials:
        try:
            result = authenticate_user(username, password)
            if result:
                print(f"   ✅ {username}: Login successful → {result['full_name']} ({result['role']})")
            else:
                print(f"   ❌ {username}: Login failed")
        except Exception as e:
            print(f"   🚨 {username}: Error → {e}")
    
    print("\n✨ Authentication test completed!")
    
if __name__ == "__main__":
    test_authentication()