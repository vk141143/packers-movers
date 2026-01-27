#!/usr/bin/env python3
"""
Deployment verification script for Client Backend
"""
import requests
import json
import sys
from datetime import datetime

# Configuration
CLIENT_BASE_URL = "https://client.voidworksgroup.co.uk"
CREW_BASE_URL = "https://crew.voidworksgroup.co.uk"

def test_endpoint(url, method="GET", data=None, expected_status=200):
    """Test an API endpoint"""
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, timeout=10)
        
        print(f"✅ {method} {url} - Status: {response.status_code}")
        
        if response.status_code != expected_status:
            print(f"⚠️  Expected {expected_status}, got {response.status_code}")
            if response.text:
                print(f"   Response: {response.text[:200]}...")
        
        return response.status_code == expected_status
    except Exception as e:
        print(f"❌ {method} {url} - Error: {str(e)}")
        return False

def main():
    print("🚀 Deployment Verification Started")
    print(f"⏰ Time: {datetime.now()}")
    print("=" * 50)
    
    # Test Client Backend
    print("\n📱 CLIENT BACKEND TESTS")
    print("-" * 30)
    
    client_tests = [
        (f"{CLIENT_BASE_URL}/", "GET"),
        (f"{CLIENT_BASE_URL}/docs", "GET"),
        (f"{CLIENT_BASE_URL}/api/service-types", "GET"),
        (f"{CLIENT_BASE_URL}/api/urgency-levels", "GET"),
        (f"{CLIENT_BASE_URL}/api/waste-types", "GET"),
        (f"{CLIENT_BASE_URL}/api/access-difficulties", "GET"),
    ]
    
    client_passed = 0
    for url, method in client_tests:
        if test_endpoint(url, method):
            client_passed += 1
    
    # Test Crew Admin Backend
    print("\n👥 CREW ADMIN BACKEND TESTS")
    print("-" * 30)
    
    crew_tests = [
        (f"{CREW_BASE_URL}/", "GET"),
        (f"{CREW_BASE_URL}/docs", "GET"),
    ]
    
    crew_passed = 0
    for url, method in crew_tests:
        if test_endpoint(url, method):
            crew_passed += 1
    
    # Test Registration Endpoint (should return validation error, not 500)
    print("\n🔐 REGISTRATION TEST")
    print("-" * 20)
    
    test_data = {
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "company_name": "Test Company",
        "phone_number": "+44 7700 900000",
        "client_type": "Council",
        "address": "Test Address"
    }
    
    reg_response = requests.post(f"{CLIENT_BASE_URL}/api/auth/register/client", json=test_data)
    if reg_response.status_code in [200, 201, 400, 422]:  # Any of these are acceptable
        print(f"✅ Registration endpoint working - Status: {reg_response.status_code}")
        registration_working = True
    else:
        print(f"❌ Registration endpoint failed - Status: {reg_response.status_code}")
        print(f"   Response: {reg_response.text[:200]}...")
        registration_working = False
    
    # Summary
    print("\n📊 DEPLOYMENT SUMMARY")
    print("=" * 30)
    print(f"Client Backend: {client_passed}/{len(client_tests)} tests passed")
    print(f"Crew Backend: {crew_passed}/{len(crew_tests)} tests passed")
    print(f"Registration: {'✅ Working' if registration_working else '❌ Failed'}")
    
    total_tests = len(client_tests) + len(crew_tests) + 1
    total_passed = client_passed + crew_passed + (1 if registration_working else 0)
    
    print(f"\nOverall: {total_passed}/{total_tests} tests passed")
    
    if total_passed == total_tests:
        print("🎉 ALL SYSTEMS OPERATIONAL!")
        return 0
    else:
        print("⚠️  Some issues detected")
        return 1

if __name__ == "__main__":
    sys.exit(main())