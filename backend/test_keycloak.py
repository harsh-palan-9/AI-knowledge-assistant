#!/usr/bin/env python3
"""
Diagnostic script to test Keycloak token verification
"""
import requests
import os
import json

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
REALM = os.getenv("KEYCLOAK_REALM", "ai-realm")

# Test token - you can get this from login and paste it here
# For automated testing, use a mock token
TEST_TOKEN = "mock_test_token_for_testing_purposes"

if not TEST_TOKEN:
    print("No token provided. Exiting.")
    exit(1)

print(f"\n{'='*60}")
print("KEYCLOAK DIAGNOSTIC TEST")
print(f"{'='*60}")
print(f"Keycloak URL: {KEYCLOAK_URL}")
print(f"Realm: {REALM}")
print(f"Token (first 50 chars): {TEST_TOKEN[:50]}...")
print(f"{'='*60}\n")

# Test 1: Get token endpoint
print("[TEST 1] Testing token endpoint availability...")
token_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"
print(f"URL: {token_url}")
try:
    response = requests.get(token_url)
    print(f"Status: {response.status_code}")
    print(f"Result: {'✓ Endpoint reachable' if response.status_code in [400, 405] else '✗ Endpoint issue'}")
except Exception as e:
    print(f"✗ Error: {e}")

print()

# Test 2: Verify token endpoint
print("[TEST 2] Verifying token against userinfo endpoint...")
userinfo_url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"
print(f"URL: {userinfo_url}")

headers = {
    "Authorization": f"Bearer {TEST_TOKEN}"
}

try:
    response = requests.get(userinfo_url, headers=headers, timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"Body: {response.text}")
    
    if response.status_code == 200:
        print(f"✓ Token is valid!")
        print(f"User info: {json.dumps(response.json(), indent=2)}")
    else:
        print(f"✗ Token verification failed")
        try:
            print(f"Error details: {json.dumps(response.json(), indent=2)}")
        except:
            pass
except Exception as e:
    print(f"✗ Request error: {e}")

print()

# Test 3: Check realm info
print("[TEST 3] Getting realm public config...")
config_url = f"{KEYCLOAK_URL}/realms/{REALM}/.well-known/openid-configuration"
print(f"URL: {config_url}")

try:
    response = requests.get(config_url, timeout=5)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        config = response.json()
        print(f"✓ Realm config found")
        print(f"Token endpoint: {config.get('token_endpoint')}")
        print(f"Userinfo endpoint: {config.get('userinfo_endpoint')}")
        print(f"Authorization endpoint: {config.get('authorization_endpoint')}")
        print(f"Issuer: {config.get('issuer')}")
    else:
        print(f"✗ Could not get realm config")
        print(f"Response: {response.text}")
except Exception as e:
    print(f"✗ Error: {e}")

print(f"\n{'='*60}")
print("DIAGNOSTIC COMPLETE")
print(f"{'='*60}")
