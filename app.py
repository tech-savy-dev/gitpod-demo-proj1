"""
Simple Python Application - Project 1
This is a basic calculator app that demonstrates Docker containerization with Docker-in-Docker support.
"""

import subprocess
import sys

def add(a, b):
    """Add two numbers"""
    return a + b

def subtract(a, b):
    """Subtract two numbers"""
    return a - b

def multiply(a, b):
    """Multiply two numbers"""
    return a * b

def divide(a, b):
    """Divide two numbers"""
    if b == 0:
        return "Error: Division by zero"
    return a / b

def check_docker():
    """Check if Docker is available inside the container"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            return result.stdout.strip()
        else:
            return "Docker not available"
    except Exception as e:
        return f"Docker check failed: {str(e)}"

def list_docker_images():
    """List Docker images available"""
    try:
        result = subprocess.run(['docker', 'images', '--format', '{{.Repository}}:{{.Tag}}'], 
                              capture_output=True, 
                              text=True, 
                              timeout=10)
        if result.returncode == 0:
            images = result.stdout.strip().split('\n')
            return images if images[0] else ["No images found"]
        else:
            return ["Unable to list images"]
    except Exception as e:
        return [f"Error: {str(e)}"]

def main():
    print("=" * 60)
    print("Welcome to Simple Calculator - Project 1 (Docker-in-Docker)")
    print("=" * 60)
    
    # Demonstrate all operations
    num1, num2 = 10, 5
    
    print(f"\n📊 Operations on {num1} and {num2}:")
    print(f"   Addition: {num1} + {num2} = {add(num1, num2)}")
    print(f"   Subtraction: {num1} - {num2} = {subtract(num1, num2)}")
    print(f"   Multiplication: {num1} * {num2} = {multiply(num1, num2)}")
    print(f"   Division: {num1} / {num2} = {divide(num1, num2)}")
    
    print("\n" + "=" * 60)
    print("🐳 Docker-in-Docker Check:")
    print("=" * 60)
    docker_version = check_docker()
    print(f"   {docker_version}")
    
    print("\n📦 Available Docker Images:")
    images = list_docker_images()
    for img in images[:5]:  # Show first 5 images
        print(f"   - {img}")
    
    print("\n" + "=" * 60)
    print("✅ Application running successfully in Docker!")
    print("=" * 60)

if __name__ == "__main__":
    main()
