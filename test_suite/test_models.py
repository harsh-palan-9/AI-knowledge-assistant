"""
Comprehensive test suite for request and response models
"""
import pytest
from pydantic import ValidationError
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.models.request_models import QueryRequest, LoginRequest
from app.models.response_models import QueryResponse


class TestQueryRequest:
    """Test QueryRequest model"""
    
    def test_query_request_valid(self):
        """Test valid QueryRequest"""
        request = QueryRequest(question="What is AI?")
        assert request.question == "What is AI?"
    
    def test_query_request_min_length(self):
        """Test QueryRequest with minimum valid length"""
        request = QueryRequest(question="ABC")
        assert request.question == "ABC"
    
    def test_query_request_exactly_min_length(self):
        """Test QueryRequest with exactly minimum length (3)"""
        request = QueryRequest(question="ABC")
        assert len(request.question) == 3
    
    def test_query_request_too_short(self):
        """Test QueryRequest with question below minimum length"""
        with pytest.raises(ValidationError):
            QueryRequest(question="AB")
    
    def test_query_request_empty(self):
        """Test QueryRequest with empty question"""
        with pytest.raises(ValidationError):
            QueryRequest(question="")
    
    def test_query_request_missing_field(self):
        """Test QueryRequest without question field"""
        with pytest.raises(ValidationError):
            QueryRequest()
    
    def test_query_request_from_dict(self):
        """Test QueryRequest from dictionary"""
        data = {"question": "What is AI?"}
        request = QueryRequest(**data)
        assert request.question == "What is AI?"
    
    def test_query_request_from_json(self):
        """Test QueryRequest from JSON string"""
        import json
        data = json.dumps({"question": "What is AI?"})
        parsed = json.loads(data)
        request = QueryRequest(**parsed)
        assert request.question == "What is AI?"
    
    def test_query_request_long_question(self):
        """Test QueryRequest with very long question"""
        long_question = "What is AI? " * 1000
        request = QueryRequest(question=long_question)
        assert request.question == long_question
    
    def test_query_request_with_special_chars(self):
        """Test QueryRequest with special characters"""
        request = QueryRequest(question="What is AI? áéíóú ñ € ©")
        assert "áéíóú" in request.question
    
    def test_query_request_with_newlines(self):
        """Test QueryRequest with newlines"""
        request = QueryRequest(question="What is AI?\nHow does it work?")
        assert "\n" in request.question
    
    def test_query_request_with_tabs(self):
        """Test QueryRequest with tabs"""
        request = QueryRequest(question="What is AI?\tHow does it work?")
        assert "\t" in request.question
    
    def test_query_request_with_quotes(self):
        """Test QueryRequest with quotes"""
        request = QueryRequest(question='What is "AI"?')
        assert '"' in request.question
    
    def test_query_request_model_dump(self):
        """Test QueryRequest model_dump method"""
        request = QueryRequest(question="What is AI?")
        dumped = request.model_dump()
        assert dumped == {"question": "What is AI?"}
    
    def test_query_request_model_dump_json(self):
        """Test QueryRequest model_dump_json method"""
        request = QueryRequest(question="What is AI?")
        json_str = request.model_dump_json()
        assert "What is AI?" in json_str
    
    def test_query_request_model_validate(self):
        """Test QueryRequest model_validate method"""
        data = {"question": "What is AI?"}
        request = QueryRequest.model_validate(data)
        assert request.question == "What is AI?"


