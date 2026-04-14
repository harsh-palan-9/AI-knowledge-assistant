from pydantic import BaseModel

class QueryResponse(BaseModel):
    user: str
    query: str
    answer: str