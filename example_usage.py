"""
Example usage of the DSA Assistant
"""

from dsa_assistant import DSAAssistant

def run_examples():
    """Run example questions"""
    
    # Initialize the assistant
    print("Initializing DSA Assistant...")
    assistant = DSAAssistant()
    
    # Example questions
    questions = [
        "What is an array and how does it work?",
        "How do I reverse a linked list?",
        "What is the difference between a stack and a queue?",
        "Explain binary search in simple terms",
        "What is Big O notation?",
        "How does bubble sort work?",
        "What is recursion?",
    ]
    
    print("\n" + "="*70)
    print("Running Example Questions")
    print("="*70)
    
    for i, question in enumerate(questions, 1):
        print(f"\n{'='*70}")
        print(f"Example {i}/{len(questions)}")
        print(f"{'='*70}")
        
        assistant.ask(question)
        
        if i < len(questions):
            input("\nPress Enter to continue to next question...")


if __name__ == "__main__":
    run_examples()
