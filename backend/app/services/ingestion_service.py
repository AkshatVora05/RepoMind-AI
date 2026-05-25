from sqlalchemy.orm import Session
from app.db import crud, models
from app.services.github_service import download_and_extract_repo, cleanup_repo_dir
from app.rag.chunker import process_directory
from app.rag.embedder import generate_embeddings
from app.rag.vector_store import get_pinecone_index
from app.services.rag_service import generate_repo_insights
import uuid
import traceback

def process_repository_background(repo_id: str, url: str, db: Session):
    """
    The main background task that handles the heavy lifting of ingestion.
    """
    temp_dir = None
    try:
        # 1. Update status to PROCESSING
        crud.update_repo_status(db, repo_id, models.IngestionStatus.PROCESSING)
        
        # 2. Download and Extract
        print(f"[{repo_id}] Downloading repository...")
        temp_dir = download_and_extract_repo(url)
        
        # 3. Parse and Chunk Files
        print(f"[{repo_id}] Parsing and chunking files...")
        chunks_data = process_directory(temp_dir)
        
        if not chunks_data:
            raise ValueError("No valid text/code files found in the repository.")
            
        # 4. Generate Embeddings & Prepare vectors for Pinecone
        print(f"[{repo_id}] Generating embeddings for {len(chunks_data)} chunks...")
        texts = [item["text"] for item in chunks_data]
        embeddings = generate_embeddings(texts)
        
        vectors_to_upsert = []
        for i, item in enumerate(chunks_data):
            # Pinecone requires unique IDs for each vector
            vector_id = f"{repo_id}#{item['metadata']['file_path']}#{item['metadata']['chunk_index']}#{uuid.uuid4().hex[:8]}"
            
            # Store the actual text in metadata so we can retrieve it later
            metadata = item["metadata"]
            metadata["repo_id"] = repo_id
            metadata["text"] = item["text"]
            
            vectors_to_upsert.append((vector_id, embeddings[i], metadata))
            
        # 5 & 6. Run Pinecone Upserts and LLM Insights Generation concurrently!
        print(f"[{repo_id}] Starting concurrent Pinecone upload and LLM generation...")
        
        def upsert_to_pinecone():
            index = get_pinecone_index()
            batch_size = 100
            for i in range(0, len(vectors_to_upsert), batch_size):
                batch = vectors_to_upsert[i:i + batch_size]
                index.upsert(vectors=batch)
            print(f"[{repo_id}] Pinecone upload complete.")

        def generate_insights():
            sample_context = "\n\n".join([c["text"] for c in chunks_data[:15]])
            return generate_repo_insights(sample_context)

        import concurrent.futures
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as executor:
            future_pinecone = executor.submit(upsert_to_pinecone)
            future_insights = executor.submit(generate_insights)
            
            # Wait for both to complete and catch any exceptions
            future_pinecone.result() 
            arch_summary, roadmap = future_insights.result()
        
        # 7. Mark as COMPLETED and save insights
        crud.update_repo_status(
            db, 
            repo_id, 
            models.IngestionStatus.COMPLETED,
            architecture_summary=arch_summary,
            roadmap=roadmap
        )
        print(f"[{repo_id}] Ingestion completed successfully!")
        
    except Exception as e:
        print(f"[{repo_id}] Ingestion failed: {e}")
        traceback.print_exc()
        crud.update_repo_status(db, repo_id, models.IngestionStatus.FAILED)
        
    finally:
        # ALWAYS clean up the temporary directory to prevent Render disk overflow
        if temp_dir:
            print(f"[{repo_id}] Cleaning up temporary files...")
            cleanup_repo_dir(temp_dir)
