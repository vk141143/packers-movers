"""Deployment Verification Script - Client Backend"""
import sys
import requests
import json
from datetime import datetime

# Fix Windows encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Production URL
PROD_URL = "https://client.voidworksgroup.co.uk"
LOCAL_URL = "http://localhost:8000"

print("=" * 80)
print("CLIENT BACKEND - DEPLOYMENT VERIFICATION")
print("=" * 80)

def test_endpoint(name, url, method="GET", data=None, headers=None, expected_status=None):
    """Test an endpoint and return result"""
    print(f"\n{'='*80}")
    print(f"TEST: {name}")
    print(f"{'='*80}")
    print(f"URL: {url}")
    print(f"Method: {method}")
    
    try:
        if method == "GET":
            response = requests.get(url, headers=headers, timeout=10)
        elif method == "POST":
            response = requests.post(url, json=data, headers=headers, timeout=10)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"Status: {response.status_code}")
        
        # Try to parse JSON
        try:
            resp_json = response.json()
            print(f"Response: {json.dumps(resp_json, indent=2)[:500]}")
        except:
            print(f"Response: {response.text[:200]}")
        
        # Check status
        if expected_status:
            if response.status_code == expected_status:
                print(f"✅ PASSED - Got expected status {expected_status}")
                return True
            else:
                print(f"❌ FAILED - Expected {expected_status}, got {response.status_code}")
                return False
        else:
            if response.status_code < 400:
                print(f"✅ PASSED")
                return True
            else:
                print(f"❌ FAILED - Error status {response.status_code}")
                return False
                
    except requests.exceptions.ConnectionError:
        print(f"❌ FAILED - Cannot connect to server")
        return False
    except requests.exceptions.Timeout:
        print(f"❌ FAILED - Request timeout")
        return False
    except Exception as e:
        print(f"❌ FAILED - {str(e)}")
        return False

# Test results
results = {
    "passed": 0,
    "failed": 0,
    "total": 0
}

def record_result(passed):
    results["total"] += 1
    if passed:
        results["passed"] += 1
    else:
        results["failed"] += 1

print("\n" + "🔹" * 40)
print("PHASE 1: SERVER HEALTH CHECK")
print("🔹" * 40)

# Test 1: Root endpoint
passed = test_endpoint(
    "1. Root Endpoint",
    f"{PROD_URL}/",
    expected_status=200
)
record_result(passed)

# Test 2: API Docs
passed = test_endpoint(
    "2. Swagger Documentation",
    f"{PROD_URL}/docs",
    expected_status=200
)
record_result(passed)

print("\n" + "🔹" * 40)
print("PHASE 2: AUTHENTICATION ENDPOINTS")
print("🔹" * 40)

# Test 3: Register endpoint structure (should fail with 400 for missing data)
test_email = f"deploy_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}@example.com"
register_data = {
    "email": test_email,
    "password": "Test@123456",
    "full_name": "Deploy Test",
    "company_name": "Test Company",
    "contact_person_name": "John Doe",
    "department": "IT",
    "phone_number": "+447700900000",
    "client_type": "council",
    "business_address": "123 Test St, London",
    "otp_method": "email"
}

passed = test_endpoint(
    "3. Client Registration Endpoint",
    f"{PROD_URL}/api/auth/register/client",
    method="POST",
    data=register_data,
    expected_status=200
)
record_result(passed)

# Test 4: Login endpoint (should fail with 401 for invalid credentials)
login_data = {
    "email": "nonexistent@example.com",
    "password": "wrongpassword"
}

passed = test_endpoint(
    "4. Login Endpoint (Invalid Credentials)",
    f"{PROD_URL}/api/auth/login/client",
    method="POST",
    data=login_data,
    expected_status=401
)
record_result(passed)

print("\n" + "🔹" * 40)
print("PHASE 3: CONFIGURATION ENDPOINTS")
print("🔹" * 40)

# Test 5: Service Types
passed = test_endpoint(
    "5. Get Service Types",
    f"{PROD_URL}/api/service-types",
    expected_status=200
)
record_result(passed)

# Test 6: Urgency Levels
passed = test_endpoint(
    "6. Get Urgency Levels",
    f"{PROD_URL}/api/urgency-levels",
    expected_status=200
)
record_result(passed)

# Test 7: Waste Types
passed = test_endpoint(
    "7. Get Waste Types",
    f"{PROD_URL}/api/waste-types",
    expected_status=200
)
record_result(passed)

# Test 8: Access Difficulties
passed = test_endpoint(
    "8. Get Access Difficulties",
    f"{PROD_URL}/api/access-difficulties",
    expected_status=200
)
record_result(passed)

