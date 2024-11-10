# Windows Installation Guide

## Prerequisites
- Windows 10/11 64-bit
- Python 3.8 or later
- Node.js 18 or later
- Git for Windows
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

## Quick Installation

1. Install Required Software:
   - [Python 3.12](https://www.python.org/downloads/) (Check "Add Python to PATH")
   - [Node.js 18 LTS](https://nodejs.org/) (Accept all defaults)
   - [Git for Windows](https://git-scm.com/download/win)
   - [Nmap](https://nmap.org/download.html) (Install WinPcap if prompted)
   - [Go](https://go.dev/dl/) (Required for some tools)

2. Clone and Install:
```cmd
:: Clone repository
git clone https://github.com/sanjay-dastute/Bug-bounty-tool.git
cd Bug-bounty-tool

:: Run installation script
install.bat
```

3. Start the Application:
```cmd
:: Terminal 1: Start backend
cd backend
python main.py

:: Terminal 2: Start frontend
cd frontend
npm run dev
```

4. Access the application:
- Open http://localhost:3000 in your browser

## Manual Installation (If automatic script fails)

1. Install Security Tools:
```cmd
:: Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/OWASP/Amass/v3/...@latest

:: Python tools
pip install mobsf mythril slither-analyzer manticore semgrep frida-tools objection apkleaks prowler scoutsuite

:: Node.js tools
npm install -g snyk
```

2. Install Application Dependencies:
```cmd
:: Frontend
cd frontend
npm install

:: Backend
cd ../backend
pip install -r requirements.txt
```

## Usage

1. Start the Backend:
```cmd
cd backend
python main.py
```

2. Start the Frontend:
```cmd
cd frontend
npm run dev
```

3. Access the Web Interface:
- Open http://localhost:3000 in your browser
- Follow the scanning guide in docs/usage/scanning_guide.md

## Troubleshooting

1. Python Issues:
```cmd
:: Upgrade pip
python -m pip install --upgrade pip
:: Reinstall requirements
pip install -r requirements.txt --no-cache-dir
```

2. Node.js Issues:
```cmd
:: Clear npm cache
npm cache clean --force
:: Reinstall dependencies
rmdir /s /q node_modules
npm install
```

3. Permission Issues:
- Run Command Prompt as Administrator
- Try using Python virtual environment

## Uninstallation

1. Remove Application:
```cmd
rmdir /s /q Bug-bounty-tool
```

2. Remove Tools (Optional):
```cmd
:: Python tools
pip uninstall -y mobsf mythril slither-analyzer manticore semgrep frida-tools objection apkleaks prowler scoutsuite

:: Node.js tools
npm uninstall -g snyk
```

For detailed usage instructions, see the [Scanning Guide](../usage/scanning_guide.md).
