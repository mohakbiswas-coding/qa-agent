#!/usr/bin/env python
"""
Startup script for QA Agent Backend with robust error handling and logging
"""
import sys
import os

# Ensure we're in the right directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Try to set unbuffered output for Render logs
try:
    if sys.version_info[0] >= 3:
        # Python 3: use os.environ and reconfigure logging after import
        os.environ['PYTHONUNBUFFERED'] = '1'
    import io
    # Flush function to ensure output appears immediately
    old_write_stdout = sys.stdout.write
    def write_stdout(s):
        old_write_stdout(s)
        sys.stdout.flush()
    sys.stdout.write = write_stdout
except Exception as e:
    pass

import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="[%(asctime)s] %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    force=True
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

try:
    logger.info("=" * 70)
    logger.info("🚀 QA AGENT BACKEND - STARTING UP")
    logger.info("=" * 70)
    
    # Step 1: Environment
    logger.info("\n[STEP 1/4] Loading environment variables...")
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("✓ Environment variables loaded")
    logger.info(f"  Working directory: {os.getcwd()}")
    logger.info(f"  Python version: {sys.version}")
    
    # Step 2: Core dependencies
    logger.info("\n[STEP 2/4] Importing core dependencies...")
    try:
        from fastapi import FastAPI
        logger.debug("  ✓ FastAPI imported")
        import uvicorn
        logger.debug("  ✓ Uvicorn imported")
    except ImportError as e:
        logger.error(f"✗ Failed to import core dependencies: {e}")
        raise
    logger.info("✓ Core dependencies loaded")
    
    # Step 3: Application module
    logger.info("\n[STEP 3/4] Initializing application...")
    try:
        from main import app
        logger.info("✓ FastAPI application initialized")
        logger.debug(f"  App title: {app.title}")
        logger.debug(f"  App version: {app.version}")
    except Exception as e:
        logger.error(f"✗ Failed to initialize application: {e}", exc_info=True)
        raise
    
    # Step 4: Starting server
    logger.info("\n[STEP 4/4] Starting uvicorn server...")
    port = int(os.getenv("PORT", 8000))
    host = "0.0.0.0"
    logger.info(f"✓ Configuration:")
    logger.info(f"  Host: {host}")
    logger.info(f"  Port: {port}")
    logger.info(f"  Environment: {os.getenv('ENVIRONMENT', 'production')}")
    logger.info(f"\n✓ Server will be available at http://{host}:{port}")
    logger.info("=" * 70 + "\n")
    
    # Start the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )

except KeyboardInterrupt:
    logger.info("\n\n⏹️ Server stopped by user")
    sys.exit(0)
    
except Exception as e:
    logger.error("\n" + "=" * 70)
    logger.error("❌ STARTUP FAILED")
    logger.error("=" * 70)
    logger.error(f"\nError: {e}")
    logger.error("\nFull traceback:", exc_info=True)
    logger.error("=" * 70 + "\n")
    sys.exit(1)
