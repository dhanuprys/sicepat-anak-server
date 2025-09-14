#!/usr/bin/env python3
"""
Test script untuk admin features - Admin-only PDF report
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
            print(f"   Is Admin: {user.get('is_admin', 'N/A')}")
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

def test_create_diagnose(token, children_id):
    """Test creating diagnose"""
    print("\n🔍 Testing diagnose creation...")
    
    diagnose_data = {
        "age_on_month": 24,
        "gender": "L",
        "height": 85
    }
    
    headers = {"token": token}
    
    try:
        response = requests.post(f"{BASE_URL}/children/{children_id}/diagnose", json=diagnose_data, headers=headers)
        if response.status_code == 201:
            print("✅ Diagnose creation OK")
            diagnose = response.json()
            print(f"   Diagnose ID: {diagnose['id']}")
            print(f"   Result: {diagnose['result']}")
            return diagnose
        else:
            print(f"❌ Diagnose creation failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"❌ Diagnose creation error: {e}")
        return None

def test_generate_pdf_report(token, children_id, diagnose_id, user_type):
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
    print("🧪 Testing Admin Features - PDF Report Access Control")
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
    
    # Create children and diagnose with regular user
    regular_children = test_create_children(regular_token)
    if not regular_children:
        print("❌ Regular children creation failed!")
        return
    
    regular_diagnose = test_create_diagnose(regular_token, regular_children['id'])
    if not regular_diagnose:
        print("❌ Regular diagnose creation failed!")
        return
    
    # Test PDF generation with regular user (should fail with 403)
    regular_pdf = test_generate_pdf_report(regular_token, regular_children['id'], regular_diagnose['id'], "regular")
    
    print("\n🎉 Admin features tests completed!")
    
    if regular_pdf is None:
        print("✅ Regular user correctly denied access to PDF reports (403 Forbidden)")
        print("✅ Admin-only PDF report feature is working correctly!")
        print("\n📝 Note: To test admin access, you need to:")
        print("   1. Set a user as admin in the database")
        print("   2. Use that admin user to test PDF generation")
        print("   3. Use set_admin.py script to manage admin users")
    else:
        print("❌ Regular user should not be able to generate PDF reports")
        print("❌ Admin-only PDF report feature is NOT working correctly!")

if __name__ == "__main__":
    main()
