from pydantic import BaseModel
from typing import List

class QueryRequest(BaseModel):
    query: str

class Citation(BaseModel):
    file_path: str
    text_snippet: str

class QueryResponse(BaseModel):
    answer: str
    citations: List[Citation]