class TestLoginRequest:
    """Test LoginRequest model"""
    
    def test_login_request_valid(self):
        """Test valid LoginRequest"""
        request = LoginRequest(username="testuser", password="testpass123")
        assert request.username == "testuser"
        assert request.password == "testpass123"
    
    def test_login_request_min_length_username(self):
        """Test LoginRequest with minimum valid username length"""
        request = LoginRequest(username="a", password="testpass")
        assert request.username == "a"
    
    def test_login_request_min_length_password(self):
        """Test LoginRequest with minimum valid password length"""
        request = LoginRequest(username="testuser", password="a")
        assert request.password == "a"
    
    def test_login_request_empty_username(self):
        """Test LoginRequest with empty username"""
        with pytest.raises(ValidationError):
            LoginRequest(username="", password="testpass")
    
    def test_login_request_empty_password(self):
        """Test LoginRequest with empty password"""
        with pytest.raises(ValidationError):
            LoginRequest(username="testuser", password="")
    
    def test_login_request_missing_username(self):
        """Test LoginRequest without username"""
        with pytest.raises(ValidationError):
            LoginRequest(password="testpass")
    
    def test_login_request_missing_password(self):
        """Test LoginRequest without password"""
        with pytest.raises(ValidationError):
            LoginRequest(username="testuser")
    
    def test_login_request_from_dict(self):
        """Test LoginRequest from dictionary"""
        data = {"username": "testuser", "password": "testpass123"}
        request = LoginRequest(**data)
        assert request.username == "testuser"
        assert request.password == "testpass123"
    
    def test_login_request_with_special_chars_username(self):
        """Test LoginRequest with special characters in username"""
        request = LoginRequest(username="user@domain.com", password="testpass")
        assert "@" in request.username
    
    def test_login_request_with_special_chars_password(self):
        """Test LoginRequest with special characters in password"""
        request = LoginRequest(username="testuser", password="p@ssw0rd!123")
        assert "@" in request.password
    
    def test_login_request_long_username(self):
        """Test LoginRequest with very long username"""
        long_username = "a" * 1000
        request = LoginRequest(username=long_username, password="testpass")
        assert request.username == long_username
    
    def test_login_request_long_password(self):
        """Test LoginRequest with very long password"""
        long_password = "x" * 1000
        request = LoginRequest(username="testuser", password=long_password)
        assert request.password == long_password
    
    def test_login_request_with_unicode(self):
        """Test LoginRequest with unicode characters"""
        request = LoginRequest(username="tëstüser", password="pässwörd")
        assert "tëstüser" == request.username
    
    def test_login_request_model_dump(self):
        """Test LoginRequest model_dump method"""
        request = LoginRequest(username="testuser", password="testpass")
        dumped = request.model_dump()
        assert dumped == {"username": "testuser", "password": "testpass"}
    
    def test_login_request_model_dump_json(self):
        """Test LoginRequest model_dump_json method"""
        request = LoginRequest(username="testuser", password="testpass")
        json_str = request.model_dump_json()
        assert "testuser" in json_str
        assert "testpass" in json_str
    
    def test_login_request_model_validate(self):
        """Test LoginRequest model_validate method"""
        data = {"username": "testuser", "password": "testpass"}
        request = LoginRequest.model_validate(data)
        assert request.username == "testuser"
        assert request.password == "testpass"


class TestQueryResponse:
    """Test QueryResponse model"""
    
    def test_query_response_valid(self):
        """Test valid QueryResponse"""
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer="AI is artificial intelligence"
        )
        assert response.user == "testuser"
        assert response.query == "What is AI?"
        assert response.answer == "AI is artificial intelligence"
    
    def test_query_response_from_dict(self):
        """Test QueryResponse from dictionary"""
        data = {
            "user": "testuser",
            "query": "What is AI?",
            "answer": "AI is artificial intelligence"
        }
        response = QueryResponse(**data)
        assert response.user == "testuser"
        assert response.query == "What is AI?"
        assert response.answer == "AI is artificial intelligence"
    
    def test_query_response_empty_fields(self):
        """Test QueryResponse with empty fields"""
        response = QueryResponse(user="", query="", answer="")
        assert response.user == ""
        assert response.query == ""
        assert response.answer == ""
    
    def test_query_response_long_answer(self):
        """Test QueryResponse with very long answer"""
        long_answer = "AI is artificial intelligence. " * 1000
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer=long_answer
        )
        assert response.answer == long_answer
    
    def test_query_response_with_special_chars(self):
        """Test QueryResponse with special characters"""
        response = QueryResponse(
            user="tëstüser",
            query="Whät is ÄI?",
            answer="ÄI is ärtificiäl intelligénce"
        )
        assert "tëstüser" == response.user
    
    def test_query_response_with_newlines(self):
        """Test QueryResponse with newlines in answer"""
        answer = "AI is artificial intelligence.\nIt uses machine learning.\nIt can learn from data."
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer=answer
        )
        assert "\n" in response.answer
    
    def test_query_response_model_dump(self):
        """Test QueryResponse model_dump method"""
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer="AI is artificial intelligence"
        )
        dumped = response.model_dump()
        assert dumped == {
            "user": "testuser",
            "query": "What is AI?",
            "answer": "AI is artificial intelligence"
        }
    
    def test_query_response_model_dump_json(self):
        """Test QueryResponse model_dump_json method"""
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer="AI is artificial intelligence"
        )
        json_str = response.model_dump_json()
        assert "testuser" in json_str
        assert "What is AI?" in json_str
    
    def test_query_response_model_validate(self):
        """Test QueryResponse model_validate method"""
        data = {
            "user": "testuser",
            "query": "What is AI?",
            "answer": "AI is artificial intelligence"
        }
        response = QueryResponse.model_validate(data)
        assert response.user == "testuser"
        assert response.query == "What is AI?"


