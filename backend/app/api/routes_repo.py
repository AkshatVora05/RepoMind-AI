from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.db import crud
from app.schemas.repo import RepoIngestRequest, RepoResponse
from app.services.ingestion_service import process_repository_background
from app.services.cleanup_service import delete_repository_data, auto_cleanup_stale_repos
from app.services.github_service import parse_github_url
from typing import List

router = APIRouter()

@router.post("/ingest", response_model=RepoResponse)
def ingest_repository(
    request: RepoIngestRequest, 
    background_tasks: BackgroundTasks, 
    db: Session = Depends(get_db)
):
    """
    Triggers the ingestion of a GitHub repository.
    The heavy lifting (download, chunk, embed) runs in the background.
    """
    try:
        owner, repo_name = parse_github_url(str(request.url))
        repo_id = f"{owner}/{repo_name}"
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid GitHub URL.")

    # Check if already exists
    existing_repo = crud.get_repo(db, repo_id=repo_id)
    if existing_repo:
        return existing_repo
        
    # Create the DB record as PENDING
    repo = crud.create_repo(db=db, repo_in=request)
    
    # Fire off background task
    background_tasks.add_task(process_repository_background, repo_id, str(request.url), db)
    
    return repo

@router.get("/", response_model=List[RepoResponse])
def list_repositories(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """List all currently ingested repositories."""
    repos = crud.get_repos(db, skip=skip, limit=limit)
    return repos

@router.get("/{owner}/{repo_name}", response_model=RepoResponse)
def get_repository(owner: str, repo_name: str, db: Session = Depends(get_db)):
    """Get metadata and status of a specific repository."""
    repo_id = f"{owner}/{repo_name}"
    repo = crud.get_repo(db, repo_id=repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
    
    # Bump last queried to prevent auto-cleanup
    crud.bump_last_queried(db, repo_id=repo_id)
    return repo

@router.delete("/{owner}/{repo_name}")
def delete_repository(owner: str, repo_name: str, db: Session = Depends(get_db)):
    """Manually delete a repository's metadata and vectors."""
    repo_id = f"{owner}/{repo_name}"
    repo = crud.get_repo(db, repo_id=repo_id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found.")
        
    delete_repository_data(db, repo_id)
    return {"message": f"Repository {repo_id} deleted successfully."}

@router.post("/trigger-cleanup")
def trigger_auto_cleanup(hours_stale: int = 3, db: Session = Depends(get_db)):
    """
    Endpoint that can be hit via a cron job (e.g., cron-job.org) 
    to trigger the deletion of stale repositories.
    """
    deleted_count = auto_cleanup_stale_repos(db, hours_stale=hours_stale)
    return {"message": f"Auto-cleanup finished. Deleted {deleted_count} stale repositories."}
