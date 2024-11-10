# Bug Bounty Tool - User Guide

This guide covers the installation, setup, and usage of all capabilities in the Bug Bounty Tool.

## Table of Contents
1. [Installation](#installation)
2. [Getting Started](#getting-started)
3. [Web Application Scanning](#web-application-scanning)
4. [Mobile Application Security](#mobile-application-security)
5. [API Security Testing](#api-security-testing)
6. [Source Code Analysis](#source-code-analysis)
7. [Smart Contract Auditing](#smart-contract-auditing)
8. [Blockchain Security](#blockchain-security)
9. [Understanding Results](#understanding-results)
10. [Best Practices](#best-practices)

## Installation

### Prerequisites
- Python 3.8 or later
- Node.js 18 or later
- Go (latest version)
- Git

### Linux Installation
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

### Windows Installation
1. Install required software:
   - Python: https://www.python.org/downloads/ (Check "Add Python to PATH")
   - Node.js: https://nodejs.org/ (LTS version)
   - Go: https://go.dev/dl/
   - Git: https://git-scm.com/download/win

2. Clone and install:
   ```cmd
   git clone https://github.com/sanjay-dastute/Bug-bounty-tool.git
   cd Bug-bounty-tool
   install.bat
   ```

## Getting Started

### Starting the Application
1. Start the backend server:
   ```bash
   cd backend
   python3 main.py  # Use 'python' on Windows
   ```

2. Start the frontend development server:
   ```bash
   cd frontend
   npm run dev
   ```

3. Access the application:
   - Open http://localhost:3000 in your browser
   - Log in with your credentials
   - Start a new scan from the dashboard

### Quick Start Guide
1. Navigate to "New Scan" in the dashboard
2. Select the type of scan you want to perform
3. Enter target information
4. Configure scan options
5. Start the scan
6. Monitor progress in real-time
7. Review results in the dashboard

## Web Application Scanning

### Scanning Options
1. Select "Web Application" as scan type
2. Enter target URL
3. Choose scanning tools:
   - Nmap: Network/port scanning
   - Nuclei: Vulnerability scanning

### Advanced Options
- **Scan Types**:
  - Quick: Basic system checks
  - Normal: Standard assessment
  - Deep: Comprehensive analysis

- **Custom Configurations**:
  ```yaml
  # Example nuclei configuration
  rate-limit: 150
  bulk-size: 25
  concurrency: 25
  ```

### Recommended Approach
- Begin with system assessment
- Follow with comprehensive scan
- Use custom templates for specific tests

## Mobile Application Security

### Supported Platforms
- Android (APK files)
- iOS (IPA files)

### Scanning Steps
1. Select "Mobile Application" scan type
2. Upload APK/IPA file or provide URL
3. Choose MobSF as scanning tool
4. Configure analysis options:
   - Static Analysis
   - Dynamic Analysis (Android only)
   - API Security

### Key Features
- OWASP Mobile Top 10 checks
- Binary analysis
- Permission analysis
- API security testing
- Malware detection

## API Security Testing

### Supported API Types
- REST
- GraphQL
- SOAP
- WebSocket

### Testing Process
1. Select "API Endpoint" scan type
2. Enter API endpoint URL
3. Configure authentication:
   ```json
   {
     "type": "bearer",
     "token": "your_token",
     "headers": {
       "Custom-Header": "value"
     }
   }
   ```

### Test Cases
- Authentication bypass
- Authorization flaws
- Input validation
- Rate limiting
- Business logic flaws

## Source Code Analysis

### Supported Languages
- Python
- JavaScript/TypeScript
- Java
- Go
- Solidity

### Analysis Steps
1. Select "Source Code" scan type
2. Provide repository URL or upload files
3. Configure analysis settings:
   ```yaml
   depth: full
   ignore_patterns:
     - "*.test.js"
     - "vendor/*"
   ```

### Security Checks
- SAST (Static Application Security Testing)
- Dependency analysis
- Secret detection
- Code quality
- Custom rule integration

## Smart Contract Auditing

### Supported Platforms
- Ethereum
- Binance Smart Chain
- Polygon
- Other EVM-compatible chains

### Audit Process
1. Select "Smart Contract" scan type
2. Enter contract address or upload source code
3. Configure Mythril scanner:
   ```yaml
   analysis_mode: full
   transaction_count: 3
   max_depth: 50
   ```

### Security Checks
- Reentrancy
- Integer overflow/underflow
- Access control
- Gas optimization
- Business logic flaws

## Blockchain Security

### Features
- Network analysis
- Transaction monitoring
- Smart contract interaction
- Token security

### Analysis Steps
1. Select "Blockchain" scan type
2. Enter blockchain address/endpoint
3. Configure analysis parameters:
   ```yaml
   chain_id: 1
   block_range: 1000
   transaction_depth: 50
   ```

## Understanding Results

### Result Categories
- **Finding**: Technical details of the discovered issue
- **Impact**: Business impact of the finding
- **Remediation**: Steps to address the issue
- **References**: Related documentation and standards

### Result Analysis
1. Review vulnerability summary
2. Check AI-powered recommendations
3. Validate findings manually
4. Generate comprehensive report

### Report Sections
- Executive Summary
- Technical Details
- Proof of Concept
- Remediation Steps
- Risk Assessment

## Best Practices

### General Guidelines
1. Start with scope definition
2. Follow responsible disclosure
3. Document findings thoroughly
4. Validate findings manually
5. Test systematically

### Testing Workflow
1. Reconnaissance
   ```bash
   # Example workflow
   1. Initial system assessment
   2. Comprehensive scan
   3. Manual verification
   4. Documentation
   ```

2. Vulnerability Assessment
   - Use multiple tools
   - Cross-validate findings
   - Check for false positives

3. Documentation
   - Clear reproduction steps
   - Impact assessment
   - Mitigation recommendations

### Security Considerations
- Respect scope boundaries
- Avoid destructive testing
- Protect sensitive data
- Follow ethical guidelines

## Tips for Bug Bounty Success
1. Focus on high-impact vulnerabilities
2. Create detailed reports
3. Provide clear proof of concepts
4. Follow program guidelines
5. Stay updated with latest threats

Remember to always:
- Test in authorized scope only
- Follow responsible disclosure
- Document findings thoroughly
- Validate before reporting
- Keep tools updated
