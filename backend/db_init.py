from backend.db.session import create_tables, engine
from backend.core.config import settings
import sys
import logging

logger = logging.getLogger("db_init")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


def init_database():
    """Initialize the database by creating all tables"""
    try:
        logger.info("Connecting to database: %s", settings.database_name)
        logger.info("Host: %s:%s", settings.database_host, settings.database_port)
        
        # Test connection
        with engine.connect() as conn:
            logger.info("✅ Database connection successful!")
        
        # Create tables
        create_tables()
        logger.info("✅ Database tables created successfully!")
        
    except Exception as e:
        logger.exception("❌ Error initializing database")
        sys.exit(1)


if __name__ == "__main__":
    init_database()
