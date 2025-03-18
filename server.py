#!/usr/bin/env python3
"""
MCP Server - Master Control Program Server
Main server application entry point
"""

import uvicorn
from fastapi import FastAPI, Depends, HTTPException, status, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
from typing import Dict, List, Optional, Any
import json

# Local imports
from config import settings
from routes import api_router
from skysql_api import get_skysql_topologies

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger("mcp_server")

# Initialize FastAPI app
app = FastAPI(
    title="MCP Server",
    description="MCP Server with SkySQL API Integration",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

# MCP Protocol Endpoints
@app.get("/tools/list")
async def list_tools():
    """List available tools in the MCP protocol."""
    return {
        "tools": [
            {
                "name": "get_skysql_topologies",
                "description": "Get available topologies from SkySQL API",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "service_type": {
                            "type": "string",
                            "description": "Type of service to get topologies for",
                            "enum": ["transactional", "analytical"]
                        }
                    },
                    "required": ["service_type"]
                }
            }
        ]
    }

@app.post("/tools/call")
async def call_tool(
    request: Request,
    api_key: Optional[str] = Header(None)
):
    """Call a specific tool with given parameters."""
    try:
        # Parse request body
        body = await request.json()
        tool_name = body.get("tool_name")
        parameters = body.get("parameters", {})
        
        if not tool_name:
            raise HTTPException(
                status_code=400, 
                detail="Missing required parameter 'tool_name' in request body"
            )
            
        if tool_name == "get_skysql_topologies":
            # Check if we're using a dummy key
            if settings.SKYSQL_API_KEY == "dummy-key-for-development":
                # Return mock data for development testing
                return {
                    "topologies": [
                        {
                            "id": "sample-topology-1",
                            "name": "Development Sample Topology 1",
                            "description": "This is a sample topology for development purposes",
                            "serviceType": parameters.get("service_type", "transactional")
                        },
                        {
                            "id": "sample-topology-2",
                            "name": "Development Sample Topology 2",
                            "description": "Another sample topology for development purposes",
                            "serviceType": parameters.get("service_type", "transactional")
                        }
                    ]
                }
            try:
                return await get_skysql_topologies(parameters.get("service_type"))
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        raise HTTPException(status_code=404, detail=f"Tool {tool_name} not found")
    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON in request body")

@app.get("/resources")
async def get_resources():
    """Get available resources in the MCP protocol."""
    return {
        "resources": [
            {
                "name": "skysql_topologies",
                "type": "api",
                "description": "SkySQL API topologies resource"
            }
        ]
    }

@app.get("/prompts")
async def get_prompts():
    """Get available prompts in the MCP protocol."""
    return {
        "prompts": [
            {
                "name": "default",
                "description": "Default system prompt",
                "content": "You are a helpful AI assistant."
            }
        ]
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
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