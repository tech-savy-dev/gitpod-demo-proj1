````markdown
# Project 1 - Simple Python Calculator with True Docker-in-Docker

This is a simple Python calculator application containerized with **True Docker-in-Docker** (DinD) support. The container runs its own Docker daemon internally - **no host socket mounting required!**

## 🎯 Key Feature: Self-Contained Docker

✨ **This image runs Docker INSIDE the container**
- ✅ No need to mount `/var/run/docker.sock`
- ✅ Isolated Docker environment
- ✅ Only requires `privileged: true`
- ✅ Perfect for use in other projects

## Structure
- `app.py` - Main Python application
- `Dockerfile` - Docker configuration with true DinD support
- `docker-compose.yml` - Docker Compose configuration
- `entrypoint.sh` - Starts Docker daemon automatically
- `.devcontainer/devcontainer.json` - VS Code Dev Container configuration
- `requirements.txt` - Python dependencies
- `test_dind.py` - Test script to verify DinD functionality
- `USAGE_IN_OTHER_PROJECTS.md` - Guide for using in other projects

## Build and Run

### Build Docker Image
```bash
docker build -t python-calculator:v1.0 .
```

### Run Container with True Docker-in-Docker
```bash
# Method 1: Using docker run
docker run -it --privileged python-calculator:v1.0

# Method 2: Using docker-compose (recommended)
docker-compose up --build

# Method 3: Interactive bash session
docker run -it --privileged python-calculator:v1.0 /bin/bash
# Inside container, you can run: docker ps, docker images, docker run hello-world, etc.
```

### Test Docker Inside Container
```bash
# Run the test script
docker run --privileged python-calculator:v1.0 python3 test_dind.py
```

## 🚀 Use in Another Project

In your other project's `docker-compose.yml`:

```yaml
version: '3.8'

services:
  my-service:
    image: python-calculator:v1.0
    privileged: true  # Only this is needed!
    # NO socket mount required!
    volumes:
      - ./my-code:/workspace
    working_dir: /workspace
```

See `USAGE_IN_OTHER_PROJECTS.md` and `example-other-project-compose.yml` for more examples.

## Features
- ✅ **True Docker-in-Docker** - Runs its own Docker daemon
- ✅ **No Socket Mount** - No need for `/var/run/docker.sock:/var/run/docker.sock`
- ✅ **Isolated Environment** - Independent from host Docker
- ✅ **Auto-start Daemon** - Docker daemon starts automatically via entrypoint
- ✅ **Python Application** - Includes calculator app example
- ✅ **Ready for Reuse** - Can be used in any other project

## Docker-in-Docker Details
- Uses Gitpod workspace-base image (includes Docker & Docker Compose)
- Docker daemon starts automatically via `entrypoint.sh`
- Uses `vfs` storage driver for compatibility
- Requires `privileged: true` (Docker daemon requirement)
- **No host Docker socket mounting needed**

## Why This Approach?

### ✅ Advantages
- **Security**: No exposure of host Docker socket
- **Isolation**: Completely separate Docker environment
- **Portability**: Works anywhere privileged containers are supported
- **Simple**: Just add `privileged: true` - nothing else needed

### ⚠️ Requirements
- Container must run with `privileged: true`
- Slightly slower than socket mounting (uses vfs storage driver)

## Testing

```bash
# Build the image
docker build -t python-calculator:v1.0 .

# Test Docker inside container
docker run --privileged python-calculator:v1.0 python3 test_dind.py

# Interactive testing
docker run -it --privileged python-calculator:v1.0 /bin/bash
docker --version
docker run hello-world
```

````
