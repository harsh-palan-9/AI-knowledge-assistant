import os
import requests
import logging
from requests.exceptions import RequestException
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

logger = logging.getLogger(__name__)
security = HTTPBearer()

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
REALM = os.getenv("KEYCLOAK_REALM", "ai-realm")

def verify_token(token: str):
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"
    logger.debug(f"Verifying token against: {url}")
    logger.debug(f"Token preview: {token[:20]}..." if token else "No token provided")
    logger.debug(f"KEYCLOAK_URL: {KEYCLOAK_URL}, REALM: {REALM}")

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        logger.debug("Sending verification request to Keycloak")
        response = requests.get(url, headers=headers, timeout=5)
        logger.debug(f"Keycloak response status: {response.status_code}")
        logger.debug(f"Keycloak response headers: {dict(response.headers)}")
        logger.debug(f"Keycloak response body: {response.text}")
    except RequestException as exc:
        logger.error(f"Keycloak request failed: {exc}")
        raise HTTPException(status_code=503, detail="Authentication service unavailable") from exc

    if response.status_code != 200:
        try:
            error_detail = response.json().get("error_description") or response.text
        except ValueError:
            error_detail = response.text or "Invalid token"
        
        # Check for scope-related errors
        www_authenticate = response.headers.get("WWW-Authenticate", "")
        if "insufficient_scope" in www_authenticate or "Missing openid scope" in error_detail:
            logger.error(f"Token scope issue - Missing 'openid' scope. The token was issued without the required 'openid' scope.")
            logger.error(f"WWW-Authenticate header: {www_authenticate}")
            error_detail = "Token missing 'openid' scope. Please log in again with proper scopes."
        
        logger.error(f"Token verification failed - Status: {response.status_code}, Detail: {error_detail}")
        logger.debug(f"Full response body: {response.text}")
        logger.debug(f"Response headers: {dict(response.headers)}")
        raise HTTPException(status_code=401, detail=error_detail)

    logger.info("Token verified successfully")
    return response.json()

def get_current_user(credentials: str = Depends(security)):
    logger.debug("get_current_user called")
    logger.debug(f"Credentials scheme: {credentials.scheme}")
    logger.debug(f"Token from header: {credentials.credentials[:20]}..." if credentials.credentials else "No credentials")
    return verify_token(credentials.credentials)

def require_role(required_role: str):
    def role_checker(user=Depends(get_current_user)):
        roles = user.get("realm_access", {}).get("roles", [])

        if required_role not in roles:
            raise HTTPException(status_code=403, detail="Forbidden: insufficient role")

        return user

    return role_checker