#!/usr/bin/env python3
"""
Demo script showing the enhanced Elch agent with general question answering capabilities.
"""

import os
import sys

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from universal_assistant import classify_question_type, answer_general_question

def demo_interactive():
    """Interactive demo of the enhanced agent."""
    print("🎯 Enhanced Elch Agent - General Question Answering Demo")
    print("=" * 60)
    print("Ask me anything! I can answer general questions or help with tasks.")
    print("Type 'quit' to exit.\n")

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("👋 Goodbye! Thanks for trying the enhanced Elch agent.")
                break

            if not user_input:
                continue

            # Classify the question
            print("🤔 Classifying your input...")
            question_type = classify_question_type(user_input)
            print(f"📋 Type: {question_type.upper()}")

            if question_type == 'general':
                print("💭 This looks like a general question. Let me answer it...")
                print("-" * 50)

                # Get answer
                answer = answer_general_question(user_input)
                print(f"🤖 Elch: {answer}")

            else:
                print("🔧 This appears to be a task that requires tools/browser automation.")
                print("🤖 Elch: I can help you with this task using my automation capabilities!")
                print("   (In a full deployment, I would now execute the appropriate tools)")

            print("\n" + "=" * 60)

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Sorry, I encountered an error: {e}")
            print("Please try again.\n")

def demo_examples():
    """Show example interactions."""
    print("🎯 Enhanced Elch Agent - Example Interactions")
    print("=" * 60)

    examples = [
        ("What is the largest planet in our solar system?", "general"),
        ("Book a flight to Tokyo", "task"),
        ("Explain how vaccines work", "general"),
        ("Find me a good coffee shop nearby", "task"),
        ("What are the benefits of renewable energy?", "general"),
        ("Fill out this online application form", "task"),
    ]

    for question, expected_type in examples:
        print(f"\n❓ Question: {question}")
        print(f"📋 Expected Type: {expected_type.upper()}")

        # Classify
        actual_type = classify_question_type(question)
        status = "✅" if actual_type == expected_type else "❌"
        print(f"🤖 Classified as: {actual_type.upper()} {status}")

        # Answer if general
        if actual_type == 'general':
            answer = answer_general_question(question)
            print(f"💬 Answer: {answer[:150]}{'...' if len(answer) > 150 else ''}")

        print("-" * 40)

def main():
    """Main demo function."""
    print("🚀 Enhanced Elch Agent Demo")
    print("Choose an option:")
    print("1. Interactive mode (ask me anything)")
    print("2. Example demonstrations")
    print("3. Exit")

    while True:
        try:
            choice = input("\nEnter your choice (1-3): ").strip()

            if choice == '1':
                demo_interactive()
                break
            elif choice == '2':
                demo_examples()
                input("\nPress Enter to return to menu...")
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("❌ Please enter 1, 2, or 3.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
