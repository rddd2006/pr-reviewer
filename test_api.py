#!/usr/bin/env python3
"""
Test script to verify the API server is working correctly.
"""

import subprocess
import time
import sys
import requests
import json

def test_api():
    """Test the API server."""
    print("🧪 Testing Diff Reviewer API...")
    print("-" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test 1: Health check
    print("1. Testing health check...")
    try:
        response = requests.get(f"{base_url}/health")
        assert response.status_code == 200
        print("   ✅ API is running")
    except Exception as e:
        print(f"   ❌ Health check failed: {e}")
        return False
    
    # Test 2: Config endpoint
    print("2. Testing config endpoint...")
    try:
        response = requests.get(f"{base_url}/config")
        assert response.status_code == 200
        config = response.json()
        print(f"   ✅ Config retrieved: {len(config.get('supported_commands', []))} commands")
    except Exception as e:
        print(f"   ❌ Config test failed: {e}")
        return False
    
    # Test 3: Review endpoint with test diff
    print("3. Testing review endpoint...")
    test_diff = """--- a/test.py
+++ b/test.py
@@ -1,3 +1,4 @@
 def hello():
-    return "world"
+    x = 1 / 0  # potential error
+    return "world"
"""
    
    try:
        response = requests.post(
            f"{base_url}/review",
            json={
                "diff": test_diff,
                "command": "review",
                "format": "json"
            }
        )
        assert response.status_code == 200
        result = response.json()
        assert result.get("status") == "success"
        print(f"   ✅ Review endpoint working")
    except Exception as e:
        print(f"   ❌ Review test failed: {e}")
        return False
    
    # Test 4: Different commands
    print("4. Testing different commands...")
    commands = ["describe", "generate_labels"]
    
    for command in commands:
        try:
            response = requests.post(
                f"{base_url}/review",
                json={
                    "diff": test_diff,
                    "command": command,
                    "format": "text"
                },
                timeout=30
            )
            if response.status_code == 200:
                print(f"   ✅ {command} command working")
            else:
                print(f"   ⚠️  {command} returned {response.status_code}")
        except requests.exceptions.Timeout:
            print(f"   ⏱️  {command} timed out (LLM processing)")
        except Exception as e:
            print(f"   ❌ {command} failed: {e}")
    
    print("-" * 50)
    print("✅ API tests completed!")
    return True


if __name__ == "__main__":
    # Check if server is running
    try:
        requests.get("http://localhost:8000/health")
    except:
        print("❌ API server is not running!")
        print("   Start it with: python api_server.py")
        sys.exit(1)
    
    # Run tests
    success = test_api()
    sys.exit(0 if success else 1)
