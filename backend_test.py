#!/usr/bin/env python3
"""
Comprehensive Backend API Testing for 3D Stuff
Tests all endpoints with various scenarios including edge cases
"""

import requests
import json
import os
from datetime import datetime
import uuid

# Get backend URL from frontend .env file
def get_backend_url():
    try:
        with open('/app/frontend/.env', 'r') as f:
            for line in f:
                if line.startswith('REACT_APP_BACKEND_URL='):
                    return line.split('=', 1)[1].strip()
    except Exception as e:
        print(f"Error reading frontend .env: {e}")
        return None

BASE_URL = get_backend_url()
if not BASE_URL:
    print("ERROR: Could not get backend URL from frontend/.env")
    exit(1)

API_BASE = f"{BASE_URL}/api"

print(f"Testing 3D Stuff Backend API at: {API_BASE}")
print("=" * 60)

# Test results tracking
test_results = {
    'passed': 0,
    'failed': 0,
    'errors': []
}

def log_test(test_name, success, details=""):
    """Log test results"""
    status = "✅ PASS" if success else "❌ FAIL"
    print(f"{status}: {test_name}")
    if details:
        print(f"   Details: {details}")
    
    if success:
        test_results['passed'] += 1
    else:
        test_results['failed'] += 1
        test_results['errors'].append(f"{test_name}: {details}")
    print()

