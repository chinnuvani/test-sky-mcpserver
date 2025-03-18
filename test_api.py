#!/usr/bin/env python3
"""
Simple script to test the MCP server's SkySQL API endpoint
"""

import requests
import json

def test_skysql_api():
    url = "http://localhost:8000/api/v1/skysql/topologies"
    params = {"service_type": "transactional"}
    headers = {"X-API-Key": "key1"}
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        
        data = response.json()
        print("Response Status Code:", response.status_code)
        print("Response Headers:", json.dumps(dict(response.headers), indent=2))
        print("Response Body:", json.dumps(data, indent=2))
        
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    print("Testing SkySQL API endpoint...")
    test_skysql_api() 