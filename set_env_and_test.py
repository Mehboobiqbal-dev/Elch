#!/usr/bin/env python3
"""
Script to set environment variables and test API keys
"""

import os
import sys

# Set the API keys as environment variables
os.environ['GEMINI_API_KEYS'] = 'AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg'

print("🔧 Setting environment variables...")
print(f"GEMINI_API_KEYS set: {os.environ.get('GEMINI_API_KEYS', 'NOT SET')}")

# Now test the API keys
print("\n🧪 Testing API keys...")

try:
    from gemini import api_key_manager
    print(f"✅ API Key Manager loaded successfully")
    print(f"Number of keys: {len(api_key_manager.api_keys)}")
    
    for i, key in enumerate(api_key_manager.api_keys):
        key_prefix = key[:10] if len(key) >= 10 else key[:6]
        print(f"Key {i+1}: {key_prefix}...")
    
    # Test the keys
    import requests
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": "Hello, this is a test."}
                ]
            }
        ]
    }
    
    successful_keys = 0
    for i, api_key in enumerate(api_key_manager.api_keys, 1):
        key_prefix = api_key[:10] if len(api_key) >= 10 else key[:6]
        print(f"\nTesting key {i}: {key_prefix}...")
        
        try:
            response = requests.post(url, headers=headers, params={"key": api_key}, json=data, timeout=10)
            if response.status_code == 200:
                print("✅ SUCCESS: Key works!")
                successful_keys += 1
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n📊 Results: {successful_keys}/{len(api_key_manager.api_keys)} keys working")
    
    if successful_keys > 0:
        print("🎉 API keys are working! The issue was with environment variable loading.")
        print("💡 You can now run the application and it should work properly.")
    else:
        print("❌ No API keys are working. Check your API keys and network connection.")
        
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 50)