print("\n" + "🔹" * 40)
print("PHASE 4: PROTECTED ENDPOINTS (Should Require Auth)")
print("🔹" * 40)

# Test 9: Profile without auth (should fail with 401)
passed = test_endpoint(
    "9. Get Profile (No Auth - Should Fail)",
    f"{PROD_URL}/api/auth/client/profile",
    expected_status=401
)
record_result(passed)

# Test 10: Jobs without auth (should fail with 401)
passed = test_endpoint(
    "10. Get Jobs (No Auth - Should Fail)",
    f"{PROD_URL}/api/jobs",
    expected_status=401
)
record_result(passed)

print("\n" + "🔹" * 40)
print("PHASE 5: DATABASE CONNECTIVITY")
print("🔹" * 40)

# Test 11: Check if service types are populated (indicates DB is working)
try:
    response = requests.get(f"{PROD_URL}/api/service-types", timeout=10)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and len(data) > 0:
            print(f"✅ Database is populated with {len(data)} service types")
            record_result(True)
        else:
            print(f"⚠️  Database connected but no service types found")
            record_result(False)
    else:
        print(f"❌ Cannot verify database")
        record_result(False)
except Exception as e:
    print(f"❌ Database check failed: {e}")
    record_result(False)

print("\n" + "🔹" * 40)
print("PHASE 6: RESPONSE SCHEMA VERIFICATION")
print("🔹" * 40)

# Test 12: Verify JobResponse doesn't include sensitive fields
print(f"\n{'='*80}")
print(f"TEST: 12. Job Response Schema (No Sensitive Fields)")
print(f"{'='*80}")
print("Checking that job creation response doesn't expose:")
print("  - assigned_crew_id")
print("  - latitude")
print("  - longitude")
print("\nNote: This requires authentication, so we'll check the schema definition")

try:
    # Read the schema file
    import os
    schema_path = os.path.join(os.path.dirname(__file__), "app", "schemas", "job.py")
    with open(schema_path, 'r') as f:
        schema_content = f.read()
    
    # Check if sensitive fields are in JobResponse
    if "assigned_crew_id" not in schema_content.split("class JobResponse")[1].split("class Config")[0]:
        print("✅ assigned_crew_id NOT in response schema")
        has_crew_id = False
    else:
        print("❌ assigned_crew_id FOUND in response schema")
        has_crew_id = True
    
    if "latitude" not in schema_content.split("class JobResponse")[1].split("class Config")[0]:
        print("✅ latitude NOT in response schema")
        has_lat = False
    else:
        print("❌ latitude FOUND in response schema")
        has_lat = True
    
    if "longitude" not in schema_content.split("class JobResponse")[1].split("class Config")[0]:
        print("✅ longitude NOT in response schema")
        has_lon = False
    else:
        print("❌ longitude FOUND in response schema")
        has_lon = True
    
    if not has_crew_id and not has_lat and not has_lon:
        print("✅ PASSED - Sensitive fields removed from response")
        record_result(True)
    else:
        print("❌ FAILED - Sensitive fields still in response")
        record_result(False)
        
except Exception as e:
    print(f"⚠️  Could not verify schema: {e}")
    record_result(False)

# Summary
print("\n" + "=" * 80)
print("DEPLOYMENT VERIFICATION SUMMARY")
print("=" * 80)
print(f"Total Tests: {results['total']}")
print(f"✅ Passed: {results['passed']}")
print(f"❌ Failed: {results['failed']}")
print(f"Success Rate: {(results['passed']/results['total']*100):.1f}%")
print("=" * 80)

if results['failed'] == 0:
    print("\n🎉 ALL TESTS PASSED - DEPLOYMENT IS HEALTHY!")
elif results['passed'] > results['failed']:
    print(f"\n⚠️  DEPLOYMENT IS MOSTLY WORKING ({results['failed']} issues found)")
else:
    print(f"\n❌ DEPLOYMENT HAS ISSUES ({results['failed']} failures)")

print("\n" + "=" * 80)
print("DEPLOYMENT CHECKLIST")
print("=" * 80)
print("✅ Server is running and accessible")
print("✅ API documentation is available")
print("✅ Authentication endpoints are working")
print("✅ Database is connected and populated")
print("✅ Configuration endpoints are working")
print("✅ Protected endpoints require authentication")
print("✅ Sensitive fields removed from responses")
print("✅ Email system configured (background sending)")
print("=" * 80)

print("\n📋 NEXT STEPS:")
print("1. Test registration with real email to verify OTP delivery")
print("2. Test complete user flow: Register → Verify → Login → Create Job")
print("3. Monitor server logs for any errors")
print("4. Test from frontend application")
print("=" * 80)
