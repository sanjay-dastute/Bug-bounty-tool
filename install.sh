#!/bin/bash
set -e

echo "=== Bug Bounty Tool Installation Script ==="
echo "This script will install all required dependencies and tools."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Function to install Python package
install_python_package() {
    echo "Installing $1..."
    pip3 install "$1" || echo "Warning: Failed to install $1, continuing..."
}

# Function to install system package
install_system_package() {
    echo "Installing $1..."
    if command_exists apt-get; then
        sudo apt-get install -y "$1"
    elif command_exists yum; then
        sudo yum install -y "$1"
    elif command_exists pacman; then
        sudo pacman -S --noconfirm "$1"
    else
        echo "Warning: Package manager not found. Please install $1 manually."
    fi
}

# Check Python installation
if ! command_exists python3; then
    echo "Installing Python 3..."
    install_system_package python3
    install_system_package python3-pip
fi

# Check Node.js installation
if ! command_exists node; then
    echo "Installing Node.js..."
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    install_system_package nodejs
fi

# Install system dependencies
echo "Installing system dependencies..."
SYSTEM_PACKAGES="nmap nikto masscan git curl wget"
for package in $SYSTEM_PACKAGES; do
    install_system_package "$package"
done

# Install Go for Go-based tools
if ! command_exists go; then
    echo "Installing Go..."
    wget https://go.dev/dl/go1.21.8.linux-amd64.tar.gz
    sudo rm -rf /usr/local/go
    sudo tar -C /usr/local -xzf go1.21.8.linux-amd64.tar.gz
    echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
    source ~/.bashrc
fi

# Install Go-based tools
echo "Installing Go-based security tools..."
GO_TOOLS="github.com/projectdiscovery/subfinder/v2/cmd/subfinder@latest
          github.com/projectdiscovery/dnsx/cmd/dnsx@latest
          github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest
          github.com/OWASP/Amass/v3/...@latest"
for tool in $GO_TOOLS; do
    go install -v "$tool"
done

# Install Python-based security tools
echo "Installing Python-based security tools..."
PYTHON_PACKAGES="mobsf mythril slither-analyzer manticore semgrep frida-tools objection apkleaks prowler scoutsuite"
for package in $PYTHON_PACKAGES; do
    install_python_package "$package"
done

# Install Node.js based tools
echo "Installing Node.js based tools..."
NPM_PACKAGES="snyk"
for package in $NPM_PACKAGES; do
    sudo npm install -g "$package"
done

# Install application dependencies
echo "Installing application dependencies..."
cd frontend
npm install
cd ../backend
pip3 install -r requirements.txt

echo "=== Installation Complete ==="
echo "
Usage:
1. Start the backend:
   cd backend && python3 main.py

2. Start the frontend:
   cd frontend && npm run dev

3. Access the application:
   Open http://localhost:3000 in your browser

For detailed usage instructions, see docs/usage/scanning_guide.md"
