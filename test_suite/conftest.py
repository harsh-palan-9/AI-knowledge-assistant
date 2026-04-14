"""
Shared fixtures and configuration for test suite
"""
import pytest
import os
import sys
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture
def mock_keycloak_response():
    """Mock successful Keycloak token response"""
    return {
        "access_token": "test_token_123",
        "refresh_token": "refresh_token_123",
        "token_type": "Bearer",
        "expires_in": 3600,
        "id_token": "id_token_123"
    }


@pytest.fixture
def mock_keycloak_userinfo():
    """Mock successful Keycloak userinfo response"""
    return {
        "sub": "user123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "realm_access": {
            "roles": ["user"]
        }
    }


@pytest.fixture
def mock_user_info():
    """Mock user info from token verification"""
    return {
        "sub": "user123",
        "preferred_username": "testuser",
        "email": "test@example.com",
        "realm_access": {
            "roles": ["user"]
        }
    }


@pytest.fixture
def mock_pdf_file():
    """Create a mock PDF file for upload testing"""
    from fastapi import UploadFile
    
    # Create a simple PDF content (minimal valid PDF)
    pdf_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Count 1\n/Kids [3 0 R]\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f\n0000000009 00000 n\n0000000058 00000 n\n0000000115 00000 n\ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n174\n%%EOF"
    
    file = UploadFile(filename="test.pdf", file=BytesIO(pdf_content))
    return file


@pytest.fixture
def mock_txt_file():
    """Create a mock TXT file for upload testing"""
    from fastapi import UploadFile
    
    txt_content = b"This is a test document content.\nIt has multiple lines.\nTesting text processing."
    
    file = UploadFile(filename="test.txt", file=BytesIO(txt_content))
    return file


@pytest.fixture
def mock_unsupported_file():
    """Create a mock unsupported file for testing error cases"""
    from fastapi import UploadFile
    
    file = UploadFile(filename="test.docx", file=BytesIO(b"fake docx content"))
    return file


@pytest.fixture
def mock_retrieved_documents():
    """Mock retrieved documents from vector store"""
    from langchain_core.documents import Document
    
    return [
        Document(page_content="Test document content 1"),
        Document(page_content="Test document content 2"),
        Document(page_content="Test document content 3")
    ]


@pytest.fixture
def mock_embeddings():
    """Mock embeddings for testing"""
    import numpy as np
    return [np.array([0.1, 0.2, 0.3, 0.4, 0.5])]


@pytest.fixture
def mock_llm_response():
    """Mock LLM response for testing"""
    return "This is a test answer based on the context provided."


@pytest.fixture
def mock_pinecone_index():
    """Mock Pinecone index"""
    index = Mock()
    index.upsert = Mock(return_value={"upserted_count": 3})
    index.query = Mock(return_value={
        "matches": [
            {"id": "1", "score": 0.9, "metadata": {"text": "content1"}},
            {"id": "2", "score": 0.8, "metadata": {"text": "content2"}}
        ]
    })
    return index


@pytest.fixture
def mock_groq_client():
    """Mock Groq client"""
    client = Mock()
    mock_response = Mock()
    mock_response.choices = [Mock()]
    mock_response.choices[0].message.content = "Test LLM response"
    client.chat.completions.create = Mock(return_value=mock_response)
    return client


@pytest.fixture
def sample_query_request():
    """Sample query request"""
    return {
        "question": "What is the main topic?"
    }


@pytest.fixture
def sample_login_request():
    """Sample login request"""
    return {
        "username": "testuser",
        "password": "testpass123"
    }


@pytest.fixture
def temp_upload_dir(tmp_path):
    """Create a temporary upload directory"""
    upload_dir = tmp_path / "uploads"
    upload_dir.mkdir()
    return str(upload_dir)


@pytest.fixture
def mock_env_vars():
    """Mock environment variables"""
    with patch.dict(os.environ, {
        'KEYCLOAK_URL': 'http://localhost:8080',
        'KEYCLOAK_REALM': 'ai-realm',
        'PINECONE_API_KEY': 'test-pinecone-key',
        'PINECONE_INDEX': 'test-index',
        'GROQ_API_KEY': 'test-groq-key'
    }):
        yield


@pytest.fixture
def mock_requests_post():
    """Mock requests.post for external API calls"""
    with patch('requests.post') as mock_post:
        yield mock_post


@pytest.fixture
def mock_requests_get():
    """Mock requests.get for external API calls"""
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture(autouse=True)
def cleanup_upload_dir():
    """Cleanup upload directory after tests"""
    yield
    # Clean up uploads directory if it exists
    upload_dir = "uploads"
    if os.path.exists(upload_dir):
        import shutil
        try:
            shutil.rmtree(upload_dir)
        except:
            pass
