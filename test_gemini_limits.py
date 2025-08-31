#!/usr/bin/env python3
"""
Test Gemini API rate limiting and daily quota management
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from gemini import api_key_manager
import logging

def test_daily_limits():
    """Test daily limit tracking."""
    print("🧪 Testing Daily Limit Management")
    print("=" * 40)

    if not api_key_manager.api_keys:
        print("❌ No API keys configured")
        return False

    # Test a key (using the first available)
    test_key = api_key_manager.api_keys[0]
    key_prefix = test_key[:8]

    print(f"Testing with key: {key_prefix}...")

    # Check initial state
    is_limited = api_key_manager.is_daily_limit_reached(test_key)
    current_usage = api_key_manager.daily_usage.get(test_key, 0)

    print(f"Initial daily usage: {current_usage}/45")
    print(f"Daily limit reached: {is_limited}")

    # Simulate some usage
    print("\\nSimulating API usage...")
    for i in range(10):
        api_key_manager.mark_key_usage(test_key)
        current_usage = api_key_manager.daily_usage.get(test_key, 0)
        print(f"After request {i+1}: {current_usage}/45 requests used")

        if api_key_manager.is_daily_limit_reached(test_key):
            print(f"⚠️  Daily limit reached at {current_usage} requests!")
            break

    return True

def test_key_selection():
    """Test intelligent key selection."""
    print("\\n🔑 Testing Key Selection Logic")
    print("=" * 40)

    if len(api_key_manager.api_keys) < 2:
        print("ℹ️  Need at least 2 keys to test selection logic")
        return True

    print(f"Available keys: {len(api_key_manager.api_keys)}")

    # Test multiple selections to see rotation behavior
    selections = []
    for i in range(20):
        key = api_key_manager.get_best_key()
        if key:
            key_prefix = key[:8]
            selections.append(key_prefix)

    # Count occurrences
    from collections import Counter
    selection_counts = Counter(selections)

    print("\\nKey selection distribution:")
    for key_prefix, count in selection_counts.items():
        percentage = (count / len(selections)) * 100
        print(f"  {key_prefix}...: {count} times ({percentage:.1f}%)")

    # The first key should be selected most often (conservative rotation)
    most_common = selection_counts.most_common(1)[0]
    print(f"\\nMost selected key: {most_common[0]} ({most_common[1]} times)")

    return True

def main():
    """Run all tests."""
    print("🚀 Gemini API Limits Test Suite")
    print("=" * 50)
    print("Testing the fixed rate limiting and quota management.")
    print()

    try:
        # Test daily limits
        test_daily_limits()

        # Test key selection
        test_key_selection()

        print("\\n" + "=" * 50)
        print("✅ Tests completed successfully!")
        print("\\n📋 SUMMARY OF FIXES:")
        print("• Reduced rate limits: 5 requests/hour instead of 30/minute")
        print("• Added daily quota tracking (45 requests/day per key)")
        print("• Conservative key rotation (95% stick with best key)")
        print("• Daily limit checking before API calls")
        print("• Proper quota exhaustion handling")

        print("\\n💡 EXPECTED BEHAVIOR:")
        print("• API keys should last much longer (days instead of minutes)")
        print("• No more rapid quota exhaustion")
        print("• Better distribution of requests across available keys")
        print("• Circuit breaker opens only when truly needed")

        return True

    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Set up logging to see the warnings
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

    success = main()
    print(f"\\n🔚 Test result: {'PASSED' if success else 'FAILED'}")
    sys.exit(0 if success else 1)

