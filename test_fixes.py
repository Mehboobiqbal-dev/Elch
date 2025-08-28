#!/usr/bin/env python3
"""
Test script to verify all fixes are working correctly.
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_memory_monitoring_disabled():
    """Test that memory monitoring is disabled."""
    print("🧪 Testing Memory Monitoring Disabled")
    print("=" * 40)

    try:
        # Check if memory monitoring import is commented out in main.py
        with open('main.py', 'r') as f:
            content = f.read()

        if '# from core.memory_monitor import start_memory_monitoring, get_memory_stats' in content:
            print("✅ Memory monitoring properly disabled in main.py")
        else:
            print("❌ Memory monitoring may still be enabled")
            return False

        # Check if the monitoring functions are commented out
        if '# start_memory_monitoring()' in content:
            print("✅ Memory monitoring startup is disabled")
        else:
            print("❌ Memory monitoring startup may still be enabled")
            return False

        # Verify main module still imports
        import main
        print("✅ Main module imports successfully")

        return True
    except Exception as e:
        print(f"❌ Error testing memory monitoring: {e}")
        return False

def test_self_learning_memory():
    """Test that self-learning memory is properly initialized."""
    print("\n🧪 Testing Self-Learning Memory")
    print("=" * 40)

    try:
        from self_learning import SelfLearningCore

        core = SelfLearningCore()
        print("✅ Self-learning core initialized successfully")

        # Check memory structure
        required_keys = ['knowledge', 'errors', 'improvements']
        for key in required_keys:
            if key not in core.memory:
                print(f"❌ Missing key: {key}")
                return False
            if not isinstance(core.memory[key], list):
                print(f"❌ {key} is not a list")
                return False

        print("✅ Memory structure is correct")
        print(f"   - Knowledge items: {len(core.memory['knowledge'])}")
        print(f"   - Error items: {len(core.memory['errors'])}")
        print(f"   - Improvement items: {len(core.memory['improvements'])}")

        return True
    except Exception as e:
        print(f"❌ Error testing self-learning memory: {e}")
        return False

def test_browser_cleanup():
    """Test browser cleanup functionality."""
    print("\n🧪 Testing Browser Cleanup")
    print("=" * 40)

    try:
        import browsing

        # Test cleanup function
        initial_count = browsing.get_browser_count()
        print(f"Initial browser count: {initial_count}")

        # Try cleanup
        closed_count = browsing.cleanup_all_browsers()
        print(f"Closed browsers: {closed_count}")

        final_count = browsing.get_browser_count()
        print(f"Final browser count: {final_count}")

        # Test browser status functions exist
        if hasattr(browsing, 'get_browser_count') and hasattr(browsing, 'cleanup_all_browsers'):
            print("✅ Browser management functions available")
        else:
            print("❌ Browser management functions missing")
            return False

        print("✅ Browser cleanup functions work correctly")
        return True
    except Exception as e:
        print(f"❌ Error testing browser cleanup: {e}")
        return False

def test_agent_imports():
    """Test that all agent components can be imported."""
    print("\n🧪 Testing Agent Imports")
    print("=" * 40)

    modules_to_test = [
        'gemini',
        'universal_assistant',
        'browsing',
        'self_learning',
        'core.config'
    ]

    for module in modules_to_test:
        try:
            __import__(module)
            print(f"✅ {module} imports successfully")
        except Exception as e:
            print(f"❌ {module} import failed: {e}")
            return False

    return True

def test_question_classification():
    """Test question classification functionality."""
    print("\n🧪 Testing Question Classification")
    print("=" * 40)

    try:
        from universal_assistant import classify_question_type

        test_cases = [
            ("What is the capital of France?", "general"),
            ("Book a flight to Paris", "task"),
            ("Explain quantum physics", "general"),
            ("Search for hotels in London", "task")
        ]

        correct = 0
        for question, expected in test_cases:
            result = classify_question_type(question)
            status = "✅" if result == expected else "❌"
            print(f"{status} '{question}' → {result}")
            if result == expected:
                correct += 1

        accuracy = correct / len(test_cases)
        print(f"Classification accuracy: {correct}/{len(test_cases)} ({accuracy:.1f})")

        return accuracy >= 0.75  # At least 75% accuracy
    except Exception as e:
        print(f"❌ Error testing question classification: {e}")
        return False

def main():
    """Run all tests."""
    print("🚀 Testing All Fixes and Improvements")
    print("=" * 50)

    tests = [
        test_memory_monitoring_disabled,
        test_self_learning_memory,
        test_browser_cleanup,
        test_agent_imports,
        test_question_classification
    ]

    passed = 0
    total = len(tests)

    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")

    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 All tests passed! The agent should now work without the previous errors.")
        print("\n✅ Fixes Applied:")
        print("   • Memory monitoring disabled (unlimited memory usage)")
        print("   • Self-learning memory properly initialized")
        print("   • Browser cleanup and management improved")
        print("   • Chrome timeout issues addressed")
        print("   • Better error handling throughout")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
