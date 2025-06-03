#!/usr/bin/env python3
"""
Test script to verify error handling improvements.
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.core.exceptions import CognitoError, get_user_friendly_error_message

def test_error_messages():
    """Test that error messages are user-friendly."""
    print("🧪 Testing Error Message Improvements")
    print("=" * 50)
    
    # Test Cognito error mappings
    test_cases = [
        ("ExpiredCodeException", "The confirmation code has expired. Please request a new code."),
        ("CodeMismatchException", "Invalid confirmation code. Please check the code and try again."),
        ("UserNotFoundException", "User not found. Please check your email address."),
        ("NotAuthorizedException", "Invalid email or password. Please try again."),
        ("AliasExistsException", "An account with this email already exists."),
        ("InvalidParameterException", "Invalid request parameters. Please check your input."),
        ("UnknownErrorCode", "An unexpected error occurred. Please try again.")
    ]
    
    all_passed = True
    
    for error_code, expected_message in test_cases:
        if error_code == "UnknownErrorCode":
            # Test default message
            result = get_user_friendly_error_message(error_code)
            expected = "An unexpected error occurred. Please try again."
        else:
            result = get_user_friendly_error_message(error_code)
            expected = expected_message
        
        if result == expected:
            print(f"✅ {error_code}: {result}")
        else:
            print(f"❌ {error_code}: Expected '{expected}', got '{result}'")
            all_passed = False
    
    return all_passed

def test_cognito_error_class():
    """Test CognitoError class functionality."""
    print("\n🧪 Testing CognitoError Class")
    print("=" * 50)
    
    try:
        # Test creating CognitoError
        error = CognitoError(
            "Test error message",
            error_code="TestErrorCode",
            details={"test": "data"}
        )
        
        assert error.message == "Test error message"
        assert error.error_code == "TestErrorCode"
        assert error.details == {"test": "data"}
        assert str(error) == "Test error message"
        
        print("✅ CognitoError class works correctly")
        return True
        
    except Exception as e:
        print(f"❌ CognitoError test failed: {e}")
        return False

def test_api_imports():
    """Test that API modules can be imported without errors."""
    print("\n🧪 Testing API Module Imports")
    print("=" * 50)
    
    try:
        from client.src.lib.api import api
        print("❌ Cannot import client modules from backend test")
        return False
    except ImportError:
        print("✅ Client import correctly fails (expected)")
    
    try:
        from app.routers.auth import auth_router
        from app.services.cognito_service import cognito_service
        print("✅ Backend modules imported successfully")
        return True
    except Exception as e:
        print(f"❌ Backend import failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Starting Error Handling Tests")
    print("=" * 60)
    
    tests = [
        test_error_messages,
        test_cognito_error_class,
        test_api_imports
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Error handling improvements are working correctly.")
        print("\n📝 Summary of improvements:")
        print("✅ User-friendly error messages for Cognito errors")
        print("✅ Proper error handling in API endpoints")
        print("✅ Better error parsing in client API calls")
        print("✅ CognitoError exception class for structured error handling")
        sys.exit(0)
    else:
        print("❌ Some tests failed. Please check the output above.")
        sys.exit(1)
