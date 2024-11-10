from typing import Dict, List
import os
import json
from ..base import SecurityTool
from datetime import datetime

class SmartContractScanner(SecurityTool):
    def __init__(self, config: Dict):
        super().__init__("smart_contract", config)

    async def setup(self) -> bool:
        """Install and configure smart contract analysis tools"""
        try:
            # Update package list
            await self.execute_command(["sudo", "apt-get", "update"])

            # Install Python dependencies
            await self.execute_command(["pip3", "install", "slither-analyzer"])
            await self.execute_command(["pip3", "install", "manticore"])

            return True
        except Exception as e:
            print(f"Failed to setup smart contract analysis tools: {e}")
            return False

    async def scan(self, target: str, tool: str = None) -> Dict:
        """Run smart contract security scan with specified tool"""
        results = {
            "tool": self.name,
            "target": target,
            "timestamp": datetime.utcnow().isoformat(),
            "findings": []
        }

        if tool == "slither":
            stdout, stderr = await self.execute_command(["slither", target, "--json", "-"])
            results["findings"].extend(self.parse_slither_output(stdout))
        elif tool == "manticore":
            stdout, stderr = await self.execute_command(["manticore", target, "--workspace", "/tmp/manticore"])
            results["findings"].extend(self.parse_manticore_output(stdout))

        return results

    def parse_slither_output(self, output: str) -> List[Dict]:
        findings = []
        try:
            data = json.loads(output)
            for detector in data.get("results", {}).get("detectors", []):
                findings.append({
                    "check": detector.get("check"),
                    "description": detector.get("description"),
                    "contract": detector.get("contract"),
                    "function": detector.get("function")
                })
        except json.JSONDecodeError:
            pass
        return findings

    def parse_manticore_output(self, output: str) -> List[Dict]:
        findings = []
        for line in output.split('\n'):
            if "found" in line.lower() and "vulnerability" in line.lower():
                findings.append({"detail": line.strip()})
        return findings
