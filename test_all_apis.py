"""Comprehensive API Test for Client Backend Authentication"""
import sys
import requests
import json
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Configuration
BASE_URL = "http://localhost:8000/api/auth"
TEST_EMAIL = f"test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
TEST_PASSWORD = "Test@123456"
TEST_PHONE = "+447700900123"

print("=" * 70)
print("CLIENT BACKEND - COMPREHENSIVE API TEST")
print("=" * 70)
print(f"Base URL: {BASE_URL}")
print(f"Test Email: {TEST_EMAIL}")
print("=" * 70)

# Store test data
test_data = {
    "email": TEST_EMAIL,
    "otp": None,
    "access_token": None,
    "refresh_token": None
}

def test_api(name, method, endpoint, data=None, headers=None, expected_status=200):
    """Helper function to test API endpoints"""
    url = f"{BASE_URL}{endpoint}"
    print(f"\n{'='*70}")
    print(f"TEST: {name}")
    print(f"{'='*70}")
    print(f"Method: {method}")
    print(f"URL: {url}")
    if data:
        print(f"Payload: {json.dumps(data, indent=2)}")
    
    try:
        if method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=30)
        elif method == "GET":
            response = requests.get(url, headers=headers, timeout=30)
        else:
            print(f"❌ Unsupported method: {method}")
            return None
        
        print(f"\nStatus Code: {response.status_code}")
        
        try:
            response_json = response.json()
            print(f"Response: {json.dumps(response_json, indent=2)}")
        except:
            print(f"Response: {response.text}")
            response_json = None
        
        if response.status_code == expected_status:
            print(f"✅ PASSED - Got expected status {expected_status}")
            return response_json
        else:
            print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
            return None
            
    except requests.exceptions.ConnectionError:
        print(f"❌ FAILED - Cannot connect to server. Is it running?")
        return None
    except requests.exceptions.Timeout:
        print(f"❌ FAILED - Request timeout")
        return None
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        return None

# Test 1: Register Client
print("\n" + "🔹" * 35)
print("PHASE 1: REGISTRATION")
print("🔹" * 35)

register_data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD,
    "full_name": "Test User",
    "company_name": "Test Company Ltd",
    "contact_person_name": "John Doe",
    "department": "IT Department",
    "phone_number": TEST_PHONE,
    "client_type": "council",
    "business_address": "123 Test Street, London, UK",
    "otp_method": "email"
}

result = test_api(
    "1. Register New Client",
    "POST",
    "/register/client",
    register_data,
    expected_status=200
)

if not result:
    print("\n❌ Registration failed. Cannot continue tests.")
    sys.exit(1)

print("\n⏳ Please check your email and enter the OTP:")
test_data["otp"] = input("Enter OTP: ").strip()

# Test 2: Verify OTP
print("\n" + "🔹" * 35)
print("PHASE 2: OTP VERIFICATION")
print("🔹" * 35)

verify_data = {
    "identifier": TEST_EMAIL,
    "otp": test_data["otp"]
}

result = test_api(
    "2. Verify OTP",
    "POST",
    "/verify-otp",
    verify_data,
    expected_status=200
)

if result and "access_token" in result:
    test_data["access_token"] = result["access_token"]
    test_data["refresh_token"] = result["refresh_token"]
    print(f"\n✅ Got access token: {test_data['access_token'][:30]}...")
else:
    print("\n⚠️ OTP verification failed. Testing resend OTP...")
    
    # Test 3: Resend OTP
    resend_data = {
        "identifier": TEST_EMAIL,
        "otp_method": "email"
    }
    
    result = test_api(
        "3. Resend OTP",
        "POST",
        "/resend-otp",
        resend_data,
        expected_status=200
    )
    
    if result:
        print("\n⏳ Please check your email again and enter the new OTP:")
        test_data["otp"] = input("Enter new OTP: ").strip()
        
        result = test_api(
            "4. Verify OTP (After Resend)",
            "POST",
            "/verify-otp",
            verify_data,
            expected_status=200
        )
        
        if result and "access_token" in result:
            test_data["access_token"] = result["access_token"]
            test_data["refresh_token"] = result["refresh_token"]

# Test 4: Login
print("\n" + "🔹" * 35)
print("PHASE 3: LOGIN")
print("🔹" * 35)

login_data = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD
}

result = test_api(
    "5. Login Client",
    "POST",
    "/login/client",
    login_data,
    expected_status=200
)

if result and "access_token" in result:
    test_data["access_token"] = result["access_token"]
    test_data["refresh_token"] = result["refresh_token"]
    print(f"\n✅ Login successful!")

# Test 5: Get Profile
print("\n" + "🔹" * 35)
print("PHASE 4: PROFILE ACCESS")
print("🔹" * 35)

if test_data["access_token"]:
    headers = {
        "Authorization": f"Bearer {test_data['access_token']}"
    }
    
    result = test_api(
        "6. Get Client Profile",
        "GET",
        "/client/profile",
        headers=headers,
        expected_status=200
    )

# Test 6: Refresh Token
print("\n" + "🔹" * 35)
print("PHASE 5: TOKEN REFRESH")
print("🔹" * 35)

if test_data["refresh_token"]:
    refresh_data = {
        "refresh_token": test_data["refresh_token"]
    }
    
    result = test_api(
        "7. Refresh Access Token",
        "POST",
        "/refresh",
        refresh_data,
        expected_status=200
    )
    
    if result and "access_token" in result:
        print(f"\n✅ Token refreshed successfully!")

# Test 7: Forgot Password Flow
print("\n" + "🔹" * 35)
print("PHASE 6: PASSWORD RESET")
print("🔹" * 35)

forgot_data = {
    "identifier": TEST_EMAIL,
    "otp_method": "email"
}

result = test_api(
    "8. Forgot Password",
    "POST",
    "/forgot-password",
    forgot_data,
    expected_status=200
)

# Test 8: Invalid Login
print("\n" + "🔹" * 35)
print("PHASE 7: NEGATIVE TESTS")
print("🔹" * 35)

invalid_login = {
    "email": TEST_EMAIL,
    "password": "WrongPassword123"
}

result = test_api(
    "9. Login with Wrong Password",
    "POST",
    "/login/client",
    invalid_login,
    expected_status=401
)

# Test 9: Duplicate Registration
duplicate_register = {
    "email": TEST_EMAIL,
    "password": TEST_PASSWORD,
    "full_name": "Duplicate User",
    "company_name": "Duplicate Company",
    "contact_person_name": "Jane Doe",
    "department": "Sales",
    "phone_number": "+447700900999",
    "client_type": "landlord",
    "business_address": "456 Another St",
    "otp_method": "email"
}

result = test_api(
    "10. Register with Existing Email",
    "POST",
    "/register/client",
    duplicate_register,
    expected_status=400
)

# Summary
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)
print(f"Test Email: {TEST_EMAIL}")
print(f"Test Password: {TEST_PASSWORD}")
print(f"Access Token: {'✅ Obtained' if test_data['access_token'] else '❌ Not obtained'}")
print(f"Refresh Token: {'✅ Obtained' if test_data['refresh_token'] else '❌ Not obtained'}")
print("=" * 70)
print("\n✅ All API tests completed!")
print("\nNOTE: Check server logs for background email sending status")
print("=" * 70)
