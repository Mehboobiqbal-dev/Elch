#!/bin/bash

echo "🔧 Fixing Oracle VM environment..."

# Uninstall the wrong google package
echo "🗑️  Uninstalling wrong google package..."
pip uninstall google -y

# Install the correct packages
echo "📦 Installing correct packages..."
pip install google-generativeai python-dotenv fastapi uvicorn requests numpy

# Create .env file
echo "🔑 Creating .env file..."
cat > .env << EOF
# Gemini API Configuration
GEMINI_API_KEYS=AIzaSyCEerwHVrPXswY8P5nc8O-_p7xD-GZdK24,AIzaSyBLciY3gyPM58jTpzR6T5wVolpNPgWFTMI,AIzaSyCMWWcj-rb93ldri33KQU-K5Gz_XCxVXtg

# Other configuration
DEBUG=True
ENVIRONMENT=development
EOF

echo "✅ Environment fixed!"

# Test the setup
echo "🧪 Testing setup..."
python3 -c "
import os
from dotenv import load_dotenv
load_dotenv('.env')

print('Environment variables:')
print(f'GEMINI_API_KEYS: {os.environ.get(\"GEMINI_API_KEYS\", \"NOT SET\")}')

try:
    import google.generativeai as genai
    print('✅ google.generativeai imported successfully')
except Exception as e:
    print(f'❌ Error importing google.generativeai: {e}')

try:
    from core.config import settings
    print(f'✅ Settings loaded: {len(settings.GEMINI_API_KEYS_LIST)} API keys')
except Exception as e:
    print(f'❌ Error loading settings: {e}')
"

echo ""
echo "🚀 To start the application, run:"
echo "   python simple_start.py"
echo "   or"
echo "   uvicorn main:app --host 0.0.0.0 --port 8000 --reload"
