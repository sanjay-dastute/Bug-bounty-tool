#!/usr/bin/env python3
import os
import sys
import shutil
import subprocess
from pathlib import Path

def run_command(command, cwd=None):
    """Run a shell command and return its output"""
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            check=True,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {command}")
        print(f"Error output: {e.stderr}")
        sys.exit(1)

def package_frontend():
    """Build and package the frontend"""
    print("Building frontend...")
    frontend_dir = Path("frontend")
    run_command("npm install", cwd=frontend_dir)
    run_command("npm run build", cwd=frontend_dir)

def package_backend():
    """Package the backend and its dependencies"""
    print("Packaging backend...")
    backend_dir = Path("backend")

    # Create virtual environment
    venv_dir = backend_dir / "venv"
    run_command(f"python -m venv {venv_dir}")

    # Install dependencies in venv
    if sys.platform == "win32":
        pip_path = venv_dir / "Scripts" / "pip"
    else:
        pip_path = venv_dir / "bin" / "pip"

    # Install required packages
    packages = [
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "python-multipart",
        "python-jose[cryptography]",
        "passlib[bcrypt]",
        "scikit-learn",
        "joblib",
        "requests",
        "aiohttp",
        "docker",
        "mythril",
    ]

    for package in packages:
        run_command(f"{pip_path} install {package}", cwd=backend_dir)

    # Save requirements
    run_command(f"{pip_path} freeze > requirements.txt", cwd=backend_dir)

def create_launcher_scripts():
    """Create platform-specific launcher scripts"""
    scripts_dir = Path("scripts")

    # Linux launcher
    linux_launcher = """#!/bin/bash
# Bug Bounty Tool Launcher for Linux

# Check for required system dependencies
command -v docker >/dev/null 2>&1 || { echo "Docker is required but not installed. Please install Docker first."; exit 1; }
command -v nmap >/dev/null 2>&1 || { echo "Nmap is required but not installed. Please install Nmap first."; exit 1; }

# Set environment variables
export PYTHONPATH="backend:$PYTHONPATH"
export NODE_ENV=production

# Start backend server
source backend/venv/bin/activate
echo "Starting backend server..."
python backend/main.py &
BACKEND_PID=$!

# Wait for backend to start
sleep 2

# Start frontend
cd frontend
echo "Starting frontend..."
npm start &
FRONTEND_PID=$!

# Handle shutdown
cleanup() {
    echo "Shutting down services..."
    kill $BACKEND_PID $FRONTEND_PID
    exit 0
}

trap cleanup SIGINT SIGTERM

# Keep running
wait
"""

    # Windows launcher
    windows_launcher = """@echo off
:: Bug Bounty Tool Launcher for Windows

:: Check for required system dependencies
where docker >nul 2>nul
if %errorlevel% neq 0 (
    echo Docker is required but not installed. Please install Docker Desktop first.
    exit /b 1
)

where nmap >nul 2>nul
if %errorlevel% neq 0 (
    echo Nmap is required but not installed. Please install Nmap first.
    exit /b 1
)

:: Set environment variables
set PYTHONPATH=backend;%PYTHONPATH%
set NODE_ENV=production

:: Start backend server
echo Starting backend server...
call backend\\venv\\Scripts\\activate
start /B python backend\\main.py

:: Wait for backend to start
timeout /t 2 /nobreak >nul

:: Start frontend
echo Starting frontend...
cd frontend
start /B npm start

:: Keep the window open
echo Services started. Press Ctrl+C to exit.
pause >nul
"""

    # Create launcher scripts
    with open(scripts_dir / "launch_linux.sh", "w") as f:
        f.write(linux_launcher)

    with open(scripts_dir / "launch_windows.bat", "w") as f:
        f.write(windows_launcher)

    # Make Linux launcher executable
    if sys.platform != "win32":
        os.chmod(scripts_dir / "launch_linux.sh", 0o755)

def create_docker_compose():
    """Create docker-compose.yml for required services"""
    docker_compose = """version: '3.8'
services:
  postgres:
    image: postgres:latest
    environment:
      POSTGRES_DB: bugbounty
      POSTGRES_USER: bugbounty
      POSTGRES_PASSWORD: ${DB_PASSWORD:-securepassword}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  mobsf: # Mobile Security Framework
    image: opensecurity/mobile-security-framework-mobsf:latest
    ports:
      - "8000:8000"
    volumes:
      - mobsf_data:/home/mobsf/.MobSF

volumes:
  postgres_data:
  mobsf_data:
"""

    with open("docker-compose.yml", "w") as f:
        f.write(docker_compose)

def package_application():
    """Package the entire application for distribution"""
    # Create dist directory
    dist_dir = Path("dist")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir()

    # Package components
    package_frontend()
    package_backend()
    create_launcher_scripts()
    create_docker_compose()

    # Copy required files to dist
    dirs_to_copy = ["backend", "frontend/build", "scripts"]
    files_to_copy = ["docker-compose.yml", "README.md"]

    for dir_name in dirs_to_copy:
        src = Path(dir_name)
        dst = dist_dir / src.name
        if src.exists():
            shutil.copytree(src, dst)

    for file_name in files_to_copy:
        src = Path(file_name)
        if src.exists():
            shutil.copy2(src, dist_dir)

    # Create platform-specific archives
    platform_suffix = "win" if sys.platform == "win32" else "linux"
    archive_name = f"bug-bounty-tool-{platform_suffix}"
    shutil.make_archive(archive_name, "zip", dist_dir)
    print(f"Application packaged successfully: {archive_name}.zip")

def main():
    try:
        package_application()
    except Exception as e:
        print(f"Error packaging application: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
