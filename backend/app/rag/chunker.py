import os

# Files to completely ignore during parsing
IGNORE_DIRS = {
    ".git", ".github", "node_modules", "venv", ".venv", "env", "dist", "build", 
    "__pycache__", ".next", "out"
}

IGNORE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".gif", ".ico", ".svg", ".webp", # Images
    ".mp4", ".mp3", ".wav", # Media
    ".pdf", ".zip", ".tar", ".gz", ".rar", # Archives
    ".exe", ".dll", ".so", ".dylib", ".class", ".pyc", # Compiled
    ".lock", # Package locks (package-lock.json, poetry.lock, etc)
}

def should_process_file(file_path: str) -> bool:
    """
    Checks if a file should be parsed based on its path and extension.
    """
    # Check directory
    parts = file_path.split(os.sep)
    for part in parts:
        if part in IGNORE_DIRS:
            return False
            
    # Check extension
    _, ext = os.path.splitext(file_path)
    # Specifically ignore lock files as they don't have standard extensions sometimes
    if "lock" in file_path.lower():
        return False
        
    if ext.lower() in IGNORE_EXTENSIONS:
        return False
        
    return True

def chunk_text(text: str, chunk_size: int = 1500, overlap: int = 200) -> list[str]:
    """
    A simple, realistic chunker that splits text into chunks of `chunk_size` characters,
    with an overlap to preserve context across boundaries.
    
    Using character length instead of token counting keeps this fast and simple without external libs.
    """
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = min(start + chunk_size, text_length)
        
        # If we are not at the end, try to find a natural break point (newline)
        if end < text_length:
            # Look backwards up to 100 characters to find a newline
            newline_pos = text.rfind('\n', max(start, end - 100), end)
            if newline_pos != -1:
                end = newline_pos + 1
                
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
            
        if end >= text_length:
            break
            
        start = end - overlap
        
    return chunks

def process_directory(directory_path: str) -> list[dict]:
    """
    Walks a directory, reads valid files, and chunks their contents.
    Returns a list of dictionaries containing chunk text and metadata.
    """
    all_chunks = []
    
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            
            # Get relative path for metadata (looks cleaner)
            rel_path = os.path.relpath(file_path, directory_path)
            
            if not should_process_file(rel_path):
                continue
                
            try:
                # Attempt to read as utf-8 text
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                if not content.strip():
                    continue
                    
                file_chunks = chunk_text(content)
                for i, chunk in enumerate(file_chunks):
                    all_chunks.append({
                        "text": chunk,
                        "metadata": {
                            "file_path": rel_path,
                            "chunk_index": i
                        }
                    })
            except UnicodeDecodeError:
                # Skip binary files that slipped through extension checks
                continue
            except Exception as e:
                print(f"Skipping file {rel_path} due to error: {e}")
                continue
                
    return all_chunks
