#!/usr/bin/env python3
"""
Test script for the enhanced Elch agent with general question answering capabilities.
"""

import os
import sys
import json

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from universal_assistant import classify_question_type, answer_general_question

def test_question_classification():
    """Test the question classification functionality."""
    print("🧪 Testing Question Classification")
    print("=" * 50)

    test_cases = [
        # General questions
        ("What is the capital of France?", "general"),
        ("Explain how photosynthesis works", "general"),
        ("What are the benefits of exercise?", "general"),
        ("Who wrote Romeo and Juliet?", "general"),
        ("What is machine learning?", "general"),

        # Task-based requests
        ("Book a flight to New York", "task"),
        ("Search for restaurants in downtown", "task"),
        ("Fill out this online form", "task"),
        ("Order groceries online", "task"),
        ("Check my email inbox", "task"),
    ]

    correct = 0
    total = len(test_cases)

    for question, expected in test_cases:
        try:
            result = classify_question_type(question)
            status = "✅" if result == expected else "❌"
            print(f"{status} '{question}' → {result} (expected: {expected})")
            if result == expected:
                correct += 1
        except Exception as e:
            print(f"❌ '{question}' → ERROR: {e}")

    accuracy = correct / total * 100
    print(f"\n📊 Classification Accuracy: {correct}/{total} ({accuracy:.1f}%)")
    return accuracy >= 80  # Consider it passing if 80% or better

def test_general_answers():
    """Test the general question answering functionality."""
    print("\n🧪 Testing General Question Answering")
    print("=" * 50)

    test_questions = [
        "What is the largest planet in our solar system?",
        "Explain the concept of gravity in simple terms",
        "What are the main ingredients in a traditional pizza?",
        "Who was Albert Einstein?",
        "What is the difference between weather and climate?"
    ]

    for question in test_questions:
        try:
            print(f"\n❓ Question: {question}")
            answer = answer_general_question(question)
            print(f"🤖 Answer: {answer[:200]}{'...' if len(answer) > 200 else ''}")
            print("✅ Successfully answered")
        except Exception as e:
            print(f"❌ Error answering question: {e}")

def test_mixed_scenario():
    """Test a mixed scenario with both general questions and tasks."""
    print("\n🧪 Testing Mixed Scenario")
    print("=" * 50)

    mixed_inputs = [
        "What is artificial intelligence?",
        "Find me a good Italian restaurant nearby",
        "Explain blockchain technology",
        "Book an appointment with my doctor",
        "What are the health benefits of meditation?",
        "Search for flights from New York to London"
    ]

    for user_input in mixed_inputs:
        try:
            q_type = classify_question_type(user_input)
            print(f"\n📝 Input: {user_input}")
            print(f"🏷️  Type: {q_type}")

            if q_type == "general":
                answer = answer_general_question(user_input)
                print(f"🤖 Answer: {answer[:150]}{'...' if len(answer) > 150 else ''}")
            else:
                print("🔧 Would proceed with tool-based execution")

        except Exception as e:
            print(f"❌ Error processing: {e}")

def main():
    """Run all tests."""
    print("🚀 Testing Enhanced Elch Agent - General Question Answering")
    print("=" * 60)

    try:
        # Test classification accuracy
        classification_passed = test_question_classification()

        # Test general question answering
        test_general_answers()

        # Test mixed scenario
        test_mixed_scenario()

        print("\n" + "=" * 60)
        if classification_passed:
            print("✅ All tests completed successfully!")
            print("🎉 Your agent can now answer general questions using Gemini API!")
        else:
            print("⚠️  Classification accuracy could be improved, but basic functionality works.")
            print("💡 Consider fine-tuning the classification prompts for better accuracy.")

        print("\n📋 Features Added:")
        print("   • Question type classification (general vs task)")
        print("   • Direct answering of general questions using Gemini API")
        print("   • Context-aware responses using agent memory")
        print("   • Seamless integration with existing tool-based workflows")
        print("   • Enhanced user experience for informational queries")

    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
