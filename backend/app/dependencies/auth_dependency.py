import requests
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

KEYCLOAK_URL = "http://keycloak:8080"

REALM = "ai-realm"

def verify_token(token: str):
    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/userinfo"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")
    return response.json()

def get_current_user(credentials: str = Depends(security)):
    return verify_token(credentials.credentials)