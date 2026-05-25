import google.generativeai as genai
from app.core.config import settings
from typing import List

genai.configure(api_key=settings.GEMINI_API_KEY)

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings using the Gemini API.
    This runs entirely in the cloud and uses 0 RAM locally.
    Outputs 768-dimensional vectors.
    """
    # Fallback to the working gemini-embedding-2 model and force 768 dimensions for Pinecone
    result = genai.embed_content(
        model="models/gemini-embedding-2",
        content=texts,
        task_type="retrieval_document",
        output_dimensionality=768
    )
    return result['embedding']
