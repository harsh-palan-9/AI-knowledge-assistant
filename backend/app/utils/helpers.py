"""
Utility helper functions for the AI Knowledge Assistant
"""
import re
from typing import Any, Dict

def format_response(data: Any) -> Dict[str, Any]:
    """Format response data for API responses"""
    if isinstance(data, dict):
        return data
    return {"data": data}

def validate_email(email: str) -> bool:
    """Validate email address format"""
    if not email or not isinstance(email, str):
        return False
    
    # Basic email validation regex
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_input(input_text: str) -> str:
    """Sanitize user input to prevent XSS and other issues"""
    if not input_text or not isinstance(input_text, str):
        return ""
    
    # Remove HTML tags
    sanitized = re.sub(r'<[^>]+>', '', input_text)
    
    # Convert HTML entities back to characters
    sanitized = sanitized.replace('&lt;', '<').replace('&gt;', '>')
    sanitized = sanitized.replace('&amp;', '&').replace('&quot;', '"')
    
    return sanitized.strip()