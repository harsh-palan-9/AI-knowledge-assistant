import requests
import streamlit as st
import jwt
import time
import logging

logger = logging.getLogger(__name__)

BASE_URL = "http://localhost:8000"


# ---------------- LOGIN ----------------
def login(username, password):
    url = "http://localhost:8080/realms/ai-realm/protocol/openid-connect/token"

    data = {
        "client_id": "ai-client",
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "openid profile email"  # Include openid scope for userinfo endpoint
    }

    logger.debug(f"Login attempt for user: {username}")
    logger.debug(f"Requesting token with scopes: openid profile email")
    
    response = requests.post(url, data=data)
    result = response.json()
    result["status_code"] = response.status_code
    
    if response.status_code == 200:
        logger.info(f"Login successful for user: {username}")
        logger.debug(f"Token received (preview): {result.get('access_token', '')[:20]}...")
    else:
        logger.error(f"Login failed - Status: {response.status_code}, Error: {result.get('error_description', result.get('error'))}")

    return result


# ---------------- TOKEN VALIDATION ----------------
def validate_token(token):
    if not token:
        return False

    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return time.time() < decoded.get("exp", 0)
    except:
        return False


# ---------------- SESSION ----------------
def clear_session():
    st.session_state.clear()


# ---------------- UPLOAD ----------------
def upload_file(file):
    token = st.session_state.get("token", "")
    logger.debug(f"Upload attempt - Token exists: {bool(token)}")
    logger.debug(f"Token preview: {token[:20]}..." if token else "No token")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    logger.debug(f"Request headers: {{'Authorization': 'Bearer {token[:20]}...'}}")

    files = {"file": (file.name, file.getvalue())}

    logger.info(f"Sending upload request to {BASE_URL}/document/upload/")
    response = requests.post(
        f"{BASE_URL}/document/upload/",
        files=files,
        headers=headers
    )

    logger.debug(f"Upload response status: {response.status_code}")
    logger.debug(f"Upload response headers: {response.headers}")
    
    if response.status_code == 401:
        logger.error("401 Unauthorized - Token may be invalid or expired")
        logger.debug(f"Response text: {response.text}")
        clear_session()
        return {"error": "Session expired", "status_code": 401, "message": "Token invalid or expired"}

    logger.debug(f"Upload response body: {response.text}")
    return response.json()


# ---------------- QUERY ----------------
def ask_question(query):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.post(
        f"{BASE_URL}/query/",
        json={"question": query},
        headers=headers
    )

    if response.status_code == 401:
        clear_session()
        return {"error": "Session expired", "status_code": 401}

    return response.json()