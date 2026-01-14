from pydantic import BaseModel

class RAGRequest(BaseModel):
    query: str
    top_k: int = 5

class RAGResponse(BaseModel):
    answer: str