#!/usr/bin/env python3
"""
MCP Server - Configuration Module
Handles loading and managing configuration settings
"""

import os
import secrets
from pydantic import BaseModel, validator
from typing import List, Optional, Dict, Any, Union
from dotenv import load_dotenv

# Load .env file if it exists
load_dotenv()

class Settings(BaseModel):
    """Application settings model"""
    
    # Server settings
    HOST: str = os.getenv("MCP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("MCP_PORT", "8000"))
    DEBUG_MODE: bool = os.getenv("MCP_DEBUG", "False").lower() in ("true", "1", "t")
    
    # Security settings
    SECRET_KEY: str = os.getenv("MCP_SECRET_KEY", secrets.token_urlsafe(32))
    API_KEY_HEADER: str = "X-API-Key"
    API_KEYS: List[str] = [x.strip() for x in os.getenv("MCP_API_KEYS", "").split(",") if x.strip()]
    
    # SkySQL API settings
    # Hardcoded API key (will override environment variable)
    SKYSQL_API_KEY: str = "skysql.1zzz.d694izfz.yT4stzKTAGHOIQpmDn2KbzpQRzVJ9o5DxoIA.59fe0332"
    
    # CORS settings
    CORS_ORIGINS: List[str] = [
        x.strip() for x in os.getenv("MCP_CORS_ORIGINS", "http://localhost,http://localhost:3000").split(",")
    ]
    
    # Database settings
    DATABASE_URL: Optional[str] = os.getenv("MCP_DATABASE_URL", None)
    
    # Logging settings
    LOG_LEVEL: str = os.getenv("MCP_LOG_LEVEL", "INFO")
    
    # Agent settings
    MAX_AGENTS: int = int(os.getenv("MCP_MAX_AGENTS", "10"))
    AGENT_TIMEOUT: int = int(os.getenv("MCP_AGENT_TIMEOUT", "60"))
    
    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": True
    }

# Initialize settings
settings = Settings()

# For debugging
if __name__ == "__main__":
    print("Current MCP Server Settings:")
    for key, value in settings.model_dump().items():
        # Don't print out sensitive values
        if key in ["SECRET_KEY", "API_KEYS", "SKYSQL_API_KEY"]:
            print(f"{key}: [REDACTED]")
        else:
            print(f"{key}: {value}") 