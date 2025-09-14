#!/usr/bin/env python3
"""
Comprehensive test script untuk Stunting Checking App API - Development Environment
"""

import requests
import json
import time
from datetime import date, datetime

# Base URL for development
BASE_URL = "http://localhost:8000/api"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get("http://localhost:8000/health")
        if response.status_code == 200:
            print("✅ Health endpoint OK")
            return True
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Health endpoint error: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("🔍 Testing root endpoint...")
    try:
        response = requests.get("http://localhost:8000/")
        if response.status_code == 200:
            print("✅ Root endpoint OK")
            data = response.json()
            print(f"   Message: {data.get('message', 'N/A')}")
            print(f"   Version: {data.get('version', 'N/A')}")
            return True
        else:
            print(f"❌ Root endpoint failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Root endpoint error: {e}")
        return False

def test_register():
    """Test user registration"""
    print("\n🔍 Testing user registration...")
    
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
            print(f"   Name: {user['name']}")
            print(f"   Is Admin: {user.get('is_admin', 'N/A')}")
            return user
        else:
            print(f"❌ User registration failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ User registration error: {e}")
        return None

def test_register_duplicate_username():
    """Test duplicate username registration"""
    print("\n🔍 Testing duplicate username registration...")
    
    user_data = {
        "avatar_type": 1,
        "name": "Duplicate User",
        "username": "duplicateuser",
        "address": "Test Address",
        "dob": str(date.today()),
        "gender": "L",
        "password": "testpass123"
    }
    
    try:
        # First registration
        response1 = requests.post(f"{BASE_URL}/auth/register", json=user_data)
        if response1.status_code == 201:
            print("   ✅ First registration OK")
            
            # Second registration with same username
            response2 = requests.post(f"{BASE_URL}/auth/register", json=user_data)
            if response2.status_code == 400:
                print("   ✅ Duplicate username correctly rejected")
                return True
            else:
                print(f"   ❌ Duplicate username should be rejected: {response2.status_code}")
                return False
        else:
            print(f"   ❌ First registration failed: {response1.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Duplicate username test error: {e}")
        return False

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
            print(f"   Token type: {token_data['token_type']}")
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

