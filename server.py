#!/usr/bin/env python3
"""
MCP Server - Master Control Program Server
Main server application entry point
"""

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, List, Optional

# Local imports
from config import settings
from routes import api_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp_server")

# Initialize FastAPI app
app = FastAPI(
    title="MCP Server",
    description="Master Control Program Server for coordinating and managing system components",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)

@app.get("/health")
async def health_check() -> Dict[str, str]:
    """Health check endpoint"""
    return {"status": "healthy"}

@app.get("/")
async def root() -> Dict[str, str]:
    """Root endpoint with API information"""
    return {
        "message": "Welcome to MCP Server API",
        "docs": "/docs",
        "version": app.version
    }

if __name__ == "__main__":
    logger.info(f"Starting MCP Server on {settings.HOST}:{settings.PORT}")
    uvicorn.run(
        "server:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG_MODE,
    ) 