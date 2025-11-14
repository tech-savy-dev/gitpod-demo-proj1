# Use Gitpod's base workspace image
FROM gitpod/workspace-base

# Set working directory
WORKDIR /app

# Switch to root for installation
USER root

# Install Python and pip
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
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
LABEL description="Simple Python Calculator Application"

# Switch back to gitpod user
USER gitpod

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["python3", "app.py"]
