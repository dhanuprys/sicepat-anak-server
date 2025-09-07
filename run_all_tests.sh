#!/bin/bash

# Comprehensive test runner untuk Stunting Checking App

echo "🧪 Running All Tests for Stunting Checking App"
echo "=" * 60

# Check if server is running
echo "🔍 Checking if server is running..."
if ! curl -s http://localhost:8000/health > /dev/null; then
    echo "❌ Server is not running. Please start the server first with:"
    echo "   python run.py"
    echo "   or"
    echo "   ./start.sh"
    exit 1
fi

echo "✅ Server is running. Starting tests..."

# Run comprehensive API tests
echo ""
echo "📊 Running Comprehensive API Tests..."
echo "-" * 40
python test_api.py

# Run predictor-specific tests
echo ""
echo "🤖 Running Predictor Tests..."
echo "-" * 40
python test_predictor.py

echo ""
echo "🎉 All tests completed!"
echo "📊 Check the results above for any failures"
echo ""
echo "💡 To run individual tests:"
echo "   python test_api.py          # API tests"
echo "   python test_predictor.py    # Predictor tests"
