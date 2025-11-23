import requests
import time
import subprocess
import sys

# Configuration
NEXUS_URL = "http://127.0.0.1:5001"
BACKEND_URL = "http://127.0.0.1:6021"
INTERNAL_KEY = "nexus-internal-secret-key-123"

def check_server(url, name):
    try:
        requests.get(url)
        print(f"✅ {name} is running")
        return True
    except:
        print(f"❌ {name} is NOT running")
        return False

def test_integration():
    print("--- Starting Integration Test ---")
    
    # 1. Test Nexus Direct Access (Should fail without key)
    print("\n1. Testing Nexus Security...")
    res = requests.get(f"{NEXUS_URL}/users/")
    if res.status_code == 401:
        print("✅ Nexus rejected request without API Key")
    else:
        print(f"❌ Nexus allowed request without key! Status: {res.status_code}")

    # 2. Test Nexus with Key
    print("\n2. Testing Nexus with Key...")
    res = requests.get(f"{NEXUS_URL}/users/", headers={"X-Internal-Key": INTERNAL_KEY})
    if res.status_code == 200:
        print("✅ Nexus accepted request with API Key")
    else:
        print(f"❌ Nexus rejected valid key! Status: {res.status_code}")

    # 3. Test Backend Signup (Should trigger Nexus Create)
    print("\n3. Testing Backend Signup -> Nexus Create...")
    email = f"test_{int(time.time())}@example.com"
    payload = {
        "email": email,
        "FirstName": "Test",
        "LastName": "User",
        "Password": "Password123!",
        "DateOfBirth": "1990-01-01",
        "Address": "123 Test St"
    }
    
    try:
        res = requests.post(f"{BACKEND_URL}/signup", json=payload)
        if res.status_code == 200:
            print("✅ Backend Signup Successful")
            
            # Verify in Nexus
            res_nexus = requests.get(f"{NEXUS_URL}/users/?role=employee", headers={"X-Internal-Key": INTERNAL_KEY})
            users = res_nexus.json()['data']
            found = any(u['email'] == email for u in users)
            if found:
                print("✅ User found in Nexus Database (Integration Works!)")
            else:
                print("❌ User NOT found in Nexus Database")
        else:
            print(f"❌ Backend Signup Failed: {res.text}")
    except Exception as e:
        print(f"❌ Backend Connection Error: {e}")

if __name__ == "__main__":
    if check_server(NEXUS_URL, "Nexus API") and check_server(BACKEND_URL, "Backend App"):
        test_integration()
    else:
        print("\nPlease start both servers manually before running this test.")
