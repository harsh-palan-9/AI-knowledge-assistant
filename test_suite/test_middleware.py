"""
Comprehensive test suite for logging middleware
"""
import pytest
from unittest.mock import Mock, patch, AsyncMock
import sys
import os
import asyncio

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from app.middleware.logging_middleware import (
    LoggingMiddleware,
    DocumentRetrievalLogger,
    LLMLogger,
    document_logger,
    llm_logger
)
from fastapi import Request, Response


class TestLoggingMiddleware:
    """Test LoggingMiddleware class"""
    
    def test_middleware_init(self):
        """Test middleware initialization"""
        from app.main import app
        
        middleware = LoggingMiddleware(app)
        
        assert middleware.app == app
        assert hasattr(middleware, 'request_start_times')
    
    def test_middleware_dispatch(self):
        """Test middleware dispatch method"""
        from app.main import app
        
        middleware = LoggingMiddleware(app)
        
        # Create mock request
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "GET"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/endpoint")
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(return_value={})
        
        # Create mock response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        # Mock call_next as async function
        async def mock_call_next(request):
            return mock_response
        
        # Run the async dispatch synchronously
        import asyncio
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_dispatch_post_query(self):
        """Test middleware with POST query request"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        # Create mock request for /query endpoint
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "POST"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/query")
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(return_value={"question": "What is AI?"})
        
        # Create mock response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_dispatch_with_error(self):
        """Test middleware when request.json fails"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        # Create mock request
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "POST"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/query")
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(side_effect=Exception("JSON parse error"))
        
        # Create mock response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_dispatch_no_client(self):
        """Test middleware when request.client is None"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        # Create mock request without client
        mock_request = Mock(spec=Request)
        mock_request.client = None
        mock_request.method = "GET"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/endpoint")
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(return_value={})
        
        # Create mock response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_dispatch_no_user_agent(self):
        """Test middleware when user-agent header is missing"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        # Create mock request without user-agent
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "GET"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/endpoint")
        mock_request.headers = {}
        mock_request.json = Mock(return_value={})
        
        # Create mock response
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_llm_response_time_logging(self):
        """Test middleware logs LLM response time for query endpoints"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        # Create mock request for /query endpoint
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "POST"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/query")
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(return_value={"question": "What is AI?"})
        
        # Create mock response with 200 status
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response


class TestDocumentRetrievalLogger:
    """Test DocumentRetrievalLogger class"""
    
    def test_log_retrieval_start(self):
        """Test log_retrieval_start method"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_start("test query", {"k": 5})
            
            mock_logger.info.assert_called_once()
            assert "test query" in str(mock_logger.info.call_args)
    
    def test_log_retrieval_start_no_params(self):
        """Test log_retrieval_start without params"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_start("test query")
            
            mock_logger.info.assert_called_once()
    
    def test_log_retrieval_complete(self):
        """Test log_retrieval_complete method"""
        from langchain_core.documents import Document
        
        docs = [Document(page_content="Test content")]
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_complete("test query", docs, 0.5)
            
            mock_logger.info.assert_called()
            assert "test query" in str(mock_logger.info.call_args)
    
    def test_log_retrieval_complete_many_docs(self):
        """Test log_retrieval_complete with many documents"""
        from langchain_core.documents import Document
        
        docs = [Document(page_content=f"Content {i}") for i in range(10)]
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_complete("test query", docs, 1.0)
            
            mock_logger.info.assert_called()
    
    def test_log_retrieval_complete_empty_docs(self):
        """Test log_retrieval_complete with empty document list"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_complete("test query", [], 0.1)
            
            mock_logger.info.assert_called()
    
    def test_log_retrieval_error(self):
        """Test log_retrieval_error method"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_error("test query", "Test error")
            
            mock_logger.error.assert_called_once()
            assert "test query" in str(mock_logger.error.call_args)
            assert "Test error" in str(mock_logger.error.call_args)
    
    def test_log_retrieval_complete_long_content(self):
        """Test log_retrieval_complete with long document content"""
        from langchain_core.documents import Document
        
        long_content = "x" * 1000
        docs = [Document(page_content=long_content)]
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_complete("test query", docs, 0.5)
            
            mock_logger.info.assert_called()
    
    def test_log_retrieval_complete_multiline_content(self):
        """Test log_retrieval_complete with multiline content"""
        from langchain_core.documents import Document
        
        docs = [Document(page_content="Line 1\nLine 2\nLine 3")]
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            DocumentRetrievalLogger.log_retrieval_complete("test query", docs, 0.5)
            
            mock_logger.info.assert_called()


class TestLLMLogger:
    """Test LLMLogger class"""
    
    def test_log_llm_call_start(self):
        """Test log_llm_call_start method"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_start("Test prompt", "llama-3.1-8b-instant")
            
            mock_logger.info.assert_called_once()
            assert "llama-3.1-8b-instant" in str(mock_logger.info.call_args)
    
    def test_log_llm_call_start_long_prompt(self):
        """Test log_llm_call_start with long prompt"""
        long_prompt = "x" * 10000
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_start(long_prompt, "llama-3.1-8b-instant")
            
            mock_logger.info.assert_called_once()
    
    def test_log_llm_call_start_multiline_prompt(self):
        """Test log_llm_call_start with multiline prompt"""
        multiline_prompt = "Line 1\nLine 2\nLine 3"
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_start(multiline_prompt, "llama-3.1-8b-instant")
            
            mock_logger.info.assert_called_once()
    
    def test_log_llm_call_complete(self):
        """Test log_llm_call_complete method"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_complete("llama-3.1-8b-instant", 1.5, 100)
            
            mock_logger.info.assert_called_once()
            assert "llama-3.1-8b-instant" in str(mock_logger.info.call_args)
            assert "1.5" in str(mock_logger.info.call_args)
    
    def test_log_llm_call_complete_long_response(self):
        """Test log_llm_call_complete with long response"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_complete("llama-3.1-8b-instant", 2.0, 1000000)
            
            mock_logger.info.assert_called_once()
    
    def test_log_llm_call_complete_fast_response(self):
        """Test log_llm_call_complete with very fast response"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_complete("llama-3.1-8b-instant", 0.001, 50)
            
            mock_logger.info.assert_called_once()
    
    def test_log_llm_call_error(self):
        """Test log_llm_call_error method"""
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_error("llama-3.1-8b-instant", "API error")
            
            mock_logger.error.assert_called_once()
            assert "llama-3.1-8b-instant" in str(mock_logger.error.call_args)
            assert "API error" in str(mock_logger.error.call_args)
    
    def test_log_llm_call_error_long_error_message(self):
        """Test log_llm_call_error with long error message"""
        long_error = "x" * 10000
        
        with patch('app.middleware.logging_middleware.logger') as mock_logger:
            LLMLogger.log_llm_call_error("llama-3.1-8b-instant", long_error)
            
            mock_logger.error.assert_called_once()


class TestGlobalLoggerInstances:
    """Test global logger instances"""
    
    def test_document_logger_instance(self):
        """Test document_logger is an instance of DocumentRetrievalLogger"""
        assert isinstance(document_logger, DocumentRetrievalLogger)
    
    def test_llm_logger_instance(self):
        """Test llm_logger is an instance of LLMLogger"""
        assert isinstance(llm_logger, LLMLogger)
    
    def test_document_logger_methods(self):
        """Test document_logger has all required methods"""
        assert hasattr(document_logger, 'log_retrieval_start')
        assert hasattr(document_logger, 'log_retrieval_complete')
        assert hasattr(document_logger, 'log_retrieval_error')
    
    def test_llm_logger_methods(self):
        """Test llm_logger has all required methods"""
        assert hasattr(llm_logger, 'log_llm_call_start')
        assert hasattr(llm_logger, 'log_llm_call_complete')
        assert hasattr(llm_logger, 'log_llm_call_error')


class TestMiddlewareEdgeCases:
    """Test edge cases for middleware"""
    
    def test_middleware_with_special_characters_in_url(self):
        """Test middleware with special characters in URL"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "GET"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value="http://test.com/endpoint?param=value&aéíóú=ñ")
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(return_value={})
        
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_with_very_long_url(self):
        """Test middleware with very long URL"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        long_url = "http://test.com/endpoint?" + "&".join([f"param{i}=value{i}" for i in range(100)])
        
        mock_request = Mock(spec=Request)
        mock_request.client = Mock()
        mock_request.client.host = "127.0.0.1"
        mock_request.method = "GET"
        mock_request.url = Mock()
        mock_request.url.__str__ = Mock(return_value=long_url)
        mock_request.headers = {"user-agent": "test-agent"}
        mock_request.json = Mock(return_value={})
        
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        
        async def mock_call_next(request):
            return mock_response
        
        result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
        
        assert result == mock_response
    
    def test_middleware_with_different_methods(self):
        """Test middleware with different HTTP methods"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        for method in ["GET", "POST", "PUT", "DELETE", "PATCH"]:
            mock_request = Mock(spec=Request)
            mock_request.client = Mock()
            mock_request.client.host = "127.0.0.1"
            mock_request.method = method
            mock_request.url = Mock()
            mock_request.url.__str__ = Mock(return_value="http://test.com/endpoint")
            mock_request.headers = {"user-agent": "test-agent"}
            mock_request.json = Mock(return_value={})
            
            mock_response = Mock(spec=Response)
            mock_response.status_code = 200
            
            async def mock_call_next(request):
                return mock_response
            
            result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
            
            assert result == mock_response
    
    def test_middleware_with_different_status_codes(self):
        """Test middleware with different response status codes"""
        from app.main import app
        import asyncio
        
        middleware = LoggingMiddleware(app)
        
        for status_code in [200, 201, 400, 401, 403, 404, 500]:
            mock_request = Mock(spec=Request)
            mock_request.client = Mock()
            mock_request.client.host = "127.0.0.1"
            mock_request.method = "GET"
            mock_request.url = Mock()
            mock_request.url.__str__ = Mock(return_value="http://test.com/endpoint")
            mock_request.headers = {"user-agent": "test-agent"}
            mock_request.json = Mock(return_value={})
            
            mock_response = Mock(spec=Response)
            mock_response.status_code = status_code
            
            async def mock_call_next(request):
                return mock_response
            
            result = asyncio.run(middleware.dispatch(mock_request, mock_call_next))
            
            assert result == mock_response
