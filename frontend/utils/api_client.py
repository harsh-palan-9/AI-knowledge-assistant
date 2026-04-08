import requests
import streamlit as st

BASE_URL = "http://localhost:8000"

def login(username, password):
    url = "http://localhost:8080/realms/ai-realm/protocol/openid-connect/token"

    data = {
        "client_id": "ai-client",
        "client_secret": "your-client-secret",
        "username": username,
        "password": password,
        "grant_type": "password"
    }
    response = requests.post(url, data=data)
    return response.json()


def upload_file(file):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    files = {"file": (file.name, file.getvalue())}
    response = requests.post(f"{BASE_URL}/upload/", files=files, headers=headers)
    return response.json()


def ask_question(query):
    headers = {
        "Authorization": f"Bearer {st.session_state.token}"
    }

    response = requests.get(f"{BASE_URL}/query/", params={"q": query}, headers=headers)
    return response.json()
