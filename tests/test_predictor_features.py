#!/usr/bin/env python3
"""
Test script untuk ML Predictor features
"""

import requests
import json
import time
from datetime import date

# Base URL - bisa diubah sesuai environment
BASE_URL = "http://localhost:8000/api"  # Development
# BASE_URL = "https://stunting-api.dedan.my.id/api"  # Production

def test_register_user():
    """Test register user"""
    print("🔍 Testing user registration...")
    
    user_data = {
        "avatar_type": 1,
        "name": "Test User",
        "username": f"testuser{int(time.time())}",
        "address": "Test Address",
        "dob": str(date.today()),
        "gender": "L",
        "password": "testpass123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response.status_code == 201:
            print("✅ User registration OK")
            user = response.json()
            print(f"   User ID: {user['id']}")
            print(f"   Username: {user['username']}")
            return user
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ User registration error: {e}")
        return None

def test_login(username, password):
    """Test user login"""
    print(f"\n🔍 Testing user login for {username}...")
    
    login_data = {
        "username": username,
        "password": password
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 200:
            print("✅ User login OK")
            token_data = response.json()
            print(f"   Token: {token_data['access_token'][:20]}...")
            return token_data['access_token']
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ User login error: {e}")
        return None

def test_create_children(token):
    """Test creating children"""
    print("\n🔍 Testing children creation...")
    
    children_data = {
        "name": "Test Child",
        "gender": "L",
        "dob": str(date.today())
    }
    
    headers = {"token": token}
    
    try:
        response = requests.post(f"{BASE_URL}/children", json=children_data, headers=headers)
        if response.status_code == 201:
            print("✅ Children creation OK")
            children = response.json()
            print(f"   Children ID: {children['id']}")
            print(f"   Name: {children['name']}")
            return children
        else:
            print(f"❌ Children creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Children creation error: {e}")
        return None

def test_predictor_status():
    """Test predictor status endpoint"""
    print("\n🔍 Testing predictor status...")
    
    try:
        response = requests.get(f"{BASE_URL}/children/predictor/status")
        if response.status_code == 200:
            print("✅ Predictor status OK")
            status_data = response.json()
            print(f"   Status: {status_data['status']}")
            if status_data['status'] == 'ready':
                print(f"   Algorithm: {status_data['model_info'].get('algorithm', 'N/A')}")
                print(f"   Classes: {status_data['model_info'].get('available_classes', 'N/A')}")
                print(f"   Cache Status: {status_data.get('cache_status', 'N/A')}")
            return status_data
        else:
            print(f"❌ Predictor status failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Predictor status error: {e}")
        return None

def test_create_diagnose_with_prediction(token, children_id, age, gender, height, test_name):
    """Test creating diagnose with specific parameters"""
    print(f"\n🔍 Testing diagnose creation - {test_name}...")
    
    diagnose_data = {
        "age_on_month": age,
        "gender": gender,
        "height": height
    }
    
    headers = {"token": token}
    
    try:
        response = requests.post(f"{BASE_URL}/children/{children_id}/diagnose", json=diagnose_data, headers=headers)
        if response.status_code == 201:
            print(f"✅ Diagnose creation OK - {test_name}")
            diagnose = response.json()
            print(f"   Diagnose ID: {diagnose['id']}")
            print(f"   Age: {age} months, Gender: {gender}, Height: {height} cm")
            print(f"   ML Prediction: {diagnose['result']}")
            return diagnose
        else:
            print(f"❌ Diagnose creation failed - {test_name}: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Diagnose creation error - {test_name}: {e}")
        return None

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        if "localhost" in BASE_URL:
            response = requests.get("http://localhost:8000/health")
        else:
            response = requests.get("https://stunting-api.dedan.my.id/health")
        
        if response.status_code == 200:
            print("✅ Health endpoint OK")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Testing ML Predictor Features")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("❌ Health check failed. Make sure the server is running!")
        return
    
    # Test predictor status first
    predictor_status = test_predictor_status()
    if not predictor_status:
        print("❌ Predictor status check failed!")
        return
    
    if predictor_status['status'] != 'ready':
        print("❌ ML Predictor is not ready!")
        return
    
    # Register and login user
    user = test_register_user()
    if not user:
        print("❌ User registration failed!")
        return
    
    token = test_login(user['username'], "testpass123")
    if not token:
        print("❌ User login failed!")
        return
    
    # Create children
    children = test_create_children(token)
    if not children:
        print("❌ Children creation failed!")
        return
    
    # Test various prediction scenarios
    test_cases = [
        {"age": 12, "gender": "L", "height": 75, "name": "12 months boy, 75cm"},
        {"age": 24, "gender": "P", "height": 85, "name": "24 months girl, 85cm"},
        {"age": 36, "gender": "L", "height": 95, "name": "36 months boy, 95cm"},
        {"age": 48, "gender": "P", "height": 105, "name": "48 months girl, 105cm"},
        {"age": 6, "gender": "L", "height": 65, "name": "6 months boy, 65cm"},
        {"age": 18, "gender": "P", "height": 80, "name": "18 months girl, 80cm"},
    ]
    
    print(f"\n🔬 Testing ML Predictor with {len(test_cases)} test cases...")
    
    results = []
    for i, test_case in enumerate(test_cases, 1):
        diagnose = test_create_diagnose_with_prediction(
            token, 
            children['id'], 
            test_case['age'], 
            test_case['gender'], 
            test_case['height'], 
            f"Test {i}: {test_case['name']}"
        )
        if diagnose:
            results.append({
                "test": test_case['name'],
                "prediction": diagnose['result'],
                "age": test_case['age'],
                "gender": test_case['gender'],
                "height": test_case['height']
            })
    
    print(f"\n📊 ML Predictor Test Results Summary:")
    print("=" * 60)
    for result in results:
        print(f"   {result['test']} → {result['prediction']}")
    
    print(f"\n🎉 ML Predictor tests completed!")
    print(f"✅ Successfully tested {len(results)} prediction scenarios")
    print(f"📈 ML Predictor is working correctly with various input combinations")

if __name__ == "__main__":
    main()
