import requests

BASE_URL = "http://127.0.0.1:8000"

def upload_file(file):
    files = {"file": (file.name, file.getvalue())}
    response = requests.post(f"{BASE_URL}/upload/", files=files)
    return response.json()


def ask_question(query):
    response = requests.get(f"{BASE_URL}/query/", params={"q": query})
    return response.json()
