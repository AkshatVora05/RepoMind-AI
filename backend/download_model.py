from fastembed import TextEmbedding

if __name__ == "__main__":
    print("Pre-downloading FastEmbed model weights (BAAI/bge-small-en-v1.5) into Docker image cache...")
    # Instantiating the model forces it to download the weights if not cached
    TextEmbedding(model_name="BAAI/bge-small-en-v1.5")
    print("Model downloaded and cached successfully!")
