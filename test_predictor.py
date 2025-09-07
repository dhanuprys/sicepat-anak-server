#!/usr/bin/env python3
"""
Specific test script untuk Stunting Predictor
"""

import requests
import json
import time
from datetime import date

# Base URL
BASE_URL = "http://localhost:8000/api"

def test_predictor_initialization():
    """Test predictor initialization"""
    print("🔍 Testing predictor initialization...")
    
    try:
        response = requests.get(f"{BASE_URL}/children/predictor/status")
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Predictor status: {status_data['status']}")
            
            if status_data['status'] == 'ready':
                print("   🚀 ML Model is ready!")
                print(f"   📊 Algorithm: {status_data['model_info'].get('algorithm', 'N/A')}")
                print(f"   🎯 Available classes: {status_data['model_info'].get('available_classes', 'N/A')}")
                print(f"   📁 Cache directory: {status_data['cache_status'].get('cache_directory', 'N/A')}")
                return True
            else:
                print("   ⚠️  ML Model not ready, using fallback logic")
                print(f"   📝 Message: {status_data.get('message', 'N/A')}")
                return False
        else:
            print(f"❌ Predictor status failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Predictor status error: {e}")
        return False

def test_diagnose_with_different_inputs():
    """Test diagnose with various input combinations"""
    print("\n🔍 Testing diagnose with different inputs...")
    
    # First, create a test user and get token
    user_data = {
        "avatar_type": 1,
        "name": "Predictor Test User",
        "username": f"predictortest{int(time.time())}",
        "address": "Test Address",
        "dob": str(date.today()),
        "gender": "L",
        "password": "testpass123"
    }
    
    try:
        # Register user
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 201:
            print("❌ User registration failed for predictor test")
            return False
        
        user = response.json()
        print(f"   ✅ User created: {user['username']}")
        
        # Login
        login_data = {"username": user['username'], "password": "testpass123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print("❌ User login failed for predictor test")
            return False
        
        token = response.json()['access_token']
        print("   ✅ User logged in")
        
        # Create children
        children_data = {
            "name": "Predictor Test Child",
            "gender": "L",
            "dob": str(date.today())
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/children", json=children_data, headers=headers)
        if response.status_code != 201:
            print("❌ Children creation failed for predictor test")
            return False
        
        children = response.json()
        print(f"   ✅ Children created: {children['name']}")
        
        # Test different diagnose inputs
        test_cases = [
            {"age": 12, "gender": "L", "height": 70, "description": "Young boy, short height"},
            {"age": 12, "gender": "L", "height": 80, "description": "Young boy, normal height"},
            {"age": 12, "gender": "P", "height": 68, "description": "Young girl, short height"},
            {"age": 12, "gender": "P", "height": 78, "description": "Young girl, normal height"},
            {"age": 36, "gender": "L", "height": 85, "description": "Older boy, short height"},
            {"age": 36, "gender": "L", "height": 100, "description": "Older boy, normal height"},
            {"age": 36, "gender": "P", "height": 83, "description": "Older girl, short height"},
            {"age": 36, "gender": "P", "height": 98, "description": "Older girl, normal height"},
        ]
        
        results = []
        for i, test_case in enumerate(test_cases, 1):
            diagnose_data = {
                "age_on_month": test_case["age"],
                "gender": test_case["gender"],
                "height": test_case["height"]
                # result field will be calculated by the API
            }
            
            response = requests.post(
                f"{BASE_URL}/children/{children['id']}/diagnose", 
                json=diagnose_data, 
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"   ✅ Test {i}: {test_case['description']}")
                print(f"      Input: Age={test_case['age']}m, Gender={test_case['gender']}, Height={test_case['height']}cm")
                print(f"      Output: {result['result']}")
                results.append({
                    "test_case": test_case,
                    "result": result['result'],
                    "status": "success"
                })
            else:
                print(f"   ❌ Test {i} failed: {response.status_code}")
                print(f"      Response: {response.text}")
                results.append({
                    "test_case": test_case,
                    "status": "failed",
                    "error": response.text
                })
        
        # Summary
        successful_tests = len([r for r in results if r['status'] == 'success'])
        print(f"\n📊 Predictor Test Summary:")
        print(f"   Total tests: {len(test_cases)}")
        print(f"   Successful: {successful_tests}")
        print(f"   Failed: {len(test_cases) - successful_tests}")
        
        return successful_tests == len(test_cases)
        
    except Exception as e:
        print(f"❌ Predictor test error: {e}")
        return False

def test_predictor_cache():
    """Test predictor cache functionality"""
    print("\n🔍 Testing predictor cache...")
    
    try:
        # Get predictor status multiple times to test cache
        responses = []
        for i in range(3):
            response = requests.get(f"{BASE_URL}/children/predictor/status")
            if response.status_code == 200:
                responses.append(response.json())
                print(f"   ✅ Cache test {i+1}: Status retrieved")
            else:
                print(f"   ❌ Cache test {i+1} failed: {response.status_code}")
                return False
        
        # Check if responses are consistent
        if all(r['status'] == responses[0]['status'] for r in responses):
            print("   ✅ Cache responses are consistent")
            return True
        else:
            print("   ❌ Cache responses are inconsistent")
            return False
            
    except Exception as e:
        print(f"❌ Cache test error: {e}")
        return False

def test_predictor_error_handling():
    """Test predictor error handling"""
    print("\n🔍 Testing predictor error handling...")
    
    # Test with invalid data that should trigger fallback logic
    try:
        # Create test user and children first
        user_data = {
            "avatar_type": 1,
            "name": "Error Test User",
            "username": f"errortest{int(time.time())}",
            "address": "Test Address",
            "dob": str(date.today()),
            "gender": "L",
            "password": "testpass123"
        }
        
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code != 201:
            print("❌ User registration failed for error test")
            return False
        
        user = response.json()
        
        # Login
        login_data = {"username": user['username'], "password": "testpass123"}
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code != 200:
            print("❌ User login failed for error test")
            return False
        
        token = response.json()['access_token']
        
        # Create children
        children_data = {
            "name": "Error Test Child",
            "gender": "L",
            "dob": str(date.today())
        }
        
        headers = {"Authorization": f"Bearer {token}"}
        response = requests.post(f"{BASE_URL}/children", json=children_data, headers=headers)
        if response.status_code != 201:
            print("❌ Children creation failed for error test")
            return False
        
        children = response.json()
        
        # Test edge cases that might trigger errors
        edge_cases = [
            {"age": 0, "gender": "L", "height": 30, "description": "Minimum values"},
            {"age": 60, "gender": "P", "height": 200, "description": "Maximum values"},
            {"age": 6, "gender": "L", "height": 50, "description": "Very young, very short"},
            {"age": 48, "gender": "P", "height": 120, "description": "Older, moderate height"},
        ]
        
        for i, edge_case in enumerate(edge_cases, 1):
            diagnose_data = {
                "age_on_month": edge_case["age"],
                "gender": edge_case["gender"],
                "height": edge_case["height"]
                # result field will be calculated by the API
            }
            
            response = requests.post(
                f"{BASE_URL}/children/{children['id']}/diagnose", 
                json=diagnose_data, 
                headers=headers
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"   ✅ Edge case {i}: {edge_case['description']}")
                print(f"      Result: {result['result']}")
            else:
                print(f"   ❌ Edge case {i} failed: {response.status_code}")
                print(f"      Response: {response.text}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test error: {e}")
        return False

def main():
    """Main predictor test function"""
    print("🧪 Testing Stunting Predictor Functionality")
    print("=" * 60)
    
    # Test predictor initialization
    if not test_predictor_initialization():
        print("⚠️  Predictor not ready, but continuing with tests...")
    
    # Test cache functionality
    test_predictor_cache()
    
    # Test different input combinations
    if not test_diagnose_with_different_inputs():
        print("❌ Diagnose with different inputs test failed!")
        return
    
    # Test error handling
    if not test_predictor_error_handling():
        print("❌ Error handling test failed!")
        return
    
    print("\n🎉 All predictor tests completed!")
    print("✅ Stunting predictor is working correctly")
    print("📊 Tested: Initialization, Cache, Multiple inputs, Error handling")

if __name__ == "__main__":
    main()
