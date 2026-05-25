from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.schemas.query import QueryRequest, QueryResponse
from app.services.rag_service import query_repository

router = APIRouter()

@router.post("/{owner}/{repo_name}", response_model=QueryResponse)
def query_repo(owner: str, repo_name: str, request: QueryRequest, db: Session = Depends(get_db)):
    """
    Ask a question about a specific repository using RAG.
    """
    repo_id = f"{owner}/{repo_name}"
    
    # Ensure the repo exists and is completed
    repo = crud.get_repo(db, repo_id=repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    
    # Bump the activity timestamp
    crud.bump_last_queried(db, repo_id=repo_id)
    
    # Perform RAG
    response_data = query_repository(repo_id, request.query)
    
    return response_data