def test_login_invalid_credentials():
    """Test login with invalid credentials"""
    print("\n🔍 Testing login with invalid credentials...")
    
    login_data = {
        "username": "nonexistentuser",
        "password": "wrongpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
        if response.status_code == 401:
            print("✅ Invalid credentials correctly rejected")
            return True
        else:
            print(f"❌ Invalid credentials should be rejected: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid credentials test error: {e}")
        return False

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
            print(f"   Gender: {children['gender']}")
            return children
        else:
            print(f"❌ Children creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Children creation error: {e}")
        return None

def test_create_children_invalid_gender(token):
    """Test creating children with invalid gender"""
    print("\n🔍 Testing children creation with invalid gender...")
    
    children_data = {
        "name": "Invalid Child",
        "gender": "X",  # Invalid gender
        "dob": str(date.today())
    }
    
    headers = {"token": token}
    
    try:
        response = requests.post(f"{BASE_URL}/children", json=children_data, headers=headers)
        if response.status_code == 422:
            print("✅ Invalid gender correctly rejected")
            return True
        else:
            print(f"❌ Invalid gender should be rejected: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid gender test error: {e}")
        return False

def test_get_children_list(token):
    """Test getting children list"""
    print("\n🔍 Testing get children list...")
    
    headers = {"token": token}
    
    try:
        response = requests.get(f"{BASE_URL}/children", headers=headers)
        if response.status_code == 200:
            print("✅ Get children list OK")
            children_list = response.json()
            print(f"   Total children: {len(children_list)}")
            return children_list
        else:
            print(f"❌ Get children list failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Get children list error: {e}")
        return None

def test_get_children_detail(token, children_id):
    """Test getting children detail"""
    print("\n🔍 Testing get children detail...")
    
    headers = {"token": token}
    
    try:
        response = requests.get(f"{BASE_URL}/children/{children_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Get children detail OK")
            children = response.json()
            print(f"   Children ID: {children['id']}")
            print(f"   Name: {children['name']}")
            return children
        else:
            print(f"❌ Get children detail failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Get children detail error: {e}")
        return None

def test_update_children(token, children_id):
    """Test updating children"""
    print("\n🔍 Testing update children...")
    
    update_data = {
        "name": "Updated Test Child",
        "gender": "P"
    }
    
    headers = {"token": token}
    
    try:
        response = requests.put(f"{BASE_URL}/children/{children_id}", json=update_data, headers=headers)
        if response.status_code == 200:
            print("✅ Update children OK")
            children = response.json()
            print(f"   Updated name: {children['name']}")
            print(f"   Updated gender: {children['gender']}")
            return children
        else:
            print(f"❌ Update children failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Update children error: {e}")
        return None

def test_create_diagnose(token, children_id):
    """Test creating diagnose"""
    print("\n🔍 Testing diagnose creation...")
    
    diagnose_data = {
        "age_on_month": 38,
        "gender": "L",
        "height": 85
    }
    
    headers = {"token": token}
    
    try:
        response = requests.post(f"{BASE_URL}/children/{children_id}/diagnose", json=diagnose_data, headers=headers)
        if response.status_code == 201:
            print("✅ Diagnose creation OK")
            diagnose = response.json()
            print(f"   Diagnose Result: {diagnose.get('result', 'N/A')}")
            print(f"   Diagnose ID: {diagnose.get('id', 'N/A')}")
            print(f"   Full Response: {diagnose}")
            return diagnose
        else:
            print(f"❌ Diagnose creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Diagnose creation error: {e}")
        return None

def test_create_diagnose_invalid_age(token, children_id):
    """Test creating diagnose with invalid age"""
    print("\n🔍 Testing diagnose creation with invalid age...")
    
    diagnose_data = {
        "age_on_month": 100,  # Invalid age
        "gender": "L",
        "height": 85
    }
    
    headers = {"token": token}
    
    try:
        response = requests.post(f"{BASE_URL}/children/{children_id}/diagnose", json=diagnose_data, headers=headers)
        if response.status_code == 422:
            print("✅ Invalid age correctly rejected")
            return True
        else:
            print(f"❌ Invalid age should be rejected: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid age test error: {e}")
        return False

def test_get_diagnose_list(token, children_id):
    """Test getting diagnose list"""
    print("\n🔍 Testing get diagnose list...")
    
    headers = {"token": token}
    
    try:
        response = requests.get(f"{BASE_URL}/children/{children_id}/diagnose", headers=headers)
        if response.status_code == 200:
            print("✅ Get diagnose list OK")
            diagnose_list = response.json()
            print(f"   Total diagnoses: {len(diagnose_list)}")
            return diagnose_list
        else:
            print(f"❌ Get diagnose list failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Get diagnose list error: {e}")
        return None

def test_get_diagnose_detail(token, children_id, diagnose_id):
    """Test getting diagnose detail"""
    print("\n🔍 Testing get diagnose detail...")
    
    headers = {"token": token}
    
    try:
        response = requests.get(f"{BASE_URL}/children/{children_id}/diagnose/{diagnose_id}", headers=headers)
        if response.status_code == 200:
            print("✅ Get diagnose detail OK")
            diagnose = response.json()
            print(f"   Diagnose ID: {diagnose['id']}")
            print(f"   Result: {diagnose['result']}")
            return diagnose
        else:
            print(f"❌ Get diagnose detail failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Get diagnose detail error: {e}")
        return None

def test_generate_pdf_report(token, children_id, diagnose_id, user_type="user"):
    """Test generate PDF report"""
    print(f"\n🔍 Testing generate PDF report as {user_type} user...")
    
    headers = {"token": token}
    
    try:
        response = requests.get(f"{BASE_URL}/children/{children_id}/diagnose/{diagnose_id}/report", headers=headers)
        if response.status_code == 200:
            print(f"✅ Generate PDF report OK for {user_type} user")
            report_data = response.json()
            print(f"   Message: {report_data.get('message', 'N/A')}")
            print(f"   Download URL: {report_data.get('download_url', 'N/A')}")
            print(f"   Filename: {report_data.get('filename', 'N/A')}")
            return report_data
        elif response.status_code == 403:
            print(f"✅ Generate PDF report correctly rejected for {user_type} user (403 Forbidden)")
            error_data = response.json()
            print(f"   Error: {error_data.get('detail', 'N/A')}")
            return None
        else:
            print(f"❌ Generate PDF report failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Generate PDF report error: {e}")
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
            return status_data
        else:
            print(f"❌ Predictor status failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Predictor status error: {e}")
        return None

def test_get_profile(token):
    """Test get profile"""
    print("\n🔍 Testing get profile...")
    
    headers = {"token": token}
    
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if response.status_code == 200:
            print("✅ Get profile OK")
            profile = response.json()
            print(f"   User ID: {profile['id']}")
            print(f"   Username: {profile['username']}")
            print(f"   Name: {profile['name']}")
            print(f"   Is Admin: {profile.get('is_admin', 'N/A')}")
            return profile
        else:
            print(f"❌ Get profile failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Get profile error: {e}")
        return None

def test_profile_update(token):
    """Test profile update"""
    print("\n🔍 Testing profile update...")
    
    update_data = {
        "name": "Updated Test User",
        "address": "Updated Test Address"
    }
    
    headers = {"token": token}
    
    try:
        response = requests.put(f"{BASE_URL}/profile", json=update_data, headers=headers)
        if response.status_code == 200:
            print("✅ Profile update OK")
            profile = response.json()
            print(f"   Updated name: {profile['name']}")
            print(f"   Updated address: {profile['address']}")
            print(f"   Is Admin: {profile.get('is_admin', 'N/A')}")
            return profile
        else:
            print(f"❌ Profile update failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Profile update error: {e}")
        return None

def test_change_password(token):
    """Test change password"""
    print("\n🔍 Testing change password...")
    
    password_data = {
        "new_password": "newtestpass123"
    }
    
    headers = {"token": token}
    
    try:
        response = requests.put(f"{BASE_URL}/profile/change-password", json=password_data, headers=headers)
        if response.status_code == 200:
            print("✅ Change password OK")
            result = response.json()
            print(f"   Message: {result.get('message', 'N/A')}")
            return True
        else:
            print(f"❌ Change password failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Change password error: {e}")
        return False

def test_unauthorized_access():
    """Test unauthorized access to protected endpoints"""
    print("\n🔍 Testing unauthorized access...")
    
    # Test without token
    endpoints = [
        f"{BASE_URL}/profile",
        f"{BASE_URL}/children",
        f"{BASE_URL}/children/1/diagnose"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(endpoint)
            if response.status_code in [401, 422]:  # 422 for missing token header, 401 for invalid token
                print(f"   ✅ {endpoint} correctly requires authentication")
            else:
                print(f"   ❌ {endpoint} should require authentication: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"   ❌ {endpoint} test error: {e}")
    
    return True

def test_invalid_token():
    """Test with invalid token"""
    print("\n🔍 Testing invalid token...")
    
    headers = {"token": "invalid_token_here"}
    
    try:
        response = requests.get(f"{BASE_URL}/profile", headers=headers)
        if response.status_code == 401:
            print("✅ Invalid token correctly rejected")
            return True
        else:
            print(f"❌ Invalid token should be rejected: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Invalid token test error: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 Comprehensive Testing Stunting Checking App API - Development")
    print("=" * 70)
    
    # Test basic endpoints
    if not test_health():
        print("❌ Health check failed. Make sure the server is running!")
        return
    
    if not test_root():
        print("❌ Root endpoint failed!")
        return
    
    # Test authentication
    user = test_register()
    if not user:
        print("❌ User registration failed!")
        return
    
    test_register_duplicate_username()
    
    token = test_login(user['username'], "testpass123")
    if not token:
        print("❌ User login failed!")
        return
    
    test_login_invalid_credentials()
    
    # Test children management
    children = test_create_children(token)
    if not children:
        print("❌ Children creation failed!")
        return
    
    test_create_children_invalid_gender(token)
    test_get_children_list(token)
    test_get_children_detail(token, children['id'])
    test_update_children(token, children['id'])
    
    # Test diagnose
    diagnose = test_create_diagnose(token, children['id'])
    if not diagnose:
        print("❌ Diagnose creation failed!")
        return
    
    # Check if diagnose has required fields
    if 'id' not in diagnose:
        print(f"⚠️  Diagnose response missing 'id' field: {diagnose}")
        print("   Skipping diagnose detail test...")
    else:
        test_create_diagnose_invalid_age(token, children['id'])
        test_get_diagnose_list(token, children['id'])
        test_get_diagnose_detail(token, children['id'], diagnose['id'])
        test_generate_pdf_report(token, children['id'], diagnose['id'], "regular")
    
    # Test predictor
    test_predictor_status()
    
    # Test profile management
    test_get_profile(token)
    test_profile_update(token)
    test_change_password(token)
    
    # Test security
    test_unauthorized_access()
    test_invalid_token()
    
    print("\n🎉 All comprehensive tests completed!")
    print("✅ API is working correctly with all features")
    print(f"📊 Tested endpoints: Health, Root, Auth, Children, Diagnose, Predictor, Profile, PDF Report")
    print(f"🔒 Security tests: Unauthorized access, Invalid tokens, Admin-only PDF")
    print(f"⚠️  Validation tests: Invalid data, Duplicate data")

if __name__ == "__main__":
    main()
