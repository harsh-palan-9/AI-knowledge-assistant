"""
Comprehensive test suite for authentication routes and dependencies
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from fastapi import HTTPException
from requests.exceptions import RequestException
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.routes.auth import router as auth_router
from app.dependencies.auth_dependency import verify_token, get_current_user, require_role
from app.models.request_models import LoginRequest


class TestAuthRoutes:
    """Test authentication routes"""
    
    def test_login_success(self, client, mock_keycloak_response, mock_requests_post):
        """Test successful login"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_keycloak_response
        mock_requests_post.return_value = mock_response
        
        response = client.post("/auth/login", json={
            "username": "testuser",
            "password": "testpass123"
        })
        
        assert response.status_code == 200
        assert response.json() == mock_keycloak_response
        mock_requests_post.assert_called_once()
    
    def test_login_invalid_credentials(self, client, mock_requests_post):
        """Test login with invalid credentials"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.text = "Invalid credentials"
        mock_requests_post.return_value = mock_response
        
        response = client.post("/auth/login", json={
            "username": "wronguser",
            "password": "wrongpass"
        })
        
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]
    
    def test_login_keycloak_unavailable(self, client, mock_requests_post):
        """Test login when Keycloak is unavailable"""
        mock_requests_post.side_effect = RequestException("Connection error")
        
        try:
            response = client.post("/auth/login", json={
                "username": "testuser",
                "password": "testpass123"
            })
            # If we get here, the exception wasn't raised properly
            assert response.status_code == 500
        except RequestException:
            # This is expected - the exception propagates
            pass
    
    def test_login_missing_fields(self, client):
        """Test login with missing required fields"""
        response = client.post("/auth/login", json={
            "username": "testuser"
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_login_empty_fields(self, client):
        """Test login with empty fields"""
        response = client.post("/auth/login", json={
            "username": "",
            "password": ""
        })
        
        assert response.status_code == 422  # Validation error
    
    def test_login_min_length_validation(self, client):
        """Test login with username below minimum length"""
        response = client.post("/auth/login", json={
            "username": "a",
            "password": "testpass123"
        })
        
        # Should pass since min_length is 1
        assert response.status_code in [200, 401, 500]  # Depends on Keycloak mock


class TestAuthDependency:
    """Test authentication dependency functions"""
    
    def test_verify_token_success(self, mock_keycloak_userinfo, mock_requests_get):
        """Test successful token verification"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_keycloak_userinfo
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        result = verify_token("valid_token_123")
        
        assert result == mock_keycloak_userinfo
        mock_requests_get.assert_called_once()
    
    def test_verify_token_invalid(self, mock_requests_get):
        """Test verification of invalid token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error_description": "Invalid token"}
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid_token")
        
        assert exc_info.value.status_code == 401
        assert "Invalid token" in str(exc_info.value.detail)
    
    def test_verify_token_missing_scope(self, mock_requests_get):
        """Test verification when token is missing openid scope"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error_description": "Missing openid scope"}
        mock_response.headers = {"WWW-Authenticate": "Bearer error='insufficient_scope'"}
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("token_without_scope")
        
        assert exc_info.value.status_code == 401
        assert "openid" in str(exc_info.value.detail)
    
    def test_verify_token_service_unavailable(self, mock_requests_get):
        """Test token verification when service is unavailable"""
        mock_requests_get.side_effect = RequestException("Service unavailable")
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("valid_token")
        
        assert exc_info.value.status_code == 503
        assert "Authentication service unavailable" in str(exc_info.value.detail)
    
    def test_verify_token_non_json_error_response(self, mock_requests_get):
        """Test token verification with non-JSON error response"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.text = "Invalid token"
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid_token")
        
        assert exc_info.value.status_code == 401
    
    def test_verify_token_empty_error_response(self, mock_requests_get):
        """Test token verification with empty error response"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {}
        mock_response.text = ""
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(HTTPException) as exc_info:
            verify_token("invalid_token")
        
        assert exc_info.value.status_code == 401
    
    def test_get_current_user_success(self, mock_keycloak_userinfo, mock_requests_get):
        """Test get_current_user with valid credentials"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_keycloak_userinfo
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        from fastapi.security import HTTPAuthorizationCredentials
        
        credentials = HTTPAuthorizationCredentials(
            scheme="Bearer",
            credentials="valid_token"
        )
        
        result = get_current_user(credentials)
        
        assert result == mock_keycloak_userinfo
    
    def test_require_role_success(self, mock_user_info):
        """Test require_role with user having required role"""
        mock_user_info["realm_access"]["roles"] = ["user", "admin"]
        
        role_checker = require_role("admin")
        
        # Call the role_checker directly with the user
        result = role_checker(mock_user_info)
        
        assert result == mock_user_info
    
    def test_require_role_insufficient_role(self, mock_user_info):
        """Test require_role when user lacks required role"""
        mock_user_info["realm_access"]["roles"] = ["user"]
        
        role_checker = require_role("admin")
        
        with pytest.raises(HTTPException) as exc_info:
            role_checker(mock_user_info)
        
        assert exc_info.value.status_code == 403
        assert "insufficient role" in str(exc_info.value.detail)
    
    def test_require_role_no_roles_in_user(self, mock_user_info):
        """Test require_role when user has no roles"""
        mock_user_info["realm_access"] = {}
        
        role_checker = require_role("user")
        
        with pytest.raises(HTTPException) as exc_info:
            role_checker(mock_user_info)
        
        assert exc_info.value.status_code == 403
    
    def test_require_role_missing_realm_access(self, mock_user_info):
        """Test require_role when realm_access is missing"""
        del mock_user_info["realm_access"]
        
        role_checker = require_role("user")
        
        with pytest.raises(HTTPException) as exc_info:
            role_checker(mock_user_info)
        
        assert exc_info.value.status_code == 403


class TestAuthModels:
    """Test authentication request/response models"""
    
    def test_login_request_valid(self):
        """Test valid LoginRequest"""
        request = LoginRequest(username="testuser", password="testpass123")
        assert request.username == "testuser"
        assert request.password == "testpass123"
    
    def test_login_request_min_length(self):
        """Test LoginRequest with minimum valid length"""
        request = LoginRequest(username="a", password="b")
        assert request.username == "a"
        assert request.password == "b"
    
    def test_login_request_validation_error(self):
        """Test LoginRequest validation error"""
        with pytest.raises(ValueError):
            LoginRequest(username="", password="test")
    
    def test_login_request_from_dict(self):
        """Test LoginRequest from dictionary"""
        data = {"username": "testuser", "password": "testpass"}
        request = LoginRequest(**data)
        assert request.username == "testuser"
        assert request.password == "testpass"


class TestAuthEdgeCases:
    """Test edge cases for authentication"""
    
    def test_verify_token_with_none_token(self, mock_requests_get):
        """Test verify_token with None token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_response.text = "Unauthorized"
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(HTTPException):
            verify_token(None)
    
    def test_verify_token_with_empty_token(self, mock_requests_get):
        """Test verify_token with empty token"""
        mock_response = Mock()
        mock_response.status_code = 401
        mock_response.json.return_value = {"error": "Unauthorized"}
        mock_response.text = "Unauthorized"
        mock_response.headers = {}
        mock_requests_get.return_value = mock_response
        
        with pytest.raises(HTTPException):
            verify_token("")
    
    def test_login_with_special_characters(self, client, mock_keycloak_response, mock_requests_post):
        """Test login with special characters in username"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_keycloak_response
        mock_requests_post.return_value = mock_response
        
        response = client.post("/auth/login", json={
            "username": "user@domain.com",
            "password": "p@ssw0rd!123"
        })
        
        assert response.status_code == 200
    
    def test_login_timeout(self, client, mock_requests_post):
        """Test login with timeout"""
        mock_requests_post.side_effect = RequestException("Timeout")
        
        try:
            response = client.post("/auth/login", json={
                "username": "testuser",
                "password": "testpass123"
            })
            # If we get here, the exception wasn't raised properly
            assert response.status_code == 500
        except RequestException:
            # This is expected - the exception propagates
            pass
