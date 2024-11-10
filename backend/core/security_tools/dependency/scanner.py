from typing import Dict, List
import os
import json
from ..base import SecurityTool
from datetime import datetime

class DependencyScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("dependency", config)
        self.snyk_token = config.get("snyk_token", "")
        self.whitesource_key = config.get("whitesource_key", "")

    async def setup(self) -> bool:
        """Install and configure dependency scanning tools"""
        try:
            # Update package list
            await self.execute_command(["sudo", "apt-get", "update"])

            # Install Node.js (required for Snyk)
            await self.execute_command(["curl", "-fsSL", "https://deb.nodesource.com/setup_lts.x", "|", "sudo", "-E", "bash", "-"])
            await self.execute_command(["sudo", "apt-get", "install", "-y", "nodejs"])

            # Install Snyk
            await self.execute_command(["sudo", "npm", "install", "-g", "snyk"])

            # Install WhiteSource Unified Agent
            await self.execute_command([
                "curl", "-LJO",
                "https://unified-agent.s3.amazonaws.com/wss-unified-agent.jar"
            ])
            await self.execute_command([
                "sudo", "mv", "wss-unified-agent.jar", "/usr/local/bin/"
            ])

            return True
        except Exception as e:
            print(f"Failed to setup dependency scanning tools: {e}")
            return False

    async def scan(self, target: str, tool: str = None) -> Dict:
        """Run dependency security scan with specified tool"""
        results = {
            "tool": self.name,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": []
        }

        if tool == "snyk":
            os.environ["SNYK_TOKEN"] = self.snyk_token
            stdout, stderr = await self.execute_command(["snyk", "test", "--json", target])
            results["findings"].extend(self.parse_snyk_output(stdout))
        elif tool == "whitesource":
            config_file = self.create_whitesource_config(target)
            stdout, stderr = await self.execute_command([
                "java", "-jar", "/usr/local/bin/wss-unified-agent.jar",
                "-c", config_file,
                "-apiKey", self.whitesource_key,
                "-d", target
            ])
            results["findings"].extend(self.parse_whitesource_output(stdout))

        return results

    def parse_snyk_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for vuln in data.get("vulnerabilities", []):
                findings.append({
                    "package": vuln.get("package"),
                    "title": vuln.get("title"),
                    "description": vuln.get("description"),
                    "version": vuln.get("version"),
                    "fixedIn": vuln.get("fixedIn")
                })
        except json.JSONDecodeError:
            pass
        return findings

    def parse_whitesource_output(self, output: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            if "Found vulnerability" in line:
                findings.append({"detail": line.strip()})
        return findings

    def create_whitesource_config(self, target: str) -> str:
        """Create WhiteSource configuration file"""
        config = {
            "apiKey": self.whitesource_key,
            "projectName": os.path.basename(target),
            "productName": "Bug Bounty Tool",
            "wss.url": "https://saas.whitesourcesoftware.com/agent"
        }

        config_path = "/tmp/whitesource-config.json"
        with open(config_path, 'w') as f:
            json.dump(config, f, indent=2)

        return config_path
