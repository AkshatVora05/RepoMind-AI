from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from app.db.models import IngestionStatus

class RepoIngestRequest(BaseModel):
    url: HttpUrl

class RepoResponse(BaseModel):
    id: str
    url: str
    status: IngestionStatus
    created_at: datetime
    last_queried_at: datetime
    architecture_summary: Optional[str] = None
    roadmap: Optional[str] = None

    class Config:
        from_attributes = True
