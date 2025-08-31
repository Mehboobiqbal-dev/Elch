#!/usr/bin/env python3
"""
Simple script to start the application with environment variables
"""

import os
import sys

# Set the API keys as environment variables
os.environ['GEMINI_API_KEYS'] = 'AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg'

print("🔧 Environment variables set")
print(f"GEMINI_API_KEYS: {os.environ.get('GEMINI_API_KEYS', 'NOT SET')}")

# Test basic imports
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported successfully")
except Exception as e:
    print(f"❌ Error importing google.generativeai: {e}")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
except Exception as e:
    print(f"❌ Error importing python-dotenv: {e}")
    sys.exit(1)

# Test API key loading
try:
    from core.config import settings
    print(f"✅ Settings loaded: {len(settings.GEMINI_API_KEYS_LIST)} API keys")
except Exception as e:
    print(f"❌ Error loading settings: {e}")
    sys.exit(1)

print("🚀 Starting uvicorn server...")
print("Press Ctrl+C to stop")

# Start uvicorn directly
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=False,  # Disable reload to avoid multiprocessing issues
        log_level="info"
    )
