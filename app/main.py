#!/usr/bin/env python3
"""
Simple FastAPI Application with REST Service Calls

This FastAPI app demonstrates how to call external REST endpoints
and provides a clean API interface for clients.

Installation:
pip install fastapi uvicorn httpx pydantic

Run:
uvicorn main:app --reload --host 0.0.0.0 --port 8000

Access:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
import logging
from datetime import datetime
from rag.routes import router as rag_route

# ============================================================================
# Configuration
# ============================================================================

class Settings:
    """Application settings"""
    
    # External API endpoints
    JSONPLACEHOLDER_BASE_URL = "https://jsonplaceholder.typicode.com"
    DEMO_URL = "https://api.demo.com/v1"
    
    # Timeouts
    REQUEST_TIMEOUT = 30.0
    
    # App info
    APP_NAME = "Simple FastAPI REST Client"
    APP_VERSION = "1.0.0"

settings = Settings()

# ============================================================================
# Logging Setup
# ============================================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title=settings.APP_NAME,
    description="A simple FastAPI application that calls external REST services",
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(rag_route)

# ============================================================================
# Root Endpoint
# ============================================================================

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}


# ============================================================================
# Error Handlers
# ============================================================================

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    """Handle HTTP exceptions"""
    logger.error(f"HTTP error {exc.status_code}: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "timestamp": datetime.utcnow().isoformat()
        }
    )
@app.exception_handler(Exception)
async def general_exception_handler(request, exc: Exception):
    """Handle general exceptions"""
    logger.error(f"Unexpected error: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "success": False,
            "message": "Internal server error",
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", 
                host="0.0.0.0", 
                port=8000, 
                reload=True, 
                log_level="debug")