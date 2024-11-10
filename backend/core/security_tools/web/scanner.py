from typing import Dict, List
import os
from ..base import SecurityTool
from datetime import datetime

class WebScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("web", config)

    async def setup(self) -> bool:
        """Install and configure web security tools"""
        try:
            # Update package list
            await self.execute_command(["sudo", "apt-get", "update"])

            # Install Java (required for Burp Suite and ZAP)
            await self.execute_command(["sudo", "apt-get", "install", "-y", "default-jre"])

            # Install SQLMap
            await self.execute_command(["sudo", "apt-get", "install", "-y", "sqlmap"])

            # Install Nikto
            await self.execute_command(["sudo", "apt-get", "install", "-y", "nikto"])

            # Install Masscan
            await self.execute_command(["sudo", "apt-get", "install", "-y", "masscan"])

            # Install Semgrep
            await self.execute_command(["pip3", "install", "semgrep"])

            # Install OWASP ZAP
            await self.execute_command([
                "wget", "https://github.com/zaproxy/zaproxy/releases/download/v2.14.0/ZAP_2.14.0_Linux.tar.gz"
            ])
            await self.execute_command(["tar", "-xf", "ZAP_2.14.0_Linux.tar.gz"])
            await self.execute_command(["sudo", "mv", "ZAP_2.14.0", "/opt/zaproxy"])
            await self.execute_command(["sudo", "ln", "-s", "/opt/zaproxy/zap.sh", "/usr/local/bin/zap"])
            await self.execute_command(["rm", "ZAP_2.14.0_Linux.tar.gz"])

            # Note: Burp Suite requires manual installation due to licensing

            return True
        except Exception as e:
            print(f"Failed to setup web security tools: {e}")
            return False

    async def scan(self, target: str, tool: str = None) -> Dict:
        """Run web security scan with specified tool"""
        results = {
            "tool": self.name,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": []
        }

        if tool == "sqlmap":
            stdout, stderr = await self.execute_command(["sqlmap", "-u", target, "--batch"])
            results["findings"].extend(self.parse_sqlmap_output(stdout))
        elif tool == "nikto":
            stdout, stderr = await self.execute_command(["nikto", "-h", target, "-Format", "json"])
            results["findings"].extend(self.parse_nikto_output(stdout))
        elif tool == "masscan":
            stdout, stderr = await self.execute_command(["masscan", target, "-p1-65535", "--rate=1000"])
            results["findings"].extend(self.parse_masscan_output(stdout))
        elif tool == "semgrep":
            stdout, stderr = await self.execute_command(["semgrep", "--config", "auto", target])
            results["findings"].extend(self.parse_semgrep_output(stdout))
        elif tool == "zap":
            # Start ZAP in daemon mode
            await self.execute_command(["zap", "-daemon", "-config", "api.key=12345"])
            # TODO: Implement ZAP API integration
            pass

        return results

    def parse_sqlmap_output(self, output: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            if "Parameter:" in line or "Type:" in line or "Title:" in line:
                findings.append({"detail": line.strip()})
        return findings

    def parse_nikto_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for item in data.get("vulnerabilities", []):
                findings.append({
                    "id": item.get("id"),
                    "message": item.get("message"),
                    "url": item.get("url")
                })
        except json.JSONDecodeError:
            pass
        return findings

    def parse_masscan_output(self, output: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            if "Discovered open port" in line:
                findings.append({"port": line.strip()})
        return findings

    def parse_semgrep_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for result in data.get("results", []):
                findings.append({
                    "rule": result.get("check_id"),
                    "message": result.get("extra", {}).get("message"),
                    "path": result.get("path"),
                    "line": result.get("start", {}).get("line")
                })
        except json.JSONDecodeError:
            pass
        return findings
