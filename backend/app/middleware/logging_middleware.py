import time
import logging
from typing import Callable
from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)

class LoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware to log system behavior including:
    - User queries
    - Retrieved documents
    - LLM response times
    """
    
    def __init__(self, app):
        super().__init__(app)
        self.request_start_times = {}
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Start timing
        start_time = time.time()
        
        # Log incoming request
        await self._log_request(request)
        
        # Process request
        response = await call_next(request)
        
        # Calculate processing time
        process_time = time.time() - start_time
        
        # Log response
        await self._log_response(request, response, process_time)
        
        return response
    
    async def _log_request(self, request: Request):
        """Log incoming request details"""
        client_ip = request.client.host if request.client else "unknown"
        method = request.method
        url = str(request.url)
        user_agent = request.headers.get("user-agent", "unknown")
        
        logger.info(
            f"REQUEST - Method: {method}, URL: {url}, IP: {client_ip}, "
            f"User-Agent: {user_agent}"
        )
        
        # Log query details for POST requests to /query endpoint
        if method == "POST" and "/query" in url:
            try:
                body = await request.json()
                if "question" in body:
                    logger.info(f"USER_QUERY - Question: {body['question']}")
            except Exception as e:
                logger.warning(f"Failed to log query body: {e}")
    
    async def _log_response(self, request: Request, response: Response, process_time: float):
        """Log response details and processing time"""
        status_code = response.status_code
        url = str(request.url)
        
        logger.info(
            f"RESPONSE - URL: {url}, Status: {status_code}, "
            f"Process_Time: {process_time:.3f}s"
        )
        
        # Log LLM response time for query endpoints
        if "/query" in url and status_code == 200:
            logger.info(f"LLM_RESPONSE_TIME - {process_time:.3f}s")

class DocumentRetrievalLogger:
    """Logger for document retrieval operations"""
    
    @staticmethod
    def log_retrieval_start(query: str, retrieval_params: dict = None):
        """Log the start of document retrieval"""
        params_str = f", Params: {retrieval_params}" if retrieval_params else ""
        logger.info(f"DOCUMENT_RETRIEVAL_START - Query: '{query}'{params_str}")
    
    @staticmethod
    def log_retrieval_complete(query: str, documents: list, retrieval_time: float):
        """Log successful document retrieval"""
        doc_count = len(documents)
        logger.info(
            f"DOCUMENT_RETRIEVAL_COMPLETE - Query: '{query}', "
            f"Documents_Retrieved: {doc_count}, Retrieval_Time: {retrieval_time:.3f}s"
        )
        
        # Log document metadata (first 200 chars of each document)
        for i, doc in enumerate(documents[:3]):  # Log first 3 documents
            content_preview = doc.page_content[:200].replace('\n', ' ')
            logger.debug(f"DOCUMENT_{i+1} - Content: '{content_preview}...'")
    
    @staticmethod
    def log_retrieval_error(query: str, error: str):
        """Log document retrieval errors"""
        logger.error(f"DOCUMENT_RETRIEVAL_ERROR - Query: '{query}', Error: {error}")

class LLMLogger:
    """Logger for LLM operations"""
    
    @staticmethod
    def log_llm_call_start(prompt: str, model: str):
        """Log the start of LLM call"""
        prompt_preview = prompt[:200].replace('\n', ' ')
        logger.info(
            f"LLM_CALL_START - Model: {model}, "
            f"Prompt_Preview: '{prompt_preview}...'"
        )
    
    @staticmethod
    def log_llm_call_complete(model: str, response_time: float, response_length: int):
        """Log successful LLM call"""
        logger.info(
            f"LLM_CALL_COMPLETE - Model: {model}, "
            f"Response_Time: {response_time:.3f}s, Response_Length: {response_length} chars"
        )
    
    @staticmethod
    def log_llm_call_error(model: str, error: str):
        """Log LLM call errors"""
        logger.error(f"LLM_CALL_ERROR - Model: {model}, Error: {error}")

# Global logger instances
document_logger = DocumentRetrievalLogger()
llm_logger = LLMLogger()