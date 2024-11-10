# Linux Installation Guide

## Prerequisites

### System Requirements
- Linux-based operating system (Ubuntu 20.04 or later recommended)
- Python 3.8 or later
- Node.js 18 or later
- 4GB RAM minimum (8GB recommended)
- 10GB free disk space

## Quick Installation

1. Clone the repository:
```bash
git clone https://github.com/sanjay-dastute/Bug-bounty-tool.git
cd Bug-bounty-tool
```

2. Run the installation script:
```bash
chmod +x install.sh
./install.sh
```

3. Start the application:
```bash
# Terminal 1: Start backend
cd backend
python3 main.py

# Terminal 2: Start frontend
cd frontend
npm run dev
```

4. Access the application:
- Open http://localhost:3000 in your browser

## Manual Installation (If automatic script fails)

1. Install system dependencies:
```bash
sudo apt-get update
sudo apt-get install -y python3 python3-pip nodejs npm nmap nikto masscan git curl wget
```

2. Install Go (required for some tools):
```bash
wget https://go.dev/dl/go1.21.8.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.21.8.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
```

3. Install security tools:
```bash
# Go tools
go install -v github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
go install -v github.com/projectdiscovery/dnsx/cmd/dnsx@latest
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
go install -v github.com/OWASP/Amass/v3/...@latest

# Python tools
pip3 install mobsf mythril slither-analyzer manticore semgrep frida-tools objection apkleaks prowler scoutsuite

# Node.js tools
sudo npm install -g snyk
```

4. Install application dependencies:
```bash
# Frontend
cd frontend
npm install

# Backend
cd ../backend
pip3 install -r requirements.txt
```

## Usage

1. Start the backend server:
```bash
cd backend
python3 main.py
```

2. Start the frontend development server:
```bash
cd frontend
npm run dev
```

3. Access the web interface:
- Open http://localhost:3000 in your browser
- Follow the scanning guide in docs/usage/scanning_guide.md

## Troubleshooting

1. Python Package Issues:
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt --no-cache-dir
```

2. Node.js Issues:
```bash
# Clear npm cache
npm cache clean --force
# Reinstall dependencies
rm -rf node_modules
npm install
```

3. Permission Issues:
```bash
# Fix Python package permissions
sudo chown -R $USER:$USER ~/.local

# Fix npm permissions
sudo chown -R $USER:$USER ~/.npm
```

## Uninstallation

1. Remove the application:
```bash
rm -rf Bug-bounty-tool
```

2. Remove installed tools (optional):
```bash
# Python tools
pip3 uninstall -y mobsf mythril slither-analyzer manticore semgrep frida-tools objection apkleaks prowler scoutsuite

# Node.js tools
sudo npm uninstall -g snyk

# Go tools will remain in $GOPATH/bin
```

For detailed usage instructions, see the [Scanning Guide](../usage/scanning_guide.md).
