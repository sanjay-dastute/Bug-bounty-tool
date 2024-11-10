# Windows Installation Guide

## Prerequisites

### System Requirements
- Windows 10/11 64-bit
- Python 3.12 or later
- Node.js 18 or later
- Docker Desktop
- 4GB RAM minimum (8GB recommended)
- 20GB free disk space
- Windows Terminal (recommended)

### Required Software Installation

1. Install Python:
   - Download Python 3.12 from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"
   - Verify installation:
     ```cmd
     python --version
     pip --version
     ```

2. Install Node.js:
   - Download Node.js 18 LTS from [nodejs.org](https://nodejs.org/)
   - During installation, accept all defaults
   - Verify installation:
     ```cmd
     node --version
     npm --version
     ```

3. Install Docker Desktop:
   - Download from [docker.com](https://www.docker.com/products/docker-desktop)
   - Follow installation wizard
   - Enable WSL 2 if prompted
   - Start Docker Desktop
   - Verify installation:
     ```cmd
     docker --version
     docker-compose --version
     ```

4. Install Nmap:
   - Download from [nmap.org](https://nmap.org/download.html)
   - Choose Windows installer
   - During installation, install WinPcap if prompted
   - Verify installation:
     ```cmd
     nmap --version
     ```

## Installation Steps

1. Download and Extract:
   - Download `bug-bounty-tool-win.zip`
   - Right-click > Extract All
   - Open Command Prompt as Administrator in extracted folder

2. Set up Backend:
   ```cmd
   :: Activate virtual environment
   cd backend
   .\venv\Scripts\activate

   :: Install dependencies
   pip install -r requirements.txt
   cd ..
   ```

3. Set up Frontend:
   ```cmd
   cd frontend
   npm install
   cd ..
   ```

4. Configure Environment:
   ```cmd
   :: Create .env file
   echo DB_PASSWORD=your_secure_password> .env
   echo JWT_SECRET=your_jwt_secret>> .env
   echo MOBSF_API_KEY=your_mobsf_key>> .env
   ```

5. Start Services:
   ```cmd
   :: Start Docker containers
   docker-compose up -d
   ```

## Running the Application

### Using Launcher Script
```cmd
scripts\launch_windows.bat
```

### Manual Startup
1. Terminal 1 (Backend):
   ```cmd
   cd backend
   .\venv\Scripts\activate
   python main.py
   ```

2. Terminal 2 (Frontend):
   ```cmd
   cd frontend
   npm start
   ```

Access the application at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Troubleshooting

### Common Issues

1. Port Conflicts:
   ```cmd
   :: Check ports
   netstat -ano | findstr :3000
   netstat -ano | findstr :8000
   ```

2. Docker Issues:
   - Restart Docker Desktop
   - Check Docker logs in Docker Desktop
   - Run:
     ```cmd
     docker-compose down
     docker-compose up -d
     ```

3. Python Environment Issues:
   ```cmd
   :: Recreate virtual environment
   rmdir /s /q backend\venv
   python -m venv backend\venv
   backend\venv\Scripts\activate
   pip install -r backend\requirements.txt
   ```

4. Node.js Issues:
   ```cmd
   :: Clear npm cache
   cd frontend
   npm cache clean --force
   del /s /q node_modules
   npm install
   ```

### Logs Location
- Backend logs: `backend\logs\`
- Frontend logs: `frontend\logs\`
- Docker logs: Docker Desktop Dashboard

## Security Considerations

1. Windows Defender Firewall:
   - Allow inbound connections for:
     - Python (Backend)
     - Node.js (Frontend)
     - Docker Desktop
     - Nmap

2. Secure Environment File:
   - Restrict .env file permissions:
     ```cmd
     icacls .env /inheritance:r
     icacls .env /grant:r "%USERNAME%":F
     ```

3. Regular Updates:
   ```cmd
   :: Update dependencies
   pip install --upgrade -r backend\requirements.txt
   cd frontend && npm update && cd ..
   ```

## Uninstallation

1. Stop Services:
   ```cmd
   :: Stop Docker containers
   docker-compose down -v
   ```

2. Remove Files:
   ```cmd
   :: Remove application directory
   cd ..
   rmdir /s /q bug-bounty-tool
   ```

3. Clean Docker (Optional):
   ```cmd
   :: Remove Docker images
   docker rmi opensecurity/mobile-security-framework-mobsf
   docker rmi postgres:latest
   ```

4. Remove Dependencies (Optional):
   - Uninstall Docker Desktop
   - Uninstall Python
   - Uninstall Node.js
   - Uninstall Nmap
