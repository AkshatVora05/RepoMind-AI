from fastembed import TextEmbedding

if __name__ == "__main__":
    print("Pre-downloading FastEmbed model weights (sentence-transformers/all-MiniLM-L6-v2) into Docker image cache...")
    # Instantiating the model forces it to download the weights if not cached
    TextEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")
    print("Model downloaded and cached successfully!")
