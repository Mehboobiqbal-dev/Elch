#!/usr/bin/env python3
"""
Test the actual agent with Gmail requests to verify the fix
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock the required modules to avoid import issues during testing
class MockWebSocket:
    def __init__(self):
        pass

    async def send_json(self, data):
        print(f"WebSocket would send: {data}")

class MockConnection:
    def __init__(self):
        self.websocket = MockWebSocket()

# Mock the active_connections
active_connections = {}

# Import the agent function
from main import agent_run
from schemas import AgentStateRequest

async def test_agent_gmail():
    """Test the agent with Gmail requests."""
    print("Testing Agent with Gmail Requests")
    print("=" * 50)

    test_requests = [
        "send gmail to john@example.com",
        "send email to john@example.com",
        "gmail to john@example.com"
    ]

    for request in test_requests:
        print(f"\n🧪 Testing: '{request}'")
        print("-" * 30)

        try:
            # Create mock request
            agent_req = AgentStateRequest(
                user_input=request,
                run_id=f"test_run_{hash(request)}"
            )

            # Mock the request object
            class MockRequest:
                pass

            # Call the agent (this will test the parsing and classification)
            result = await agent_run(MockRequest(), agent_req, None, None)

            print(f"✅ Agent Response: {result.message}")
            print(f"   Status: {result.status}")

            if result.status == "error" and "Could not identify the action" in result.message:
                print(f"❌ FAILED: Still getting the original error")
                return False
            else:
                print(f"✅ SUCCESS: No more 'Could not identify the action' error")

        except Exception as e:
            print(f"❌ Exception: {e}")
            import traceback
            traceback.print_exc()
            return False

    print(f"\n🎉 All Gmail requests processed successfully!")
    print("✅ The original 'Could not identify the action you want to perform on gmail' issue is FIXED!")
    return True

if __name__ == "__main__":
    import asyncio
    success = asyncio.run(test_agent_gmail())
    sys.exit(0 if success else 1)

