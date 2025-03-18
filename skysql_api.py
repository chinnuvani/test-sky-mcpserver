#!/usr/bin/env python3
"""
MCP Server - SkySQL API Module
Handles interactions with the SkySQL API
"""

import httpx
from typing import Dict, List, Optional, Any
from config import settings

class SkySQLAPI:
    """SkySQL API client"""
    
    BASE_URL = "https://api.skysql.com"
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    async def get_topologies(self, service_type: str = "transactional") -> Dict[str, Any]:
        """Get available topologies for a service type"""
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.BASE_URL}/provisioning/v1/topologies",
                params={"service_type": service_type},
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()

# Create a singleton instance
skysql_client = SkySQLAPI(settings.SKYSQL_API_KEY)

# Add the function that server.py is trying to import
async def get_skysql_topologies(service_type: str = "transactional") -> Dict[str, Any]:
    """Wrapper function to get topologies from SkySQL API"""
    return await skysql_client.get_topologies(service_type) 