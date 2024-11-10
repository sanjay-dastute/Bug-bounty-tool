from typing import Dict, List
import json
import os
import aiohttp
from ..base import SecurityTool
from datetime import datetime

class MobSFScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("mobsf", config)
        self.api_key = config.get("api_key", "")
        self.host = config.get("host", "http://localhost:8000")
        self.headers = {"Authorization": self.api_key}

    async def setup(self) -> bool:
        """Install and configure MobSF"""
        try:
            # Check if Docker is installed
            stdout, stderr = await self.execute_command(["which", "docker"])
            if not stdout:
                # Install Docker
                await self.execute_command(["sudo", "apt-get", "update"])
                await self.execute_command([
                    "sudo", "apt-get", "install", "-y",
                    "docker.io"
                ])

            # Pull and run MobSF Docker container
            await self.execute_command([
                "docker", "run", "-d",
                "--name", "mobsf",
                "-p", "8000:8000",
                "opensecurity/mobile-security-framework-mobsf:latest"
            ])

            # Wait for service to start
            await self.execute_command(["sleep", "30"])

            # Get API key
            container_id = (await self.execute_command(["docker", "ps", "-q", "--filter", "name=mobsf"]))[0].strip()
            api_key = (await self.execute_command([
                "docker", "exec", container_id,
                "cat", "/home/mobsf/.MobSF/secret"
            ]))[0].strip()

            self.api_key = api_key
            self.headers = {"Authorization": api_key}
            return True

        except Exception as e:
            print(f"Failed to setup MobSF: {e}")
            return False

    async def scan(self, file_path: str) -> Dict:
        """Scan mobile application"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        async with aiohttp.ClientSession() as session:
            # Upload file
            upload_url = f"{self.host}/api/v1/upload"
            with open(file_path, 'rb') as f:
                files = {'file': f}
                async with session.post(upload_url, headers=self.headers, data=files) as response:
                    upload_data = await response.json()
                    if not upload_data.get("hash"):
                        raise Exception("Failed to upload file")

            file_hash = upload_data["hash"]

            # Start scan
            scan_url = f"{self.host}/api/v1/scan"
            scan_data = {
                "hash": file_hash,
                "scan_type": self._get_scan_type(file_path)
            }
            async with session.post(scan_url, headers=self.headers, json=scan_data) as response:
                scan_result = await response.json()

            # Get report
            report_url = f"{self.host}/api/v1/report_json"
            report_data = {"hash": file_hash}
            async with session.post(report_url, headers=self.headers, json=report_data) as response:
                report = await response.json()

            return {
                "tool": self.name,
                "target": file_path,
                "timestamp": datetime.utcnow().isoformat(),
                "findings": await self.parse_results(report),
                "raw_output": report
            }

    def _get_scan_type(self, file_path: str) -> str:
        """Determine scan type based on file extension"""
        ext = os.path.splitext(file_path)[1].lower()
        if ext == '.apk':
            return 'apk'
        elif ext == '.ipa':
            return 'ipa'
        elif ext == '.appx':
            return 'appx'
        raise ValueError(f"Unsupported file type: {ext}")

    async def parse_results(self, report: Dict) -> List[Dict]:
        """Parse MobSF scan results"""
        findings = []

        # Security Score
        if "security_score" in report:
            findings.append({
                "type": "security_score",
                "score": report["security_score"],
                "severity": "info"
            })

        # Vulnerabilities
        if "vulnerabilities" in report:
            for vuln_type, vulns in report["vulnerabilities"].items():
                for vuln in vulns:
                    finding = {
                        "type": "vulnerability",
                        "category": vuln_type,
                        "name": vuln.get("name", "Unknown"),
                        "severity": vuln.get("severity", "unknown"),
                        "description": vuln.get("description", ""),
                        "reference": vuln.get("ref", []),
                        "cvss": vuln.get("cvss", 0),
                        "cwe": vuln.get("cwe", "")
                    }
                    findings.append(finding)

        # Permissions
        if "permissions" in report:
            findings.append({
                "type": "permissions",
                "details": report["permissions"],
                "severity": "info"
            })

        # Code Analysis
        if "code_analysis" in report:
            for issue in report["code_analysis"]:
                finding = {
                    "type": "code_analysis",
                    "category": issue.get("category", "Unknown"),
                    "name": issue.get("name", "Unknown"),
                    "severity": issue.get("severity", "unknown"),
                    "description": issue.get("description", ""),
                    "file": issue.get("file", ""),
                    "line": issue.get("line", 0)
                }
                findings.append(finding)

        return findings

    async def cleanup(self):
        """Clean up MobSF resources"""
        try:
            await self.execute_command(["docker", "stop", "mobsf"])
            await self.execute_command(["docker", "rm", "mobsf"])
            return True
        except Exception as e:
            print(f"Failed to cleanup MobSF: {e}")
            return False
