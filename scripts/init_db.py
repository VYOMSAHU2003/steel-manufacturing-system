"""
Initialize the database and create all tables
Run this script once to set up the database schema
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base
from models.database_models import (
    User, RawMaterial, ProductionOrder, InventoryLog, QualityInspection, Shipment,
    FinishedProduct, DefectTracking, DispatchRecord, CustomerOrder, ProductionPrediction,
    MaterialConsumption, LowStockAlert, MaterialReorderSuggestion,  # New tracking models
    UserRole
)
import bcrypt
from config.database import SessionLocal

def create_tables():
    """Create all tables in the database"""
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("✓ Tables created successfully")

def seed_initial_data():
    """Seed the database with initial users and sample data"""
    db = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).count()
        if existing_users > 0:
            print("✓ Database already has users, skipping seed")
            return
        
        print("Seeding initial data...")
        
        # Create default users with enhanced roles
        users = [
            User(
                username="admin",
                email="admin@steel.com",
                password_hash=bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode(),
                full_name="System Administrator",
                role=UserRole.ADMIN
            ),
            User(
                username="store_manager",
                email="store@steel.com",
                password_hash=bcrypt.hashpw(b"store123", bcrypt.gensalt()).decode(),
                full_name="Store Manager",
                role=UserRole.STORE_MANAGER
            ),
            User(
                username="production_manager",
                email="production@steel.com",
                password_hash=bcrypt.hashpw(b"prod123", bcrypt.gensalt()).decode(),
                full_name="Production Manager",
                role=UserRole.PRODUCTION_MANAGER
            ),
            User(
                username="quality_manager",
                email="quality@steel.com",
                password_hash=bcrypt.hashpw(b"quality123", bcrypt.gensalt()).decode(),
                full_name="Quality Manager",
                role=UserRole.QUALITY_MANAGER
            ),
            User(
                username="dispatch_manager",
                email="dispatch@steel.com",
                password_hash=bcrypt.hashpw(b"dispatch123", bcrypt.gensalt()).decode(),
                full_name="Dispatch Manager", 
                role=UserRole.DISPATCH_MANAGER
            ),
            User(
                username="operator",
                email="operator@steel.com",
                password_hash=bcrypt.hashpw(b"operator123", bcrypt.gensalt()).decode(),
                full_name="Production Operator",
                role=UserRole.OPERATOR
            ),
            User(
                username="viewer",
                email="viewer@steel.com",
                password_hash=bcrypt.hashpw(b"viewer123", bcrypt.gensalt()).decode(),
                full_name="Read-only Viewer",
                role=UserRole.VIEWER
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print("✓ Enhanced user roles created")
        print("\n🔐 Default Credentials:")
        print("  Admin:              admin           | Password: admin123")
        print("  Store Manager:      store_manager   | Password: store123")
        print("  Production Manager: production_manager | Password: prod123")
        print("  Quality Manager:    quality_manager | Password: quality123")
        print("  Dispatch Manager:   dispatch_manager| Password: dispatch123")
        print("  Operator:           operator        | Password: operator123")
        print("  Viewer:             viewer          | Password: viewer123")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_initial_data()
    print("\n✓ Database initialization complete!")
