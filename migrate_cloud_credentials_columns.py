import os
import sys
import logging
from sqlalchemy import text

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Ensure import path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.db import engine


def column_exists(connection, table: str, column: str) -> bool:
    result = connection.execute(text(
        """
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name = :table AND column_name = :column
        """
    ), {"table": table, "column": column})
    return result.fetchone() is not None


def migrate_cloud_credentials():
    """Add missing columns to cloud_credentials to match ORM model."""
    with engine.connect() as connection:
        trans = connection.begin()
        try:
            # name (non-nullable); default to provider + ' credential' if needed
            if not column_exists(connection, 'cloud_credentials', 'name'):
                logger.info("Adding name column to cloud_credentials...")
                connection.execute(text("""
                    ALTER TABLE cloud_credentials
                    ADD COLUMN name VARCHAR NOT NULL DEFAULT 'Default Credential'
                """))
                logger.info("name column added")

            # created_at
            if not column_exists(connection, 'cloud_credentials', 'created_at'):
                logger.info("Adding created_at column to cloud_credentials...")
                connection.execute(text("""
                    ALTER TABLE cloud_credentials
                    ADD COLUMN created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                """))
                logger.info("created_at column added")

            # updated_at
            if not column_exists(connection, 'cloud_credentials', 'updated_at'):
                logger.info("Adding updated_at column to cloud_credentials...")
                connection.execute(text("""
                    ALTER TABLE cloud_credentials
                    ADD COLUMN updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
                """))
                logger.info("updated_at column added")

            trans.commit()
            logger.info("Migration completed successfully")
        except Exception as e:
            trans.rollback()
            logger.error(f"Migration failed: {e}")
            raise


if __name__ == '__main__':
    migrate_cloud_credentials()
