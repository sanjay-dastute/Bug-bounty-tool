from typing import Dict, List
import json
from ..base import SecurityTool
from datetime import datetime

class NmapScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("nmap", config)
        self.scan_types = {
            "quick": ["-sV", "-sC", "-F"],
            "full": ["-sV", "-sC", "-p-", "--min-rate", "1000"],
            "vuln": ["-sV", "-sC", "--script", "vuln"]
        }

    async def setup(self) -> bool:
        """Install and configure Nmap"""
        try:
            stdout, stderr = await self.execute_command(["which", "nmap"])
            if stdout:
                return True

            # Install Nmap if not found
            stdout, stderr = await self.execute_command(["sudo", "apt-get", "update"])
            stdout, stderr = await self.execute_command(["sudo", "apt-get", "install", "-y", "nmap"])
            return bool(await self.execute_command(["which", "nmap"])[0])
        except Exception as e:
            print(f"Failed to setup Nmap: {e}")
            return False

    async def scan(self, target: str, scan_type: str = "quick") -> Dict:
        """Execute Nmap scan with specified options"""
        if scan_type not in self.scan_types:
            scan_type = "quick"

        command = ["nmap"] + self.scan_types[scan_type] + [target]
        stdout, stderr = await self.execute_command(command)

        results = await self.parse_results(stdout)
        return {
            "tool": self.name,
            "target": target,
            "scan_type": scan_type,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": results,
            "raw_output": stdout,
            "errors": stderr
        }

    async def parse_results(self, raw_output: str) -> List[Dict]:
        """Parse Nmap scan results"""
        findings = []
        current_port = None
        current_service = None

        for line in raw_output.split('\n'):
            line = line.strip()

            # Parse port information
            if '/tcp' in line or '/udp' in line:
                parts = line.split()
                if len(parts) >= 3:
                    current_port = {
                        "port": parts[0],
                        "state": parts[1],
                        "service": parts[2],
                        "version": " ".join(parts[3:]) if len(parts) > 3 else "",
                        "vulnerabilities": []
                    }
                    findings.append(current_port)
                    current_service = current_port

            # Parse vulnerability information
            elif current_service and '|' in line:
                vuln_info = line.split('|')[1].strip()
                if vuln_info:
                    current_service["vulnerabilities"].append({
                        "type": "potential_vulnerability",
                        "description": vuln_info
                    })

        return findings

    async def get_os_detection(self, target: str) -> Dict:
        """Perform OS detection scan"""
        command = ["nmap", "-O", "--osscan-guess", target]
        stdout, stderr = await self.execute_command(command)

        os_info = {
            "os_match": [],
            "raw_output": stdout
        }

        for line in stdout.split('\n'):
            if "OS guess:" in line:
                os_guess = line.split("OS guess:")[1].strip()
                accuracy = os_guess.split(")")[-1].strip().replace("%", "")
                os_name = os_guess.split("(")[0].strip()
                os_info["os_match"].append({
                    "name": os_name,
                    "accuracy": accuracy
                })

        return os_info

    async def get_service_versions(self, target: str) -> Dict:
        """Perform service version detection"""
        command = ["nmap", "-sV", "--version-intensity", "5", target]
        stdout, stderr = await self.execute_command(command)

        return {
            "services": await self.parse_results(stdout),
            "raw_output": stdout
        }
