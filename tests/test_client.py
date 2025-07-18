import requests
import json

# API base URL
BASE_URL = "http://localhost:8001"

def test_health_endpoint():
    """Test the health check endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def test_chat_endpoint(message):
    """Test the chat endpoint"""
    print(f"Testing chat with message: '{message}'")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": message}
    )
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Response: {data['response']}")
        if data.get('sources'):
            print(f"Sources: {len(data['sources'])} found")
    else:
        print(f"Error: {response.text}")
    print("-" * 50)

def test_non_gym_question():
    """Test with a non-gym related question"""
    print("Testing non-gym question...")
    response = requests.post(
        f"{BASE_URL}/chat",
        json={"message": "What's the weather like today?"}
    )
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()['response']}")
    print("-" * 50)

def test_reset_endpoint():
    """Test the reset endpoint"""
    print("Testing reset endpoint...")
    response = requests.post(f"{BASE_URL}/reset")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("-" * 50)

def main():
    """Run all tests"""
    print("=== Gym Pro API Test Client ===\n")
    
    # Test basic endpoints
    test_health_endpoint()
    
    # Test chat with gym-related questions
    gym_questions = [
        "What are the best exercises for chest?",
        "How do I perform a proper squat?",
        "What should I eat for muscle building?",
        "How often should I do cardio?",
        "What's a good beginner workout routine?"
    ]
    
    for question in gym_questions:
        test_chat_endpoint(question)
    
    # Test non-gym question
    test_non_gym_question()
    
    # Test reset
    test_reset_endpoint()

if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the API server.")
        print("Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"Error: {e}")
