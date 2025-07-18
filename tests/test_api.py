"""
Test suite for the GymPro RAG Chatbot API
"""
import requests
import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

BASE_URL = "http://localhost:8001"

class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    END = '\033[0m'
    BOLD = '\033[1m'

def print_colored(text: str, color: str):
    """Print colored text to terminal"""
    print(f"{color}{text}{Colors.END}")

def test_health_endpoint():
    """Test the health endpoint"""
    try:
        print_colored("🏥 Testing Health Endpoint", Colors.BLUE + Colors.BOLD)
        response = requests.get(f"{BASE_URL}/")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_colored(f"✅ Health check passed", Colors.GREEN)
            print(f"RAG Enabled: {data.get('rag_enabled')}")
            print(f"Status: {data.get('status')}")
        else:
            print_colored(f"❌ Health check failed", Colors.RED)
            print(f"Response: {response.text}")
        
        print("-" * 60)
        return response.status_code == 200
        
    except Exception as e:
        print_colored(f"❌ Health check failed: {e}", Colors.RED)
        print("-" * 60)
        return False

def test_detailed_health():
    """Test the detailed health endpoint"""
    try:
        print_colored("🔍 Testing Detailed Health Endpoint", Colors.BLUE + Colors.BOLD)
        response = requests.get(f"{BASE_URL}/health")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_colored(f"✅ Detailed health check passed", Colors.GREEN)
            print(json.dumps(data, indent=2))
        else:
            print_colored(f"❌ Detailed health check failed", Colors.RED)
            print(f"Response: {response.text}")
        
        print("-" * 60)
        return response.status_code == 200
        
    except Exception as e:
        print_colored(f"❌ Detailed health check failed: {e}", Colors.RED)
        print("-" * 60)
        return False

def test_chat_endpoint():
    """Test the chat endpoint with various questions"""
    test_cases = [
        {
            "question": "What's the proper form for squats?",
            "expected_gym_related": True,
            "description": "Basic exercise question"
        },
        {
            "question": "How much protein should I eat for muscle building?",
            "expected_gym_related": True,
            "description": "Nutrition question"
        },
        {
            "question": "What's the best workout routine for beginners?",
            "expected_gym_related": True,
            "description": "Workout planning question"
        },
        {
            "question": "Tell me about the weather today",
            "expected_gym_related": False,
            "description": "Non-gym related question (should be rejected)"
        },
        {
            "question": "How do I prevent injury while deadlifting?",
            "expected_gym_related": True,
            "description": "Safety question"
        }
    ]
    
    print_colored("💬 Testing Chat Endpoint", Colors.BLUE + Colors.BOLD)
    
    passed = 0
    total = len(test_cases)
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            print(f"\n{i}. {test_case['description']}")
            print_colored(f"Question: '{test_case['question']}'", Colors.CYAN)
            
            payload = {"message": test_case["question"]}
            response = requests.post(f"{BASE_URL}/chat", json=payload)
            
            if response.status_code == 200:
                data = response.json()
                gym_related = data.get('is_gym_related')
                response_text = data.get('response')
                sources = data.get('sources', [])
                
                # Check if gym_related matches expectation
                if gym_related == test_case['expected_gym_related']:
                    print_colored(f"✅ Correct categorization (gym_related: {gym_related})", Colors.GREEN)
                    passed += 1
                else:
                    print_colored(f"❌ Wrong categorization (expected: {test_case['expected_gym_related']}, got: {gym_related})", Colors.RED)
                
                print(f"Response length: {len(response_text)} characters")
                print(f"Sources found: {len(sources)}")
                print(f"Response preview: {response_text[:150]}...")
                
            else:
                print_colored(f"❌ HTTP Error {response.status_code}: {response.text}", Colors.RED)
                
        except Exception as e:
            print_colored(f"❌ Test failed: {e}", Colors.RED)
    
    print(f"\n{'-' * 60}")
    print_colored(f"Chat Tests: {passed}/{total} passed", 
                 Colors.GREEN if passed == total else Colors.YELLOW)
    print("-" * 60)
    
    return passed == total

def test_reset_endpoint():
    """Test the system reset endpoint"""
    try:
        print_colored("🔄 Testing Reset Endpoint", Colors.BLUE + Colors.BOLD)
        response = requests.post(f"{BASE_URL}/reset")
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print_colored(f"✅ Reset successful", Colors.GREEN)
            print(f"Status: {data.get('status')}")
            print(f"Message: {data.get('message')}")
        else:
            print_colored(f"❌ Reset failed", Colors.RED)
            print(f"Response: {response.text}")
        
        print("-" * 60)
        return response.status_code == 200
        
    except Exception as e:
        print_colored(f"❌ Reset test failed: {e}", Colors.RED)
        print("-" * 60)
        return False

def main():
    """Run all tests"""
    print_colored("🚀 GymPro RAG Chatbot API Test Suite", Colors.PURPLE + Colors.BOLD)
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_endpoint),
        ("Detailed Health", test_detailed_health),
        ("Chat Functionality", test_chat_endpoint),
        ("System Reset", test_reset_endpoint)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print_colored(f"❌ {test_name} failed with exception: {e}", Colors.RED)
    
    # Final results
    print("=" * 60)
    if passed == total:
        print_colored(f"🎉 All tests passed! ({passed}/{total})", Colors.GREEN + Colors.BOLD)
    else:
        print_colored(f"⚠️ Some tests failed. ({passed}/{total} passed)", Colors.YELLOW + Colors.BOLD)
    
    print_colored("\n💡 Tips:", Colors.CYAN)
    print("• Make sure the server is running on http://localhost:8000")
    print("• Check that your Google API key is properly configured")
    print("• Verify that gym_data.txt is in the data/ directory")

if __name__ == "__main__":
    main()
