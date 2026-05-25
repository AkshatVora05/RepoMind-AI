from sqlalchemy.orm import Session
from app.db import models
from app.schemas.repo import RepoIngestRequest
from app.services.github_service import parse_github_url
import datetime

def get_repo(db: Session, repo_id: str):
    return db.query(models.Repository).filter(models.Repository.id == repo_id).first()

def get_repos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Repository).offset(skip).limit(limit).all()

def create_repo(db: Session, repo_in: RepoIngestRequest):
    owner, repo_name = parse_github_url(str(repo_in.url))
    repo_id = f"{owner}/{repo_name}"
    
    db_repo = models.Repository(
        id=repo_id,
        url=str(repo_in.url),
        status=models.IngestionStatus.PENDING
    )
    db.add(db_repo)
    db.commit()
    db.refresh(db_repo)
    return db_repo

def update_repo_status(db: Session, repo_id: str, status: models.IngestionStatus, architecture_summary: str = None, roadmap: str = None):
    db_repo = get_repo(db, repo_id)
    if db_repo:
        db_repo.status = status
        if architecture_summary:
            db_repo.architecture_summary = architecture_summary
        if roadmap:
            db_repo.roadmap = roadmap
        db.commit()
        db.refresh(db_repo)
    return db_repo

def bump_last_queried(db: Session, repo_id: str):
    db_repo = get_repo(db, repo_id)
    if db_repo:
        db_repo.last_queried_at = datetime.datetime.now(datetime.timezone.utc)
        db.commit()
        db.refresh(db_repo)
    return db_repo

def delete_repo(db: Session, repo_id: str):
    db_repo = get_repo(db, repo_id)
    if db_repo:
        db.delete(db_repo)
        db.commit()
    return db_repo

def get_stale_repos(db: Session, hours_stale: int = 3):
    threshold = datetime.datetime.now(datetime.timezone.utc) - datetime.timedelta(hours=hours_stale)
    return db.query(models.Repository).filter(models.Repository.last_queried_at < threshold).all()
