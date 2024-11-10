from typing import Dict, List
import os
from ..base import SecurityTool
from datetime import datetime

class CloudScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("cloud", config)

    async def setup(self) -> bool:
        """Install and configure cloud security tools"""
        try:
            # Update package list
            await self.execute_command(["sudo", "apt-get", "update"])

            # Install Python dependencies
            await self.execute_command(["pip3", "install", "cloudsploit"])
            await self.execute_command(["pip3", "install", "scout-suite"])
            await self.execute_command(["pip3", "install", "prowler"])

            # Install Azure CLI (required for AzureDumper)
            await self.execute_command([
                "curl", "-sL", "https://aka.ms/InstallAzureCLIDeb",
                "|", "sudo", "bash"
            ])

            # Install AzureDumper
            await self.execute_command([
                "git", "clone", "https://github.com/microsoft/AzureDumper.git",
                "/opt/azuredumper"
            ])
            await self.execute_command([
                "pip3", "install", "-r", "/opt/azuredumper/requirements.txt"
            ])

            return True
        except Exception as e:
            print(f"Failed to setup cloud security tools: {e}")
            return False

    async def scan(self, provider: str, credentials: Dict) -> Dict:
        """Run cloud security scan with specified provider"""
        results = {
            "tool": self.name,
            "provider": provider,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": []
        }

        if provider == "aws":
            # Run CloudSploit
            os.environ["AWS_ACCESS_KEY_ID"] = credentials.get("aws_access_key")
            os.environ["AWS_SECRET_ACCESS_KEY"] = credentials.get("aws_secret_key")
            stdout, stderr = await self.execute_command(["cloudsploit", "scan"])
            results["findings"].extend(self.parse_cloudsploit_output(stdout))

            # Run Scout Suite
            stdout, stderr = await self.execute_command(["scout", "aws"])
            results["findings"].extend(self.parse_scout_output(stdout))

            # Run Prowler
            stdout, stderr = await self.execute_command(["prowler", "aws"])
            results["findings"].extend(self.parse_prowler_output(stdout))

        elif provider == "azure":
            # Run AzureDumper
            os.environ["AZURE_CLIENT_ID"] = credentials.get("client_id")
            os.environ["AZURE_CLIENT_SECRET"] = credentials.get("client_secret")
            os.environ["AZURE_TENANT_ID"] = credentials.get("tenant_id")
            stdout, stderr = await self.execute_command([
                "python3", "/opt/azuredumper/azuredumper.py"
            ])
            results["findings"].extend(self.parse_azuredumper_output(stdout))

        return results

    def parse_cloudsploit_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for finding in data:
                findings.append({
                    "service": finding.get("service"),
                    "region": finding.get("region"),
                    "resource": finding.get("resource"),
                    "message": finding.get("message")
                })
        except json.JSONDecodeError:
            pass
        return findings

    def parse_scout_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for service in data.get("services", []):
                for finding in service.get("findings", []):
                    findings.append({
                        "service": service.get("name"),
                        "description": finding.get("description"),
                        "resource": finding.get("resource")
                    })
        except json.JSONDecodeError:
            pass
        return findings

    def parse_prowler_output(self, output: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            if "[INFO]" in line or "[WARN]" in line:
                findings.append({"detail": line.strip()})
        return findings

    def parse_azuredumper_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for resource in data:
                findings.append({
                    "type": resource.get("type"),
                    "name": resource.get("name"),
                    "location": resource.get("location"),
                    "properties": resource.get("properties")
                })
        except json.JSONDecodeError:
            pass
        return findings
