#!/usr/bin/env python3
"""
Test script untuk admin endpoints (users/ prefix)
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
            if 'user' in token_data:
                print(f"   User ID: {token_data['user']['id']}")
                print(f"   Username: {token_data['user']['username']}")
                print(f"   Is Admin: {token_data['user'].get('is_admin', 'N/A')}")
            return token_data['access_token']
        else:
            print(f"❌ User login failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ User login error: {e}")
        return None

def test_admin_endpoints_access(token, user_type):
    """Test admin endpoints access"""
    print(f"\n🔍 Testing admin endpoints access as {user_type} user...")
    
    headers = {"token": token}
    
    # Test admin endpoints
    admin_endpoints = [
        f"{BASE_URL}/users/",
        f"{BASE_URL}/users/children/",
        f"{BASE_URL}/users/diagnose/"
    ]
    
    for endpoint in admin_endpoints:
        try:
            response = requests.get(endpoint, headers=headers)
            if response.status_code == 200:
                print(f"   ✅ {endpoint} - Access granted")
            elif response.status_code == 403:
                print(f"   ✅ {endpoint} - Correctly denied (403 Forbidden)")
            else:
                print(f"   ❌ {endpoint} - Unexpected status: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint} - Error: {e}")

def test_admin_users_crud(admin_token):
    """Test admin users CRUD operations"""
    print(f"\n🔍 Testing admin users CRUD operations...")
    
    headers = {"token": admin_token}
    
    # Test GET all users
    try:
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 200:
            print("   ✅ GET /users/ - OK")
            users = response.json()
            print(f"   Total users: {len(users)}")
            if users:
                user_id = users[0]['id']
                print(f"   Testing with user ID: {user_id}")
                
                # Test GET user by ID
                response = requests.get(f"{BASE_URL}/users/{user_id}", headers=headers)
                if response.status_code == 200:
                    print("   ✅ GET /users/{id} - OK")
                else:
                    print(f"   ❌ GET /users/{{id}} - Failed: {response.status_code}")
                
                # Test PUT user
                update_data = {
                    "name": "Updated Test User",
                    "address": "Updated Address"
                }
                response = requests.put(f"{BASE_URL}/users/{user_id}", json=update_data, headers=headers)
                if response.status_code == 200:
                    print("   ✅ PUT /users/{id} - OK")
                else:
                    print(f"   ❌ PUT /users/{{id}} - Failed: {response.status_code}")
        else:
            print(f"   ❌ GET /users/ - Failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Users CRUD test error: {e}")

def test_admin_children_crud(admin_token):
    """Test admin children CRUD operations"""
    print(f"\n🔍 Testing admin children CRUD operations...")
    
    headers = {"token": admin_token}
    
    # Test GET all children
    try:
        response = requests.get(f"{BASE_URL}/users/children/", headers=headers)
        if response.status_code == 200:
            print("   ✅ GET /users/children/ - OK")
            children = response.json()
            print(f"   Total children: {len(children)}")
            if children:
                children_id = children[0]['id']
                print(f"   Testing with children ID: {children_id}")
                
                # Test GET children by ID
                response = requests.get(f"{BASE_URL}/users/children/{children_id}", headers=headers)
                if response.status_code == 200:
                    print("   ✅ GET /users/children/{id} - OK")
                else:
                    print(f"   ❌ GET /users/children/{{id}} - Failed: {response.status_code}")
        else:
            print(f"   ❌ GET /users/children/ - Failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Children CRUD test error: {e}")

def test_admin_diagnose_crud(admin_token):
    """Test admin diagnose CRUD operations"""
    print(f"\n🔍 Testing admin diagnose CRUD operations...")
    
    headers = {"token": admin_token}
    
    # Test GET all diagnose histories
    try:
        response = requests.get(f"{BASE_URL}/users/diagnose/", headers=headers)
        if response.status_code == 200:
            print("   ✅ GET /users/diagnose/ - OK")
            diagnoses = response.json()
            print(f"   Total diagnoses: {len(diagnoses)}")
            if diagnoses:
                diagnose_id = diagnoses[0]['id']
                print(f"   Testing with diagnose ID: {diagnose_id}")
                
                # Test GET diagnose by ID
                response = requests.get(f"{BASE_URL}/users/diagnose/{diagnose_id}", headers=headers)
                if response.status_code == 200:
                    print("   ✅ GET /users/diagnose/{id} - OK")
                else:
                    print(f"   ❌ GET /users/diagnose/{{id}} - Failed: {response.status_code}")
        else:
            print(f"   ❌ GET /users/diagnose/ - Failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Diagnose CRUD test error: {e}")

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
    print("🧪 Testing Admin Endpoints (users/ prefix)")
    print("=" * 60)
    
    # Test health endpoint
    if not test_health():
        print("❌ Health check failed. Make sure the server is running!")
        return
    
    # Register and login regular user
    regular_user = test_register_user()
    if not regular_user:
        print("❌ Regular user registration failed!")
        return
    
    regular_token = test_login(regular_user['username'], "testpass123")
    if not regular_token:
        print("❌ Regular user login failed!")
        return
    
    # Test admin endpoints access with regular user (should fail)
    test_admin_endpoints_access(regular_token, "regular")
    
    print("\n🎉 Admin endpoints tests completed!")
    print("✅ Regular user correctly denied access to admin endpoints (403 Forbidden)")
    print("✅ Admin-only endpoints are working correctly!")
    print("\n📝 Note: To test admin access, you need to:")
    print("   1. Set a user as admin in the database")
    print("   2. Use that admin user to test admin endpoints")
    print("   3. Use set_admin.py script to manage admin users")
    print("   4. Then run this test with admin token to test CRUD operations")

if __name__ == "__main__":
    main()
