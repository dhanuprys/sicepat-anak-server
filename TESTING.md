# 🧪 Testing Guide - Stunting Checking App

## 📋 Overview

Testing suite untuk Stunting Checking App yang mencakup:
- **API Endpoints Testing** - Semua endpoint dan fitur
- **Predictor Testing** - ML model dan fallback logic
- **Security Testing** - Authentication dan authorization
- **Validation Testing** - Input validation dan error handling

## 🚀 Quick Start

### 1. Start the Server
```bash
# Option 1: Direct
python run.py

# Option 2: Using script
./start.sh

# Option 3: Using Makefile
make run
```

### 2. Run All Tests
```bash
# Run all tests
./run_all_tests.sh

# Or run individually
python test_api.py          # API tests
python test_predictor.py    # Predictor tests
```

## 📊 Test Coverage

### **API Tests (`test_api.py`)**

#### **Basic Endpoints**
- ✅ Health check (`/health`)
- ✅ Root endpoint (`/`)
- ✅ API documentation (`/docs`, `/redoc`)

#### **Authentication**
- ✅ User registration (`POST /api/auth/register`)
- ✅ User login (`POST /api/auth/login`)
- ✅ Duplicate username handling
- ✅ Invalid credentials handling

#### **User Management**
- ✅ Profile update (`PUT /api/profile`)
- ✅ Password change (`PUT /api/profile/change-password`)

#### **Children Management**
- ✅ Create children (`POST /api/children`)
- ✅ Get children list (`GET /api/children`)
- ✅ Get children detail (`GET /api/children/{id}`)
- ✅ Update children (`PUT /api/children/{id}`)
- ✅ Invalid data validation

#### **Diagnose System**
- ✅ Create diagnose (`POST /api/children/{id}/diagnose`)
- ✅ Get diagnose list (`GET /api/children/{id}/diagnose`)
- ✅ Get diagnose detail (`GET /api/children/{id}/diagnose/{diagnose_id}`)
- ✅ Input validation (age, height, gender)

#### **Security & Validation**
- ✅ Unauthorized access protection
- ✅ Invalid token handling
- ✅ Input validation
- ✅ Error status codes

### **Predictor Tests (`test_predictor.py`)**

#### **ML Model Testing**
- ✅ Predictor initialization
- ✅ Cache system functionality
- ✅ Multiple input combinations
- ✅ Edge case handling

#### **Test Cases**
- **Age Groups**: 0-24 months, 25-60 months
- **Gender**: Laki-laki (L), Perempuan (P)
- **Height Ranges**: 30-200 cm
- **Expected Results**: Normal, Risiko Stunting, Stunting

#### **Input Combinations**
```
Young Children (≤24 months):
├── Laki-laki: 70cm, 80cm, 85cm
└── Perempuan: 68cm, 78cm, 83cm

Older Children (>24 months):
├── Laki-laki: 85cm, 90cm, 100cm
└── Perempuan: 83cm, 88cm, 98cm
```

## 🧪 Running Tests

### **Individual Test Files**

#### **1. API Tests**
```bash
python test_api.py
```

**Output Example:**
```
🧪 Comprehensive Testing Stunting Checking App API
============================================================
🔍 Testing health endpoint...
✅ Health endpoint OK

🔍 Testing root endpoint...
✅ Root endpoint OK
   Message: Welcome to Stunting Checking App API
   Version: 1.0.0

🔍 Testing user registration...
✅ User registration OK
   User ID: 1
   Username: testuser1234567890
   Name: Test User

🎉 All comprehensive tests completed!
✅ API is working correctly with all features
```

#### **2. Predictor Tests**
```bash
python test_predictor.py
```

**Output Example:**
```
🧪 Testing Stunting Predictor Functionality
============================================================
🔍 Testing predictor initialization...
✅ Predictor status: ready
   🚀 ML Model is ready!
   📊 Algorithm: SVM (Linear Kernel)
   🎯 Available classes: ['Normal', 'Risiko Stunting', 'Stunting']

🔍 Testing diagnose with different inputs...
   ✅ Test 1: Young boy, short height
      Input: Age=12m, Gender=L, Height=70cm
      Output: Stunting

🎉 All predictor tests completed!
✅ Stunting predictor is working correctly
```

