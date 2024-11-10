# Linux Installation Guide

## Prerequisites

### System Requirements
- Linux-based operating system (Ubuntu 20.04 or later recommended)
- Python 3.12 or later
- Node.js 18 or later
- Docker and Docker Compose
- 4GB RAM minimum (8GB recommended)
- 20GB free disk space

### Required Dependencies
```bash
# Update package list
sudo apt update

# Install system dependencies
sudo apt install -y \
    python3.12 \
    python3.12-venv \
    python3-pip \
    nodejs \
    npm \
    docker.io \
    docker-compose \
    nmap \
    git

# Start and enable Docker service
sudo systemctl start docker
sudo systemctl enable docker

# Add current user to docker group
sudo usermod -aG docker $USER
```

## Installation Steps

1. Download and extract the application:
```bash
unzip bug-bounty-tool-linux.zip
cd bug-bounty-tool
```

2. Set up the backend:
```bash
# Activate virtual environment
source backend/venv/bin/activate

# Install Python dependencies
pip install -r backend/requirements.txt
```

3. Set up the frontend:
```bash
cd frontend
npm install
cd ..
```

4. Configure environment variables:
```bash
# Create .env file
cat > .env << EOL
DB_PASSWORD=your_secure_password
JWT_SECRET=your_jwt_secret
MOBSF_API_KEY=your_mobsf_key
EOL
```

5. Start required services:
```bash
# Start PostgreSQL and MobSF containers
docker-compose up -d
```

## Running the Application

1. Using the launcher script:
```bash
./scripts/launch_linux.sh
```

2. Manual startup (if needed):
```bash
# Terminal 1: Start backend
source backend/venv/bin/activate
python backend/main.py

# Terminal 2: Start frontend
cd frontend
npm start
```

The application will be available at:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## Troubleshooting

### Common Issues

1. Port conflicts:
```bash
# Check if ports are in use
sudo lsof -i :3000
sudo lsof -i :8000
```

2. Docker issues:
```bash
# Restart Docker service
sudo systemctl restart docker

# Check Docker logs
docker-compose logs
```

3. Permission issues:
```bash
# Fix permissions
sudo chown -R $USER:$USER .
chmod +x scripts/launch_linux.sh
```

### Logs Location
- Backend logs: `backend/logs/`
- Frontend logs: `frontend/logs/`
- Docker logs: Use `docker-compose logs`

## Security Considerations

1. Firewall configuration:
```bash
# Allow required ports
sudo ufw allow 3000/tcp
sudo ufw allow 8000/tcp
```

2. Secure the environment file:
```bash
chmod 600 .env
```

3. Regular updates:
```bash
# Update dependencies
pip install --upgrade -r backend/requirements.txt
cd frontend && npm update && cd ..
```

## Uninstallation

To completely remove the application:
```bash
# Stop containers
docker-compose down -v

# Remove files
cd ..
rm -rf bug-bounty-tool

# Remove Docker images (optional)
docker rmi opensecurity/mobile-security-framework-mobsf
docker rmi postgres:latest
```
