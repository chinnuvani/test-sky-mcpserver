#!/usr/bin/env python3
"""
Local development script to run the MCP server with configuration
"""

import os
import json
import subprocess
from typing import Dict, Any

def run_server() -> None:
    """Run the server with local development configuration."""
    # Create environment variables
    env = {
        "MCP_HOST": "0.0.0.0",
        "MCP_PORT": "8000",
        "MCP_DEBUG": "True",  # Enable debug mode for local development
        "MCP_SECRET_KEY": "local-dev-secret-key",
        "MCP_API_KEYS": "local-dev-key",
        "SKYSQL_API_KEY": "skysql.1zzz.d694izfz.yT4stzKTAGHOIQpmDn2KbzpQRzVJ9o5DxoIA.59fe0332"
    }
    
    # Update environment with existing variables
    env.update(os.environ)
    
    print("\nStarting server with environment:")
    for key in ["MCP_HOST", "MCP_PORT", "MCP_DEBUG", "MCP_API_KEYS"]:
        print(f"{key}: {env[key]}")
    print("SKYSQL_API_KEY: [redacted]")
    print("\nPress Ctrl+C to stop the server")
    
    # Run the server
    try:
        subprocess.run(
            ["python", "server.py"],
            env=env,
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(f"Error running server: {e}")
    except KeyboardInterrupt:
        print("\nServer stopped by user")

if __name__ == "__main__":
    run_server() 