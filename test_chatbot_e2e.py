#!/usr/bin/env python3
"""
End-to-end test script for the AI-Powered Todo Chatbot
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Test the health endpoint"""
    print("Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    print("[PASS] Health endpoint is working")

def test_signup():
    """Test user signup"""
    print("Testing user signup...")
    signup_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    response = requests.post(f"{BASE_URL}/api/v1/auth/signup", json=signup_data)
    assert response.status_code == 201
    result = response.json()
    assert "access_token" in result
    assert "user" in result
    print("[PASS] User signup successful")
    return result["access_token"], result["user"]["id"]

def test_chat_functionality(access_token, user_id):
    """Test the AI chat functionality"""
    print("Testing chat functionality...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Create a new task via chat
    chat_data = {
        "message": "Add a task to buy groceries"
    }
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    assert "conversation_id" in result
    print(f"[PASS] Chat response received: {result['response'][:50]}...")

    conversation_id = result["conversation_id"]

    # Test 2: Ask to list tasks
    chat_data = {
        "conversation_id": conversation_id,
        "message": "What tasks do I have?"
    }
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    print(f"[PASS] Chat response for listing tasks: {result['response'][:50]}...")

    # Test 3: Complete a task via chat
    chat_data = {
        "conversation_id": conversation_id,
        "message": "Complete the grocery task"
    }
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    print(f"[PASS] Chat response for completing task: {result['response'][:50]}...")

    return conversation_id

def test_conversation_persistence(access_token, user_id, conversation_id):
    """Test that conversation persists between requests"""
    print("Testing conversation persistence...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Ask about the previous conversation
    chat_data = {
        "conversation_id": conversation_id,
        "message": "What did we talk about?"
    }
    response = requests.post(f"{BASE_URL}/api/{user_id}/chat", json=chat_data, headers=headers)
    assert response.status_code == 200
    result = response.json()
    assert "response" in result
    print(f"[PASS] Conversation persistence confirmed: {result['response'][:50]}...")

def run_tests():
    """Run all end-to-end tests"""
    print("Starting end-to-end tests for AI-Powered Todo Chatbot...\n")
    
    try:
        # Test 1: Health check
        test_health()
        print()
        
        # Test 2: Signup
        access_token, user_id = test_signup()
        print()
        
        # Test 3: Chat functionality
        conversation_id = test_chat_functionality(access_token, user_id)
        print()
        
        # Test 4: Conversation persistence
        test_conversation_persistence(access_token, user_id, conversation_id)
        print()
        
        print("[PASS] All end-to-end tests passed successfully!")

    except Exception as e:
        print(f"[FAIL] Test failed with error: {str(e)}")
        raise

if __name__ == "__main__":
    run_tests()