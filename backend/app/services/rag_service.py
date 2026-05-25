import google.generativeai as genai
from app.core.config import settings
from app.rag.vector_store import get_pinecone_index
from app.rag.embedder import generate_embeddings
from typing import Dict

# Configure Gemini
genai.configure(api_key=settings.GEMINI_API_KEY)
# We use gemini-2.5-flash as it is fast, free-tier friendly, and great for RAG
model = genai.GenerativeModel('gemini-2.5-flash')

def query_repository(repo_id: str, query: str) -> Dict:
    """
    1. Embeds the user query
    2. Searches Pinecone for the top 5 most relevant chunks for this specific repo
    3. Prompts Gemini with the chunks as context
    """
    # 1. Embed query
    query_embedding = generate_embeddings([query])[0]
    
    # 2. Retrieve from Pinecone
    index = get_pinecone_index()
    search_response = index.query(
        vector=query_embedding,
        top_k=5,
        filter={"repo_id": {"$eq": repo_id}},
        include_metadata=True
    )
    
    # 3. Format chunks for prompt and citations
    chunks = []
    citations = []
    for match in search_response.get("matches", []):
        metadata = match.get("metadata", {})
        text = metadata.get("text", "")
        file_path = metadata.get("file_path", "unknown")
        
        chunks.append(f"--- FILE: {file_path} ---\n{text}\n")
        citations.append({
            "file_path": file_path,
            "text_snippet": text[:200] + "..."
        })
        
    context_text = "\n".join(chunks)
    
    if not context_text:
        return {
            "answer": "I couldn't find any relevant code in this repository to answer your question.",
            "citations": []
        }
    
    # 4. Generate answer using Gemini
    prompt = f"""
    You are an expert senior software engineer answering a question about a codebase.
    Base your answer ONLY on the provided code context. Do not make up internal details if they are not in the context.
    If the context does not contain the answer, simply say "I don't have enough context from the codebase to answer this."
    
    CONTEXT:
    {context_text}
    
    USER QUESTION: {query}
    
    ANSWER:
    """
    
    response = model.generate_content(prompt)
    
    return {
        "answer": response.text,
        "citations": citations
    }

def generate_repo_insights(context_text: str) -> tuple[str, str]:
    """
    Generates a high-level architecture summary and beginner roadmap based on a 
    sample of the repository's main files (like README, main.py, package.json).
    """
    prompt = f"""
    You are a senior technical architect. I am providing you with the core files of a repository.
    
    CONTEXT:
    {context_text}
    
    Please provide TWO things separated by a clear delimiter "|||DELIMITER|||":
    1. A clear, high-level Architecture Summary (how this project is structured).
    2. A Beginner Onboarding Roadmap (step-by-step guide on how a new dev should read the code).
    
    Keep both professional, concise, and use markdown formatting.
    """
    
    try:
        response = model.generate_content(prompt)
        parts = response.text.split("|||DELIMITER|||")
        if len(parts) >= 2:
            return parts[0].strip(), parts[1].strip()
        return response.text, "Roadmap generation failed."
    except Exception as e:
        print(f"Failed to generate insights: {e}")
        return "Insight generation failed.", "Insight generation failed."
