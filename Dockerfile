# Use Gitpod's Python workspace image (includes Python, Docker, and common tools)
FROM gitpod/workspace-python

# Set working directory in container
WORKDIR /app

# Switch to root for installation
USER root

# Install additional dependencies if needed
RUN apt-get update && apt-get install -y \
    iptables \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy application code and entrypoint
COPY app.py .
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directory for logs
RUN mkdir -p /var/log

# Set metadata
LABEL maintainer="project1"
LABEL description="Simple Python Calculator Application with Docker-in-Docker using Gitpod Python workspace"

# Stay as root (required for Docker daemon)
USER root

# Set entrypoint to start Docker daemon first
ENTRYPOINT ["/entrypoint.sh"]

# Default command to run the application
CMD ["python3", "app.py"]