class TestModelsEdgeCases:
    """Test edge cases for models"""
    
    def test_query_request_with_numbers(self):
        """Test QueryRequest with numbers in question"""
        request = QueryRequest(question="What is AI in 2024?")
        assert "2024" in request.question
    
    def test_query_request_with_emoji(self):
        """Test QueryRequest with emoji"""
        request = QueryRequest(question="What is AI? 🤖")
        assert "🤖" in request.question
    
    def test_login_request_with_email_username(self):
        """Test LoginRequest with email as username"""
        request = LoginRequest(username="user@example.com", password="pass123")
        assert "@" in request.username
    
    def test_login_request_with_underscore_username(self):
        """Test LoginRequest with underscore in username"""
        request = LoginRequest(username="test_user", password="pass123")
        assert "_" in request.username
    
    def test_query_response_with_html_entities(self):
        """Test QueryResponse with HTML entities in answer"""
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer="AI is &lt;artificial&gt; intelligence"
        )
        assert "&lt;" in response.answer
    
    def test_query_response_with_json_like_content(self):
        """Test QueryResponse with JSON-like content in answer"""
        answer = '{"key": "value", "nested": {"item": "data"}}'
        response = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer=answer
        )
        assert response.answer == answer
    
    def test_query_request_with_url(self):
        """Test QueryRequest with URL in question"""
        request = QueryRequest(question="What is https://example.com?")
        assert "https://" in request.question
    
    def test_login_request_whitespace(self):
        """Test LoginRequest with whitespace handling"""
        request = LoginRequest(username="  testuser  ", password="  pass  ")
        # Pydantic doesn't strip by default, so this tests the raw value
        assert "  testuser  " == request.username


class TestModelsSerialization:
    """Test model serialization and deserialization"""
    
    def test_query_request_serialize_deserialize(self):
        """Test QueryRequest serialization round-trip"""
        original = QueryRequest(question="What is AI?")
        dumped = original.model_dump()
        restored = QueryRequest(**dumped)
        assert restored.question == original.question
    
    def test_login_request_serialize_deserialize(self):
        """Test LoginRequest serialization round-trip"""
        original = LoginRequest(username="testuser", password="testpass")
        dumped = original.model_dump()
        restored = LoginRequest(**dumped)
        assert restored.username == original.username
        assert restored.password == original.password
    
    def test_query_response_serialize_deserialize(self):
        """Test QueryResponse serialization round-trip"""
        original = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer="AI is artificial intelligence"
        )
        dumped = original.model_dump()
        restored = QueryResponse(**dumped)
        assert restored.user == original.user
        assert restored.query == original.query
        assert restored.answer == original.answer
    
    def test_query_request_json_serialize_deserialize(self):
        """Test QueryRequest JSON serialization round-trip"""
        original = QueryRequest(question="What is AI?")
        json_str = original.model_dump_json()
        restored = QueryRequest.model_validate_json(json_str)
        assert restored.question == original.question
    
    def test_login_request_json_serialize_deserialize(self):
        """Test LoginRequest JSON serialization round-trip"""
        original = LoginRequest(username="testuser", password="testpass")
        json_str = original.model_dump_json()
        restored = LoginRequest.model_validate_json(json_str)
        assert restored.username == original.username
        assert restored.password == original.password
    
    def test_query_response_json_serialize_deserialize(self):
        """Test QueryResponse JSON serialization round-trip"""
        original = QueryResponse(
            user="testuser",
            query="What is AI?",
            answer="AI is artificial intelligence"
        )
        json_str = original.model_dump_json()
        restored = QueryResponse.model_validate_json(json_str)
        assert restored.user == original.user
        assert restored.query == original.query
        assert restored.answer == original.answer


class TestModelsWithExtraFields:
    """Test models with extra fields"""
    
    def test_query_request_with_extra_field(self):
        """Test QueryRequest with extra field (should be ignored by default)"""
        data = {"question": "What is AI?", "extra_field": "value"}
        request = QueryRequest(**data)
        assert request.question == "What is AI?"
        assert not hasattr(request, "extra_field") or request.model_dump().get("extra_field") is None
    
    def test_login_request_with_extra_field(self):
        """Test LoginRequest with extra field (should be ignored by default)"""
        data = {"username": "testuser", "password": "testpass", "extra_field": "value"}
        request = LoginRequest(**data)
        assert request.username == "testuser"
        assert request.password == "testpass"
    
    def test_query_response_with_extra_field(self):
        """Test QueryResponse with extra field (should be ignored by default)"""
        data = {
            "user": "testuser",
            "query": "What is AI?",
            "answer": "AI is artificial intelligence",
            "extra_field": "value"
        }
        response = QueryResponse(**data)
        assert response.user == "testuser"
        assert response.query == "What is AI?"
        assert response.answer == "AI is artificial intelligence"
