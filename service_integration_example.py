#!/usr/bin/env python3
"""
Simple example showing how to use the enhanced Elch Agent
for browser-based service integration.
"""

import requests
import json
import time

# Configuration
BASE_URL = "http://localhost:8000"
AUTH_TOKEN = "your-auth-token-here"  # Replace with actual token

def make_request(endpoint, method="POST", data=None):
    """Helper function to make API requests."""
    url = f"{BASE_URL}{endpoint}"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AUTH_TOKEN}"
    }

    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method == "GET":
            response = requests.get(url, headers=headers)
        else:
            print(f"Unsupported method: {method}")
            return None

        if response.status_code == 401:
            print("❌ Authentication failed. Please check your token.")
            return None
        elif response.status_code != 200:
            print(f"❌ Request failed: {response.status_code} - {response.text}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return None

def example_1_simple_email():
    """Example 1: Send a simple email via Gmail."""
    print("📧 Example 1: Send Email via Gmail")
    print("-" * 40)

    # Step 1: Create a persistent browser for Gmail
    print("1. Creating persistent browser...")
    browser_result = make_request("/browsers/create", data={
        "profile_name": "gmail_session"
    })

    if not browser_result:
        return

    print(f"✅ Browser created: {browser_result.get('message', 'Unknown')}")

    # Step 2: Navigate to Gmail (you would need to log in manually first)
    print("2. Navigating to Gmail...")
    nav_result = make_request("/service/navigate", data={
        "service": "gmail",
        "browser_id": "persistent_gmail_session_0"  # Adjust based on actual ID
    })

    if nav_result:
        print(f"✅ Navigation: {nav_result.get('message', 'Unknown')}")

    # Step 3: Send email (would work if logged in)
    print("3. Sending email...")
    email_result = make_request("/service/send-email", data={
        "service": "gmail",
        "browser_id": "persistent_gmail_session_0",
        "to": "friend@example.com",
        "subject": "Hello from Elch Agent!",
        "body": "This email was sent automatically by the Elch Agent using your browser session."
    })

    if email_result:
        print(f"✅ Email result: {email_result.get('message', 'Unknown')}")

def example_2_agent_integration():
    """Example 2: Use the agent to handle service requests automatically."""
    print("\n🤖 Example 2: Agent Integration")
    print("-" * 40)

    # Use the enhanced agent which will automatically:
    # 1. Classify the request as 'service'
    # 2. Parse the request to extract service, action, and parameters
    # 3. Create browser and execute the action

    user_request = "Send an email to john@example.com about tomorrow's meeting"

    print(f"User Request: '{user_request}'")
    print("\nAgent will automatically:")
    print("1. ✅ Classify as 'service' request")
    print("2. ✅ Parse to extract: service=gmail, action=send_email")
    print("3. ✅ Create persistent browser")
    print("4. ✅ Navigate to Gmail")
    print("5. ✅ Check login status")
    print("6. ✅ Send the email")
    print("7. ✅ Report success/failure")

    # Make the request to the agent
    result = make_request("/agent/run", data={
        "user_input": user_request,
        "run_id": f"run_{int(time.time())}"
    })

    if result:
        print("
🎯 Agent Response:"        print(f"Status: {result.get('status', 'unknown')}")
        print(f"Message: {result.get('message', 'No message')}")
        if result.get('final_result'):
            print(f"Result: {result.get('final_result')}")

def example_3_skype_call():
    """Example 3: Make a Skype call."""
    print("\n📞 Example 3: Make Skype Call")
    print("-" * 40)

    # Create browser for Skype
    print("1. Creating Skype browser...")
    browser_result = make_request("/browsers/create", data={
        "profile_name": "skype_session"
    })

    if browser_result:
        print(f"✅ Browser: {browser_result.get('message', 'Unknown')}")

        # Navigate to Skype
        print("2. Navigating to Skype...")
        nav_result = make_request("/service/navigate", data={
            "service": "skype",
            "browser_id": "persistent_skype_session_0"
        })

        if nav_result:
            print(f"✅ Navigation: {nav_result.get('message', 'Unknown')}")

            # Start call
            print("3. Starting call...")
            call_result = make_request("/service/start-call", data={
                "service": "skype",
                "browser_id": "persistent_skype_session_0",
                "contact": "friend@example.com"
            })

            if call_result:
                print(f"✅ Call result: {call_result.get('message', 'Unknown')}")

def example_4_browser_management():
    """Example 4: Browser management and status."""
    print("\n🌐 Example 4: Browser Management")
    print("-" * 40)

    # Get browser status
    print("1. Checking browser status...")
    status_result = make_request("/browsers/status", method="GET")

    if status_result:
        print("✅ Current Status:")
        print(f"   Active browsers: {status_result.get('active_browsers', 0)}")
        print(f"   Browser IDs: {status_result.get('browser_ids', [])}")
        print(f"   Profiles: {status_result.get('profiles', [])}")

    # Cleanup browsers
    print("2. Cleaning up browsers...")
    cleanup_result = make_request("/browsers/cleanup")

    if cleanup_result:
        print(f"✅ Cleanup: {cleanup_result.get('message', 'Unknown')}")
        print(f"   Active browsers: {cleanup_result.get('active_browsers', 0)}")

def example_5_login_status_check():
    """Example 5: Check login status for services."""
    print("\n🔐 Example 5: Login Status Check")
    print("-" * 40)

    # Check Gmail login status
    print("1. Checking Gmail login status...")
    login_result = make_request("/service/check-login", data={
        "service": "gmail",
        "browser_id": "persistent_gmail_session_0"
    })

    if login_result:
        login_status = login_result.get('login_status', {})
        print("✅ Gmail Login Status:")
        print(f"   Logged in: {login_status.get('logged_in', 'Unknown')}")
        print(f"   Service: {login_status.get('service', 'Unknown')}")
        print(f"   Confidence: {login_status.get('confidence', 'Unknown')}")

def main():
    """Run all examples."""
    print("🚀 Elch Agent Service Integration Examples")
    print("=" * 60)
    print("This script demonstrates how to use the enhanced Elch Agent")
    print("for browser-based service integration.")
    print()

    if AUTH_TOKEN == "your-auth-token-here":
        print("⚠️  Please set your AUTH_TOKEN before running these examples!")
        print("   You can get a token by logging in via the /token endpoint.")
        print()

    # Run examples
    try:
        example_1_simple_email()
        example_2_agent_integration()
        example_3_skype_call()
        example_4_browser_management()
        example_5_login_status_check()

        print("\n" + "=" * 60)
        print("🎉 Examples Complete!")
        print("\n💡 Key Takeaways:")
        print("   • Agent automatically classifies and handles service requests")
        print("   • Persistent browser sessions maintain login state")
        print("   • Service-specific handlers manage complex interactions")
        print("   • Seamless integration with existing agent workflow")
        print("   • Support for Gmail, Skype, Outlook, and many more services")

    except KeyboardInterrupt:
        print("\n👋 Examples stopped by user.")
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")

if __name__ == "__main__":
    main()

