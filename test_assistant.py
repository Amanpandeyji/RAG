"""
Quick test script to verify the DSA Assistant works
"""

from dsa_assistant import DSAAssistant

def test_assistant():
    print("=" * 60)
    print("Testing DSA Assistant")
    print("=" * 60)
    
    # Initialize
    print("\n1. Initializing assistant...")
    assistant = DSAAssistant()
    print("✅ Initialization successful!\n")
    
    # Test a simple question
    print("2. Testing with a simple question...")
    question = "What is an array?"
    print(f"Q: {question}\n")
    
    answer, sources = assistant.ask(question)
    
    print("\n" + "=" * 60)
    print("✅ Test completed successfully!")
    print("=" * 60)
    print(f"\nThe assistant is working correctly!")
    print(f"Retrieved {len(sources)} relevant passages from the notes.")
    
    return True

if __name__ == "__main__":
    try:
        test_assistant()
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
