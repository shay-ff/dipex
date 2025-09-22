from backend.db.session import create_tables, engine
from backend.core.config import settings
import sys

def init_database():
    """Initialize the database by creating all tables"""
    try:
        print(f"Connecting to database: {settings.database_name}")
        print(f"Host: {settings.database_host}:{settings.database_port}")
        
        # Test connection
        with engine.connect() as conn:
            print("✅ Database connection successful!")
        
        # Create tables
        create_tables()
        print("✅ Database tables created successfully!")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    init_database()
