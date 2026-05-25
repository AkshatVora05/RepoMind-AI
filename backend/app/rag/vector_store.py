from pinecone import Pinecone
from app.core.config import settings

# Initialize Pinecone globally
pc = Pinecone(api_key=settings.PINECONE_API_KEY)

def get_pinecone_index():
    """
    Returns the Pinecone index instance.
    Raises an error if the index doesn't exist.
    """
    # Just grab the index object. Pinecone client handles connections internally.
    index = pc.Index(settings.PINECONE_INDEX_NAME)
    return index
