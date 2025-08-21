# Python slim image
FROM python:3.12-slim

# Install system dependencies (if any future additions like ffmpeg needed, uncomment)
# RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for layer caching
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . /app

# Create output directory inside container
RUN mkdir -p /downloads

# Default command expects a YouTube URL argument.
# Example: docker run image "https://youtu.be/xxxx" 
ENTRYPOINT ["python", "ytCaptionDownloader.py"]