def test_health_check():
    """Test health check endpoint"""
    try:
        response = requests.get(f"{API_BASE}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'healthy':
                log_test("Health Check", True, f"Status: {data.get('message')}")
                return True
            else:
                log_test("Health Check", False, f"Unexpected response: {data}")
                return False
        else:
            log_test("Health Check", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("Health Check", False, f"Exception: {str(e)}")
        return False

def test_get_all_products():
    """Test GET /api/products - List all products"""
    try:
        response = requests.get(f"{API_BASE}/products", timeout=10)
        if response.status_code == 200:
            products = response.json()
            if isinstance(products, list):
                log_test("GET /api/products", True, f"Retrieved {len(products)} products")
                return products
            else:
                log_test("GET /api/products", False, "Response is not a list")
                return None
        else:
            log_test("GET /api/products", False, f"Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        log_test("GET /api/products", False, f"Exception: {str(e)}")
        return None

def test_get_products_by_category():
    """Test GET /api/products?category=Utilitários"""
    try:
        response = requests.get(f"{API_BASE}/products?category=Utilitários", timeout=10)
        if response.status_code == 200:
            products = response.json()
            if isinstance(products, list):
                # Check if all products have the correct category
                valid_category = all(p.get('category') == 'Utilitários' for p in products)
                if valid_category:
                    log_test("GET /api/products?category=Utilitários", True, f"Retrieved {len(products)} utility products")
                    return True
                else:
                    log_test("GET /api/products?category=Utilitários", False, "Some products have wrong category")
                    return False
            else:
                log_test("GET /api/products?category=Utilitários", False, "Response is not a list")
                return False
        else:
            log_test("GET /api/products?category=Utilitários", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("GET /api/products?category=Utilitários", False, f"Exception: {str(e)}")
        return False

def test_get_products_all_category():
    """Test GET /api/products?category=Todos"""
    try:
        response = requests.get(f"{API_BASE}/products?category=Todos", timeout=10)
        if response.status_code == 200:
            products = response.json()
            if isinstance(products, list):
                log_test("GET /api/products?category=Todos", True, f"Retrieved {len(products)} products (all categories)")
                return True
            else:
                log_test("GET /api/products?category=Todos", False, "Response is not a list")
                return False
        else:
            log_test("GET /api/products?category=Todos", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("GET /api/products?category=Todos", False, f"Exception: {str(e)}")
        return False

def test_get_single_product(products):
    """Test GET /api/products/{id} with valid product ID"""
    if not products or len(products) == 0:
        log_test("GET /api/products/{id} (valid)", False, "No products available for testing")
        return False
    
    try:
        product_id = products[0]['id']
        response = requests.get(f"{API_BASE}/products/{product_id}", timeout=10)
        if response.status_code == 200:
            product = response.json()
            if product.get('id') == product_id:
                log_test("GET /api/products/{id} (valid)", True, f"Retrieved product: {product.get('name')}")
                return True
            else:
                log_test("GET /api/products/{id} (valid)", False, "Product ID mismatch")
                return False
        else:
            log_test("GET /api/products/{id} (valid)", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("GET /api/products/{id} (valid)", False, f"Exception: {str(e)}")
        return False

def test_get_invalid_product():
    """Test GET /api/products/{id} with invalid product ID"""
    try:
        invalid_id = "999"
        response = requests.get(f"{API_BASE}/products/{invalid_id}", timeout=10)
        if response.status_code == 404:
            log_test("GET /api/products/{id} (invalid)", True, "Correctly returned 404 for invalid product ID")
            return True
        else:
            log_test("GET /api/products/{id} (invalid)", False, f"Expected 404, got {response.status_code}")
            return False
    except Exception as e:
        log_test("GET /api/products/{id} (invalid)", False, f"Exception: {str(e)}")
        return False

def test_post_contact_valid():
    """Test POST /api/contact with valid data"""
    try:
        contact_data = {
            "name": "João Silva",
            "email": "joao.silva@email.com",
            "message": "Gostaria de saber mais sobre os produtos de impressão 3D disponíveis."
        }
        
        response = requests.post(f"{API_BASE}/contact", json=contact_data, timeout=10)
        if response.status_code == 200:
            result = response.json()
            if result.get('name') == contact_data['name'] and result.get('email') == contact_data['email']:
                log_test("POST /api/contact (valid)", True, f"Contact message created with ID: {result.get('id')}")
                return result.get('id')
            else:
                log_test("POST /api/contact (valid)", False, "Response data doesn't match input")
                return None
        else:
            log_test("POST /api/contact (valid)", False, f"Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        log_test("POST /api/contact (valid)", False, f"Exception: {str(e)}")
        return None

def test_post_contact_invalid():
    """Test POST /api/contact with missing required fields"""
    try:
        # Test with missing name
        invalid_data = {
            "email": "test@email.com",
            "message": "Test message"
        }
        
        response = requests.post(f"{API_BASE}/contact", json=invalid_data, timeout=10)
        if response.status_code == 422:  # FastAPI validation error
            log_test("POST /api/contact (missing name)", True, "Correctly returned validation error")
        else:
            log_test("POST /api/contact (missing name)", False, f"Expected 422, got {response.status_code}")
        
        # Test with missing email
        invalid_data2 = {
            "name": "Test User",
            "message": "Test message"
        }
        
        response2 = requests.post(f"{API_BASE}/contact", json=invalid_data2, timeout=10)
        if response2.status_code == 422:
            log_test("POST /api/contact (missing email)", True, "Correctly returned validation error")
        else:
            log_test("POST /api/contact (missing email)", False, f"Expected 422, got {response2.status_code}")
            
        return True
    except Exception as e:
        log_test("POST /api/contact (invalid)", False, f"Exception: {str(e)}")
        return False

def test_get_contact_messages():
    """Test GET /api/contact - Retrieve all contact messages"""
    try:
        response = requests.get(f"{API_BASE}/contact", timeout=10)
        if response.status_code == 200:
            messages = response.json()
            if isinstance(messages, list):
                log_test("GET /api/contact", True, f"Retrieved {len(messages)} contact messages")
                return True
            else:
                log_test("GET /api/contact", False, "Response is not a list")
                return False
        else:
            log_test("GET /api/contact", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("GET /api/contact", False, f"Exception: {str(e)}")
        return False

def test_get_company_info():
    """Test GET /api/company-info"""
    try:
        response = requests.get(f"{API_BASE}/company-info", timeout=10)
        if response.status_code == 200:
            company_info = response.json()
            required_fields = ['name', 'slogan', 'about', 'whatsapp', 'email', 'social_media']
            if all(field in company_info for field in required_fields):
                log_test("GET /api/company-info", True, f"Company: {company_info.get('name')}")
                return True
            else:
                missing_fields = [field for field in required_fields if field not in company_info]
                log_test("GET /api/company-info", False, f"Missing fields: {missing_fields}")
                return False
        else:
            log_test("GET /api/company-info", False, f"Status code: {response.status_code}")
            return False
    except Exception as e:
        log_test("GET /api/company-info", False, f"Exception: {str(e)}")
        return False

def test_invalid_endpoint():
    """Test invalid endpoint - should return 404"""
    try:
        response = requests.get(f"{API_BASE}/invalid-endpoint", timeout=10)
        if response.status_code == 404:
            log_test("Invalid endpoint test", True, "Correctly returned 404 for invalid endpoint")
            return True
        else:
            log_test("Invalid endpoint test", False, f"Expected 404, got {response.status_code}")
            return False
    except Exception as e:
        log_test("Invalid endpoint test", False, f"Exception: {str(e)}")
        return False

def test_malformed_request():
    """Test malformed JSON request"""
    try:
        # Send invalid JSON to contact endpoint
        response = requests.post(f"{API_BASE}/contact", data="invalid json", 
                               headers={'Content-Type': 'application/json'}, timeout=10)
        if response.status_code == 422:  # FastAPI returns 422 for malformed JSON
            log_test("Malformed JSON test", True, "Correctly handled malformed JSON")
            return True
        else:
            log_test("Malformed JSON test", False, f"Expected 422, got {response.status_code}")
            return False
    except Exception as e:
        log_test("Malformed JSON test", False, f"Exception: {str(e)}")
        return False

def run_all_tests():
    """Run all backend API tests"""
    print("Starting comprehensive backend API testing...")
    print()
    
    # Test health check first
    if not test_health_check():
        print("❌ Health check failed - API may not be running properly")
        return
    
    # Test Products API
    print("🔍 Testing Products API...")
    products = test_get_all_products()
    test_get_products_by_category()
    test_get_products_all_category()
    test_get_single_product(products)
    test_get_invalid_product()
    
    # Test Contact API
    print("📧 Testing Contact API...")
    test_post_contact_valid()
    test_post_contact_invalid()
    test_get_contact_messages()
    
    # Test Company Info API
    print("🏢 Testing Company Info API...")
    test_get_company_info()
    
    # Test Error Handling
    print("⚠️ Testing Error Handling...")
    test_invalid_endpoint()
    test_malformed_request()
    
    # Print final results
    print("=" * 60)
    print("FINAL TEST RESULTS:")
    print(f"✅ Passed: {test_results['passed']}")
    print(f"❌ Failed: {test_results['failed']}")
    print(f"📊 Success Rate: {(test_results['passed'] / (test_results['passed'] + test_results['failed']) * 100):.1f}%")
    
    if test_results['errors']:
        print("\n🚨 FAILED TESTS:")
        for error in test_results['errors']:
            print(f"   - {error}")
    
    print("=" * 60)

if __name__ == "__main__":
    run_all_tests()