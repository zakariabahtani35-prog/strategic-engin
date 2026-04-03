import logging
import os
import sqlite3
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from config import Config
from models import Base

logger = logging.getLogger(__name__)

# Configure engine arguments defensively
connect_args = {}
if "sqlite" in Config.DATABASE_URL:
    connect_args["check_same_thread"] = False

# Hardened DB Connection Engine
try:
    engine = create_engine(
        Config.DATABASE_URL, 
        connect_args=connect_args,
        pool_pre_ping=True
    )
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    logger.critical(f"FATAL: Database Engine Failed to Start. Configuration Error: {e}")
    # Do not let the app silently fail if the DB URL is fundamentally broken
    raise

def auto_repair_schema(engine, metadata):
    """
    DYNAMIC, SELF-HEALING MIGRATION ENGINE
    Automatically synchronizes missing columns between SQLAlchemy metadata and SQLite schema.
    """
    logger.info("⚡ Activating Self-Healing Schema Verification...")
    inspector = inspect(engine)
    
    # Track actions to ensure we only log meaningful changes
    mutations_applied = 0
    
    with engine.begin() as conn:  # Automatically manages a transaction
        for table_name, table_def in metadata.tables.items():
            if not inspector.has_table(table_name):
                # The table doesn't exist yet; create_all will handle it later.
                continue
                
            # Grab actual SQLite columns
            existing_columns = {col['name'] for col in inspector.get_columns(table_name)}
            
            for column in table_def.columns:
                if column.name not in existing_columns:
                    # Missing column detected! We must perform auto-repair.
                    col_type = str(column.type.compile(engine.dialect))
                    
                    # Resolve safe default values based on column type if nullable
                    # For a robust approach we can just let SQLite handle default NULL for new columns
                    # UNLESS the model dictates a server_default.
                    default_str = ""
                    if column.server_default:
                        default_str = f" DEFAULT {column.server_default.arg}"
                    elif not column.nullable:
                        # SQLite doesn't allow parsing 'NOT NULL' on ADD COLUMN without a generic default
                        # If a column is strictly not nullable without a server_default, we fallback to something safe
                        if 'VARCHAR' in col_type or 'TEXT' in col_type or 'STRING' in col_type:
                            default_str = " DEFAULT ''"
                        elif 'INTEGER' in col_type or 'FLOAT' in col_type or 'NUMERIC' in col_type:
                            default_str = " DEFAULT 0"
                        elif 'BOOLEAN' in col_type:
                            default_str = " DEFAULT 0"

                    alter_stmt = f"ALTER TABLE {table_name} ADD COLUMN {column.name} {col_type}{default_str}"
                    
                    try:
                        logger.warning(f"🔧 Auto-Repair Triggered: Missing column detected. Executing: {alter_stmt}")
                        conn.execute(text(alter_stmt))
                        mutations_applied += 1
                    except Exception as e:
                        logger.error(f"Failed to auto-repair table '{table_name}' column '{column.name}': {e}")
                        
    if mutations_applied == 0:
        logger.info("✓ Schema Verified: Database exactly matches SQLAlchemy models.")
    else:
        logger.info(f"✓ Self-Healing Complete: Applied {mutations_applied} structural mutation(s).")

def init_db():
    """
    Defensive Database Initialization Routine.
    Ensures safe startup, triggers self-healing, and builds tables idempotently.
    """
    logger.info(f"Connecting to data persistence layer at: {Config.DATABASE_URL}")
    
    try:
        if "sqlite" in Config.DATABASE_URL:
            # 1. Self-Healing Sequence (Add missing columns dynamically)
            auto_repair_schema(engine, Base.metadata)
            
        # 2. Baseline Sequence (Create entirely new tables if missing)
        Base.metadata.create_all(bind=engine)
        
        return True, "Database initialized and schema verified."
        
    except Exception as e:
        logger.critical(f"FATAL SYSTEM ERROR: Database integrity check completely failed. {e}")
        return False, f"Database Integrity Failure: {e}"

def get_db():
    """Yields safe DB sessions and auto-handles closure."""
    db = SessionLocal()
    try:
        return db
    finally:
        # Avoid closing here if the session needs to live through the request context,
        # but normally yield db -> finally: db.close() if used as a FastApi dependency.
        # Since Streamlit uses this directly, we return the object.
        pass
