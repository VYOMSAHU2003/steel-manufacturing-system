"""
Initialize the database and create all tables
Run this script once to set up the database schema
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.database import engine, Base
from models.database_models import User, RawMaterial, ProductionOrder, InventoryLog, QualityInspection, Shipment
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
        
        # Create default users
        users = [
            User(
                username="admin",
                email="admin@steel.com",
                password_hash=bcrypt.hashpw(b"admin123", bcrypt.gensalt()).decode(),
                full_name="Admin User",
                role="admin"
            ),
            User(
                username="manager",
                email="manager@steel.com",
                password_hash=bcrypt.hashpw(b"manager123", bcrypt.gensalt()).decode(),
                full_name="Plant Manager",
                role="manager"
            ),
            User(
                username="operator",
                email="operator@steel.com",
                password_hash=bcrypt.hashpw(b"operator123", bcrypt.gensalt()).decode(),
                full_name="Production Operator",
                role="operator"
            ),
            User(
                username="quality",
                email="quality@steel.com",
                password_hash=bcrypt.hashpw(b"quality123", bcrypt.gensalt()).decode(),
                full_name="Quality Inspector",
                role="quality"
            ),
            User(
                username="logistics",
                email="logistics@steel.com",
                password_hash=bcrypt.hashpw(b"logistics123", bcrypt.gensalt()).decode(),
                full_name="Logistics Manager",
                role="logistics"
            )
        ]
        
        for user in users:
            db.add(user)
        
        db.commit()
        print("✓ Initial users created")
        print("\nDefault credentials:")
        print("  Username: admin     | Password: admin123")
        print("  Username: manager   | Password: manager123")
        print("  Username: operator  | Password: operator123")
        print("  Username: quality   | Password: quality123")
        print("  Username: logistics | Password: logistics123")
        
    except Exception as e:
        db.rollback()
        print(f"Error seeding data: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_tables()
    seed_initial_data()
    print("\n✓ Database initialization complete!")
