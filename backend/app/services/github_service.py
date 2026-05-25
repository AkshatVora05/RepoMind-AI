import requests
import zipfile
import io
import os
import tempfile
import shutil
from app.core.config import settings

def parse_github_url(url: str) -> tuple[str, str]:
    """
    Extracts owner and repo name from a GitHub URL.
    Example: https://github.com/owner/repo -> ('owner', 'repo')
    """
    url = url.rstrip('/')
    parts = url.split('/')
    if len(parts) < 2:
        raise ValueError("Invalid GitHub URL")
    
    repo = parts[-1]
    owner = parts[-2]
    
    # Strip off .git if present
    if repo.endswith('.git'):
        repo = repo[:-4]
        
    return owner, repo

def get_default_branch(owner: str, repo: str) -> str:
    """
    Fetches the default branch for the repository using the API.
    """
    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {"Accept": "application/vnd.github.v3+json"}
    
    if settings.GITHUB_PAT:
        headers["Authorization"] = f"token {settings.GITHUB_PAT}"
        
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    return response.json().get("default_branch", "main")

def download_and_extract_repo(url: str) -> str:
    """
    Downloads the repository as a ZIP file, extracts it to a temporary directory,
    and returns the path to the extracted directory.
    
    The caller is responsible for deleting the directory after processing.
    """
    owner, repo = parse_github_url(url)
    default_branch = get_default_branch(owner, repo)
    
    # The /zipball endpoint downloads the entire repo in one request
    zip_url = f"https://api.github.com/repos/{owner}/{repo}/zipball/{default_branch}"
    
    headers = {"Accept": "application/vnd.github.v3+json"}
    if settings.GITHUB_PAT:
        headers["Authorization"] = f"token {settings.GITHUB_PAT}"

    response = requests.get(zip_url, headers=headers, stream=True)
    response.raise_for_status()

    # Create a temporary directory
    temp_dir = tempfile.mkdtemp(prefix=f"repomind_{owner}_{repo}_")
    
    # Extract zip directly from memory to disk
    with zipfile.ZipFile(io.BytesIO(response.content)) as zip_ref:
        zip_ref.extractall(temp_dir)
        
    # The extracted zip usually contains a single root folder (e.g., owner-repo-commitHash)
    # Let's find it and return the path to the actual contents
    extracted_items = os.listdir(temp_dir)
    if len(extracted_items) == 1 and os.path.isdir(os.path.join(temp_dir, extracted_items[0])):
        return os.path.join(temp_dir, extracted_items[0])
        
    return temp_dir

def cleanup_repo_dir(dir_path: str):
    """
    Deletes the temporary directory and all its contents.
    """
    if os.path.exists(dir_path):
        shutil.rmtree(dir_path, ignore_errors=True)
