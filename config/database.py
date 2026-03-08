import os
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Check if we should use SQLite (for deployment)
USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

# For development/testing with SQLite (fallback)
FALLBACK_DATABASE_URL = "sqlite:///./manufacturing.db"

import os
from sqlalchemy import create_engine, pool
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

# Check if we should use SQLite (for deployment)
USE_SQLITE = os.getenv("USE_SQLITE", "false").lower() == "true"

# For development/testing with SQLite (fallback)
FALLBACK_DATABASE_URL = "sqlite:///./manufacturing.db"

if USE_SQLITE:
    # Force SQLite for cloud deployment
    print("Using SQLite database for deployment")
    engine = create_engine(FALLBACK_DATABASE_URL, connect_args={"check_same_thread": False})
else:
    # Try Oracle connection for local development
    ORACLE_HOST = os.getenv("ORACLE_HOST", "localhost")
    ORACLE_PORT = os.getenv("ORACLE_PORT", "1521")
    ORACLE_SERVICE_NAME = os.getenv("ORACLE_SERVICE_NAME", "ORCL")
    ORACLE_USER = os.getenv("ORACLE_USER", "system")
    ORACLE_PASSWORD = os.getenv("ORACLE_PASSWORD", "")

    # Connection URL for cx_Oracle
    DATABASE_URL = f"oracle://{ORACLE_USER}:{ORACLE_PASSWORD}@{ORACLE_HOST}:{ORACLE_PORT}/{ORACLE_SERVICE_NAME}"

    try:
        # Try Oracle connection
        engine = create_engine(
            DATABASE_URL,
            poolclass=pool.QueuePool,
            max_overflow=10,
            pool_size=5,
            pool_pre_ping=True,
            echo=False
        )
        # Test connection
        with engine.connect() as conn:
            conn.execute("SELECT 1 FROM dual")
        print("Connected to Oracle database successfully")
    except Exception as e:
        print(f"Oracle connection failed: {e}")
        print("Falling back to SQLite for development")
        engine = create_engine(FALLBACK_DATABASE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
