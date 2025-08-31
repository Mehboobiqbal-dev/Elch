#!/bin/bash

echo "🔧 Setting up Oracle VM environment..."

# Install required Python packages
echo "📦 Installing Python packages..."
pip install google-generativeai python-dotenv fastapi uvicorn requests numpy

# Create .env file with API keys
echo "🔑 Creating .env file with API keys..."
cat > .env << EOF
# Gemini API Configuration
GEMINI_API_KEYS=AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg

# Other configuration
DEBUG=True
ENVIRONMENT=development
EOF

echo "✅ .env file created successfully!"

# Test API keys
echo "🧪 Testing API keys..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv('.env')

print('Environment variables:')
print(f'GEMINI_API_KEYS: {os.environ.get(\"GEMINI_API_KEYS\", \"NOT SET\")}')

try:
    from gemini import api_key_manager
    print(f'API Key Manager loaded: {len(api_key_manager.api_keys)} keys')
    for i, key in enumerate(api_key_manager.api_keys):
        print(f'Key {i+1}: {key[:10]}...')
    print('✅ API keys loaded successfully!')
except Exception as e:
    print(f'❌ Error: {e}')
"

echo ""
echo "🚀 To start the application, run:"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
echo ""
echo "💡 The application should now work with all 3 API keys!"
