#!/usr/bin/env python3
"""
Script to set up the .env file with API keys
"""

import os

# API keys to add
api_keys = 'AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg'

# Content for .env file
env_content = f"""# Gemini API Configuration
GEMINI_API_KEYS={api_keys}

# Other configuration
DEBUG=True
ENVIRONMENT=development
"""

print("🔧 Setting up .env file...")

# Write to .env file
try:
    with open('.env', 'w') as f:
        f.write(env_content)
    print("✅ .env file created successfully!")
    
    # Verify the file was created
    if os.path.exists('.env'):
        print("✅ .env file exists and is readable")
        
        # Test loading the environment variables
        from dotenv import load_dotenv
        load_dotenv('.env')
        
        loaded_keys = os.environ.get('GEMINI_API_KEYS', '')
        if loaded_keys:
            print(f"✅ Environment variables loaded: {loaded_keys[:50]}...")
        else:
            print("❌ Environment variables not loaded")
            
    else:
        print("❌ .env file was not created")
        
except Exception as e:
    print(f"❌ Error creating .env file: {e}")

print("\n📝 Next steps:")
print("1. Run: python start_with_env.py")
print("2. Or run: uvicorn main:app --host 0.0.0.0 --port 8000 --reload")
print("3. The application should now work with all 3 API keys!")
