from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.config import settings

# Create SQLAlchemy engine
# pool_pre_ping=True helps prevent "SQL server has gone away" style errors over long connections
engine = create_engine(settings.DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    """
    Dependency function to provide a database session per request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
