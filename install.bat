@echo off
echo === Bug Bounty Tool Installation Script ===
echo This script will install all required dependencies and tools.

:: Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is required but not installed.
    echo Please install Python from https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    exit /b 1
)

:: Check Node.js installation
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Node.js is required but not installed.
    echo Please install Node.js from https://nodejs.org/
    exit /b 1
)

:: Check Go installation
go version >nul 2>&1
if %errorlevel% neq 0 (
    echo Go is required but not installed.
    echo Please install Go from https://go.dev/dl/
    exit /b 1
)

:: Install Go-based tools
echo Installing Go-based security tools...
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/OWASP/Amass/v3/...@latest

:: Install Python-based tools
echo Installing Python-based security tools...
pip install mobsf mythril slither-analyzer manticore semgrep frida-tools objection apkleaks prowler scoutsuite

:: Install Node.js based tools
echo Installing Node.js based tools...
npm install -g snyk

:: Install application dependencies
echo Installing application dependencies...
cd frontend
npm install
cd ../backend
pip install -r requirements.txt

echo === Installation Complete ===
echo.
echo Usage:
echo 1. Start the backend:
echo    cd backend ^& python main.py
echo.
echo 2. Start the frontend:
echo    cd frontend ^& npm run dev
echo.
echo 3. Access the application:
echo    Open http://localhost:3000 in your browser
echo.
echo For detailed usage instructions, see docs/usage/scanning_guide.md
