FROM python:3.10-slim

# Install git (needed if any dependencies require it, or for downloading repos)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Set up a new user named "user" with user ID 1000
# This is a strict requirement/best practice for Hugging Face Spaces
RUN useradd -m -u 1000 user

# Switch to the "user" user
USER user

# Set environment variables for the user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory inside the user's home folder
WORKDIR $HOME/app

# Copy requirements first to leverage Docker cache (chown gives the user permission)
COPY --chown=user requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY --chown=user . .

# Hugging Face Spaces expose port 7860 by default
EXPOSE 7860

# Command to run the application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "7860"]
