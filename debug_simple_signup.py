#!/usr/bin/env python3
"""
Simple test to debug signup issue
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.models.user import UserCreate
from pydantic import ValidationError

def test_user_create_validation():
    """Test if UserCreate validation works correctly"""
    print("Testing UserCreate validation...")
    
    # Test valid data
    try:
        user_data = UserCreate(
            email="test@example.com",
            password="SecurePassword123!",
            name="Test User"
        )
        print(f"[OK] Valid user creation succeeded: {user_data.email}")
    except ValidationError as e:
        print(f"[ERROR] Valid user creation failed: {e}")
        return False
    
    # Test invalid email
    try:
        invalid_user = UserCreate(
            email="invalid-email",
            password="SecurePassword123!"
        )
        print(f"[ERROR] Invalid email should have failed but didn't: {invalid_user.email}")
        return False
    except ValidationError:
        print("[OK] Invalid email correctly rejected")
    
    # Test short password
    try:
        invalid_user = UserCreate(
            email="test2@example.com",
            password="short"
        )
        print(f"[ERROR] Short password should have failed but didn't: {invalid_user.password}")
        return False
    except ValidationError:
        print("[OK] Short password correctly rejected")
    
    return True

if __name__ == "__main__":
    success = test_user_create_validation()
    if success:
        print("\n[OK] All validation tests passed!")
    else:
        print("\n[ERROR] Some validation tests failed!")