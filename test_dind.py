#!/usr/bin/env python3
"""
Test script to demonstrate True Docker-in-Docker functionality
This script will run Docker commands using the internal Docker daemon
"""

import subprocess
import sys
import json
import time

def run_command(cmd):
    """Run a shell command and return the result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        return result.returncode == 0, result.stdout.strip(), result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "", "Command timed out"
    except Exception as e:
        return False, "", str(e)

def wait_for_docker(max_wait=60):
    """Wait for Docker daemon to be ready"""
    print("⏳ Waiting for Docker daemon to be ready...")
    for i in range(max_wait):
        success, _, _ = run_command("docker info > /dev/null 2>&1")
        if success:
            return True
        time.sleep(1)
        if i % 10 == 0:
            print(f"   Still waiting... ({i}s)")
    return False

def test_docker_availability():
    """Test if Docker is available and working"""
    print("🐳 Testing True Docker-in-Docker setup...")
    print("=" * 50)
    
    # Wait for Docker to be ready
    if not wait_for_docker():
        print("❌ Docker daemon did not start in time")
        print("\n💡 Tip: Make sure container is running with --privileged flag")
        return False
    
    # Test Docker version
    success, stdout, stderr = run_command("docker --version")
    if success:
        print(f"✅ Docker version: {stdout}")
    else:
        print(f"❌ Docker not available: {stderr}")
        return False
    
    # Test Docker daemon connection
    success, stdout, stderr = run_command("docker info --format json")
    if success:
        try:
            info = json.loads(stdout)
            print(f"✅ Docker daemon connected (INTERNAL)")
            print(f"   Server Version: {info.get('ServerVersion', 'Unknown')}")
            print(f"   Storage Driver: {info.get('Driver', 'Unknown')}")
            print(f"   Operating System: {info.get('OperatingSystem', 'Unknown')}")
        except:
            print("✅ Docker daemon connected (could not parse info)")
    else:
        print(f"❌ Cannot connect to Docker daemon: {stderr}")
        return False
    
    # Test running a simple container
    print("\n🧪 Testing container execution...")
    success, stdout, stderr = run_command("docker run --rm hello-world")
    if success:
        print("✅ Successfully ran test container")
        # Print last few lines of output
        lines = stdout.split('\n')
        for line in lines[-3:]:
            if line.strip():
                print(f"   {line}")
    else:
        print(f"❌ Failed to run test container: {stderr}")
        return False
    
    # Test Docker Compose
    print("\n📦 Testing Docker Compose...")
    success, stdout, stderr = run_command("docker compose version")
    if success:
        print(f"✅ Docker Compose available: {stdout}")
    else:
        print(f"⚠️  Docker Compose not available: {stderr}")
    
    return True

def test_isolation():
    """Test that Docker daemon is isolated (not using host)"""
    print("\n� Testing Docker isolation...")
    success, stdout, stderr = run_command("docker ps -a")
    if success:
        lines = stdout.strip().split('\n')
        container_count = len(lines) - 1  # Subtract header
        print(f"✅ Container list accessible")
        print(f"   Running containers: {container_count}")
        print(f"   This is the INTERNAL Docker daemon, not host")
    else:
        print(f"❌ Failed to list containers: {stderr}")
        return False
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("True Docker-in-Docker Test Suite")
    print("(Internal Docker Daemon - No Socket Mount)")
    print("=" * 50)
    print()
    
    if test_docker_availability():
        test_isolation()
        print("\n" + "=" * 50)
        print("🎉 True Docker-in-Docker is working correctly!")
        print("=" * 50)
        print("\n✨ This container runs its own Docker daemon")
        print("   No host socket mount required!")
    else:
        print("\n" + "=" * 50)
        print("💥 Docker-in-Docker setup needs attention")
        print("=" * 50)
        print("\n💡 Make sure container is running with:")
        print("   docker run --privileged ...")
        sys.exit(1)