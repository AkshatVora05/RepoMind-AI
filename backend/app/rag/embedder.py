import google.generativeai as genai
from app.core.config import settings
from typing import List

genai.configure(api_key=settings.GEMINI_API_KEY)

from fastembed import TextEmbedding

# Initialize globally to load into memory only once
# BAAI/bge-small-en-v1.5 outputs 384-dimensional vectors.
print("Loading FastEmbed model (BAAI/bge-small-en-v1.5)...")
embedding_model = TextEmbedding(model_name="BAAI/bge-small-en-v1.5")

def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generates embeddings using the fastembed library.
    Runs entirely locally using ONNX Runtime (low RAM).
    Outputs 384-dimensional vectors.
    """
    if not texts:
        return []
        
    # fastembed.embed returns a generator of numpy arrays
    embeddings_gen = embedding_model.embed(texts)
    
    # Convert numpy arrays to lists of floats
    all_embeddings = [vector.tolist() for vector in embeddings_gen]
    
    return all_embeddings