### **All Tests at Once**
```bash
./run_all_tests.sh
```

## 🔧 Test Configuration

### **Environment Variables**
```bash
# Base URL for testing
BASE_URL = "http://localhost:8000/api"

# Test data
- Username: auto-generated with timestamp
- Password: "testpass123"
- Gender: L (Laki-laki), P (Perempuan)
- Age: 0-60 months
- Height: 30-200 cm
```

### **Test Data Generation**
```python
# Unique usernames
username = f"testuser{int(time.time())}"

# Random test data
test_cases = [
    {"age": 12, "gender": "L", "height": 70},
    {"age": 36, "gender": "P", "height": 98}
]
```

## 📈 Test Results Interpretation

### **Success Indicators**
- ✅ All endpoints return correct status codes
- ✅ Authentication works properly
- ✅ Data validation rejects invalid input
- ✅ ML predictor returns consistent results
- ✅ Cache system functions correctly

### **Common Issues & Solutions**

#### **1. Server Not Running**
```
❌ Health check failed. Make sure the server is running!
```
**Solution**: Start the server with `python run.py`

#### **2. Database Connection Issues**
```
❌ Database connection failed
```
**Solution**: Check `.env` file and database configuration

#### **3. ML Predictor Not Ready**
```
⚠️  ML Model not ready, using fallback logic
```
**Solution**: Check if dataset file exists at `app/mod/data_balita.xlsx`

#### **4. Validation Errors**
```
❌ Invalid age should be rejected: 200
```
**Solution**: Check input validation rules in schemas

## 🚨 Troubleshooting

### **Test Failures**

#### **API Tests Failing**
1. Check server status: `curl http://localhost:8000/health`
2. Verify database connection
3. Check API logs for errors
4. Ensure all dependencies installed

#### **Predictor Tests Failing**
1. Check predictor status: `GET /api/children/predictor/status`
2. Verify dataset file exists
3. Check cache directory permissions
4. Review ML model initialization logs

### **Common Commands**
```bash
# Check server health
curl http://localhost:8000/health

# Check predictor status
curl http://localhost:8000/api/children/predictor/status

# View API documentation
open http://localhost:8000/docs

# Check logs
tail -f app.log
```

## 📝 Adding New Tests

### **New API Endpoint Test**
```python
def test_new_endpoint(token):
    """Test new endpoint"""
    print("\n🔍 Testing new endpoint...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    try:
        response = requests.get(f"{BASE_URL}/new-endpoint", headers=headers)
        if response.status_code == 200:
            print("✅ New endpoint OK")
            return response.json()
        else:
            print(f"❌ New endpoint failed: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ New endpoint error: {e}")
        return None
```

### **New Predictor Test**
```python
def test_new_prediction_scenario():
    """Test new prediction scenario"""
    print("\n🔍 Testing new prediction scenario...")
    
    # Test logic here
    return True
```

## 🎯 Best Practices

1. **Test Isolation**: Each test should be independent
2. **Data Cleanup**: Use unique identifiers (timestamps)
3. **Error Handling**: Test both success and failure cases
4. **Validation**: Test edge cases and invalid inputs
5. **Documentation**: Clear test descriptions and expected results

## 📊 Performance Testing

### **Load Testing**
```bash
# Install Apache Bench
sudo apt-get install apache2-utils

# Test API performance
ab -n 100 -c 10 http://localhost:8000/health
```

### **Memory Testing**
```bash
# Monitor memory usage
watch -n 1 'ps aux | grep python'
```

## 🔍 Continuous Integration

### **GitHub Actions Example**
```yaml
name: Test Stunting App
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.10
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python test_api.py
```

---

**Happy Testing! 🎉**
