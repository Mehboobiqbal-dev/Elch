#!/usr/bin/env python3
"""
Script to start the application with proper environment variables
"""

import os
import sys
import subprocess

# Set the API keys as environment variables
os.environ['GEMINI_API_KEYS'] = 'AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg'

print("🔧 Starting application with environment variables...")
print(f"GEMINI_API_KEYS set: {os.environ.get('GEMINI_API_KEYS', 'NOT SET')}")

# Test that the API keys are loaded correctly
try:
    from gemini import api_key_manager
    print(f"✅ API Key Manager loaded successfully")
    print(f"Number of keys: {len(api_key_manager.api_keys)}")
    
    for i, key in enumerate(api_key_manager.api_keys):
        key_prefix = key[:10] if len(key) >= 10 else key[:6]
        print(f"Key {i+1}: {key_prefix}...")
    
    if len(api_key_manager.api_keys) == 3:
        print("✅ All 3 API keys loaded successfully!")
    else:
        print(f"⚠️  Only {len(api_key_manager.api_keys)} keys loaded, expected 3")
        
except Exception as e:
    print(f"❌ Error loading API keys: {e}")
    sys.exit(1)

# Start the uvicorn server
print("\n🚀 Starting uvicorn server...")
try:
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
except KeyboardInterrupt:
    print("\n🛑 Server stopped by user")
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)
