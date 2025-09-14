# 🧪 Test Suite - Stunting Checking App

This directory contains comprehensive test scripts for the Stunting Checking App API.

## 📁 Test Files

### Core API Tests
- **`test_api_dev.py`** - Comprehensive API tests for development environment (`http://localhost:8000`)
- **`test_api_prod.py`** - Comprehensive API tests for production environment (`https://stunting-api.dedan.my.id`)

### Feature-Specific Tests
- **`test_admin_features.py`** - Tests for admin-only features (PDF report access control)
- **`test_admin_endpoints.py`** - Tests for admin endpoints (users/ prefix)
- **`test_predictor_features.py`** - Tests for ML predictor functionality

## 🚀 Running Tests

### Development Environment
```bash
# Run comprehensive API tests
python tests/test_api_dev.py

# Run admin features tests
python tests/test_admin_features.py

# Run ML predictor tests
python tests/test_predictor_features.py

# Run admin endpoints tests
python tests/test_admin_endpoints.py
```

### Production Environment
```bash
# Run comprehensive API tests
python tests/test_api_prod.py
```

## 📋 Test Coverage

### API Endpoints Tested
- ✅ **Health & Root** - Basic server endpoints
- ✅ **Authentication** - Login, register, invalid credentials
- ✅ **User Management** - Profile get/update, password change
- ✅ **Children Management** - CRUD operations, validation
- ✅ **Diagnose System** - Create, list, detail, validation
- ✅ **ML Predictor** - Status check, various prediction scenarios
- ✅ **PDF Reports** - Admin-only access control
- ✅ **Admin Endpoints** - users/ prefix endpoints (admin-only)
- ✅ **Security** - Unauthorized access, invalid tokens

### Test Scenarios
- ✅ **Valid Data** - Normal operation flows
- ✅ **Invalid Data** - Validation error handling
- ✅ **Duplicate Data** - Duplicate username handling
- ✅ **Authentication** - Token-based access control
- ✅ **Authorization** - Admin-only features
- ✅ **Error Handling** - Proper HTTP status codes

## 🔧 Test Configuration

### Environment Variables
Tests automatically detect environment based on BASE_URL:
- **Development**: `http://localhost:8000/api`
- **Production**: `https://stunting-api.dedan.my.id/api`

### Admin Testing
For admin feature tests, you need to set a user as admin in the database:
```bash
# Set user as admin
docker compose exec -ti app python set_admin.py <username>

# Remove admin status
docker compose exec -ti app python set_admin.py <username> false

# List all users
docker compose exec -ti app python set_admin.py list
```

## 📊 Expected Results

### Successful Test Run
```
🧪 Comprehensive Testing Stunting Checking App API - Development
======================================================================
🔍 Testing health endpoint...
✅ Health endpoint OK
🔍 Testing root endpoint...
✅ Root endpoint OK
...
🎉 All comprehensive tests completed!
✅ API is working correctly with all features
📊 Tested endpoints: Health, Root, Auth, Children, Diagnose, Predictor, Profile, PDF Report
🔒 Security tests: Unauthorized access, Invalid tokens, Admin-only PDF
⚠️  Validation tests: Invalid data, Duplicate data
```

### Admin Features Test
```
🧪 Testing Admin Features - PDF Report Access Control
============================================================
...
✅ Regular user correctly denied access to PDF reports (403 Forbidden)
✅ Admin-only PDF report feature is working correctly!
```

### ML Predictor Test
```
🧪 Testing ML Predictor Features
==================================================
...
📊 ML Predictor Test Results Summary:
============================================================
   Test 1: 12 months boy, 75cm → Normal
   Test 2: 24 months girl, 85cm → Stunted
   Test 3: 36 months boy, 95cm → Severely Stunted
   ...
✅ Successfully tested 6 prediction scenarios
📈 ML Predictor is working correctly with various input combinations
```

## 🛠️ Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure server is running
   - Check if port 8000 is accessible (dev) or production URL is reachable

2. **Authentication Errors**
   - Verify token header format: `{"token": "your_token_here"}`
   - Check if user exists and password is correct

3. **Admin Access Denied**
   - Ensure user has `is_admin = true` in database
   - Use `set_admin.py` script to manage admin users

4. **ML Predictor Not Ready**
   - Check if model files exist in `model_cache/` directory
   - Verify predictor initialization in server logs

### Debug Mode
Add debug prints to test functions to see detailed request/response data:
```python
print(f"Request: {request_data}")
print(f"Response: {response.json()}")
```

## 📝 Notes

- Tests create temporary users and data - no cleanup required
- Each test run uses unique timestamps to avoid conflicts
- PDF reports are generated in `reports/` directory (git-ignored)
- Tests are designed to be idempotent and can be run multiple times
