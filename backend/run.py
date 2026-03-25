#!/usr/bin/env python
"""
Startup script for QA Agent Backend with robust error handling
"""
import sys
import os

# Force unbuffered output for Render logs
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 0) if sys.version_info[0] < 3 else sys.stdout
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0) if sys.version_info[0] < 3 else sys.stderr

import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger(__name__)

try:
    logger.info("=" * 60)
    logger.info("🚀 QA Agent Backend - Starting")
    logger.info("=" * 60)
    
    logger.info("Step 1: Setting up environment...")
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    logger.info(f"   Working directory: {os.getcwd()}")
    
    from dotenv import load_dotenv
    load_dotenv()
    logger.info("✓ Environment loaded")
    
    logger.info("Step 2: Importing dependencies...")
    from fastapi import FastAPI
    logger.info("   ✓ FastAPI imported")
    
    # Import the app from main
    import importlib.util
    spec = importlib.util.spec_from_file_location("main_module", os.path.join(os.path.dirname(__file__), "main.py"))
    main_module = importlib.util.module_from_spec(spec)
    logger.info("   ✓ Loading main.py...")
    
    try:
        spec.loader.exec_module(main_module)
        logger.info("   ✓ main.py loaded successfully")
    except Exception as e:
        logger.error(f"✗ Failed to load main.py: {e}", exc_info=True)
        raise
    
    app = main_module.app
    
    logger.info("Step 3: Starting uvicorn server...")
    port = int(os.getenv("PORT", 8000))
    logger.info(f"   Port: {port}")
    logger.info(f"   Host: 0.0.0.0")
    logger.info(f"   Environment: {os.getenv('ENV', 'production')}")
    
    import uvicorn
    logger.info("=" * 60)
    logger.info("✓ All checks passed. Starting server...")
    logger.info("=" * 60)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

except Exception as e:
    logger.error("=" * 60)
    logger.error(f"✗ STARTUP FAILED: {e}")
    logger.error("=" * 60, exc_info=True)
    sys.exit(1)
