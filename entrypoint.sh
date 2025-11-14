#!/bin/bash
set -e

echo "🐳 Starting Docker daemon..."

# Start Docker daemon in the background
dockerd --storage-driver=vfs --host=unix:///var/run/docker.sock > /var/log/dockerd.log 2>&1 &

# Wait for Docker daemon to be ready
echo "⏳ Waiting for Docker daemon to start..."
timeout=30
while [ $timeout -gt 0 ]; do
    if docker info > /dev/null 2>&1; then
        echo "✅ Docker daemon is ready!"
        break
    fi
    sleep 1
    timeout=$((timeout - 1))
done

if [ $timeout -eq 0 ]; then
    echo "❌ Docker daemon failed to start within 30 seconds"
    cat /var/log/dockerd.log
    exit 1
fi

# Show Docker version
echo "📦 Docker version:"
docker --version

# Execute the main command
echo "🚀 Starting application..."
exec "$@"
