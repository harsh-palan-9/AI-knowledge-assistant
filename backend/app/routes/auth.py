from fastapi import APIRouter, HTTPException
import requests
import os
import logging
from app.models.request_models import LoginRequest

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/auth", tags=["Auth"])

KEYCLOAK_URL = "http://localhost:8080"
REALM = "ai-realm"
CLIENT_ID = "ai-client"


@router.post("/login")
def login(request: LoginRequest):
    username = request.username
    password = request.password

    url = f"{KEYCLOAK_URL}/realms/{REALM}/protocol/openid-connect/token"

    payload = {
        "client_id": CLIENT_ID,
        "username": username,
        "password": password,
        "grant_type": "password",
        "scope": "openid profile email"   
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    logger.debug(f"Auth login request for user: {username}")
    response = requests.post(url, data=payload, headers=headers)
    logger.debug(f"Keycloak token endpoint response status: {response.status_code}")

    if response.status_code != 200:
        logger.error(f"Login failed for user {username}: {response.text}")
        raise HTTPException(status_code=401, detail=response.text)

    logger.info(f"Login successful for user: {username}")
    return response.json()