#!/usr/bin/env python3
"""
Test script to verify GOBZIGH static file serving is working.
Run this after restarting Home Assistant with the updated integration.
"""

import requests
import sys

def test_static_files():
    """Test if static files are accessible."""
    # Base URL for Home Assistant
    base_url = input("Enter your Home Assistant URL (e.g., http://localhost:8123): ").strip()
    if not base_url:
        base_url = "http://localhost:8123"
    
    # Test files to check
    test_files = [
        "/api/gobzigh/static/icon.png",
        "/api/gobzigh/static/water_0.png",
        "/api/gobzigh/static/water_5.png",
        "/api/gobzigh/static/diesel_0.png",
        "/api/gobzigh/static/gobzigh-1.png"
    ]
    
    print(f"Testing static file access at: {base_url}")
    print("-" * 50)
    
    success_count = 0
    for file_path in test_files:
        url = f"{base_url}{file_path}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f"✅ {file_path} - OK ({len(response.content)} bytes)")
                success_count += 1
            else:
                print(f"❌ {file_path} - Error {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"❌ {file_path} - Connection error: {e}")
    
    print("-" * 50)
    print(f"Result: {success_count}/{len(test_files)} files accessible")
    
    if success_count == len(test_files):
        print("🎉 All static files are working correctly!")
        return True
    else:
        print("⚠️  Some static files are not accessible. Check the integration setup.")
        return False

if __name__ == "__main__":
    success = test_static_files()
    sys.exit(0 if success else 1)
