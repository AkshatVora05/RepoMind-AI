from sqlalchemy.orm import Session
from app.db import crud
from app.rag.vector_store import get_pinecone_index

def delete_repository_data(db: Session, repo_id: str):
    """
    Completely removes a repository from the system.
    1. Deletes all vectors associated with the repo_id from Pinecone.
    2. Deletes the metadata record from Postgres.
    """
    # 1. Clean Pinecone vectors
    try:
        index = get_pinecone_index()
        # Pinecone doesn't allow deleting by metadata directly in the free tier easily 
        # unless you query and delete by ID. However, Pinecone Serverless supports delete with filter.
        index.delete(filter={"repo_id": {"$eq": repo_id}})
        print(f"[{repo_id}] Successfully deleted vectors from Pinecone.")
    except Exception as e:
        print(f"[{repo_id}] Failed to delete vectors from Pinecone: {e}")
        # Proceed to delete from DB anyway so the user isn't stuck
        
    # 2. Clean Postgres metadata
    crud.delete_repo(db, repo_id)
    print(f"[{repo_id}] Successfully deleted metadata from Database.")

def auto_cleanup_stale_repos(db: Session, hours_stale: int = 3):
    """
    Finds all repos that haven't been queried in the last `hours_stale` hours
    and deletes them completely to free up space.
    """
    stale_repos = crud.get_stale_repos(db, hours_stale=hours_stale)
    
    for repo in stale_repos:
        print(f"Auto-cleanup triggered for stale repo: {repo.id}")
        delete_repository_data(db, repo.id)
        
    return len(stale_repos)
