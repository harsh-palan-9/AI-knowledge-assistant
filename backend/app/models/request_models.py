from pydantic import BaseModel, Field

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3, json_schema_extra={"example": "What is AI?"})

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=1, json_schema_extra={"example": "testuser"})
    password: str = Field(..., min_length=1, json_schema_extra={"example": "password123"})