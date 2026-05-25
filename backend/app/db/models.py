from sqlalchemy import Column, String, DateTime, Text, Enum
from sqlalchemy.sql import func
import enum
from app.db.database import Base

class IngestionStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Repository(Base):
    __tablename__ = "repositories"

    id = Column(String, primary_key=True, index=True) # E.g., "owner/repo"
    url = Column(String, unique=True, index=True, nullable=False)
    status = Column(Enum(IngestionStatus), default=IngestionStatus.PENDING)
    
    # Store pre-generated insights
    architecture_summary = Column(Text, nullable=True)
    roadmap = Column(Text, nullable=True)

    # Lifecycle tracking for auto-cleanup
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_queried_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
