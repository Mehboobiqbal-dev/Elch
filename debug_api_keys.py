#!/usr/bin/env python3
"""
Debug script to check API key loading
"""

import os
import sys

print("🔍 Debugging API Key Loading")
print("=" * 40)

# Check environment variables
print("Environment Variables:")
print(f"GEMINI_API_KEYS: {os.environ.get('GEMINI_API_KEYS', 'NOT SET')}")
print(f"GEMINI_API_KEY: {os.environ.get('GEMINI_API_KEY', 'NOT SET')}")

# Check if .env file exists
env_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if file.endswith('.env'):
            env_files.append(os.path.join(root, file))

print(f"\n.env files found: {env_files}")

# Try to load settings
try:
    from core.config import settings
    print(f"\nSettings loaded:")
    print(f"GEMINI_API_KEYS_LIST: {settings.GEMINI_API_KEYS_LIST}")
    print(f"GEMINI_API_KEY: {settings.GEMINI_API_KEY}")
except Exception as e:
    print(f"\nError loading settings: {e}")

# Try to load from gemini module
try:
    from gemini import api_key_manager
    print(f"\nGemini API Key Manager:")
    print(f"Number of keys: {len(api_key_manager.api_keys)}")
    for i, key in enumerate(api_key_manager.api_keys):
        key_prefix = key[:10] if len(key) >= 10 else key[:6]
        print(f"Key {i+1}: {key_prefix}...")
except Exception as e:
    print(f"\nError loading gemini module: {e}")

print("\n" + "=" * 40)
