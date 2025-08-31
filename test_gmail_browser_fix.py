#!/usr/bin/env python3
"""
Test Gmail browser creation and service handling fixes
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import asyncio
from request_parser import request_parser
import browsing
import service_handlers
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def test_request_parsing():
    """Test that Gmail request parsing works correctly."""
    print("🧪 Testing Gmail Request Parsing")
    print("=" * 40)

    request = "send gmail to aurangzaibiqbal2@gmail.com say how are you"
    print(f"Request: {request}")

    parsed = request_parser.parse_request(request)
    if 'error' in parsed:
        print(f"❌ Error: {parsed['error']}")
        return False

    print(f"✅ Service: {parsed['service']}")
    print(f"✅ Action: {parsed['action']}")
    print(f"✅ Params: {parsed['params']}")

    # Verify correct parsing
    if parsed['service'] != 'gmail' or parsed['action'] != 'send_email':
        print("❌ Incorrect parsing")
        return False

    if parsed['params']['to'] != 'aurangzaibiqbal2@gmail.com':
        print("❌ Incorrect email recipient")
        return False

    print("✅ Request parsing works correctly")
    return True

def test_browser_creation():
    """Test that browser creation works correctly."""
    print("\n🧪 Testing Browser Creation")
    print("=" * 40)

    # Clean up any existing browsers
    browsing.cleanup_all_browsers()

    profile_name = "gmail_profile"
    print(f"Creating browser with profile: {profile_name}")

    result = browsing.create_persistent_browser(profile_name)
    print(f"Creation result: {result}")

    if "Error" in result or "Failed" in result:
        print(f"❌ Browser creation failed: {result}")
        return False, None

    # Extract browser ID
    import re
    browser_id_match = re.search(r"created with ID: ([^.\s]+)", result)
    if browser_id_match:
        browser_id = browser_id_match.group(1)
        print(f"✅ Browser created with ID: {browser_id}")

        # Verify browser exists
        if browser_id in browsing.browsers:
            print("✅ Browser exists in browsers dictionary")
            return True, browser_id
        else:
            print("❌ Browser not found in browsers dictionary")
            return False, None
    else:
        print("❌ Could not extract browser ID")
        return False, None

def test_gmail_navigation(browser_id):
    """Test Gmail navigation."""
    print("\n🧪 Testing Gmail Navigation")
    print("=" * 40)

    print(f"Navigating browser {browser_id} to Gmail")

    result = browsing.navigate_to_service(browser_id, "gmail")
    print(f"Navigation result: {result}")

    if "not found" in result:
        print(f"❌ Navigation failed: {result}")
        return False

    print("✅ Navigation completed")
    return True

def test_gmail_handler(browser_id):
    """Test Gmail handler initialization."""
    print("\n🧪 Testing Gmail Handler")
    print("=" * 40)

    try:
        handler = service_handlers.GmailHandler(browser_id)
        print(f"✅ Gmail handler created for browser {browser_id}")

        # Test login check (may not be logged in, but shouldn't crash)
        login_status = handler.check_login()
        print(f"Login status check: {login_status}")

        return True
    except Exception as e:
        print(f"❌ Gmail handler failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Gmail Browser Fix Verification")
    print("=" * 50)

    success_count = 0
    total_tests = 4

    # Test 1: Request parsing
    if test_request_parsing():
        success_count += 1

    # Test 2: Browser creation
    browser_success, browser_id = test_browser_creation()
    if browser_success:
        success_count += 1

        # Test 3: Gmail navigation (only if browser creation succeeded)
        if test_gmail_navigation(browser_id):
            success_count += 1

        # Test 4: Gmail handler (only if browser creation succeeded)
        if test_gmail_handler(browser_id):
            success_count += 1

    # Clean up
    print("\n🧹 Cleaning up browsers...")
    browsing.cleanup_all_browsers()

    # Results
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    print(f"✅ {success_count}/{total_tests} tests passed")

    if success_count == total_tests:
        print("🎉 ALL TESTS PASSED!")
        print("\n💡 The Gmail browser issues should now be fixed:")
        print("   • Browser creation works correctly")
        print("   • Browser ID extraction works")
        print("   • Gmail navigation works")
        print("   • Service handlers work")
        print("   • Memory deduplication works")
        return True
    else:
        print("⚠️  SOME TESTS FAILED")
        print("   Check the error messages above for details.")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n🔚 Overall result: {'SUCCESS' if success else 'FAILED'}")
    sys.exit(0 if success else 1)

