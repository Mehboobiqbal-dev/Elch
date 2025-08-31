#!/usr/bin/env python3
"""
Demo script for the enhanced Elch Agent with browser-based service integration.
Shows how to use Gmail, Skype, Outlook, and other services with persistent browser sessions.
"""

import os
import sys
import json
import time

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from request_parser import request_parser
from service_handlers import get_service_handler
import browsing

def demo_request_parsing():
    """Demonstrate intelligent request parsing."""
    print("🎯 Request Parsing Demo")
    print("=" * 50)

    test_requests = [
        "Send an email to john@example.com about the project meeting",
        "Call mom on Skype to wish her happy birthday",
        "Send a message to the team on Slack about the deadline",
        "What is the capital of France?",  # General question
        "Book a flight to Paris",  # Task
        "Send email to boss@company.com subject: 'Project Update' saying 'The project is on track'",
        "Make a video call with john on Teams",
        "Text 'Hello' to Sarah on WhatsApp",
        "Post an update on LinkedIn about my new job"
    ]

    for request in test_requests:
        print(f"\n📝 Request: {request}")

        # Parse the request
        parsed = request_parser.parse_request(request)

        if "error" in parsed:
            print(f"❌ Error: {parsed['error']}")
        else:
            print(f"✅ Service: {parsed['service']}")
            print(f"✅ Action: {parsed['action']}")
            print(f"✅ Params: {json.dumps(parsed['params'], indent=2)}")

            # Generate execution plan
            plan = request_parser.generate_plan(parsed)
            if "error" not in plan:
                print("✅ Execution Plan:"                for i, step in enumerate(plan['steps'], 1):
                    print(f"   {i}. {step['action']} with params: {step.get('params', {})}")

        print("-" * 40)
        time.sleep(0.5)  # Brief pause between requests

def demo_browser_management():
    """Demonstrate browser management features."""
    print("\n🌐 Browser Management Demo")
    print("=" * 50)

    try:
        # Check initial status
        print("📊 Initial browser status:")
        status = {
            "active_browsers": browsing.get_browser_count(),
            "browser_ids": list(browsing.browsers.keys()),
            "profiles": list(browsing.browser_profiles.keys())
        }
        print(json.dumps(status, indent=2))

        # Create a persistent browser
        print("\n🆕 Creating persistent browser for Gmail...")
        result = browsing.create_persistent_browser("gmail_demo")
        print(f"✅ Result: {result}")

        # Check status after creation
        print("\n📊 Status after browser creation:")
        status = {
            "active_browsers": browsing.get_browser_count(),
            "browser_ids": list(browsing.browsers.keys()),
            "profiles": list(browsing.browser_profiles.keys())
        }
        print(json.dumps(status, indent=2))

        # Test navigation (if browser was created successfully)
        if "Error" not in result and browsing.browsers:
            browser_id = list(browsing.browsers.keys())[0]

            print(f"\n🧭 Testing navigation to Gmail with browser {browser_id}...")
            nav_result = browsing.navigate_to_service(browser_id, "gmail")
            print(f"✅ Navigation result: {nav_result}")

            # Test login status check
            print("
🔐 Checking Gmail login status..."            login_status = browsing.check_login_status(browser_id, "gmail")
            print(f"✅ Login status: {json.dumps(login_status, indent=2)}")

        # Cleanup
        print("
🧹 Cleaning up browsers..."        cleanup_count = browsing.cleanup_all_browsers()
        print(f"✅ Cleaned up {cleanup_count} browsers")

    except Exception as e:
        print(f"❌ Browser management demo failed: {e}")

def demo_service_handlers():
    """Demonstrate service-specific handlers."""
    print("\n📧 Service Handlers Demo")
    print("=" * 50)

    # Create a mock browser for demonstration
    print("🔧 Note: This demo shows handler capabilities.")
    print("   In real usage, you would have an actual browser instance.")
    print("   The handlers are ready to use with persistent browser sessions.")

    services_to_demo = ["gmail", "skype", "outlook"]

    for service in services_to_demo:
        print(f"\n🌐 {service.upper()} Handler:")

        # Get handler (would normally have a real browser_id)
        handler = get_service_handler(service, "mock_browser_id")

        if handler:
            print("✅ Handler created successfully"            print(f"   Type: {type(handler).__name__}")

            # Show available methods
            methods = [method for method in dir(handler) if not method.startswith('_') and callable(getattr(handler, method))]
            print(f"   Available methods: {', '.join(methods)}")

            if hasattr(handler, 'check_login'):
                print("   ✅ Login checking supported"            if hasattr(handler, 'send_email'):
                print("   ✅ Email sending supported"            if hasattr(handler, 'start_call'):
                print("   ✅ Call starting supported"            if hasattr(handler, 'send_message'):
                print("   ✅ Message sending supported"        else:
            print(f"❌ No handler available for {service}")

def demo_integration_workflow():
    """Demonstrate a complete integration workflow."""
    print("\n🚀 Complete Integration Workflow Demo")
    print("=" * 50)

    print("This demonstrates how the enhanced agent processes requests:")
    print()

    # Simulate the workflow
    user_request = "Send an email to john@example.com about tomorrow's meeting"

    print("1️⃣ User Request:")
    print(f"   '{user_request}'")
    print()

    print("2️⃣ Request Classification:")
    print("   → Detected as 'service' request (not 'general' or 'task')")
    print()

    print("3️⃣ Intelligent Parsing:")
    parsed = request_parser.parse_request(user_request)
    print(f"   Service: {parsed.get('service', 'unknown')}")
    print(f"   Action: {parsed.get('action', 'unknown')}")
    print(f"   Parameters: {json.dumps(parsed.get('params', {}), indent=2)}")
    print()

    print("4️⃣ Plan Generation:")
    if "error" not in parsed:
        plan = request_parser.generate_plan(parsed)
        if "error" not in plan:
            print("   Execution Steps:")
            for i, step in enumerate(plan['steps'], 1):
                print(f"   {i}. {step['action']} with params: {step.get('params', {})}")
    print()

    print("5️⃣ Browser Session Management:")
    print("   → Create persistent browser with Gmail profile")
    print("   → Navigate to Gmail (https://mail.google.com)")
    print("   → Check login status")
    print("   → Execute email composition and sending")
    print()

    print("6️⃣ Service-Specific Execution:")
    print("   → Use GmailHandler to compose and send email")
    print("   → Handle Gmail-specific UI elements")
    print("   → Confirm successful sending")
    print()

    print("7️⃣ Session Persistence:")
    print("   → Browser profile saved for future use")
    print("   → Login session maintained between requests")
    print("   → Cookies and authentication preserved")

def demo_supported_services():
    """Show all supported services and their capabilities."""
    print("\n📋 Supported Services & Capabilities")
    print("=" * 50)

    services = {
        "gmail": {
            "url": "https://mail.google.com",
            "capabilities": ["send_email"],
            "description": "Send emails via Gmail"
        },
        "skype": {
            "url": "https://web.skype.com",
            "capabilities": ["start_call", "send_message"],
            "description": "Make calls and send messages via Skype"
        },
        "outlook": {
            "url": "https://outlook.live.com",
            "capabilities": ["send_email"],
            "description": "Send emails via Outlook/Hotmail"
        },
        "slack": {
            "url": "https://app.slack.com",
            "capabilities": ["send_message", "schedule_meeting"],
            "description": "Send messages and schedule meetings via Slack"
        },
        "discord": {
            "url": "https://discord.com/app",
            "capabilities": ["send_message", "start_call", "join_meeting"],
            "description": "Send messages and make calls via Discord"
        },
        "whatsapp": {
            "url": "https://web.whatsapp.com",
            "capabilities": ["send_message", "start_call"],
            "description": "Send messages and make calls via WhatsApp Web"
        },
        "telegram": {
            "url": "https://web.telegram.org",
            "capabilities": ["send_message"],
            "description": "Send messages via Telegram Web"
        },
        "facebook": {
            "url": "https://www.facebook.com",
            "capabilities": ["send_message", "post_update"],
            "description": "Send messages and post updates via Facebook"
        },
        "twitter": {
            "url": "https://twitter.com",
            "capabilities": ["post_update", "send_dm"],
            "description": "Post updates and send direct messages via Twitter/X"
        },
        "linkedin": {
            "url": "https://www.linkedin.com",
            "capabilities": ["send_message", "post_update"],
            "description": "Send messages and post updates via LinkedIn"
        },
        "zoom": {
            "url": "https://zoom.us",
            "capabilities": ["schedule_meeting", "join_meeting"],
            "description": "Schedule and join meetings via Zoom"
        },
        "teams": {
            "url": "https://teams.microsoft.com",
            "capabilities": ["send_message", "schedule_meeting", "join_meeting", "start_call"],
            "description": "Send messages, schedule meetings, and make calls via Microsoft Teams"
        },
        "meet": {
            "url": "https://meet.google.com",
            "capabilities": ["schedule_meeting", "join_meeting"],
            "description": "Schedule and join meetings via Google Meet"
        }
    }

    for service, info in services.items():
        print(f"\n🌐 {service.upper()}")
        print(f"   URL: {info['url']}")
        print(f"   Capabilities: {', '.join(info['capabilities'])}")
        print(f"   Description: {info['description']}")

def demo_api_endpoints():
    """Show the new API endpoints for service integration."""
    print("\n🔗 New API Endpoints for Service Integration")
    print("=" * 50)

    endpoints = [
        {
            "method": "POST",
            "path": "/browsers/create",
            "description": "Create a persistent browser with saved sessions",
            "params": ["profile_name", "user_data_dir"]
        },
        {
            "method": "GET",
            "path": "/browsers/status",
            "description": "Get current browser status and profiles",
            "params": []
        },
        {
            "method": "POST",
            "path": "/browsers/cleanup",
            "description": "Force cleanup of all browser instances",
            "params": []
        },
        {
            "method": "POST",
            "path": "/service/check-login",
            "description": "Check if user is logged into a specific service",
            "params": ["service", "browser_id"]
        },
        {
            "method": "POST",
            "path": "/service/navigate",
            "description": "Navigate to a specific service",
            "params": ["service", "browser_id"]
        },
        {
            "method": "POST",
            "path": "/service/send-email",
            "description": "Send email via supported service",
            "params": ["service", "browser_id", "to", "subject", "body", "cc", "bcc"]
        },
        {
            "method": "POST",
            "path": "/service/start-call",
            "description": "Start a call via supported service",
            "params": ["service", "browser_id", "contact"]
        },
        {
            "method": "POST",
            "path": "/service/send-message",
            "description": "Send message via supported service",
            "params": ["service", "browser_id", "contact", "message"]
        }
    ]

    for endpoint in endpoints:
        print(f"\n{endpoint['method']} {endpoint['path']}")
        print(f"   Description: {endpoint['description']}")
        if endpoint['params']:
            print(f"   Parameters: {', '.join(endpoint['params'])}")

def main():
    """Run all demos."""
    print("🎯 Enhanced Elch Agent - Service Integration Demo")
    print("=" * 60)
    print("This demo shows the new browser-based service integration capabilities.")
    print("The agent can now use your existing browser sessions to:")
    print("• Send emails via Gmail/Outlook")
    print("• Make calls via Skype/Teams")
    print("• Send messages via various platforms")
    print("• Schedule meetings and more!")
    print()

    # Run demos
    demo_supported_services()
    demo_request_parsing()
    demo_browser_management()
    demo_service_handlers()
    demo_integration_workflow()
    demo_api_endpoints()

    print("\n" + "=" * 60)
    print("🎉 Demo Complete!")
    print("\n🚀 Key Features:")
    print("   • Intelligent request parsing")
    print("   • Persistent browser sessions")
    print("   • Service-specific handlers")
    print("   • Login state management")
    print("   • Seamless integration with existing agent")
    print("   • Support for 12+ popular services")
    print("\n💡 Try it out:")
    print("   POST /agent/run with: 'Send email to friend@example.com saying hello'")
    print("   The agent will handle browser management and email sending automatically!")

if __name__ == "__main__":
    main()

