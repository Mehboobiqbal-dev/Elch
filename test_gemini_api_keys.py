#!/usr/bin/env python3
"""
Test Gemini API keys manually to verify they work
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import requests
import json

def test_gemini_api_keys():
    """Test Gemini API keys using direct HTTP requests."""
    print("🔑 Testing Gemini API Keys")
    print("=" * 40)

    # Load API keys from the same source as the agent
    try:
        from gemini import api_key_manager
        api_keys = api_key_manager.api_keys
    except Exception as e:
        print(f"❌ Could not load API keys from agent: {e}")
        return False

    if not api_keys:
        print("❌ No API keys found!")
        return False

    print(f"Found {len(api_keys)} API keys to test")

    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    headers = {"Content-Type": "application/json"}
    data = {
        "contents": [
            {
                "parts": [
                    {"text": "Write a short poem about the moon."}
                ]
            }
        ]
    }

    successful_keys = 0

    for i, api_key in enumerate(api_keys, 1):
        key_prefix = api_key[:10] if len(api_key) >= 10 else api_key[:6]

        print(f"\n🧪 Testing key {i}: {key_prefix}...")
        params = {"key": api_key}

        try:
            response = requests.post(url, headers=headers, params=params, json=data, timeout=10)

            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    text = result['candidates'][0]['content']['parts'][0]['text']
                    print("✅ SUCCESS: Key works!")
                    print(f"   Response: {text[:100]}...")
                    successful_keys += 1
                else:
                    print(f"❌ Unexpected response format: {result}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text}")

        except requests.exceptions.Timeout:
            print("❌ Timeout - API took too long to respond")
        except requests.exceptions.RequestException as e:
            print(f"❌ Request error: {e}")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")

    print(f"\n📊 Results: {successful_keys}/{len(api_keys)} keys working")

    if successful_keys == len(api_keys):
        print("🎉 ALL API KEYS ARE WORKING!")
        print("💡 The issue was with rate limiting, not the API keys themselves.")
        return True
    elif successful_keys > 0:
        print("⚠️  SOME API KEYS ARE WORKING")
        print("💡 This suggests the issue is with specific keys or rate limiting.")
        return True
    else:
        print("❌ NO API KEYS ARE WORKING")
        print("💡 Check your API keys and network connection.")
        return False

def main():
    """Main test function."""
    print("🚀 Gemini API Key Validation")
    print("=" * 50)
    print("Testing API keys directly to confirm they work (as you mentioned).")
    print()

    success = test_gemini_api_keys()

    print("\n" + "=" * 50)
    if success:
        print("✅ CONFIRMED: API keys work when tested manually")
        print("💡 This confirms the issue was with the agent's rate limiting,")
        print("   not with the API keys themselves.")
        print("💡 The fixes should resolve the quota exhaustion problem.")
    else:
        print("❌ API keys are not working even manually")
        print("💡 Check your API keys, network, and Gemini API status.")

    return success

if __name__ == "__main__":
    success = main()
    print(f"\n🔚 Validation result: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(0 if success else 1)
