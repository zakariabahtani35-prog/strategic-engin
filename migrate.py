import logging
from app.db import engine, auto_repair_schema
from app.models import Base

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
logger = logging.getLogger("MigrationEngine")

def run_migration_engine():
    """
    Professional Standalone Migration Engine.
    Leverages the core auto-repair logic to ensure the schema is production-ready.
    Idempotent by design.
    """
    logger.info("=== INITIALIZING STRATEGIC ENGINE DATABASE MIGRATION ===")
    
    try:
        # Pre-flight Check: Does the database exist at all?
        logger.info("Step 1: Baseline Structural Validation.")
        Base.metadata.create_all(bind=engine)
        logger.info("✓ Core table structures verified/created.")
        
        # Deep Inspection: Resolve Schema Mismatches
        logger.info("Step 2: Deep Schema Inspection & Auto-Repair.")
        auto_repair_schema(engine, Base.metadata)
        
        logger.info("=== MIGRATION SEQUENCE COMPLETED SUCCESSFULLY ===")
        
    except Exception as e:
        logger.critical(f"xxx MIGRATION FATAL EXCEPTION: {e}")
        logger.critical("MANUAL INTERVENTION REQUIRED. Check database locks and file permissions.")

if __name__ == "__main__":
    run_migration_engine()
